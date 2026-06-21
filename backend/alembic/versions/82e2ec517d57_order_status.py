"""order status

Revision ID: 82e2ec517d57
Revises: 4246eec0f167
Create Date: 2026-06-21 16:48:01.290798
"""
from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

revision: str = '82e2ec517d57'
down_revision: str | None = '4246eec0f167'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        'orders',
        sa.Column('status', sa.String(length=20), server_default='active', nullable=False),
    )
    op.create_check_constraint(
        'ck_order_status', 'orders', "status in ('active', 'cancelled')"
    )


def downgrade() -> None:
    op.drop_constraint('ck_order_status', 'orders', type_='check')
    op.drop_column('orders', 'status')
