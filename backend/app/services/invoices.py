"""Lógica de negocio de facturación electrónica con Factus.

Convierte un pedido (Order) en el payload que espera POST /{v}/bills/validate,
persiste el resultado en la tabla `invoices` y expone descargas de PDF/XML.

Notas de la API V2 (la V1 usa IDs y precios con IVA incluido):
- El precio de cada ítem va SIN IVA (base gravable), máximo 2 decimales.
- El total lo calcula Factus: Σ(price × qty × (1-descuento)) × (1+IVA).
- payment_details[].amount debe ser igual al total calculado por Factus;
  si difiere, la API responde 422 con "Esperado: X" y se reintenta corrigiendo.
"""

from __future__ import annotations

import json
import re
from datetime import UTC, datetime
from decimal import ROUND_HALF_UP, Decimal
from typing import Any

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.exceptions import AppException
from app.models.invoice import Invoice, InvoiceStatus
from app.models.order import Order, OrderStatus
from app.models.user import User
from app.schemas.invoice import InvoiceCreate
from app.services import factus
from app.services.orders import get_order_for_user

# Valores estándar DIAN/Factus (códigos de tablas de referencia)
UNIT_MEASURE_CODE = "94"  # unidad
STANDARD_CODE = "999"  # Estándar de adopción del contribuyente
IVA_CODE = "01"  # tributo IVA
TWO_PLACES = Decimal("0.01")


def _default_tax_rate() -> Decimal:
    return Decimal(settings.factus_default_tax_rate or "0")


def _base_price(tax_included_price: Decimal, rate_pct: Decimal) -> Decimal:
    """Convierte un precio con IVA incluido a precio base (sin IVA), 2 decimales."""
    factor = Decimal("1") + rate_pct / Decimal("100")
    return (tax_included_price / factor).quantize(TWO_PLACES, rounding=ROUND_HALF_UP)


def _products_discount_rate(order: Order) -> Decimal:
    """Porcentaje uniforme de descuento (cupón) repartido entre los ítems con IVA.

    La API V2 no acepta allowance_charges como la V1; el descuento del cupón
    se aplica como discount_rate a nivel de cada línea de producto.
    """
    discount = Decimal(order.discount_amount or 0)
    if discount <= 0 or not order.coupon_code:
        return Decimal("0")
    subtotal = sum((Decimal(i.unit_price) * i.quantity for i in order.items), Decimal("0"))
    if subtotal <= 0:
        return Decimal("0")
    rate = (discount / subtotal * Decimal("100")).quantize(TWO_PLACES, rounding=ROUND_HALF_UP)
    return min(rate, Decimal("100"))


def _estimate_factus_total(order: Order, tax_rate_pct: Decimal, discount_rate_pct: Decimal) -> Decimal:
    """Replica el cálculo que hace Factus para el total del documento.

    total = Σ( price_base × qty × (1 - desc%) × (1 + iva%) ) + envío,
    redondeado al final a 2 decimales.
    """
    total = Decimal("0")
    for item in order.items:
        base = _base_price(Decimal(item.unit_price), tax_rate_pct)
        line = base * Decimal(item.quantity)
        line *= Decimal("1") - discount_rate_pct / Decimal("100")
        line *= Decimal("1") + tax_rate_pct / Decimal("100")
        total += line
    total += Decimal(order.shipping_cost or 0)  # línea exenta de IVA
    return total.quantize(TWO_PLACES, rounding=ROUND_HALF_UP)


def build_bill_payload(order: Order, options: InvoiceCreate) -> dict[str, Any]:
    """Arma el JSON que espera POST /bills/validate (API v2) a partir del pedido."""
    tax_rate_pct = _default_tax_rate()
    discount_rate_pct = _products_discount_rate(order)
    tax_rate_str = f"{tax_rate_pct:.2f}"

    items: list[dict[str, Any]] = []
    for item in order.items:
        base_price = _base_price(Decimal(item.unit_price), tax_rate_pct)
        items.append(
            {
                "code_reference": f"PROD-{item.product_id}" if item.product_id else f"ITEM-{item.id}",
                "name": item.product_name[:200],
                "quantity": f"{Decimal(item.quantity):.2f}",
                "discount_rate": f"{discount_rate_pct:.2f}",
                "price": f"{base_price:.2f}",
                "unit_measure_code": UNIT_MEASURE_CODE,
                "standard_code": STANDARD_CODE,
                "taxes": [{"code": IVA_CODE, "rate": tax_rate_str}],
            }
        )

    if order.shipping_cost and order.shipping_cost > 0:
        items.append(
            {
                "code_reference": "ENVIO",
                "name": f"Envío ({order.shipping_method or 'estandar'})",
                "quantity": "1.00",
                "discount_rate": "0.00",
                "price": f"{Decimal(order.shipping_cost):.2f}",
                "unit_measure_code": UNIT_MEASURE_CODE,
                "standard_code": STANDARD_CODE,
                "taxes": [{"code": IVA_CODE, "rate": "0.00"}],
            }
        )

    customer_input = options.customer
    customer: dict[str, Any] = {
        "identification_document_code": customer_input.identification_document_code,
        "identification": customer_input.identification,
        "legal_organization_code": customer_input.legal_organization_code,
        "tribute_code": customer_input.tribute_code,
        "names": customer_input.names or order.user.full_name,
        "email": str(customer_input.email) if customer_input.email else order.user.email,
    }
    optional_fields = ("dv", "company", "trade_name", "address", "phone", "municipality_code")
    for field in optional_fields:
        value = getattr(customer_input, field)
        if value is not None:
            customer[field] = value

    estimated_total = _estimate_factus_total(order, tax_rate_pct, discount_rate_pct)

    payload: dict[str, Any] = {
        "document": "01",  # Factura electrónica de venta
        "reference_code": f"order-{order.id}",
        "customer": customer,
        "items": items,
        "payment_details": [
            {
                "payment_form": options.payment_form,
                "payment_method_code": str(options.payment_method_code),
                "amount": f"{estimated_total:.2f}",
            }
        ],
        "send_email": options.send_email,
    }

    if settings.factus_numbering_range_id is not None:
        payload["numbering_range_id"] = settings.factus_numbering_range_id

    if options.observation:
        payload["observation"] = options.observation

    return payload


