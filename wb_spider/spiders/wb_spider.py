from ._spider.user_info_spider import UserSpider
from ._spider.post_spider import PostSpider
from scrapy import Request

class wb_spider(UserSpider, PostSpider):
    name = 'wb_spider'

    def init(self, uid, *args, **kwargs):
        super(wb_spider, self).__init__()
        
    def start_requests(self):
        uid_list = self.get_uid_list(self.uid)
        for uid in uid_list:
            u_url = self._u_generator.gen_url(uid)
            yield Request(
                url=u_url, dont_filter=True, callback=self._parse_profile, errback=self.parse_err, meta={'uid': uid}
            )
            p_url = self._p_generator.gen_url(uid=uid, page=None)
            yield Request(
                url=p_url, dont_filter=True, callback=self._parse_post, errback=self.parse_err, meta={'uid': uid, 'last_page': 0}
            )
        