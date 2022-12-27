"""empty message

Revision ID: c5e243e8d232
Revises: dd5121ac6fc4
Create Date: 2022-12-26 21:32:37.914709

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'c5e243e8d232'
down_revision = 'dd5121ac6fc4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('borrowers')
    with op.batch_alter_table('borrow', schema=None) as batch_op:
        batch_op.drop_constraint('borrow_ibfk_2', type_='foreignkey')
        batch_op.drop_column('borrower_id')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('borrow', schema=None) as batch_op:
        batch_op.add_column(sa.Column('borrower_id', mysql.INTEGER(), autoincrement=False, nullable=True))
        batch_op.create_foreign_key('borrow_ibfk_2', 'borrowers', ['borrower_id'], ['id'])

    op.create_table('borrowers',
    sa.Column('id', mysql.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('first_Name', mysql.VARCHAR(length=255), nullable=False),
    sa.Column('last_Name', mysql.VARCHAR(length=255), nullable=False),
    sa.Column('email', mysql.VARCHAR(length=120), nullable=False),
    sa.Column('apartment_number', mysql.INTEGER(), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id'),
    mysql_collate='utf8mb4_0900_ai_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    # ### end Alembic commands ###
