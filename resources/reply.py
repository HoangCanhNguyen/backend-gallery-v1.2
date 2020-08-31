from flask_restful import Resource, request
from flask import jsonify, make_response
from bson import json_util

from models.reply import ReplyModule


class Reply(Resource):
    def post(self):
        cmt_id = request.get_json()["cmt_id"]
        replies = list(ReplyModule.find_by_cmt_id(cmt_id))

        return make_response(json_util.dumps(replies, ensure_ascii=False).encode('utf8'), 200)
