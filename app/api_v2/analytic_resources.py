# from flask_restful import Resource
import os

from app.utils.patch import BasicResource
from flask import request, g, current_app, send_file

from app.ext import db, redis_db
from app.utils.decorators import auth
from app.services import analytic_services 

class AnalyticResource(BasicResource):
	"""docstring for UserResource"""
	@auth
	def get(self, id):
		dashboard = analytic_services.get_analytic_by_id(id)
		return dashboard.to_dict()

class DashboardThumbnailResource(BasicResource):

    @auth
    def get(self, dashboard_id):
        dashboard = analytic_services.get_analytic_by_id(dashboard_id)
        root_path = os.path.dirname(current_app.instance_path)
        response = send_file(root_path + '/' + dashboard.thumbnail , mimetype = 'image/gif')
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response