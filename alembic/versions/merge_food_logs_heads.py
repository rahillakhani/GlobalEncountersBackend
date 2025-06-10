"""merge food logs heads

Revision ID: merge_food_logs_heads
Revises: fix_food_logs_table, merge_heads
Create Date: 2024-03-19 10:05:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'merge_food_logs_heads'
down_revision = ('fix_food_logs_table', 'merge_heads')
branch_labels = None
depends_on = None


def upgrade():
    pass


def downgrade():
    pass 