from wb_spider.base import Pipeline
from wb_spider.items import ErrorItem

class ErrorPipeline(Pipeline):
    def __init__(self, db_connector):
        super(ErrorPipeline, self).__init__(db_connector)
        
    def process_item(self, item, spider):
        #TODO: add comment
        if isinstance(item, ErrorItem):
            self.db['error_log'].insert_one(dict(item))
        return item