"""empty message

Revision ID: f4bdbd0d0f30
Revises: cc05a10449c2
Create Date: 2022-12-29 22:29:11.407736

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f4bdbd0d0f30'
down_revision = 'cc05a10449c2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('borrow', schema=None) as batch_op:
        batch_op.add_column(sa.Column('borrow_date', sa.Date(), nullable=True))
        batch_op.drop_column('date')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('borrow', schema=None) as batch_op:
        batch_op.add_column(sa.Column('date', sa.DATE(), nullable=True))
        batch_op.drop_column('borrow_date')

    # ### end Alembic commands ###