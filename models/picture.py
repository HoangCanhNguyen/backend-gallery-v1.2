from database import pic_col
from schemas.picture import PictureSchema
from config import pusher


class PictureModule:
    def __init__(self, id='', title='', creator_name='', artist='', category='', price='', imageURL='', description='', status='in stock', admin_confirmation=False, created_at='', **kwargs):
        self.id = id
        self.title = title
        self.creator_name = creator_name
        self.artist = artist
        self.category = category
        self.price = price
        self.imageURL = imageURL
        self.description = description
        self.status = status
        self.admin_confirmation = admin_confirmation
        self.created_at = created_at

    def find_by_title(self):
        pic = pic_col.find_one({"title": self.title})
        return pic if pic else None

    def find_by_id(self):
        pic = pic_col.find_one({"id": self.id})
        return pic if pic else None

    @property
    def get_maxium_pics(self):
        return pic_col.find().count() + 1

    def update_picture_to_db(self, data, role):
        pic = self.find_by_id()
        if pic["creator_name"] == data["creator_name"] or role == 'admin':
            pic_col.update_one({"id": data["id"]}, {
                "$set": {
                    "title": data["title"],
                    "status": data["status"],
                    "price": data["price"],
                    "category": data["category"],
                    "admin_confirmation": data["admin_confirmation"],
                    "artist": data["artist"],
                    "imageURL": data["imageURL"],
                    "description": data["description"]
                }
            })
            return True
        else:
            return False

    @classmethod
    def save_pic_to_db(cls, pic, data):
        pic_col.insert_one(pic)
        pusher.trigger("picture", "creation", data)

    @classmethod
    def get_all_pics(cls):
        pics = pic_col.find()
        return pics
