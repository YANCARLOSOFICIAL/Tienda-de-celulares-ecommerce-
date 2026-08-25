"""Pruebas de la integración con Factus (cliente HTTP y endpoints /api/invoices).

Factus se simula con httpx.MockTransport: no se hacen peticiones reales.
"""

import json
from base64 import b64decode, b64encode
from decimal import Decimal
from urllib.parse import parse_qs

import httpx
import pytest

from app.core.config import settings
from app.models.invoice import InvoiceStatus
from app.models.order import Order, OrderItem
from app.models.user import User
from app.services import factus
from tests.conftest import register_and_login
from tests.test_orders import add_to_cart
from tests.test_products import create_product

FAKE_BILL_NUMBER = "SETP990000001"
FAKE_CUFE = "cufe-" + "a" * 32


@pytest.fixture
def mock_factus(monkeypatch):
    """Configura credenciales falsas y un servidor Factus simulado.

    Devuelve la lista de llamadas registradas: tuplas (método, ruta, cuerpo).
    """
    monkeypatch.setattr(settings, "factus_client_id", "test-client-id")
    monkeypatch.setattr(settings, "factus_client_secret", "test-client-secret")
    monkeypatch.setattr(settings, "factus_username", "sandbox@tiendacell.com")
    monkeypatch.setattr(settings, "factus_password", "secret")
    monkeypatch.setattr(settings, "factus_numbering_range_id", 4)

    calls: list[tuple[str, str, dict]] = []
    token_requests = {"count": 0}

    def _bill_payload() -> dict:
        return {
            "status": "Created",
            "message": f"Documento {FAKE_BILL_NUMBER} registrado y validado",
            "data": {
                "reference_code": "order-1",
                "number": FAKE_BILL_NUMBER,
                "cufe": FAKE_CUFE,
                "qr": None,
                "is_validated": True,
                "validated_at": "25-08-2026 10:00:00 AM",
                "customer": {"identification": "1020304050"},
                "totals": {},
            },
        }

    def handler(request: httpx.Request) -> httpx.Response:
        body = {}
        if request.content:
            parsed = parse_qs(request.content.decode())
            body = {k: v[0] for k, v in parsed.items()}
        calls.append((request.method, request.url.path, body))

        if request.url.path == "/oauth/token":
            assert body.get("client_id") == "test-client-id"
            assert body.get("client_secret") == "test-client-secret"
            token_requests["count"] += 1
            return httpx.Response(
                200,
                json={
                    "token_type": "Bearer",
                    "expires_in": 3600,
                    "access_token": f"access-token-{token_requests['count']}",
                    "refresh_token": "refresh-token-1",
                },
            )
        auth = request.headers.get("Authorization", "")
        if not auth.startswith("Bearer access-token-"):
            return httpx.Response(401, json={"message": "Unauthenticated."})

        if request.method == "POST" and request.url.path == "/v2/bills/validate":
            payload = json.loads(request.content)
            assert payload["reference_code"].startswith("order-")
            return httpx.Response(201, json=_bill_payload())

        if request.method == "GET" and request.url.path == f"/v2/bills/{FAKE_BILL_NUMBER}":
            return httpx.Response(200, json=_bill_payload())

        if request.method == "DELETE" and request.url.path.startswith("/v2/bills/destroy/reference/"):
            return httpx.Response(200, json={"status": "OK", "message": "eliminado"})

        if request.method == "GET" and request.url.path == f"/v2/bills/{FAKE_BILL_NUMBER}/download-pdf":
            encoded = b64encode(b"%PDF-1.4 fake pdf").decode()
            return httpx.Response(
                200,
                json={"data": {"file_name": "factura.pdf", "pdf_base_64_encoded": encoded}},
            )

        if request.method == "GET" and request.url.path == f"/v2/bills/{FAKE_BILL_NUMBER}/download-xml":
            encoded = b64encode(b"<Invoice/> fake xml").decode()
            return httpx.Response(
                200,
                json={"data": {"file_name": "factura.xml", "xml_base_64_encoded": encoded}},
            )

        if request.method == "GET" and request.url.path == "/v2/numbering-ranges":
            return httpx.Response(
                200,
                json={
                    "data": {
                        "data": [
                            {"id": 4, "prefix": "SETP", "current": 990000875, "is_active": 1}
                        ]
                    }
                },
            )

        return httpx.Response(404, json={"message": "Not found"})

    client = httpx.Client(transport=httpx.MockTransport(handler), base_url="https://mock.factus.test")
    factus.set_http_client(client)
    yield calls
    factus.set_http_client(None)


