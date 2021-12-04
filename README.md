# Spider

 ![](https://img.shields.io/badge/Scrapy-v2.4-blue) ![](https://img.shields.io/badge/Python-v3.8-orange) ![](https://img.shields.io/badge/Spider-Weibo-yellow)

A spider for news on **Twitter** and **Weibo**.


## Pre-Knowledge
[Some basic knowledge and the developement log](./docs/development_log.md)

---
## How to start

### Operating environment

- Operating system: Common Linux distribution is feasible (my OS for development test is ubuntu 20.04) 
- `Python> = 3.6.0`
- `mongoDB> =4.2`
-  **Docker**, if you can, please keep the Docker version is the latest

###  Clone and install dependencies

Clone and install the dependencies of python

```shell
git@github.com:LonelVino/Spider.git
cd Spider
pip install -r requirements.txt
```

### Select Spider

You can use the SCRAPY_PROJECT environment variable in `scrapy.cfg` to specify a different project for scrapy to use. For example, we define `project2=tw_spider.settings` in `scrapy.cfg`, then we can change the project as Twitter Spider by using: 

```shell
export SCRAPY_PROJECT=project2
```
(Refer to [Command line tool](https://docs.scrapy.org/en/latest/topics/commands.html))

By default, the scrapy command-line tool will use the default settings, e.g. `wb_spider`. 

> ### some tips of `scrapy` command tool
>```shell
> Usage:
>   scrapy <command> [options] [args]
> Available commands:
>   crawl:        Run a spider
>   settings:     Getting settings value
>   startprojet:  Creates a new Scrapy project
>```

### **Initialize and Start Spider**


- [Weibo Spider Manual](./docs/wb_spider_manual.md)
- [Twitter Spider Manual](./docs/tw_spider_manual.md)

--- 

## DataBase

You have kinds of ways to explore the database, such as [MongoDB Atlas](https://docs.atlas.mongodb.com/getting-started/), [MongoDB Compass](https://docs.mongodb.com/compass/current/), [MongoDB Server](https://docs.mongodb.com/manual/tutorial/getting-started/), etc., according to the [MongoDB documents](https://docs.mongodb.com/). Here, I used MongoDB Server and MongoDB Compass together.

#### MongoDB Server

You can refer to the [official tutorial](https://docs.mongodb.com/manual/tutorial/getting-started/), which is very comprehensive.

#### MongoDB Compass
Besides, I use [MongoDB Campass](https://docs.mongodb.com/compass/current/) to visualize the database, which is a powerful GUI for querying, aggregating, and analyzing the MongoDB data in a visual environment. The examples of Database are as follows:

![Tag Posts Database](./assets/img/tag_post_db.png)
![Reviews Database](./assets/img/review_db.png)


## Appendix

> ### Some tips of Docker
>
> start or stop a docker container
>
> ```docker
> sudo docker container start [container name]
> sudo docker container stop [container name]
> sudo docker container ls
> ```
>
> Check the ip of a container
> 
> ```docker
> docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' [container_id or container_name]
> ```
>

