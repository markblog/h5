"""empty message

Revision ID: d75bb81b399a
Revises: 0cccc063c7da
Create Date: 2018-01-29 15:28:14.881306

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd75bb81b399a'
down_revision = '0cccc063c7da'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('alert', sa.Column('description', sa.String(length=128), nullable=True))
    op.drop_column('alert', 'title')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('alert', sa.Column('title', sa.VARCHAR(length=128), autoincrement=False, nullable=True))
    op.drop_column('alert', 'description')
    # ### end Alembic commands ###