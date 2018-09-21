"""Add lat and long to population

Revision ID: 2d71ec5904a0
Revises: f75a9ac50ec3
Create Date: 2018-09-21 12:05:53.037421

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2d71ec5904a0'
down_revision = 'f75a9ac50ec3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('population', sa.Column('latitude', sa.Float(), nullable=True))
    op.add_column('population', sa.Column('longitude', sa.Float(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('population', 'longitude')
    op.drop_column('population', 'latitude')
    # ### end Alembic commands ###
