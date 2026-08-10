from fastapi import APIRouter

from app.core.dependencies import CurrentUser, DbDep
from app.schemas.user import UserApiResponse, UserOut, UserUpdate
from app.services import users as user_service

router = APIRouter(prefix="/users", tags=["Usuarios"])


@router.get("/me", response_model=UserApiResponse, summary="Obtener el usuario autenticado")
def get_me(current_user: CurrentUser) -> UserApiResponse:
    return UserApiResponse(
        success=True, message="Usuario obtenido correctamente", data=UserOut.model_validate(current_user)
    )


@router.patch("/me", response_model=UserApiResponse, summary="Actualizar el perfil del usuario")
def update_me(payload: UserUpdate, current_user: CurrentUser, db: DbDep) -> UserApiResponse:
    user = user_service.update_profile(db, current_user, payload)
    return UserApiResponse(
        success=True, message="Perfil actualizado correctamente", data=UserOut.model_validate(user)
    )
