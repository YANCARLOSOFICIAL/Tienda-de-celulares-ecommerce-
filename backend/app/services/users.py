from sqlalchemy.orm import Session

from app.core.exceptions import AppException
from app.core.security import hash_password, verify_password
from app.models.user import User
from app.schemas.user import UserUpdate


def update_profile(db: Session, user: User, payload: UserUpdate) -> User:
    changes = payload.model_dump(exclude_unset=True, exclude_none=True)

    new_password = changes.pop("password", None)
    if new_password is not None:
        if user.password_hash and verify_password(new_password, user.password_hash):
            raise AppException(status_code=400, message="La nueva contraseña no puede ser igual a la actual")
        user.password_hash = hash_password(new_password)

    if "full_name" in changes:
        full_name = changes["full_name"].strip()
        if not full_name:
            raise AppException(status_code=422, message="El nombre completo no puede estar vacío")
        user.full_name = full_name

    db.add(user)
    db.commit()
    db.refresh(user)
    return user
