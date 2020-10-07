from flask_restful import Resource, request
from flask import jsonify, make_response
from bson import json_util
from flask_jwt_extended import jwt_required

from models.notification import NotificationModule


class Notification(Resource):
    @jwt_required
    def get(self, _id):
        noti_list = []
        data = NotificationModule.find_by_creator_id(_id)
        if data:
            notis = list(data)
            for noti in notis:
                noti_list.append(noti)
            return make_response(json_util.dumps(noti_list, ensure_ascii=False).encode('utf8'), 200)
        else:
            return {"msg": "error"}, 400

class ReplyNotification(Resource):
    @jwt_required
    def get(self, _id):
        noti_list = []
        data = NotificationModule.find_by_user_id(_id)
        print(data)
        if data:
            notis = list(data)
            for noti in notis:
                noti_list.append(noti)
            return make_response(json_util.dumps(noti_list, ensure_ascii=False).encode('utf8'), 200)
        else:
            return {"msg": "error"}, 400