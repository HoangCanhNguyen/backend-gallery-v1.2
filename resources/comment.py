from flask_restful import Resource, request
from flask import jsonify, make_response
from bson import json_util

from models.comment import CommentModule


class Comment(Resource):
    def post(self):
        _pic_id = request.get_json()["pic_id"]
        cmts = list(CommentModule.find_by_pic_id(_pic_id))

        return make_response(json_util.dumps(cmts, ensure_ascii=False).encode('utf8'), 200)


class CommentCreation(Resource):
    def post(self):
      pass