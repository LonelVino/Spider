# settings for selenium
from shutil import which
SELENIUM_DRIVER_NAME = 'firefox'
SELENIUM_BROWSER_EXECUTABLE_PATH = which('firefox')
SELENIUM_DRIVER_EXECUTABLE_PATH = which('geckodriver')
SELENIUM_DRIVER_ARGUMENTS=['-headless']  # '--headless' if using chrome instead of firefox

# !!! # Crawl responsibly by identifying yourself (and your website/e-mail) on the user-agent
USER_AGENT = 'firefox/lonelvino@gmail.com'

# =============================  Regular Settings ============================= 

# settings for spiders
BOT_NAME = 'tw_spider'

SPIDER_MODULES = ['tw_spider.spiders']
NEWSPIDER_MODULE = 'tw_spider.spiders'

LOG_LEVEL = 'INFO'
LOG_FILE = 'tw_spider.log'

DOWNLOAD_DELAY = 1.0


ITEM_PIPELINES = {
    'tw_spider.pipelines.UserPipeline': 100,
    'tw_spider.pipelines.TagTweetPipeline': 150, 
    'tw_spider.pipelines.ErrorPipeline': 250
}

# The downloader middleware is a framework of hooks into Scrapy’s request/response processing
DOWNLOADER_MIDDLEWARES = {
    'tw_spider.middleware.InitialMiddleware': 50,
    'tw_spider.middleware.FakeUserAgentMiddleware': 100,
    'tw_spider.middleware.ProxyMiddleware': None,  # 150
    'tw_spider.middleware.RetryMiddleware': None,  # 250
    'scrapy_selenium.SeleniumMiddleware': 800
}

# To get proxy, each proxy form like "https://xxx.xxx.xxx:xxxx/"
PROXY_URL = ''
