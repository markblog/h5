from functools import wraps
from flask import request, g, current_app, Response
from app.db_models.user import User, Role
from app.ext import redis_db

from app.services.asset_services import get_default_set

def auth(func):
    """
    According to the token in the cookies and authorization header to determine the login status. if user has logined,
    the user object will be in global varaibles, so we can access it easily and return normally. however, the cases below
    will not allowed to finish the request:
        1. no token or authorization content
        2. token is in black list
        3. token is expired
    In two cases, the token will be added to the black list.
        1. logout by the user
        2. the outdate token, which means the token will be expired in ten minutes(for now)
    """
    
    def wrapper(*args, **kwargs):
        
        if not getattr(func, 'auth', True):
            return func(*args, **kwargs)

        token = request.headers.get('Authorization') or request.args.get('token')
        # to process the authorization correctly
        if not token:
            return 'Please login first!', 401

        token = token.split(' ')[-1]
        # logout for user
        if token in redis_db.get('token_black_list'):
            return 'Invalid token', 401

        user, refresh = User.verify_auth_token(token)

        if user:
            g.user = user
            try:
                res = func(*args, **kwargs)
            except Exception as e:
                current_app.logger.exception(e)
                res = '', 500
            if refresh:
                res.setdefault('token', user.generate_auth_token())
                redis_db.get('token_black_list').append(token)
            return res
        else:
            return 'Invalid token or token has expired', 401

    return wrapper

def parse_paremeters_and_modified_response(func):

    def wrapper(*args, **kwargs):
        g.args = request.get_json()
        try:
            res = func(*args, **kwargs)
        except Exception as e:
            current_app.logger.exception(e)
            return {'message': 'Wow...,none bussiness with me, do not hurt me, this is the guy who wrote this -- YHuang@StateStreet.com'}, 500

        
        if isinstance(res, tuple):
            data, code = res
            if code in [200,201]:
                ret = {'data': data, 'message': 'Hope this is what you want'}, code
            else:
                ret = {'data':'No data avaiable for this request','message': data}, code
        elif isinstance(res, Response):
            ret = res
        else:
            ret = {'data': res, 'message':'Hope this is what you want'}, 200

        return ret

    return wrapper

def admin_oper(original_function):
    def new_function(*args, **kwargs):

        if g.user.role_id != Role.ADMIN.value:
            return {"message": "no authorization"}

        result = original_function(*args, **kwargs) 

        return result

    return new_function
