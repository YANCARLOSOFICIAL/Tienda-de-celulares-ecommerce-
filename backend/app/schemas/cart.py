from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, Field, field_validator

from app.schemas.common import ApiResponse, ORMModel
from app.schemas.product import ProductOut


class CartItemOut(ORMModel):
    id: int
    product_id: int
    product: ProductOut
    quantity: int
    subtotal: Decimal
    created_at: datetime
    updated_at: datetime


class CartOut(ORMModel):
    id: int
    items: list[CartItemOut]
    total: Decimal
    item_count: int


class CartItemCreate(BaseModel):
    product_id: int = Field(..., gt=0)
    quantity: int = Field(..., ge=1, description="Cantidad, debe ser >= 1")


class CartItemUpdate(BaseModel):
    quantity: int = Field(..., ge=1, description="Nueva cantidad, debe ser >= 1")

    @field_validator("quantity")
    @classmethod
    def validate_quantity(cls, v: int) -> int:
        if v < 1:
            raise ValueError("La cantidad debe ser al menos 1")
        return v


class CartApiResponse(ApiResponse[CartOut]):
    data: CartOut | None = None


class CartItemApiResponse(ApiResponse[CartItemOut]):
    data: CartItemOut | None = None


class CartMessageApiResponse(ApiResponse[None]):
    data: None = None
