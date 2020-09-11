from models.user import UserModule
from config import pusher

class VendorModule(UserModule):
    def __init__(self, id='', username='', raw_password='', password='', activated=False, avatarURL='', email='', role='user',tel='', dateOfBirth='',admin_confirmation='', **kwargs):
        super().__init__(id=id, username=username, raw_password=raw_password, password=password, activated=activated, avatarURL=avatarURL, email=email, role=role, **kwargs)

        self.admin_confirmation = admin_confirmation
        self.tel = tel
        self.dateOfBirth = dateOfBirth

    @classmethod
    def save_to_database(cls, vendor,data):
        super().save_to_database(vendor)
        pusher.trigger("vendor_register","registration", data)