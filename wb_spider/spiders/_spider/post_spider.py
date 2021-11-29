
import json

from scrapy.http.request import Request
from wb_spider.base import BaseSpider
from wb_spider.config import PostConfig
from wb_spider.items import PostItem
from wb_spider.items.LongtextItem import LongtextItem

#https://doc.scrapy.org/en/latest/topics/request-resp.html?highlight=Request#scrapy.http.Request

#TODO: check the request and resp again

class PostSpider(BaseSpider):
    name = 'post_spider'
    
    def __init__(self, uid:str, *args, **kwargs):
        super(PostSpider, self).__init__(uid, *args, **kwargs)
        self._p_generator = PostConfig()
        
    def start_requests(self):
        uid_list = self.get_uid_list(self.uid)
        for uid in uid_list:
            url = self._p_generator.gen_url(uid)
            yield Request(url=url, dont_filter=True, callback=self._parse_post,\
                errback=self.parse_err, meta={'uid': uid, 'last_page': 0})

    def _parse_post(self, resp, **kwargs):
        """
            Parse crawled json str and tweet_spider iteratively generate new Request obj.
        """

        weibo_info = json.loads(resp.text)
        data = weibo_info['data']
        page = data['cardlistInfo']['page']
        uid = resp.meta['uid']
        last_page = resp.meta['last_page']

        if page is not None and int(page) != last_page:
            url = self._p_generator.gen_url(uid=uid, page=page)
            yield Request(url=url, dont_filter=True, callback=self._parse_post, errback=self.parse_err, meta={'uid': uid, 'last_page': int(page)})

        for card in data['cards']:
            item = PostItem()
            card['mblog']['uid'] = uid
            item['post_info'] = card['mblog']
            if card['mblog']['isLongText']:
                t_id = card['mblog']['id']
                url = self._p_generator.gen_url(t_id=t_id)
                longtext_req = Request(
                    url=url, dont_filter=True, errback=self.parse_err,
                    callback=self._parse_longtext, meta={'uid': uid, 't_id': t_id}
                )
                yield longtext_req
            yield item

    def _parse_longtext(self, resp, **kwargs):
        long_text = json.loads(resp.text)
        item = LongtextItem()
        item['uid'] = resp.meta['uid']
        item['t_id'] = resp.meta['t_id']
        item['longtext'] = long_text['data']['longTextContent']
        yield item

    def parse(self, resp, **kwargs):
        """
            Compulsorily implemented due to abstract method.
        """
        pass
