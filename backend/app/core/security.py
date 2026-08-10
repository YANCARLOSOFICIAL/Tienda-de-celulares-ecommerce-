from datetime import datetime, timedelta, timezone

import bcrypt
import jwt

from app.core.config import settings


class SecurityError(Exception):
    """Error de autenticación/seguridad."""


def hash_password(password: str) -> str:
    """Genera el hash bcrypt de una contraseña en texto plano."""
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def verify_password(plain_password: str, password_hash: str) -> bool:
    """Verifica una contraseña en texto plano contra su hash."""
    try:
        return bcrypt.checkpw(plain_password.encode("utf-8"), password_hash.encode("utf-8"))
    except ValueError:
        return False


def create_access_token(subject: str, extra: dict | None = None) -> str:
    """Crea un token JWT firmado con la clave secreta de la aplicación."""
    now = datetime.now(timezone.utc)
    payload = {
        "sub": subject,
        "iat": now,
        "exp": now + timedelta(minutes=settings.access_token_expire_minutes),
        "type": "access",
    }
    if extra:
        payload.update(extra)
    return jwt.encode(payload, settings.secret_key, algorithm=settings.jwt_algorithm)


def decode_access_token(token: str) -> dict:
    """Decodifica y valida un token JWT. Lanza SecurityError si es inválido/vencido."""
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.jwt_algorithm])
    except jwt.ExpiredSignatureError as exc:
        raise SecurityError("Token expirado") from exc
    except jwt.InvalidTokenError as exc:
        raise SecurityError("Token inválido") from exc
    if payload.get("type") != "access":
        raise SecurityError("Token inválido")
    return payload
