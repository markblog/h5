from flask import request, g

from app.utils.patch import BasicResource
from app.utils.decorators import auth
from app.services import task_services, message_services
from app.db_models.task import TaskType
from app.utils.time_utils import datetime_to_timestamp

class TaskListResource(BasicResource):
    """docstring for AssetResource"""
    @auth
    def get(self):
        # to get the latest date
        page = request.args.get('page', default = 1, type = int)
        page_size = request.args.get('page_size', default = 9, type = int)
        type = request.args.get('type', default = 1, type = int)

        task_type = TaskType(type)

        return task_services.get_tasks_by_type_and_page(task_type.value, int(page), int(page_size))

    @auth
    def post(self):
        task = task_services.create_task()

        return 'task created success', 201
        

class TaskResource(BasicResource):
    """docstring for AssetResource"""
    @auth
    def get(self, task_id):
        # to get the latest date
        return task_services.get_task_details(task_id)

    @auth
    def put(self, task_id):
        task = task_services.get_task_by_id(task_id)
        if task.from_uid == g.user.id:
            task_services.update_task(task_id)
            return 'task updated success', 200
        else:
            return 'No authorization'

    @auth
    def delete(self, task_id):
        task_services.delete_task_by_id(task_id)
        return 'task delete success', 200

class TaskCloseResource(BasicResource):

    @auth
    def put(self, task_id):

        task_services.close_task(task_id)

        return 'Task closed'


class CommentListResource(BasicResource):

    @auth
    def get(self, task_id):
        # to get the latest date
        return task_services.get_task_comments(task_id)

    @auth
    def post(self, task_id):

        comment = task_services.create_comment(task_id)

        return {'commentId':comment.id, 'createdTime': datetime_to_timestamp(comment.created_time)}

class CommentResource(BasicResource):
    

    @auth
    def delete(self, task_id, comment_id):
        task_services.delete_comment_by_id(comment_id)

        return 'comment delete success'

class ReplyResource(BasicResource):

    @auth
    def delete(self, task_id, comment_id, reply_id):
        task_services.delete_reply_by_id(reply_id)

        return 'Reply delete success'

class ReplyListResource(BasicResource):

    @auth
    def post(self, task_id, comment_id):
        reply = task_services.create_reply(comment_id)

        return {'replyId':reply.id}


class TaskListInSocialResource(BasicResource):

    @auth
    def get(self):

        # to get the latest date
        page = request.args.get('page', default = 1, type = int)
        page_size = request.args.get('page_size', default = 9, type = int)
        search = request.args.get('search', None)

        return task_services.get_tasks_for_social_component(page, page_size, search) 

class TaskAssigneesForPC(BasicResource):

    @auth
    def post(self):

        return task_services.get_pre_assignee_of_task()

class UserTaskResource(BasicResource):

    @auth
    def put(self, task_id):

        return task_services.update_user_task(task_id)
