from app.db.session import engine  # noqa: F401  (asegura el engine al importar base)
from app.models.base import Base  # noqa: F401
from app.models.address import Address  # noqa: F401
from app.models.category import Category  # noqa: F401
from app.models.coupon import Coupon  # noqa: F401
from app.models.password_reset import PasswordResetToken  # noqa: F401
from app.models.payment import Payment  # noqa: F401
from app.models.product import Product  # noqa: F401
from app.models.review import Review  # noqa: F401
from app.models.role import Role  # noqa: F401
from app.models.user import User  # noqa: F401
from app.models.wishlist import WishlistItem  # noqa: F401
from app.models.cart import Cart, CartItem  # noqa: F401
from app.models.order import Order, OrderItem  # noqa: F401
from app.models.invoice import Invoice  # noqa: F401

# Registro completo de modelos: cualquier entrypoint (seed, alembic, workers)
# que importe este módulo ve todos los mappers y la metadata completa.
