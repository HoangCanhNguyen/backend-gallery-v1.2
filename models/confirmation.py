import time

from confirmation_token import confirm_token
from database import user_col


class ConfirmationModule:
    @classmethod
    def confirm_email(cls, token):
        try:
            email = confirm_token(token)
        except:
            return False
        user = user_col.find_one({"email": email})
        if user["status"] != "pending email":
            return True
        elif user["role"] == "user":
            user_col.update_one({"email": email}, {
                                "$set": {"status": "approved"}})
            return True
        else:
            user_col.update_one({"email": email}, {
                "$set": {"status": "pending approval"}
            })
            return True
