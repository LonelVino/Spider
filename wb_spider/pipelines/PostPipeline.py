from wb_spider.base import Pipeline
from wb_spider.items import PostItem

class PostPipeline(Pipeline):
    def __init__(self, db_connector):
        super(PostPipeline, self).__init__(db_connector)
        
    def process_item(self, item, spider):
        #TODO: add comment
        if isinstance(item, PostItem):
            self.db['post'].update_one(
                {'id': int(item['post_info']['id'])},
                {'$set': item['post_info']},
                upsert=True
            )
        return item