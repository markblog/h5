# from flask_restful import Resource
from app.utils.patch import BasicResource
from app.utils.decorators import auth
from app.services import alert_services, chart_services, asset_services
from flask import g,request 
import datetime


class MAlertListResource(BasicResource):
    """docstring for AssetResource"""
    @auth
    def get(self):
        # to get the latest date
        page = request.args.get('page', default = 1, type = int)
        page_size = request.args.get('page_size', default = 10, type = int)

        default_set = asset_services.get_default_set()
        
        return alert_services.get_alerts_by_page(default_set, page, page_size,[])

class MAlertResource(BasicResource):
    """docstring for MAlertResource"""
    @auth
    def get(self, alert_id):

        res = {}

        alert = alert_services.get_alert_by_id(alert_id)
        entity = asset_services.get_entity_by_id(alert.entity_id)
        chart = chart_services.get_chart_details_without_additional_info(alert.chart_id, datetime.datetime.utcnow() )

        res = alert.to_dict()
        res.update({'entityName': entity.name, 'chartData': chart})

        return res