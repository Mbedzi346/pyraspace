"""Add status column

Revision ID: bfe95ee179f6
Revises: 7f4d0ea353b9
Create Date: 2018-11-25 18:06:46.644946

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bfe95ee179f6'
down_revision = '7f4d0ea353b9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('product', sa.Column('status', sa.String(length=20), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('product', 'status')
    # ### end Alembic commands ###