# ---------------------------------------------------------------------------
# Cliente HTTP (tokens y descargas)
# ---------------------------------------------------------------------------


def test_token_is_requested_once_and_cached(mock_factus):
    assert factus.get_access_token() == "access-token-1"
    assert factus.get_access_token() == "access-token-1"
    oauth_calls = [c for c in mock_factus if c[1] == "/oauth/token"]
    assert len(oauth_calls) == 1


def test_expired_token_triggers_refresh_grant(mock_factus):
    assert factus.get_access_token() == "access-token-1"
    calls_after_first = len(mock_factus)
    factus.force_refresh_token()
    second = factus.get_access_token()
    assert second == "access-token-2"
    grants = [c for c in mock_factus[calls_after_first:] if c[1] == "/oauth/token"]
    assert any(c[2].get("grant_type") == "refresh_token" for c in grants)


def test_download_pdf_decodes_base64(mock_factus):
    file_name, content = factus.download_pdf(FAKE_BILL_NUMBER)
    assert file_name == "factura.pdf"
    assert content.startswith(b"%PDF")


def test_download_xml_decodes_base64(mock_factus):
    file_name, content = factus.download_xml(FAKE_BILL_NUMBER)
    assert file_name == "factura.xml"
    assert content.startswith(b"<Invoice")


def test_not_configured_raises(monkeypatch):
    monkeypatch.setattr(settings, "factus_client_id", None)
    from app.core.exceptions import AppException

    with pytest.raises(AppException) as exc_info:
        factus.get_access_token()
    assert "no está configurado" in exc_info.value.message


# ---------------------------------------------------------------------------
# Construcción del payload de factura
# ---------------------------------------------------------------------------


def test_build_bill_payload_structure(monkeypatch):
    from app.schemas.invoice import CustomerData, InvoiceCreate
    from app.services.invoices import build_bill_payload

    monkeypatch.setattr(settings, "factus_numbering_range_id", 4)

    user = User(full_name="Alan Turing", email="alan@test.com")
    order = Order(
        id=42,
        total=Decimal("2099.00"),
        shipping_cost=Decimal("99.00"),
        shipping_method="express",
        coupon_code="BIENVENIDA",
        discount_amount=Decimal("100.00"),
        user=user,
    )
    order.items = [
        OrderItem(
            id=1,
            product_id=7,
            product_name="Celular X",
            unit_price=Decimal("1000.00"),
            quantity=2,
            subtotal=Decimal("2000.00"),
        ),
    ]

    bill = build_bill_payload(order, InvoiceCreate(customer=CustomerData(identification="1020304050")))

    assert bill["document"] == "01"
    assert bill["reference_code"] == "order-42"
    assert bill["numbering_range_id"] == 4
    assert bill["customer"]["names"] == "Alan Turing"
    assert bill["customer"]["email"] == "alan@test.com"
    assert bill["customer"]["identification"] == "1020304050"
    assert bill["customer"]["identification_document_code"] == "13"
    assert len(bill["items"]) == 2  # producto + envío

    # V2: precio base sin IVA (1000 / 1.19 redondeado a 840.34) y descuento de cupón por ítem
    product_item = bill["items"][0]
    assert product_item["code_reference"] == "PROD-7"
    assert product_item["quantity"] == "2.00"
    assert product_item["price"] == "840.34"
    assert product_item["discount_rate"] == "5.00"  # cupón 100 sobre subtotal 2000
    assert product_item["taxes"] == [{"code": "01", "rate": "19.00"}]

    shipping_item = bill["items"][1]
    assert shipping_item["code_reference"] == "ENVIO"
    assert shipping_item["price"] == "99.00"
    assert shipping_item["taxes"] == [{"code": "01", "rate": "0.00"}]
    assert shipping_item["discount_rate"] == "0.00"

    # Total estimado con la fórmula de Factus: 840.34×2×0.95×1.19 + 99 = 1999.01
    assert "allowance_charges" not in bill  # V2 no usa allowance_charges
    assert bill["payment_details"][0]["amount"] == "1999.01"
    assert bill["payment_details"][0]["payment_form"] == "1"
    assert bill["payment_details"][0]["payment_method_code"] == "10"


