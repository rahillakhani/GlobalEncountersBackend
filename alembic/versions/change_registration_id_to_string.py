"""change_registration_id_to_string

Revision ID: change_registration_id_to_string
Revises: 86d8c54a2ed5
Create Date: 2024-03-21 11:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'change_registration_id_to_string'
down_revision: Union[str, None] = '86d8c54a2ed5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create a temporary column
    op.add_column('food_logs', sa.Column('registration_id_new', sa.String(), nullable=True), schema='fnb')
    
    # Copy data from old column to new column, converting to string
    op.execute("UPDATE fnb.food_logs SET registration_id_new = registration_id::text")
    
    # Drop the old column and its constraints
    op.drop_constraint('food_logs_pkey', 'food_logs', schema='fnb')
    op.drop_column('food_logs', 'registration_id', schema='fnb')
    
    # Rename the new column to the original name
    op.alter_column('food_logs', 'registration_id_new', new_column_name='registration_id', schema='fnb')
    
    # Recreate the primary key constraint
    op.create_primary_key('food_logs_pkey', 'food_logs', ['registration_id', 'date'], schema='fnb')
    
    # Recreate the index
    op.create_index('ix_fnb_food_logs_registration_id', 'food_logs', ['registration_id'], schema='fnb')


def downgrade() -> None:
    # Create a temporary column
    op.add_column('food_logs', sa.Column('registration_id_old', sa.Integer(), nullable=True), schema='fnb')
    
    # Copy data from string column to integer column, converting to integer
    op.execute("UPDATE fnb.food_logs SET registration_id_old = NULLIF(regexp_replace(registration_id, '[^0-9]', '', 'g'), '')::integer")
    
    # Drop the string column and its constraints
    op.drop_constraint('food_logs_pkey', 'food_logs', schema='fnb')
    op.drop_column('food_logs', 'registration_id', schema='fnb')
    
    # Rename the integer column to the original name
    op.alter_column('food_logs', 'registration_id_old', new_column_name='registration_id', schema='fnb')
    
    # Recreate the primary key constraint
    op.create_primary_key('food_logs_pkey', 'food_logs', ['registration_id', 'date'], schema='fnb')
    
    # Recreate the index
    op.create_index('ix_fnb_food_logs_registration_id', 'food_logs', ['registration_id'], schema='fnb') 