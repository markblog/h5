# from flask_restful import Resource
from app.utils.patch import BasicResource
from flask import request, g

from app.ext import db, redis_db
from app.utils.decorators import auth
from app.utils.time_utils import datetime_to_timestamp
from app.mixins.dict import DictMixin
from app.services import asset_services, user_services, chart_services

from app.models.tab import AnalyticTab, IntelligentChartTab, IntelligentChartTabHub, IntelligentChartType
import datetime

class AssetResource(BasicResource):

    @auth
    def get(self):

        level_map = {1: "Strategy",
            2: "Asset Class Level 1",
            3: "Asset Class Level 2",
            4: "Manager"
        }

        entity_id = request.args.get('entity', type = int, default = None)
        level = request.args.get('level', type = int, default = None)
        metric_id = request.args.get('metric', type = int, default = 2)
        page = request.args.get('page', type = int, default = 1)
        date = request.args.get('as_of_date', type = float, default = datetime_to_timestamp(datetime.datetime.utcnow()))
        type = request.args.get('type', default = 1, type = int)
        as_of_date = datetime.datetime.fromtimestamp(date / 1000)
        
        res = {}
        # to get the latest date
        default_set = asset_services.get_default_set(as_of_date)

        if level:
            level = level_map.get(level)

        res['tabs'] = {
            'IntelligentCharts': {
                'categories':['Intelligent Charts','Analytic'],
                'subCategories': [member.name.lower().capitalize() for member in list(IntelligentChartType)],
                'categoryData': IntelligentChartTab(IntelligentChartType(type), level, page = page, entity_id = entity_id, as_of_date = as_of_date).to_dict()
            },
            'Analytic': {
                'categoryData': AnalyticTab(default_set, entity_id).to_dict()
            }
        }

        res['availableStartDate'] = datetime_to_timestamp(chart_services.get_available_start_date())

        if entity_id:
            res['sankeyData'] = asset_services.generate_sankey_for_entity(default_set, entity_id, metric_id)
        else:
            res['sankeyData'] = asset_services.generate_sankey_for_whole_set(default_set, metric_id)
    
        access_entity_ids = user_services.get_access_entity_ids()

        for item in res.get('sankeyData').get('nodes'):
            if item.get('id') in access_entity_ids:
                item['access'] = 1
            else:
                item['access'] = 1

        res['sankeyData']['title'] = 'Assets Map'
        res['effectiveDate'] = datetime_to_timestamp(default_set.date_key)

        return res

class EntityResource(BasicResource):

    @auth
    def get(self):

        date = request.args.get('as_of_date', type = float, default = datetime_to_timestamp(datetime.datetime.utcnow()))
        as_of_date = datetime.datetime.fromtimestamp(date / 1000)
        query_string = request.args.get('query')
        default_set = asset_services.get_default_set(as_of_date)
        access_entity_ids = user_services.get_access_entity_ids()
        access_entity_ids.add(-1)
        results = asset_services.fuzzy_entity_name_matching(default_set, query_string, access_entity_ids)

        return results.to_dict()