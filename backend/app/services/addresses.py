from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.exceptions import AppException
from app.models.address import Address
from app.models.user import User
from app.schemas.address import AddressCreate, AddressUpdate


def list_addresses(db: Session, user: User) -> list[Address]:
    return list(db.scalars(select(Address).where(Address.user_id == user.id).order_by(Address.is_default.desc(), Address.id)))


def get_address_or_404(db: Session, user: User, address_id: int) -> Address:
    address = db.get(Address, address_id)
    if address is None or address.user_id != user.id:
        raise AppException(status_code=404, message="Direccion no encontrada")
    return address


def create_address(db: Session, user: User, payload: AddressCreate) -> Address:
    if payload.is_default:
        _clear_default(db, user)
    address = Address(user_id=user.id, **payload.model_dump())
    db.add(address)
    db.commit()
    db.refresh(address)
    return address


def update_address(db: Session, user: User, address_id: int, payload: AddressUpdate) -> Address:
    address = get_address_or_404(db, user, address_id)
    data = payload.model_dump(exclude_unset=True)
    if data.get("is_default"):
        _clear_default(db, user)
    for field, value in data.items():
        setattr(address, field, value)
    db.commit()
    db.refresh(address)
    return address


def delete_address(db: Session, user: User, address_id: int) -> None:
    address = get_address_or_404(db, user, address_id)
    db.delete(address)
    db.commit()


def _clear_default(db: Session, user: User) -> None:
    stmt = select(Address).where(Address.user_id == user.id, Address.is_default.is_(True))
    for addr in db.scalars(stmt):
        addr.is_default = False
        db.add(addr)
