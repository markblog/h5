import datetime

from app.ext import db
from enum import Enum
from app.mixins.dict import DictMixin

class BookmarkType(Enum):
    ALERTS = 1
    ASSETS = 2
    ANALYTICS = 3
    REPORTS = 4

class Bookmark(DictMixin, db.Model):
    __tablename__ = 'bookmark'

    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.Integer)
    bookmark_entity_id = db.Column(db.Integer)
    state = db.Column(db.Integer, default = 1) # 1 in use  ; 0 deleted
    created_time = db.Column(db.DateTime, default = datetime.datetime.utcnow())