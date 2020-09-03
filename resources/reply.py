from flask_restful import Resource, request
from flask import jsonify, make_response
from bson import json_util
from flask_jwt_extended import jwt_required


from models.reply import ReplyModule


class Reply(Resource):
    def post(self):
        cmt_id = request.get_json()["cmt_id"]
        replies = list(ReplyModule.find_by_cmt_id(cmt_id))

        return make_response(json_util.dumps(replies, ensure_ascii=False).encode('utf8'), 200)


class ReplyCreation(Resource):
    @jwt_required
    def post(self):
        reply_info = request.get_json()
        return make_response(json_util.dumps(reply_info, ensure_ascii=False).encode('utf8'), 200) if ReplyModule.create_reply(reply_info) else None