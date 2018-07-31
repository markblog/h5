# from flask_restful import Resource
from app.utils.patch import BasicResource
from flask import request, g

from app.ext import db, redis_db
from app.utils.decorators import auth
from app.mixins.dict import DictMixin
from app.services import chart_services


class MIntelligentChartResource(BasicResource):
	"""docstring for UserResource"""
	
	@auth
	def get(self, chart_id):
		chart = chart_services.m_get_chart_details(chart_id)
		return chart

