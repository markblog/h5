import datetime

from flask import g
from app.ext import raw_db, db
from app.sqls import task_sqls
from app.utils.time_utils import datetime_to_timestamp
from app.db_models.task import Task, UserTask, EntityType, Comment, CommentAttachment, Reply, TaskStatus
from app.db_models.alert import Alert
from app.db_models.asset import Entity
from app.db_models.message import Message
from app.utils.pagination import PaginationHelper

def get_task_by_id(task_id):

    return Task.query.get(task_id)

def create_task():

    task = Task.from_dict(g.args)
    task.from_uid = g.user.id
    db.session.add(task)
    db.session.flush()

    for assignee in g.args.get('assignees'):
        if assignee != g.user.id:
            user_task = UserTask.from_dict({'user_id': assignee, 'task_id': task.id})
            message = Message.from_dict({
                'content': '{} has assigned a new task - {}'.format(g.user.name, task.title),
                'to_uid': assignee,
                'from_uid': g.user.id,
                'type': 2,
                'message_entity_id': task.id
            })
            db.session.add(message)
            db.session.add(user_task)

    task.created_time = datetime.datetime.utcnow()

    # also add the task to the publisher's list
    user_task = UserTask.from_dict({'user_id': g.user.id, 'task_id': task.id})
    db.session.add(user_task)

    db.session.commit()

def update_task(task_id):

    task = Task.query.get(task_id)
    task.update_dict(g.args)

    assignees = get_assignees_of_task(task_id)

    UserTask.query.filter_by(task_id = task_id).delete()

    for assignee in g.args.get('assignees',[]):
        user_task = UserTask.from_dict({'user_id': assignee, 'task_id': task.id})
        db.session.add(user_task)

    user_task = UserTask.from_dict({'user_id': g.user.id, 'task_id': task.id})
    db.session.add(user_task)
        
    task.updated_time = datetime.datetime.utcnow()
    db.session.commit()

def close_task(task_id):

    task = Task.query.get(task_id)
    raw_db.query(task_sqls.close_task, task_id = task_id)
    task.updated_time = datetime.datetime.utcnow()
    db.session.commit()

def update_user_task(task_id):

    user_task = UserTask.query.filter_by(task_id = task_id).filter_by(user_id = g.user.id).first()
    user_task.new_reply = False

    db.session.add(user_task)
    db.session.commit()

def create_comment(task_id):

    comment = Comment.from_dict(g.args)
    comment.task_id = task_id
    comment.from_uid = g.user.id
    comment.created_time = datetime.datetime.utcnow()

    db.session.add(comment)
    task = Task.query.get(task_id)
    notify_users = raw_db.query(task_sqls.get_notifier, task_id = task_id, user_id = g.user.id)

    for notify_user in notify_users:
        message = Message.from_dict({
            'content': '{} commented on the task - {}'.format(g.user.name, task.title),
            'to_uid': notify_user.id,
            'type': 3,
            'message_entity_id': task.id
        })

        db.session.add(message)

    # update the status for all the other user
    raw_db.query(task_sqls.update_new_reply_status_when_comment, task_id = task_id, user_id = g.user.id)

    db.session.flush()

    # add attachments
    attachments  = g.args.get('attachments')
    if attachments:
        for attachment in g.args.get('attachments'):
            atta = CommentAttachment.from_dict({'comment_id': comment.id, 'attachment_id': attachment})
            db.session.add(atta)

    db.session.commit()

    return comment

