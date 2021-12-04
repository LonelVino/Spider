# Spider

 ![](https://img.shields.io/badge/Scrapy-v2.4-blue) ![](https://img.shields.io/badge/Python-v3.8-orange) ![](https://img.shields.io/badge/Spider-Weibo-yellow)

A spider for news on **Twitter** and **Weibo**.


## Pre-Knowledge
[Some basic knowledge and the developement log](./development_log.md)

## How to start

### Operating environment

- Operating system: Common Linux distribution is feasible (my OS for development test is ubuntu 20.04) 
- `Python> = 3.6.0`
- `mongoDB> =4.2`
-  **Docker**, if you can, please keep the Docker version is the latest

###  Initialize

Clone and install the dependencies of python

```shell
git@github.com:LonelVino/Spider.git
cd Spider
pip install -r requirements.txt
```

**Initialize docker container:** 
The container is mounted from image `mongoDB`, used as a database of spider. 

1. **Create Weibo Spider**
```shell
sudo chmod 755 ./init/init_wb.sh
./init/init_wb.sh
```
2. **Create Twitter Spider**
```shell
sudo chmod 755 ./init/init_tw.sh
./init/init_tw.sh
```

`Init_*.sh` will create the necessary configurations and mapped directories for `mongoDB` in the docker container.  The data is stored in `Home/mongoDB`

**Initialize the database:**

Then，according to the hint of`init_*.sh`，we need to execute the following command to call the script `db_init_wb.js` or `db_init_tw.js`， which is used to initialize the database.

```shell
sudo docker exec -it wb_spider mongo 127.0.0.1:27018 /etc/resource/db_init_wb.js
sudo docker exec -it tw_spider mongo 127.0.0.1:27019 /etc/resource/db_init_tw.js
```

- When you create Weibo Spider: It will create 2 users respectively: `admin`(administrator) and `weibo`(usual user)，and 6 tables `user`,`user_post`, `tag_post`, `review` and `error_log`.
- When you create Twitter Spider: It will also create 2 users: `admin` and `twitter`, and 3 tables `user`, `tag_post`, `error_log`. 

> **NB**:  You will be asked to input your own password when you create the `admin` and `weibo` or `twitter`.


**Modify the params:**

1. When using Weibo Spider:

Rewrite `./wb_spider/database/DBconnector.py`，modify the `mongo_pwd` in function `__init__` to your own password，which is used for Spider to connect to the database。

```python
def __init__(self):
  self.mongo_uri = "127.0.0.1:27018" # IP used to connect with Docker.
  self.mongo_database = "weibo" # database created from init_db.js
  self.mongo_user_name = "weibo" # the user in database 'weibo'
  self.mongo_pass_wd = "Your password."
```

2. When using Twitter Spider:

Change the `USER_AGENT` in `TweetScraper/settings.py` to identify who you are
```
USER_AGENT = 'your website/e-mail' 
```
For example: `firefox/xxxxxx@gmail.com`

Rewrite `./tw_spider/database/DBconnector.py`，modify the `mongo_pwd` in function `__init__` to your own password，which is used for Spider to connect to the database。

```python
def __init__(self):
  self.mongo_uri = "127.0.0.1:27019" # IP used to connect with Docker.
  self.mongo_database = "twitter" # database created from init_db.js
  self.mongo_user_name = "twitter" # the user in database 'weibo'
  self.mongo_pass_wd = "Your password."
```

> ##### Some tips of Docker
>
> start or stop a docker container
>
> ```shell
> sudo docker container start [container name]
> sudo docker container stop [container name]
> sudo docker container ls
> ```
>
> Check the ip of a container
> 
> ```shell
> docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' [container_id or container_name]
> ```
>

### Start
0. **Select Spider**

You can use the SCRAPY_PROJECT environment variable in `scrapy.cfg` to specify a different project for scrapy to use. For example, we define `project2=tw_spider.settings` in `scrapy.cfg`, then we can change the project as Twitter Spider by using: 

```shell
export SCRAPY_PROJECT=project2
```
(Refer to [Commandline tool](https://docs.scrapy.org/en/latest/topics/commands.html))

By default, the scrapy command-line tool will use the default settings, e.g. `wb_spider`. 

> ##### some tips of `scrapy` command tool
> Usage:
>    scrapy <command> [options] [args]
> Available commands:
>   crawl:        Run a spider
>   settings:     Getting settings value
>   startprojet:  Creates a new Scrapy project


1. **Weibo**

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


2. **Twitter**
#### With ternimal command

|  Spider Name   |                    CMD                     |                           Function                           |
| :------------: | :----------------------------------------: | :----------------------------------------------------------: |
| `tag_post_spider`  | `scrapy crawl tag_post_spider -a query="#xxx,xxx"`  | Collect all the blog posts of the target hashtag, parameters `query` should be `#[keyword]` or `[keyword]`, such as `#shaanxi` or `shaanxi` (the whole command is `scrapy crawl tag_post_spider -a query="#shaanxi"`). |


### DataBase

You have kinds of ways to explore the database, such as [MongoDB Atlas](https://docs.atlas.mongodb.com/getting-started/), [MongoDB Compass](https://docs.mongodb.com/compass/current/), [MongoDB Server](https://docs.mongodb.com/manual/tutorial/getting-started/), etc., according to the [MongoDB documents](https://docs.mongodb.com/). Here, I used MongoDB Server and MongoDB Compass together.

#### MongoDB Server

You can refer to the [official tutorial](https://docs.mongodb.com/manual/tutorial/getting-started/), which is very comprehensive.

#### MongoDB Compass
Besides, I use [MongoDB Campass](https://docs.mongodb.com/compass/current/) to visualize the database, which is a powerful GUI for querying, aggregating, and analyzing the MongoDB data in a visual environment. The examples of Database are as follows:

![Tag Posts Database](./assets/img/tag_post_db.png)
![Reviews Database](./assets/img/review_db.png)


## overall idea

todo

## Structure

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