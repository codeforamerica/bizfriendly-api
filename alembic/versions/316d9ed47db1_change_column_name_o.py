"""Change column name on user_to_lesson

Revision ID: 316d9ed47db1
Revises: 530c0d70d57d
Create Date: 2013-11-01 14:56:51.205741

"""

# revision identifiers, used by Alembic.
revision = '316d9ed47db1'
down_revision = '530c0d70d57d'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user_to_lesson', sa.Column('recent_step_id', sa.Integer(), nullable=True))
    op.drop_column('user_to_lesson', u'recent_step')
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user_to_lesson', sa.Column(u'recent_step', sa.INTEGER(), nullable=True))
    op.drop_column('user_to_lesson', 'recent_step_id')
    ### end Alembic commands ###