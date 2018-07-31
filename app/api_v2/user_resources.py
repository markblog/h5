# from flask_restful import Resource
from app.utils.patch import BasicResource
from flask import request, g

from app.ext import db, redis_db
from app.utils.decorators import auth
from app.services import user_services

class UserListResource(BasicResource):
    """docstring for UserResource"""
    def post(self):
        user=user_services.get_user_by_email()

        if user:
            return 'email already registered!', 400
        else:
            user_services.create_user()

        return 'user created success', 201

    @auth
    def get(self):
        page = request.args.get('page', default = 1, type = int)
        page_size = request.args.get('page_size', default = 10, type = int)

        return user_services.get_all_user(page, page_size)


class LoginResource(BasicResource):
    """docstring for LoginResource"""
    def post(self):
        user=user_services.get_user_by_email()

        if user and user.verify_password(g.args.get('password')):

            token = user.generate_auth_token()
            return {'token':token, 'expiration':3600 * 24, 'userName': user.name, 'userId': user.id}
        else:
            return 'user does not exist or email and password does not match, please check!', 400


class UserResource(BasicResource):

    @auth
    def get(self):
        return g.user.to_dict(excludes = ['password_hash'])

class LogoutResource(BasicResource):
    
    @auth
    def get(self):
        token = request.headers.get('Authorization') or request.cookies.get('session_id')
        redis_db.get('token_black_list').append(token.split(' ')[-1])
        return 'login out success'
        
class UserDetialResource(BasicResource):

    @auth
    def get(self):

        user_id = request.args.get('user_id')

        return user_services.get_user_detail(user_id)

class UserActiveResource(BasicResource):

    @auth
    def get(self):

        return user_services.get_user_active()

    @auth
    def put(self, user_id):

        user_services.update_user_active(user_id)

        return 'user active update success', 200

class UserSearchResource(BasicResource):

    @auth
    def get(self):
        search = request.args.get('search')
        page = request.args.get('page', default = 1, type = int)
        page_size = request.args.get('page_size', default = 10, type = int)

        return user_services.search_user(search, page, page_size)

class UserGroupResource(BasicResource):

    @auth
    def get(self):

        return user_services.get_all_group()