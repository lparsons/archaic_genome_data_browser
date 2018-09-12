"""add archaic genome data tables

Revision ID: 6c8442b2dd91
Revises: a774a04f4f36
Create Date: 2018-09-11 13:41:35.870373

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6c8442b2dd91'
down_revision = 'a774a04f4f36'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('archaic_analysis_run',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=128), nullable=True),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('publication_doi', sa.String(length=256), nullable=True),
    sa.Column('date', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_archaic_analysis_run_name'), 'archaic_analysis_run', ['name'], unique=True)
    op.create_table('archaic_genome_data',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('sample_id', sa.Integer(), nullable=True),
    sa.Column('archaic_analysis_run_id', sa.Integer(), nullable=True),
    sa.Column('neandertal_bp', sa.Integer(), nullable=True),
    sa.Column('neandertal_haplotypes', sa.Integer(), nullable=True),
    sa.Column('neandertal_sstar_bed', sa.String(length=512), nullable=True),
    sa.Column('denisovan_bp', sa.Integer(), nullable=True),
    sa.Column('denisovan_haplotypes', sa.Integer(), nullable=True),
    sa.Column('denisovan_sstar_bed', sa.String(length=512), nullable=True),
    sa.ForeignKeyConstraint(['archaic_analysis_run_id'], ['archaic_analysis_run.id'], ),
    sa.ForeignKeyConstraint(['sample_id'], ['sample.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('archaic_genome_data')
    op.drop_index(op.f('ix_archaic_analysis_run_name'), table_name='archaic_analysis_run')
    op.drop_table('archaic_analysis_run')
    # ### end Alembic commands ###