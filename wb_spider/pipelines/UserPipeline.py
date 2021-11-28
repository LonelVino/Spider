from wb_spider.base import Pipeline
from wb_spider.items import UserItem

class UserPipeline(Pipeline):
    def __init__(self, db_connector):
        super(UserPipeline, self).__init__(db_connector)
        
    def process_item(self, item, spider):
        #TODO: add comment
        if isinstance(item, UserItem):
            self.db['user'].update_one(
                {'uid': int(item['user_info']['id'])},
                {'$set': item['user_info']},
                upsert=True
            )
        return item