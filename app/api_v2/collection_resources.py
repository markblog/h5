from flask import request 

from app.utils.patch import BasicResource
from app.utils.decorators import auth
from app.services import collection_services

class CollectionListResource(BasicResource):

    @auth
    def get(self):
        page = request.args.get('page', default = 1, type = int)
        page_size = request.args.get('page_size', default = 9, type = int)
        search = request.args.get('search', None)

        return collection_services.get_collections_by_page(page, page_size, search)

    @auth
    def post(self):

        collection_exist_or_not = collection_services.collection_exist_or_not()

        if collection_exist_or_not:
            return 'Collection already exist, please change the collection name', 400
        else:
            collection = collection_services.create_collection()
            return { 'collectionId': collection.id }, 201


class CollectionResource(BasicResource):

    @auth
    def delete(self, collection_id):

        collection_services.delete_collection(collection_id)
        return 'collection delete success', 200

    @auth
    def put(self, collection_id):

        item = collection_services.update_collection(collection_id)

        if item:
            return {'collection_item_id': item.id}
        else:
            return 'collection updated success', 200

    @auth
    def post(self):

        collection_services.batch_delete_collection()
        return 'collection delete success', 200

class CollectionItemListResource(BasicResource):

    @auth
    def get(self, collection_id):

        page = request.args.get('page', default = 1, type = int)
        page_size = request.args.get('page_size', default = 9, type = int)

        return collection_services.get_collection_items_by_collection_id(collection_id, page, page_size)

class CollectionItemResource(BasicResource):

    @auth
    def delete(self, collection_item_id):

        collection_services.delete_collection_item(collection_item_id)

        return 'collection item is deleted'
