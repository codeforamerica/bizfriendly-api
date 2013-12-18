"""Getting rid of rating and request tables.

Revision ID: 23aebf11a765
Revises: 1c7d0970bb93
Create Date: 2013-09-20 11:52:13.610590

"""

# revision identifiers, used by Alembic.
revision = '23aebf11a765'
down_revision = '1c7d0970bb93'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.drop_table('rating')
    op.drop_table('request')


def downgrade():
    op.create_table('rating',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('lesson_or_step', sa.Unicode(), nullable=True),
    sa.Column('lesson_or_step_id', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('rating', sa.Integer(), nullable=True),
    sa.Column('feedback', sa.Unicode(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['bf_user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('request',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.Unicode(), nullable=True),
    sa.Column('description', sa.Unicode(), nullable=True),
    sa.Column('why', sa.Unicode(), nullable=True),
    sa.Column('creator_id', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
