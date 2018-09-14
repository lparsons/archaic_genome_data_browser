from archaic_genome_data_browser import db
from sqlalchemy.orm import column_property
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy import select, func


class Sample(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(32), index=True, unique=True)
    family_code = db.Column(db.String(32), index=True)
    gender = db.Column(db.String(32))
    family_relationship = db.Column(db.String(128))
    comments = db.Column(db.Text)
    population_id = db.Column(db.Integer, db.ForeignKey('population.id'))
    archaic_genome_data = db.relationship('ArchaicGenomeData',
                                          backref='sample',
                                          lazy='dynamic')

    def __repr__(self):
        return '<Sample {}>'.format(self.code)


class Population(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(32), index=True, unique=True)
    name = db.Column(db.String(128), unique=True)
    description = db.Column(db.String(256))
    super_population_id = db.Column(db.Integer,
                                    db.ForeignKey('super_population.id'))
    samples = db.relationship('Sample', backref='population', lazy='dynamic')

    sample_count = column_property(
        select([func.count(Sample.id)]).
        where(Sample.population_id == id).
        correlate_except(Sample)
    )

    def __repr__(self):
        return '<Population {}>'.format(self.code)


class SuperPopulation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(32), index=True, unique=True)
    name = db.Column(db.String(128))
    populations = db.relationship('Population',
                                  backref='super_population',
                                  lazy='dynamic')

    # TODO Make this a hybrid_property?
    def samples(self):
        samples = set()
        for population in self.populations:
            for sample in population.samples:
                samples.add(sample)
        return samples

    population_count = column_property(
        select([func.count(Population.id)]).
        where(Population.super_population_id == id).
        correlate_except(Population)
    )

    sample_count = column_property(
        select([func.count(Sample.id)]).
        select_from(Population.__table__.join(Sample.__table__)).
        where(Population.super_population_id == id).
        correlate_except(Sample)
    )

    def __repr__(self):
        return '<Sample {}>'.format(self.code)


class ArchaicAnalysisRun(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), index=True, unique=True)
    description = db.Column(db.Text)
    publication_doi = db.Column(db.String(256))
    date = db.Column(db.DateTime)
    archaic_genome_data = db.relationship('ArchaicGenomeData',
                                          backref='archaic_analysis_run',
                                          lazy='dynamic')

    @hybrid_property
    def publication_url(self):
        publication_url = None
        if self.publication_doi is not None:
            publication_url = "https://doi.org/{}".foramt(self.publication_doi)
        return publication_url

    def __repr__(self):
        return '<ArchaicAnalysisRun {}>'.format(self.name)


class ArchaicGenomeData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sample_id = db.Column(db.Integer, db.ForeignKey('sample.id'),
                          nullable=False)
    archaic_analysis_run_id = db.Column(
        db.Integer, db.ForeignKey('archaic_analysis_run.id'),
        nullable=False)
    __table_args__ = (
        db.Index('idx_sample_run', 'sample_id',
                 'archaic_analysis_run_id', unique=True),
    )
    neandertal_bp = db.Column(db.Integer)
    neandertal_haplotypes = db.Column(db.Integer)
    neandertal_sstar_bed = db.Column(db.String(512))
    denisovan_bp = db.Column(db.Integer)
    denisovan_haplotypes = db.Column(db.Integer)
    denisovan_sstar_bed = db.Column(db.String(512))

    def __repr__(self):
        return '<ArchaicGenomeData {}:{}>'.format(
            self.sample.code, self.archaic_analysis_run.name)


def get_one_or_create(session, model, create_method='',
                      create_method_kwargs=None, **kwargs):
    try:
        return session.query(model).filter_by(**kwargs).one(), False
    except NoResultFound:
        kwargs.update(create_method_kwargs or {})
        created = getattr(model, create_method, model)(**kwargs)
        try:
            session.add(created)
            session.flush()
            return created, True
        except IntegrityError:
            session.rollback()
            return session.query(model).filter_by(**kwargs).one(), False
