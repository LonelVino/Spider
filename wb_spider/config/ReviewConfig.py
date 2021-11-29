from wb_spider.base import BaseConfig

# https://m.weibo.cn/comments/hotflow?id=4708523898569807
# &mid=4708523898569807
# &max_id_type=0
class ReviewConfig(BaseConfig):
    def __init__(self):
        super(ReviewConfig, self).__init__()
        self.__api = {
            'api_0': 'comments/hotflow?id=',
            'api_1': '&mid=',
            'api_2': '&max_id_type=',
            'longtext_api': 'statuses/extend?id='
        }
        
        
    def __call__(self, **kwargs):
        self.gen_url(**kwargs)
        
    def gen_url(self, **kwargs):
        assert 'pid' in kwargs.keys() and 'mid' in kwargs.keys() and 'page' in kwargs.keys(), 'Input Arguments Error!'
        pid = str(kwargs['pid'])
        mid = str(kwargs['mid'])
        page = str(kwargs['page'])
        url = self.url + self.__api['api_0'] + pid + self.__api['api_1'] + mid + self.__api['api_2'] + page
        return url