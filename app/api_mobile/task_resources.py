# from flask_restful import Resource
from collections import defaultdict, OrderedDict
from operator import itemgetter

from flask import request 

from app.utils.patch import BasicResource
from app.utils.decorators import auth, parse_paremeters_and_modified_response
from app.services import task_services, user_services


class MTaskListResource(BasicResource):
    """docstring for AssetResource"""
    @auth
    def get(self):
        # to get the latest date
        page = request.args.get('page', default = 1, type = int)
        page_size = request.args.get('page_size', default = 5, type = int)
        type = request.args.get('type', default = 1, type = int)

        return task_services.get_tasks_by_type_and_page(int(type), int(page), int(page_size))

    @auth
    def post(self):

        task_services.create_task()
        return 'task created success', 201


class MTaskResource(BasicResource):
    """docstring for AssetResource"""
    @auth
    def get(self, task_id):
        # to get the latest date
        return task_services.get_task_details(task_id)

    @auth
    def put(self, task_id):

        task_services.update_task(task_id)
        return 'task updated success', 200

class MAssgineeResource(BasicResource):
    """docstring for AssetResource"""
    @auth
    def get(self):

        users = user_services.get_users_except_current_user()

        temp_dic = defaultdict(list)

        for user in users:
            group = user.name[0].upper()
            temp_dic[group].append(user.to_dict())

        ordered_dict = OrderedDict(sorted(temp_dic.items(), key = itemgetter(0)))

        ret = [ {'group': group, 'assignees': users} for group, users in ordered_dict.items()]

        return ret

class MCloseTaskResource(BasicResource):
    """docstring for AssetResource"""
    @auth
    def get(self, task_id):

        task_services.close_task(task_id)

        return 'task closed success', 200

class MCommentListResource(BasicResource):

    @auth
    def post(self, task_id):

        task_services.create_comment(task_id)

        return 'commented success', 200

class MReplyListResource(BasicResource):

    @auth
    def post(self, task_id, comment_id):
        task_services.create_reply(comment_id)

        return 'replied success', 200

        