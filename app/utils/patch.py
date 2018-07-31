from flask_restful import Resource
from .decorators import parse_paremeters_and_modified_response

class BasicResource(Resource):
    method_decorators = [parse_paremeters_and_modified_response]