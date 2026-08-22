from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.exceptions import AppException
from app.models.order import Order
from app.models.payment import Payment, PaymentStatus
from app.models.user import User


def _has_mercadopago_credentials() -> bool:
    return bool(getattr(settings, "mercadopago_access_token", None))


def create_payment(db: Session, user: User, order_id: int) -> Payment:
    order = db.get(Order, order_id)
    if order is None:
        raise AppException(status_code=404, message="Pedido no encontrado")
    if order.user_id != user.id:
        raise AppException(status_code=403, message="No tienes permiso para pagar este pedido")

    existing = db.scalar(select(Payment).where(Payment.order_id == order_id))
    if existing and existing.status == PaymentStatus.APPROVED:
        raise AppException(status_code=400, message="El pedido ya esta pagado")
    if existing and existing.status == PaymentStatus.PENDING:
        return existing

    checkout_url = None
    external_id = None

    if _has_mercadopago_credentials():
        try:
            import mercadopago
            sdk = mercadopago.SDK(settings.mercadopago_access_token)
            preference_data = {
                "items": [
                    {
                        "title": f"Pedido #{order.id}",
                        "quantity": 1,
                        "unit_price": float(order.total),
                        "currency_id": "MXN",
                    }
                ],
                "external_reference": str(order.id),
                "back_urls": {
                    "success": f"{settings.frontend_url}/orders/{order.id}",
                    "failure": f"{settings.frontend_url}/orders/{order.id}",
                    "pending": f"{settings.frontend_url}/orders/{order.id}",
                },
            }
            result = sdk.preference().create(preference_data)
            external_id = result.get("id")
            checkout_url = result.get("init_point")
        except Exception:
            pass

    payment = Payment(
        order_id=order.id,
        external_id=external_id,
        status=PaymentStatus.PENDING,
        amount=order.total,
        currency="MXN",
        checkout_url=checkout_url,
    )
    db.add(payment)
    db.commit()
    db.refresh(payment)
    return payment


def get_payment_for_order(db: Session, user: User, order_id: int) -> Payment:
    payment = db.scalar(select(Payment).where(Payment.order_id == order_id))
    if payment is None:
        raise AppException(status_code=404, message="Pago no encontrado")
    order = db.get(Order, order_id)
    if order is None or (order.user_id != user.id and user.role.name != "ADMIN"):
        raise AppException(status_code=404, message="Pago no encontrado")
    return payment


def simulate_paymentApproval(db: Session, payment_id: int) -> Payment:
    payment = db.get(Payment, payment_id)
    if payment is None:
        raise AppException(status_code=404, message="Pago no encontrado")
    payment.status = PaymentStatus.APPROVED
    order = db.get(Order, payment.order_id)
    if order:
        order.status = "CONFIRMED"
        db.add(order)
    db.commit()
    db.refresh(payment)
    return payment
