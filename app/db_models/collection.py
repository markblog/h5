from app.ext import db
from app.mixins.dict import DictMixin

import datetime

class Collection(db.Model, DictMixin):
	"""docstring for ClassName"""

	__tablename__ = 'collection'

	id = db.Column(db.Integer, primary_key = True)
	user_id = db.Column(db.Integer)
	title = db.Column(db.String(128))
	created_time = db.Column(db.Date, default = datetime.datetime.utcnow())
	updated_time = db.Column(db.DateTime, default = datetime.datetime.utcnow())
	state = db.Column(db.Integer, default = 1)


class CollectionItem(db.Model, DictMixin):

	__tablename__ = 'collection_item'

	id = db.Column(db.Integer, primary_key = True)
	collection_id = db.Column(db.Integer)
	name = db.Column(db.String(256))
	charting_data = db.Column(db.JSON)
	date_key = db.Column(db.Date, default = datetime.datetime.utcnow())
