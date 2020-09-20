from marshmallow import Schema, fields


class PictureSchema(Schema):

    id = fields.Str()
    creator_id = fields.Str()
    title = fields.Str()
    price = fields.Str()
    description = fields.Str()
    category = fields.Str()
    artist = fields.Str()
    imageURL = fields.Str()
    admin_confirmation = fields.Boolean(default=False)
    status = fields.Str(default='in stock')
    creator_name = fields.Str(default='admin')
    comment_id = fields.Str()
    rating = fields.Int()
    status = fields.Str()
    dimension = fields.Str()
    created_at = fields.Str()
