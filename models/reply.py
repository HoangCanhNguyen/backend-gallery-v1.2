from database import reply_col
from schemas.reply import ReplySchema


class ReplyModule:
    def __init__(self, _id=''):
        self.id = _id

    @classmethod
    def find_by_cmt_id(cls, cmt_id):
        reply = reply_col.find({"cmt_id": cmt_id})
        return reply if reply else None

    @classmethod
    def create_reply(cls, data):
        try:
            reply_col.insert_one(data)
            return True
        except:
            return False
