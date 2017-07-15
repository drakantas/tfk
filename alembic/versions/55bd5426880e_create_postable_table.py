"""Create postable table

Revision ID: 55bd5426880e
Revises: c1e0260e5351
Create Date: 2017-07-01 18:55:46.179943

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '55bd5426880e'
down_revision = 'c1e0260e5351'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('postable',
                    sa.Column('id', sa.Integer, primary_key=True, autoincrement=True, index=True),
                    sa.Column('created_at', sa.DateTime, nullable=False),
                    sa.Column('updated_at', sa.DateTime, nullable=False))


def downgrade():
    op.drop_table('postable')
