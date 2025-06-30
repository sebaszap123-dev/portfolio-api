"""experience update

Revision ID: 479fe4cd4945
Revises: 60605c556bbd
Create Date: 2025-06-30 13:26:14.861975

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import sqlite

# revision identifiers, used by Alembic.
revision: str = '479fe4cd4945'
down_revision: Union[str, Sequence[str], None] = '60605c556bbd'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    bind = op.get_bind()
    dialect = bind.dialect.name

    if dialect == 'sqlite':
        # SQLite doesn't support DROP COLUMN directly, so we need to:
        # 1. Rename the original table
        op.rename_table('experiences', 'experiences_old')
        
        # 2. Create new table with the desired schema (technologies instead of achievements)
        op.create_table(
            'experiences',
            sa.Column('id', sa.Integer(), primary_key=True),
            sa.Column('title', sa.String(100), nullable=False),
            sa.Column('company', sa.String(100), nullable=False),
            sa.Column('start_date', sa.Date(), nullable=False),
            sa.Column('end_date', sa.Date()),
            sa.Column('is_current', sa.Boolean(), default=False),
            sa.Column('employment_type', sa.String(50)),
            sa.Column('description', sa.String(500)),
            sa.Column('technologies', sqlite.JSON(), nullable=True),
        )

        # 3. Copy data from old table to new table
        op.execute("""
            INSERT INTO experiences (
                id, title, company, start_date, end_date, is_current,
                employment_type, description, technologies
            )
            SELECT 
                id, title, company, start_date, end_date, is_current,
                employment_type, description, NULL as technologies
            FROM experiences_old;
        """)

        # 4. Drop the old table
        op.drop_table('experiences_old')

    else:
        # For other databases that support DROP COLUMN
        op.drop_column('experiences', 'achievements')
        op.add_column('experiences', sa.Column('technologies', sa.JSON(), nullable=True))


def downgrade():
    bind = op.get_bind()
    dialect = bind.dialect.name

    if dialect == 'sqlite':
        # For SQLite, we need to do the table recreation dance again
        # 1. Rename the current table
        op.rename_table('experiences', 'experiences_old')
        
        # 2. Create new table with the original schema (achievements instead of technologies)
        op.create_table(
            'experiences',
            sa.Column('id', sa.Integer(), primary_key=True),
            sa.Column('title', sa.String(100), nullable=False),
            sa.Column('company', sa.String(100), nullable=False),
            sa.Column('start_date', sa.Date(), nullable=False),
            sa.Column('end_date', sa.Date()),
            sa.Column('is_current', sa.Boolean(), default=False),
            sa.Column('employment_type', sa.String(50)),
            sa.Column('description', sa.String(500)),
            sa.Column('achievements', sqlite.JSON(), nullable=True),
        )

        # 3. Copy data from old table to new table
        op.execute("""
            INSERT INTO experiences (
                id, title, company, start_date, end_date, is_current,
                employment_type, description, achievements
            )
            SELECT 
                id, title, company, start_date, end_date, is_current,
                employment_type, description, NULL as achievements
            FROM experiences_old;
        """)

        # 4. Drop the old table
        op.drop_table('experiences_old')

    else:
        # For other databases
        op.drop_column('experiences', 'technologies')
        op.add_column('experiences', sa.Column('achievements', sa.JSON(), nullable=True))