from scrapy import Item, Field


class TagTweetItem(Item):
    id_ = Field()
    tag_tweet_info = Field()