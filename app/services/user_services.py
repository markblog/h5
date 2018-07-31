from flask import g
from app.db_models.asset import EntitySet
from app.ext import raw_db
from app.sqls import user_sqls, user_extend_sqls
from app.db_models.user import User, Role
from app.db_models.user_extend import UserEntity
from app.ext import db

from app.utils.decorators import admin_oper
from app.services import asset_services

import datetime

def get_user_by_email():
    """
    query user data filter by email
    """
    user = User.query.filter_by(email = g.args.get('email').lower()).first()
    return user

def create_user():
    """
    update user data to the database
    """
    user = User.from_dict(g.args)
    user.email = user.email.lower()
    db.session.add(user)
    db.session.commit()

def get_all_group():

    groups = raw_db.query(user_sqls.get_all_group).to_dict()

    return groups

def get_users_except_current_user():

    users = raw_db.query(user_sqls.get_users_except_current_user, group_id = g.user.group_id, user_id = g.user.id)

    return users

def get_user_profile():

    user = User.query.get(g.user.id)

    return user


def get_user_id_by_email(email):

    user_id = raw_db.query(user_sqls.get_user_id_by_email, email=email).first()
    if user_id:
        user_id = user_id.to_dict()
    else:
        print("user_id is null")
        return None

    return user_id.get('id')

def get_user_detail(user_id):

    if user_id:
        pass
    else:
        user_id = g.user.id

    user = User.query.get(user_id)

    result = {}
    detail = raw_db.query(user_sqls.get_user_detail, group_id=user.group_id).first().to_dict()
    result['colleague'] = detail
    result['user'] = user.to_dict(excludes = ['password_hash', 'group_id'])

    return result

@admin_oper
def get_all_user(page, page_size):

    parameters = {
        'offset': (page - 1) * page_size,
        'limit': page_size,
        'group_id': g.user.group_id
    }

    users = raw_db.query(user_sqls.get_all_user, parameters).to_dict()
    total_users_count = raw_db.query(user_sqls.get_all_count, parameters).first()

    result = {}
    result['users'] = users
    result['totalUsersCount'] = total_users_count.total_users_count

    return result

@admin_oper
def get_user_active():

    parameters = {
        "status": 1, 
        'group_id': g.user.group_id
    }

    activated = raw_db.query(user_sqls.get_active_from_user, parameters).first()
    inactivated = raw_db.query(user_sqls.get_active_from_user, parameters).first()

    results = {
        "activated_count": activated.count,
        "all_count": activated.count + inactivated.count
    }
    return results

@admin_oper
def search_user(search, page, page_size):

    parameters = {
        "search1": '%{}%'.format(search.lower()),
        "search2": '%{}%'.format(search.upper()),
        'offset': (page - 1) * page_size,
        'limit': page_size,
        'group_id': g.user.group_id
    }

    result = raw_db.query(user_sqls.search_user, parameters).to_dict()
    result_count = raw_db.query(user_sqls.search_count, parameters).first()
    parameters['status'] = 1
    result_count_activated = raw_db.query(user_sqls.search_count_activated,parameters).first()

    results = {}
    results['users'] = result
    results['totalUsersCount'] = result_count.count
    results['totalActivated'] = result_count_activated.count

    return results

@admin_oper
def update_modify_time(user_id):
    user = User.query.get(user_id)
    user.updated_time = datetime.datetime.utcnow()

    db.session.commit()

@admin_oper
def update_user_active(user_id):

    user = User.query.get(user_id)

    user.status = (user.status + 1) % 2
    user.updated_time = datetime.datetime.utcnow()

    db.session.commit()

@admin_oper
def add_entity_to_user(entitys):

    # entitys = g.args.get('entity')
    for entity in entitys:
        user_entity = UserEntity.from_dict(entity)
        db.session.add(user_entity)
    db.session.commit()

@admin_oper
def def_entity_from_user_batch(entitys):

    # entitys = g.args.get('entity')
    for entity in entitys:
        raw_db.query(user_extend_sqls.delete_user_entity,entity)

