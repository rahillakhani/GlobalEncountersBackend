"""fix_food_logs_primary_key

Revision ID: new_migration_fix_food_logs_primary_key
Revises: 86d8c54a2ed5
Create Date: 2024-03-21 12:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'new_migration_fix_food_logs_primary_key'
down_revision: Union[str, None] = '86d8c54a2ed5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Drop the existing primary key constraint and sequence
    op.drop_constraint('food_logs_pkey', 'food_logs', schema='fnb')
    op.execute('DROP SEQUENCE IF EXISTS fnb.food_logs_id_seq')
    
    # Make registration_id and date not null
    op.alter_column('food_logs', 'registration_id',
                    existing_type=sa.Integer(),
                    nullable=False,
                    schema='fnb')
    op.alter_column('food_logs', 'date',
                    existing_type=sa.DateTime(timezone=True),
                    nullable=False,
                    schema='fnb')
    
    # Add new composite primary key
    op.create_primary_key(
        'food_logs_pkey',
        'food_logs',
        ['registration_id', 'date'],
        schema='fnb'
    )


def downgrade() -> None:
    # Drop the composite primary key
    op.drop_constraint('food_logs_pkey', 'food_logs', schema='fnb')
    
    # Create sequence for userid
    op.execute('CREATE SEQUENCE IF NOT EXISTS fnb.food_logs_id_seq')
    
    # Make registration_id and date nullable again
    op.alter_column('food_logs', 'registration_id',
                    existing_type=sa.Integer(),
                    nullable=True,
                    schema='fnb')
    op.alter_column('food_logs', 'date',
                    existing_type=sa.DateTime(timezone=True),
                    nullable=True,
                    schema='fnb')
    
    # Restore original primary key
    op.create_primary_key(
        'food_logs_pkey',
        'food_logs',
        ['userid'],
        schema='fnb'
    ) 