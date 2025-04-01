"""initial

Revision ID: 65f3ee7f059e
Revises:
Create Date: 2025-04-01 16:20:49.154947

"""

from typing import (
    Sequence,
    Union,
)

import sqlalchemy as sa  # noqa F401

from alembic import op  # noqa F401

# revision identifiers, used by Alembic.
revision: str = "65f3ee7f059e"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
