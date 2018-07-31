from app.ext import db
from enum import Enum
from app.mixins.dict import DictMixin

import datetime

class MessageType(Enum):
	SYS = 1
	TASK = 2
	COMMENT = 3
	REPLY = 4

class MessageStatus(Enum):
	UNREAD = 1
	ISREAD = 2
	DELETE = 3

class Message(db.Model, DictMixin):

	__tablename__ = 'message'

	id = db.Column(db.Integer, primary_key = True)
	content = db.Column(db.String(128))
	created_time = db.Column(db.DateTime, default = datetime.datetime.utcnow())
	status = db.Column(db.Integer, default = 1)
	to_uid = db.Column(db.Integer)
	from_uid = db.Column(db.Integer)
	type = db.Column(db.Integer)
	message_entity_id = db.Column(db.Integer)