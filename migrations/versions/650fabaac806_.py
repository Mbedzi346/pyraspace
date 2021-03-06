"""empty message

Revision ID: 650fabaac806
Revises: 5cebbc1f4ea4
Create Date: 2018-12-25 17:15:46.997823

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '650fabaac806'
down_revision = '5cebbc1f4ea4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('product', sa.Column('ad_fee_paid', sa.String(length=3), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('product', 'ad_fee_paid')
    # ### end Alembic commands ###
