from flask_restful import Resource, request
from flask import url_for, make_response, render_template
from flask_jwt_extended import jwt_required, get_jwt_claims, get_raw_jwt, get_jwt_identity
from bson import json_util

from config import queue as q

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


class User(Resource):
    @jwt_required
    def get(self):
        user_info = UserSchema(
            only=("username", "id", "email", "role", "avatarURL"))
        _id = get_jwt_identity()
        user = UserModule(id=_id)
        current_user = UserModule(**user.find_by_id())
        reponse_user = user_info.dump(current_user)
        return make_response(reponse_user)

    @jwt_required
    def delete(self, id):
        user = UserModule(id=id)
        user.delete_user()


class UserRegister(Resource):
    def post(self):
        data = user_schema.load(request.get_json())

        user = UserModule(**data)
        if user.find_by_username():
            return {"msg": "TÊN ĐĂNG NHẬP ĐÃ TỒN TẠI"}, 400
        if user.find_by_email():
            return {"msg": "EMAIL ĐÃ TỒN TẠI"}, 400

        token = generate_confirmation_token(user.email)
        confirm_url = url_for('userregister', token=token, _external=True)

        email_confirmation = q.enqueue(Mail.send_mail_confirmation_to_user, args=(
            user.email, confirm_url,), result_ttl=0)

        user.id = user.find_maxium_user()
        user.password = user.hash_password

        user.save_to_database(user_schema.dump(user))

        return {"msg": "XÁC THỰC EMAIL ĐỂ KÍCH HOẠT TÀI KHOẢN"}, 201


class UserLogin(Resource):
    def post(self):
        data = user_schema.load(request.get_json())

        user = UserModule(**data)
        user_exist = user.find_by_email()

        if user_exist and user.verify_password():
            if user_exist["status"] != "pending email":
                accessToken = access_token(
                    user_exist["id"], True)
                refreshToken = refresh_token(
                    user_exist["id"])
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
