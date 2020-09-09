from flask_restful import Resource, request
from flask_jwt_extended import jwt_required, get_jwt_claims, get_raw_jwt, get_jwt_identity

from jwt_token import access_token, refresh_token, recreate_access_token

from models.user import UserModule
from schemas.user import UserSchema
from blacklist import BLACKLIST


user_schema = UserSchema()


class VendorLogin(Resource):
    def post(self):
        user_data = user_schema.load(request.get_json())

        email = user_data["email"]
        password = user_data["raw_password"]

        user = UserModule.find_by_email(email)
        if user and UserModule.verify_password(email, password):
            if user["activated"] and (user['role'] == 'artist' or user['role'] == 'collector'):
                accessToken = access_token(
                    UserModule.find_by_email(email)["id"], True)
                refreshToken = refresh_token(
                    UserModule.find_by_email(email)["id"])
                return {
                    "access_token": accessToken,
                    "refresh_token": refreshToken
                }, 200
            return {'msg': 'Opps, BẠN KHÔNG THỂ ĐĂNG NHẬP'}, 401
        return {'msg': 'TÀI KHOẢN/MẬT KHẨU KHÔNG ĐÚNG'}, 401

class VendorLogout(Resource):
    @jwt_required
    def get(self):
        jti = get_raw_jwt()['jti']
        BLACKLIST.add(jti)
        return {"msg": "Log out successfully"}