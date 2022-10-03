import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import abort, Blueprint
from db import stores, items



blp = Blueprint("stores", __name__, description="Operations on store")

@blp.route("/store/<string:store_id>")
class Store(MethodView):
    def put(self, store_id):
        store_data = request.get_json()
        if tuple(store_data) != ('name',):
            abort(404, "Bad request. Insure that 'name' is included in json payload.") 
        
        try:
            store = stores[store_id]
            store |= store_data
            return store, 200
        except KeyError:
            abort(404, "Store not found.")

    def delete(self, store_id):
        try:
            del stores[store_id]
            return {"message":"Store deleted."}, 200
        except KeyError:
            abort(404, "Store not found.")

    def get(self, store_id):
        try:
            return stores[store_id], 200
        
        except KeyError:
            abort(404, "Store not found")


@blp.route("/store")
class StoreList(MethodView):
    def get(self):
        return {"stores" : list( stores.values() )}

    def post(self):
        store_data      = request.get_json()
    
        if tuple(store_data) != ('name',):
            abort(400, "Bad request. Insure that 'name' is included in json payload.")

        if store_data['name'] in [store['name'] for store in stores.values() ]:
            abort(400, "Store already exists")

        store_id        = uuid.uuid4().hex
        new_store       = {**store_data, "id":store_id} 
        stores[store_id]= new_store
        return new_store, 201


@blp.route("/store/item/<string:store_id>")
class StoreItem(MethodView):

    def get(self, store_id):
        if store_id in stores:
            store_items = [item for item_id, item in items.items() 
                                if item['store_id'] == store_id]
            return {"items": store_items}, 200
        
        else:
            abort(404, "Store not found")

    def post(self, store_id):
        item_data       = request.get_json()
        if tuple(item_data) != ('name' , 'price'):
            abort(400, "Bad request. Insure that 'name' and 'price' is included in json payload")
        
        for item in items.values():
            if item['store_id'] == store_id and item['name'] == item_data['name']:
                abort(400, "Item already exists.")

        if store_id in stores:
            item_id         = uuid.uuid4().hex 
            new_item        = {**item_data, "id":item_id, 'store_id':store_id}
            items[item_id]  = new_item
            return new_item, 201

        else:
            abort(404, "Store not found")
