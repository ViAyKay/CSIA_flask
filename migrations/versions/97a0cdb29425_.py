"""empty message

Revision ID: 97a0cdb29425
Revises: 7749dd979df2
Create Date: 2023-01-17 10:10:57.737227

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '97a0cdb29425'
down_revision = '7749dd979df2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('borrow', schema=None) as batch_op:
        batch_op.drop_column('daysleft')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('borrow', schema=None) as batch_op:
        batch_op.add_column(sa.Column('daysleft', mysql.INTEGER(), autoincrement=False, nullable=False))

    # ### end Alembic commands ###
