# from flask_restful import Resource
from app.utils.patch import BasicResource
from flask import request, g

from app.ext import db, redis_db
from app.utils.decorators import auth
from app.services import user_services

class MUserProfileResources(BasicResource):
	"""docstring for UserResource"""

	@auth
	def get(self):

		user=user_services.get_user_profile()

		res = {
			'name': user.name,
			'email': user.email,
			'tel': user.tel
		}

		return res
		




		
		