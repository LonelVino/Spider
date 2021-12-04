import os
from fake_useragent import UserAgent
from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware


class FakeUserAgentMiddleware(UserAgentMiddleware):
    def __init__(self, ua):
        super(UserAgentMiddleware, self).__init__()
        self.ua = ua

    @classmethod   #  returns a class method for the given function, return a UserAgent in the resourse folder
    def from_crawler(cls, crawler):
        path = f'{os.path.dirname(os.path.dirname(__file__))}/middlewares/resource/0.1.11.json'
        ua = UserAgent(path=path)
        s = cls(ua=ua) 
        # Always use self for the first argument to instance methods.
        # Always use cls for the first argument to class methods.
        return s

    def process_request(self, request, spider):
        request.headers['User-agent'] = self.ua.random
        return None
