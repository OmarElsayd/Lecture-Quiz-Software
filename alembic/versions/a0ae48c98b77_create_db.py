"""create_db

Revision ID: a0ae48c98b77
Revises: 
Create Date: 2023-01-14 19:59:17.143811

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'a0ae48c98b77'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('answer_lists',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('first_answer', sa.String(length=50), nullable=True),
    sa.Column('second_answer', sa.String(length=50), nullable=True),
    sa.Column('third_answer', sa.String(length=50), nullable=True),
    sa.Column('fourth_answer', sa.String(length=50), nullable=True),
    sa.Column('created', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    schema='lqs'
    )
    op.create_table('lectures',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=True),
    sa.Column('created', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    schema='lqs'
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=True),
    sa.Column('email', sa.String(length=50), nullable=True),
    sa.Column('password', sa.String(length=50), nullable=True),
    sa.Column('role', postgresql.ENUM('Instructor', 'Student', name='role'), nullable=True),
    sa.Column('created', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    schema='lqs'
    )
    op.create_table('quizzes',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('quiz_name', sa.String(length=50), nullable=True),
    sa.Column('quiz_type', postgresql.ENUM('MultipleChoice', name='quiztype'), nullable=True),
    sa.Column('number_of_questions', sa.Integer(), nullable=True),
    sa.Column('quiz_duration', sa.Integer(), nullable=True),
    sa.Column('lecture_id', sa.Integer(), nullable=False),
    sa.Column('created', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['lecture_id'], ['lqs.lectures.id'], ),
    sa.PrimaryKeyConstraint('id'),
    schema='lqs'
    )
    op.create_table('questions',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('question', sa.String(length=50), nullable=True),
    sa.Column('correct_answer', sa.String(length=50), nullable=True),
    sa.Column('answer_list_id', sa.Integer(), nullable=False),
    sa.Column('quiz_id', sa.Integer(), nullable=False),
    sa.Column('created', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['answer_list_id'], ['lqs.answer_lists.id'], ),
    sa.ForeignKeyConstraint(['quiz_id'], ['lqs.quizzes.id'], ),
    sa.PrimaryKeyConstraint('id'),
    schema='lqs'
    )
    op.create_table('scores',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('quiz_id', sa.Integer(), nullable=False),
    sa.Column('score', sa.Integer(), nullable=True),
    sa.Column('created', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['quiz_id'], ['lqs.quizzes.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['lqs.users.id'], ),
    sa.PrimaryKeyConstraint('id'),
    schema='lqs'
    )
    op.create_table('responses',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('question_id', sa.Integer(), nullable=False),
    sa.Column('answer', sa.String(length=50), nullable=True),
    sa.Column('correct', sa.Boolean(), nullable=True),
    sa.Column('created', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['question_id'], ['lqs.questions.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['lqs.users.id'], ),
    sa.PrimaryKeyConstraint('id'),
    schema='lqs'
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('responses', schema='lqs')
    op.drop_table('scores', schema='lqs')
    op.drop_table('questions', schema='lqs')
    op.drop_table('quizzes', schema='lqs')
    op.drop_table('users', schema='lqs')
    op.drop_table('lectures', schema='lqs')
    op.drop_table('answer_lists', schema='lqs')
    # ### end Alembic commands ###
