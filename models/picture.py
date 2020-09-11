from database import pic_col
from schemas.picture import PictureSchema


class PictureModule:
    def __init__(self, id='', title='', **kwargs):
        self.id = id
        self.title = title

    def find_by_title(self):
        pic = pic_col.find_one({"title": self.title})
        return pic if pic else None

    @property
    def find_by_id(self):
        pic = pic_col.find_one({"id": self.id})
        return pic if pic else None

    @classmethod
    def get_all_pics(cls):
        pics = pic_col.find()
        return pics
