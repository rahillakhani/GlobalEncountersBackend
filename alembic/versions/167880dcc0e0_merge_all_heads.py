"""merge_all_heads

Revision ID: 167880dcc0e0
Revises: 20240321100000, change_registration_id_to_string, drop_audit_logs_table, fix_food_logs_for_special_registrations, merge_food_logs_heads
Create Date: 2025-06-14 17:21:36.953893

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '167880dcc0e0'
down_revision: Union[str, None] = ('20240321100000', 'change_registration_id_to_string', 'drop_audit_logs_table', 'fix_food_logs_for_special_registrations', 'merge_food_logs_heads')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
