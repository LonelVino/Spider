## Weibo Spider Manual

### Initialize 

**1. Initialize docker container:** 
The container is mounted from image `mongoDB_wb`, used as a database of spider. 

**2. Create Weibo Spider**
```shell
sudo chmod 755 ./init/init_wb.sh
./init/init_wb.sh
```

`init_wb.sh` will create the necessary configurations and mapped directories for `mongoDB_wb` in the docker container.  The data is stored in `Home/mongoDB_wb`


**3. Initialize the Weibo database:**

Then，according to the hint of`init_wb.sh`，we need to execute the following command to call the script `db_init_wb.js`， which is used to initialize the database.

```shell
sudo docker exec -it wb_spider mongo 127.0.0.1:27018 /etc/resource/db_init_wb.js
```

`db_init_wb.js` will create 2 users respectively: `admin`(administrator) and `weibo`(usual user)，and 6 tables `user`,`user_post`, `tag_post`, `review` and `error_log`.


> **NB**:  You will be asked to input your own password when you create the `admin` and `weibo`.


**4.Modify the params**

Rewrite `./wb_spider/database/DBconnector.py`，modify the `mongo_pwd` in function `__init__` to your own password，which is used for Spider to connect to the database。

```python
def __init__(self):
  self.mongo_uri = "127.0.0.1:27018" # IP used to connect with Docker.
  self.mongo_database = "weibo" # database created from init_db.js
  self.mongo_user_name = "weibo" # the user in database 'weibo'
  self.mongo_pass_wd = "Your password."
```

### Start

#### With terminal command

There are 4 spiders available now, and the corresponding commands are as follow:

|  Spider Name   |                    CMD                     |                           Function                           |
| :------------: | :----------------------------------------: | :----------------------------------------------------------: |
| `wb_spider` | `scrapy crawl wb_spider -a uid=xxx&verbar;xxx` | Collecting the target users’ information and all blog posts, which must be introduced `-a uid = xxx &verbar; xxx"` (the target collection user's `UID`) |
| `user_spider`  | `scrapy crawl user_spdier -a uid=xxx&verbar;xxx`  | Collect the target users’ information， parameters are the same as`weibo_spider`. |
| `user_post_spider`  | `scrapy crawl user_post_spider -a uid=xxx&verbar;xxx`  | Collect all the blog posts of the target users, parameters are the same as`wb_spider`. |
| `tag_post_spider`  | `scrapy crawl tag_post_spider -a uid=xxx&verbar;xxx`  | Collect all the blog posts of the target hashtag and reviews of each post, parameters `uid` should be `%23[keyword]`, such as `%23陕西` (the whole command is `scrapy crawl tag_post_spider -a uid="%23陕西"`). |

#### With Python Script

According to the [command line tool of scrapy](https://doc.scrapy.org/en/latest/topics/commands.html?highlight=scrapy%20crawl), we can execute `cmd` command with python to call the sprider:

```python
from scrapy.cmdline import execute

if __name__ == '__main__':
    spider_cmd = "scrapy crawl wb_spider -a uid=user1_id|user2_id|...."
    execute(spider_cmd.split())
    
```



### File Tree Structure

```
📦wb_spider
 ┣ 📂base
 ┃ ┣ 📜BaseConfig.py
 ┃ ┣ 📜BaseSpider.py
 ┃ ┣ 📜Pipeline.py
 ┃ ┗ 📜__init__.py
 ┣ 📂config
 ┃ ┣ 📜ReviewConfig.py
 ┃ ┣ 📜TagPostConfig.py
 ┃ ┣ 📜UserConfig.py
 ┃ ┣ 📜UserPostConfig.py
 ┃ ┗ 📜__init__.py
 ┣ 📂database
 ┃ ┣ 📜DBConnector.py
 ┃ ┗ 📜__init__.py
 ┣ 📂items
 ┃ ┣ 📜ErrorItem.py
 ┃ ┣ 📜LongtextItem.py
 ┃ ┣ 📜ReviewItem.py
 ┃ ┣ 📜TagPostItem.py
 ┃ ┣ 📜UserItem.py
 ┃ ┣ 📜UserPostItem.py
 ┃ ┗ 📜__init__.py
 ┣ 📂middlewares
 ┃ ┣ 📜DepthMiddleware.py
 ┃ ┣ 📜FakeUserAgentMiddleware.py
 ┃ ┣ 📜InitialMiddleware.py
 ┃ ┣ 📜ProxyMiddleware.py
 ┃ ┣ 📜RetryMiddleware.py
 ┃ ┗ 📜__init__.py
 ┣ 📂pipelines
 ┃ ┣ 📜ErrorPipeline.py
 ┃ ┣ 📜LongtextPipeline.py
 ┃ ┣ 📜ReviewPipeline.py
 ┃ ┣ 📜TagPostPipeline.py
 ┃ ┣ 📜UserPipeline.py
 ┃ ┣ 📜UserPostPipeline.py
 ┃ ┗ 📜__init__.py
 ┣ 📂resource
 ┃ ┗ 📜0.1.11.json
 ┣ 📂spiders
 ┃ ┣ 📂_spider
 ┃ ┃ ┣ 📜__init__.py
 ┃ ┃ ┣ 📜tag_post_spider.py
 ┃ ┃ ┣ 📜user_info_spider.py
 ┃ ┃ ┗ 📜user_post_spider.py
 ┃ ┣ 📜__init__.py
 ┃ ┗ 📜wb_spider.py
 ┣ 📜__init__.py
 ┗ 📜settings.py
```