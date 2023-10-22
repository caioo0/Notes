# Torch-Rechub Tutorial：Milvus

- 场景：召回
- 数据：MovieLens-1M

- 本教程包括以下内容：
    1. 安装并启动milvus服务
    2. 使用milvus进行召回


## 什么是milvus?

Milvus 是一款云原生向量数据库，它具备高可用、高性能、易拓展的特点，用于海量向量数据的实时召回。

Milvus 基于 FAISS、Annoy、HNSW 等向量搜索库构建，核心是解决稠密向量相似度检索的问题。
在向量检索库的基础上，Milvus 支持数据分区分片、数据持久化、增量数据摄取、标量向量混合查询、time travel 等功能，
同时大幅优化了向量检索的性能，可满足任何向量检索场景的应用需求。
通常，建议用户使用 Docker 部署 Milvus，以获得最佳可用性和弹性。

Milvus 采用共享存储架构，存储计算完全分离，计算节点支持横向扩展。
从架构上来看，Milvus 遵循数据流和控制流分离，整体分为了四个层次，分别为接入层（access layer）、协调服务（coordinator service）、执行节点（worker node）和存储层（storage）。各个层次相互独立，独立扩展和容灾。

### 前置条件
1. 安装docker，可以参考https://www.runoob.com/docker/ubuntu-docker-install.html
2. 安装docker-compose，可以参考https://www.runoob.com/docker/docker-compose.html



```python
#安装milvus https://milvus.io/docs/install_standalone-docker.md
#下载docker-compose配置文件
!wget https://github.com/milvus-io/milvus/releases/download/v2.2.2/milvus-standalone-docker-compose.yml -O docker-compose.yml
#启动milvus docker镜像
!sudo docker-compose up -d
#检查milvus状态
!sudo docker-compose ps
#关闭milvus docker镜像
# !sudo docker-compose down

```


```python
#安装pymilvus
!pip install pymilvus
```

至此安装已经完成（本文使用版本为---milvus2.2.2,pymilvus2.2.0），下面我们来使用milvus进行召回。

## 使用milvus进行召回


```python
import torch
import pandas as pd
import numpy as np
import os
pd.set_option('display.max_rows',500)
pd.set_option('display.max_columns',500)
pd.set_option('display.width',1000)
torch.manual_seed(2022)
```




    <torch._C.Generator at 0x7f83656c8210>



