"""add_hash

Revision ID: 99d3f1bc5a08
Revises: f9636f013003
Create Date: 2024-09-05 17:03:30.743557

This migration adds a hash column to the transactions table (instead of id) and a transaction_hash column to the transactions_audit table (instead of transaction_id).
To remain backwards compatible and downgradable, the hash and nonce are set to the current id on existing transactions.

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "99d3f1bc5a08"
down_revision: Union[str, None] = "f9636f013003"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add the new 'hash' column
    op.add_column(
        "transactions", sa.Column("hash", sa.String(length=66), nullable=True)
    )

    # Update the 'hash' column with the current 'id' value
    op.execute("UPDATE transactions SET hash = CAST(id AS VARCHAR(255))")
    op.execute("UPDATE transactions SET nonce = id")

    # Set the 'hash' column to not nullable
    op.alter_column("transactions", "hash", nullable=False)

    # Create the unique constraint
    op.create_unique_constraint("uq_transactions_hash", "transactions", ["hash"])

    # Make 'hash' the primary key
    op.execute("ALTER TABLE transactions DROP CONSTRAINT transactions_pkey")
    op.execute("ALTER TABLE transactions ADD PRIMARY KEY (hash)")

    # Add the 'transaction_hash' column to the audit table
    op.add_column(
        "transactions_audit",
        sa.Column("transaction_hash", sa.String(length=66), nullable=True),
    )

    # Use legacy ID as default value for hash column
    op.execute(
        "UPDATE transactions_audit SET transaction_hash = CAST(transaction_id AS VARCHAR(255))"
    )

    # Add foreign key constraint
    op.create_foreign_key(
        "transaction_hash_fkey",
        "transactions_audit",
        "transactions",
        ["transaction_hash"],
        ["hash"],
        ondelete="CASCADE",
    )

    # Delete the id column
    op.drop_column("transactions", "id")
    op.drop_column("transactions_audit", "transaction_id")


def downgrade() -> None:
    # Revert primary key to 'id'
    op.execute("ALTER TABLE transactions DROP CONSTRAINT transactions_pkey")

    # Add 'id' column to transactions table
    op.add_column(
        "transactions", sa.Column("id", sa.INTEGER(), autoincrement=True, nullable=True)
    )

    # Set 'id' to 'nonce' value
    op.execute("UPDATE transactions SET id = nonce")

    # Make 'id' the primary key
    op.execute("ALTER TABLE transactions ADD PRIMARY KEY (id)")

    # Add 'transaction_id' column to transactions_audit table
    op.add_column(
        "transactions_audit",
        sa.Column("transaction_id", sa.INTEGER(), autoincrement=False, nullable=True),
    )

    # Update transaction_id in transactions_audit based on hash
    op.execute(
        """
        UPDATE transactions_audit
        SET transaction_id = transactions.id
        FROM transactions
        WHERE transactions_audit.transaction_hash = transactions.hash
    """
    )

    # Drop the foreign key constraint
    op.drop_constraint(
        "transaction_hash_fkey", "transactions_audit", type_="foreignkey"
    )

    # Drop the transaction_hash column from transactions_audit
    op.drop_column("transactions_audit", "transaction_hash")

    # Drop the hash column and constraint from transactions
    op.drop_constraint("uq_transactions_hash", "transactions", type_="unique")
    op.drop_column("transactions", "hash")

    # Reset nonce to null
    op.execute("UPDATE transactions SET nonce = null")

    # ### end Alembic commands ###
