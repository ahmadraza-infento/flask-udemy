from flask import request
from flask.views import MethodView
from flask_smorest import abort, Blueprint
from db import db
from models import ItemModel
from sqlalchemy.exc import SQLAlchemyError
from schemas import ItemUpdateSchema, ItemSchema

blp = Blueprint("items", __name__, "operations on store items")


@blp.route("/item/<string:item_id>")
@blp.route("/item")
class Item(MethodView):

    @blp.response(200, ItemSchema)
    def get(self, item_id):
        item = ItemModel.query.get_or_404(item_id)
        return item

    @blp.arguments(ItemSchema)
    @blp.response(201, ItemSchema)
    def post(self, item_data):
        item = ItemModel(**item_data)

        try:
            db.session.add(item)
            db.session.commit()
        
        except SQLAlchemyError:
            abort(500, "An error occured while creating item.")
        
        return item

    @blp.arguments(ItemUpdateSchema)
    @blp.response(200, ItemSchema)
    def put(self, item_data, item_id):
        item = ItemModel.query.get(item_id)
        if item:
            item.name = item_data['name']
            item.price= item_data['price']

        else:
            item = ItemModel(id=item_id, **item_id)
        
        db.session.add(item)
        db.session.commit()
        return item, 200

    def delete(self, item_id):
        item = ItemModel.query.get_or_404(item_id)
        db.session.delete(item)
        db.session.commit()

        return {"message":"Item deleted."}

    