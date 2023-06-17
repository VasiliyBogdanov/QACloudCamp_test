from marshmallow import Schema, ValidationError


def validate_json(json_dict: dict, schema: Schema, many=True):
    try:
        schema(many=many).load(json_dict)
    except ValidationError as e:
        return e.messages
