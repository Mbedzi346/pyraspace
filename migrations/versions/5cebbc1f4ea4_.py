"""empty message

Revision ID: 5cebbc1f4ea4
Revises: fc0e8fe7f1ca
Create Date: 2018-12-04 21:03:52.354977

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '5cebbc1f4ea4'
down_revision = 'fc0e8fe7f1ca'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('order', sa.Column('status', sa.String(length=20), nullable=True))
    op.drop_column('order', 'type')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('order', sa.Column('type', mysql.VARCHAR(length=20), nullable=True))
    op.drop_column('order', 'status')
    # ### end Alembic commands ###
