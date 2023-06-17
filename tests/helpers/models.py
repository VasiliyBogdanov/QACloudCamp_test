from marshmallow import Schema, fields


class PostSchema(Schema):
    id = fields.Integer(strict=True, required=True)
    title = fields.String(required=True)
    body = fields.String(required=True)
    userId = fields.Integer(strict=True, required=True)
