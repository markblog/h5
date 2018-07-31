# from flask_restful import Resource
from app.utils.patch import BasicResource
from app.utils.decorators import auth
from app.services import meeting_services
from flask import g, request 
from app.utils.time_utils import now, int_to_timestamp

import datetime



class MMeetingListResource(BasicResource):
	"""docstring for AssetResource"""
	@auth
	def get(self):
		# to get the latest date
		page = request.args.get('page', default = 1, type = int)
		page_size = request.args.get('page_size', default = 7, type = int)
		date = request.args.get('date', default = now(), type = int)
		date = int_to_timestamp(date)
		meetings = meeting_services.m_get_meetings_by_page_and_attendance_after_date(date, page, page_size)
		return meetings