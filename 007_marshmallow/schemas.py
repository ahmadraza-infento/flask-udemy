from marshmallow import Schema, fields


class StoreSchema(Schema):
    id  = fields.Str(dump_only=True)
    name= fields.Str(required=True)

class StoreUpdateSchema(Schema):
    id  = fields.Str(dump_only=True)
    name= fields.Str()
    
class StoreItemSchema(Schema):
    id      = fields.Str(dump_only=True)
    name    = fields.Str(required=True)
    price   = fields.Float(required=True)

class StoreItemUpdateSchema(Schema):
    id      = fields.Str(dump_only=True)
    name    = fields.Str()
    price   = fields.Float()