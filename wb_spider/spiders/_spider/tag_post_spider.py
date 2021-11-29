import json
from scrapy.http.request import Request

from wb_spider.base import BaseSpider
from wb_spider.config import TagPostConfig
from wb_spider.config import ReviewConfig
from wb_spider.items import TagPostItem
from wb_spider.items import ReviewItem
from wb_spider.items.LongtextItem import LongtextItem


class TagPostSpider(BaseSpider):
    name = 'tag_post_spider'
    
    def __init__(self, uid:str, *args, **kwargs):
        super(TagPostSpider, self).__init__(uid, *args, **kwargs)
        self._tp_generator = TagPostConfig()
        self._rw_generator = ReviewConfig()
        
    def start_requests(self):
        uid_list = self.get_uid_list(self.uid)
        for uid in uid_list:
            url = self._tp_generator.gen_url(uid=uid, page=None)
            print(url)
            yield Request(url=url, dont_filter=True, callback=self._parse_post,\
                errback=self.parse_err, meta={'uid': uid, 'last_page': 0})
            
    def _parse_post(self, resp, **kwargs):
        info = json.loads(resp.text)
        data = info['data']
        page = data['cardlistInfo']['page']
        uid = resp.meta['uid']
        last_page = resp.meta['last_page']
        
        if page is not None and int(page) != last_page:
            url = self._tp_generator.gen_url(uid=uid, page=page)
            yield Request(url=url, dont_filter=True, callback=self._parse_post, errback=self.parse_err, meta={'uid': uid, 'last_page': int(page)})
            
        # store each post
        for card in data['cards']:
            item = TagPostItem()
            card['mblog']['uid'] = uid
            item['tag_post_info'] = card['mblog']
            
            # store each review
            pid, mid = card['mblog']['id'], card['mblog']['mid']
            rw_url = self._rw_generator.gen_url(pid=pid, mid=mid, page=0)
            yield Request(url=rw_url, dont_filter=True, callback=self._parse_review, errback=self.parse_err, meta={'pid': pid, 'mid': mid, 'last_page': 0})
            
            # store the long text
            if card['mblog']['isLongText']:
                t_id = card['mblog']['id']
                url = self._tp_generator.gen_url(t_id=t_id)
                longtext_req = Request(
                    url=url, dont_filter=True, errback=self.parse_err,
                    callback=self._parse_longtext, meta={'uid': uid, 't_id': t_id}
                )
                yield longtext_req
            yield item
    
    
    def _parse_review(self, resp, **kwargs):
        response = json.loads(resp.text)        
        if response['ok']:
            reviews = response['data']['data']
            for review in reviews:
                item = ReviewItem()
                item['pid'] = resp.meta['pid']
                review['pid'] = resp.meta['pid']
                item['review_info'] = review
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