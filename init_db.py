from WeiboSpider.database import DBConnector

db_connector = DBConnector()
db, client = db_connector.connect()
print('Database connected! URL: ', db_connector.mongo_uri)