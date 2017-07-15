"""Create blog comment table

Revision ID: b193e817f00a
Revises: cf43553dd11d
Create Date: 2017-07-01 19:01:12.333814

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b193e817f00a'
down_revision = 'cf43553dd11d'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('blog_comment',
                    sa.Column('id', sa.Integer, primary_key=True, index=True),
                    sa.Column('author_id', sa.Integer, primary_key=True, index=True),
                    sa.Column('body', sa.Text, nullable=False))

    op.create_foreign_key('blog_comment_id_fk', 'blog_comment', 'postable', ['id'], ['id'], ondelete="CASCADE")

    op.create_foreign_key('blog_comment_author_id_fk', 'blog_comment', 'user', ['author_id'], ['id'],
                          ondelete="CASCADE")


def downgrade():
    op.drop_table('blog_comment')
