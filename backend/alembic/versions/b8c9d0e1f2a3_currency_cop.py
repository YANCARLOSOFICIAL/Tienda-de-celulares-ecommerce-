"""default payment currency to COP (Colombia)

Revision ID: b8c9d0e1f2a3
Revises: a7b8c9d0e1f2
Create Date: 2026-08-27
"""
from alembic import op

revision = "b8c9d0e1f2a3"
down_revision = "a7b8c9d0e1f2"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.alter_column("payments", "currency", server_default="COP")
    op.execute("UPDATE payments SET currency = 'COP' WHERE currency = 'MXN'")


def downgrade() -> None:
    op.alter_column("payments", "currency", server_default="MXN")
    op.execute("UPDATE payments SET currency = 'MXN' WHERE currency = 'COP'")
