from marshmallow import Schema, fields

class TaskSchema(Schema):
    id = fields.Str(dump_only=True)
    name = fields.Str(required=True)
    status = fields.Str(required=True)
    
class TaskUpdateSchema(Schema):
    name = fields.Str()
    status = fields.Str()