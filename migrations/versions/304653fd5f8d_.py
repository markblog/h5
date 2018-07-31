"""empty message

Revision ID: 304653fd5f8d
Revises: 51ab28b87402
Create Date: 2018-01-30 09:24:43.427527

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '304653fd5f8d'
down_revision = '51ab28b87402'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('meeting', sa.Column('status', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('meeting', 'status')
    # ### end Alembic commands ###
