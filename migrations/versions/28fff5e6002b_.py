"""empty message

Revision ID: 28fff5e6002b
Revises: 95360d0a0f2f
Create Date: 2018-05-29 10:56:18.150766

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '28fff5e6002b'
down_revision = '95360d0a0f2f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('alert_type', sa.Column('template', sa.JSON(), nullable=True))
    op.drop_column('alert_type', 'Template')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('alert_type', sa.Column('Template', postgresql.JSON(astext_type=sa.Text()), autoincrement=False, nullable=True))
    op.drop_column('alert_type', 'template')
    # ### end Alembic commands ###
