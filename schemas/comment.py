from marshmallow import Schema, fields


class CommentSchema(Schema):
    class Meta:
        load_only = ("id",)
        dump_only = ("content", "rating", "created_at", "user_id", )

    id = fields.Str()
    user_id = fields.Str()
    pic_id = fields.Str()
    content = fields.Str()
    rating = fields.Int()
    created_at = fields.Str()
