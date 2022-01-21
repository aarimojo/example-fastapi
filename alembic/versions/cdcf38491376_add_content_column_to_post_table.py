"""add content column to post table

Revision ID: cdcf38491376
Revises: 91a06f0e9a40
Create Date: 2022-01-20 20:23:04.356296

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cdcf38491376'
down_revision = '91a06f0e9a40'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('content', sa.String, nullable=False))


def downgrade():
    op.drop_column('posts', 'content')
