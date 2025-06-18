"""add date to food logs

Revision ID: 2c3f92fb0c29
Revises: cb61821d823a
Create Date: 2024-03-19 10:00:00.000000

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
    # Check if column exists before adding it
    conn = op.get_bind()
    inspector = sa.inspect(conn)
    columns = [col['name'] for col in inspector.get_columns('food_logs', schema='fnb')]
    
    if 'date' not in columns:
        op.add_column('food_logs', sa.Column('date', sa.DateTime(timezone=True), nullable=True), schema='fnb')


def downgrade() -> None:
    # Check if column exists before dropping it
    conn = op.get_bind()
    inspector = sa.inspect(conn)
    columns = [col['name'] for col in inspector.get_columns('food_logs', schema='fnb')]
    
    if 'date' in columns:
        op.drop_column('food_logs', 'date', schema='fnb')
