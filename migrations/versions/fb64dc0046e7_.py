"""empty message

Revision ID: fb64dc0046e7
Revises: 
Create Date: 2018-11-09 22:01:23.207283

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fb64dc0046e7'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('feature',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=64), nullable=True),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('client', sa.String(length=24), nullable=True),
    sa.Column('client_priority', sa.Integer(), nullable=True),
    sa.Column('target_date', sa.DateTime(), nullable=True),
    sa.Column('product_area', sa.String(length=24), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('feature')
    # ### end Alembic commands ###
