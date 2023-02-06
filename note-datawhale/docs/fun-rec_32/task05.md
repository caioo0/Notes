# Task05 推荐流程的构建

> （本学习笔记来源于DataWhale-12月组队学习：[推荐系统实战](https://github.com/datawhalechina/fun-rec)，[直播视频地址](https://datawhale.feishu.cn/minutes/obcnzns778b725r5l535j32o)） 

```bash
    The past is the past. The future is all that's worth discussing.
    不念过往，未来可期。
```

![](http://ryluo.oss-cn-chengdu.aliyuncs.com/图片Untitled.png)


##  推荐系统流程构建

- `Offilne`部分：主要是基于离线物料系统生成的物料画像和用户画像进行离线计算，为每个用户生成热门页列表和推荐页列表并进行缓存(存储到`Redis`中),方便online服务的列表获取
- `Online`部分：为用户在使用APP或者系统的过程中触发的行为提供一系列服务,主要是针对不同的用户，使用不同的策略，提供热门页列表和推荐页列表的新闻数据，进行过滤排序之后，展示到前端页面上。

## 1 `Offline`部分

### 1.1 热门页列表构建

#### 1.1.1 业务流程

- 热门页规则： 每篇文章，会根据它的发布时间，用户对它的行为记录(获得的点赞数，收藏数和阅读数)去计算该文章的热度信息， 然后根据热度值进行排序得到， 所以计算文章的热门记录， 只需要文章画像的动静态信息即可，（`天级更新`）。
-  offline：每天凌晨物料系统生成的物料画像（储存在`MongoDB`.`NewsRecSys`.`FeatureProtail`集合），根据热门规则，更新所有新闻的热度值，根据热度值排序，得到文章热门列表并存入`redis`,供online服务提取显示热门页列表。


#### 1.1.2 部分实现代码

代码位于`recprocess/recall/hot_recall.py`

```python
# 导入
import sys
sys.path.append('../../')
from conf.dao_config import cate_dict
from dao.mongo_server import MongoServer
from dao.redis_server import RedisServer
from datetime import datetime


'''
这里需要从物料库中获取物料的信息，然后更新物料当天最新的热度信息;
最终将计算好的物料热度，对物料进行排序
'''
class HotRecall(object):
    def __init__(self):
        # MongoDB.NewsRecSys.FeatureProtail集合
        self.feature_protrail_collection = MongoServer().get_feature_protrail_collection()
        
        self.reclist_redis = RedisServer().get_reclist_redis()
        self.cate_dict = cate_dict

    def update_hot_value(self):
        
        """
        更新物料库中所有新闻的热度值（最近3天的数）
        """
        # 遍历物料池里面的所有文章
        for item in self.feature_protrail_collection.find():
            news_id = item['news_id']
            news_cate = item['cate']
            news_ctime = item['ctime']
            news_likes_num = item['likes']
            news_collections_num = item['collections']
            news_read_num = item['read_num']
            news_hot_value = item['hot_value']

            # 时间转换与计算时间差   前提要保证当前时间大于新闻创建时间，目前没有捕捉异常
            news_ctime_standard = datetime.strptime(news_ctime, "%Y-%m-%d %H:%M")
            cur_time_standard = datetime.now()
            time_day_diff = (cur_time_standard - news_ctime_standard).days
            time_hour_diff = (cur_time_standard - news_ctime_standard).seconds / 3600

            # 只要最近3天的内容
            if time_day_diff > 3:
                continue

            # 72 表示的是3天的72小时（0.6，0.3d等为权重）
            news_hot_value = (news_likes_num * 0.6 + news_collections_num * 0.3 + news_read_num * 0.1) * 10 / (1 + time_hour_diff / 72) 

            # 更新物料池的文章hot_value
            item['hot_value'] = news_hot_value
            self.feature_protrail_collection.update({'news_id':news_id}, item)

            
    '''
    主要用于将物料库（`FeatureProtail`集合），通过遍历各类新闻，按照下面形式存入Redis[0]的`hot_list_news_cate`中：
    hot_list_news_cate:<新闻类别标识>: {<新闻类别名>_<新闻id>:<热度值>}
    '''
    def group_cate_for_news_list_to_redis(self, ):
        """
        将每个用户的推荐列表按照类别分开，方便后续打散策略的实现
        对于热门页来说，只需要提前将所有的类别新闻都分组聚合就行，后面单独取就可以
        注意：运行当前脚本的时候需要需要先更新新闻的热度值
        """
        # 1. 按照类别先将所有的新闻都分开存储
        for cate_id, cate_name in self.cate_dict.items():
            redis_key = "hot_list_news_cate:{}".format(cate_id)
            for item in self.feature_protrail_collection.find({"cate": cate_name}):
                self.reclist_redis.zadd(redis_key, {'{}_{}'.format(item['cate'], item['news_id']): item['hot_value']})
        

if __name__ == "__main__":
    hot_recall = HotRecall()
    # 更新物料的热度值
    hot_recall.update_hot_value()
    # 将新闻的热度模板添加到redis中
    hot_recall.group_cate_for_news_list_to_redis()

```

> 公式源于魔方秀公式：  (总赞数 * 0.7 + 总评论数 * 0.3) * 1000 / (公布时间距离当前时间的小时差+2) ^ 1.2
> 最初的公式为Hacker News算法： Score = (P-1) / (T+2)^G 其中P表示文章得到的投票数，需要去掉文章发布者的那一票；T表示时间衰减（单位小时）；G为权重，默认值为1.8


```python
news_hot_value = (news_likes_num * 0.6 + news_collections_num * 0.3 + news_read_num * 0.1) * 10 / (1 + time_hour_diff / 72)
```


    ---------------------------------------------------------------------------

    NameError                                 Traceback (most recent call last)

    ~\AppData\Local\Temp/ipykernel_25196/481962602.py in <module>
    ----> 1 news_hot_value = (news_likes_num * 0.6 + news_collections_num * 0.3 + news_read_num * 0.1) * 10 / (1 + time_hour_diff / 72)
    

    NameError: name 'news_likes_num' is not defined




### 1.2 推荐页列表构建

#### 1.2.1 业务流程


推荐页规则： 每个用户，我们会生成不同的推荐页面，这就是我们所知悉的"千人千面"。

- 针对新用户：建立冷启动的推荐页列表数据，比如年龄，性别(用户注册时会获取到)等，获取到一些大类别下的文章(适合该年龄，该性别看的文章)，然后再根据文章的热度信息，给新用户生成一份冷启动推荐列表；

- 针对老用户：提供个性化推荐，就走个性化推荐流程， 通过召回→排序→重排等，给老用户生成一份个性化列表。最终都存储到Redis中。

#### 1.2.2 部分实现代码


代码位于`recprocess/cold_start/cold_start.py`

```python

# 导入模块
import sys
from sqlalchemy.sql.functions import user
sys.path.append('../../')
from conf.dao_config import cate_dict
from dao.mongo_server import MongoServer
from dao.redis_server import RedisServer
from dao.mysql_server import MysqlServer
from dao.entity.register_user import RegisterUser
from collections import defaultdict


# 这里需要从物料库中获取物料的信息，把物料按冷启用户分组
# 对不同组的冷启用户推荐对应物料50条 + 10条本地新闻 按热度值排序 并去重 

"""
第一版先不考虑用户位置和新闻位置的关系，因为目前新闻的数据量太少了
冷启动用户分组，最终的内容按照热度进行排序：
"""

class ColdStart(object):
    
    # 初始化 
    def __init__(self):
        
        # 物料库（MongoDB.NewsRecSys.FeatureProtail集合数据
        self.feature_protrail_collection = MongoServer().get_feature_protrail_collection()
        # redis 
        self.reclist_redis = RedisServer().get_reclist_redis()
        # Mysql
        self.register_user_sess = MysqlServer().get_register_user_session()
        self.cate_dict = cate_dict
        self.name2id_cate_dict = {v: k for k, v in self.cate_dict.items()}
        self._set_user_group()

        
    def _set_user_group(self):
        """将用户进行分组
        1. age < 23 && gender == female  
        2. age >= 23 && gender == female 
        3. age < 23 && gender == male 
        4. age >= 23 && gender == male  
        """
        self.user_group = {
            "1": ["国内","娱乐","体育","科技"],
            "2": ["国内","社会","美股","财经","股市"],
            "3": ["国内","股市","体育","科技"],
            "4": ["国际", "国内","军事","社会","美股","财经","股市"]
        }
        self.group_to_cate_id_dict = defaultdict(list)
        for k, cate_list in self.user_group.items():
            for cate in cate_list:
                self.group_to_cate_id_dict[k].append(self.name2id_cate_dict[cate])

                
    def _copy_cold_start_list_to_redis(self, user_id, group_id):
        
        """
        将确定分组后的用户的物料添加到redis中，并记录当前用户的所有新闻类别id
        """
        # 遍历当前分组的新闻类别
        for cate_id in self.group_to_cate_id_dict[group_id]:
            group_redis_key = "cold_start_group:{}:{}".format(group_id, cate_id)
            user_redis_key = "cold_start_user:{}:{}".format(user_id, cate_id)
            self.reclist_redis.zunionstore(user_redis_key, [group_redis_key])
        # 将用户的类别集合添加到redis中
        cate_id_set_redis_key = "cold_start_user_cate_set:{}".format(user_id)
        self.reclist_redis.sadd(cate_id_set_redis_key, *self.group_to_cate_id_dict[group_id])

    def user_news_info_to_redis(self):
        """
        按照用户、新闻分类提供用户冷启动的推荐模板；遍历所有用户;
        将每个用户涉及到的不同的新闻列表取出新闻热度值存储到redis.cold_start_user中去
        """
        for user_info in self.register_user_sess.query(RegisterUser).all():
            # 年龄不正常的人，随便先给一个分组，后面还需要在前后端补充相关逻辑
            try:
                age = int(user_info.age)
            except:
                self._copy_cold_start_list_to_redis(user_info.userid, group_id="4")
                print("user_info.age: {}".format(user_info.age)) 

            if age < 23 and user_info.gender == "female":
                self._copy_cold_start_list_to_redis(user_info.userid, group_id="1")
            elif age >= 23 and user_info.gender == "female":
                self._copy_cold_start_list_to_redis(user_info.userid, group_id="2")
            elif age < 23 and user_info.gender == "male":
                self._copy_cold_start_list_to_redis(user_info.userid, group_id="3")
            elif age >= 23 and user_info.gender == "male":
                self._copy_cold_start_list_to_redis(user_info.userid, group_id="4")
            else:
                pass 

    # 当先系统使用的方法
    def generate_cold_user_strategy_templete_to_redis_v2(self):
        
        """
        冷启动用户模板，总共分成了四类人群
        每类人群都把每个类别的新闻单独存储
        cold_start_group:<人群分类ID>:<新闻类别标识>: {<新闻类别名>_<新闻id>:<热度值>}
        """
        for k, item in self.user_group.items():
            for cate in item:
                cate_cnt = 0
                cate_id = self.name2id_cate_dict[cate]
                # k 表示人群分组
                redis_key = "cold_start_group:{}:{}".format(str(k), cate_id)
                for news_info in self.feature_protrail_collection.find({"cate": cate}):
                    cate_cnt += 1
                    self.reclist_redis.zadd(redis_key, {news_info['cate'] + '_' + news_info['news_id']: news_info['hot_value']}, nx=True)
                print("类别 {} 的 新闻数量为 {}".format(cate, cate_cnt))


if __name__ == "__main__":
    # ColdStart().generate_cold_user_strategy_templete_to_redis_v2()
    # ColdStart().generate_cold_start_news_list_to_redis_for_register_user()
    cold_start = ColdStart()
    cold_start.generate_cold_user_strategy_templete_to_redis_v2()
    cold_start.user_news_info_to_redis()

```



## 2 `Online`部分

### 2.1 热门页列表构建

#### 2.1.1 业务流程

- 获取用户曝光列表，得到所有的新闻ID
- 针对新用户，从之前的离线热门页列表中，为该用户生成一份热门页列表，针对老用户，直接获取该用户的热门页列表
- 对上述热门列表，每次选取10条新闻，进行页面展示
- 对已选取的10条新闻，更新曝光记录;

#### 2.1.2 核心代码逻辑
代码位于`recprocess/online.py`

```python

import sys
sys.path.append("../../")
sys.path.append("../")
import json
import time
import threading
from conf.dao_config import cate_dict
from conf.proj_path import bad_case_news_log_path
from dao.redis_server import RedisServer
from dao.mysql_server import MysqlServer
from dao.entity.register_user import RegisterUser
from controller.user_action_controller import UserAction
from collections import defaultdict

redis_server = RedisServer()

class OnlineServer(object):
    """单例模式推荐服务类
    """
    _instance_lock = threading.Lock()
 
    def __init__(self,):
        self.reclist_redis_db = redis_server.get_reclist_redis()
        self.static_news_info_redis_db = redis_server.get_static_news_info_redis()
        self.dynamic_news_info_redis_db = redis_server.get_dynamic_news_info_redis()
        self.exposure_redis_db = redis_server.get_exposure_redis()
        self.register_sql_sess = MysqlServer().get_register_user_session()
        self.cate_dict = cate_dict
        self.cate_id_list = list(self.cate_dict.keys())
        self.bad_case_news_log_path = bad_case_news_log_path
        self.name2id_cate_dict = {v: k for k, v in self.cate_dict.items()}
        self._set_user_group() 

    def __new__(cls, *args, **kwargs):
        if not hasattr(OnlineServer, "_instance"):
            with OnlineServer._instance_lock:
                if not hasattr(OnlineServer, "_instance"):
                    OnlineServer._instance = object.__new__(cls)  
        return OnlineServer._instance
    
    def _get_register_user_cold_start_redis_key(self, userid):
        """通过查sql表得到用户的redis key进而确定当前新用户使用哪一个新的模板
        """
        user_info = self.register_sql_sess.query(RegisterUser).filter(RegisterUser.userid == userid).first()
        print(user_info)
        if int(user_info.age) < 23 and user_info.gender == "female":
            redis_key = "cold_start_group:{}".format(str(1))
        elif int(user_info.age) >= 23 and user_info.gender == "female":
            redis_key = "cold_start_group:{}".format(str(2))
        elif int(user_info.age) < 23 and user_info.gender == "male":
            redis_key = "cold_start_group:{}".format(str(3))
        elif int(user_info.age) >= 23 and user_info.gender == "male":
            redis_key = "cold_start_group:{}".format(str(4))
        else:
            pass 
        return redis_key

    def _set_user_group(self):
        """将用户进行分组
        1. age < 23 && gender == female  
        2. age >= 23 && gender == female 
        3. age < 23 && gender == male 
        4. age >= 23 && gender == male  
        """
        self.user_group = {
            "1": ["国内","娱乐","体育","科技"],
            "2": ["国内","社会","美股","财经","股市"],
            "3": ["国内","股市","体育","科技"],
            "4": ["国际", "国内","军事","社会","美股","财经","股市"]
        }
        self.group_to_cate_id_dict = defaultdict(list)
        for k, cate_list in self.user_group.items():
            for cate in cate_list:
                self.group_to_cate_id_dict[k].append(self.name2id_cate_dict[cate])

    def _get_register_user_group_id(self, age, gender):
        """获取注册用户的分组,
        bug: 新用户注册可能会有延迟
        """
        if int(age) < 23 and gender == "female":
            return "1"
        elif int(age) >= 23 and gender == "female":
            return "2"
        elif int(age) < 23 and gender == "male":
            return "3"
        elif int(age) >= 23 and gender == "male":
            return "4"
        else:
            return "error" 

    def _copy_cold_start_list_to_redis(self, user_id, group_id):
        """将确定分组后的用户的物料添加到redis中，并记录当前用户的所有新闻类别id
        """
        # 遍历当前分组的新闻类别
        for cate_id in self.group_to_cate_id_dict[group_id]:
            group_redis_key = "cold_start_group:{}:{}".format(group_id, cate_id)
            user_redis_key = "cold_start_user:{}:{}".format(user_id, cate_id)
            self.reclist_redis_db.zunionstore(user_redis_key, [group_redis_key])
        # 将用户的类别集合添加到redis中
        cate_id_set_redis_key = "cold_start_user_cate_set:{}".format(user_id)
        self.reclist_redis_db.sadd(cate_id_set_redis_key, *self.group_to_cate_id_dict[group_id])

    def _judge_and_get_user_reverse_index(self, user_id, rec_type, age=None, gender=None):
        """判断当前用户是否存在倒排索引, 如果没有的话拷贝一份
        """
        if rec_type == 'hot_list':
            # 判断用户是否存在热门列表
            cate_id = self.cate_id_list[0] # 随机选择一个就行
            hot_list_user_key = "user_id_hot_list:{}:{}".format(str(user_id), cate_id)
            if self.reclist_redis_db.exists(hot_list_user_key) == 0:
                # 给用户拷贝一份每个类别的倒排索引
                for cate_id in self.cate_id_list:
                    cate_id_news_templete_key = "hot_list_news_cate:{}".format(cate_id)
                    hot_list_user_key = "user_id_hot_list:{}:{}".format(str(user_id), cate_id)
                    self.reclist_redis_db.zunionstore(hot_list_user_key, [cate_id_news_templete_key])
        elif rec_type == "cold_start":
             # 判断用户是否在冷启动列表中
             cate_id_set_redis_key = "cold_start_user_cate_set:{}".format(user_id)
             print("判断用户是否在冷启动列表中 {}".format(self.reclist_redis_db.exists(cate_id_set_redis_key)))
             if self.reclist_redis_db.exists(cate_id_set_redis_key) == 0:
                # 如果系统中没有当前用户的冷启动倒排索引, 那么就需要从冷启动模板中复制一份
                # 确定用户分组
                try:
                    group_id = self._get_register_user_group_id(age, gender)
                except:
                    return False
                print("group_id : {}".format(group_id))
                self._copy_cold_start_list_to_redis(user_id, group_id)
        else:
            pass 
        return True

    def _get_user_expose_set(self, user_id):
        """获取用户曝光列表
        """
        user_exposure_prefix = "user_exposure:"
        user_exposure_key = user_exposure_prefix + str(user_id)
        # 获取用户当前曝光列表
        if self.exposure_redis_db.exists(user_exposure_key) > 0:
            exposure_list = self.exposure_redis_db.smembers(user_exposure_key)
            news_expose_set = set(map(lambda x: x.split(':')[0], exposure_list))
        else:
            news_expose_set = set()
        return news_expose_set

    def _save_user_exposure(self, user_id, newslist):
        """记录用户曝光到redis"""
        if len(newslist) == 0: return False   # 无曝光数目

        ctime = str(round(time.time()*1000))  # 曝光时间戳
        key = "user_exposure:" + str(user_id)    # 为key拼接
        # 将历史曝光记录与newlist(最新曝光)的交集新闻提出来  并将该部分删除，防止重复存储曝光新闻
        exposure_news_set = self.exposure_redis_db.smembers(key)  # 历史曝光记录

        del_exposure_news = []   # 历史曝光记录与newlist(最新曝光)的交集新闻,需要删除
        if exposure_news_set.__len__() != 0:
            del_exposure_news = [item for item in exposure_news_set if item.split(":")[0] in newslist]  

        # 为曝光过的新闻拼接时间
        news_save = []
        for news_id in newslist:
            val = news_id+":"+ctime
            val = val.replace('"', "'" )  # 将双引号都替换成单引号
            news_save.append(val)
        
        # 存储redis
        try:
            if del_exposure_news.__len__() != 0:
                self.exposure_redis_db.srem(key,*del_exposure_news)
            self.exposure_redis_db.sadd(key,*news_save)
        except Exception as e:
            print(str(e))
            return False
        return True

    def _get_polling_rec_list(self, user_id, news_expose_set, cate_id_list, rec_type, one_page_news_cnt=10):
        """获取轮询的打散新闻列表
        """
        # 候选曝光列表
        exposure_news_list = []
        # 用户展示新闻列表
        user_news_list = []
        iter_cnt = 0
        # 给每个用户轮询每个类别的新闻，获取打散之后的新闻列表
        while len(user_news_list) != one_page_news_cnt:
            cate_id_index = iter_cnt % len(cate_id_list)
            cate_id = cate_id_list[cate_id_index]
            if rec_type == "hot_list":
                user_redis_key = "user_id_hot_list:{}:{}".format(str(user_id), cate_id) 
            elif rec_type == "cold_start":
                user_redis_key = "cold_start_user:{}:{}".format(str(user_id), cate_id)
            else:
                pass 
            cur_cate_cnt = 0
            while self.reclist_redis_db.zcard(user_redis_key) > 0:
                # 摘取排名第一的新闻
                news_id_and_cate = self.reclist_redis_db.zrevrange(user_redis_key, 0, 0)[0]
                news_id = news_id_and_cate.split('_')[1] # 将新闻id切分出来
                if news_id in news_expose_set:
                    # 将当前新闻id添加到待删除的新闻列表中
                    self.reclist_redis_db.zrem(user_redis_key, news_id_and_cate) 
                    continue
                # TODO 在数据入库的时候离线处理无法成功加载json的问题
                # 获取新闻详细信息, 由于爬取的新闻没有做清理，导致有些新闻无法转化成json的形式
                # 所以这里如果转化失败的内容也直接删除掉
                try:
                    news_info_dict = self.get_news_detail(news_id)
                    cur_cate_cnt += 1
                except Exception as e:  
                    # 删除无效的新闻
                    self.reclist_redis_db.zrem(user_redis_key, news_id_and_cate)                   
                    # 记录无效的新闻的id
                    with open(self.bad_case_news_log_path, "a+") as f:
                        f.write(news_id + "\n")
                        print("there are not news detail info for {}".format(news_id))
                    continue
                # 删除当前key
                self.reclist_redis_db.zrem(user_redis_key, news_id_and_cate) 
                # 判断当前类别的新闻是否摘取成功, 摘取成功的话就推出当前循环
                if cur_cate_cnt == 1:
                    # 将摘取成功的新闻信息添加到用户新闻列表中
                    user_news_list.append(news_info_dict)
                    exposure_news_list.append(news_id)
                    break
            iter_cnt += 1
        return user_news_list, exposure_news_list

    def get_cold_start_rec_list_v2(self, user_id, age=None, gender=None):
        """推荐页展示列表，使用轮询的方式进行打散
        """
        # 获取用户曝光列表
        news_expose_set = self._get_user_expose_set(user_id)
        
        # 判断用户是否存在冷启动列表中
        flag = self._judge_and_get_user_reverse_index(user_id, "cold_start", age, gender)

        if not flag:
            print("_judge_and_get_user_reverse_index fail")
            return []

        # 获取用户的cate id列表
        cate_id_set_redis_key = "cold_start_user_cate_set:{}".format(user_id)
        cate_id_list = list(self.reclist_redis_db.smembers(cate_id_set_redis_key))

        # 通过轮询的方式
        user_news_list, exposure_news_list = self._get_polling_rec_list(user_id, news_expose_set, cate_id_list, rec_type="cold_start")
        
        # 添加曝光内容
        self._save_user_exposure(user_id, exposure_news_list)
        return user_news_list

    def get_hot_list_v2(self, user_id):
        """热门页展示列表，使用轮询的方式进行打散
        """
        # 获取用户曝光列表
        news_expose_set = self._get_user_expose_set(user_id)

        # 判断用户是否存在热门列表
        self._judge_and_get_user_reverse_index(user_id, "hot_list")

        # 通过轮询的方式获取用户的展示列表
        user_news_list, exposure_news_list = self._get_polling_rec_list(user_id, news_expose_set, self.cate_id_list, rec_type="hot_list")

        # 添加曝光内容
        self._save_user_exposure(user_id, exposure_news_list)
        return user_news_list

    def get_news_detail(self, news_id):
        """获取新闻展示的详细信息
        """
        news_info_str = self.static_news_info_redis_db.get("static_news_detail:" + news_id)
        news_info_str = news_info_str.replace('\'', '\"' ) # 将单引号都替换成双引号
        news_info_dit = json.loads(news_info_str)
        news_dynamic_info_str = self.dynamic_news_info_redis_db.get("dynamic_news_detail:" + news_id)
        news_dynamic_info_str = news_dynamic_info_str.replace("'", '"' ) # 将单引号都替换成双引号
        news_dynamic_info_dit = json.loads(news_dynamic_info_str)
        for k in news_dynamic_info_dit.keys():
            news_info_dit[k] = news_dynamic_info_dit[k]
        return news_info_dit

    def update_news_dynamic_info(self, news_id,action_type):
        """更新新闻展示的详细信息
        """
        news_dynamic_info_str = self.dynamic_news_info_redis_db.get("dynamic_news_detail:" + news_id)
        news_dynamic_info_str = news_dynamic_info_str.replace("'", '"' ) # 将单引号都替换成双引号
        news_dynamic_info_dict = json.loads(news_dynamic_info_str)
        if len(action_type) == 2:
            if action_type[1] == "true":
                news_dynamic_info_dict[action_type[0]] +=1
            elif action_type[1] == "false":
                news_dynamic_info_dict[action_type[0]] -=1
        else:
            news_dynamic_info_dict["read_num"] +=1
        news_dynamic_info_str = json.dumps(news_dynamic_info_dict)
        news_dynamic_info_str = news_dynamic_info_str.replace('"', "'" )
        res = self.dynamic_news_info_redis_db.set("dynamic_news_detail:" + news_id, news_dynamic_info_str)
        return res

    def test(self):
        user_info = self.register_sql_sess.query(RegisterUser).filter(RegisterUser.userid == "4566566568405766145").first()
        print(user_info.age)


if __name__ == "__main__":
    # 测试单例模式
    oneline_server = OnlineServer()
    # oneline_server.get_hot_list("4563333734895456257")
    oneline_server.test()

```

### 2.2 推荐页列表构建

#### 2.2.1 业务流程
- 获取用户曝光列表，得到所有的新闻ID
- 针对新用户，从之前的离线推荐页列表中，为该用户生成一份推荐页列表，针对老用户，直接获取该用户的推荐页列表
- 对上述热门列表，每次选取10条新闻，进行页面展示
- 对已选取的10条新闻，更新曝光记录

#### 2.2.1 核心代码逻辑

代码位于`recprocess/online.py`

- `_get_user_expose_set()`方法：主要获取用户曝光列表，得到所有的新闻ID并存储在`Redis`

    ```python
     def _get_user_expose_set(self, user_id):
        """获取用户曝光列表
        """
        user_exposure_prefix = "user_exposure:"
        user_exposure_key = user_exposure_prefix + str(user_id)
        # 获取用户当前曝光列表
        if self.exposure_redis_db.exists(user_exposure_key) > 0:
            exposure_list = self.exposure_redis_db.smembers(user_exposure_key)
            news_expose_set = set(map(lambda x: x.split(':')[0], exposure_list))
        else:
            news_expose_set = set()
        return news_expose_set
    ```

- `_judge_and_get_user_reverse_index()`方法：用于判断用户是否存在冷启动列表，如果用户是新用户，获取分组ID，根据用户DI和分组ID，从Redis.`cold_start_group`中的数据，复制创建该用户的推荐列表

```python
    
     def _judge_and_get_user_reverse_index(self, user_id, rec_type, age=None, gender=None):
        """判断当前用户是否存在倒排索引, 如果没有的话拷贝一份
        """
        if rec_type == 'hot_list':
            # 判断用户是否存在热门列表
            cate_id = self.cate_id_list[0] # 随机选择一个就行
            hot_list_user_key = "user_id_hot_list:{}:{}".format(str(user_id), cate_id)
            if self.reclist_redis_db.exists(hot_list_user_key) == 0:
                # 给用户拷贝一份每个类别的倒排索引
                for cate_id in self.cate_id_list:
                    cate_id_news_templete_key = "hot_list_news_cate:{}".format(cate_id)
                    hot_list_user_key = "user_id_hot_list:{}:{}".format(str(user_id), cate_id)
                    self.reclist_redis_db.zunionstore(hot_list_user_key, [cate_id_news_templete_key])
        elif rec_type == "cold_start":
             # 判断用户是否在冷启动列表中
             cate_id_set_redis_key = "cold_start_user_cate_set:{}".format(user_id)
             print("判断用户是否在冷启动列表中 {}".format(self.reclist_redis_db.exists(cate_id_set_redis_key)))
             if self.reclist_redis_db.exists(cate_id_set_redis_key) == 0:
                # 如果系统中没有当前用户的冷启动倒排索引, 那么就需要从冷启动模板中复制一份
                # 确定用户分组
                try:
                    group_id = self._get_register_user_group_id(age, gender)
                except:
                    return False
                print("group_id : {}".format(group_id))
                self._copy_cold_start_list_to_redis(user_id, group_id)
        else:
            pass 
        return True


 ```
    将用户当前的新闻类别标识，存放到`cold_start_user_cate_set`中，具体格式如下：
    ```
    cold_start_user_cate_set:<用户ID>: {<新闻ID>}
    ```

- `_get_polling_rec_list()`方法：通过轮询方式获取用户的展示列表，每次只取出10条新闻；通过while循环方式，从Redis[0]的`cold_start_user:<用户ID>:<新闻分类标识>`中选取新闻，之后删除已选取的新闻，并把选取的10条新闻内容放到用户新闻（`user_news_list`）数组中，新闻ID放到曝光列表（`exposure_news_list`）中。

```python
 def _get_polling_rec_list(self, user_id, news_expose_set, cate_id_list, rec_type, one_page_news_cnt=10):
        """获取轮询的打散新闻列表
        """
        # 候选曝光列表
        exposure_news_list = []
        # 用户展示新闻列表
        user_news_list = []
        iter_cnt = 0
        # 给每个用户轮询每个类别的新闻，获取打散之后的新闻列表
        while len(user_news_list) != one_page_news_cnt:
            cate_id_index = iter_cnt % len(cate_id_list)
            cate_id = cate_id_list[cate_id_index]
            if rec_type == "hot_list":
                user_redis_key = "user_id_hot_list:{}:{}".format(str(user_id), cate_id) 
            elif rec_type == "cold_start":
                user_redis_key = "cold_start_user:{}:{}".format(str(user_id), cate_id)
            else:
                pass 
            cur_cate_cnt = 0
            while self.reclist_redis_db.zcard(user_redis_key) > 0:
                # 摘取排名第一的新闻
                news_id_and_cate = self.reclist_redis_db.zrevrange(user_redis_key, 0, 0)[0]
                news_id = news_id_and_cate.split('_')[1] # 将新闻id切分出来
                if news_id in news_expose_set:
                    # 将当前新闻id添加到待删除的新闻列表中
                    self.reclist_redis_db.zrem(user_redis_key, news_id_and_cate) 
                    continue
                # TODO 在数据入库的时候离线处理无法成功加载json的问题
                # 获取新闻详细信息, 由于爬取的新闻没有做清理，导致有些新闻无法转化成json的形式
                # 所以这里如果转化失败的内容也直接删除掉
                try:
                    news_info_dict = self.get_news_detail(news_id)
                    cur_cate_cnt += 1
                except Exception as e:  
                    # 删除无效的新闻
                    self.reclist_redis_db.zrem(user_redis_key, news_id_and_cate)                   
                    # 记录无效的新闻的id
                    with open(self.bad_case_news_log_path, "a+") as f:
                        f.write(news_id + "\n")
                        print("there are not news detail info for {}".format(news_id))
                    continue
                # 删除当前key
                self.reclist_redis_db.zrem(user_redis_key, news_id_and_cate) 
                # 判断当前类别的新闻是否摘取成功, 摘取成功的话就推出当前循环
                if cur_cate_cnt == 1:
                    # 将摘取成功的新闻信息添加到用户新闻列表中
                    user_news_list.append(news_info_dict)
                    exposure_news_list.append(news_id)
                    break
            iter_cnt += 1
        return user_news_list, exposure_news_list

```

- `_save_user_exposure()`方法：将曝光新闻数据存储到Redis[3]中；设置曝光时间，删除重复的曝光新闻，并按照下列格式存储到Redis[3]的`user_exposure`中：

```python
        def _save_user_exposure(self, user_id, newslist):
        """记录用户曝光到redis"""
        if len(newslist) == 0: return False   # 无曝光数目

        ctime = str(round(time.time()*1000))  # 曝光时间戳
        key = "user_exposure:" + str(user_id)    # 为key拼接
        # 将历史曝光记录与newlist(最新曝光)的交集新闻提出来  并将该部分删除，防止重复存储曝光新闻
        exposure_news_set = self.exposure_redis_db.smembers(key)  # 历史曝光记录

        del_exposure_news = []   # 历史曝光记录与newlist(最新曝光)的交集新闻,需要删除
        if exposure_news_set.__len__() != 0:
            del_exposure_news = [item for item in exposure_news_set if item.split(":")[0] in newslist]  

        # 为曝光过的新闻拼接时间
        news_save = []
        for news_id in newslist:
            val = news_id+":"+ctime
            val = val.replace('"', "'" )  # 将双引号都替换成单引号
            news_save.append(val)
        
        # 存储redis
        try:
            if del_exposure_news.__len__() != 0:
                self.exposure_redis_db.srem(key,*del_exposure_news)
            self.exposure_redis_db.sadd(key,*news_save)
        except Exception as e:
            print(str(e))
            return False
        return True
```


## 参考资料：

1. https://relph1119.github.io/my-team-learning/#/recommender_system32/task05

