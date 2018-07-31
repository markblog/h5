from flask import jsonify
from werkzeug.wrappers import Response

def ok(data = None):
    response = {'code': 200, 'data': data, 'message': 'ok'}
    return response

def created(data = None):
    response = {'code': 201, 'data': data, 'message': 'created'}
    return response

def bad_request(message):
    response = {'code': 400, 'error':'bad request', 'message': message}
    return response

def unauthorized(message):
    response = {'code': 401, 'error': 'unauthorized', 'message': message}
    return response

def forbidden(message):
    response = {'code':403, 'error': 'forbidden', 'message': message}
    return response

def internal_error():
    response = {'code':500, 'error': 'internal server error', 'message': 'an error occured'}
    return response
		
response_map = {
	200: ok,
	201: created,
	400: bad_request,
	401: unauthorized,
	403: forbidden,
	500: internal_error
}