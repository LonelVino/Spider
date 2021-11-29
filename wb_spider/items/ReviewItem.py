from scrapy import Item, Field

class ReviewItem(Item):
    '''
        Hash Tag Post Item    
    '''
    pid = Field()
    review_info = Field()