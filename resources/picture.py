from flask_restful import Resource, request
from flask import jsonify, make_response
from bson import json_util
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt_claims


from database import Database
from schemas.picture import PictureSchema
from models.picture import PictureModule
from models.vendor import VendorModule

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


class PictureCreation(Resource):
  # create new pic
    @jwt_required
    def post(self):
        claims = get_jwt_claims()
        if claims['role'] != 'user':
            data = picture_schema.load(request.get_json())

            creator_id = get_jwt_identity()
            creator = VendorModule(id=creator_id).find_by_id()

            pic = PictureModule(creator_name=creator["username"], **data)

            pic.id = pic.get_maxium_pics

            trigger_data = {
                "id": pic.id,
                "title": pic.title,
                "creator": pic.creator_name,
                "status": pic.status,
                "price": pic.price,
                "category": pic.category,
                "admin_confirmation": pic.admin_confirmation,
                "created_at": pic.created_at,
                "artist": pic.artist
            }

            response_pic = picture_schema.dump(pic)
            pic_creation = pic.save_pic_to_db(response_pic, trigger_data)
        else:
            return {"msg": "Forbidden"}, 403
