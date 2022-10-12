from flask import request
from flask.views import MethodView
from flask_smorest import abort, Blueprint
from db import items
from schemas import StoreItemUpdateSchema, StoreItemSchema

blp = Blueprint("items", __name__, "operations on store items")


@blp.route("/item/<string:item_id>")
class Item(MethodView):

    @blp.response(200, StoreItemSchema)
    def get(self, item_id):
        try:
            return items[item_id], 200
        except KeyError:
            abort(404, "Item not found.")

    @blp.arguments(StoreItemUpdateSchema)
    @blp.response(200, StoreItemSchema)
    def put(self, item_data, item_id):
        try:
            item = items[item_id]
            item |= item_data
            return item, 200
        except KeyError:
            abort(404, "Item not found.")

    def delete(self, item_id):
        try:
            del items[item_id]
            return {"message":"Item deleted."}, 200
        except KeyError:
            abort(404, "Item not found.")

