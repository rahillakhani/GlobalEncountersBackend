"""add_id_to_error_logs

Revision ID: add_id_to_error_logs
Revises: 86d8c54a2ed5
Create Date: 2024-03-21 10:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'add_id_to_error_logs'
down_revision: Union[str, None] = '86d8c54a2ed5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add id column to error_logs table
    op.add_column('error_logs', sa.Column('id', sa.Integer(), nullable=False, server_default='1'), schema='fnb')
    op.create_index(op.f('ix_fnb_error_logs_id'), 'error_logs', ['id'], unique=True, schema='fnb')
    
    # Make id the primary key
    op.execute('ALTER TABLE fnb.error_logs ADD PRIMARY KEY (id)')
    
    # Create sequence for id
    op.execute('CREATE SEQUENCE IF NOT EXISTS fnb.error_logs_id_seq')
    op.execute('ALTER TABLE fnb.error_logs ALTER COLUMN id SET DEFAULT nextval(\'fnb.error_logs_id_seq\')')
    op.execute('ALTER SEQUENCE fnb.error_logs_id_seq OWNED BY fnb.error_logs.id')


def downgrade() -> None:
    # Remove id column from error_logs table
    op.drop_index(op.f('ix_fnb_error_logs_id'), table_name='error_logs', schema='fnb')
    op.drop_column('error_logs', 'id', schema='fnb')
    op.execute('DROP SEQUENCE IF EXISTS fnb.error_logs_id_seq') 