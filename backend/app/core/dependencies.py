from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.exceptions import AppException
from app.core.security import SecurityError, decode_access_token
from app.db.session import get_db
from app.models.user import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=settings.auth_url)
oauth2_scheme_optional = OAuth2PasswordBearer(tokenUrl=settings.auth_url, auto_error=False)

DbDep = Annotated[Session, Depends(get_db)]
TokenDep = Annotated[str, Depends(oauth2_scheme)]


def get_current_user(db: DbDep, token: TokenDep) -> User:
    """Obtiene el usuario autenticado a partir del token JWT."""
    try:
        payload = decode_access_token(token)
    except SecurityError as exc:
        raise AppException(status_code=401, message=exc.args[0]) from exc

    user_id = payload.get("sub")
    if not user_id:
        raise AppException(status_code=401, message="Token inválido")

    user = db.get(User, int(user_id))
    if user is None:
        raise AppException(status_code=401, message="Usuario no encontrado")
    if not user.is_active:
        raise AppException(status_code=403, message="Usuario inactivo")
    return user


CurrentUser = Annotated[User, Depends(get_current_user)]


def get_optional_current_user(
    db: DbDep, token: Annotated[str | None, Depends(oauth2_scheme_optional)]
) -> User | None:
    """Devuelve el usuario autenticado o None si no se proporcionó un token válido."""
    if token is None:
        return None
    try:
        return get_current_user(db, token)
    except AppException:
        return None


OptionalUser = Annotated[User | None, Depends(get_optional_current_user)]


def require_role(*roles: str):
    """Crea una dependencia que exige que el usuario autenticado tenga uno de los roles dados."""

    def role_checker(current_user: CurrentUser) -> User:
        if current_user.role.name not in roles:
            raise AppException(
                status_code=403,
                message="No tienes permisos para realizar esta acción",
            )
        return current_user

    return role_checker


AdminUser = Annotated[User, Depends(require_role("ADMIN"))]
