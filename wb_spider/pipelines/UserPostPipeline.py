from wb_spider.base import Pipeline
from wb_spider.items import UserPostItem

class UserPostPipeline(Pipeline):
    def __init__(self, db_connector):
        super(UserPostPipeline, self).__init__(db_connector)
        
    def process_item(self, item, spider):
        #TODO: add comment
        if isinstance(item, UserPostItem):
            self.db['user_post'].update_one(
                {'id': int(item['user_post_info']['id'])},
                {'$set': item['user_post_info']},
                upsert=True
            )
        return item