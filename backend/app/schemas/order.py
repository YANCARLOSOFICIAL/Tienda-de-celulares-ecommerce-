from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, Field

from app.schemas.common import ApiResponse, ORMModel
from app.schemas.invoice import InvoiceSummary
from app.schemas.order_status import OrderStatus


class OrderItemOut(ORMModel):
    id: int
    product_id: int | None
    product_name: str
    unit_price: Decimal
    quantity: int
    subtotal: Decimal


class OrderOut(ORMModel):
    id: int
    status: OrderStatus
    total: Decimal
    shipping_method: str | None = None
    shipping_cost: Decimal = Decimal("0.00")
    coupon_code: str | None = None
    discount_amount: Decimal = Decimal("0.00")
    items: list[OrderItemOut]
    invoice: InvoiceSummary | None = None
    created_at: datetime
    updated_at: datetime


class OrderDetailOut(ORMModel):
    id: int
    status: OrderStatus
    total: Decimal
    user_id: int
    address_id: int | None = None
    shipping_method: str | None = None
    shipping_cost: Decimal = Decimal("0.00")
    coupon_code: str | None = None
    discount_amount: Decimal = Decimal("0.00")
    shipping_address_snapshot: str | None = None
    notes: str | None = None
    items: list[OrderItemOut]
    invoice: InvoiceSummary | None = None
    created_at: datetime
    updated_at: datetime


class OrderCreate(BaseModel):
    address_id: int | None = None
    shipping_method: str = Field(default="estandar", description="Metodo de envio: estandar, express, recoleccion")
    coupon_code: str | None = Field(default=None, max_length=50, description="Codigo de cupon a aplicar")
    notes: str | None = Field(default=None, max_length=500)


class OrderStatusUpdate(BaseModel):
    status: OrderStatus = Field(..., description="Nuevo estado del pedido")


class OrderApiResponse(ApiResponse[OrderDetailOut]):
    data: OrderDetailOut | None = None


class OrderListApiResponse(ApiResponse[list[OrderDetailOut]]):
    data: list[OrderDetailOut] | None = None
