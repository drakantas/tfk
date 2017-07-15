"""Create blog vote table

Revision ID: 76417aa0526a
Revises: b193e817f00a
Create Date: 2017-07-01 19:04:48.307066

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '76417aa0526a'
down_revision = 'b193e817f00a'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('blog_vote',
                    sa.Column('postable_id', sa.Integer, primary_key=True, index=True),
                    sa.Column('author_id', sa.Integer, primary_key=True, index=True),
                    sa.Column('score', sa.SmallInteger, nullable=False, default=3),
                    sa.Column('created_at', sa.DateTime, nullable=False),
                    sa.Column('updated_at', sa.DateTime, nullable=False))

    op.create_foreign_key('blog_vote_postable_id_fk', 'blog_vote', 'postable', ['postable_id'], ['id'],
                          ondelete="CASCADE")

    op.create_foreign_key('blog_vote_author_id_fk', 'blog_vote', 'user', ['author_id'], ['id'],
                          ondelete="CASCADE")


def downgrade():
    op.drop_table('blog_vote')
