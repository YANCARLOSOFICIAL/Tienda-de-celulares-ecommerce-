from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, Field

from app.schemas.category import CategoryOut
from app.schemas.common import ApiResponse, ORMModel, Page


class ProductCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=200)
    description: str | None = None
    price: Decimal = Field(..., gt=0, description="Precio unitario, debe ser mayor a 0")
    stock: int = Field(..., ge=0, description="Existencia inicial, debe ser >= 0")
    brand: str = Field(..., min_length=1, max_length=100)
    model: str | None = Field(default=None, max_length=100)
    category_id: int | None = Field(default=None, description="ID de la categoría (opcional)")
    image: str | None = Field(default=None, max_length=500)
    images: list[str] = Field(default_factory=list, description="Galería de imágenes (URLs)")
    is_active: bool = True


class ProductUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=2, max_length=200)
    description: str | None = None
    price: Decimal | None = Field(default=None, gt=0)
    stock: int | None = Field(default=None, ge=0)
    brand: str | None = Field(default=None, min_length=1, max_length=100)
    model: str | None = Field(default=None, max_length=100)
    category_id: int | None = Field(default=None)
    image: str | None = Field(default=None, max_length=500)
    images: list[str] | None = Field(default=None, description="Galería de imágenes (URLs)")
    is_active: bool | None = None


class ProductOut(ORMModel):
    id: int
    name: str
    description: str | None
    price: Decimal
    stock: int
    brand: str
    model: str | None
    image: str | None
    images: list[str] = []
    is_active: bool
    category_id: int | None
    category: CategoryOut | None = None
    created_at: datetime
    updated_at: datetime


class ProductApiResponse(ApiResponse[ProductOut]):
    data: ProductOut | None = None


class ProductListApiResponse(ApiResponse[Page[ProductOut]]):
    data: Page[ProductOut] | None = None
