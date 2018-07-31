import datetime

from flask import g
from app.ext import raw_db, db
from app.sqls import collection_sqls
from app.utils.time_utils import datetime_to_timestamp
from app.db_models.collection import Collection, CollectionItem

def collection_exist_or_not():

    collection = Collection.query.filter_by(title = g.args.get('title')).filter_by(user_id = g.user.id).filter_by(state = 1).first()
    if collection:
        return True
    else:
        return False

def create_collection():

    collection = Collection.from_dict(g.args)
    collection.user_id = g.user.id
    db.session.add(collection)
    db.session.flush()

    if g.args.get('items'):
        for item in g.args.get('items'):
            collection_item = CollectionItem.from_dict(item)
            collection_item.name = item.get('charting_data').get('title')
            collection_item.collection_id = collection.id
            db.session.add(collection_item)

        db.session.commit()
    return collection

def delete_collection(collection_id):

    collection = Collection.query.get(collection_id)
    collection.state = 0
    db.session.commit()

def batch_delete_collection():

    collection_ids = g.args.get('collection_ids', [])

    if len(collection_ids) == 0:
        return

    raw_db.query(collection_sqls.batch_delete_collection, {'state':0, 'ids': tuple(collection_ids)})

def delete_collection_item(collection_item_id):

    collection_item = CollectionItem.query.get(collection_item_id)
    db.session.delete(collection_item)
    db.session.commit()


def get_collections_by_page(page, page_size,search):

    parameters = {
        'offset': (page - 1) * page_size,
        'limit': page_size,
        'user_id': g.user.id
    }

    if search:
        parameters['search'] = '%{}%'.format(search)
        sql = collection_sqls.search_collections
    else:
        sql = collection_sqls.get_collections_by_page   
    
    return raw_db.query(sql, parameters).to_dict()


def update_collection(collection_id):

    collection = Collection.query.get(collection_id)
    collection.update_dict(g.args)

    if g.args.get('item'):
        item = CollectionItem()
        item.name = g.args.get('item').get('name')
        item.charting_data = g.args.get('item').get('chartingData')
        item.collection_id =  int(collection_id)
        db.session.add(item)

    collection.updated_time = datetime.datetime.utcnow()

    db.session.commit()

    if g.args.get('item'):
        return item
    else:
        return None

def get_collection_items_by_collection_id(collection_id, page, page_size):

    parameters = {
        'offset': (page - 1) * page_size,
        'limit': page_size,
        'collection_id': collection_id
    }

    return raw_db.query(collection_sqls.get_collection_item_by_collection_id, parameters).to_dict()