@admin_oper
def query_entity(user_id, page, page_size, search):

    parameters = {
        "group_id": g.user.group_id,
        "user_id": user_id,
        'offset': (page - 1) * page_size,
        'limit': page_size
    }

    # set_id = raw_db.query(user_extend_sqls.get_entity_set_id, parameters).to_dict()
    set_id = asset_services.get_default_set()
    parameters['set_id'] = set_id.id

    user_entity_ids = raw_db.query(user_extend_sqls.get_user_entity, parameters).to_dict()

    structure_ids = raw_db.query(user_extend_sqls.get_structure_id, parameters).to_dict()


    structure = []
    user_entity = []
    for structure_id in structure_ids:
        structure.append(structure_id.get('entityId'))

    structure = set(structure)

    if user_entity_ids:
        for user_entity_id in user_entity_ids:
            user_entity.append(user_entity_id.get('entityId'))
        user_entity = set(user_entity)
        activated = len(user_entity)
    else:
        user_entity.append(-1)
        user_entity = set(user_entity)
        activated = 0

    # print("before ---------- ", user_entity)

    # child_tree = set([])
    # for user_entity_id in user_entity:
    #     get_structure(user_entity_id, set_id.id, child_tree)

    # print("after ---------- ", child_tree)

    # user_entity = user_entity.union(child_tree)
    # activated = len(user_entity)

    dif = structure.difference(user_entity)
    total = len(dif)
    if total == 0:
        dif.add(-1)

    # print(user_entity, '------', structure)
    parameters['list1'] = tuple(user_entity)
    parameters['list2'] = tuple(dif)

    results = {}

    if search:
        parameters['search1'] = '%{}%'.format(search.lower())
        parameters['search2'] = '%{}%'.format(search.upper())

        result = raw_db.query(user_extend_sqls.get_entity_search, parameters).to_dict()
        search = raw_db.query(user_extend_sqls.get_entity_search_count, parameters).first()
        results['search'] = search.count
    else:
        result = raw_db.query(user_extend_sqls.get_entity, parameters).to_dict()

    results['entity'] = result
    results['activated'] = activated
    results['total'] = len(structure)
    results['set_id'] = parameters.get('set_id')

    # print(results)
    return results

@admin_oper
def add_del_all(user_id, access):

    parameters = {
        "group_id": g.user.group_id,
        "user_id": user_id
    }

    # set_id = raw_db.query(user_extend_sqls.get_entity_set_id, parameters).to_dict()
    set_id = asset_services.get_default_set()
    parameters['set_id'] = set_id.id

    if access == 1:
        raw_db.query(user_extend_sqls.delete_user_entity_all, parameters)
        return

    structure_ids = raw_db.query(user_extend_sqls.get_structure_id, parameters).to_dict()

    add_entity = {}
    add_entity['set_id'] = set_id.id

    for structure_id in structure_ids:
        add_entity['entity_id'] = structure_id.get('entityId')
        add_entity['user_id'] = user_id

        user_entity = UserEntity.from_dict(add_entity)
        db.session.add(user_entity)

    db.session.commit()


def get_access_entity_ids():
    set_id = asset_services.get_default_set()
    user_entity_ids = raw_db.query(user_extend_sqls.get_user_entity, {"user_id": g.user.id, "set_id": set_id.id}).to_dict()
    child_tree = set([])
    for user_entity_id in user_entity_ids:
        child_tree.add(user_entity_id.get('entityId'))
        structures = raw_db.query(user_extend_sqls.select_structure_by_parent_id, {"set_id": set_id.id,"entity_id": user_entity_id.get('entityId')}).all()
        # print("*** ",structures ," ***")
        if structures:
            for structure in structures:
                get_structure(structure.id, set_id.id, child_tree)

    # print("*** ", child_tree, " ***")
    return child_tree

def get_structure(structure_id, set_id, entity_ids):

    structures = raw_db.query(user_extend_sqls.select_by_parent_id_and_set_id, {"set_id": set_id,"parent_id": structure_id}).all()
    if structures:
        for structure in structures:
            # print("********* " ,structure.id, " *********")
            entity_ids.add(structure.entity_id)
            get_structure(structure.id, set_id, entity_ids)