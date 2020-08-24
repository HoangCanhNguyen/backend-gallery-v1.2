from marshmallow import Schema, fields

from user import UserSchema


class VendorSchema(UserSchema):
    class Meta():
        load_only = ("raw_password",)
        dump_only = ("admin_confirmation","id", "password","activated",)

    description = fields.Str()
    admin_confirmation = fields.Boolean(default=False)
    role = fields.Str()