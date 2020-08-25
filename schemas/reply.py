from marshmallow import Schema, fields


class ReplySchema(Schema):
  class Meta:
    load_only = ("cmt_id", )
    dumb_only = ("content", "created_at", "user_id", )

  id = fields.Str()
  user_id = fields.Str()
  cmt_id = fields.Str()
  content = fields.Str()
  created_at = fields.Str()
