"""Added roles to users.

Revision ID: 59d92e59df91
Revises: 478a09dd7dd6
Create Date: 2013-09-17 19:57:40.523768

"""

# revision identifiers, used by Alembic.
revision = '59d92e59df91'
down_revision = '478a09dd7dd6'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column('bf_user', sa.Column('role', sa.Unicode(), nullable=True))
    ### end Alembic commands ###


def downgrade():
    op.drop_column('bf_user', 'role')
    ### end Alembic commands ###
