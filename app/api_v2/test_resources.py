# from flask_restful import Resource
from app.utils.patch import BasicResource
from flask import request, g

from app.services import test_services
from app.services import chart_services

from app.utils.decorators import auth
from app.utils.time_utils import datetime_to_timestamp

import datetime

class TestResource(BasicResource):
	"""docstring for UserResource"""
	def get(self):
		test_services.test_db_text()

		return 'test db text success', 200


class ChartTypeResource(BasicResource):
	"""docstring for UserResource"""
	@auth
	def get(self, type):
		res = chart_services.get_chart_type_data(type)

		return res

class ChartAsOfDateResource(BasicResource):
	"""docstring for UserResource"""
	@auth
	def get(self):
		date = datetime.datetime.utcnow()
		chart_services._get_chart_operation_before_as_of_date(date)

		return 'test db text success', 200