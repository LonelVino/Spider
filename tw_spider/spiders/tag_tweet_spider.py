import re, json
from urllib.parse import quote

from scrapy import http
from logging import log, INFO, WARNING
from scrapy.core.downloader.middleware import DownloaderMiddlewareManager
from scrapy_selenium import SeleniumRequest, SeleniumMiddleware
from tw_spider.base import BaseSpider

from tw_spider.items import TagTweetItem, UserItem


class TagTweetSpider(BaseSpider):
    name = 'tag_tweet_spider'
    
    def __init__(self, query:str, *args, **kwargs):
        super(TagTweetSpider, self).__init__(query, *args, **kwargs)
        self.url = (
            f'https://api.twitter.com/2/search/adaptive.json?'
            f'include_profile_interstitial_type=1'
            f'&include_blocking=1'
            f'&include_blocked_by=1'
            f'&include_followed_by=1'
            f'&include_want_retweets=1'
            f'&include_mute_edge=1'
            f'&include_can_dm=1'
            f'&include_can_media_tag=1'
            f'&skip_status=1'
            f'&cards_platform=Web-12'
            f'&include_cards=1'
            f'&include_ext_alt_text=true'
            f'&include_quote_count=true'
            f'&include_reply_count=1'
            f'&tweet_mode=extended'
            f'&include_entities=true'
            f'&include_user_entities=true'
            f'&include_ext_media_color=true'
            f'&include_ext_media_availability=true'
            f'&send_error_codes=true'
            f'&simple_quoted_tweet=true'
            f'&query_source=typed_query'
            f'&pc=1'
            f'&spelling_corrections=1'
            f'&ext=mediaStats%2ChighlightedLabel'
            f'&count=20'
            f'&tweet_search_mode=live'
        )
        self.url = self.url + '&q={query}'
        self.query = query
        self.query_list = self.get_param_list(self.query)
        self.num_search_issued = 0
        # regex for finding next cursor
        self.cursor_re = re.compile('"(scroll:[^"]*)"')
        # ^: Matches the start of the string;
        # []:Used to indicate a set of characters, Special characters lose their special meaning inside sets.
        # *: match char left to it, as many repetitions as possible, such as ab* match 'a', 'ab',  or ‘a’ followed by any number of ‘b’s.
        # cursor example -- scroll:thGAVUV0VFVBYBFoDM18LDsYzWKBIYlAISY8LrAAAB9D-AYk3S8an8AAAAIBRRROiJVxAEFFVvaVqUcAcUWdKxaRZQDxRamOlBFFABFFJSEyHVgAASUvbajRfQARRXHywJl9AIFFX0HiGUYAMUSMoxmZZQABRZc8V6FUAAFFvNK9-XwAQUVm3JJRewAxRVhVGsFXABFFl6PpfVQAMUUTVYJpRwHhRSJRV1FmAJFFFpknUUYAYUVfPZJNWABBRIyS3-18ABFFl7LAhUUAEUWXZdldWAAhRatMYzVzAEFFGq50vUUAAUVeAoOpcwABRWctId17AHFFbY5vNXsAMUUmtXLFVwARRYF96x1kADFFqQoIAVgAoUUp4qrlfAChRRJOmR1UAaFFE0kD5WUAJhFYCEehWAiXoYB0RFRkFVTFQ1QBUCFQAA


    def start_requests(self):
        """
        Use the landing page to get cookies first
        
        `SeleniumRequest()`: The request will be handled by selenium, 
            with an additional "meta" key, named "driver" containing the selenium driver with the request processed.
        """
        print('Press Control+C to interrupt the Scraper.')
        print('Or Press Control+Z to put the Scraper in the background, suspended.')
        yield SeleniumRequest(url="https://twitter.com/explore", callback=self.parse_home_page)


    def parse_home_page(self, response):
        """
        Use the landing page to get cookies first, and then run requests
        """
        self.update_cookies(response)
        for r in self.start_query_request():
            yield r


    
    def start_query_request(self, cursor=None):
        """
        Generate the search request
        """
        for query in self.query_list:
            if cursor:
                url = self.url + '&cursor={cursor}'
                url = url.format(query=quote(query), cursor=quote(cursor))
            else:
                url = self.url.format(query=quote(query))
            request = http.Request(url, callback=self.parse_result_page, cookies=self.cookies, headers=self.headers)
            yield request

            self.num_search_issued += 1
            if self.num_search_issued % 100 == 0:
                # get new SeleniumMiddleware       
                for m in self.crawler.engine.downloader.middleware.middlewares:
                    if isinstance(m, SeleniumMiddleware):
                        m.spider_closed()  # spider.close() is the native function of Spider
                self.crawler.engine.downloader.middleware = DownloaderMiddlewareManager.from_crawler(self.crawler)
                # update cookies
                yield SeleniumRequest(url="https://twitter.com/explore", callback=self.update_cookies, dont_filter=True)



    def parse_result_page(self, response):
        """
        Get the tweets & users & next request
        """
        # inspect_response(response, self)

        # handle current page
        data = json.loads(response.text)
        for item in self.parse_tweet_item(data['globalObjects']['tweets']):
            yield item
        for item in self.parse_user_item(data['globalObjects']['users']):
            yield item

        # get next page
        cursor = self.cursor_re.search(response.text).group(1)
        for r in self.start_query_request(cursor=cursor):
            yield r


    def parse_tweet_item(self, items):
        for k,v in items.items():
            tweet = TagTweetItem()
            tweet['id_'] = k
            tweet['tag_tweet_info'] = v
            yield tweet


    def parse_user_item(self, items):
        for k,v in items.items():
            user = UserItem()
            user['id_'] = k
            user['user_info'] = v
            yield user


    def update_cookies(self, response):
        '''
        Update the cookies by driver.get_cookies() 
        
        driver.get_cookies(): Returns a set of dictionaries, corresponding to cookies visible in the current session.
        (refer to https://selenium-python.readthedocs.io/api.html#module-selenium.webdriver.remote.webdriver)
        '''
        driver = response.meta['driver']
        try:
            self.cookies = driver.get_cookies()
            self.x_guest_token = driver.get_cookie('gt')['value']
            # self.x_csrf_token = driver.get_cookie('ct0')['value']
        except:
            log(msg='cookies are not updated!', level=WARNING)

        self.headers = {
            'authorization': 'Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA',
            'x-guest-token': self.x_guest_token,
            # 'x-csrf-token': self.x_csrf_token,
        }
        msg = f'headers:\n--------------------------\n'\
            f'{self.headers}'\
            f'\n--------------------------\n'
        log(msg=msg, level=INFO)
            
