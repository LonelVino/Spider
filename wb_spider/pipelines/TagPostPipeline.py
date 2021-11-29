from wb_spider.base import Pipeline
from wb_spider.items import TagPostItem

class TagPostPipeline(Pipeline):
    def __init__(self, db_connector):
        super(TagPostPipeline, self).__init__(db_connector)
        
    def process_item(self, item, spider):
        #TODO: add comment
        if isinstance(item, TagPostItem):
            self.db['tag_post'].update_one(
                {'id': int(item['tag_post_info']['id'])},
                {'$set': item['tag_post_info']},
                upsert=True
            )
        return item