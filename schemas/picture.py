from marshmallow import Schema, fields


class PictureSchema(Schema):

    class Meta:
        load_only = ("id", "comment_id", "user_id")
        
    id = fields.Str()
    comment_id = fields.Str()  # Foreign key
    user_id = fields.Str()  # Foreign key
    title = fields.Str()
    price = fields.Str()
    description = fields.Str()
    rating = fields.Int()
    category = fields.Str()
    artist = fields.Str()
    imageURL = fields.Str()
    status = fields.Str()
    dimension = fields.Str()
    created_at = fields.Str()
