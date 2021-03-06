"""empty message

Revision ID: 982c68259d3f
Revises: 6542c2f79c0f
Create Date: 2018-02-24 16:48:54.838664

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '982c68259d3f'
down_revision = '6542c2f79c0f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('attachment')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('attachment',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('title', sa.VARCHAR(length=255), autoincrement=False, nullable=True),
    sa.Column('report_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['report_id'], ['report.id'], name='attachment_report_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='attachment_pkey')
    )
    # ### end Alembic commands ###
