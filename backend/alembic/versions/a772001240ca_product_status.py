"""product status

Revision ID: a772001240ca
Revises: cb03d8c3cd00
Create Date: 2026-06-21 16:48:00.619515
"""
from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

revision: str = 'a772001240ca'
down_revision: str | None = 'cb03d8c3cd00'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        'products',
        sa.Column('status', sa.String(length=20), server_default='active', nullable=False),
    )
    op.create_check_constraint(
        'ck_product_status', 'products', "status in ('active', 'archived')"
    )


def downgrade() -> None:
    op.drop_constraint('ck_product_status', 'products', type_='check')
    op.drop_column('products', 'status')
