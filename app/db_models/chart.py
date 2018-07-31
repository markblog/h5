import datetime

from app.ext import db
from enum import Enum
from app.mixins.dict import DictMixin

class ChartInsight(DictMixin, db.Model):
	__tablename__ = 'chart_insight'

	chart_id = db.Column(db.String(255), primary_key=True)
	user_id = db.Column(db.Integer)
	insight = db.Column(db.Text)
	is_show_original = db.Column(db.Integer, default = 1)
	create_time = db.Column(db.DateTime, default = datetime.datetime.utcnow())
	updated_time = db.Column(db.DateTime, default = datetime.datetime.utcnow())

class ChartComment(DictMixin, db.Model):
	__tablename__ = 'chart_comment'

	id = db.Column(db.Integer, primary_key=True)
	chart_id = db.Column(db.String(255))
	user_id = db.Column(db.Integer)
	comment = db.Column(db.String(255))
	create_time = db.Column(db.DateTime, default = datetime.datetime.utcnow())
