"""drop audit logs table

Revision ID: drop_audit_logs_table
Revises: fix_food_logs_table
Create Date: 2024-03-21 11:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'drop_audit_logs_table'
down_revision: Union[str, None] = 'fix_food_logs_table'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Drop the audit_logs table
    op.drop_table('audit_logs', schema='fnb')


def downgrade() -> None:
    # Recreate the audit_logs table
    op.create_table('audit_logs',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=True),
        sa.Column('action', sa.String(), nullable=True),
        sa.Column('entity_type', sa.String(), nullable=True),
        sa.Column('entity_id', sa.String(), nullable=True),
        sa.Column('changes', sa.JSON(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        schema='fnb'
    )
    op.create_index(op.f('ix_fnb_audit_logs_id'), 'audit_logs', ['id'], unique=False, schema='fnb')
    op.create_index(op.f('ix_fnb_audit_logs_user_id'), 'audit_logs', ['user_id'], unique=False, schema='fnb') 