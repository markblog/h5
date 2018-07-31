# from flask_restful import Resource
from app.utils.patch import BasicResource
from app.utils.decorators import auth
from app.services import asset_services, chart_services, meeting_services
from app.utils.time_utils import now, int_to_timestamp

from flask import g,request 


class MAssetResource(BasicResource):
    """docstring for AssetResource"""
    @auth
    def get(self):
        # to get the latest date
        return chart_services.m_chart_insight()

class MAssetStatisticsResources(BasicResource):
    """docstring for Stactistics"""
    
    @auth
    def get(self):

        default_set = asset_services.get_default_set()

        res = {}
        res['userName'] = g.user.name
        res['statistics'] = asset_services.m_assets_statistics(default_set)

        return res

class MAssetLevelResource(BasicResource):

    @auth
    def get(self, level):
        
        res = {}
        default_set = asset_services.get_default_set() 
        page = request.args.get('page', default = 1, type = int)
        page_size = request.args.get('page_size', default = 7, type = int)

        details, level_name, counts = asset_services.m_assets_level_details(level, default_set, page, page_size)

        res = {
            'level_name': level_name,
            'count': counts,
            'details': details.to_dict()
        }

        return res

class MEntityResource(BasicResource):

    @auth
    def get(self, entity_id):

        res = {}
        structure, lowest_level, date_key = asset_services.m_is_lowest_level(entity_id)
        res['metricData'] = asset_services.m_get_metrics_data_of_structure(entity_id, date_key).to_dict()
        if structure.level == lowest_level:
            res['cardInfo'] = meeting_services.m_get_first_upcoming_meeting_by_entity_id(entity_id, int_to_timestamp(now()))
            res['type'] = 'meeting'
        else:
            res['cardInfo'] = asset_services.m_top3_holding_funds(entity_id, lowest_level, date_key).to_dict()
            res['type'] = 'top3'
        res['insights'] = chart_services.m_chart_insight(entity_id)

        return res

class MFundsInEntityResource(BasicResource):

    @auth
    def get(self, entity_id):

        res = {}

        page = request.args.get('page', default = 1, type = int)
        page_size = request.args.get('page_size', default = 7, type = int)

        structure, lowest_level, date_key = asset_services.m_is_lowest_level(entity_id)
        funds, counts, level_name = asset_services.m_all_funds(entity_id, lowest_level, date_key, page, page_size)
        res = {
            'level_name': level_name,
            'count': counts,
            'details': funds.to_dict()
        }
        return res
