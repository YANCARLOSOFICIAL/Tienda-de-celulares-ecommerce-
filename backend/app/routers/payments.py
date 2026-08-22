from fastapi import APIRouter

from app.core.dependencies import CurrentUser, DbDep, AdminUser
from app.schemas.common import ApiResponse
from app.schemas.payment import PaymentApiResponse, PaymentCreateApiResponse, PaymentCreateResponse, PaymentOut
from app.services import payments as payment_service

router = APIRouter(prefix="/payments", tags=["Pagos"])


@router.post("/create/{order_id}", response_model=PaymentCreateApiResponse, summary="Crear pago para un pedido")
def create_payment(order_id: int, db: DbDep, current_user: CurrentUser) -> PaymentCreateApiResponse:
    payment = payment_service.create_payment(db, current_user, order_id)
    return PaymentCreateApiResponse(
        success=True,
        message="Pago creado correctamente",
        data=PaymentCreateResponse(
            payment_id=payment.id,
            checkout_url=payment.checkout_url or "",
            preference_id=payment.external_id,
        ),
    )


@router.get("/order/{order_id}", response_model=PaymentApiResponse, summary="Obtener pago de un pedido")
def get_payment(order_id: int, db: DbDep, current_user: CurrentUser) -> PaymentApiResponse:
    payment = payment_service.get_payment_for_order(db, current_user, order_id)
    return PaymentApiResponse(
        success=True,
        message="Pago obtenido correctamente",
        data=PaymentOut.model_validate(payment),
    )


@router.post("/simulate/{payment_id}", response_model=PaymentApiResponse, summary="Simular aprobacion de pago (sandbox)")
def simulate_approval(payment_id: int, db: DbDep, _admin: AdminUser) -> PaymentApiResponse:
    payment = payment_service.simulate_paymentApproval(db, payment_id)
    return PaymentApiResponse(
        success=True,
        message="Pago aprobado (simulacion)",
        data=PaymentOut.model_validate(payment),
    )
