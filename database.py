from flask_pymongo import pymongo


# connect to mongodb atlas
mongo = pymongo.MongoClient(
    "mongodb+srv://canh:danielnguyennhc@cluster-art-gallery.yotsq.mongodb.net/gallery?retryWrites=true&w=majority")
db = pymongo.database.Database(mongo, 'gallery')

# create collection
user_col = pymongo.collection.Collection(db, 'user')
pic_col = pymongo.collection.Collection(db, 'picture')
comment_col = pymongo.collection.Collection(db, 'comment')
reply_col = pymongo.collection.Collection(db, 'reply')


class Database:
    def __init__(self):
        pass

    @classmethod
    def save_user_to_db(cls, data):
        try:
            user_col.insert_one(data)
            return True
        except:
            return False