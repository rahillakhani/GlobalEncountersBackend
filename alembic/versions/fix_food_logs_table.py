"""fix food logs table

Revision ID: fix_food_logs_table
Revises: add_id_to_error_logs
Create Date: 2024-03-19 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fix_food_logs_table'
down_revision = 'add_id_to_error_logs'
branch_labels = None
depends_on = None


def upgrade():
    # Drop existing primary key constraint
    op.execute('ALTER TABLE fnb.food_logs DROP CONSTRAINT food_logs_pkey')
    
    # Drop the sequence if it exists
    op.execute('DROP SEQUENCE IF EXISTS fnb.food_logs_userid_seq')
    
    # Make registration_id and date not null
    op.alter_column('food_logs', 'registration_id',
                    existing_type=sa.String(),
                    nullable=False,
                    schema='fnb')
    op.alter_column('food_logs', 'date',
                    existing_type=sa.Date(),
                    nullable=False,
                    schema='fnb')
    
    # Drop the userid column entirely (instead of making it nullable)
    op.drop_column('food_logs', 'userid', schema='fnb')
    
    # Create new composite primary key
    op.create_primary_key(
        'food_logs_pkey',
        'food_logs',
        ['registration_id', 'date'],
        schema='fnb'
    )


def downgrade():
    # Drop the composite primary key
    op.execute('ALTER TABLE fnb.food_logs DROP CONSTRAINT food_logs_pkey')
    
    # Make columns nullable again
    op.alter_column('food_logs', 'registration_id',
                    existing_type=sa.String(),
                    nullable=True,
                    schema='fnb')
    op.alter_column('food_logs', 'date',
                    existing_type=sa.Date(),
                    nullable=True,
                    schema='fnb')
    
    # Recreate the original primary key on userid
    op.create_primary_key(
        'food_logs_pkey',
        'food_logs',
        ['userid'],
        schema='fnb'
    )
    
    # Recreate the sequence
    op.execute('CREATE SEQUENCE IF NOT EXISTS fnb.food_logs_userid_seq') 