from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.exceptions import AppException
from app.models.address import Address
from app.models.cart import Cart
from app.models.order import Order, OrderItem
from app.models.product import Product
from app.models.user import User
from app.schemas.order import OrderCreate
from app.services.coupons import validate_coupon, calculate_discount

SHIPPING_COSTS = {
    "estandar": Decimal("99.00"),
    "express": Decimal("199.00"),
    "recoleccion": Decimal("0.00"),
}


def _lock_products(db: Session, product_ids: list[int]) -> list[Product]:
    """Bloquea las filas de producto (SELECT ... FOR UPDATE) para evitar condiciones de carrera.

    `populate_existing` fuerza a SQLAlchemy a refrescar los objetos Product desde el
    resultado bloqueado (los objetos ya cargados en el identity map quedarían obsoletos
    con el valor previo de stock, provocando *lost updates*).
    """
    if not product_ids:
        return []
    stmt = select(Product).where(Product.id.in_(product_ids)).with_for_update()
    return list(db.scalars(stmt, execution_options={"populate_existing": True}))


def create_order(db: Session, user: User, payload: OrderCreate | None = None) -> Order:
    """Crea un pedido a partir del carrito del usuario, dentro de una unica transaccion.

    Si cualquier validacion falla, la transaccion se revierte por completo:
    no queda un pedido incompleto, el stock no se descuenta parcialmente
    y el carrito no se vacia.
    """
    shipping_method = payload.shipping_method if payload else "estandar"
    shipping_cost = SHIPPING_COSTS.get(shipping_method, Decimal("99.00"))
    notes = payload.notes if payload else None
    coupon_code = payload.coupon_code if payload else None

    address_snapshot = None
    address_id = None
    if payload and payload.address_id:
        address = db.get(Address, payload.address_id)
        if address and address.user_id == user.id:
            address_id = address.id
            parts = [
                address.street,
                address.street_number,
                address.interior,
                address.neighborhood,
                address.city,
                address.state,
                address.zip_code,
            ]
            address_snapshot = ", ".join(p for p in parts if p)

    try:
        cart = db.scalar(select(Cart).where(Cart.user_id == user.id))
        if cart is None or not cart.items:
            raise AppException(status_code=400, message="El carrito esta vacio")

        cart_items = cart.items
        product_ids = [item.product_id for item in cart_items]
        products = {p.id: p for p in _lock_products(db, product_ids)}

        if len(products) != len(product_ids):
            raise AppException(status_code=404, message="Alguno de los productos ya no existe")

        order = Order(
            user_id=user.id,
            status="PENDING",
            total=Decimal("0.00"),
            address_id=address_id,
            shipping_method=shipping_method,
            shipping_cost=shipping_cost,
            shipping_address_snapshot=address_snapshot,
            notes=notes,
        )
        db.add(order)
        db.flush()

        total = Decimal("0.00")
        for item in cart_items:
            product = products[item.product_id]
            if not product.is_active:
                raise AppException(
                    status_code=400, message=f"El producto '{product.name}' ya no esta disponible"
                )
            if product.stock < item.quantity:
                raise AppException(
                    status_code=400,
                    message=f"Stock insuficiente para '{product.name}'. Disponible: {product.stock}",
                )

            subtotal = product.price * Decimal(item.quantity)
            total += subtotal
            db.add(
                OrderItem(
                    order_id=order.id,
                    product_id=product.id,
                    product_name=product.name,
                    unit_price=product.price,
                    quantity=item.quantity,
                    subtotal=subtotal,
                )
            )
            product.stock -= item.quantity

        discount = Decimal("0.00")
        if coupon_code:
            coupon = validate_coupon(db, coupon_code, total)
            discount = calculate_discount(coupon, total)
            coupon.used_count += 1
            db.add(coupon)

        order.total = total + shipping_cost - discount
        order.coupon_code = coupon_code
        order.discount_amount = discount

        cart.items.clear()
        db.commit()
        db.refresh(order)
        return order
    except AppException:
        db.rollback()
        raise
    except Exception:
        db.rollback()
        raise


def get_order_for_user(db: Session, user: User, order_id: int) -> Order:
    order = db.get(Order, order_id)
    if order is None:
        raise AppException(status_code=404, message="Pedido no encontrado")
    if user.role.name != "ADMIN" and order.user_id != user.id:
        raise AppException(status_code=404, message="Pedido no encontrado")
    return order


def list_orders(db: Session, user: User) -> list[Order]:
    if user.role.name == "ADMIN":
        stmt = select(Order).order_by(Order.created_at.desc())
    else:
        stmt = select(Order).where(Order.user_id == user.id).order_by(Order.created_at.desc())
    return list(db.scalars(stmt))


def update_order_status(db: Session, user: User, order_id: int, new_status: str) -> Order:
    order = get_order_for_user(db, user, order_id)
    if user.role.name != "ADMIN":
        raise AppException(status_code=403, message="No tienes permisos para realizar esta acción")
    order.status = new_status
    db.add(order)
    db.commit()
    db.refresh(order)
    return order
