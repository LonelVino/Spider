from abc import abstractmethod, ABC
from wb_spider.database import DBConnector

'''
abc - Abstract Base Classes
Provide the infrastructure for defining abstract base classes (ABCs) in Python
Abstract class: provide a common definition of a base class that multiple derived classes can share
'''

#TODO:comment each function according to scrapy

class Pipeline(ABC):
    def __init__(self, db_connector):
        self.connector = db_connector

    @classmethod
    def from_crawler(cls, crawler):
        return cls(db_connector=DBConnector())

    def open_spider(self, spider):
        self.db, self.client = self.connector.connect()

    def close_spider(self, spider):
        self.client.close()

    @abstractmethod
    def process_item(self, item, spider):
        pass
