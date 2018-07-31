# charts services
from app.ext import mc
from app.libs.chart_lib.charts_factory import ChartFactory, get_config_dict


from app.db_models.asset import Structure, Entity
from app.ext import mc
from flask import g, current_app
import os,math
import datetime
from app.libs.ai_lib.chart_operations import Chartoperation
# from orderedset import OrderedSet

from functools import lru_cache
from app.db_models.user import Group


def get_available_start_date():

    group = Group.query.get(g.user.group_id)

    root_path = os.path.dirname(current_app.instance_path)
    dates = os.listdir(root_path + '/ic_data/v6/' + group.name)
    dates = [ datetime.datetime.strptime(date,'%Y-%m') for date in dates ]
    dates.sort()
    return dates[0]

# @lru_cache(maxsize=16)
def _get_chart_operation_before_as_of_date(as_of_date):
    if not as_of_date:
        as_of_date = datetime.datetime.utcnow()

    group = Group.query.get(g.user.group_id)

    root_path = os.path.dirname(current_app.instance_path)
    dates = os.listdir(root_path + '/ic_data/v6/' + group.name)
    dates = [ datetime.datetime.strptime(date,'%Y-%m') for date in dates ]
    dates.sort()

    latest_date = as_of_date
    
    for date in dates:
        if date <= as_of_date:
            latest_date = date
        else:
            break

    return _get_singleton_chartoperation(latest_date.strftime('%Y-%m'), group.name)


@lru_cache(maxsize=64)
def _get_singleton_chartoperation(date, group_name):
    chart_dict_all = mc[group_name.lower() +'_' + date + '_' + 'all_charts_dict']
    shown_chart_names = mc[group_name.lower() +'_' + date + '_' + 'all_chart_shown']
    single_entity_dict = mc[group_name.lower() +'_' + date + '_' + 'singleEntityDict_filtered']
    crossEntityDict_filtered = mc[group_name.lower() +'_' + date + '_' + 'crossEntityDict_filtered']
    all_alert_type_dict = mc[group_name.lower() +'_' + date + '_' + 'alert_type_dict']
    themedict = mc[group_name.lower() +'_' + date + '_' + 'themedict']
    typedict = mc[group_name.lower() +'_' + date + '_' + 'typedict']

    chart_op = Chartoperation('2017_6_22', 
        chart_dict_all, 
        shown_chart_names, 
        single_entity_dict,
        crossEntityDict_filtered,
        all_alert_type_dict,
        themedict,
        typedict
    )

    return chart_op

def m_chart_insight(entity_id = None, page = 1, page_size = 6, type = 0):

    res_list = []
    chart_op = _get_chart_operation_before_as_of_date(datetime.datetime.utcnow())
    s = Structure.query.filter_by(entity_id = entity_id).first()
    charts_factory = ChartFactory()
    charts_dict = get_config_dict()

    if not entity_id:
        # get the intelligent charts of the whole assets
        charts, total_number = chart_op.get_charts_by_page(chart_op.shown_chart_names, page, page_size)
    else:
        # get the intelligent charts of the entity
        shown_chart_names = chart_op.single_entity_dict.get(int(entity_id), chart_op.shown_chart_names)
        charts, total_number = chart_op.get_charts_by_page(shown_chart_names, page, page_size)

    for chart_id, data in charts.items():
        chart = charts_factory.get_chart_instance_with_refection(data)
        try:
            chart.transformation(data)
        except Exception as e:
            print(data['type'])
        res_dict = {}
        res_dict['id'] = chart_id
        res_dict['title'] = data['title']
        res_dict['summary'] = data['narrative']
        res_dict['chartData'] = chart.as_dict()
        res_list.append(res_dict)

    return res_list

def m_get_chart_details(chart_id):

    charts_dict = get_config_dict()
    charts_factory = ChartFactory()

    chart_op = _get_chart_operation_before_as_of_date(datetime.datetime.utcnow())
    data = chart_op.get_charts_details(chart_id)
    chart = charts_factory.get_chart_instance_with_refection(data)
    try:
        chart.transformation(data)
    except Exception as e:
        print(data.get('type'))
    return {
        'chart_id': chart_id,
        'chart_data':chart.as_dict()
    }


