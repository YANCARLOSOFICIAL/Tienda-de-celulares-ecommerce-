from datetime import datetime

from pydantic import BaseModel, Field

from app.schemas.common import ApiResponse, ORMModel


class AddressCreate(BaseModel):
    label: str = Field(default="Casa", max_length=50)
    full_name: str = Field(..., min_length=1, max_length=120)
    phone: str = Field(..., min_length=1, max_length=20)
    street: str = Field(..., min_length=1, max_length=200)
    street_number: str | None = Field(default=None, max_length=20)
    interior: str | None = Field(default=None, max_length=50)
    neighborhood: str = Field(..., min_length=1, max_length=100)
    city: str = Field(..., min_length=1, max_length=100)
    state: str = Field(..., min_length=1, max_length=100)
    zip_code: str = Field(..., min_length=1, max_length=10)
    is_default: bool = False


class AddressUpdate(BaseModel):
    label: str | None = Field(default=None, max_length=50)
    full_name: str | None = Field(default=None, min_length=1, max_length=120)
    phone: str | None = Field(default=None, min_length=1, max_length=20)
    street: str | None = Field(default=None, min_length=1, max_length=200)
    street_number: str | None = Field(default=None, max_length=20)
    interior: str | None = Field(default=None, max_length=50)
    neighborhood: str | None = Field(default=None, min_length=1, max_length=100)
    city: str | None = Field(default=None, min_length=1, max_length=100)
    state: str | None = Field(default=None, min_length=1, max_length=100)
    zip_code: str | None = Field(default=None, min_length=1, max_length=10)
    is_default: bool | None = None


class AddressOut(ORMModel):
    id: int
    user_id: int
    label: str
    full_name: str
    phone: str
    street: str
    street_number: str | None
    interior: str | None
    neighborhood: str
    city: str
    state: str
    zip_code: str
    is_default: bool
    created_at: datetime
    updated_at: datetime


class AddressApiResponse(ApiResponse[AddressOut]):
    data: AddressOut | None = None


class AddressListApiResponse(ApiResponse[list[AddressOut]]):
    data: list[AddressOut] | None = None
