from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.exceptions import AppException
from app.core.security import create_access_token, hash_password, verify_password
from app.models.role import Role
from app.models.user import User
from app.schemas.auth import RegisterRequest


def get_role_by_name(db: Session, name: str) -> Role:
    role = db.scalar(select(Role).where(Role.name == name))
    if role is None:
        raise AppException(status_code=500, message=f"Rol '{name}' no configurado")
    return role


def register_user(db: Session, payload: RegisterRequest) -> User:
    existing = db.scalar(select(User).where(User.email == payload.email.lower()))
    if existing:
        raise AppException(status_code=409, message="Ya existe un usuario con ese correo")

    user_role = get_role_by_name(db, "USER")
    user = User(
        email=payload.email.lower(),
        full_name=payload.full_name.strip(),
        password_hash=hash_password(payload.password),
        role_id=user_role.id,
        is_active=True,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def authenticate(db: Session, email: str, password: str) -> User:
    user = db.scalar(select(User).where(User.email == email.lower()))
    if user is None or not verify_password(password, user.password_hash):
        raise AppException(status_code=401, message="Credenciales incorrectas")
    if not user.is_active:
        raise AppException(status_code=403, message="Usuario inactivo")
    return user


def issue_token(user: User) -> str:
    return create_access_token(subject=str(user.id), extra={"role": user.role.name})
