from marshmallow import Schema, fields


class UserSchema(Schema):
    class Meta:
        load_only = ("raw_password",)
        dump_only = ("id", "password","activated","role")

    id = fields.Str()
    username = fields.Str()
    raw_password = fields.Str()
    email = fields.Email()
    password = fields.Raw()
    activated = fields.Boolean(default=False)
    role = fields.Str(default="user")
    avatarURL = fields.Raw()
    address = fields.Str()