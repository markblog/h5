import math
import datetime
from flask import g
from collections import defaultdict
from app.ext import raw_db, db
from app.sqls import alert_sqls, asset_sqls
from app.utils.time_utils import datetime_to_timestamp
from app.db_models.alert import Alert, AlertThreshold, AlertType

from app.utils.pagination import PaginationHelper
from app.services import asset_services

def get_latest_date_of_alert():

    date = raw_db.query(alert_sqls.get_latest_date_of_alerts, group_id = g.user.group_id).first()

    return date

def get_alerts_by_page(default_set, page, page_size, entity_ids = set([])):

    parameters = {
        'user_id': g.user.id,
        'group_id': g.user.group_id,
        'page': page,
        'page_size': page_size,
        'date_key': default_set.date_key
    }

    if len(entity_ids) > 0:
        parameters['entity_ids'] = tuple(entity_ids)
        alerts_pagination = raw_db.paginate(alert_sqls.get_alerts_by_page_and_in_entity_ids, parameters)
    else:
        alerts_pagination = raw_db.paginate(alert_sqls.get_alerts_by_page, parameters)

    alerts = PaginationHelper(alerts_pagination).to_dict()
    # print("*** ", alerts, " ***")

    return alerts

def set_alert_flag_on_map(sankey_data, default_set):
    latest_alert = get_latest_date_of_alert()
    if latest_alert:

        s = set()
        alert_entities = raw_db.query(
            alert_sqls.get_alerts_entity_id, 
            date_key = default_set.date_key, 
            user_id = g.user.id, 
            group_id = g.user.group_id
        )


        for alert in alert_entities:
            s.add(alert.entity_id)


        for node in sankey_data.get('nodes'):
            if node.get('id') in s:
                node['alert'] = True

    return sankey_data

def get_alerts_by_page_and_entity(default_set, entity_id, page, page_size):

    parameters = {
        'user_id': g.user.id,
        'group_id': g.user.group_id,
        'page': page,
        'page_size': page_size,
        'entity_id': entity_id,
        'date_key': default_set.date_key
    }

    alerts_pagination = raw_db.paginate(alert_sqls.get_alerts_by_page_and_entity, parameters)

    alerts = PaginationHelper(alerts_pagination).to_dict()
    
    return alerts

def get_alert_by_id(alert_id):

    alert = Alert.query.get(alert_id)
    alert.is_read = True

    db.session.commit()

    return alert

def get_related_alerts(alert):

    parameters = {
        'user_id': g.user.id,
        'group_id': g.user.group_id,
        'alert_type_id':alert.alert_type_id,
        'date_key': alert.date_key
    }

    related_alerts = raw_db.query(alert_sqls.get_related_alerts, parameters)
    return related_alerts

def get_alerts_of_entity_in_specific_page(alert, page_size = 6):

    parameters = {
        'user_id': g.user.id,
        'group_id': g.user.group_id,
        'entity_id': alert.entity_id,
        'date_key': alert.date_key
    }

    
    alerts = raw_db.query(alert_sqls.get_alerts_of_entity, parameters)

    for index, r_alert in enumerate(alerts):
        if alert.id == r_alert.alert_id:
            page = math.ceil(index // page_size) + 1

    parameters['page'] = page
    parameters['page_size'] = page_size

    alerts_pagination = raw_db.paginate(alert_sqls.get_alerts_of_entity, parameters)
    alerts = PaginationHelper(alerts_pagination).to_dict()
    return alerts

def get_alerts_of_entity(alert, page, page_size):

    parameters = {
        'user_id': g.user.id,
        'group_id': g.user.group_id,
        'date_key': alert.date_key,
        'entity_id': alert.entity_id,
        'page': page,
        'page_size': page_size
    }

    alerts_pagination = raw_db.paginate(alert_sqls.get_alerts_of_entity, parameters)
    alerts = PaginationHelper(alerts_pagination).to_dict()
    return alerts

def get_alert_threshold_by_page(page, page_size):

    parameters = {
        'offset': (page - 1) * page_size,
        'limit': page_size,
        'user_id': g.user.id
    }

    alert_thresholds = raw_db.query(alert_sqls.get_alert_threshold_by_page, parameters).to_dict(camelcase = False)

    return alert_thresholds

def set_alert_threshold_activate(id):

    alert_threshold = AlertThreshold.query.get(id)
    alert_threshold.activate = (alert_threshold.activate + 1) % 2

    db.session.commit()

def update_alert_threshold_parameters(_id):

    alert_threshold = AlertThreshold.query.get(_id)
    update_parameters =  {'description': g.args.get('parameters')}
    for parameter in g.args.get('parameters'):

        if parameter.get('editable'):

            update_parameters[parameter.get('name')] = parameter.get('value')

    alert_threshold.update_dict(update_parameters)

    db.session.commit()

def get_entity_ids_by_level(level):
    set_id = asset_services.get_default_set()

    strutures = raw_db.query(asset_sqls.select_structure_by_level, {"level": level, "set_id": set_id.id}).all()
    entity_ids = []
    for struture in strutures:
        entity_ids.append(struture.entity_id)

    return entity_ids

def get_all_alert_type():

    all_alert_type =  AlertType.query.filter_by(group_id = g.user.group_id).all()

    dic = defaultdict(dict)

    for alert_type in all_alert_type:
        if not dic[alert_type.category].get(alert_type.subcategory):
            dic[alert_type.category][alert_type.subcategory] = []
        dic[alert_type.category][alert_type.subcategory].append(alert_type.to_dict())

    ret = []

    for category, data in sorted(dic.items()):
        res = {}
        res['data'] = []
        for subcategory, subcategory_data in sorted(data.items()):
            sub_res = {}
            sub_res['subcategory'] = subcategory
            sub_res['alert_templates'] = subcategory_data
            res['data'].append(sub_res)
        res['category'] = category
        ret.append(res)

    return ret

def create_alert_threshold():
    alert = AlertThreshold.from_dict(g.args)
    alert.user_id = g.user.id
    alert.date_key = datetime.datetime.utcnow()
    alert.activate = 1
    db.session.add(alert)
    db.session.commit()
