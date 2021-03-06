"""empty message

Revision ID: f8ee08b6a29e
Revises: 2bb4b2b6832e
Create Date: 2018-03-19 11:14:27.595877

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f8ee08b6a29e'
down_revision = '2bb4b2b6832e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('bookmark',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('type', sa.Integer(), nullable=True),
    sa.Column('bookmark_entity_id', sa.Integer(), nullable=True),
    sa.Column('state', sa.Integer(), nullable=True),
    sa.Column('created_time', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('bookmark')
    # ### end Alembic commands ###
