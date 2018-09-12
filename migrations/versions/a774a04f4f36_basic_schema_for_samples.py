"""basic schema for samples

Revision ID: a774a04f4f36
Revises: 
Create Date: 2018-09-06 15:47:41.679466

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a774a04f4f36'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('super_population',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('code', sa.String(length=32), nullable=True),
    sa.Column('name', sa.String(length=128), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_super_population_code'), 'super_population', ['code'], unique=True)
    op.create_table('population',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('code', sa.String(length=32), nullable=True),
    sa.Column('name', sa.String(length=128), nullable=True),
    sa.Column('description', sa.String(length=256), nullable=True),
    sa.Column('super_population_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['super_population_id'], ['super_population.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_index(op.f('ix_population_code'), 'population', ['code'], unique=True)
    op.create_table('sample',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('code', sa.String(length=32), nullable=True),
    sa.Column('family_code', sa.String(length=32), nullable=True),
    sa.Column('gender', sa.String(length=32), nullable=True),
    sa.Column('family_relationship', sa.String(length=128), nullable=True),
    sa.Column('comments', sa.Text(), nullable=True),
    sa.Column('population_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['population_id'], ['population.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_sample_code'), 'sample', ['code'], unique=True)
    op.create_index(op.f('ix_sample_family_code'), 'sample', ['family_code'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_sample_family_code'), table_name='sample')
    op.drop_index(op.f('ix_sample_code'), table_name='sample')
    op.drop_table('sample')
    op.drop_index(op.f('ix_population_code'), table_name='population')
    op.drop_table('population')
    op.drop_index(op.f('ix_super_population_code'), table_name='super_population')
    op.drop_table('super_population')
    # ### end Alembic commands ###