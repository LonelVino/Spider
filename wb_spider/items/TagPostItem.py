from scrapy import Item, Field

class TagPostItem(Item):
    '''
        Hash Tag Post Item    
    '''
    tag_post_info = Field()