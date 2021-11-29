
from abc import ABC, abstractmethod


class BaseConfig(ABC):
    def __init__(self):
        self.url = "https://m.weibo.cn/"

    @abstractmethod
    def gen_url(self, *args, **kwargs):
        pass
