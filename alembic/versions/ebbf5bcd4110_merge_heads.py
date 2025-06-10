"""merge_heads

Revision ID: ebbf5bcd4110
Revises: 2c3f92fb0c29, 948f0b123e23
Create Date: 2025-06-04 23:48:43.135237

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ebbf5bcd4110'
down_revision: Union[str, None] = ('2c3f92fb0c29', '948f0b123e23')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
