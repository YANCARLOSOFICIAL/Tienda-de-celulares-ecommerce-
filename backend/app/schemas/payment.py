from decimal import Decimal

from pydantic import BaseModel

from app.schemas.common import ApiResponse, ORMModel


class PaymentOut(ORMModel):
    id: int
    order_id: int
    external_id: str | None = None
    payment_method: str | None = None
    status: str
    amount: Decimal
    currency: str
    checkout_url: str | None = None


class PaymentCreateResponse(ORMModel):
    payment_id: int
    checkout_url: str
    preference_id: str | None = None


class PaymentApiResponse(ApiResponse[PaymentOut]):
    data: PaymentOut | None = None


class PaymentCreateApiResponse(ApiResponse[PaymentCreateResponse]):
    data: PaymentCreateResponse | None = None
