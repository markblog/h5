"""All assets that asset owner have"""
from app.ext import db
from app.mixins.dict import DictMixin


class EntitySet(db.Model):
    __tablename__ = 'entity_set'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'))
    date_key = db.Column(db.Date)

class Entity(db.Model):

    __tablename__ = 'entity'

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(64))
    name_in_performance = db.Column(db.String(63))
    name_in_risk = db.Column(db.String(63))
    name_in_accounting = db.Column(db.String(63))
    sector_id = db.Column(db.Integer, db.ForeignKey('sector.id'))
    currency_id = db.Column(db.Integer, db.ForeignKey('currency.id'))
    region_id = db.Column(db.Integer, db.ForeignKey('region.id'))
    
class Structure(db.Model):
    """docstring for ClassName"""
    __tablename__ = 'structure'

    id = db.Column(db.Integer, primary_key = True)
    level = db.Column(db.Integer)
    level_name = db.Column(db.String(64))
    parent_id = db.Column(db.Integer)
    benchmark_id = db.Column(db.Integer)
    entity_id = db.Column(db.Integer, db.ForeignKey('entity.id'))
    set_id = db.Column(db.Integer)

class StructureMetricValue(db.Model):
    __tablename__ = 'structure_metric_value'

    id = db.Column(db.Integer, primary_key = True)
    structure_id = db.Column(db.Integer, db.ForeignKey('structure.id'))
    metric_id = db.Column(db.Integer, db.ForeignKey('metric.id'))
    value = db.Column(db.Float)
    date_key = db.Column(db.Date)

class EntityMetricValue(db.Model):
    __tablename__ = 'entity_metric_value'

    id = db.Column(db.Integer, primary_key = True)
    entity_id = db.Column(db.Integer, db.ForeignKey('entity.id'))
    metric_id = db.Column(db.Integer, db.ForeignKey('metric.id'))
    value = db.Column(db.Float)
    date_key = db.Column(db.Date)
