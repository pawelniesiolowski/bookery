"""empty message

Revision ID: 1ec6cb4131e1
Revises: ee7507f540cb
Create Date: 2020-10-21 17:19:23.432150

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1ec6cb4131e1'
down_revision = 'ee7507f540cb'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('book', sa.Column('publication_year', sa.Numeric(precision=4, scale=0), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('book', 'publication_year')
    # ### end Alembic commands ###
