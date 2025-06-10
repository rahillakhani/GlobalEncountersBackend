"""merge heads

Revision ID: merge_heads
Revises: add_id_to_error_logs, new_migration_fix_food_logs_constraints, add_username_column, new_migration_fix_food_logs_primary_key, new_migration_update_food_logs_primary_key, add_user_columns
Create Date: 2024-03-21 13:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'merge_heads'
down_revision: Union[str, None] = ('add_id_to_error_logs', 'new_migration_fix_food_logs_constraints', 'add_username_column', 'new_migration_fix_food_logs_primary_key', 'new_migration_update_food_logs_primary_key', 'add_user_columns')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass 