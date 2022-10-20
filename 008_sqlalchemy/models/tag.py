from db import db



class TagModel(db.Model):
    __tablename__ = "tag"
    id  = db.Column(db.Integer, primary_key=True )
    name= db.Column(db.String(100), unique=False, nullable=False)
    store_id = db.Column(db.Integer, db.ForeignKey("store.id"), unique=False, nullable=False)

    store = db.relationship("StoreModel", back_populates="tags")