from wb_spider.base import BaseConfig

# https://m.weibo.cn/api/container/getIndex?
# containerid=100103typetype%3D60%26&q%3D%23陕西   
# %26t%3D0&page_type=searchall
# &page=2
# NB: here %23陕西 -> #陕西, is the input parameter
class TagPostConfig(BaseConfig):
    def __init__(self):
        super(TagPostConfig, self).__init__()
        self.__api = {
            'api_0': 'api/container/getIndex?containerid=100103type%3D61%26q%3D',
            'api_1': '%26t%3D0&page_type=searchall',
            'api_2': '&page=',
            'longtext_api': 'statuses/extend?id='
        }
        
        
    def __call__(self, **kwargs):
        self.gen_url(**kwargs)
        
    def gen_url(self, **kwargs):
        assert ('uid' in kwargs.keys() and 'page' in kwargs.keys()) or 't_id' in kwargs.keys(), 'Input Arguments Error!'
        if 'page' in kwargs.keys():
            uid = str(kwargs['uid'])
            page = kwargs['page']
            url = self.url + self.__api['api_0'] + uid + self.__api['api_1']
            if page:
                url += self.__api['api_2'] + str(page)
            return url
        else:
            t_id = str(kwargs['t_id'])
            return self.url + self.__api['longtext_api'] + t_id
