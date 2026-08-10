from pydantic import BaseModel, EmailStr, Field

from app.schemas.common import ApiResponse, ORMModel


class TokenData(BaseModel):
    access_token: str
    token_type: str = "bearer"


class RegisterRequest(BaseModel):
    email: EmailStr = Field(..., description="Correo electrónico del usuario")
    full_name: str = Field(..., min_length=2, max_length=120, description="Nombre completo")
    password: str = Field(..., min_length=8, max_length=128, description="Contraseña (mínimo 8 caracteres)")


class LoginResponse(TokenData):
    pass


class RegisterResponse(ORMModel):
    id: int
    email: EmailStr
    full_name: str


class TokenApiResponse(ApiResponse[LoginResponse]):
    data: LoginResponse | None = None


class RegisterApiResponse(ApiResponse[RegisterResponse]):
    data: RegisterResponse | None = None
