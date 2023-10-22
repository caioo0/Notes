# Task01 推荐系统流程的构建
---

（本学习笔记来源于DataWhale-12月组队学习：[推荐系统实战](https://github.com/datawhalechina/fun-rec)，[直播视频地址](https://datawhale.feishu.cn/minutes/obcnzns778b725r5l535j32o)） ,

```md
环境：window 10 + wsl (ubuntu 20.04)
```
新闻推荐系统流程构建包括offline和online部分； 按照展示形式分为前端展示页面和后端服务端部分；

![](http://ryluo.oss-cn-chengdu.aliyuncs.com/图片Untitled.png)

## 1. offline
基于存储好的物料画像和用户画像进行离线计算， 为每个用户提供一个热门页列表和推荐页列表并进行缓存， 方便online服务的列表获取。

### 热门页列表

**离线热门页定义：**
- 文章发布时间和用户对它的行为记录(获得的点赞数，收藏数和阅读数)计算文章热度
- 根据热度排序得到文章画像的动静态信息，按天更新存入`redis`
代码实现:
  
```python
      """获取物料的点赞，收藏和创建时间等信息，计算热度并生成热度推荐列表存入redis
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

          #print(news_id, news_cate, news_ctime, news_likes_num, news_collections_num, news_read_num, news_hot_value)

          # 时间转换与计算时间差   前提要保证当前时间大于新闻创建时间，目前没有捕捉异常
          news_ctime_standard = datetime.strptime(news_ctime, "%Y-%m-%d %H:%M")
          cur_time_standard = datetime.now()
          time_day_diff = (cur_time_standard - news_ctime_standard).days
          time_hour_diff = (cur_time_standard - news_ctime_standard).seconds / 3600

          # 只要最近3天的内容
          if time_day_diff > 3:
              continue
          
          # 计算热度分，这里使用魔方秀热度公式， 可以进行调整, read_num 上一次的 hot_value  上一次的hot_value用加？  因为like_num这些也都是累加上来的， 所以这里计算的并不是增值，而是实时热度吧
          # news_hot_value = (news_likes_num * 6 + news_collections_num * 3 + news_read_num * 1) * 10 / (time_hour_diff+1)**1.2
          # 72 表示的是3天，
          news_hot_value = (news_likes_num * 0.6 + news_collections_num * 0.3 + news_read_num * 0.1) * 10 / (1 + time_hour_diff / 72) 

          #print(news_likes_num, news_collections_num, time_hour_diff)

          # 更新物料池的文章hot_value
          item['hot_value'] = news_hot_value
          self.feature_protrail_collection.update({'news_id':news_id}, item)

          #print("news_hot_value: ", news_hot_value)

          # 保存到redis中
          self.reclist_redis.zadd('hot_list', {'{}_{}'.format(news_cate, news_id): news_hot_value}, nx=True)
  ```

### 推荐页列表

**离线推荐页**

根据新老用户，分为冷启动和个性化推荐页面

- 冷启动： 是针对新用户，根据用户基本画像信息（年龄，性别），结合文章热度推荐相似用户推荐列表，实现代码：

```python
def generate_cold_start_news_list_to_redis_for_register_user(self):
        """给已经注册的用户制作冷启动新闻列表
        """
        for user_info in self.register_user_sess.query(RegisterUser).all():
            if int(user_info.age) < 23 and user_info.gender == "female":
                redis_key = "cold_start_group:{}".format(str(1))
                self.copy_redis_sorted_set(user_info.userid, redis_key)
            elif int(user_info.age) >= 23 and user_info.gender == "female":
                redis_key = "cold_start_group:{}".format(str(2))
                self.copy_redis_sorted_set(user_info.userid, redis_key)
            elif int(user_info.age) < 23 and user_info.gender == "male":
                redis_key = "cold_start_group:{}".format(str(3))
                self.copy_redis_sorted_set(user_info.userid, redis_key)
            elif int(user_info.age) >= 23 and user_info.gender == "male":
                redis_key = "cold_start_group:{}".format(str(4))
                self.copy_redis_sorted_set(user_info.userid, redis_key)
            else:
                pass 
        print("generate_cold_start_news_list_to_redis_for_register_user.")
        
```

- 个性化：针对老用户，根据推荐流程进行个性化推荐（召回→排序→重排→个性化）生成列表；



## 2. online
online: 为用户在使用APP或者系统的过程中触发的行为获取推荐列表，获取热门页列表（新用户和老用户推荐的内容有所区别）

- 获取推荐页列表
  - 新用户：从离线存储好的冷启动列表中读取推荐列表，进行曝光去重和更新曝光记录
  - 老用户：从离线存储好的个性化列表读取推荐列表，同样进行曝光去重和更新曝光记录
  
- 获取热门列表
  - 新用户：从离线存储好的冷启动列表中读取热门列表，进行曝光去重和更新曝光记录
  - 老用户：从离线存储好的个性化列表读取热门列表，同样进行曝光去重和更新曝光记录

部分实现代码：

```python
def get_hot_list(self, user_id):
        """热门页列表结果"""
        hot_list_key_prefix = "user_id_hot_list:"
        hot_list_user_key = hot_list_key_prefix + str(user_id)

        user_exposure_prefix = "user_exposure:"
        user_exposure_key = user_exposure_prefix + str(user_id)

        # 当数据库中没有这个用户的数据，就从热门列表中拷贝一份 
        if self.reclist_redis_db.exists(hot_list_user_key) == 0: # 存在返回1，不存在返回0
            print("copy a hot_list for {}".format(hot_list_user_key))
            # 给当前用户重新生成一个hot页推荐列表， 也就是把hot_list里面的列表复制一份给当前user， key换成user_id
            self.reclist_redis_db.zunionstore(hot_list_user_key, ["hot_list"])

        # 一页默认10个item, 但这里候选20条，因为有可能有的在推荐页曝光过
        article_num = 200

        # 返回的是一个news_id列表   zrevrange排序分值从大到小
        candiate_id_list = self.reclist_redis_db.zrevrange(hot_list_user_key, 0, article_num-1)

        if len(candiate_id_list) > 0:
            # 根据news_id获取新闻的具体内容，并返回一个列表，列表中的元素是按照顺序展示的新闻信息字典
            news_info_list = []
            selected_news = []   # 记录真正被选了的
            cou = 0

            # 曝光列表
            print("self.reclist_redis_db.exists(key)",self.exposure_redis_db.exists(user_exposure_key))
            if self.exposure_redis_db.exists(user_exposure_key) > 0:
                exposure_list = self.exposure_redis_db.smembers(user_exposure_key)
                news_expose_list = set(map(lambda x: x.split(':')[0], exposure_list))
            else:
                news_expose_list = set()

            for i in range(len(candiate_id_list)):
                candiate = candiate_id_list[i]
                news_id = candiate.split('_')[1]

                # 去重曝光过的，包括在推荐页以及hot页
                if news_id in news_expose_list:
                    continue

                # TODO 有些新闻可能获取不到静态的信息，这里应该有什么bug
                # bug 原因是，json.loads() redis中的数据会报错，需要对redis中的数据进行处理
                # 可以在物料处理的时候过滤一遍，json无法load的新闻
                try:
                    news_info_dict = self.get_news_detail(news_id)
                except Exception as e:
                    with open("/home/recsys/news_rec_server/logs/news_bad_cases.log", "a+") as f:
                        f.write(news_id + "\n")
                        print("there are not news detail info for {}".format(news_id))
                    continue
                # 需要确认一下前端接收的json，key需要是单引号还是双引号
                news_info_list.append(news_info_dict)
                news_expose_list.add(news_id)
                # 注意，原数的key中是包含了类别信息的
                selected_news.append(candiate)
                cou += 1
                if cou == 10:
                    break
            
            if len(selected_news) > 0:
                # 手动删除读取出来的缓存结果, 这个很关键, 返回被删除的元素数量，用来检测是否被真的被删除了
                removed_num = self.reclist_redis_db.zrem(hot_list_user_key, *selected_news)
                print("the numbers of be removed:", removed_num)

            # 曝光重新落表
            self._save_user_exposure(user_id,news_expose_list)
            return news_info_list 
        else:
            #TODO 临时这么做，这么做不太好
            self.reclist_redis_db.zunionstore(hot_list_user_key, ["hot_list"])
            print("copy a hot_list for {}".format(hot_list_user_key))
            # 如果是把所有内容都刷完了再重新拷贝的数据，还得记得把今天的曝光数据给清除了
            self.exposure_redis_db.delete(user_exposure_key)
            return  self.get_hot_list(user_id)
```

## 3. 后端交互响应


具体功能实现代码见`server.py`，服务端执行页面是同一个文件;

- 注册调用函数：`register()`
- 登录调用函数：`login()`
- 推荐列表调用函数：`rec_list()`
- 热门列表调用函数：`hot_list()`
- 具体新闻内容调用函数：`news_detail()`
- 用户行为调用函数(阅读,喜欢和收藏）：`actions()`


## 4. 前端交互请求

### 4.1 注册页面

调用接口：http://127.0.0.1:5000/recsys/register
参考请求参数：
```json
{
	"username": "admin",
	"passwd": "admin",
	"passwd2": "admin",
	"city": "TianJin",
	"age": "22",
	"gender": "male"
}
```

响应成功参数:
```json
{
	"code": 200,
	"msg": "action success"
}
```


### 4.2 登录页面

调用接口：http://127.0.0.1:5000/recsys/login  
请求参数：

```json
{
  "username": "*",
  "passwd": "*"
}
```


响应成功参数:
```json
{
	"code": 200,
	"msg": "action success"
}
```


### 4.3 推荐列表

调用接口：Request URL: http://127.0.0.1:5000/recsys/rec_list?user_id=choi  
响应参数：
```json
{
"code": 200,
"data": [
{
"cate": "体育",
"collections": 0,
"content": "据《每日体育报》报道，在被问及弗伦基·德容的未来去向时，他的父亲没有关闭任何大门，尽管他现在不认为德容会离开。德容的父亲表示：“我知道巴萨需要钱，对弗伦基的一份大报价可能会对巴萨有帮助，但我认为这不会发生。”德容的父亲补充说，欧洲豪门对他的儿子的兴趣确实存在：“然而，欧洲最好的5家俱乐部都给他打过电话。”《每日体育报》表示，德容的父亲病没有排除儿子离开巴萨的可能性，最近德容遇到一些问题，表现不佳，为此他遭受了媒体和球迷的批评。（伊万）",
"ctime": "2021-12-14 09:26",
"likes": 0,
"news_id": "f32791e6-f350-413c-b83d-056f4a129f80",
"read_num": 0,
"title": "德容父亲：欧洲5家最好的俱乐部都联系过我儿子",
"url": "https://sports.sina.com.cn/g/laliga/2021-12-14/doc-ikyakumx4013333.shtml"
},
{
"cate": "国内",
"collections": 0,
"content": "原标题：教育部：成立全国学校食品安全与营养健康工作专家组据教育部网站12月14日消息，教育部办公厅发布关于成立全国学校食品安全与营养健康工作专家组的通知。为贯彻落实《教育部办公厅市场监管总局办公厅国家卫生健康委办公厅关于加强学校食堂卫生安全与营养健康管理工作的通知》（教体艺厅函〔2021〕38号），进一步加强学校食品安全与营养健康管理，发挥专家对学校食品安全与营养健康工作的咨询、研究、评估、指导、宣教等作用，教育部决定组建全国学校食品安全与营养健康工作专家组（以下简称专家组）。专家组是在教育部领导下，对全国学校食品安全与营养健康工作发挥咨询、研究、评估、指导、宣教等作用的专家组织。主要职责是指导全国学校开展食品安全与营养健康工作，组织开展学校食品安全与营养健康研究，就学校食品安全与营养健康相关问题向教育部提出专业、科学的咨询意见和建议。专家组专家共61人，聘期4年，自2021年11月起至2025年11月止。专家组设组长1人，副组长4人。专家组的工作由组长主持，副组长协助。组长单位为中国农业大学，请中国农业大学为专家组工作提供有力支持。各地要积极支持专家组的工作，专家组成员所在单位应为专家提供参加专家组工作的必要保障。责任编辑：贾楠SN245",
"ctime": "2021-12-14 17:17",
"likes": 0,
"news_id": "ab7f0e47-c981-4813-82c0-04fab58f8309",
"read_num": 0,
"title": "教育部：成立全国学校食品安全与营养健康工作专家组",
"url": "https://news.sina.com.cn/c/2021-12-14/doc-ikyamrmy8937338.shtml"
}
],
"msg": "request rec_list success.",
"user_id": 4568708059086459000
}
```

### 4.4 热门列表

  调用接口：http://127.0.0.1:5000/recsys/hot_list?user_id=choi  
  响应参数：
```json
{
  "code": 200,
  "data": [
    {
      "cate": "国内",
      "collections": 0,
      "content": "原标题：林郑月娥：香港计划明年1月开始扩大第三剂疫苗接种据香港电台网站12月14日报道，香港特区政府行政长官林郑月娥表示，计划在明年1月初开始，扩大复必泰疫苗第三剂接种计划。她说，已指示食物及卫生局，为所有市民接种第三剂疫苗作准备，不再局限于高风险群组接种，而是容许所有达合格年龄，以及已接种首两针复必泰的人士已相隔一段时间的人士，都可以打第三针，详细安排有待专家在两个联合科学委员会尽快开会决定。责任编辑：贾楠SN245",
      "ctime": "2021-12-14 13:29",
      "likes": 0,
      "news_id": "8dc17da0-10f8-4e31-ab41-0c92e7b8facc",
      "read_num": 0,
      "title": "林郑月娥：香港计划明年1月开始扩大第三剂疫苗接种",
      "url": "https://news.sina.com.cn/c/2021-12-14/doc-ikyamrmy8892116.shtml"
    },
    {
      "cate": "国际",
      "collections": 0,
      "content": "原标题：印度近万名儿童在疫情期间成为孤儿超500人被遗弃印度全国儿童权利保护委员会近日表示，2020年4月至2021年12月的新冠疫情期间，印度有近万名儿童成为孤儿，13.2万名儿童至少失去了一位双亲。据《今日印度》13日报道，印度最高法院日前审理了一起案件，涉及因失去父母一方或双方而受到新冠疫情不利影响的儿童，而印度儿童权利保护委员会提供的一份证词中显示了重要信息。该委员会指出，从2020年4月起至2021年12月7日，已有9855名印度儿童成为孤儿，132113名儿童失去了父母中的一方，此外还有508名儿童被遗弃。印度最高法院方面还表示，识别受到新冠疫情不利影响的流浪儿童过程缓慢，并称各邦和联邦直辖区应立即采取措施发现这些儿童，并让他们得到帮助。有法官表示，印度可能有“数十万儿童流落街头”。责任编辑：张建利",
      "ctime": "2021-12-14 11:14",
      "likes": 0,
      "news_id": "9dd67403-ba81-43df-a4c5-352614adf4c3",
      "read_num": 0,
      "title": "印度近万名儿童在疫情期间成为孤儿 超500人被遗弃",
      "url": "https://news.sina.com.cn/w/2021-12-14/doc-ikyamrmy8867052.shtml"
    },
    {
      "cate": "社会",
      "collections": 0,
      "content": "原标题：张玉宁头球绝杀广州队新外援前锋首秀有点“懵”13日晚，北京国安在中超第二阶段争冠组首轮比赛中迎来了和老对手广州队的争夺，凭借张玉宁在第83分钟的头球破门，国安1比0绝杀对手取得开门红。虽然成功拿到3分，但比赛中国安攻击型球员暴露出门前把握机会的能力有限的弱点，新外援安德森·席尔瓦首秀也有点“懵”。京穗大战向来都是足够吸引人眼球的，不过由于广州队在过去一段时间里经历了不小的人员变动，此番来到赛区的球队阵容并不完整，被动实现了全华班。而像蒋光太和张琳芃这样的绝对主力，本场比赛也没进入到大名单中，因此广州队的实力受到了不小的影响。比赛开始仅仅35秒，国安就制造了第一个角球，安德森·席尔瓦在这次进攻中完成了个人在中超比赛中的首次射门，可惜葡萄牙人的头球攻门被对手后卫化解。在短短5分钟之后，这位巴西外援在对手半区得球后长驱直入，可惜的是，他的左脚打门偏出了近门柱。广州队在适应了国安的节奏之后，表现得越来越好，尤其是边路的韦世豪和杨立瑜，两人一左一右的突破内切给国安的后防线造成了一定的威胁。上半时的后半段，虽然双方互有攻守，但实际上还是广州队踢得更加积极主动一些，或许和国安队员相比，广州球员“生存”的压力更大，也更想通过比赛来表现自己，为将来赢得机会。易边再战之后，双方在场上的身体接触更多，国安的高天意和李磊相继因为动作过大而遭到黄牌警告，比赛的节奏瞬间加快。而广州队则利用直接任意球的机会由廖力生威胁了国安的球门，好在侯森注意力集中，化解了对手的这次质量很高的射门。比赛第60分钟，国安同样利用一次定位球机会创造了机会，可惜的是，张稀哲的传球虽然找到了禁区内的张玉宁，但国安9号却未能真正完成头球攻门，他的微微一蹭没有改变皮球的方向，这也是国安最接近破门的一次良机。之后的两次进攻，李磊的大力射门被刘殿座拒之门外、安德森·席尔瓦则面对空门不进，国安短时间内对广州队形成了围攻，但却总是距离得分差那么一点点。最后15分钟，国安对于广州队实现了完全的压制，基本把对手压在本方防守30米区域内，张稀哲一度为队友送出不错的传球，但可惜的是，池忠国的射门虽然力量十足，但却因为角度太正被对手门将没收。直到第82分钟，狂攻了一场的国安终于迎来了进球，张玉宁在角球战术中前点头球一蹭破门。1比0的比分保持到了终场，国安如愿拿下这场京穗德比战的胜利，为这个阶段的中超联赛开了个好头。责任编辑：祝加贝",
      "ctime": "2021-12-14 00:42",
      "likes": 0,
      "news_id": "9b8d9612-6798-4211-a4c3-27b6ccff4741",
      "read_num": 0,
      "title": "张玉宁头球绝杀广州队 新外援前锋首秀有点“懵”",
      "url": "https://news.sina.com.cn/s/2021-12-14/doc-ikyamrmy8781547.shtml"
    }
  ],
  "msg": "request hot_list success.",
  "user_id": 4568708059086459000
}
```

### 4.5 文章详情页面

**4.5.1 获取文章详情页面**

调用接口：http://127.0.0.1:5000/recsys/news_detail?news_id=e6ffa001-676d-425d-8a5a-20602b158e2f&user_name=choi   
响应参数：

```json
{
"code": 0,
"data": {
"cate": "科技",
"collections": false,
"content": "近日，有媒体曝光称，两家门店存在使用过期食材等问题，引发舆论热议。又一家大品牌的问题曝光在了媒体卧底下，这不禁让人疑问，为何头部企业也经不起食品安全卧底？媒体卧底报道指出，涉事星巴克门店的食材过期后仍继续用，部分产品被人为篡改保质期。12月13日晚间，星巴克中国发布声明称，经过调查，涉事门店确实存在营运操作上的违规行为，已闭店进行调查与整改，同时，中国内地所有星巴克门店将立即启动食品安全标准执行情况的全面自查。无锡市场监管部门12月13日表示，初步核实涉事门店有更改食品原料内控期限标识、使用超过内控期限原料的行为，已责成涉事门店停业整改。市场监管部门同步对其他82家星巴克门店开展排查，发现从业人员未戴工作帽、加工区物品摆放零乱、消毒记录不全等15处问题，均已责令整改。无锡市场监管部门对星巴克进行了行政约谈，要求公司对存在的食品安全问题进行全面自查、落实整改。从胖哥俩、奈雪的茶到海底捞，餐饮行业的连锁大品牌们不仅是行业内看齐的对象，也是消费者心中的“金字招牌”。然而，这些头部企业却未能经得起媒体卧底监督，被发现存在多重食品安全问题，令人咋舌。食品安全是企业不能触碰的底线。这个道理，适用于所有的餐饮企业。对头部企业来说，更应该在公众的“放大镜”下，谨小慎微，认认真真抓好食品安全问题，履行对消费者的承诺，避免“动作走形”。",
"ctime": "2021-12-14 16:28",
"likes": false,
"news_id": "e6ffa001-676d-425d-8a5a-20602b158e2f",
"read_num": 1,
"title": "半月谈评星巴克事件：头部品牌为何经不起食品安全卧底？",
"url": "https://finance.sina.com.cn/tech/2021-12-14/doc-ikyakumx4115536.shtml"
},
"msg": "request news_detail success."
}
```

**4.5.2 喜欢&收藏文章**

调用接口：http://127.0.0.1:5000/recsys/action  
请求参数： 

- 喜欢: `"action_type": "likes:true"`
- 取消喜欢：`"action_type": "likes:false"`
- 收藏：`"action_type": "collections:true"`
- 取消收藏：`"action_type": "collections:false"`
```json
{
"user_name": "choi",
"news_id": "e6ffa001-676d-425d-8a5a-20602b158e2f",
"action_time": 1639559716179,
"action_type": "likes:false"
}
```

响应成功参数:
```json
{
	"code": 200,
	"msg": "action success"
}
```


  

## 参考资料
[1]. https://zhuanlan.zhihu.com/p/76349679
