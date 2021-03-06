"""update models for department and feedback

Revision ID: 62dc20efb287
Revises: be880cdcfc3b
Create Date: 2020-12-05 19:23:47.511290

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '62dc20efb287'
down_revision = 'be880cdcfc3b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('department',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('owner_id', sa.Integer(), nullable=True),
    sa.Column('hospital_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['hospital_id'], ['hospital.id'], ),
    sa.ForeignKeyConstraint(['owner_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_department_id'), 'department', ['id'], unique=False)
    op.create_index(op.f('ix_department_name'), 'department', ['name'], unique=False)
    op.create_table('feedback',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('comment', sa.String(), nullable=True),
    sa.Column('owner_id', sa.Integer(), nullable=True),
    sa.Column('survey_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['owner_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['survey_id'], ['survey.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_feedback_comment'), 'feedback', ['comment'], unique=False)
    op.create_index(op.f('ix_feedback_id'), 'feedback', ['id'], unique=False)
    op.add_column('survey', sa.Column('answers', sa.JSON(), nullable=True))
    op.add_column('survey', sa.Column('department_id', sa.Integer(), nullable=True))
    op.add_column('survey', sa.Column('images', sa.JSON(), nullable=True))
    op.drop_constraint('survey_hospital_id_fkey', 'survey', type_='foreignkey')
    op.create_foreign_key(None, 'survey', 'department', ['department_id'], ['id'])
    op.drop_column('survey', 'hospital_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('survey', sa.Column('hospital_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'survey', type_='foreignkey')
    op.create_foreign_key('survey_hospital_id_fkey', 'survey', 'hospital', ['hospital_id'], ['id'])
    op.drop_column('survey', 'images')
    op.drop_column('survey', 'department_id')
    op.drop_column('survey', 'answers')
    op.drop_index(op.f('ix_feedback_id'), table_name='feedback')
    op.drop_index(op.f('ix_feedback_comment'), table_name='feedback')
    op.drop_table('feedback')
    op.drop_index(op.f('ix_department_name'), table_name='department')
    op.drop_index(op.f('ix_department_id'), table_name='department')
    op.drop_table('department')
    # ### end Alembic commands ###
