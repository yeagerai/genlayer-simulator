"""add plugin and plugin_config to validators

Revision ID: 986d9a6b0dda
Revises: db38e78684a8
Create Date: 2024-09-10 14:47:10.730407

"""

from typing import Sequence, Union

from alembic import op
from sqlalchemy import column, table
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from backend.node.create_nodes.providers import get_default_provider_for

# revision identifiers, used by Alembic.
revision: str = "986d9a6b0dda"
down_revision: Union[str, None] = "db38e78684a8"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("validators", sa.Column("plugin", sa.String(length=255)))
    op.add_column(
        "validators",
        sa.Column("plugin_config", postgresql.JSONB(astext_type=sa.Text())),
    )

    # Modify below

    # Create a table object for the validators table
    validators = table(
        "validators",
        column("id", sa.Integer),
        column("provider", sa.String),
        column("model", sa.String),
        column("plugin", sa.String),
        column("plugin_config", postgresql.JSONB),
        column("config", postgresql.JSONB),
    )

    # Fetch existing data
    conn = op.get_bind()
    results = conn.execute(validators.select())

    # Process data and perform updates
    for validator in results:
        id = validator.id
        provider = validator.provider
        model = validator.model
        default_provider = get_default_provider_for(provider=provider, model=model)
        conn.execute(
            validators.update()
            .where(validators.c.id == id)
            .values(
                plugin=default_provider.plugin,
                plugin_config=default_provider.plugin_config,
                config=default_provider.config,
            )
        )
    # Modify above

    op.alter_column(
        "validators", "plugin", existing_type=sa.VARCHAR(length=255), nullable=False
    )
    op.alter_column(
        "validators",
        "plugin_config",
        existing_type=postgresql.JSONB(astext_type=sa.Text()),
        nullable=False,
    )
    op.alter_column(
        "validators", "provider", existing_type=sa.VARCHAR(length=255), nullable=False
    )
    op.alter_column(
        "validators", "model", existing_type=sa.VARCHAR(length=255), nullable=False
    )


def downgrade() -> None:
    op.alter_column(
        "validators", "model", existing_type=sa.VARCHAR(length=255), nullable=True
    )
    op.alter_column(
        "validators", "provider", existing_type=sa.VARCHAR(length=255), nullable=True
    )
    op.drop_column("validators", "plugin_config")
    op.drop_column("validators", "plugin")
