"""empty message

Revision ID: f3e5779705f4
Revises: 1ec6cb4131e1
Create Date: 2021-02-25 20:31:53.618727

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f3e5779705f4'
down_revision = '1ec6cb4131e1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('book', sa.Column('image_name', sa.String(length=255), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('book', 'image_name')
    # ### end Alembic commands ###