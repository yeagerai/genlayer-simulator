"""add_hash

Revision ID: 99d3f1bc5a08
Revises: 986d9a6b0dda
Create Date: 2024-09-05 17:03:30.743557

This migration adds a hash column to the transactions table (instead of id) and a transaction_hash column to the transactions_audit table (instead of transaction_id).
It generates proper hashes for existing transactions using the _generate_transaction_hash method.

"""

from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
import rlp
from eth_utils import to_bytes, keccak, is_address
import json

# revision identifiers, used by Alembic.
revision: str = "99d3f1bc5a08"
down_revision: Union[str, None] = "986d9a6b0dda"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def _generate_transaction_hash(
    from_address: str,
    to_address: str,
    data: dict,
    value: float,
    type: int,
    nonce: int,
) -> str:
    from_address_bytes = (
        to_bytes(hexstr=from_address) if is_address(from_address) else None
    )
    to_address_bytes = to_bytes(hexstr=to_address) if is_address(to_address) else None
    data_bytes = to_bytes(text=json.dumps(data))

    tx_elements = [
        from_address_bytes,
        to_address_bytes,
        to_bytes(hexstr=hex(int(value))),
        data_bytes,
        to_bytes(hexstr=hex(type)),
        to_bytes(hexstr=hex(nonce)),
        to_bytes(hexstr=hex(0)),  # gas price (placeholder)
        to_bytes(hexstr=hex(0)),  # gas limit (placeholder)
    ]

    tx_elements = [elem for elem in tx_elements if elem is not None]
    rlp_encoded = rlp.encode(tx_elements)
    hash = "0x" + keccak(rlp_encoded).hex()
    return hash


def upgrade() -> None:
    # Add the new 'hash' column
    op.add_column(
        "transactions", sa.Column("hash", sa.String(length=66), nullable=True)
    )
    op.execute("UPDATE transactions SET nonce = id")

    # Generate proper hashes for existing transactions
    connection = op.get_bind()
    transactions = connection.execute(
        sa.text(
            "SELECT id, from_address, to_address, data, value, type, nonce FROM transactions"
        )
    ).fetchall()

    for transaction in transactions:
        hash = _generate_transaction_hash(
            transaction.from_address,
            transaction.to_address,
            transaction.data,
            float(transaction.value),
            transaction.type,
            transaction.nonce,
        )
        connection.execute(
            sa.text("UPDATE transactions SET hash = :hash WHERE id = :id"),
            {"hash": hash, "id": transaction.id},
        )

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

    # Update transaction_hash in transactions_audit
    op.execute(
        """
        UPDATE transactions_audit
        SET transaction_hash = transactions.hash
        FROM transactions
        WHERE transactions_audit.transaction_id = transactions.id
        """
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
