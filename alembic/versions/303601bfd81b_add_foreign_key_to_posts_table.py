"""add foreign-key to posts table

Revision ID: 303601bfd81b
Revises: 31f66949a2e7
Create Date: 2022-01-20 20:37:00.447474

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '303601bfd81b'
down_revision = '31f66949a2e7'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('owner_id', sa.Integer, nullable=False))
    op.create_foreign_key('posts_users_fk', source_table='posts',
                            referent_table='users', local_cols=['owner_id'],
                            remote_cols=['id'], ondelete='CASCADE')


def downgrade():
    op.drop_constraint('posts_users_fk', table_name='posts')
    op.drop_column('posts', 'owner_id')
