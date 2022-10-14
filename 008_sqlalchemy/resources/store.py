from db import db
from models import StoreModel
from flask.views import MethodView
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from flask_smorest import abort, Blueprint
from schemas import StoreSchema, StoreUpdateSchema


blp = Blueprint("stores", __name__, description="Operations on store")

@blp.route("/store")
class Store(MethodView):
    @blp.response(200, StoreSchema(many=True) )
    def get(self):
        return StoreModel.query.all()

    @blp.arguments(StoreSchema)
    @blp.response(200, StoreSchema)
    def post(self, store_data):
        new_store = StoreModel(**store_data)
        try:
            db.session.add(new_store)
            db.session.commit()
        except IntegrityError:
            abort(400, "A store with same name already exists.")
        
        except SQLAlchemyError:
            abort(500, "An error occured while creating store.")
        
        return new_store, 200

@blp.route("/store/<string:store_id>")
class StoreOperation(MethodView):
    
    @blp.response(200, StoreSchema)
    def get(self, store_id):
       store = StoreModel.query.get_or_404(store_id)
       return store

    @blp.arguments(StoreUpdateSchema)
    @blp.response(200, StoreSchema)
    def put(self, store_data, store_id): 
        store = StoreModel.query.get(store_id)
        if store:
            store.name = store_data['name']
        
        else:
            store = StoreModel(id=store_id, **store_data)
        
        db.session.add(store)
        db.session.commit()

        return store, 200

    def delete(self, store_id):
        store = StoreModel.query.get_or_404(store_id)
        db.session.delete(store)
        db.session.commit()

        return {"message":"store deleted."}, 200

