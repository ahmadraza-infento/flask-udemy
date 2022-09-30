import uuid
from db import stores, items
from flask import Flask, request
from flask_smorest import abort


app    = Flask(__name__)


@app.route("/store", methods=['POST'])
def create_store():
    store_data      = request.get_json()
    
    if 'name' not in store_data:
        abort(400, "Bad request. Insure that 'name' is included in json payload.")

    if store_data['name'] in [store['name'] for store in stores.values() ]:
        abort(400, "Store already exists")

    store_id        = uuid.uuid4().hex
    new_store       = {**store_data, "id":store_id} 
    stores[store_id]= new_store

    return new_store, 201

@app.route("/store/<string:store_id>")
def get_store(store_id):
    try:
        return stores[store_id], 200
    
    except KeyError:
        abort(404, "Store not found")
    
@app.route("/store")
def get_stores():
    return {"stores" : list( stores.values() ) }


@app.route("/store/item", methods=["POST"])
def create_store_item():
    item_data       = request.get_json()

    if ('store_id' not in item_data or
        'name' not in item_data or
        'price' not in item_data
        ):
        abort(400, "Bad request. Insure that 'store_id', 'name' and 'price' is included in json payload")
    
    for item in items.values():
        if item['store_id'] == item_data['store_id'] and item['name'] == item_data['name']:
            abort(400, "Item already exists.")

    if item_data['store_id'] in stores:
        item_id         = uuid.uuid4().hex 
        new_item        = {**item_data, "id":item_id}
        items[item_id]  = new_item
        return new_item, 201

    else:
        abort(404, "Store not found")

@app.route("/store/item", methods=["GET"])
def get_store_items():

    item_data   = request.get_json()
    if 'store_id' not in item_data:
        abort(404, "Bad request. Insure that 'store_id' is included in json payload")

    store_id    = item_data['store_id'] 
    if store_id in stores:
        store_items = [item for item_id, item in items.items() 
                            if item['store_id'] == store_id]
        return {"items": store_items}, 200
    
    else:
        abort(404, "Store not found")



if __name__ == "__main__":
    app.run(port=5000)