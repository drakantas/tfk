"""Create blog entry table

Revision ID: cf43553dd11d
Revises: 55bd5426880e
Create Date: 2017-07-01 18:57:33.813699

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cf43553dd11d'
down_revision = '55bd5426880e'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('blog_entry',
                    sa.Column('id', sa.Integer, primary_key=True, index=True),
                    sa.Column('title', sa.String(128), unique=True, nullable=False),
                    sa.Column('slug', sa.String(128), unique=True, index=True, nullable=False),
                    sa.Column('author_id', sa.Integer, nullable=False),
                    sa.Column('body', sa.Text, nullable=False))

    op.create_foreign_key('blog_entry_id_fk', 'blog_entry', 'postable', ['id'], ['id'], ondelete="CASCADE")

    op.create_foreign_key('blog_entry_author_id_fk', 'blog_entry', 'user', ['author_id'], ['id'], ondelete="CASCADE")


def downgrade():
    op.drop_table('blog_entry')
