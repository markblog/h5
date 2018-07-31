"""empty message

Revision ID: b295de5df52c
Revises: c1258116bd07
Create Date: 2018-04-04 17:00:21.563932

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b295de5df52c'
down_revision = 'c1258116bd07'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('alert_threshold', sa.Column('description', sa.JSON(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('alert_threshold', 'description')
    # ### end Alembic commands ###
