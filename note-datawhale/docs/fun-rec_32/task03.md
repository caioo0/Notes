# Task03:离线物料系统的构建
---

> （本学习笔记来源于DataWhale-12月组队学习：[推荐系统实战](https://github.com/datawhalechina/fun-rec)） 

**离线物料系统模块**

- 爬取新浪新闻：采用爬虫工具`scrapy`，每天1点爬取前一天的新浪新闻内容存储到`mongodb.SinaNews`数据库中；
- 物料画像构建：更新新闻动态画像，1.将用户上一天新闻交互信息（阅读、点赞、收藏）等信息存入`redis`；2.对物料画像处理，将新闻静态和动态数据分别存入对应的`redis`中；
- 用户画像构建：用户表`register_user`,用户阅读表`user_red`,用户点赞表`user_likes`,用户收藏表`user_collections`，用户画像构建就是将当天新的用户信息和所有用户的交互行为数据构造用户画像融合到`mongodb.UserProtrai`集合中;
- 画像自动化构建：`crontab`定时任务，将上面构建动作设为定时自动化处理；

## scrapy新闻爬取


- 初始化项目: `scrapy startproject sinanews`  , [详细参见](https://doc.scrapy.org/en/latest/intro/tutorial.html)

```bash
└─sinanews
    │  scrapy.cfg               - 项目配置文件
    │
    └─sinanews                  - 项目python模块
        │  items.py             - 用户定义类对象
        │  middlewares.py       - 中间件,用于配置请求头,代理,cookie,会话维持等;
        │  pipelines.py         - 管道文件,用于将爬取的数据进行持久化存储
        │  settings.py          - 配置文件,用于配置数据库
        │  __init__.py          - 模块初始化文件
        │
        └─spiders
                __init__.py     -放置spider的目录，爬虫的具体逻辑就是在这里实现的（具体逻辑写在spider.py文件中）,可以使用命令行创建spider，也可以直接在这个文件夹中创建spider相关的py文件

```
- scrapy运行周期

1. 通过`scrapy.Request(url,callback)`方法爬取网址,返回数据,`callback`可指定回调函数;
2. 在回调函数,解析响应(网页内容)并返回[`item.objects`](https://www.osgeo.cn/scrapy/topics/items.html#topics-items),最后实现本地存储;

新浪新闻 (spider)抓取代码实现:

```python
# -*- coding: utf-8 -*-
import re
import json
import random
import scrapy
from scrapy import Request
from ..items import SinanewsItem
from datetime import datetime


class SinaSpider(scrapy.Spider):
    # spider的名字
    name = 'sina_spider'

    def __init__(self, pages=None):
        super(SinaSpider).__init__()

        self.total_pages = int(pages)
        # base_url 对应的是新浪新闻的简洁版页面，方便爬虫，并且不同类别的新闻也很好区分
        self.base_url = 'https://feed.mix.sina.com.cn/api/roll/get?pageid=153&lid={}&k=&num=50&page={}&r={}'
        # lid和分类映射字典
        self.cate_dict = {
            "2510":  "国内",
            "2511":  "国际",
            "2669":  "社会",
            "2512":  "体育",
            "2513":  "娱乐",
            "2514":  "军事",
            "2515":  "科技",
            "2516":  "财经",
            "2517":  "股市",
            "2518":  "美股"
        }

    def start_requests(self):
        """返回一个Request迭代器
        """
        # 遍历所有类型的论文
        for cate_id in self.cate_dict.keys():
            for page in range(1, self.total_pages + 1):
                lid = cate_id
                # 这里就是一个随机数，具体含义不是很清楚
                r = random.random()
                # cb_kwargs 是用来往解析函数parse中传递参数的
                yield Request(self.base_url.format(lid, page, r), callback=self.parse, cb_kwargs={"cate_id": lid})
    
    def parse(self, response, cate_id):
        """解析网页内容，并提取网页中需要的内容
        """
        json_result = json.loads(response.text) # 将请求回来的页面解析成json
        # 提取json中我们想要的字段
        # json使用get方法比直接通过字典的形式获取数据更方便，因为不需要处理异常
        data_list = json_result.get('result').get('data')
        for data in data_list:
            item = SinanewsItem()

            item['cate'] = self.cate_dict[cate_id]
            item['title'] = data.get('title')
            item['url'] = data.get('url')
            item['raw_key_words'] = data.get('keywords')

            # ctime = datetime.fromtimestamp(int(data.get('ctime')))
            # ctime = datetime.strftime(ctime, '%Y-%m-%d %H:%M')

            # 保留的是一个时间戳
            item['ctime'] = data.get('ctime')

            # meta参数传入的是一个字典，在下一层可以将当前层的item进行复制
            yield Request(url=item['url'], callback=self.parse_content, meta={'item': item})
    
    def parse_content(self, response):
        """解析文章内容
        """
        item = response.meta['item']
        content = ''.join(response.xpath('//*[@id="artibody" or @id="article"]//p/text()').extract())
        content = re.sub(r'\u3000', '', content)
        content = re.sub(r'[ \xa0?]+', ' ', content)
        content = re.sub(r'\s*\n\s*', '\n', content)
        content = re.sub(r'\s*(\s)', r'\1', content)
        content = ''.join([x.strip() for x in content])
        item['content'] = content
        yield item 

```

数据持久化实现,代码实现:

```python
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
# useful for handling different item types with a single interface
import time
import datetime
import pymongo
from pymongo.errors import DuplicateKeyError
from sinanews.items import SinanewsItem
from itemadapter import ItemAdapter


# 新闻item持久化
class SinanewsPipeline:
    """数据持久化：将数据存放到mongodb中
    """
    def __init__(self, host, port, db_name, collection_name):
        self.host = host
        self.port = port
        self.db_name = db_name
        self.collection_name = collection_name

    @classmethod    
    def from_crawler(cls, crawler):
        """自带的方法，这个方法可以重新返回一个新的pipline对象，并且可以调用配置文件中的参数
        """
        return cls(
            host = crawler.settings.get("MONGO_HOST"),
            port = crawler.settings.get("MONGO_PORT"),
            db_name = crawler.settings.get("DB_NAME"),
            # mongodb中数据的集合按照日期存储
            collection_name = crawler.settings.get("COLLECTION_NAME") + \
                "_" + time.strftime("%Y%m%d", time.localtime())
        )

    def open_spider(self, spider):
        """开始爬虫的操作，主要就是链接数据库及对应的集合
        """
        self.client = pymongo.MongoClient(self.host, self.port)
        self.db = self.client[self.db_name]
        self.collection = self.db[self.collection_name]
        
    def close_spider(self, spider):
        """关闭爬虫操作的时候，需要将数据库断开
        """
        self.client.close()

    def process_item(self, item, spider):
        """处理每一条数据，注意这里需要将item返回
        注意：判断新闻是否是今天的，每天只保存当天产出的新闻，这样可以增量的添加新的新闻数据源
        """
        if isinstance(item, SinanewsItem):
            try:
                # TODO 物料去重逻辑，根据title进行去重，先读取物料池中的所有物料的title然后进行去重

                cur_time = int(item['ctime'])
                str_today = str(datetime.date.today())
                min_time = int(time.mktime(time.strptime(str_today + " 00:00:00", '%Y-%m-%d %H:%M:%S')))
                max_time = int(time.mktime(time.strptime(str_today + " 23:59:59", '%Y-%m-%d %H:%M:%S')))
                if cur_time > min_time and cur_time <= max_time:
                    self.collection.insert(dict(item))
            except DuplicateKeyError:
                """
                说明有重复
                """
                pass
        return item

```

**抓取新闻相关文件**

- `items.py`:定义新闻数据的对象
- `sina.py`:抓取新闻数据,通过新闻分类映射字典,然后遍历新闻内容网页,解析网页获得网页内容;
- `pipelines.py`:数据持久化实现,存储在`mongodb`数据库并处理数据,如果上一天的数据则,存储到`SinaNews.new_<current_date>`集合中;
- `settings.py` :配置文件;
- `monitor_news.py`:监控文件,定时脚本调用文件
- `run_scrapy_sina.sh`:运行脚本，具体用法`sh run_scrapy_sina.sh`

## 物料画像构建

**物料来源**: 每天在新闻网站上爬取获取存储在`mongodb`的数据;

**实现逻辑** 

- 将新物料添加到物料特征库中（`MongoDB.NewsRecSys`库`FeatureProtrail`集合）;
- 旧物料画像，通过用户的交互记录进行更新;
- 完成了新、旧物料画像的更新之后,最新的数据存储到`RedisPortrail`集合中，用于前端展示;

**物料画像更新核心代码**: `materials/material_process/news_protrait.py`

```python
# -*- coding: utf-8 -*-
from re import S
import sys
import json
sys.path.append("../")
from material_process.utils import get_key_words
from dao.mongo_server import MongoServer
from dao.redis_server import RedisServer

"""
新闻画像中包含的字段：
0. news_id 新闻的id
1. title 标题
2. raw_key_words (爬下来的关键词，可能有缺失)
3. manual_key_words (根据内容生成的关键词)
4. ctime 时间
5. content 新闻具体内容
6. cate 新闻类别
7. likes 新闻点赞数量
8. collections 新闻收藏数量
9. read_nums 阅读次数
10. url 新闻原始链接
"""

class NewsProtraitServer:
    def __init__(self):
        """初始化相关参数
        """
        self.mongo_server = MongoServer()   
        self.sina_collection = self.mongo_server.get_sina_news_collection()
        self.material_collection = self.mongo_server.get_feature_protrail_collection()
        self.redis_mongo_collection = self.mongo_server.get_redis_mongo_collection()
        self.news_dynamic_feature_redis = RedisServer().get_dynamic_news_info_redis()

    def _find_by_title(self, collection, title):
        """从数据库中查找是否有相同标题的新闻数据
        数据库存在当前标题的数据返回True, 反之返回Flase
        """
        # find方法，返回的是一个迭代器
        find_res = collection.find({"title": title})
        if len(list(find_res)) != 0:
            return True
        return False

    def _generate_feature_protrail_item(self, item):
        """生成特征画像数据，返回一个新的字典
        """
        news_item = dict()
        news_item['news_id'] = item['news_id']
        news_item['title'] = item['title']
        # 从新闻内容中提取的关键词没有原始新闻爬取时的关键词准确，所以手动提取的关键词
        # 只是作为一个补充，当原始新闻中没有提供关键词的时候可以使用
        news_item['raw_key_words'] = item['raw_key_words']
        key_words_list = get_key_words(item['content'])
        news_item['manual_key_words'] = ",".join(key_words_list)
        news_item['ctime'] = item['ctime']
        news_item['content'] = item['content']
        news_item['cate'] = item['cate']
        news_item['url'] = item['url']
        news_item['likes'] = 0
        news_item['collections'] = 0
        news_item['read_num'] = 0
        news_item['hot_value'] = 1000 # 初始化一个比较大的热度值，会随着时间进行衰减
        
        return news_item

    def update_new_items(self):
        """将今天爬取的数据构造画像存入画像数据库中
        """
        # 遍历今天爬取的所有数据
        for item in self.sina_collection.find():
            # 根据标题进行去重
            if self._find_by_title(self.material_collection, item["title"]):
                continue
            news_item = self._generate_feature_protrail_item(item)
            # 插入物料池
            self.material_collection.insert_one(news_item)
        
        print("run update_new_items success.")

    def update_redis_mongo_protrail_data(self):
        """每天都需要将新闻详情更新到redis中，并且将前一天的redis数据删掉
        """
        # 每天先删除前一天的redis展示数据，然后再重新写入
        self.redis_mongo_collection.drop()
        print("delete RedisProtrail ...")
        # 遍历特征库
        for item in self.material_collection.find():
            news_item = dict()
            news_item['news_id'] = item['news_id']
            news_item['title'] = item['title']
            news_item['ctime'] = item['ctime']
            news_item['content'] = item['content']
            news_item['cate'] = item['cate']
            news_item['url'] = item['url']
            news_item['likes'] = 0
            news_item['collections'] = 0
            news_item['read_num'] = 0

            self.redis_mongo_collection.insert_one(news_item)
        print("run update_redis_mongo_protrail_data success.")

    def update_dynamic_feature_protrail(self):
        """用redis的动态画像更新mongodb的画像
        """
        # 遍历redis的动态画像，将mongodb中对应的动态画像更新        
        news_list = self.news_dynamic_feature_redis.keys()
        for news_key in news_list:
            news_dynamic_info_str = self.news_dynamic_feature_redis.get(news_key)
            news_dynamic_info_str = news_dynamic_info_str.replace("'", '"' ) # 将单引号都替换成双引号
            news_dynamic_info_dict = json.loads(news_dynamic_info_str)
            
            # 查询mongodb中对应的数据，并将对应的画像进行修改
            news_id = news_key.split(":")[1]
            mongo_info = self.material_collection.find_one({"news_id": news_id})
            new_mongo_info = mongo_info.copy()
            new_mongo_info['likes'] = news_dynamic_info_dict["likes"]
            new_mongo_info['collections'] = news_dynamic_info_dict["collections"]
            new_mongo_info['read_num'] = news_dynamic_info_dict["read_num"]

            self.material_collection.replace_one(mongo_info, new_mongo_info, upsert=True) # upsert为True的话，没有就插入
        print("update_dynamic_feature_protrail success.")


# 系统最终执行的不是这个脚本，下面的代码是用来测试的
if __name__ == "__main__":
    news_protrait = NewsProtraitServer()
    # 新物料画像的更新
    news_protrait.update_new_items()
    # 更新动态特征
    news_protrait.update_dynamic_feature_protrail()
    # redis展示新闻内容的备份
    news_protrait.update_redis_mongo_protrail_data()
```

**用于前端展示的逻辑代码**:`materials/material_process/news_to_redis.py`

```python
import sys
sys.path.append("../../")
from dao.mongo_server import MongoServer
from dao.redis_server import RedisServer


class NewsRedisServer(object):
    def __init__(self):
        self.rec_list_redis = RedisServer().get_reclist_redis()
        self.static_news_info_redis = RedisServer().get_static_news_info_redis()
        self.dynamic_news_info_redis = RedisServer().get_dynamic_news_info_redis()

        self.redis_mongo_collection = MongoServer().get_redis_mongo_collection()

        # 删除前一天redis中的内容
        self._flush_redis_db()

    def _flush_redis_db(self):
        """每天都需要删除redis中的内容，更新当天新的内容上去
        """
        try:
            self.rec_list_redis.flushall()
        except Exception:
            print("flush redis fail ... ")

    def _get_news_id_list(self):
        """获取物料库中所有的新闻id
        """
        # 获取所有数据的news_id,
        # 暴力获取，直接遍历整个数据库，得到所有新闻的id
        # TODO 应该存在优化方法可以通过查询的方式只返回new_id字段
        news_id_list = []
        for item in self.redis_mongo_collection.find():
            news_id_list.append(item["news_id"])
        return news_id_list

    def _set_info_to_redis(self, redisdb, content):
        """将content添加到指定redis
        """
        try: 
            redisdb.set(*content)
        except Exception:
            print("set content fail".format(content))

    def news_detail_to_redis(self):
        """将需要展示的画像内容存储到redis
        静态不变的特征存到static_news_info_db_num
        动态会发生改变的特征存到dynamic_news_info_db_num
        """ 
        news_id_list = self._get_news_id_list()

        for news_id in news_id_list:
            news_item_dict = self.redis_mongo_collection.find_one({"news_id": news_id}) # 返回的是一个列表里面套了一个字典  
            news_item_dict.pop("_id")

            # 分离动态属性和静态属性
            static_news_info_dict = dict()
            static_news_info_dict['news_id'] = news_item_dict['news_id']
            static_news_info_dict['title'] = news_item_dict['title']
            static_news_info_dict['ctime'] = news_item_dict['ctime']
            static_news_info_dict['content'] = news_item_dict['content']
            static_news_info_dict['cate'] = news_item_dict['cate']
            static_news_info_dict['url'] = news_item_dict['url']
            static_content_tuple = "static_news_detail:" + str(news_id), str(static_news_info_dict)
            self._set_info_to_redis(self.static_news_info_redis, static_content_tuple)

            dynamic_news_info_dict = dict()
            dynamic_news_info_dict['likes'] = news_item_dict['likes']
            dynamic_news_info_dict['collections'] = news_item_dict['collections']
            dynamic_news_info_dict['read_num'] = news_item_dict['read_num']
            dynamic_content_tuple = "dynamic_news_detail:" + str(news_id), str(dynamic_news_info_dict)
            self._set_info_to_redis(self.dynamic_news_info_redis, dynamic_content_tuple)

        print("news detail info are saved in redis db.")


if __name__ == "__main__":
    # 每次创建这个对象的时候都会把数据库中之前的内容删除
    news_redis_server = NewsRedisServer()
    # 将最新的前端展示的画像传到redis
    news_redis_server.news_detail_to_redis()
```

## 用户画像构建 

用户画像的更新主要分为两方面：
1. 新注册用户画像的更新
2. 老用户画像的更新

实现逻辑:
- `materials/user_process/user_to_mysql.py`.`user_exposure_to_mysql()`:用户新闻曝光数据从`Redis（用户ID：{<list>(新闻ID: 曝光时刻)}）`存储到`MySQL.exposure_<current_date>`表;
- `materials/user_process/user_protrail.py`.`update_user_protrail_from_register_table()`:当天新用户（注册用户）和老用户的静态信息和动态信息（阅读、点赞、收藏等相关指标数据）都添加到用户画像`MongoDB.NewsRecSys.UserProtrail`集合;
- `materials/user_process/user_protrail.py`.`_user_info_to_dict()`:用户基本属性和用户的动态信息进行组合，已有指标数据（点赞和收藏关键指标:历史Top3新闻类别、新闻Top3关键词、新闻的平均热度、用户15天内喜欢的新闻数量）进行更新，新指标数据进行初始化;


核心逻辑代码:

```python
import sys
import datetime
from collections import Counter, defaultdict

from sqlalchemy.sql.expression import table
sys.path.append("../../")
from dao.mongo_server import MongoServer
from dao.mysql_server import MysqlServer
from dao.entity.register_user import RegisterUser
from dao.entity.user_read import UserRead
from dao.entity.user_likes import UserLikes
from dao.entity.user_collections import UserCollections


class UserProtrail(object):
    def __init__(self):
        self.user_protrail_collection = MongoServer().get_user_protrail_collection()
        self.material_collection = MongoServer().get_feature_protrail_collection()
        self.register_user_sess = MysqlServer().get_register_user_session()
        self.user_collection_sess = MysqlServer().get_user_collection_session()
        self.user_like_sess = MysqlServer().get_user_like_session()
        self.user_read_sess = MysqlServer().get_user_read_session()

    def _user_info_to_dict(self, user):
        """将mysql查询出来的结果转换成字典存储
        """
        info_dict = dict()
        
        # 基本属性特征
        info_dict["userid"] = user.userid
        info_dict["username"] = user.username
        info_dict["passwd"] = user.passwd
        info_dict["gender"] = user.gender
        info_dict["age"] = user.age
        info_dict["city"] = user.city

        # 兴趣爱好 
        behaviors=["like","collection"]
        time_range = 15
        _, feature_dict = self.get_statistical_feature_from_history_behavior(user.userid,time_range,behavior_types=behaviors)
        for type in feature_dict.keys():
            if feature_dict[type]:
                info_dict["{}_{}_intr_cate".format(type,time_range)] = feature_dict[type]["intr_cate"]  # 历史喜欢最多的Top3的新闻类别
                info_dict["{}_{}_intr_key_words".format(type,time_range)] = feature_dict[type]["intr_key_words"] # 历史喜欢新闻的Top3的关键词
                info_dict["{}_{}_avg_hot_value".format(type,time_range)] = feature_dict[type]["avg_hot_value"] # 用户喜欢新闻的平均热度
                info_dict["{}_{}_news_num".format(type,time_range)] = feature_dict[type]["news_num"] # 用户15天内喜欢的新闻数量
            else:
                info_dict["{}_{}_intr_cate".format(type,time_range)] = ""  # 历史喜欢最多的Top3的新闻类别
                info_dict["{}_{}_intr_key_words".format(type,time_range)] = "" # 历史喜欢新闻的Top3的关键词
                info_dict["{}_{}_avg_hot_value".format(type,time_range)] = 0 # 用户喜欢新闻的平均热度
                info_dict["{}_{}_news_num".format(type,time_range)] = 0 # 用户15天内喜欢的新闻数量

        return info_dict

    def update_user_protrail_from_register_table(self):
        """每天都需要将当天注册的用户添加到用户画像池中
        """
        # 遍历注册用户表
        for user in self.register_user_sess.query(RegisterUser).all():
            user_info_dict = self._user_info_to_dict(user)
            old_user_protrail_dict = self.user_protrail_collection.find_one({"username": user.username})
            if old_user_protrail_dict is None:
                self.user_protrail_collection.insert_one(user_info_dict)
            else:
                # 使用参数upsert设置为true对于没有的会创建一个
                # replace_one 如果遇到相同的_id 就会更新
                self.user_protrail_collection.replace_one(old_user_protrail_dict, user_info_dict, upsert=True)
            

    def get_statistical_feature_from_history_behavior(self, user_id, time_range, behavior_types):
        """获取用户历史行为的统计特征 ["read","like","collection"] """
        fail_type = []
        sess, table_obj, history = None, None, None
        feature_dict = defaultdict(dict)

        end = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        start = (datetime.datetime.now()+datetime.timedelta(days=-time_range)).strftime("%Y-%m-%d %H:%M:%S")

        for type in behavior_types:
            if type == "read":
                sess = getattr(self,"user_{}_sess".format(type))
                table_obj = UserRead
            elif type == "like":
                sess = getattr(self,"user_{}_sess".format(type))
                table_obj = UserLikes
            elif type == "collection":
                sess = getattr(self,"user_{}_sess".format(type))
                table_obj = UserCollections
            try:
                history = sess.query(table_obj).filter(table_obj.userid==user_id).filter(table_obj.curtime>=start).filter(table_obj.curtime<=end).all()
            except Exception as e:
                print(str(e))
                fail_type.append(type)
                continue
            
            feature_dict[type] = self._gen_statistical_feature(history)
            
        return fail_type, feature_dict
          
    def _gen_statistical_feature(self,history):
        """"""
        # 为history 获取特征
        if not len(history): return None
        history_new_id = []
        history_hot_value = []
        history_new_cate = []
        history_key_word = []
        for h in history:
            news_id = h.newid 
            newsquery = {"news_id":news_id}
            result = self.material_collection.find_one(newsquery)
            history_new_id.append(result["news_id"])
            history_hot_value.append(result["hot_value"])
            history_new_cate.append(result["cate"])
            history_key_word += result["manual_key_words"].split(",")
        
        feature_dict = dict()
        # 计算平均热度
        feature_dict["avg_hot_value"] = 0 if sum(history_hot_value) < 0.001 else sum(history_hot_value) / len(history_hot_value)

        # 计算Top3的类别
        cate_dict = Counter(history_new_cate)
        cate_list= sorted(cate_dict.items(),key = lambda d: d[1], reverse=True)
        cate_str = ",".join([item[0] for item in cate_list[:3]] if len(cate_list)>=3 else [item[0] for item in cate_list] )
        feature_dict["intr_cate"] = cate_str

        # 计算Top3的关键词
        word_dict = Counter(history_key_word)
        word_list= sorted(word_dict.items(),key = lambda d: d[1], reverse=True)
        # TODO 关键字属于长尾 如果关键字的次数都是一次 该怎么去前3
        word_str = ",".join([item[0] for item in word_list[:3]] if len(cate_list)>=3 else [item[0] for item in word_list] )
        feature_dict["intr_key_words"] = word_str
        # 新闻数目
        feature_dict["news_num"] = len(history_new_id)

        return feature_dict


if __name__ == "__main__":
    user_protrail = UserProtrail().update_user_protrail_from_register_table()

```
## 自动化构建画像

物料画像:`materials\process_material.py`;

```python

from material_process.news_protrait import NewsProtraitServer
from material_process.news_to_redis import NewsRedisServer

def process_material():
    """物料处理函数
    """
    # 画像处理
    protrail_server = NewsProtraitServer()
    # 处理最新爬取新闻的画像，存入特征库
    protrail_server.update_new_items()
    # 更新新闻动态画像, 需要在redis数据库内容清空之前执行
    protrail_server.update_dynamic_feature_protrail()
    # 生成前端展示的新闻画像，并在mongodb中备份一份
    protrail_server.update_redis_mongo_protrail_data()


if __name__ == "__main__":
    process_material() 

```

用户画像:`materials\process_user.py`;

```python
from user_process.user_to_mysql import UserMysqlServer
from user_process.user_protrail import UserProtrail

"""
1. 将用户的曝光数据从redis落到mysql中。
2. 更新用户画像
"""

    
def process_users():
    """将用户数据落 Mysql
    """
    # 用户mysql存储
    user_mysql_server = UserMysqlServer()
    # 用户曝光数据落mysql
    user_mysql_server.user_exposure_to_mysql()

    # 更新用户画像
    user_protrail = UserProtrail()
    user_protrail.update_user_protrail_from_register_table()


if __name__ == "__main__":
    process_users() 
```

`Redis`数据更新:（`materials\update_redis.py`);

```python

from material_process.news_protrait import NewsProtraitServer
from material_process.news_to_redis import NewsRedisServer


def update():
    """物料处理函数
    """
    # 新闻数据写入redis, 注意这里处理redis数据的时候是会将前一天的数据全部清空
    news_redis_server = NewsRedisServer()
    # 将最新的前端展示的画像传到redis
    news_redis_server.news_detail_to_redis()


if __name__ == "__main__":
    update() 

```

最后将上面三个脚本穿起来的shell脚本`offline_material_and_user_process.sh`：

```python
#!/bin/bash

python=/home/recsys/miniconda3/envs/news_rec_py3/bin/python  #注意修改路径
news_recsys_path="/home/recsys/news_rec_server" # 注意修改路径

echo "$(date -d today +%Y-%m-%d-%H-%M-%S)"

# 为了更方便的处理路径的问题，可以直接cd到我们想要运行的目录下面
cd ${news_recsys_path}/materials

# 更新物料画像
${python} process_material.py
if [ $? -eq 0 ]; then
    echo "process_material success."
else   
    echo "process_material fail."
fi 

# 更新用户画像
${python} process_user.py
if [ $? -eq 0 ]; then
    echo "process_user.py success."
else   
    echo "process_user.py fail."
fi

# 清除前一天redis中的数据，更新最新今天最新的数据
${python} update_redis.py
if [ $? -eq 0 ]; then
    echo "update_redis success."
else   
    echo "update_redis fail."
fi


echo " "
```

crontab定时任务，每天凌晨1点执行shell脚本


## 参考文件

1. [Scrapy框架新手入门教程](https://blog.csdn.net/sxf1061700625/article/details/106866547/)
2. [scrapy中文文档](https://www.osgeo.cn/scrapy/index.html)