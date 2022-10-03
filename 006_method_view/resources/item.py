from flask import request
from flask.views import MethodView
from flask_smorest import abort, Blueprint
from db import items


blp = Blueprint("items", __name__, "operations on store items")


@blp.route("/item/<string:item_id>")
class Item(MethodView):
    def get(self, item_id):
        try:
            return items[item_id], 200
        except KeyError:
            abort(404, "Item not found.")

    def delete(self, item_id):
        try:
            del items[item_id]
            return {"message":"Item deleted."}, 200
        except KeyError:
            abort(404, "Item not found.")

    def put(self, item_id):
        item_data = request.get_json()
        if tuple(item_data) != ('name', 'price'):
            abort(404, "Bad request. Insure that 'name' and 'price' is included in json payload.")
        
        try:
            item = items[item_id]
            item |= item_data
            return item, 200
        except KeyError:
            abort(404, "Item not found.")

