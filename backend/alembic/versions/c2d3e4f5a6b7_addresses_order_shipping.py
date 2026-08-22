"""addresses + order shipping

Revision ID: c2d3e4f5a6b7
Revises: ba881e09a277
Create Date: 2026-08-22
"""
from alembic import op
import sqlalchemy as sa

revision = "c2d3e4f5a6b7"
down_revision = "ba881e09a277"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Addresses table
    op.create_table(
        "addresses",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("label", sa.String(50), nullable=False, server_default="Casa"),
        sa.Column("full_name", sa.String(120), nullable=False),
        sa.Column("phone", sa.String(20), nullable=False),
        sa.Column("street", sa.String(200), nullable=False),
        sa.Column("street_number", sa.String(20), nullable=True),
        sa.Column("interior", sa.String(50), nullable=True),
        sa.Column("neighborhood", sa.String(100), nullable=False),
        sa.Column("city", sa.String(100), nullable=False),
        sa.Column("state", sa.String(100), nullable=False),
        sa.Column("zip_code", sa.String(10), nullable=False),
        sa.Column("is_default", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )

    # New order columns
    op.add_column("orders", sa.Column("address_id", sa.Integer(), sa.ForeignKey("addresses.id", ondelete="SET NULL"), nullable=True))
    op.add_column("orders", sa.Column("shipping_method", sa.String(50), nullable=True))
    op.add_column("orders", sa.Column("shipping_cost", sa.Numeric(10, 2), nullable=False, server_default="0.00"))
    op.add_column("orders", sa.Column("shipping_address_snapshot", sa.Text(), nullable=True))
    op.add_column("orders", sa.Column("notes", sa.Text(), nullable=True))


def downgrade() -> None:
    op.drop_column("orders", "notes")
    op.drop_column("orders", "shipping_address_snapshot")
    op.drop_column("orders", "shipping_cost")
    op.drop_column("orders", "shipping_method")
    op.drop_column("orders", "address_id")
    op.drop_table("addresses")
