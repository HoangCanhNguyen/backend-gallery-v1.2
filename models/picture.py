from database import pic_col
from schemas.picture import PictureSchema
from config import pusher

class PictureModule:
    def __init__(self, id='', title='', creator_name='', artist='', category='', price='', imageURL='', description='',status='in stock',admin_confirmation=False,created_at='', **kwargs):
        self.id = id
        self.title = title
        self.creator_name = creator_name
        self.artist = artist
        self.category = category
        self.price = price
        self.imageURL = imageURL
        self.description = description
        self.status = status
        self.admin_confirmation = admin_confirmation
        self.created_at = created_at

    def find_by_title(self):
        pic = pic_col.find_one({"title": self.title})
        return pic if pic else None

    @property
    def find_by_id(self):
        pic = pic_col.find_one({"id": self.id})
        return pic if pic else None

    @property
    def get_maxium_pics(self):
        return pic_col.find().count() + 1

    def save_pic_to_db(self, data):
        pic_col.insert_one(self)
        pusher.trigger("picture", "creation", data)

    @classmethod
    def get_all_pics(cls):
        pics = pic_col.find()
        return pics
