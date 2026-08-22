from datetime import datetime

from pydantic import BaseModel

from app.schemas.common import ApiResponse, ORMModel
from app.schemas.product import ProductOut


class WishlistItemOut(ORMModel):
    id: int
    product_id: int
    product: ProductOut
    created_at: datetime


class WishlistApiResponse(ApiResponse[list[WishlistItemOut]]):
    data: list[WishlistItemOut] | None = None
