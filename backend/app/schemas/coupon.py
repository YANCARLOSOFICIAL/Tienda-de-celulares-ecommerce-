from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, Field

from app.schemas.common import ApiResponse, ORMModel


class CouponCreate(BaseModel):
    code: str = Field(..., min_length=3, max_length=50, description="Codigo del cupon (se guarda en mayusculas)")
    discount_type: str = Field(..., description="PERCENTAGE o FIXED")
    discount_value: Decimal = Field(..., gt=0, description="Valor del descuento (porcentaje o monto fijo)")
    min_purchase: Decimal = Field(default=Decimal("0.00"), ge=0, description="Compra minima para aplicar")
    max_uses: int | None = Field(default=None, ge=1, description="Numero maximo de usos (null = sin limite)")
    expires_at: datetime | None = Field(default=None, description="Fecha de expiracion (null = sin expiracion)")


class CouponUpdate(BaseModel):
    discount_type: str | None = None
    discount_value: Decimal | None = Field(default=None, gt=0)
    min_purchase: Decimal | None = Field(default=None, ge=0)
    max_uses: int | None = None
    expires_at: datetime | None = None
    is_active: bool | None = None


class CouponOut(ORMModel):
    id: int
    code: str
    discount_type: str
    discount_value: Decimal
    min_purchase: Decimal
    max_uses: int | None
    used_count: int
    expires_at: datetime | None
    is_active: bool
    created_at: datetime


class CouponValidateOut(ORMModel):
    id: int
    code: str
    discount_type: str
    discount_value: Decimal
    min_purchase: Decimal


class CouponApiResponse(ApiResponse[CouponOut]):
    data: CouponOut | None = None


class CouponListApiResponse(ApiResponse[list[CouponOut]]):
    data: list[CouponOut] | None = None


class CouponValidateResponse(ApiResponse[CouponValidateOut]):
    data: CouponValidateOut | None = None
