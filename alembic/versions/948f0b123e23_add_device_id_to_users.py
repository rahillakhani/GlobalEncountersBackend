"""add device_id to users

Revision ID: 948f0b123e23
Revises: cb61821d823a
Create Date: 2024-03-19 10:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '948f0b123e23'
down_revision: Union[str, None] = 'cb61821d823a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add device_id column to users table
    op.add_column('users', sa.Column('device_id', sa.String(100), nullable=True), schema='fnb')


def downgrade() -> None:
    # Remove device_id column from users table
    op.drop_column('users', 'device_id', schema='fnb')
