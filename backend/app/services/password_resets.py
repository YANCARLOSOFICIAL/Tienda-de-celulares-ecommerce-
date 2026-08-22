import secrets
from datetime import datetime, timedelta, timezone

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.exceptions import AppException
from app.core.security import hash_password
from app.models.password_reset import PasswordResetToken
from app.models.user import User


def request_reset(db: Session, email: str) -> str:
    user = db.scalar(select(User).where(User.email == email))
    if user is None:
        raise AppException(status_code=404, message="No existe una cuenta con ese email")

    token = secrets.token_urlsafe(48)
    reset_token = PasswordResetToken(
        user_id=user.id,
        token=token,
        expires_at=datetime.now(timezone.utc) + timedelta(hours=1),
        used=False,
    )
    db.add(reset_token)
    db.commit()
    return token


def confirm_reset(db: Session, token: str, new_password: str) -> None:
    reset_token = db.scalar(select(PasswordResetToken).where(PasswordResetToken.token == token))
    if reset_token is None:
        raise AppException(status_code=404, message="Token invalido o expirado")
    if reset_token.used:
        raise AppException(status_code=400, message="El token ya fue utilizado")
    if reset_token.is_expired():
        raise AppException(status_code=400, message="El token ha expirado")

    user = db.get(User, reset_token.user_id)
    if user is None:
        raise AppException(status_code=404, message="Usuario no encontrado")

    user.password_hash = hash_password(new_password)
    reset_token.used = True
    db.commit()
