from app.ext import db
from enum import Enum
from app.mixins.dict import DictMixin

class DashboardType(Enum):

    ANALYTICS = 1
    FUSION = 2

class Dashboard(DictMixin, db.Model):
    """
    general dashboard concept in app, it havn't decided by the filters or the other conditions
    """
    __tablename__ = 'dashboard'

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(255))
    path = db.Column(db.String(255)) # name parameter in front-end
    site_root = db.Column(db.String(255))
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'))
    thumbnail = db.Column(db.String(255))
    icon = db.Column(db.String(31))
    date_key = db.Column(db.Date)
    description = db.Column(db.String(256))
    type = db.Column(db.Integer, default = DashboardType.ANALYTICS.value)


class DashboardFiltered(DictMixin, db.Model):

    __tablename__ = 'dashboard_filtered'
    """
    In our application, the dashboards also have the different filters on it, to get the conrresponding data, 
    we need to give the filter by default in some scenario,and show them on the UI
    here is the class which have the specific filter of the dashboard and also connected with the entity
    """
    id = db.Column(db.Integer, primary_key = True)
    dashboard_id = db.Column(db.Integer, db.ForeignKey('dashboard.id'))
    entity_id = db.Column(db.Integer, db.ForeignKey('entity.id'))
    filters = db.Column(db.String(1023))
    dashboard = db.relationship('Dashboard',foreign_keys = dashboard_id)