from config import pusher

from database import notification_col


class NotificationModule:
    def __init__(self, _id='', user_id ='', pic_id='', pic_title='', creator_id='', created_at='', commenter_id='', username='', **kwargs):
        self.id = _id
        self.user_id = user_id
        self.pic_id = pic_id
        self.pic_title = pic_title
        self.creator_id = creator_id
        self.created_at = created_at
        self.commenter_id = commenter_id
        self.username = username

    @classmethod
    def create_notification_id(cls):
        return str(notification_col.find().count() + 1)

    @classmethod
    def find_by_creator_id(cls, creator_id):
        return notification_col.find({"creator_id": creator_id})
    
    @classmethod
    def save_notification_to_db(cls, noti):
        try:
            notification_col.insert_one(noti)
            return True
        except:
            return False

    @classmethod
    def find_by_user_id(cls, user_id):
        return notification_col.find({"user_id": user_id})