import datetime

from app.ext import db
from enum import Enum
from app.mixins.dict import DictMixin

class TaskStatus(Enum):
    
    NEW = 1
    PROCESSING = 2
    END = 3

class TaskType(Enum):

    ALL = 1
    ASSIGNED_BY_ME = 2
    ASSIGNED_TO_ME = 3

class EntityType(Enum):

    ALERT = 1
    ENTITY = 2 # this means the entity in entity table
    INTELLIGENT_CHART = 3

class AttachmentType(Enum):

    REPORT = 1


class Task(DictMixin, db.Model):

    __tablename__ = 'task'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64))
    # status = db.Column(db.Integer, default = TaskStatus.NEW.value)
    from_uid = db.Column(db.Integer, db.ForeignKey('user.id'))
    due_date = db.Column(db.DateTime)
    created_time = db.Column(db.DateTime, default = datetime.datetime.utcnow())
    updated_time = db.Column(db.DateTime, default = datetime.datetime.utcnow())
    entity = db.Column(db.JSON)
    structure_id = db.Column(db.Integer) 
    description = db.Column(db.Text)

class UserTask(DictMixin, db.Model):
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    task_id = db.Column(db.Integer, db.ForeignKey('task.id'))
    new_reply = db.Column(db.Boolean, default = False)
    status = db.Column(db.Integer, default = TaskStatus.NEW.value)

class Comment(DictMixin, db.Model):
    id = db.Column(db.Integer, primary_key = True)
    task_id = db.Column(db.Integer, db.ForeignKey('task.id'))
    content = db.Column(db.Text(512))
    from_uid = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_time = db.Column(db.DateTime, default = datetime.datetime.utcnow())

class Reply(DictMixin, db.Model):
    id = db.Column(db.Integer, primary_key = True)
    comment_id = db.Column(db.Integer, db.ForeignKey('comment.id'))
    content = db.Column(db.Text(512))
    from_uid = db.Column(db.Integer, db.ForeignKey('user.id'))
    to_uid = db.Column(db.Integer, db.ForeignKey('user.id'))
    at = db.Column(db.String(32))
    created_time = db.Column(db.DateTime, default = datetime.datetime.utcnow())

class CommentAttachment(DictMixin, db.Model):
    id = db.Column(db.Integer, primary_key = True)
    comment_id = db.Column(db.Integer, db.ForeignKey('comment.id'))
    attachment_id = db.Column(db.Integer)
    attachment_type = db.Column(db.Integer, default = AttachmentType.REPORT.value)

