"""update_food_log_date_timezone

Revision ID: 86d8c54a2ed5
Revises: ebbf5bcd4110
Create Date: 2024-03-21 10:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '86d8c54a2ed5'
down_revision: Union[str, None] = 'ebbf5bcd4110'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Update food_logs table to ensure date columns have timezone
    op.alter_column('food_logs', 'date',
                    existing_type=sa.DateTime(timezone=True),
                    nullable=True,
                    schema='fnb')
    op.alter_column('food_logs', 'lunch_takenon',
                    existing_type=sa.DateTime(timezone=True),
                    nullable=True,
                    schema='fnb')
    op.alter_column('food_logs', 'dinner_takenon',
                    existing_type=sa.DateTime(timezone=True),
                    nullable=True,
                    schema='fnb')


def downgrade() -> None:
    # No downgrade needed as we're just ensuring timezone support
    pass
