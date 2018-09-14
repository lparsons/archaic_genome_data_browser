"""Initial data model

Revision ID: a23e9ade59d4
Revises: 
Create Date: 2018-09-14 16:23:06.175448

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a23e9ade59d4'
down_revision = None
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
    op.create_table('data_source',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=128), nullable=True),
    sa.Column('description', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_data_source_name'), 'data_source', ['name'], unique=True)
    op.create_table('digital_object_identifier',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=128), nullable=True),
    sa.Column('doi', sa.String(length=256), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('doi')
    )
    op.create_index(op.f('ix_digital_object_identifier_name'), 'digital_object_identifier', ['name'], unique=True)
    op.create_table('data_source_doi',
    sa.Column('doi_id', sa.Integer(), nullable=True),
    sa.Column('data_source_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['data_source_id'], ['data_source.id'], ),
    sa.ForeignKeyConstraint(['doi_id'], ['digital_object_identifier.id'], )
    )
    op.create_table('super_population',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('code', sa.String(length=32), nullable=True),
    sa.Column('name', sa.String(length=128), nullable=True),
    sa.Column('data_source_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['data_source_id'], ['data_source.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_super_population_code'), 'super_population', ['code'], unique=True)
    op.create_table('population',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('code', sa.String(length=32), nullable=True),
    sa.Column('name', sa.String(length=128), nullable=True),
    sa.Column('description', sa.String(length=256), nullable=True),
    sa.Column('super_population_id', sa.Integer(), nullable=True),
    sa.Column('data_source_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['data_source_id'], ['data_source.id'], ),
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
    sa.Column('data_source_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['data_source_id'], ['data_source.id'], ),
    sa.ForeignKeyConstraint(['population_id'], ['population.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_sample_code'), 'sample', ['code'], unique=True)
    op.create_index(op.f('ix_sample_family_code'), 'sample', ['family_code'], unique=False)
    op.create_table('archaic_genome_data',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('sample_id', sa.Integer(), nullable=False),
    sa.Column('archaic_analysis_run_id', sa.Integer(), nullable=False),
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
    op.create_index('idx_sample_run', 'archaic_genome_data', ['sample_id', 'archaic_analysis_run_id'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('idx_sample_run', table_name='archaic_genome_data')
    op.drop_table('archaic_genome_data')
    op.drop_index(op.f('ix_sample_family_code'), table_name='sample')
    op.drop_index(op.f('ix_sample_code'), table_name='sample')
    op.drop_table('sample')
    op.drop_index(op.f('ix_population_code'), table_name='population')
    op.drop_table('population')
    op.drop_index(op.f('ix_super_population_code'), table_name='super_population')
    op.drop_table('super_population')
    op.drop_table('data_source_doi')
    op.drop_index(op.f('ix_digital_object_identifier_name'), table_name='digital_object_identifier')
    op.drop_table('digital_object_identifier')
    op.drop_index(op.f('ix_data_source_name'), table_name='data_source')
    op.drop_table('data_source')
    op.drop_index(op.f('ix_archaic_analysis_run_name'), table_name='archaic_analysis_run')
    op.drop_table('archaic_analysis_run')
    # ### end Alembic commands ###
