"""add missing columns to users table

Revision ID: add_user_columns
Revises: 948f0b123e23
Create Date: 2024-03-19 09:30:00.000000

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
    # Check if columns exist before adding them
    conn = op.get_bind()
    inspector = sa.inspect(conn)
    columns = [col['name'] for col in inspector.get_columns('users', schema='fnb')]
    
    if 'username' not in columns:
        op.add_column('users', sa.Column('username', sa.String(100), nullable=False), schema='fnb')
    
    if 'email' not in columns:
        op.add_column('users', sa.Column('email', sa.String(100), nullable=True), schema='fnb')
    
    if 'phone' not in columns:
        op.add_column('users', sa.Column('phone', sa.String(20), nullable=True), schema='fnb')


def downgrade() -> None:
    # Check if columns exist before dropping them
    conn = op.get_bind()
    inspector = sa.inspect(conn)
    columns = [col['name'] for col in inspector.get_columns('users', schema='fnb')]
    
    if 'username' in columns:
        op.drop_column('users', 'username', schema='fnb')
    
    if 'email' in columns:
        op.drop_column('users', 'email', schema='fnb')
    
    if 'phone' in columns:
        op.drop_column('users', 'phone', schema='fnb') 