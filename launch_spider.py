from scrapy.cmdline import execute

topics = ['%2323岁交警泥浆中救出女子后轻拥安抚',
          '%23西安地铁涉事保安已停职',
          '%23交通运输部回应西安地铁事件',
          '%23西安地铁需要公开道歉',
          '%23西安地铁女乘客被拖离事件',
          '%23官方回应西安地铁保安拖拽女子事件',
          '%23西安地铁通报女子被保安拖拽下车',
          '%23西安地铁',
          '%23央视评西安通报引发舆论争议',
          '%23西安地铁通报女子被保安拖拽下车'] 

if __name__ == '__main__':
    base_cmd = "scrapy crawl tag_post_spider -a uid="
    for i in topics:
        spider_cmd = base_cmd + i
        execute(spider_cmd.split())