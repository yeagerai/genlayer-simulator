"""add transactions audit table and transactions 'status' field

Revision ID: 188ca1c3a340
Revises:
Create Date: 2024-06-27 10:34:24.161235

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "188ca1c3a340"
down_revision: Union[str, None] = "953de60a1dd8"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


transaction_status = postgresql.ENUM(
    "PENDING",
    "CANCELED",
    "PROPOSING",
    "COMMITTING",
    "REVEALING",
    "ACCEPTED",
    "FINALIZED",
    "UNDETERMINED",
    name="transaction_status",
)


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "transactions_audit",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("transaction_id", sa.Integer(), nullable=True),
        sa.Column("data", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=True,
        ),
        sa.PrimaryKeyConstraint("id", name="transactions_audit_pkey"),
    )

    transaction_status.create(op.get_bind(), checkfirst=True)

    op.add_column(
        "transactions",
        sa.Column(
            "status",
            transaction_status,
            server_default=sa.text("'PENDING'::transaction_status"),
            nullable=True,
        ),
    )


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("transactions", "status")
    op.drop_table("transactions_audit")
    # ### end Alembic commands ###
