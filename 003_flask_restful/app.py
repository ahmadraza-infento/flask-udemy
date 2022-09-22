from flask import Flask, request
from flask_jwt import JWT, jwt_required
from flask_restful import Resource, Api
from security import authenticate, identity

app             = Flask(__name__)
app.secret_key  = "store_app"
api             = Api(app)
jwt             = JWT(app, authenticate, identity)
items           = []

class Item(Resource):
    @jwt_required()
    def get(self, name):
        item = next( filter(lambda i : i['name']==name, items), None)
        return {"item":item}, 200 if item else 404

    def post(self, name):
        if next( filter(lambda i : i['name']==name, items), None) is not None:
            return {"message": "An item with name '{}' already exists.".format(name)}, 400

        data = request.get_json()
        item = {'name':name, 'price':data['price']}
        items.append(item)

        return item, 201

    def delete(self, name):
        global items
        items = list(filter(lambda item: item['name'] != name, items))

        return {"message":"item deleted"}

    def put(self, name):
        data = request.get_json()
        item = next(filter(lambda item: item['name'] == name, items), None)
        if item:
            item['price'] = data['price']
        
        else:
            item = {'name':name, 'price':data['price']}
            items.append(item)
        
        return item, 201

class ItemsList(Resource):
    def get(self):
        return {"items":items}

api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemsList, '/items')

app.run(port=5000)
