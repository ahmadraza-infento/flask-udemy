from schemas import PlainTagSchema, TagSchema
from flask_smorest import abort, Blueprint
from sqlalchemy.exc import SQLAlchemyError
from models import StoreModel, TagModel
from flask.views import MethodView
from db import db

blp = Blueprint("tags", __name__, "operations on item tags in a store")


@blp.route('/store/<int:store_id>/tag')
class TagsInStore(MethodView):
    @blp.response(200, PlainTagSchema(many=True))
    def get(self, store_id):
        store = StoreModel.query.get_or_404(store_id)
        return store.tags.all()

    @blp.arguments(PlainTagSchema)
    @blp.response(200, PlainTagSchema)
    def post(self, tag_data, store_id):

        if TagModel.query.filter(TagModel.name==tag_data['name'], TagModel.store_id==store_id).first():
            abort(400, message="The tag with same name is already created in this store.")

        tag = TagModel(**tag_data, store_id=store_id)
        try:
            db.session.add(tag)
            db.session.commit()
        
        except SQLAlchemyError as e:
            abort(500, str(e) )
        
        return tag


@blp.route('/store/tag/<int:tag_id>')
class TagOperations(MethodView):

    @blp.response(200, TagSchema)
    def get(self, tag_id):
        tag = TagModel.query.get_or_404(tag_id)
        return tag

    def delete(self, tag_id):
        tag = TagModel.query.get_or_404(tag_id)

        db.session.delete(tag)
        db.session.commit()

        return {"message": "tag deleted."}, 200