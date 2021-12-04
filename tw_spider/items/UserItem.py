from scrapy import Item, Field


class UserItem(Item):
    id_ = Field()
    user_info = Field()
