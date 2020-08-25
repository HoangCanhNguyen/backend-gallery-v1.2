from marshmallow import Schema, fields


class FavouriteSchema(Schema):
  class Meta:
    load_only = ("user_id", )
    dumb_only = ("pic_id", )

  id = fields.Str()
  user_id = fields.Str()
  pic_id = fields.Str()
