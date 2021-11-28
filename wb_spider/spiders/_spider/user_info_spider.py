
import json

from scrapy.http.request import Request
from wb_spider.base import BaseSpider
from wb_spider.config import UserConfig
from wb_spider.items import UserItem

#https://doc.scrapy.org/en/latest/topics/request-response.html?highlight=Request#scrapy.http.Request

class UserSpider(BaseSpider):
    name = 'user_spider'
    
    def __init__(self, uid:str, *args, **kwargs):
        super(UserSpider, self).__init__(uid, *args, **kwargs)
        self._u_generator = UserConfig()
        
    def start_requests(self):
        uid_list = self.get_uid_list(self.uid)
        for uid in uid_list:
            url = self._u_generator.gen_url(uid)
            yield Request(url=url, dont_filter=True, callback=self._parse_profile,\
                errback=self.parse_err, meta={'uid': uid})

    def _parse_profile(self, resp):
        item = UserItem()
        user_info = json.loads(resp.text)['data']['userinfo']
        item['user_info'] = user_info
        yield item
        
        
    

