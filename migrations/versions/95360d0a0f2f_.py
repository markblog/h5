"""empty message

Revision ID: 95360d0a0f2f
Revises: e4a3bb48f8d6
Create Date: 2018-05-29 10:53:38.591096

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '95360d0a0f2f'
down_revision = 'e4a3bb48f8d6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('alert_type', sa.Column('Template', sa.JSON(), nullable=True))
    op.add_column('alert_type', sa.Column('category', sa.String(length=64), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('alert_type', 'category')
    op.drop_column('alert_type', 'Template')
    # ### end Alembic commands ###
