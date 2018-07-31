# from flask_restful import Resource
from app.utils.patch import BasicResource
from flask import request, g

from app.ext import db, redis_db
from app.utils.decorators import auth
from app.utils.time_utils import datetime_to_timestamp
from app.mixins.dict import DictMixin
from app.services import chart_services
from app.services import chart_extend_service

from app.models.tab import AnalyticTab, IntelligentChartTab, IntelligentChartTabHub, IntelligentChartType

import datetime

class IntelligentChartListResource(BasicResource):

    @auth
    def get(self):

        level_map = {1: "Option",
            2: "Asset Class Level 1",
            3: "Asset Class Level 2",
            4: "Manager"
        }

        page = request.args.get('page', default = 1, type = int)
        page_size = request.args.get('page_size', default = 6, type = int)
        entity_id = request.args.get('entity', default = None, type = int)

        type = request.args.get('type', default = 1, type = int)
        level = request.args.get('level', type = int, default = None)

        if level:
            level = level_map.get(level)

        date = request.args.get('as_of_date', type = float, default = datetime_to_timestamp(datetime.datetime.utcnow()))
        as_of_date = datetime.datetime.fromtimestamp(date / 1000)

        res = {
            'IntelligentCharts': IntelligentChartTab(IntelligentChartType(type), level, page, page_size, entity_id, as_of_date).to_dict()
        }

        return res

class IntelligentChartResource(BasicResource):
    """docstring for IntelligentChartResource"""
    @auth
    def get(self, chart_id):

        res = {}

        res['chartData'] = chart_services.get_chart_details_without_additional_info(chart_id, None)
        effectiveDate = datetime.datetime.strptime(chart_id[:7],'%Y_%m')
        res['effectiveDate'] = datetime_to_timestamp(effectiveDate)

        return res
    
    @auth
    def post(self, chart_id):
        
        page = request.args.get('page', default = 1, type = int)
        page_size = request.args.get('page_size', default = 6, type = int)
        entity_id = g.args.get('entity')#, default = None, type = int
        date = g.args.get('as_of_date', datetime_to_timestamp(datetime.datetime.utcnow()))#, type = float, default = datetime_to_timestamp(datetime.datetime.utcnow())
        # temp
        if date == 'undefined':
            date = datetime_to_timestamp(datetime.datetime.utcnow())
        as_of_date = datetime.datetime.fromtimestamp(float(date) / 1000)
        history_charts = g.args.get('history_charts')#, default = None

        res = chart_services.get_chart_details(chart_id, entity_id, page, page_size, as_of_date, True, history_charts)

        relatedCharts = res.get('relatedCharts')
        chartData = res.get('chartData')

        newSummary = chart_extend_service.query_chart_insight(chartData.get('chart_id'), g.user.id)

        if newSummary:
            # if newSummary.to_dict()[0].get('is_show_original') == 0:
            chartData['new_summary'] = newSummary.to_dict()[0].get('insight')
            chartData['is_show_original'] = newSummary.to_dict()[0].get('isShowOriginal')
        else:
            chartData['new_summary'] = None
            chartData['is_show_original'] = 1

        samePageCharts = []
        
        if history_charts:
            # history_charts = set(history_charts)
            for chart_id in history_charts:
                history_chart = chart_services.get_chart_details(chart_id, entity_id, page, page_size, as_of_date, False)
                samePageCharts.append({"chart_id":history_chart.get('chartData').get('chart_id') ,"chart_data":history_chart.get('chartData')})
        else:
            samePageCharts.append({"chart_id":chartData.get('chart_id'),"chart_data":chartData})

        res['samePageCharts'] = samePageCharts
        effectiveDate = datetime.datetime.strptime(chart_id[:7],'%Y_%m')
        res['effectiveDate'] = datetime_to_timestamp(effectiveDate)

        return res


class IntelligentChartsListInDetailResource(BasicResource):

    @auth
    def get(self):

        page = request.args.get('page', default = 1, type = int)
        page_size = request.args.get('page_size', default = 6, type = int)
        entity_id = request.args.get('entity', default = None, type = int)
        date = request.args.get('as_of_date', type = float, default = datetime_to_timestamp(datetime.datetime.utcnow()))
        as_of_date = datetime.datetime.fromtimestamp(date / 1000)

        return chart_services.get_intelligent_chart_list(entity_id, page, page_size, type, as_of_date)
