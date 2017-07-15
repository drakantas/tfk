"""Create authenticable table

Revision ID: 8eb157c83e49
Revises: 76417aa0526a
Create Date: 2017-07-12 15:26:47.369692

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8eb157c83e49'
down_revision = '76417aa0526a'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('authenticable',
                    sa.Column('id', sa.Integer, primary_key=True, index=True),
                    sa.Column('token', sa.String(256), primary_key=True, unique=True, index=True),
                    sa.Column('secret', sa.String(64), unique=True, nullable=False))

    op.create_foreign_key('authenticable_id_fk', 'authenticable', 'user', ['id'], ['id'], ondelete="CASCADE")


def downgrade():
    op.drop_table('authenticable')
