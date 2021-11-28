
from scrapy import Item, Field


class UserItem(Item):
    """
    User Info Item
    """
    user_info = Field()
