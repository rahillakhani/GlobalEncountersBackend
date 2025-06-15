"""add_date_to_food_logs

Revision ID: 2c3f92fb0c29
Revises: cb61821d823a
Create Date: 2024-03-21 10:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2c3f92fb0c29'
down_revision: Union[str, None] = 'cb61821d823a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add date column to food_logs table, but only if it doesn't already exist
    conn = op.get_bind()
    result = conn.execute(sa.text("""
        SELECT column_name FROM information_schema.columns
        WHERE table_schema='fnb' AND table_name='food_logs' AND column_name='date'
    """))
    if not result.fetchone():
    op.add_column('food_logs', sa.Column('date', sa.DateTime(timezone=True), nullable=True), schema='fnb')
    op.create_index(op.f('ix_fnb_food_logs_date'), 'food_logs', ['date'], unique=False, schema='fnb')


def downgrade() -> None:
    # Remove date column from food_logs table, but only if it exists
    conn = op.get_bind()
    result = conn.execute(sa.text("""
        SELECT column_name FROM information_schema.columns
        WHERE table_schema='fnb' AND table_name='food_logs' AND column_name='date'
    """))
    if result.fetchone():
    op.drop_index(op.f('ix_fnb_food_logs_date'), table_name='food_logs', schema='fnb')
    op.drop_column('food_logs', 'date', schema='fnb')
