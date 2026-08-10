from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.core.dependencies import DbDep
from app.schemas.auth import LoginResponse, RegisterApiResponse, RegisterRequest, TokenApiResponse
from app.services import auth as auth_service

router = APIRouter(prefix="/auth", tags=["Autenticación"])


@router.post(
    "/register",
    response_model=RegisterApiResponse,
    status_code=201,
    summary="Registrar un nuevo usuario",
)
def register(payload: RegisterRequest, db: DbDep) -> RegisterApiResponse:
    user = auth_service.register_user(db, payload)
    return RegisterApiResponse(success=True, message="Usuario registrado correctamente", data=user)


@router.post(
    "/login",
    response_model=TokenApiResponse,
    summary="Iniciar sesión y obtener token JWT",
    description="Autentica con correo y contraseña. Devuelve un access token tipo Bearer.",
)
def login(
    db: DbDep,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> TokenApiResponse:
    user = auth_service.authenticate(db, form_data.username, form_data.password)
    token = auth_service.issue_token(user)
    return TokenApiResponse(
        success=True,
        message="Sesión iniciada correctamente",
        data=LoginResponse(access_token=token, token_type="bearer"),
    )
