"""customer status

Revision ID: 4246eec0f167
Revises: a772001240ca
Create Date: 2026-06-21 16:48:00.965059
"""
from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

revision: str = '4246eec0f167'
down_revision: str | None = 'a772001240ca'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        'customers',
        sa.Column('status', sa.String(length=20), server_default='active', nullable=False),
    )
    op.create_check_constraint(
        'ck_customer_status', 'customers', "status in ('active', 'archived')"
    )


def downgrade() -> None:
    op.drop_constraint('ck_customer_status', 'customers', type_='check')
    op.drop_column('customers', 'status')
