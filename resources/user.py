from flask_restful import Resource, request
from flask import url_for, make_response, render_template
from flask_jwt_extended import jwt_required, get_jwt_claims, get_raw_jwt, get_jwt_identity
from threading import Thread
from bson import json_util

from database import db, Database
from schemas.user import UserSchema
from models.user import UserModule
from models.confirmation import ConfirmationModule
from models.ConfirmPasswordForm import UserRegistryForm
from confirmation_token import generate_confirmation_token
from jwt_token import access_token, refresh_token, recreate_access_token
from blacklist import BLACKLIST
from mail import Mail

from flask_jwt_extended import jwt_required

user_schema = UserSchema()


class UserInfo(Resource):
    @jwt_required
    def get(self):
        user_info = UserSchema(
            only=("username", "id", "email", "role", "avatarURL"))
        _id = get_jwt_identity()
        user = UserModule.find_by_id(_id)
        current_user = UserModule(**user)
        reponse_user = user_info.dump(current_user)
        return make_response(reponse_user)


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
        id = UserModule.find_maxium_user()
        data = UserModule(id=id, password=password, **user_data)
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
            if user["activated"] and user["role"] == 'user' or user["role"] =='admin':
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


class UserLogout(Resource):
    @jwt_required
    def get(self):
        jti = get_raw_jwt()['jti']
        BLACKLIST.add(jti)
        return {"msg": "Log out successfully"}


class PasswordConfirmation(Resource):
    def get(self):
        token = request.args.get('token')
        url = request.path
        email = ConfirmationModule.confirm_email(token)
        return make_response(render_template('auth_credential.html', email=email, token=token))


class ConfirmPasswordAction(Resource):
    def post(self, token):
        form = UserRegistryForm()
        # if form.validate_on_submit():
        raw_password = request.form['password']
        email = ConfirmationModule.confirm_email(token)
        password = UserModule.hash_password(raw_password)
        data = {"email": email, "password": password}
        Database.update_user_in_db(data)


class TokenRefresh(Resource):
    def post(self):
        new_token = recreate_access_token()
        if new_token:
            return {"access_token": new_token}, 200
        return {"msg": "Can not create new access token"}, 400


class AvatarUpload(Resource):
    @jwt_required
    def post(self):
        _id = get_jwt_identity()
        avatarURL = request.get_json()["avatarURL"]
        result = UserModule.upload_avatar(_id, avatarURL)
