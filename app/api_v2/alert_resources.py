# from flask_restful import Resource
import datetime
from app.utils.time_utils import datetime_to_timestamp
from app.utils.patch import BasicResource
from flask import request, g

from app.ext import db, redis_db
from app.utils.decorators import auth
from app.mixins.dict import DictMixin
from app.services import asset_services, alert_services, chart_services, user_services

from app.models.tab import AnalyticTab, IntelligentChartTab, IntelligentChartTabHub, IntelligentChartType


class AlertsMapResource(BasicResource):

    @auth
    def get(self):

        entity_id = request.args.get('entity', type = int, default = None)
        metric_id = request.args.get('metric', type = int, default = 1)
        page = request.args.get('page', type = int, default = 1)
        date = request.args.get('as_of_date', type = float, default = datetime_to_timestamp(datetime.datetime.utcnow()))
        as_of_date = datetime.datetime.fromtimestamp(date / 1000)
        level = request.args.get('level', type = int, default = None)

        entity_ids = []
        if level:
            entity_ids = alert_services.get_entity_ids_by_level(level)

        res = {}
        # to get the latest date
        default_set = asset_services.get_default_set(as_of_date)
        sankey_data = asset_services.generate_sankey_for_entity(default_set, entity_id, metric_id)
        if entity_id:
            sankey_data = asset_services.generate_sankey_for_entity(default_set, entity_id, metric_id)
            res['sankeyData'] = alert_services.set_alert_flag_on_map(sankey_data, default_set)
            res['alerts'] = alert_services.get_alerts_by_page_and_entity(default_set, entity_id, page, 9)
        else:
            sankey_data = asset_services.generate_sankey_for_whole_set(default_set, metric_id)
            res['sankeyData'] = alert_services.set_alert_flag_on_map(sankey_data, default_set)
            res['alerts'] = alert_services.get_alerts_by_page(default_set, page, 9, entity_ids)
            
        access_entity_ids = user_services.get_access_entity_ids()

        for item in res.get('sankeyData').get('nodes'):
            if item.get('id') in access_entity_ids:
                item['access'] = 1
            else:
                item['access'] = 1

        res['sankeyData']['title'] = 'Alerts Map'
        res['effectiveDate'] = datetime_to_timestamp(default_set.date_key)
        res['availableStartDate'] = datetime_to_timestamp(chart_services.get_available_start_date())

        return res

class AlertListResource(BasicResource):

    @auth
    def get(self, entity_id = None):
        page = request.args.get('page', default = 1, type = int)
        page_size = request.args.get('page_size', default = 9, type = int)
        entity_id = request.args.get('entity', default = None, type = int)
        level = request.args.get('level', type = int, default = None)
        date = request.args.get('as_of_date', type = float, default = datetime_to_timestamp(datetime.datetime.utcnow()))
        as_of_date = datetime.datetime.fromtimestamp(date / 1000)

        entity_ids = []
        if level:
            entity_ids = alert_services.get_entity_ids_by_level(level)

        default_set = asset_services.get_default_set(as_of_date)

        if entity_id:
            res = alert_services.get_alerts_by_page_and_entity(default_set, entity_id, page, page_size)
        else:
            res = alert_services.get_alerts_by_page(default_set, page, page_size, entity_ids)

        return res

class AlertResource(BasicResource):

    @auth
    def get(self, alert_id):
        res = {}

        alert = alert_services.get_alert_by_id(alert_id)
        entity = asset_services.get_entity_by_id(alert.entity_id)

        date = request.args.get('as_of_date', type = float, default = datetime_to_timestamp(datetime.datetime.utcnow()))
        as_of_date = datetime.datetime.fromtimestamp(date / 1000)

        res['chart'] = chart_services.get_chart_details_without_additional_info(alert.chart_id, as_of_date)
        res['chart']['alert'] = alert.description
        res['chart']['entityName'] = entity.name
        res['relatedAlerts'] = alert_services.get_related_alerts(alert).to_dict()
        res['alertsOfEntity'] = alert_services.get_alerts_of_entity_in_specific_page(alert)
        effectiveDate = datetime.datetime.strptime(alert.chart_id[:7],'%Y_%m')
        res['effectiveDate'] = datetime_to_timestamp(effectiveDate)

        return res

class AlertPageResource(BasicResource):

    @auth
    def get(self, alert_id):

        res = {}

        page = request.args.get('page', default = 1, type = int)
        page_size = request.args.get('page_size', default = 6, type = int)

        alert = alert_services.get_alert_by_id(alert_id)
        entity = asset_services.get_entity_by_id(alert.entity_id)

        date = request.args.get('as_of_date', type = float, default = datetime_to_timestamp(datetime.datetime.utcnow()))
        as_of_date = datetime.datetime.fromtimestamp(date / 1000)

        res['chart'] = chart_services.get_chart_details_without_additional_info(alert.chart_id, as_of_date)
        res['chart']['alert'] = alert.description
        res['chart']['entityName'] = entity.name
        res['relatedAlerts'] = alert_services.get_related_alerts(alert).to_dict()
        res['alertsOfEntity'] = alert_services.get_alerts_of_entity(alert, page, page_size)

        return res

class AlertTemplateListResource(BasicResource):

    @auth
    def get(self):
        return alert_services.get_all_alert_type()

    @auth
    def post(self):
        alert_services.create_alert_threshold()
        return 'alert setting created success'

class AlertSettingListResource(BasicResource):

    @auth
    def get(self):

        page = request.args.get('page', default = 1, type = int)
        page_size = request.args.get('page_size', default = 10, type = int)

        alert_settings = {
            'level':['Strategy Level', 'Asset Class Level 1', 'Asset Class Level 2', 'Manager Level'],
            'type':['over', 'under'],
            'alerts_threshold': alert_services.get_alert_threshold_by_page(page, page_size)
        }

        return alert_settings

    @auth
    def post(self):

        pass


class AlertSettingResource(BasicResource):

    @auth
    def delete(self, id):

        alert_services.set_alert_threshold_activate(id)
        return 'alert_threshold activate update success', 200