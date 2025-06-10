"""add username column to users table

Revision ID: add_username_column
Revises: 948f0b123e23
Create Date: 2024-03-19 10:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'add_username_column'
down_revision: Union[str, None] = '948f0b123e23'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add username column to users table
    op.add_column('users', sa.Column('username', sa.String(100), nullable=True), schema='fnb')
    # Add unique constraint
    op.create_unique_constraint('uq_users_username', 'users', ['username'], schema='fnb')
    # Add index
    op.create_index('ix_fnb_users_username', 'users', ['username'], schema='fnb')


def downgrade() -> None:
    # Remove username column from users table
    op.drop_index('ix_fnb_users_username', table_name='users', schema='fnb')
    op.drop_constraint('uq_users_username', 'users', schema='fnb')
    op.drop_column('users', 'username', schema='fnb') 