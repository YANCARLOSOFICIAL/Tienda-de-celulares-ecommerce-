from fastapi import APIRouter

from app.core.dependencies import DbDep
from app.schemas.password_reset import (
    PasswordResetConfirm,
    PasswordResetConfirmResponse,
    PasswordResetRequest,
    PasswordResetRequestResponse,
)
from app.services import password_resets as reset_service

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/forgot-password", response_model=PasswordResetRequestResponse, summary="Solicitar reset de contrasena")
def forgot_password(payload: PasswordResetRequest, db: DbDep) -> PasswordResetRequestResponse:
    token = reset_service.request_reset(db, payload.email)
    return PasswordResetRequestResponse(
        success=True,
        message="Se envio un token de recuperacion a tu email (token de prueba: " + token + ")",
        data=None,
    )


@router.post("/reset-password", response_model=PasswordResetConfirmResponse, summary="Restablecer contrasena")
def reset_password(payload: PasswordResetConfirm, db: DbDep) -> PasswordResetConfirmResponse:
    reset_service.confirm_reset(db, payload.token, payload.new_password)
    return PasswordResetConfirmResponse(
        success=True,
        message="Contrasena actualizada correctamente",
        data=None,
    )
