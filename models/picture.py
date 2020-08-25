'''
find_by_name
find_by_id
insert method
delete method
update method
'''

from flask_pymongo import pymongo
from flask import jsonify

from database import pic_col
from schemas.picture import PictureSchema

class PictureModule:
  def __inti__(self, _id ="", title="", **kwargs):
    self.id = _id,
    self.title = title

  @staticmethod
  def find_by_title(title):
    pic = pic_col.find_one({"title": title})
    return pic if pic else None

  @staticmethod
  def find_by_id(_id):
    pic = pic_col.find_one({"id": _id})
    return pic if pic else None

  @classmethod
  def get_all_pics(cls):
    pics = pic_col.find()
    return pics