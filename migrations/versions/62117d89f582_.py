"""empty message

Revision ID: 62117d89f582
Revises: 5a89e97e9b7e
Create Date: 2022-12-17 18:38:38.103366

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '62117d89f582'
down_revision = '5a89e97e9b7e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('book',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=255), nullable=False),
    sa.Column('synopsis', sa.Text(), nullable=True),
    sa.Column('cover_image', sa.BLOB(), nullable=False),
    sa.Column('available', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('superuser', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('borrow',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('book_id', sa.Integer(), nullable=True),
    sa.Column('return_date', sa.Date(), nullable=False),
    sa.ForeignKeyConstraint(['book_id'], ['book.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('borrow')
    op.drop_table('users')
    op.drop_table('book')
    # ### end Alembic commands ###
