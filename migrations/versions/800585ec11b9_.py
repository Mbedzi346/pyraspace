"""empty message

Revision ID: 800585ec11b9
Revises: 571805fda94c
Create Date: 2019-01-02 21:54:16.609276

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '800585ec11b9'
down_revision = '571805fda94c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('admin',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=255), nullable=True),
    sa.Column('password', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('admin')
    # ### end Alembic commands ###
