from datetime import datetime

from pydantic import BaseModel, Field

from app.schemas.common import ApiResponse, ORMModel


class ReviewCreate(BaseModel):
    product_id: int
    rating: int = Field(..., ge=1, le=5, description="Calificacion del 1 al 5")
    title: str | None = Field(default=None, max_length=200)
    comment: str | None = Field(default=None, max_length=2000)


class ReviewUpdate(BaseModel):
    rating: int | None = Field(default=None, ge=1, le=5)
    title: str | None = Field(default=None, max_length=200)
    comment: str | None = Field(default=None, max_length=2000)


class ReviewOut(ORMModel):
    id: int
    user_id: int
    product_id: int
    rating: int
    title: str | None = None
    comment: str | None = None
    user_name: str = ""
    created_at: datetime


class ProductRatingSummary(BaseModel):
    average: float
    total: int
    distribution: dict[int, int]


class ReviewApiResponse(ApiResponse[ReviewOut]):
    data: ReviewOut | None = None


class ReviewListApiResponse(ApiResponse[list[ReviewOut]]):
    data: list[ReviewOut] | None = None


class RatingSummaryApiResponse(ApiResponse[ProductRatingSummary]):
    data: ProductRatingSummary | None = None
