"""empty message

Revision ID: 7ca83cf86add
Revises: eaefca1fdf20
Create Date: 2022-02-02 16:17:01.779653

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7ca83cf86add'
down_revision = 'eaefca1fdf20'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('notification',
    sa.Column('T_Number', sa.String(length=10), nullable=False),
    sa.Column('service_date', sa.Date(), nullable=True),
    sa.Column('registration_exp', sa.Date(), nullable=True),
    sa.Column('fitness_exp', sa.Date(), nullable=True),
    sa.Column('carrier_exp', sa.Date(), nullable=True),
    sa.Column('cn_exp', sa.Date(), nullable=True),
    sa.Column('insurance_exp', sa.Date(), nullable=True),
    sa.ForeignKeyConstraint(['T_Number'], ['vehicle.T_Number'], ),
    sa.PrimaryKeyConstraint('T_Number')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('notification')
    # ### end Alembic commands ###
