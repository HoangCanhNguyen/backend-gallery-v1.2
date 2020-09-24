from flask_restful import Resource, request
from flask import jsonify, make_response, url_for
from bson import json_util
from flask_jwt_extended import jwt_required, get_jwt_claims, get_raw_jwt, get_jwt_identity

from jwt_token import access_token, refresh_token, recreate_access_token
from confirmation_token import generate_confirmation_token
from config import queue as q

from models.vendor import VendorModule
from models.picture import PictureModule

from schemas.vendor import VendorSchema
from blacklist import BLACKLIST
from mail import Mail


vendor_schema = VendorSchema()


class VendorRegister(Resource):
    def post(self):
        data = vendor_schema.load(request.get_json())

        vendor = VendorModule(**data)
        if (vendor.find_by_username()):
            return {"msg": "TÊN ĐĂNG NHẬP ĐÃ TỒN TẠI"}, 400
        if (vendor.find_by_email()):
            return {"msg": "EMAIL ĐÃ TỒN TẠI"}, 400

        token = generate_confirmation_token(vendor.email)
        confirm_url = url_for('userregister', token=token, _external=True)

        email_confirmation = q.enqueue(Mail.send_mail_confirmation_to_user, args=(
            vendor.email, confirm_url,), result_ttl=0)

        vendor.id = vendor.find_maxium_user()
        vendor.password = vendor.hash_password

        trigger_data = {
            "id": vendor.id,
            "username": vendor.username,
            "email": vendor.email,
            "tel": vendor.tel,
            "role": vendor.role,
            "status": vendor.status,
        }

        email_confirmation = q.enqueue(vendor.save_to_database, args=(
            vendor_schema.dump(vendor), trigger_data,), result_ttl=0)

        return {"msg": "XÁC THỰC EMAIL ĐỂ KÍCH HOẠT TÀI KHOẢN"}, 201


class VendorInfo(Resource):
    def post(self):
        data = request.get_json()
        vendor = VendorModule(email=data["email"])
        data["id"] = vendor.create_information_id()
        if vendor.find_by_email():
            vendor.save_vendor_info_to_db(data), 200
        else:
            return 400


class VendorLogin(Resource):
    def post(self):
        data = vendor_schema.load(request.get_json())

        vendor = VendorModule(**data)
        current_vendor = vendor.find_by_email()

        if current_vendor and vendor.verify_password():
            if current_vendor["status"] != "pending approval" and current_vendor["role"] == 'artist' or current_vendor["role"] == 'collector':
                accessToken = access_token(
                    current_vendor["id"], True)
                refreshToken = refresh_token(
                    current_vendor["id"])
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


class AccountInfo(Resource):
    def get(self):
        account_list = []
        accounts = list(VendorModule.find_all_account())
        for account in accounts:
            account_list.append(account)
        return make_response(json_util.dumps(account_list, ensure_ascii=False).encode('utf8'), 200)

    def post(self):
        account_list = []
        status = request.get_json()["status"]
        accounts = VendorModule.filter_by_status(status)
        for account in accounts:
            account_list.append(account)
        return make_response(json_util.dumps(account_list, ensure_ascii=False).encode('utf8'), 200)


class PendingApproval(Resource):
    @jwt_required
    def get(self):
        account_num = VendorModule.get_pending_approval()
        return make_response(json_util.dumps(account_num), 200)

    @jwt_required
    def post(self):
        user = VendorModule(**request.get_json())
        current_user = user.vendor_approval()


class PictureByCreator(Resource):
    @jwt_required
    def get(self):
        pic_list = []
        role = get_jwt_claims()['role']
        if role != 'user':
            vendor = VendorModule(id=get_jwt_identity())
            creator_name = vendor.find_by_id()['username']
            picObj = PictureModule(creator_name=creator_name)
            pics = list(picObj.find_by_creator_name())
            for pic in pics:
                pic_list.append(pic)
            return make_response(json_util.dumps(pic_list, ensure_ascii=False).encode('utf8'), 200)
        else:
            return {"msg": "Forbidden"}, 403
