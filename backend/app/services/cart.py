from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.exceptions import AppException
from app.models.cart import Cart, CartItem
from app.models.product import Product
from app.models.user import User
from app.schemas.cart import CartItemCreate


def get_or_create_cart(db: Session, user: User) -> Cart:
    cart = db.scalar(select(Cart).where(Cart.user_id == user.id))
    if cart is None:
        cart = Cart(user_id=user.id)
        db.add(cart)
        db.commit()
        db.refresh(cart)
    return cart


def _get_product(db: Session, product_id: int) -> Product:
    product = db.get(Product, product_id)
    if product is None or not product.is_active:
        raise AppException(status_code=404, message="Producto no encontrado")
    return product


def _validate_quantity(product: Product, quantity: int) -> None:
    if quantity < 1:
        raise AppException(status_code=422, message="La cantidad debe ser al menos 1")
    if product.stock < quantity:
        raise AppException(
            status_code=400,
            message=f"Stock insuficiente para '{product.name}'. Disponible: {product.stock}",
        )


def add_item(db: Session, user: User, payload: CartItemCreate) -> dict:
    cart = get_or_create_cart(db, user)
    product = _get_product(db, payload.product_id)
    _validate_quantity(product, payload.quantity)

    item = db.scalar(
        select(CartItem).where(
            CartItem.cart_id == cart.id, CartItem.product_id == payload.product_id
        )
    )
    if item:
        item.quantity += payload.quantity
        _validate_quantity(product, item.quantity)
    else:
        item = CartItem(cart_id=cart.id, product_id=payload.product_id, quantity=payload.quantity)
        db.add(item)

    db.commit()
    db.refresh(item)
    return serialize_item(item)


def update_item_quantity(db: Session, user: User, item_id: int, quantity: int) -> dict:
    item = _get_item(db, user, item_id)
    _validate_quantity(item.product, quantity)
    item.quantity = quantity
    db.add(item)
    db.commit()
    db.refresh(item)
    return serialize_item(item)


def remove_item(db: Session, user: User, item_id: int) -> None:
    item = _get_item(db, user, item_id)
    db.delete(item)
    db.commit()


def clear_cart(db: Session, user: User) -> None:
    cart = db.scalar(select(Cart).where(Cart.user_id == user.id))
    if cart:
        cart.items.clear()
        db.commit()


def _get_item(db: Session, user: User, item_id: int) -> CartItem:
    cart = db.scalar(select(Cart).where(Cart.user_id == user.id))
    item = db.get(CartItem, item_id) if cart else None
    if item is None or cart is None or item.cart_id != cart.id:
        raise AppException(status_code=404, message="Ítem de carrito no encontrado")
    return item


def serialize_item(item: CartItem) -> dict:
    return {
        "id": item.id,
        "product_id": item.product_id,
        "product": item.product,
        "quantity": item.quantity,
        "subtotal": (Decimal(item.quantity) * item.product.price),
        "created_at": item.created_at,
        "updated_at": item.updated_at,
    }


def get_cart_data(db: Session, user: User) -> dict:
    cart = db.scalar(select(Cart).where(Cart.user_id == user.id))
    if cart is None:
        return {"id": 0, "items": [], "total": Decimal("0.00"), "item_count": 0}

    items = cart.items
    serialized_items = [serialize_item(i) for i in items]
    total = sum((i["subtotal"] for i in serialized_items), Decimal("0.00"))
    item_count = sum(i["quantity"] for i in serialized_items)
    return {
        "id": cart.id,
        "items": serialized_items,
        "total": total,
        "item_count": item_count,
    }
