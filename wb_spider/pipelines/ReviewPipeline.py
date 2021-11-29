from wb_spider.base import Pipeline
from wb_spider.items import ReviewItem

class ReviewPipeline(Pipeline):
    def __init__(self, db_connector):
        super(ReviewPipeline, self).__init__(db_connector)
        
    def process_item(self, item, spider):
        #TODO: add comment
        if isinstance(item, ReviewItem):
            self.db['review'].update_one(
                {'id': int(item['review_info']['id'])},
                {'$set': item['review_info']},
                upsert=True
            )
        return item