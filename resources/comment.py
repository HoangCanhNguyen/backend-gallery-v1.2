from flask_restful import Resource, request
from flask import jsonify, make_response
from bson import json_util
from flask_jwt_extended import jwt_required
from config import pusher

from models.comment import CommentModule
from models.notification import NotificationModule
from models.picture import PictureModule
from models.user import UserModule


class Comment(Resource):
    def post(self):
        _pic_id = request.get_json()["pic_id"]
        cmts = list(CommentModule.find_by_pic_id(_pic_id))

        return make_response(json_util.dumps(cmts, ensure_ascii=False).encode('utf8'), 200)

class Comment1(Resource):
    def get(self, _id):
        cmt = CommentModule.find_one_comment_by_id(_id)
        print(cmt)
        return make_response(json_util.dumps(cmt, ensure_ascii=False).encode('utf8'), 200)


class CommentCreation(Resource):
    # @jwt_required
    def post(self):
        cmt_data = request.get_json()

        _id = CommentModule.create_comment_id()

        pic = PictureModule(id=cmt_data["pic_id"])
        pic_data = pic.find_by_id()
        pic_title = pic_data["title"]
        pic_category = pic_data["category"]
        creator_name = cmt_data["creator_name"]
        creator = UserModule(username=creator_name)
        creator_id = creator.find_by_username()["id"]

        comment = {
            "id": _id,
            "username": cmt_data["username"],
            "pic_id": cmt_data["pic_id"],
            "content": cmt_data["content"],
            "user_id":cmt_data["user_id"],
            "star": cmt_data["star"],
            "avatarURL": cmt_data["avatarURL"]
        }

        notification = {
            "pic_id": cmt_data["pic_id"],
            "pic_title": pic_title,
            "created_at": cmt_data["created_at"],
            "commenter_username": cmt_data["username"],
            "creator_id": creator_id,
            "pic_category": pic_category
        }

        comment_channel = "comment-channel_%s" % (creator_id)
        status = CommentModule.create_comment(comment)
        NotificationModule.save_notification_to_db(notification)
        pusher.trigger(comment_channel, 'comment', json_util.dumps(notification))
        return make_response(json_util.dumps(comment, ensure_ascii=False).encode('utf8'), 200) if status else None

