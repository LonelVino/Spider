
from scrapy import Item, Field


class PostItem(Item):
    '''
        Post Item
    '''
    post_info = Field()