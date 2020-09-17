from marshmallow import Schema, fields


class PictureSchema(Schema):

    class Meta:
        load_only = ("comment_id")
        dump_only = ("creator_id", "id")

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

    comment_id = fields.Str()
    rating = fields.Int()
    status = fields.Str()
    dimension = fields.Str()
    created_at = fields.Str()
