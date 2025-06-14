"""fix_food_logs_for_special_registrations

Revision ID: fix_food_logs_for_special_registrations
Revises: new_migration_fix_food_logs_primary_key
Create Date: 2024-03-22 10:00:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from app.core.special_registrations import SPECIAL_REGISTRATIONS

# revision identifiers, used by Alembic.
revision: str = 'fix_food_logs_for_special_registrations'
down_revision: Union[str, None] = 'new_migration_fix_food_logs_primary_key'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    # Drop the existing primary key constraint
    op.drop_constraint('food_logs_pkey', 'food_logs', schema='fnb')
    
    # Add an id column as the new primary key
    op.add_column('food_logs', 
                 sa.Column('id', sa.Integer(), nullable=False, server_default=sa.text("nextval('fnb.food_logs_id_seq')")),
                 schema='fnb')
    
    # Create the sequence if it doesn't exist
    op.execute('CREATE SEQUENCE IF NOT EXISTS fnb.food_logs_id_seq')
    
    # Set the new primary key
    op.create_primary_key('food_logs_pkey', 'food_logs', ['id'], schema='fnb')
    
    # Create a unique constraint for non-special registrations
    op.execute("""
        CREATE UNIQUE INDEX food_logs_reg_date_unique 
        ON fnb.food_logs (registration_id, date) 
        WHERE registration_id NOT IN (
            SELECT unnest(ARRAY[%s])::integer
        )
    """ % ','.join(map(str, SPECIAL_REGISTRATIONS.values())))
    
    # Create an index on registration_id and date for faster lookups
    op.create_index('ix_fnb_food_logs_reg_date', 'food_logs', 
                   ['registration_id', 'date'], 
                   schema='fnb')

def downgrade() -> None:
    # Drop the unique constraint
    op.execute('DROP INDEX IF EXISTS fnb.food_logs_reg_date_unique')
    
    # Drop the index
    op.drop_index('ix_fnb_food_logs_reg_date', table_name='food_logs', schema='fnb')
    
    # Drop the id column
    op.drop_column('food_logs', 'id', schema='fnb')
    
    # Drop the sequence
    op.execute('DROP SEQUENCE IF EXISTS fnb.food_logs_id_seq')
    
    # Restore the original composite primary key
    op.create_primary_key('food_logs_pkey', 'food_logs', 
                         ['registration_id', 'date'], 
                         schema='fnb') 