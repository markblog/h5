import math, datetime
from dateutil.relativedelta import relativedelta
from flask import g
# from orderedset import OrderedSet
from app.db_models.asset import EntitySet, Structure, Entity
from app.ext import raw_db
from app.sqls import asset_sqls

def get_entity_by_id(entity_id):

    entity = Entity.query.get(entity_id)

    return entity


def get_default_set(as_of_date = None):
    """
    give the defalut entity set according the latest date
    """
    if not as_of_date:
        as_of_date = datetime.datetime.utcnow()
    else:
        as_of_date = as_of_date + relativedelta(day = 1, months = 1, days=-1)

    default_entity_set = EntitySet.query.filter_by(group_id = g.user.group_id).filter(EntitySet.date_key <= as_of_date)\
                        .order_by(EntitySet.date_key.desc()).first()

    return default_entity_set

def fuzzy_entity_name_matching(set, query_string):

    results = raw_db.query(asset_sqls.fuzzy_entity_name_matching, set_id = set.id, query_string = '%{}%'.format(query_string.lower()))
    return results

def generate_sankey_for_whole_set(set, metric_id):
    """
    generate the sankey chart data format for the whole structure
    """
    links = raw_db.query(
        asset_sqls.whole_set_data, 
        set_id = set.id, 
        metric_id = 1,
        date_key = set.date_key
    )
    
    nodes = raw_db.query(
        asset_sqls.get_whole_set_nodes_order_data, 
        set_id = set.id, 
        metric_id = 1,
        date_key = set.date_key
    )

    _nodes, min_return, max_return = _order_sankey_nodes(nodes, set, metric_id)

    sankey_result = {
        'links': _format_sankey_links(links),
        'nodes': _nodes,
        'tabs': ['Strategy','Asset Class Level 1', 'Asset Class Level 2', 'Manager'],
        'metrics': [
                        # {'id': 1, 'name':'Ending Market Value'}
                        {'id': 2, 'name':'1 Month Absolute Return'},
                        {'id': 4, 'name':'1 Month Excess Return'},
                        {'id': 8, 'name':'1 Year Absolute Return'},
                        {'id': 10, 'name':'1 Year Excess Return'}
                        # {'id': 2, 'name':'Absolute Return'}
                    ],
        'maxReturn': max_return,
        'minReturn': min_return
    }

    return sankey_result

def generate_sankey_for_entity(set, entity_id, metric_id):
    """
    generate the sankey chart data format for the specific entity
    """
    links = raw_db.query(
        asset_sqls.get_entity_data, 
        entity_id = entity_id,
        set_id = set.id, 
        metric_id = 1,
        date_key = set.date_key
    )

    nodes = raw_db.query(
        asset_sqls.get_entity_nodes_order_data, 
        entity_id = entity_id,
        set_id = set.id, 
        metric_id = 1,
        date_key = set.date_key
    )

    _nodes, min_return, max_return = _order_sankey_nodes(nodes, set, metric_id)

    sankey_result = {
        'links': _format_sankey_links(links),
        'nodes': _nodes,
        'tabs': ['Strategy','Asset Class Level 1', 'Asset Class Level 2', 'Manager'],
        'metrics': [
                        {'id': 2, 'name':'1 Month Absolute Return'},
                        {'id': 4, 'name':'1 Month Excess Return'},
                        {'id': 8, 'name':'1 Year Absolute Return'},
                        {'id': 10, 'name':'1 Year Excess Return'}
                    ],
        'maxReturn': max_return,
        'minReturn': min_return
    }
    # Todo
    return sankey_result

def _format_sankey_links(data):

    links = []

    for record in data:
        links.append({
            "source":record.parent_name,
            "target":record.child_name,
            "value": record.value,
            "level": record.level
        })

    return links

def _get_entity_metric_value(set, metric_id):

    entity_metric_data = raw_db.query(asset_sqls.get_entity_metric_data, set_id = set.id, date_key = set.date_key, metric_id = metric_id).all()
    entity_metric_data_dic = {}

    returns = []

    for entity_data in entity_metric_data:
        entity_metric_data_dic[entity_data.entity_id] = {
            'emv': entity_data.emv,
            'return': entity_data.ret
        }

        returns.append(abs(entity_data.ret))

    returns.sort()

    entity_numbers = len(returns)
    
    return entity_metric_data_dic, returns[math.floor(entity_numbers * 0.2)], returns[math.floor(entity_numbers * 0.8)]

