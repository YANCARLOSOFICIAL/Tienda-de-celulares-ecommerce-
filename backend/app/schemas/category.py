from datetime import datetime

from pydantic import BaseModel, Field, field_validator

from app.schemas.common import ApiResponse, ORMModel


class CategoryCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    description: str | None = Field(default=None, max_length=500)


class CategoryUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=2, max_length=100)
    description: str | None = Field(default=None, max_length=500)

    @field_validator("name", "description")
    @classmethod
    def strip_whitespace(cls, v: str | None) -> str | None:
        if v is not None:
            v = v.strip()
        return v


class CategoryOut(ORMModel):
    id: int
    name: str
    slug: str
    description: str | None
    created_at: datetime
    updated_at: datetime


class CategoryApiResponse(ApiResponse[CategoryOut]):
    data: CategoryOut | None = None


class CategoryListApiResponse(ApiResponse[list[CategoryOut]]):
    data: list[CategoryOut] | None = None
