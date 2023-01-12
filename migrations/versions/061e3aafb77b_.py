"""empty message

Revision ID: 061e3aafb77b
Revises: f4bdbd0d0f30
Create Date: 2023-01-12 11:42:02.170989

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '061e3aafb77b'
down_revision = 'f4bdbd0d0f30'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('borrow', schema=None) as batch_op:
        batch_op.alter_column('daysleft',
               existing_type=mysql.INTEGER(),
               nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('borrow', schema=None) as batch_op:
        batch_op.alter_column('daysleft',
               existing_type=mysql.INTEGER(),
               nullable=True)

    # ### end Alembic commands ###
