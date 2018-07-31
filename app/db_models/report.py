# models for report
import datetime
from app.ext import db
from enum import Enum
from app.mixins.dict import DictMixin

class ReportType(Enum):
    
    ALL = 1
    ONEOFF = 2
    SCHEDULED = 3

class ReportTemplate(DictMixin, db.Model):

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(128))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_time = db.Column(db.DateTime, default = datetime.datetime.utcnow())
    updated_time = db.Column(db.DateTime, default = datetime.datetime.utcnow())
    frequency = db.Column(db.Integer, default = 7)
    current_cycle_left = db.Column(db.Integer, default = 7)
    template = db.Column(db.JSON)
    is_delete = db.Column(db.Boolean, default = False)
    thumbnail = db.Column(db.String(256))



class Report(DictMixin, db.Model):

    id  = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(64))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    path = db.Column(db.String(256))
    data = db.Column(db.JSON)
    report_template_id = db.Column(db.Integer, db.ForeignKey('report_template.id',ondelete='CASCADE'))
    report_type_id = db.Column(db.Integer, default = ReportType.ONEOFF.value)
    updated_time = db.Column(db.DateTime, default = datetime.datetime.utcnow())
    created_time = db.Column(db.DateTime, default = datetime.datetime.utcnow())
    is_delete = db.Column(db.Boolean, default = False)
    thumbnail = db.Column(db.String(256))
    
    report_template = db.relationship('ReportTemplate', foreign_keys = report_template_id)


