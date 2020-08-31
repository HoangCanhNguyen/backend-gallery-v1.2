import bcrypt
from flask_pymongo import pymongo
from flask import jsonify

from database import user_col
from confirmation_token import confirm_token


class UserModule():
    def __init__(self, id='', username='', password='', activated=False, email='', **kwargs):
        self.id = id
        self.username = username
        self.password = password
        self.activated = activated
        self.email = email

    @classmethod
    def find_maxium_user(cls):
        return str(user_col.find().count() + 1)

    @staticmethod
    def find_by_username(username):
        user = user_col.find_one({"username": username})
        return user if user else None

    @staticmethod
    def find_by_id(_id):
        user = user_col.find_one({"id": _id})
        return user if user else None

    @staticmethod
    def find_by_email(email):
        user = user_col.find_one({"email": email})
        return user if user else None

    @classmethod
    def verify_password(cls, email, password):
        if not user_col.find_one({"email": email}):
            return False
        else:
            hased_pw = user_col.find_one({"email": email})["password"]

        return True if bcrypt.checkpw(password.encode("utf-8"), hased_pw) else False

    @classmethod
    def hash_password(cls, password):
        return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

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