def _order_sankey_nodes(data, _set, metric_id):

    s = set()
    entity_metric_data, min_return, max_return = _get_entity_metric_value(_set, metric_id)
    nodes = []

    for record in data:
        dic = {}
        if record.grand_parent_name and record.grand_parent_name not in s:
            dic = {'id': record.grand_parent_id, 'name': record.grand_parent_name}
            dic.update(entity_metric_data.get(record.grand_parent_id, {'emv': 0,'return': 0}))
            s.add(record.grand_parent_name)
            nodes.append(dic)
        if record.parent_name and record.parent_name not in s:
            dic = {'id': record.parent_id, 'name': record.parent_name}
            dic.update(entity_metric_data.get(record.parent_id, {'emv': 0,'return': 0}))
            s.add(record.parent_name)
            nodes.append(dic)
        if record.child_name and record.child_name not in s:
            dic = {'id': record.child_id, 'name': record.child_name}
            dic.update(entity_metric_data.get(record.child_id, {'emv': 0,'return': 0}))
            s.add(record.child_name)
            nodes.append(dic)

    return nodes, min_return, max_return

def _get_threshold_for_charting_sankey(links, metric_id):
    
    ln_value = []

    threshold = None

    if metric_id == 1:
        for link in links:
            if link.get('level') != 4:
                ln_value.append(math.log(math.fabs(link.get('value')) + 1))

        sorted_list = sorted(ln_value)
        threshold = sorted_list[math.floor(len(sorted_list) * 0.30)]

    return threshold

def m_assets_statistics(set):
    statistics = {}

    entities = raw_db.query(asset_sqls.m_assets_statistics, set_id = set.id)
    total_amount = raw_db.query(asset_sqls.m_total_amount, set_id = set.id, date_key = set.date_key)

    statistics = {
        'entities': entities.to_dict(),
        'totalAmount': total_amount.first().total_amount
    }

    return statistics

def m_assets_level_details(level, set, page, page_size):
    parameters = {
        'date_key': set.date_key,
        'offset': (page - 1) * page_size,
        'limit': page_size,
        'set_id': set.id,
        'level': level
    }
    counts = raw_db.query(asset_sqls.m_assets_level_detail_counts, parameters).first().counts
    details = raw_db.query(asset_sqls.m_assets_level_detail, parameters)
    level_name = Structure.query.filter_by(set_id = set.id).filter_by(level = level).first().level_name
    return details, level_name, counts

def m_is_lowest_level(entity_id):

    entity_set = EntitySet.query.filter_by(group_id = g.user.group_id).order_by(EntitySet.date_key.desc()).first()
    structure = Structure.query.filter_by(entity_id = entity_id).filter_by(set_id = entity_set.id).first()
    lowest_level = Structure.query.filter_by(set_id = entity_set.id)\
                    .order_by(Structure.level.desc())\
                    .first().level

    return structure, lowest_level, entity_set.date_key

def m_get_metrics_data_of_structure(entity_id, date_key):

    metrics_data = raw_db.query(asset_sqls.m_entity_detail, entity_id = entity_id, date_key = date_key).first()

    return metrics_data

def m_top3_holding_funds(entity_id, lowest_level, date_key):

    parameters = {
        'id': entity_id,
        'lowest_level': lowest_level,
        'date_key': date_key
    }
    
    top3_holding_funds = raw_db.query(asset_sqls.m_top3_holding_funds, parameters)

    return top3_holding_funds

def m_all_funds(entity_id, lowest_level, date_key, page, page_size):

    parameters = {
        'id': entity_id,
        'lowest_level': lowest_level,
        'date_key': date_key,
        'offset': (page - 1) * page_size,
        'limit': page_size
    }

    counts = raw_db.query(asset_sqls.m_holding_funds_counts, parameters).first().counts
    funds = raw_db.query(asset_sqls.m_holding_funds, parameters)

    return funds, counts, 'Manager'