"""Create user table

Revision ID: dca1fe78883f
Revises: 
Create Date: 2017-07-01 18:54:49.683332

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'dca1fe78883f'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('user',
                    sa.Column('id', sa.Integer, primary_key=True, autoincrement=True, index=True),
                    sa.Column('username', sa.String(16), unique=True, index=True, nullable=False),
                    sa.Column('email', sa.String(64), unique=True, index=True, nullable=False),
                    sa.Column('password', sa.String(128), nullable=False),
                    sa.Column('avatar', sa.Binary, nullable=True),
                    sa.Column('created_at', sa.DateTime, nullable=False),
                    sa.Column('updated_at', sa.DateTime, nullable=False))


def downgrade():
    op.drop_table('user')
