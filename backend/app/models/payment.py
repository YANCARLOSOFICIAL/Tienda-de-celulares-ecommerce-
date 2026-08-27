from __future__ import annotations

import enum
from decimal import Decimal

from sqlalchemy import ForeignKey, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin


class PaymentStatus(str, enum.Enum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    CANCELLED = "CANCELLED"
    REFUNDED = "REFUNDED"


class Payment(Base, TimestampMixin):
    __tablename__ = "payments"

    id: Mapped[int] = mapped_column(primary_key=True)
    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id", ondelete="CASCADE"), nullable=False, index=True)
    external_id: Mapped[str | None] = mapped_column(String(200), nullable=True, index=True)
    payment_method: Mapped[str | None] = mapped_column(String(50), nullable=True)
    status: Mapped[PaymentStatus] = mapped_column(
        String(20), default=PaymentStatus.PENDING, nullable=False
    )
    amount: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    currency: Mapped[str] = mapped_column(String(3), default="COP", nullable=False)
    checkout_url: Mapped[str | None] = mapped_column(String(500), nullable=True)

    order: Mapped["Order"] = relationship(back_populates="payments")

    def __repr__(self) -> str:
        return f"<Payment id={self.id} order_id={self.order_id} status={self.status}>"
