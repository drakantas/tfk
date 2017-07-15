"""Create user profile table

Revision ID: c1e0260e5351
Revises: dca1fe78883f
Create Date: 2017-07-01 18:55:13.647606

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c1e0260e5351'
down_revision = 'dca1fe78883f'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('user_profile',
                    sa.Column('id', sa.Integer, primary_key=True, index=True),
                    sa.Column('full_name', sa.String(64), nullable=True),
                    sa.Column('last_name', sa.String(64), nullable=True),
                    sa.Column('age', sa.SmallInteger, nullable=True),
                    sa.Column('gender', sa.SmallInteger, nullable=True, default=0),
                    sa.Column('country', sa.SmallInteger, nullable=True, default=1),
                    sa.Column('created_at', sa.DateTime, nullable=False),
                    sa.Column('updated_at', sa.DateTime, nullable=False))

    op.create_foreign_key('user_profile_id_fk', 'user_profile', 'user', ['id'], ['id'], ondelete="CASCADE")


def downgrade():
    op.drop_table('user_profile')
