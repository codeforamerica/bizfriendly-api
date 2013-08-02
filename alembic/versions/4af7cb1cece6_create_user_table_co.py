"""Create user table, connection table, user_to_lesson table

Revision ID: 4af7cb1cece6
Revises: 52b9c8f82d15
Create Date: 2013-08-02 14:04:36.383942

"""

# revision identifiers, used by Alembic.
revision = '4af7cb1cece6'
down_revision = '52b9c8f82d15'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table(
		'user',
		sa.Column('id', sa.Integer, primary_key=True),
		sa.Column('email', sa.Unicode(), unique=True, nullable=False),
		sa.Column('password', sa.Unicode(), nullable=False),
		sa.Column('access_token', sa.Unicode(), unique=True, nullable=False)
		)
	op.create_table(
		'connection',
		sa.Column('id', sa.Integer, primary_key=True),
		sa.Column('user_id', sa.Integer, sa.ForeignKey('user.id')),
		sa.Column('service', sa.Unicode(), nullable=False),
		sa.Column('access_token', sa.Unicode(), nullable=False)
		)
	op.create_table(
		'user_to_lesson',
		sa.Column('user_id', sa.Integer, sa.ForeignKey('user.id')),
		sa.Column('lesson_id', sa.Integer, sa.ForeignKey('lesson.id')),
		sa.Column('start_dt', sa.DateTime(timezone=True),
			default=datetime.utcnow()),
		sa.Column('end_dt', sa.DateTime(timezone=True))
		)

def downgrade():
	op.drop_table('user_to_lesson')
	op.drop_table('connection')
	op.drop_table('user')

