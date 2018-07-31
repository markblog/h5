"""All assets that asset owner have"""
from app.ext import db
from app.mixins.dict import DictMixin

import datetime


class AlertType(db.Model, DictMixin):
    __tablename__ = 'alert_type'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    category = db.Column(db.String(64))
    subcategory = db.Column(db.String(64))
    template = db.Column(db.JSON)
    group_id = db.Column(db.Integer)

class AlertThreshold(db.Model, DictMixin):

    __tablename__ = 'alert_threshold'

    id = db.Column(db.Integer, primary_key = True)
    alert_type_id = db.Column(db.Integer, db.ForeignKey('alert_type.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    date_key = db.Column(db.Date)
    y_metric = db.Column(db.String(128))
    level = db.Column(db.String(64))
    type = db.Column(db.String(64))
    thresh_number = db.Column(db.Float)
    thresh_diff = db.Column(db.Float)
    period = db.Column(db.Integer)
    description = db.Column(db.JSON)
    activate = db.Column(db.Integer, default = 0)

    
class Alert(DictMixin, db.Model):
    """docstring for ClassName"""
    __tablename__ = 'alert'

    id = db.Column(db.Integer, primary_key = True)
    description = db.Column(db.String(128))
    is_read = db.Column(db.Boolean, default = False)
    date_key = db.Column(db.Date, default = datetime.datetime.utcnow())
    chart_id = db.Column(db.String(64))
    entity_id = db.Column(db.Integer, db.ForeignKey('entity.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'))
    alert_threshold_id = db.Column(db.Integer, db.ForeignKey('alert_threshold.id'))
    alert_type_id = db.Column(db.Integer, db.ForeignKey('alert_type.id'))
        
