from __future__ import annotations

from decimal import Decimal

from sqlalchemy import Boolean, ForeignKey, Integer, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin


class Product(Base, TimestampMixin):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(200), index=True, nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    price: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    stock: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    brand: Mapped[str] = mapped_column(String(100), index=True, nullable=False)
    model: Mapped[str | None] = mapped_column(String(100), nullable=True)
    image: Mapped[str | None] = mapped_column(String(500), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, index=True, nullable=False)

    category_id: Mapped[int | None] = mapped_column(
        ForeignKey("categories.id", ondelete="SET NULL"), nullable=True, index=True
    )
    category: Mapped["Category | None"] = relationship(back_populates="products")

    cart_items: Mapped[list["CartItem"]] = relationship(back_populates="product")
    order_items: Mapped[list["OrderItem"]] = relationship(back_populates="product")
    wishlist_items: Mapped[list["WishlistItem"]] = relationship(back_populates="product")
    reviews: Mapped[list["Review"]] = relationship(back_populates="product", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"<Product id={self.id} name={self.name!r}>"
