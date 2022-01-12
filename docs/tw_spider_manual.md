# Twitter Spider Manual

## Initialize

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

Change the `USER_AGENT` in `tw_spider/settings.py` to identify who you are
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

## Start

#### Start Docker

If you initialize the spider as the instruction above, then you can skip the guide about how to start docker.

If you initialize your spider before and wanna use it directly, following the next command. (If it has been a long time that your forget the name of your spider container, use `docker ls` to check the name of the container you wanna use)  

```bash
docker start wb_spider  # start your spider container, here wb_spider is the name of container
docker exec -it wb_spider /bin/bash # enter the bash commandline mode of your spider container 
```

#### Start and Connect to Mongodb

After you enter into the bash of your spider container, you can run the command below to start the mongo database service:

```
mongo [IP address] # start mongo service, for example: mongo 127.0.0.1:27018
```

Then specify the database you want to use, and authenticate with your username and password which are created when initializing the spider.

```
use weibo # use the database 'weibo'
db.auth('weibo', '123456')  # db.auth( <username>, <password> )
```

Congratulation, you connect to your database successfully ! Now you can check and modify the data your crawled from the website. There are some common mongodb shell commands:

```
show dbs # display the database
show collections  # show the data tables & collections

db.createCollection(name) # create a collection
db.COLLECTION_NAME.drop();  # drop a collection
db.COLLECTION_NAME.find(condition)  # query in a collection
db.colloction.remove(CONDITION)  # delete document
```

 More commands of mongodb shell, please refer to [mongo tutorial](https://tecadmin.net/tutorial/mongodb/mongodb-tutorials/) .

### Start Spider

#### With ternimal command

|  Spider Name   |                    CMD                     |                           Function                           |
| :------------: | :----------------------------------------: | :----------------------------------------------------------: |
| `tag_tweet_spider`  | `scrapy crawl tag_tweet_spider -a query=#xxx&verbar;xxx`  | Collect all the blog posts of the target hashtag, parameters `query` should be `#[keyword]` or `[keyword]`, such as `#shaanxi` or `shaanxi` (the whole command is `scrapy crawl tag_tweet_spider -a query=#shaanxi`). |




## File Tree Structure
```
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
```