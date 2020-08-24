from flask_restful import Resource, request
from flask import jsonify, url_for
from flask_jwt_extended import jwt_required, get_jwt_claims, get_raw_jwt
from marshmallow import ValidationError
from threading import Thread

from database import db, Database
from schemas.user import UserSchema
from models.user import UserModule
from confirmation_token import generate_confirmation_token
from jwt_token import access_token, refresh_token, recreate_access_token
from blacklist import BLACKLIST
from mail import Mail


user_schema = UserSchema()


class UserRegister(Resource):
    def post(self):
        user_data = user_schema.load(request.get_json())

        username = user_data["username"]
        email = user_data["email"]
        raw_password = user_data["raw_password"]

        user = UserModule.find_by_username(username)

        if user:
            return {"msg": "TÊN ĐĂNG NHẬP ĐÃ TỒN TẠI"}, 400
        if UserModule.find_by_email(email):
            return {"msg": "EMAIL ĐÃ TỒN TẠI"}, 400

        token = generate_confirmation_token(email)
        confirm_url = url_for('userregister', token=token, _external=True)

        sending_thread = Thread(target=Mail.send_mail_confirmation_to_user, args=(
            email, confirm_url,), daemon=True)
        sending_thread.start()

        password = UserModule.hash_password(raw_password)
        _id = UserModule.find_maxium_user()
        data = UserModule(_id=_id, password=password, **user_data)
        converted_data = user_schema.dump(data)

        if Database.save_user_to_db(converted_data):
            return {"msg": "XÁC THỰC EMAIL ĐỂ KÍCH HOẠT TÀI KHOẢN"}, 201


class UserLogin(Resource):
    def post(self):
        user_data = user_schema.load(request.get_json())

        email = user_data["email"]
        password = user_data["raw_password"]

        user = UserModule.find_by_email(email)
        if user and UserModule.verify_password(email, password):
            if user["activated"]:
                accessToken = access_token(
                    UserModule.find_by_email(email)["id"], True)
                refreshToken = refresh_token(
                    UserModule.find_by_email(email)["id"])
                return {
                    "access_token": accessToken,
                    "refresh_token": refreshToken
                }, 200
            return {'msg': 'Hãy xác nhận email của bạn'}, 401
        return {'msg': 'Opps, BẠN KHÔNG THỂ ĐĂNG NHẬP'}, 401


class UserLogout(Resource):
    @jwt_required
    def post(self):
        jti = get_raw_jwt()['jti']
        BLACKLIST.add(jti)
        return {"msg": "Log out successfully"}


class TokenRefresh(Resource):
    def post(self):
        new_token = recreate_access_token()
        if new_token:
            return {"access_token": new_token}, 200
        return {"msg": "Can not create new access token"}, 400



