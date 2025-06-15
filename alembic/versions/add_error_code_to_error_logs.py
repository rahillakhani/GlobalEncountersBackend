"""add error_code to error_logs

Revision ID: add_error_code_to_error_logs
Revises: 167880dcc0e0
Create Date: 2024-03-21 16:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'add_error_code_to_error_logs'
down_revision = '167880dcc0e0'
branch_labels = None
depends_on = None


def upgrade():
    # Add error_code column to error_logs table
    op.add_column('error_logs', sa.Column('error_code', sa.String(10), nullable=True), schema='fnb')
    op.create_index(op.f('ix_fnb_error_logs_error_code'), 'error_logs', ['error_code'], unique=False, schema='fnb')


def downgrade():
    # Remove error_code column from error_logs table
    op.drop_index(op.f('ix_fnb_error_logs_error_code'), table_name='error_logs', schema='fnb')
    op.drop_column('error_logs', 'error_code', schema='fnb') 