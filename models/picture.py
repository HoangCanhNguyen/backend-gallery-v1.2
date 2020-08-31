from database import pic_col
from schemas.picture import PictureSchema


class PictureModule:
    def __init__(self, id='', title='', **kwargs):
        self.id = id
        self.title = title

    @staticmethod
    def find_by_title(title):
        pic = pic_col.find_one({"title": title})
        return pic if pic else None

    @classmethod
    def find_by_id(cls, _id):
        pic = pic_col.find_one({"id": _id})
        return pic if pic else None

    @classmethod
    def get_all_pics(cls):
        pics = pic_col.find()
        return pics
