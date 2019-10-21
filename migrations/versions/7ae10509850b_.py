"""empty message

Revision ID: 7ae10509850b
Revises: 28fff5e6002b
Create Date: 2018-06-05 18:04:31.394973

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7ae10509850b'
down_revision = '28fff5e6002b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('alert_type', sa.Column('group_id', sa.Integer(), nullable=True))
    op.add_column('alert_type', sa.Column('subcategory', sa.String(length=64), nullable=True))
    op.drop_column('alert_type', 'period')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('alert_type', sa.Column('period', sa.VARCHAR(length=64), autoincrement=False, nullable=True))
    op.drop_column('alert_type', 'subcategory')
    op.drop_column('alert_type', 'group_id')
    # ### end Alembic commands ###