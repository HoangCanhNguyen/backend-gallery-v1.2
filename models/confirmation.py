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
        if user["activated"]:
            return {"msg": " TÀI KHOẢN ĐÃ ĐƯỢC KÍCH HOẠT"}, 200
        else:
            user_col.update_one({"email": email}, {
                                "$set": {"activated": True}})
            return {"msg": "TÀI KHOẢN KÍCH HOẠT THÀNH CÔNG"}