from wb_spider.base import Pipeline
from wb_spider.items import LongtextItem

class LongtextPipeline(Pipeline):
    def __init__(self, *args, **kwargs):
        super(LongtextPipeline, self).__init__(*args, **kwargs)
        
    def process_item(self, item, spider):
        #TODO: add comment
        if isinstance(item, LongtextItem):
            self.db['longtext'].update_one(
                {'id': int(item['t_id'])},
                {'$set': dict(item)},
                upsert=True
            )
        return item