### MovieLens数据集
- MovieLens数据集是电影网站提供的一份数据集，[原数据](https://grouplens.org/datasets/movielens/1m/)分为三个文件，users.dat movies.dat ratings.dat，包含了用户信息、电影信息和用户对电影的评分信息。

- 提供原始数据处理之后（参考examples/matching/data/ml-1m/preprocess_ml.py），全量数据集[**ml-1m.csv**](https://cowtransfer.com/s/5a3ab69ebd314e)

- 采样后的**ml-1m_sample.csv**(examples/matching/data/ml-1m/ml-1m_sample.csv)，是在全量数据中取出的前100个样本，调试用。在大家用ml-1m_sample.csv跑通代码后，便可以下载全量数据集测试效果，共100万个样本。


```python
# sample中只有两个用户
file_path = '../examples/matching/data/ml-1m/ml-1m_sample.csv'
data = pd.read_csv(file_path)
print(data.head())
```

       user_id  movie_id  rating  timestamp                                   title                        genres gender  age  occupation    zip
    0        1      1193       5  978300760  One Flew Over the Cuckoo's Nest (1975)                         Drama      F    1          10  48067
    1        1       661       3  978302109        James and the Giant Peach (1996)  Animation|Children's|Musical      F    1          10  48067
    2        1       914       3  978301968                     My Fair Lady (1964)               Musical|Romance      F    1          10  48067
    3        1      3408       4  978300275                  Erin Brockovich (2000)                         Drama      F    1          10  48067
    4        1      2355       5  978824291                    Bug's Life, A (1998)   Animation|Children's|Comedy      F    1          10  48067
    

### 在MovieLens-1M数据集上数据集训练一个DSSM模型

[DSSM 论文链接](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/cikm2013_DSSM_fullversion.pdf)

#### 特征预处理
在本DSSM模型中，我们使用两种类别的特征，分别是稀疏特征（SparseFeature）和序列特征（SequenceFeature）。

- 对于稀疏特征，是一个离散的、有限的值（例如用户ID，一般会先进行LabelEncoding操作转化为连续整数值），模型将其输入到Embedding层，输出一个Embedding向量。

- 对于序列特征，每一个样本是一个List[SparseFeature]（一般是观看历史、搜索历史等），对于这种特征，默认对于每一个元素取Embedding后平均，输出一个Embedding向量。此外，除了平均，还有拼接，最值等方式，可以在pooling参数中指定。

- 框架还支持稠密特征（DenseFeature），即一个连续的特征值（例如概率），这种类型一般需归一化处理。但是本样例中未使用。

以上三类特征的定义在`torch_rechub/basic/features.py`


```python
# 处理genres特征，取出其第一个作为标签
data["cate_id"] = data["genres"].apply(lambda x: x.split("|")[0])

# 指定用户列和物品列的名字、离散和稠密特征，适配框架的接口
user_col, item_col = "user_id", "movie_id"
sparse_features = ['user_id', 'movie_id', 'gender', 'age', 'occupation', 'zip', "cate_id"]
dense_features = []
```


```python
save_dir = '../examples/ranking/data/ml-1m/saved/'
if not os.path.exists(save_dir):
    os.makedirs(save_dir)
# 对SparseFeature进行LabelEncoding
from sklearn.preprocessing import LabelEncoder
print(data[sparse_features].head())
feature_max_idx = {}
for feature in sparse_features:
    lbe = LabelEncoder()
    data[feature] = lbe.fit_transform(data[feature]) + 1
    feature_max_idx[feature] = data[feature].max() + 1
    if feature == user_col:
        user_map = {encode_id + 1: raw_id for encode_id, raw_id in enumerate(lbe.classes_)}  #encode user id: raw user id
    if feature == item_col:
        item_map = {encode_id + 1: raw_id for encode_id, raw_id in enumerate(lbe.classes_)}  #encode item id: raw item id
np.save(save_dir+"raw_id_maps.npy", (user_map, item_map))  # evaluation时会用到
print('LabelEncoding后：')
print(data[sparse_features].head())
```

       user_id  movie_id gender  age  occupation    zip    cate_id
    0        1      1193      F    1          10  48067      Drama
    1        1       661      F    1          10  48067  Animation
    2        1       914      F    1          10  48067    Musical
    3        1      3408      F    1          10  48067      Drama
    4        1      2355      F    1          10  48067  Animation
    LabelEncoding后：
       user_id  movie_id  gender  age  occupation  zip  cate_id
    0        1        32       1    1           1    1        7
    1        1        17       1    1           1    1        3
    2        1        22       1    1           1    1        8
    3        1        91       1    1           1    1        7
    4        1        66       1    1           1    1        3
    

#### 用户塔与物品塔
在DSSM中，分为用户塔和物品塔，每一个塔的输出是用户/物品的特征拼接后经过MLP（多层感知机）得到的。
下面我们来定义物品塔和用户塔都有哪些特征：


```python
# 定义两个塔对应哪些特征
user_cols = ["user_id", "gender", "age", "occupation", "zip"]
item_cols = ['movie_id', "cate_id"]

# 从data中取出相应的数据
user_profile = data[user_cols].drop_duplicates('user_id')
item_profile = data[item_cols].drop_duplicates('movie_id')
print(user_profile.head())
print(item_profile.head())
from torch_rechub.utils.match import generate_seq_feature_match, gen_model_input
df_train, df_test = generate_seq_feature_match(data,
                                               user_col,
                                               item_col,
                                               time_col="timestamp",
                                               item_attribute_cols=[],
                                               sample_method=1,
                                               mode=0,
                                               neg_ratio=3,
                                               min_item=0)
print(df_train.head())
x_train = gen_model_input(df_train, user_profile, user_col, item_profile, item_col, seq_max_len=50)
y_train = x_train["label"]
x_test = gen_model_input(df_test, user_profile, user_col, item_profile, item_col, seq_max_len=50)
y_test = x_test["label"]
print({k: v[:3] for k, v in x_train.items()})
```

        user_id  gender  age  occupation  zip
    0         1       1    1           1    1
    53        2       2    2           2    2
       movie_id  cate_id
    0        32        7
    1        17        3
    2        22        8
    3        91        7
    4        66        3
    preprocess data
    

    generate sequence features: 100%|██████████| 2/2 [00:00<00:00, 1328.15it/s]

    n_train: 384, n_test: 2
    0 cold start user droped 
       user_id  movie_id                                      hist_movie_id  histlen_movie_id  label
    0        2        16        [35, 37, 43, 32, 78, 36, 34, 92, 3, 79, 86]                11      0
    1        1        18  [87, 51, 25, 41, 65, 53, 91, 34, 74, 32, 5, 18...                29      0
    2        2        40            [35, 37, 43, 32, 78, 36, 34, 92, 3, 79]                10      0
    3        1        64  [87, 51, 25, 41, 65, 53, 91, 34, 74, 32, 5, 18...                51      0
    4        1        39  [87, 51, 25, 41, 65, 53, 91, 34, 74, 32, 5, 18...                34      0
    {'user_id': array([2, 1, 2]), 'movie_id': array([16, 18, 40]), 'hist_movie_id': array([[ 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
             0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
             0,  0,  0,  0,  0,  0,  0, 35, 37, 43, 32, 78, 36, 34, 92,  3,
            79, 86],
           [ 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
             0,  0,  0,  0,  0, 87, 51, 25, 41, 65, 53, 91, 34, 74, 32,  5,
            18, 23, 14, 70, 55, 58, 82, 24, 28, 56, 57,  4, 26, 29, 22, 42,
            73, 71],
           [ 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
             0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
             0,  0,  0,  0,  0,  0,  0,  0, 35, 37, 43, 32, 78, 36, 34, 92,
             3, 79]]), 'histlen_movie_id': array([11, 29, 10]), 'label': array([0, 0, 0]), 'gender': array([2, 1, 2]), 'age': array([2, 1, 2]), 'occupation': array([2, 1, 2]), 'zip': array([2, 1, 2]), 'cate_id': array([1, 3, 2])}
    

    
    


```python
#定义特征类型

from torch_rechub.basic.features import SparseFeature, SequenceFeature
user_features = [
    SparseFeature(feature_name, vocab_size=feature_max_idx[feature_name], embed_dim=16) for feature_name in user_cols
]
user_features += [
    SequenceFeature("hist_movie_id",
                    vocab_size=feature_max_idx["movie_id"],
                    embed_dim=16,
                    pooling="mean",
                    shared_with="movie_id")
]

item_features = [
    SparseFeature(feature_name, vocab_size=feature_max_idx[feature_name], embed_dim=16) for feature_name in item_cols
]
print(user_features)
print(item_features)
```

    [<SparseFeature user_id with Embedding shape (3, 16)>, <SparseFeature gender with Embedding shape (3, 16)>, <SparseFeature age with Embedding shape (3, 16)>, <SparseFeature occupation with Embedding shape (3, 16)>, <SparseFeature zip with Embedding shape (3, 16)>, <SequenceFeature hist_movie_id with Embedding shape (94, 16)>]
    [<SparseFeature movie_id with Embedding shape (94, 16)>, <SparseFeature cate_id with Embedding shape (11, 16)>]
    


```python
# 将dataframe转为dict
from torch_rechub.utils.data import df_to_dict
all_item = df_to_dict(item_profile)
test_user = x_test
print({k: v[:3] for k, v in all_item.items()})
print({k: v[0] for k, v in test_user.items()})
```

    {'movie_id': array([32, 17, 22]), 'cate_id': array([7, 3, 8])}
    {'user_id': 2, 'movie_id': 50, 'hist_movie_id': array([ 0,  0,  0,  0, 35, 37, 43, 32, 78, 36, 34, 92,  3, 79, 86, 82, 44,
           56, 40, 21, 30, 93, 80, 81, 39, 61, 60, 62, 88, 15, 38, 45, 31, 64,
           84, 58, 76, 49, 89, 16, 52, 83,  7, 75, 68, 90,  6, 59,  8, 46]), 'histlen_movie_id': 46, 'label': 1, 'gender': 2, 'age': 2, 'occupation': 2, 'zip': 2, 'cate_id': 1}
    

### 训练模型

- 根据之前的x_train字典和y_train等数据生成训练用的Dataloader（train_dl）、测试用的Dataloader（test_dl, item_dl）。

- 定义一个双塔DSSM模型，`user_features`表示用户塔有哪些特征，`user_params`表示用户塔的MLP的各层维度和激活函数。（Note：在这个样例中激活函数的选取对最终结果影响很大，调试时不要修改激活函数的参数）
- 定义一个召回训练器MatchTrainer，进行模型的训练。


```python
from torch_rechub.models.matching import DSSM
from torch_rechub.trainers import MatchTrainer
from torch_rechub.utils.data import MatchDataGenerator
# 根据之前处理的数据拿到Dataloader
dg = MatchDataGenerator(x=x_train, y=y_train)
train_dl, test_dl, item_dl = dg.generate_dataloader(test_user, all_item, batch_size=256)

# 定义模型
model = DSSM(user_features,
             item_features,
             temperature=0.02,
             user_params={
                 "dims": [256, 128, 64],
                 "activation": 'prelu',  # important!!
             },
             item_params={
                 "dims": [256, 128, 64],
                 "activation": 'prelu',  # important!!
             })

# 模型训练器
trainer = MatchTrainer(model,
                       mode=0,  # 同上面的mode，需保持一致
                       optimizer_params={
                           "lr": 1e-4,
                           "weight_decay": 1e-6
                       },
                       n_epoch=1,
                       device='cpu',
                       model_path=save_dir)

# 开始训练
trainer.fit(train_dl)
```

    epoch: 0
    

    train: 100%|██████████| 2/2 [00:00<00:00,  6.67it/s]
    

### Milvus向量化召回 评估
- 使用trainer获取测试集中每个user的embedding和数据集中所有物品的embedding集合
- 用annoy构建物品embedding索引，对每个用户向量进行ANN（Approximate Nearest Neighbors）召回K个物品
- 查看topk评估指标，一般看recall、precision、hit



```python
import collections
import numpy as np
import pandas as pd
from torch_rechub.utils.match import Milvus
from torch_rechub.basic.metric import topk_metrics

def match_evaluation(user_embedding, item_embedding, test_user, all_item, user_col='user_id', item_col='movie_id',
                     raw_id_maps="./raw_id_maps.npy", topk=10):
    print("evaluate embedding matching on test data")
    
    milvus = Milvus(dim=64)
    milvus.fit(item_embedding)

    #for each user of test dataset, get ann search topk result
    print("matching for topk")
    user_map, item_map = np.load(raw_id_maps, allow_pickle=True)
    match_res = collections.defaultdict(dict)  # user id -> predicted item ids
    for user_id, user_emb in zip(test_user[user_col], user_embedding):
        items_idx, items_scores = milvus.query(v=user_emb, n=topk)  #the index of topk match items
        match_res[user_map[user_id]] = np.vectorize(item_map.get)(all_item[item_col][items_idx])

    #get ground truth
    print("generate ground truth")

    data = pd.DataFrame({user_col: test_user[user_col], item_col: test_user[item_col]})
    data[user_col] = data[user_col].map(user_map)
    data[item_col] = data[item_col].map(item_map)
    user_pos_item = data.groupby(user_col).agg(list).reset_index()
    ground_truth = dict(zip(user_pos_item[user_col], user_pos_item[item_col]))  # user id -> ground truth

    print("compute topk metrics")
    out = topk_metrics(y_true=ground_truth, y_pred=match_res, topKs=[topk])
    return out
```


```python
user_embedding = trainer.inference_embedding(model=model, mode="user", data_loader=test_dl, model_path=save_dir)
item_embedding = trainer.inference_embedding(model=model, mode="item", data_loader=item_dl, model_path=save_dir)
match_evaluation(user_embedding, item_embedding, test_user, all_item, topk=10, raw_id_maps=save_dir+"raw_id_maps.npy")

```

    user inference: 100%|██████████| 1/1 [00:00<00:00,  7.13it/s]
    item inference: 100%|██████████| 1/1 [00:00<00:00,  5.43it/s]
    

    evaluate embedding matching on test data
    Start connecting to Milvus
    Does collection rechub exist? True
    Number of entities in Milvus: 93
    matching for topk
    generate ground truth
    compute topk metrics
    

    /tmp/ipykernel_2562245/2287123622.py:20: FutureWarning: Using a non-tuple sequence for multidimensional indexing is deprecated; use `arr[tuple(seq)]` instead of `arr[seq]`. In the future this will be interpreted as an array index, `arr[np.array(seq)]`, which will result either in an error or a different result.
      match_res[user_map[user_id]] = np.vectorize(item_map.get)(all_item[item_col][items_idx])
    




    defaultdict(list,
                {'NDCG': ['NDCG@10: 0.0'],
                 'MRR': ['MRR@10: 0.0'],
                 'Recall': ['Recall@10: 0.0'],
                 'Hit': ['Hit@10: 0.0'],
                 'Precision': ['Precision@10: 0.0']})




```python

```
