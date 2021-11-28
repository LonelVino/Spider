from scrapy.cmdline import execute


if __name__ == '__main__':
    spider_cmd = "scrapy crawl weibo_spider -a uid=1915671961"
    execute(spider_cmd.split())