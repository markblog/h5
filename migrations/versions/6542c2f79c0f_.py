"""empty message

Revision ID: 6542c2f79c0f
Revises: a8474bc3f0be
Create Date: 2018-02-24 16:47:46.997317

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6542c2f79c0f'
down_revision = 'a8474bc3f0be'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('comment_attachment', sa.Column('attachment_type', sa.Integer(), nullable=True))
    op.drop_constraint('comment_attachment_attachment_id_fkey', 'comment_attachment', type_='foreignkey')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_foreign_key('comment_attachment_attachment_id_fkey', 'comment_attachment', 'attachment', ['attachment_id'], ['id'])
    op.drop_column('comment_attachment', 'attachment_type')
    # ### end Alembic commands ###