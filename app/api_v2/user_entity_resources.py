from app.utils.patch import BasicResource
from flask import request, g

from app.ext import db, redis_db
from app.utils.decorators import auth

from app.services import user_services


class UserEntityListResource(BasicResource):

    @auth
    def get(self):

        user_id = request.args.get('user_id', type = int)
        page = request.args.get('page', default = 1, type = int)
        page_size = request.args.get('page_size', default = 10, type = int)
        search = request.args.get('search')

        return user_services.query_entity(user_id, page, page_size, search)

    @auth
    def post(self, user_id):

        access = g.args.get('access')
        all_oper = g.args.get('all_oper')
        # user_id = g.args.get('user_id')

        if all_oper == 'activated':
            user_services.add_del_all(user_id, access)

            return 'user_entity update success', 201

        to_del = []
        to_add = []
        entitys = g.args.get('entity')
        for entity in entitys:
            if entity.get('access') == 1:
                to_del.append(entity)
            elif entity.get('access') == 0:
                to_add.append(entity)
            else:
                pass

        user_services.def_entity_from_user_batch(to_del)
        user_services.add_entity_to_user(to_add)

        user_services.update_modify_time(user_id)

        return 'user_entity update success', 201

    @auth
    def delete(self):

        entity_id = request.args.get('entity_id')
        user_id = request.args.get('user_id')

        user_services.del_entity_from_user(entity_id, user_id)
        return 'user_entity delete success', 200
