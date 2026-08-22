from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.exceptions import AppException
from app.models.product import Product
from app.models.user import User
from app.models.wishlist import WishlistItem


def list_wishlist(db: Session, user: User) -> list[WishlistItem]:
    return list(db.scalars(select(WishlistItem).where(WishlistItem.user_id == user.id).order_by(WishlistItem.created_at.desc())))


def add_to_wishlist(db: Session, user: User, product_id: int) -> WishlistItem:
    product = db.get(Product, product_id)
    if product is None or not product.is_active:
        raise AppException(status_code=404, message="Producto no encontrado")
    existing = db.scalar(
        select(WishlistItem).where(WishlistItem.user_id == user.id, WishlistItem.product_id == product_id)
    )
    if existing:
        raise AppException(status_code=400, message="El producto ya esta en tu lista de favoritos")
    item = WishlistItem(user_id=user.id, product_id=product_id)
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


def remove_from_wishlist(db: Session, user: User, product_id: int) -> None:
    item = db.scalar(
        select(WishlistItem).where(WishlistItem.user_id == user.id, WishlistItem.product_id == product_id)
    )
    if item is None:
        raise AppException(status_code=404, message="Producto no encontrado en favoritos")
    db.delete(item)
    db.commit()