def get_intelligent_chart_list(entity_id, level, page, page_size, _type, as_of_date):

    def _intersection_of_list(list_a, list_b):
        return [ element for element in list_a if element in list_b ]

    chart_op = _get_chart_operation_before_as_of_date(as_of_date)
    if entity_id:
        # get the intelligent charts of the entity
        shown_chart_names = chart_op.get_themecharts(_type.lower())
        entity_shown_chart_names = chart_op.single_entity_dict.get(entity_id, chart_op.shown_chart_names)
        #list(OrderedSet(entity_shown_chart_names).intersection(OrderedSet(shown_chart_names)))
        chart_names = _intersection_of_list(entity_shown_chart_names, shown_chart_names)
        charts, total_number = chart_op.get_charts_by_page(chart_names, page, page_size)
    elif level:
        shown_chart_names = chart_op.get_themecharts(_type.lower())
        level_shown_chart_names = chart_op.crossEntityDict.get(level, chart_op.shown_chart_names)
        # chart_names = list(OrderedSet(level_shown_chart_names).intersection(OrderedSet(shown_chart_names)))
        chart_names = _intersection_of_list(level_shown_chart_names, shown_chart_names)
        charts, total_number = chart_op.get_charts_by_page(chart_names, page, page_size)
    else:
        # get the intelligent charts of the whole assets
        shown_chart_names = chart_op.get_themecharts(_type.lower())
        # chart_names = list(OrderedSet(chart_op.shown_chart_names).intersection(OrderedSet(shown_chart_names)))
        chart_names = _intersection_of_list(chart_op.shown_chart_names, shown_chart_names)
        charts, total_number = chart_op.get_charts_by_page(chart_names, page, page_size)

    res = {}
    charts_list = []
    charts_factory = ChartFactory()
    charts_dict = get_config_dict()

    for chart_id, data in charts.items():
        if data['type'] in charts_dict.keys():
            chart = charts_factory.get_chart_instance_with_refection(data)
            if chart_id == '2017_12_F00041_all_0_Strategy 3':
                print(data)
            try:
                chart.transformation(data)
            except Exception as e:
                print(data['type'])
            charts_list.append({
            'chart_id': chart_id,
            'chart_data':chart.as_dict()
            })
        else:
            print(data)

    res['charts'] = charts_list
    res['totalNumber'] = total_number
    res['page'] = page

    return res

def _get_as_of_date_from_chart_id(chart_id):
    as_of_date = datetime.datetime.strptime(chart_id[:7],'%Y_%m')
    return as_of_date

def get_chart_details(chart_id, entity_id, page, page_size, as_of_date = None, boolean_related_charts = True, history_charts = None):

    def _get_related_charts(chart_data, as_of_date, chart_id, history_charts = None):

        related_charts = chart_data.get('related_charts')
        if related_charts and history_charts:
            related_charts = [ chart for chart in related_charts if chart not in history_charts ]

        # print("*** ", related_charts, " ***")
        charts_list = []
        chart_op = _get_chart_operation_before_as_of_date(as_of_date)
        charts_factory = ChartFactory() 
        for chart_id in related_charts[:10]:
            data = chart_op.get_charts_details(chart_id)
            chart = charts_factory.get_chart_instance_with_refection(data)
            try:
                chart.transformation(data)
            except Exception as e:
                print(data.get('type'))
            charts_list.append({
                'chart_id': chart_id,
                'chart_data':chart.as_dict(),
            })

        return charts_list

    as_of_date = _get_as_of_date_from_chart_id(chart_id)


    res = {}
    chart_op = _get_chart_operation_before_as_of_date(as_of_date)

    data = chart_op.get_charts_details(chart_id)
    charts_factory = ChartFactory()
    chart = charts_factory.get_chart_instance_with_refection(data)
    try:
        chart.transformation(data)
    except Exception as e:
        print(data.get('type'))
    res['chartData'] = chart.as_dict()
    res['chartData']['chart_id'] = chart_id
    if boolean_related_charts:
        if history_charts == None:
            history_charts = []
        try:
            history_charts.index(chart_id)
        except ValueError as e:
            history_charts.append(chart_id)
        res['relatedCharts'] = _get_related_charts(data, as_of_date, chart_id, history_charts)

    if entity_id:
        res['entityName'] = Entity.query.get(entity_id).name
    else:
        res['entityName'] = None            

    return res

def get_chart_details_without_additional_info(chart_id, as_of_date):

    if not as_of_date:
        as_of_date = _get_as_of_date_from_chart_id(chart_id)

    res = {}
    chart_op = _get_chart_operation_before_as_of_date(as_of_date)

    data = chart_op.get_charts_details(chart_id)

    charts_factory = ChartFactory()
    chart = charts_factory.get_chart_instance_with_refection(data)
    try:
        chart.transformation(data)
    except Exception as e:
        print(data.get('type'))

    res = chart.as_dict()
    res['chart_id'] = chart_id
    
    return res


def get_chart_type_data(type):

    chart_op = _get_chart_operation_before_as_of_date(datetime.datetime.utcnow())

    data = chart_op.get_typechart(type)
    # print(data)
    # data = data['2017_06_F00093_S2BC_INTLSH_INTLSHAC_SUQ1']
    charts_factory = ChartFactory()
    chart = charts_factory.get_chart_instance_with_refection(data)
    try:
        chart.transformation(data)
    except Exception as e:
        print(e)

    res = chart.as_dict()
    # res['chart_id'] = chart_id

    return res


