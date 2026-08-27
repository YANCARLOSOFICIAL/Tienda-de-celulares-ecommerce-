"""product images gallery (JSON array of URLs)

Revision ID: c9d0e1f2a3b4
Revises: b8c9d0e1f2a3
Create Date: 2026-08-27
"""
from alembic import op
import sqlalchemy as sa

revision = "c9d0e1f2a3b4"
down_revision = "b8c9d0e1f2a3"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "products",
        sa.Column("images", sa.JSON(), nullable=False, server_default=sa.text("'[]'::json")),
    )
    # Sembrar la galería con la imagen principal existente.
    op.execute(
        "UPDATE products SET images = json_build_array(image) WHERE image IS NOT NULL AND image <> ''"
    )


def downgrade() -> None:
    op.drop_column("products", "images")
