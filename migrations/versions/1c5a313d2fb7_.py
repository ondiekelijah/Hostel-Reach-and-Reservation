"""empty message

Revision ID: 1c5a313d2fb7
Revises: d11f336e2b8d
Create Date: 2021-06-26 12:57:34.523578

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1c5a313d2fb7'
down_revision = 'd11f336e2b8d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('hostel', sa.Column('contact', sa.String(length=10), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('hostel', 'contact')
    # ### end Alembic commands ###