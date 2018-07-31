import datetime
from app.ext import db
from app.mixins.dict import DictMixin

class UserEntity(DictMixin, db.Model):
    __tablename__ = 'user_entity'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    entity_id = db.Column(db.Integer)
    set_id = db.Column(db.Integer)
    created_time = db.Column(db.DateTime, default = datetime.datetime.utcnow())