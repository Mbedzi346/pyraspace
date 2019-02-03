"""empty message

Revision ID: a961745b85e8
Revises: b0ef6e7cffd7
Create Date: 2019-01-19 20:58:43.309009

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a961745b85e8'
down_revision = 'b0ef6e7cffd7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('phone_number', sa.String(length=255), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'phone_number')
    # ### end Alembic commands ###
