import time

from confirmation_token import confirm_token
from database import user_col
from worker import q as queue

class ConfirmationModule:
    @classmethod
    def confirm_email(cls, token):
        try:
            email = confirm_token(token)
        except:
            return False
        user = user_col.find_one({"email": email})
        if user["activated"]:
            return email
        else:
            user_col.update_one({"email": email}, {
                                "$set": {"activated": True}})
            return email

    @classmethod
    def check_activated(cls, email):
        try:
            activated = user_col.find_one({"email": email})["activated"]
        except:
            return False
    
    @classmethod
    def enqueue(cls, email):
        email_confirmation_job = queue.enqueue(ConfirmationModule.check_activated, args=(email,), job_id="email_confirmation", result_ttl=20)
