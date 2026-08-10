from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, Field

from app.schemas.common import ApiResponse, ORMModel
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
    items: list[OrderItemOut]
    created_at: datetime
    updated_at: datetime


class OrderDetailOut(ORMModel):
    id: int
    status: OrderStatus
    total: Decimal
    user_id: int
    items: list[OrderItemOut]
    created_at: datetime
    updated_at: datetime


class OrderCreate(BaseModel):
    pass


class OrderStatusUpdate(BaseModel):
    status: OrderStatus = Field(..., description="Nuevo estado del pedido")


class OrderApiResponse(ApiResponse[OrderDetailOut]):
    data: OrderDetailOut | None = None


class OrderListApiResponse(ApiResponse[list[OrderDetailOut]]):
    data: list[OrderDetailOut] | None = None
