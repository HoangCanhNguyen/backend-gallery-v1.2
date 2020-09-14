import bcrypt
from flask_pymongo import pymongo
from flask import jsonify

from database import user_col
from confirmation_token import confirm_token


class UserModule():
    def __init__(self, id='', username='', raw_password='', password='', status='pending email', avatarURL='', email='', role='user', **kwargs):
        self.id = id
        self.username = username
        self.password = password
        self.raw_password = raw_password
        self.status = status
        self.email = email
        self.avatarURL = avatarURL
        self.role = role

    def find_by_username(self):
        user = user_col.find_one({"username": self.username})
        return user if user else None

    def find_by_email(self):
        user = user_col.find_one({"email": self.email})
        return user if user else None

    def find_by_id(self):
        user = user_col.find_one({"id": self.id})
        return user if user else None

    @property
    def hash_password(self):
        return bcrypt.hashpw(self.raw_password.encode("utf-8"), bcrypt.gensalt())

    def verify_password(self):
        user = user_col.find_one({"email": self.email})
        if not user:
            return False
        else:
            hased_pw = user["password"]
        return True if bcrypt.checkpw(self.raw_password.encode("utf-8"), hased_pw) else False

    def delete_user(self):
        try:
            user_col.delete_one({"id": self.id})
        except:
            return None

    @classmethod
    def save_to_database(cls, data):
        user_col.insert_one(data)

    @classmethod
    def find_maxium_user(cls):
        return str(user_col.find().count() + 1)

    @classmethod
    def find_all_account(cls):
        collections = list(user_col.find({}, {
            "_id": 0,
            "id": 1,
            "username": 1,
            "email": 1,
            "role": 1,
            "status": 1
        }))
        return collections

    @classmethod
    def get_pending_approval(cls):
        return user_col.find({"status": "pending approval"}).count()

    @classmethod
    def confirm_email(cls, token):
        try:
            email = confirm_token(token)
        except:
            return False
        user = user_col.find_one({"email": email})
        if user["activated"]:
            return True
        else:
            user_col.update_one({"email": email}, {
                                "$set": {"activated": True}})
            return True

    @classmethod
    def upload_avatar(cls, _id, url):
        try:
            user_col.update_one({"id": _id}, {
                "$set": {"avatarURL": url}
            })
            return True
        except:
            return False
