from flask_restful import Resource, request
from flask import jsonify, make_response
from bson import json_util

from database import Database
from schemas.picture import PictureSchema
from models.picture import PictureModule

picture_schema = PictureSchema()

class Picture(Resource):
  def get(self):
    pic_list = []
    pics = list(PictureModule.get_all_pics())
    for pic in pics:
      pic_list.append(pic)
    return make_response(json_util.dumps(pic_list, ensure_ascii=False).encode('utf8'), 200)
  