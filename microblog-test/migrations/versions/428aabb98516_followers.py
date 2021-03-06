"""followers

Revision ID: 428aabb98516
Revises: 6e8d3207fc24
Create Date: 2018-04-03 12:43:31.340158

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '428aabb98516'
down_revision = '6e8d3207fc24'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('followers',
    sa.Column('follower_id', sa.Integer(), nullable=True),
    sa.Column('followed_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['followed_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['follower_id'], ['user.id'], )
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('followers')
    # ### end Alembic commands ###
