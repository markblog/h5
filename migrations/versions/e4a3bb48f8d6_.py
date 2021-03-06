"""empty message

Revision ID: e4a3bb48f8d6
Revises: cf4a6f7b16cf
Create Date: 2018-05-16 20:33:34.483686

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e4a3bb48f8d6'
down_revision = 'cf4a6f7b16cf'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('dashboard', sa.Column('thumbnail', sa.String(length=255), nullable=True))
    op.drop_column('dashboard', 'thumbnail_path')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('dashboard', sa.Column('thumbnail_path', sa.VARCHAR(length=255), autoincrement=False, nullable=True))
    op.drop_column('dashboard', 'thumbnail')
    # ### end Alembic commands ###
