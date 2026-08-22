from decimal import Decimal

from pydantic import BaseModel

from app.schemas.common import ApiResponse


class AdminStats(BaseModel):
    total_orders: int
    total_revenue: Decimal
    total_products: int
    total_users: int
    orders_by_status: dict[str, int]
    recent_orders: list[dict]
    top_products: list[dict]


class AdminStatsApiResponse(ApiResponse[AdminStats]):
    data: AdminStats | None = None
