"""add ghost contract address column

Revision ID: cb34b6b353ed
Revises: 0d9538be0318
Create Date: 2024-03-19 xx:xx:xx.xxxxxx

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'cb34b6b353ed'
down_revision: Union[str, None] = '0d9538be0318'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('transactions', sa.Column('ghost_contract_address', sa.String(length=255), nullable=True))


def downgrade() -> None:
    op.drop_column('transactions', 'ghost_contract_address')
