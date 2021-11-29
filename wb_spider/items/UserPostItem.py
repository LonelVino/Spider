
from scrapy import Item, Field


class UserPostItem(Item):
    '''
        User's Post Item
    '''
    user_post_info = Field()