"""Added owners to lessons and states.

Revision ID: 478a09dd7dd6
Revises: e8bc7cfa219
Create Date: 2013-09-17 19:37:42.580793

"""

# revision identifiers, used by Alembic.
revision = '478a09dd7dd6'
down_revision = 'e8bc7cfa219'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column('lesson', sa.Column('state', sa.Unicode(), nullable=True))
    op.add_column('lesson', sa.Column('creator_id', sa.Integer(), nullable=True))


def downgrade():
    op.drop_column('lesson', 'creator_id')
    op.drop_column('lesson', 'state')