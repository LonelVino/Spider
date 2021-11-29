from wb_spider.base import BaseConfig


# base_url + api/container/getIndex?type=__uid&value=[uid] + &containerid=107603[uid] + &page=2
class UserConfig(BaseConfig):
    def __init__(self):
        super(UserConfig, self).__init__()
        self.__api = {
            'api_0': 'api/container/getIndex?type=__uid&value=',
            'api_1': '&containerid=100505',
        }
        
    def __call__(self, uid):
        return self.gen_url(uid)
    
    def gen_url(self, uid):
        return self.url + self.__api['api_0'] + uid + self.__api['api_1'] + uid