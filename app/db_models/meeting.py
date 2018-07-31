import datetime

from app.ext import db
from enum import Enum
from app.mixins.dict import DictMixin

class MeetingStatus(Enum):

    NEW = 1
    IN_MEETING = 2
    END = 3

class Meeting(DictMixin, db.Model):

    __tablename__ = 'meeting'

    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(128))
    location = db.Column(db.String(64))
    start_time = db.Column(db.DateTime, default = datetime.datetime.utcnow())
    end_time = db.Column(db.DateTime, default = datetime.datetime.utcnow())
    status = db.Column(db.Integer, default = MeetingStatus.NEW.value)
    entity_id = db.Column(db.Integer, db.ForeignKey('entity.id'))
    organizer_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class MeetingAttendance(db.Model,DictMixin):

    __tablename__ = 'meeting_attendance'

    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    meeting_id = db.Column(db.Integer, db.ForeignKey('meeting.id'))

