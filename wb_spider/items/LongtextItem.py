from scrapy import Item, Field


class LongtextItem(Item):
    longtext = Field()
    uid = Field()  # unique identifier
    t_id = Field() # time identifier
