
import pymongo

#TODO: save the url, db, usr, pwd in a ENV file. 
class DBConnector:
    def __init__(self):
        self.mongo_url = "127.0.0.1"
        self.mongo_db = "weibo"
        self.mongo_usr = "weibo"
        self.mongo_pwd= "123456"

    def connect(self):
        client = pymongo.MongoClient(self.mongo_url)
        db = client[self.mongo_db]
        db.authenticate(self.mongo_usr, self.mongo_pwd)
        return db, client
