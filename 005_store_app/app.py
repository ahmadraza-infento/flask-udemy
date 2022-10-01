import uuid
from db import stores, items
from flask import Flask, request
from flask_smorest import abort


app    = Flask(__name__)


#region Store
@app.post("/store")
def create_store():
    store_data      = request.get_json()
    
    if tuple(store_data) != ('name',):
        abort(400, "Bad request. Insure that 'name' is included in json payload.")

    if store_data['name'] in [store['name'] for store in stores.values() ]:
        abort(400, "Store already exists")

    store_id        = uuid.uuid4().hex
    new_store       = {**store_data, "id":store_id} 
    stores[store_id]= new_store
    return new_store, 201

@app.get("/store/<string:store_id>")
def get_store(store_id):
    try:
        return stores[store_id], 200
    
    except KeyError:
        abort(404, "Store not found")

@app.get("/store/item/<store_id>")
def get_store_items(store_id):

    if store_id in stores:
        store_items = [item for item_id, item in items.items() 
                            if item['store_id'] == store_id]
        return {"items": store_items}, 200
    
    else:
        abort(404, "Store not found")

@app.get("/store")
def get_stores():
    return {"stores" : list( stores.values() ) }

@app.delete("/store/<string:store_id>")
def delete_store(store_id):
    try:
        del stores[store_id]
        return {"message":"Store deleted."}, 200
    except KeyError:
        abort(404, "Store not found.")

@app.put("/store/<string:store_id>")
def update_store(store_id):
    store_data = request.get_json()
    if tuple(store_data) != ('name',):
        abort(404, "Bad request. Insure that 'name' is included in json payload.") 
    
    try:
        store = stores[store_id]
        store |= store_data
        return store, 200
    except KeyError:
        abort(404, "Store not found.")

#endregion

#region Store Item
@app.get("/item/<string:item_id>")
def get_item(item_id):
    try:
        return items[item_id], 200
    except KeyError:
        abort(404, "Item not found.")

@app.post("/store/item")
def create_store_item():
    item_data       = request.get_json()
    if tuple(item_data) != ('store_id', 'name' , 'price'):
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

@app.delete('/item/<string:item_id>')
def delete_item(item_id):
    try:
        del items[item_id]
        return {"message":"Item deleted."}, 200
    except KeyError:
        abort(404, "Item not found.")


@app.put("/item/<string:item_id>")
def update_item(item_id):
    item_data = request.get_json()
    if tuple(item_data) != ('name', 'price'):
        abort(404, "Bad request. Insure that 'name' and 'price' is included in json payload.")
    
    try:
        item = items[item_id]
        item |= item_data
        return item, 200
    except KeyError:
        abort(404, "Item not found.")



#endregion 


if __name__ == "__main__":
    app.run(port=5000)