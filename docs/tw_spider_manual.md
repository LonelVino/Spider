## Twitter Spider Manual

### Initialize 

**1. Initialize docker container:** 
The container is mounted from image `mongoDB_tw`, used as a database of spider. 

**2. Create Twitter Spider**
```shell
sudo chmod 755 ./init/init_tw.sh
./init/init_tw.sh
```

`init_tw.sh` will create the necessary configurations and mapped directories for `mongoDB_tw` in the docker container.  The data is stored in `Home/mongoDB_tw`


**3. Initialize the Twitter database:**

Then，according to the hint of`init_tw.sh`，we need to execute the following command to call the script `db_init_tw.js`， which is used to initialize the database.

```shell
sudo docker exec -it tw_spider mongo 127.0.0.1:27019 /etc/resource/db_init_tw.js
```

`db_init_tw.js` will create 2 users: `admin` and `twitter`, and 3 tables `user`, `tag_tweet`, `error_log`. 

> **NB**:  You will be asked to input your own password when you create the `admin` and `twitter`.


**4.Modify the params**

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
  self.mongo_user_name = "twitter" # the user in database 'twitter'
  self.mongo_pass_wd = "Your password."
```


### Start

#### With ternimal command

|  Spider Name   |                    CMD                     |                           Function                           |
| :------------: | :----------------------------------------: | :----------------------------------------------------------: |
| `tag_tweet_spider`  | `scrapy crawl tag_tweet_spider -a query="#xxx&verbar;xxx"`  | Collect all the blog posts of the target hashtag, parameters `query` should be `#[keyword]` or `[keyword]`, such as `#shaanxi` or `shaanxi` (the whole command is `scrapy crawl tag_tweet_spider -a query="#shaanxi"`). |




### File Tree Structure

📦tw_spider
 ┣ 📂base
 ┃ ┣ 📜BaseSpider.py
 ┃ ┣ 📜Pipeline.py
 ┃ ┗ 📜__init__.py
 ┣ 📂database
 ┃ ┣ 📜DBConnector.py
 ┃ ┗ 📜__init__.py
 ┣ 📂items
 ┃ ┣ 📜ErrorItem.py
 ┃ ┣ 📜TagTweetItem.py
 ┃ ┣ 📜UserItem.py
 ┃ ┗ 📜__init__.py
 ┣ 📂middleware
 ┃ ┗ 📜__init__.py
 ┣ 📂pipelines
 ┃ ┣ 📜ErrorPipeline.py
 ┃ ┣ 📜TagTweetPipeline.py
 ┃ ┣ 📜UserPipeline.py
 ┃ ┗ 📜__init__.py
 ┣ 📂spiders
 ┃ ┣ 📜__init__.py
 ┃ ┗ 📜tag_tweet_spider.py
 ┣ 📜settings.py
 ┗ 📜utlis.py