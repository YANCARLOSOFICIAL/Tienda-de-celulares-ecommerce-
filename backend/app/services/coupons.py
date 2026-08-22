from decimal import Decimal
from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.exceptions import AppException
from app.models.coupon import Coupon
from app.schemas.coupon import CouponCreate, CouponUpdate


def list_coupons(db: Session) -> list[Coupon]:
    return list(db.scalars(select(Coupon).order_by(Coupon.created_at.desc())))


def get_coupon(db: Session, coupon_id: int) -> Coupon:
    coupon = db.get(Coupon, coupon_id)
    if coupon is None:
        raise AppException(status_code=404, message="Cupon no encontrado")
    return coupon


def create_coupon(db: Session, payload: CouponCreate) -> Coupon:
    existing = db.scalar(select(Coupon).where(Coupon.code == payload.code.upper()))
    if existing:
        raise AppException(status_code=400, message="Ya existe un cupon con ese codigo")
    coupon = Coupon(
        code=payload.code.upper(),
        discount_type=payload.discount_type.upper(),
        discount_value=payload.discount_value,
        min_purchase=payload.min_purchase,
        max_uses=payload.max_uses,
        expires_at=payload.expires_at,
        is_active=True,
    )
    db.add(coupon)
    db.commit()
    db.refresh(coupon)
    return coupon


def update_coupon(db: Session, coupon_id: int, payload: CouponUpdate) -> Coupon:
    coupon = get_coupon(db, coupon_id)
    update_data = payload.model_dump(exclude_unset=True)
    if "discount_type" in update_data and update_data["discount_type"] is not None:
        coupon.discount_type = update_data.pop("discount_type").upper()
    for field, value in update_data.items():
        setattr(coupon, field, value)
    db.commit()
    db.refresh(coupon)
    return coupon


def delete_coupon(db: Session, coupon_id: int) -> None:
    coupon = get_coupon(db, coupon_id)
    db.delete(coupon)
    db.commit()


def validate_coupon(db: Session, code: str, subtotal: Decimal) -> Coupon:
    coupon = db.scalar(select(Coupon).where(Coupon.code == code.upper()))
    if coupon is None:
        raise AppException(status_code=404, message="Cupon no encontrado")
    if not coupon.is_active:
        raise AppException(status_code=400, message="El cupon no esta activo")
    if coupon.expires_at and coupon.expires_at < datetime.now(timezone.utc):
        raise AppException(status_code=400, message="El cupon ha expirado")
    if coupon.max_uses is not None and coupon.used_count >= coupon.max_uses:
        raise AppException(status_code=400, message="El cupon ha alcanzado su limite de usos")
    if subtotal < coupon.min_purchase:
        raise AppException(
            status_code=400,
            message=f"La compra minima para este cupon es ${coupon.min_purchase}",
        )
    if coupon.discount_type == "PERCENTAGE" and coupon.discount_value > Decimal("100"):
        raise AppException(status_code=400, message="El porcentaje de descuento no puede ser mayor a 100")
    return coupon


def calculate_discount(coupon: Coupon, subtotal: Decimal) -> Decimal:
    if coupon.discount_type == "PERCENTAGE":
        return (subtotal * coupon.discount_value / Decimal("100")).quantize(Decimal("0.01"))
    return min(coupon.discount_value, subtotal)
