from flask_restful import Resource, request
from flask import jsonify, make_response
from bson import json_util
from flask_jwt_extended import jwt_required

from database import Database
from schemas.picture import PictureSchema
from models.picture import PictureModule

picture_schema = PictureSchema()


class Picture(Resource):
  # get all pics
    def get(self):
        pic_list = []
        pics = list(PictureModule.get_all_pics())
        for pic in pics:
            pic_list.append(pic)
        return make_response(json_util.dumps(pic_list, ensure_ascii=False).encode('utf8'), 200)

  # get pic by ID
    def post(self):
        pic = PictureModule(id=request.get_json()["id"])
        return make_response(json_util.dumps(pic.find_by_id), 200)

    def delete(self):
        pass

    def update(self):
        pass


class PictureInsert(Resource):
  # create new pic
    def post(self):
        data = request.get_json()
        pic = PictureModule(**data)
        pic.insert_picture()
    