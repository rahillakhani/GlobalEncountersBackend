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
    # Drop the existing primary key constraint if it exists
    conn = op.get_bind()
    result = conn.execute(sa.text("""
        SELECT constraint_name FROM information_schema.table_constraints
        WHERE table_schema='fnb' AND table_name='food_logs' AND constraint_type='PRIMARY KEY' AND constraint_name='food_logs_pkey'
    """))
    if result.fetchone():
        op.drop_constraint('food_logs_pkey', 'food_logs', schema='fnb')
    
    # Add a new composite primary key if it doesn't exist
    result = conn.execute(sa.text("""
        SELECT constraint_name FROM information_schema.table_constraints
        WHERE table_schema='fnb' AND table_name='food_logs' AND constraint_type='PRIMARY KEY' AND constraint_name='food_logs_pkey'
    """))
    if not result.fetchone():
        op.create_primary_key(
            'food_logs_pkey',
            'food_logs',
            ['userid', 'date'],
            schema='fnb'
        )


def downgrade() -> None:
    # Drop the composite primary key if it exists
    conn = op.get_bind()
    result = conn.execute(sa.text("""
        SELECT constraint_name FROM information_schema.table_constraints
        WHERE table_schema='fnb' AND table_name='food_logs' AND constraint_type='PRIMARY KEY' AND constraint_name='food_logs_pkey'
    """))
    if result.fetchone():
        op.drop_constraint('food_logs_pkey', 'food_logs', schema='fnb')
    
    # Restore the original primary key if it doesn't exist
    result = conn.execute(sa.text("""
        SELECT constraint_name FROM information_schema.table_constraints
        WHERE table_schema='fnb' AND table_name='food_logs' AND constraint_type='PRIMARY KEY' AND constraint_name='food_logs_pkey'
    """))
    if not result.fetchone():
        op.create_primary_key(
            'food_logs_pkey',
            'food_logs',
            ['userid'],
            schema='fnb'
        ) 