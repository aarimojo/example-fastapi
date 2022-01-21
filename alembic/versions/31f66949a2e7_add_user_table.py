"""add user table

Revision ID: 31f66949a2e7
Revises: cdcf38491376
Create Date: 2022-01-20 20:27:42.841435

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '31f66949a2e7'
down_revision = 'cdcf38491376'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('users',
        sa.Column('id', sa.Integer, nullable=False),
        sa.Column('email', sa.String, nullable=False),
        sa.Column('password', sa.String, nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), 
            nullable=False, server_default=sa.text('NOW()')),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email'))


def downgrade():
    op.drop_table('users')
