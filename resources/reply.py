from flask_restful import Resource, request
from flask import jsonify, make_response
from bson import json_util
from flask_jwt_extended import jwt_required


from models.reply import ReplyModule
from models.notification import NotificationModule
from models.picture import PictureModule
from config import pusher

class Reply(Resource):
    def post(self):
        cmt_id = request.get_json()["cmt_id"]
        replies = list(ReplyModule.find_by_cmt_id(cmt_id))

        return make_response(json_util.dumps(replies, ensure_ascii=False).encode('utf8'), 200)


class ReplyCreation(Resource):
    @jwt_required
    def post(self):
        reply_info = request.get_json()
        pic = PictureModule(id=reply_info["pic_id"])
        pic_data = pic.find_by_id()
        print(reply_info)
        reply_channel = "reply-channel_%s" % (reply_info["commenter_id"])
        print(reply_channel)
        reply_status = ReplyModule.create_reply(reply_info)

        notification = {
            "pic_id":reply_info["pic_id"],
            "pic_title": pic_data["title"],
            "created_at": reply_info["created_at"],
            "commenter_username": reply_info["username"],
            "pic_category": pic_data["category"]
        }

        NotificationModule.save_notification_to_db(notification)
        pusher.trigger(reply_channel,'reply', json_util.dumps(notification))
        return make_response(json_util.dumps(reply_info, ensure_ascii=False).encode('utf8'), 200) if reply_status else None