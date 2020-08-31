from flask_pymongo import pymongo

from database import comment_col
from schemas.picture import PictureSchema

class CommentModule:
  def __init__(self, _id=''):
    self.id = _id

  @classmethod
  def find_by_pic_id(cls, _pic_id):
    cmt = comment_col.find({"pic_id": _pic_id})
    return cmt if cmt else None