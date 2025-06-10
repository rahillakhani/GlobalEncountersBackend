"""fix_food_logs_constraints

Revision ID: new_migration_fix_food_logs_constraints
Revises: 86d8c54a2ed5
Create Date: 2024-03-21 13:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'new_migration_fix_food_logs_constraints'
down_revision: Union[str, None] = '86d8c54a2ed5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # First, make sure date is not null for existing records
    op.execute("""
        UPDATE fnb.food_logs 
        SET date = CURRENT_TIMESTAMP 
        WHERE date IS NULL
    """)
    
    # Make date column not null
    op.alter_column('food_logs', 'date',
                    existing_type=sa.DateTime(timezone=True),
                    nullable=False,
                    schema='fnb')
    
    # Drop the existing primary key constraint
    op.drop_constraint('food_logs_pkey', 'food_logs', schema='fnb')
    
    # Drop the sequence since we won't need it anymore
    op.execute('DROP SEQUENCE IF EXISTS fnb.food_logs_id_seq')
    
    # Add a new composite primary key
    op.create_primary_key(
        'food_logs_pkey',
        'food_logs',
        ['userid', 'date'],
        schema='fnb'
    )


def downgrade() -> None:
    # Drop the composite primary key
    op.drop_constraint('food_logs_pkey', 'food_logs', schema='fnb')
    
    # Create the sequence again
    op.execute('CREATE SEQUENCE IF NOT EXISTS fnb.food_logs_id_seq')
    
    # Restore the original primary key
    op.create_primary_key(
        'food_logs_pkey',
        'food_logs',
        ['userid'],
        schema='fnb'
    )
    
    # Make date column nullable again
    op.alter_column('food_logs', 'date',
                    existing_type=sa.DateTime(timezone=True),
                    nullable=True,
                    schema='fnb') 