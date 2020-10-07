from flask_pymongo import pymongo
from config import pusher

from database import comment_col
from schemas.picture import PictureSchema

class CommentModule:
  def __init__(self, _id=''):
    self.id = _id

  @classmethod
  def create_comment_id(cls):
    return str(comment_col.find().count() + 1)

  @classmethod
  def find_by_pic_id(cls, _pic_id):
    cmt = comment_col.find({"pic_id": _pic_id})
    return cmt if cmt else None

  @classmethod
  def create_comment(cls, data):
    try:
      comment_col.insert_one(data)
      return True
    except:
      return False

  @classmethod
  def find_one_comment_by_id(cls, _id):
    return comment_col.find_one({"id": _id})