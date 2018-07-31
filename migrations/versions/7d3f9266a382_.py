"""empty message

Revision ID: 7d3f9266a382
Revises: 24a8710d8ed2
Create Date: 2018-01-17 10:57:15.152812

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7d3f9266a382'
down_revision = '24a8710d8ed2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('entity_set', sa.Column('group_id', sa.Integer(), nullable=True))
    op.drop_constraint('entity_set_owner_id_fkey', 'entity_set', type_='foreignkey')
    op.create_foreign_key(None, 'entity_set', 'group', ['group_id'], ['id'])
    op.drop_column('entity_set', 'owner_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('entity_set', sa.Column('owner_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'entity_set', type_='foreignkey')
    op.create_foreign_key('entity_set_owner_id_fkey', 'entity_set', 'group', ['owner_id'], ['id'])
    op.drop_column('entity_set', 'group_id')
    # ### end Alembic commands ###
