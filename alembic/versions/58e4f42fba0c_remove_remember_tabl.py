"""Remove remember table.

Revision ID: 58e4f42fba0c
Revises: 4af7cb1cece6
Create Date: 2013-08-29 15:52:34.076224

"""

# revision identifiers, used by Alembic.
revision = '58e4f42fba0c'
down_revision = '4af7cb1cece6'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.drop_table('thing_to_remember')


def downgrade():
    op.create_table('thing_to_remember',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('access_token', sa.Unicode(), nullable=True),
    sa.Column('thing_to_remember', sa.Unicode(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )