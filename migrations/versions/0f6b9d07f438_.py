"""empty message

Revision ID: 0f6b9d07f438
Revises: 61ef3bc80a9a
Create Date: 2018-03-20 10:36:41.513372

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0f6b9d07f438'
down_revision = '61ef3bc80a9a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('collection',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('title', sa.String(length=128), nullable=True),
    sa.Column('created_time', sa.Date(), nullable=True),
    sa.Column('updated_time', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('collection_item',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('chart_id', sa.Integer(), nullable=True),
    sa.Column('collection_id', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('collection_item')
    op.drop_table('collection')
    # ### end Alembic commands ###
