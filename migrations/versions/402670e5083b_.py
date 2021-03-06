"""empty message

Revision ID: 402670e5083b
Revises: 6108419b2752
Create Date: 2022-01-21 14:23:30.936786

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '402670e5083b'
down_revision = '6108419b2752'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('expense', schema=None) as batch_op:
        batch_op.add_column(sa.Column('date', sa.Date(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('expense', schema=None) as batch_op:
        batch_op.drop_column('date')

    # ### end Alembic commands ###
