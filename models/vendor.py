from models.user import UserModule
from config import pusher

from database import user_col


class VendorModule(UserModule):
    def __init__(self, id='', username='', raw_password='', password='', activated=False, avatarURL='', email='', role='user', tel='', dateOfBirth='', admin_confirmation='', **kwargs):
        super().__init__(id=id, username=username, raw_password=raw_password, password=password,
                         activated=activated, avatarURL=avatarURL, email=email, role=role, **kwargs)

        self.admin_confirmation = admin_confirmation
        self.tel = tel
        self.dateOfBirth = dateOfBirth

    def vendor_approval(self):
        update = user_col.update_one({"id": self.id}, {
            "$set": {"status": "approved"}})

        return update if update else None

    @classmethod
    def save_to_database(cls, vendor, data):
        super().save_to_database(vendor)
        pusher.trigger("vendor_register", "registration", data)

    @classmethod
    def filter_by_status(cls, status):
        account_collection = user_col.find({"status": status})
        return account_collection if account_collection else None
