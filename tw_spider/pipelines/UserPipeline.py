from tw_spider.base import Pipeline
from tw_spider.items import UserItem

class UserPipeline(Pipeline):
    def __init__(self, db_connector):
        super(UserPipeline, self).__init__(db_connector)
        
    def process_item(self, item, spider):
        #TODO: add comment
        if isinstance(item, UserItem):
            self.db['user'].update_one(
                {'id_': int(item['id_'])},
                {'$set': item['user_info']},
                upsert=True
            )
        return item