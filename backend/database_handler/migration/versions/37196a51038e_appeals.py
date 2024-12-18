"""appeals

Revision ID: 37196a51038e
Revises: 1daddff774b2
Create Date: 2024-10-25 17:39:00.130046

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "37196a51038e"
down_revision: Union[str, None] = "1daddff774b2"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(
        "rollup_transactions_hash", "rollup_transactions", ["transaction_hash"]
    )
    op.add_column("transactions", sa.Column("appealed", sa.Boolean(), nullable=True))
    op.add_column(
        "transactions", sa.Column("timestamp_accepted", sa.BigInteger(), nullable=True)
    )
    op.add_column(
        "transactions",
        sa.Column("ghost_contract_address", sa.String(length=255), nullable=True),
    )
    # Set all existing 'appealed' values to False
    op.execute("UPDATE transactions SET appealed = FALSE WHERE appealed IS NULL")
    # Set all existing 'timestamp_accepted' values to 0
    op.execute(
        "UPDATE transactions SET timestamp_accepted = 0 WHERE timestamp_accepted IS NULL"
    )
    # Set all existing 'ghost_contract_address' values to an empty string
    op.execute(
        "UPDATE transactions SET ghost_contract_address = '' WHERE ghost_contract_address IS NULL"
    )
    # Alter the columns to be not nullable
    op.alter_column("transactions", "appealed", nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("transactions", "ghost_contract_address")
    op.drop_column("transactions", "timestamp_accepted")
    op.drop_column("transactions", "appealed")
    op.drop_constraint(
        "rollup_transactions_hash", "rollup_transactions", type_="unique"
    )
    # ### end Alembic commands ###