def create_reply(comment_id):
    reply = Reply.from_dict(g.args)
    reply.from_uid = g.user.id
    reply.comment_id = comment_id
    reply.created_time = datetime.datetime.utcnow()

    comment = Comment.query.get(comment_id)

    message = Message.from_dict({
        'content': '{} mentioned you in the task'.format(g.user.name),
        'to_uid': g.args.get('to_uid'),
        'from_uid': g.user.id,
        'type': 4,
        'message_entity_id': comment.task_id
    })

    db.session.add(message)
    db.session.add(reply)

    # update the new reply status for the user
    task = Task.query.get(comment.task_id)
    user_ids = (g.args.get('to_uid'), task.from_uid) if task.from_uid != g.user.id else (g.args.get('to_uid'),)

    if user_ids:
        raw_db.query(task_sqls.update_new_reply_status_when_reply, task_id = comment.task_id, user_ids = user_ids)

    db.session.commit()
    return reply

def get_tasks_by_type_and_page(type, page, page_size):

    parameters = {
        'user_id': g.user.id,
        'page': page,
        'page_size': page_size
    }

    if type == 1:
        sql = task_sqls.get_all_tasks
    elif type == 2:
        sql = task_sqls.get_assigned_by_me_task
    else:
        sql = task_sqls.get_assigned_to_me_task

    task_pagination = raw_db.paginate(sql, parameters)

    tasks = PaginationHelper(task_pagination).to_dict()

    return tasks

def get_assignees_of_task(task_id):

    task = Task.query.get(task_id)
    assignees = raw_db.query(task_sqls.get_assignees, task_id = task_id, from_uid = task.from_uid)

    return assignees

def get_task_details(task_id):

    db.session.commit()
    user_task = UserTask.query.filter_by(user_id=g.user.id).filter_by(task_id=task_id).first()
    if user_task.status == TaskStatus.NEW.value:
        user_task.status = TaskStatus.PROCESSING.value
    user_task.new_reply = False
    db.session.commit()
    task = raw_db.query(task_sqls.get_task_details, task_id = task_id, user_id = g.user.id).first().to_dict()
    assignees = get_assignees_of_task(task_id)
    task['assignees'] = [ {'id': assignee.id, 'name': assignee.name} for assignee in assignees ]
    task['comments'] = get_task_comments(task_id)
    return task

def get_task_comments(task_id):

    def _get_replies(comment_id):
        return raw_db.query(task_sqls.get_replies_of_comment, comment_id = comment_id).to_dict({'createdTime': datetime_to_timestamp})

    def _get_attachments(comment_id):
        return raw_db.query(task_sqls.get_attachments_of_comment, comment_id = comment_id).to_dict()

    comments = raw_db.query(task_sqls.get_comments_of_tasks, task_id = task_id).to_dict({'createdTime': datetime_to_timestamp})

    for comment in comments:
        comment['replies'] = _get_replies(comment.get('commentId'))
        comment['attachments'] = _get_attachments(comment.get('commentId'))

    return comments


def get_tasks_for_social_component(page, page_size, search):

    parameters = {
        'user_id': g.user.id,
        'offset': (page - 1) * page_size,
        'limit': page_size
    }

    if search:
        parameters['search'] = '%{}%'.format(search)
        sql = task_sqls.tasks_search
    else:
        sql = task_sqls.social_all_tasks

    tasks = raw_db.query(sql, parameters).to_dict()

    for task in tasks:
        result = raw_db.query(task_sqls.get_task_in_panel, task_id = task.get('id')).first()

        if result:
            result = result.to_dict()

        task['latestComment'] = result

    return tasks

def get_pre_assignee_of_task():
    selected_ids = g.args.get('selected_ids')
    selected_ids.append(-1)

    parameters = {
        'query_string': '%{}%'.format(g.args.get('query_string').lower()),
        'selected_ids': tuple(selected_ids)
    }

    assignees = raw_db.query(task_sqls.fuzzy_matching_pre_assignee, parameters).to_dict()
    return assignees

def delete_task_by_id(task_id):

    raw_db.query(task_sqls.delete_task_all_by_id, task_id=task_id)


def delete_comment_by_id(comment_id):

    raw_db.query(task_sqls.delete_comment_by_id, comment_id = comment_id)

def delete_reply_by_id(reply_id):

    Reply.query.filter_by(id = reply_id).delete()
    db.session.commit()

