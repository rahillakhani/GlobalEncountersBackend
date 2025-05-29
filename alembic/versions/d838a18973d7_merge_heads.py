"""merge heads

Revision ID: d838a18973d7
Revises: 2530ae688365, cb61821d823a
Create Date: 2025-05-28 15:40:00.049437

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd838a18973d7'
down_revision: Union[str, None] = ('2530ae688365', 'cb61821d823a')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
