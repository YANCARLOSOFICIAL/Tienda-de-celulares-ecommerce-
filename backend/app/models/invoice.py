from __future__ import annotations

import enum
from datetime import datetime
from decimal import Decimal

from sqlalchemy import DateTime, Enum, ForeignKey, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin


class InvoiceStatus(str, enum.Enum):
    """Estado local de la factura. VALIDATED = aceptada por la DIAN en Factus."""

    PENDING = "PENDING"
    VALIDATED = "VALIDATED"
    FAILED = "FAILED"


class Invoice(Base, TimestampMixin):
    __tablename__ = "invoices"

    id: Mapped[int] = mapped_column(primary_key=True)
    order_id: Mapped[int] = mapped_column(
        ForeignKey("orders.id", ondelete="CASCADE"), nullable=False, unique=True, index=True
    )
    reference_code: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    bill_number: Mapped[str | None] = mapped_column(String(100), nullable=True, unique=True, index=True)
    cufe: Mapped[str | None] = mapped_column(String(200), nullable=True)
    qr_url: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[InvoiceStatus] = mapped_column(
        Enum(InvoiceStatus, name="invoice_status"), default=InvoiceStatus.PENDING, nullable=False, index=True
    )
    total: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    customer_identification: Mapped[str | None] = mapped_column(String(50), nullable=True)
    error_message: Mapped[str | None] = mapped_column(Text, nullable=True)
    factus_response: Mapped[str | None] = mapped_column(Text, nullable=True)
    validated_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    order: Mapped["Order"] = relationship(back_populates="invoice")

    def __repr__(self) -> str:
        return f"<Invoice id={self.id} order_id={self.order_id} number={self.bill_number!r} status={self.status.value}>"
