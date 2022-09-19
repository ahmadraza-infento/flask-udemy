from flask import Flask, jsonify, request


app    = Flask(__name__)
stores = []

#POST /store {name:}
@app.route("/store", methods=['POST'])
def create_store():
    request_data= request.get_json()
    new_store   = {
                    "name"  : request_data['name'],
                    "items" : []
                } 
    stores.append(new_store)

    return jsonify(new_store)

#GET /store/<string:name>
@app.route("/store/<string:name>")
def get_store(name):
    
    for store in stores:
        if store['name'] == name:
            return jsonify(store)
    
    return jsonify({'message':"store not found"})

#GET /store
@app.route("/store")
def get_stores():
    return jsonify({"stores":stores})

#POST /store/<string:name>/item {name:, price:}
@app.route("/store/<string:name>/item", methods=["POST"])
def create_store_item(name):
    request_data = request.get_json()

    for store in stores:
        if store['name'] == name:
            new_item = {"name":request_data['name'], 'price':request_data['price']}
            store['items'].append( new_item )
            return jsonify(new_item)

    return jsonify({"message":"store not found"})

#GET /store/<string:name>/item
@app.route("/store/<string:name>/item", methods=["POST"])
def get_store_items(name):
    for store in stores:
        if store['name'] == name:
            return jsonify({'items': store['items']})
    
    return {"message":"store not found"}



app.run(port=5000)