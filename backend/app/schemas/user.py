from datetime import datetime

from pydantic import BaseModel, EmailStr, Field

from app.schemas.common import ApiResponse, ORMModel


class RoleOut(ORMModel):
    id: int
    name: str


class UserOut(ORMModel):
    id: int
    email: EmailStr
    full_name: str
    is_active: bool
    role: RoleOut
    created_at: datetime
    updated_at: datetime


class UserUpdate(BaseModel):
    full_name: str | None = Field(default=None, min_length=2, max_length=120)
    password: str | None = Field(default=None, min_length=8, max_length=128)


class UserApiResponse(ApiResponse[UserOut]):
    data: UserOut | None = None