_EXPECTED_TOTAL_RE = re.compile(r"Esperado:\s*([\d.,]+)")


def _parse_expected_total(errors: list[str]) -> Decimal | None:
    """Extrae 'Esperado: 45,600.00' de un error 422 de payment_details.

    Factus formatea con coma como separador de miles y punto decimal.
    """
    for text in errors:
        match = _EXPECTED_TOTAL_RE.search(text)
        if match:
            raw = match.group(1).strip().replace(",", "")
            try:
                return Decimal(raw)
            except Exception:  # noqa: BLE001
                return None
    return None


def _get_invoice_by_order(db: Session, order_id: int) -> Invoice | None:
    return db.scalar(select(Invoice).where(Invoice.order_id == order_id))


def _mark_failed(db: Session, invoice: Invoice | None, message: str, errors: list[str]) -> None:
    if invoice is None:
        return
    invoice.status = InvoiceStatus.FAILED
    invoice.error_message = "; ".join(errors) if errors else message
    db.add(invoice)
    db.commit()


def create_invoice_for_order(db: Session, user: User, order_id: int, options: InvoiceCreate) -> Invoice:
    """Genera y valida la factura electrónica del pedido en Factus.

    Idempotencia: si el pedido ya tiene una factura vigente se devuelve esa.
    Si existe un intento fallido previo, se elimina en Factus y se reintenta.
    Si Factus rechaza por desajuste de centavos en payment_details ("Esperado: X"),
    se reintenta una vez con el total exacto que reporta la API.
    """
    order = get_order_for_user(db, user, order_id)
    if order.status == OrderStatus.CANCELLED:
        raise AppException(status_code=400, message="No se puede facturar un pedido cancelado")

    existing = _get_invoice_by_order(db, order.id)
    if existing and existing.status in (InvoiceStatus.PENDING, InvoiceStatus.VALIDATED):
        return existing

    reference_code = f"order-{order.id}"
    if existing and existing.status == InvoiceStatus.FAILED:
        # La API exige eliminar la referencia antes de volver a crearla (error 409)
        try:
            factus.destroy_bill(reference_code)
        except AppException:
            pass  # puede no existir aún en Factus; se procede con la creación

    payload = build_bill_payload(order, options)

    try:
        try:
            response = factus.validate_bill(payload)
        except AppException as exc:
            expected = _parse_expected_total(list(exc.errors))
            if expected is None or not payload.get("payment_details"):
                raise
            payload["payment_details"][0]["amount"] = f"{expected:.2f}"
            response = factus.validate_bill(payload)
    except AppException as exc:
        fresh = _get_invoice_by_order(db, order.id)
        _mark_failed(db, fresh, exc.message, list(exc.errors))
        raise

    data = response.get("data") or {}
    validated = data.get("is_validated")
    if validated is None:
        validated = (data.get("bill") or {}).get("status") == 1
    status = InvoiceStatus.VALIDATED if validated else InvoiceStatus.PENDING

    if existing is None:
        existing = Invoice(order_id=order.id, reference_code=reference_code)
    existing.bill_number = data.get("number")
    existing.cufe = data.get("cufe")
    existing.qr_url = data.get("qr")
    existing.status = status
    existing.total = Decimal(data.get("total") or payload["payment_details"][0]["amount"])
    existing.customer_identification = (data.get("customer") or {}).get("identification")
    existing.error_message = None
    existing.factus_response = json.dumps(response, ensure_ascii=False)[:10000]
    existing.validated_at = datetime.now(UTC) if status == InvoiceStatus.VALIDATED else None

    db.add(existing)
    db.commit()
    db.refresh(existing)
    return existing


def get_invoice_for_order(db: Session, user: User, order_id: int) -> Invoice:
    order = get_order_for_user(db, user, order_id)
    invoice = _get_invoice_by_order(db, order.id)
    if invoice is None:
        raise AppException(status_code=404, message="El pedido no tiene factura electrónica")
    return invoice


def get_invoice_for_download(db: Session, user: User, bill_number: str) -> Invoice:
    """Valida permisos sobre la factura identificada por su número Factus."""
    invoice = db.scalar(select(Invoice).where(Invoice.bill_number == bill_number))
    if invoice is None:
        raise AppException(status_code=404, message="Factura no encontrada")
    order = db.get(Order, invoice.order_id)
    if order is None or (user.role.name != "ADMIN" and order.user_id != user.id):
        raise AppException(status_code=404, message="Factura no encontrada")
    return invoice


def delete_invoice(db: Session, user: User, order_id: int) -> Invoice:
    """Elimina en Factus una factura NO validada y borra el registro local."""
    invoice = get_invoice_for_order(db, user, order_id)
    if invoice.status == InvoiceStatus.VALIDATED:
        raise AppException(
            status_code=400,
            message="La factura ya fue validada por la DIAN; debe emitirse una nota crédito",
        )
    try:
        factus.destroy_bill(invoice.reference_code)
    except AppException as exc:
        # Si Factus ya no la tiene (o nunca llegó a crearse), el borrado local es válido
        if "no encontrad" not in exc.message.lower() and "not found" not in exc.message.lower():
            raise
    db.delete(invoice)
    db.commit()
    return invoice
