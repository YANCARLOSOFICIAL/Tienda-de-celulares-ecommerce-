from pydantic import BaseModel, EmailStr, Field

from app.schemas.common import ApiResponse


class PasswordResetRequest(BaseModel):
    email: EmailStr = Field(..., description="Email del usuario")


class PasswordResetConfirm(BaseModel):
    token: str = Field(..., min_length=10, description="Token de recuperacion")
    new_password: str = Field(..., min_length=8, max_length=100, description="Nueva contrasena")


class PasswordResetRequestResponse(ApiResponse):
    data: None = None


class PasswordResetConfirmResponse(ApiResponse):
    data: None = None
