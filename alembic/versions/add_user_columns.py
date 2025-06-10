"""add missing columns to users table

Revision ID: add_user_columns
Revises: 948f0b123e23
Create Date: 2024-03-19 10:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'add_user_columns'
down_revision: Union[str, None] = '948f0b123e23'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add missing columns to users table
    op.add_column('users', sa.Column('username', sa.String(100), nullable=False), schema='fnb')
    op.add_column('users', sa.Column('email', sa.String(100), nullable=False), schema='fnb')
    op.add_column('users', sa.Column('full_name', sa.String(100), nullable=True), schema='fnb')
    op.add_column('users', sa.Column('password', sa.String(100), nullable=False), schema='fnb')
    op.add_column('users', sa.Column('is_active', sa.Boolean(), nullable=False, server_default='true'), schema='fnb')
    
    # Add unique constraints
    op.create_unique_constraint('uq_users_username', 'users', ['username'], schema='fnb')
    op.create_unique_constraint('uq_users_email', 'users', ['email'], schema='fnb')


def downgrade() -> None:
    # Remove columns from users table
    op.drop_constraint('uq_users_username', 'users', schema='fnb')
    op.drop_constraint('uq_users_email', 'users', schema='fnb')
    op.drop_column('users', 'username', schema='fnb')
    op.drop_column('users', 'email', schema='fnb')
    op.drop_column('users', 'full_name', schema='fnb')
    op.drop_column('users', 'password', schema='fnb')
    op.drop_column('users', 'is_active', schema='fnb') 