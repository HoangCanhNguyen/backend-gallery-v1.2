from marshmallow import Schema, fields

from schemas.user import UserSchema


class VendorSchema(UserSchema):
    class Meta():
        load_only = ("raw_password",)
        dump_only = ("admin_confirmation","id", "password","status",)

    dateOfBirth = fields.Raw()
    description = fields.Str()
    role = fields.Str()
    tel = fields.Str()