def test_build_bill_payload_retries_expected_total(monkeypatch):
    """El parser extrae 'Esperado: X' del error 422 de Factus."""
    from app.services.invoices import _parse_expected_total

    assert _parse_expected_total(["payment_details: La suma ... Esperado: 45,600.00 - Enviado: ..."]) == Decimal("45600.00")
    assert _parse_expected_total(["otro error"]) is None


# ---------------------------------------------------------------------------
# End-to-end vía API (/api/invoices)
# ---------------------------------------------------------------------------


def _create_order(client, admin_token, user_token) -> int:
    product = create_product(client, admin_token, price="1000.00", stock=10).json()["data"]["id"]
    add_to_cart(client, user_token, product, quantity=2)
    response = client.post("/api/orders", headers={"Authorization": f"Bearer {user_token}"})
    assert response.status_code == 201
    return response.json()["data"]["id"]


INVOICE_BODY = {
    "customer": {"identification": "1020304050", "names": "Usuario Prueba", "email": "user@test.com"}
}


def test_create_invoice_for_order(client, admin_token, user_token, mock_factus):
    order_id = _create_order(client, admin_token, user_token)

    response = client.post(
        f"/api/invoices/orders/{order_id}",
        json=INVOICE_BODY,
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert response.status_code == 201, response.text
    data = response.json()["data"]
    assert data["bill_number"] == FAKE_BILL_NUMBER
    assert data["cufe"] == FAKE_CUFE
    assert data["status"] == InvoiceStatus.VALIDATED.value
    assert data["reference_code"] == f"order-{order_id}"


def test_create_invoice_is_idempotent(client, admin_token, user_token, mock_factus):
    order_id = _create_order(client, admin_token, user_token)
    headers = {"Authorization": f"Bearer {admin_token}"}

    first = client.post(f"/api/invoices/orders/{order_id}", json=INVOICE_BODY, headers=headers)
    second = client.post(f"/api/invoices/orders/{order_id}", json=INVOICE_BODY, headers=headers)

    assert first.status_code == 201
    assert second.status_code == 201
    validate_calls = [c for c in mock_factus if c[:2] == ("POST", "/v2/bills/validate")]
    assert len(validate_calls) == 1  # la segunda llamada reutiliza la factura existente
    assert second.json()["data"]["bill_number"] == FAKE_BILL_NUMBER


def test_invoice_requires_admin_to_create(client, admin_token, user_token, mock_factus):
    order_id = _create_order(client, admin_token, user_token)
    response = client.post(
        f"/api/invoices/orders/{order_id}",
        json=INVOICE_BODY,
        headers={"Authorization": f"Bearer {user_token}"},
    )
    assert response.status_code == 403


def test_owner_can_get_invoice_and_download_pdf(client, admin_token, user_token, mock_factus):
    order_id = _create_order(client, admin_token, user_token)
    client.post(
        f"/api/invoices/orders/{order_id}",
        json=INVOICE_BODY,
        headers={"Authorization": f"Bearer {admin_token}"},
    )

    got = client.get(
        f"/api/invoices/orders/{order_id}", headers={"Authorization": f"Bearer {user_token}"}
    )
    assert got.status_code == 200
    bill_number = got.json()["data"]["bill_number"]

    pdf = client.get(
        f"/api/invoices/{bill_number}/pdf", headers={"Authorization": f"Bearer {user_token}"}
    )
    assert pdf.status_code == 200
    assert pdf.headers["content-type"].startswith("application/pdf")
    assert pdf.content.startswith(b"%PDF")


def test_other_user_cannot_download_invoice(client, admin_token, user_token, mock_factus):
    order_id = _create_order(client, admin_token, user_token)
    client.post(
        f"/api/invoices/orders/{order_id}",
        json=INVOICE_BODY,
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    other_token = register_and_login(client, "other@test.com", "OtherPass123!")

    denied = client.get(
        "/api/invoices/SETP990000001/pdf", headers={"Authorization": f"Bearer {other_token}"}
    )
    assert denied.status_code == 404


def test_delete_validated_invoice_rejected(client, admin_token, user_token, mock_factus):
    order_id = _create_order(client, admin_token, user_token)
    client.post(
        f"/api/invoices/orders/{order_id}",
        json=INVOICE_BODY,
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    response = client.delete(
        f"/api/invoices/orders/{order_id}", headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 400
    assert "nota crédito" in response.json()["message"]


def test_numbering_ranges_requires_admin(client, user_token, mock_factus):
    response = client.get(
        "/api/invoices/numbering-ranges", headers={"Authorization": f"Bearer {user_token}"}
    )
    assert response.status_code == 403
