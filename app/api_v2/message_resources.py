from flask import request, g

from app.utils.patch import BasicResource
from app.utils.decorators import auth
from app.services import message_services

class MessageListResource(BasicResource):

    @auth
    def get(self):
        page = request.args.get('page', default = 1, type = int)
        page_size = request.args.get('page_size', default = 9, type = int)

        return message_services.get_messages_by_page(page,page_size)

    @auth
    def post(self):

        message_services.create_message()

        return 'message created success', 201

    @auth
    def put(self, status):
        
        message_services.update_all_message(status)

        return 'message operate success', 200

class MessageResource(BasicResource):

    @auth
    def get(self):

        return message_services.get_new_message_count()

    @auth
    def put(self, id, status):

        message_services.update_specific_message(id, status)

        return 'message operate success', 200