from marshmallow import Schema, fields

class UserPostSchemaValidator(Schema):
    user_id = fields.Str()

