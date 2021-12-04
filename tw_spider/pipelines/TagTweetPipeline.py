from tw_spider.items import TagTweetItem
from tw_spider.base import Pipeline

class TagTweetPipeline(Pipeline):
    def __init__(self, db_connector):
        super(TagTweetPipeline, self).__init__(db_connector)
        
    def process_item(self, item, spider):
        #TODO: add comment
        if isinstance(item, TagTweetItem):
            self.db['tag_tweet'].update_one(
                {'id_': int(item['id_'])},
                {'$set': item['tag_tweet_info']},
                upsert=True
            )
        return item