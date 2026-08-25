"""invoices table (Factus e-invoicing)

Revision ID: a7b8c9d0e1f2
Revises: a6b7c8d9e0f1
Create Date: 2026-08-25
"""
from alembic import op
import sqlalchemy as sa

revision = "a7b8c9d0e1f2"
down_revision = "a6b7c8d9e0f1"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "invoices",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("order_id", sa.Integer(), sa.ForeignKey("orders.id", ondelete="CASCADE"), nullable=False, unique=True),
        sa.Column("reference_code", sa.String(100), nullable=False, unique=True),
        sa.Column("bill_number", sa.String(100), nullable=True, unique=True),
        sa.Column("cufe", sa.String(200), nullable=True),
        sa.Column("qr_url", sa.Text(), nullable=True),
        sa.Column(
            "status",
            sa.Enum("PENDING", "VALIDATED", "FAILED", name="invoice_status"),
            server_default="PENDING",
            nullable=False,
            index=True,
        ),
        sa.Column("total", sa.Numeric(12, 2), nullable=False),
        sa.Column("customer_identification", sa.String(50), nullable=True),
        sa.Column("error_message", sa.Text(), nullable=True),
        sa.Column("factus_response", sa.Text(), nullable=True),
        sa.Column("validated_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_index("ix_invoices_order_id", "invoices", ["order_id"])


def downgrade() -> None:
    op.drop_index("ix_invoices_order_id", table_name="invoices")
    op.drop_table("invoices")
    sa.Enum(name="invoice_status").drop(op.get_bind(), checkfirst=True)
