"""update_food_logs_primary_key

Revision ID: new_migration_update_food_logs_primary_key
Revises: 86d8c54a2ed5
Create Date: 2024-03-21 12:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'new_migration_update_food_logs_primary_key'
down_revision: Union[str, None] = '86d8c54a2ed5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Drop the existing primary key constraint
    op.drop_constraint('food_logs_pkey', 'food_logs', schema='fnb')
    
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
    
    # Restore the original primary key
    op.create_primary_key(
        'food_logs_pkey',
        'food_logs',
        ['userid'],
        schema='fnb'
    ) 