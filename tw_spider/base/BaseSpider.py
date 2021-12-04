
from abc import ABC
from scrapy.spiders import CrawlSpider
from tw_spider.items import ErrorItem


class BaseSpider(CrawlSpider, ABC):
    """
        Base Class for all spiders in this project. All the scrapy spiders must inherit this class and input the \
        parameter `query`. `Params` is a sting which contains several target user's id string and separated by `|`.

        This class also provides a static method named `get_params_list which` receives the string `params` and divides it
        into a list obj.

        The `parse_err` method is a general callback function to handle with the `IgnoreRequest` error.
    """

    allowed_domains = ['twitter.com']

    def __init__(self, params, *args, **kwargs):
        super(BaseSpider, self).__init__(*args, **kwargs)
        self.params = params
    
    @staticmethod
    def get_param_list(params: str) -> list:
        return list(filter(None, params.split('|')))

    def parse_err(self, response):
        item = ErrorItem()
        item['url'] = response.request.url
        yield item
