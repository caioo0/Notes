# Torch-Rechub Tutorial：Matching

- 场景：召回
- 模型：DSSM、YouTubeDNN
- 数据：MovieLens-1M

- 本教程包括以下内容：
    1. 在MovieLens-1M数据集上数据集训练一个DSSM召回模型
    2. 在MovieLens-1M数据集上数据集训练一个YouTubeDNN召回模型

- 在阅读本教程前，希望你对YouTubeDNN和DSSM有一个初步的了解，大概了解数据在模型中是如何流动的，否则直接怼代码可能一脸懵逼。模型介绍：[YouTubeDNN](https://datawhalechina.github.io/fun-rec/#/ch02/ch2.1/ch2.1.2/YoutubeDNN)    [DSSM](https://datawhalechina.github.io/fun-rec/#/ch02/ch2.1/ch2.1.2/DSSM)
- 本教程是对`examples/matching/run_ml_dssm.py`和`examples/matching/run_ml_youtube_dnn.py`两个文件的更详细的解释，代码基本与两个文件一致。
- 本框架还在开发阶段，可能还有一些bug。如果你在复现后，发现指标明显高于当前，欢迎与我们交流。


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




    <torch._C.Generator at 0x7fea361c9f10>



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

       user_id  movie_id  rating  timestamp                                   title                        genres gender  age  occupation    zip    cate_id
    0        1      1193       5  978300760  One Flew Over the Cuckoo's Nest (1975)                         Drama      F    1          10  48067      Drama
    1        1       661       3  978302109        James and the Giant Peach (1996)  Animation|Children's|Musical      F    1          10  48067  Animation
    2        1       914       3  978301968                     My Fair Lady (1964)               Musical|Romance      F    1          10  48067    Musical
    3        1      3408       4  978300275                  Erin Brockovich (2000)                         Drama      F    1          10  48067      Drama
    4        1      2355       5  978824291                    Bug's Life, A (1998)   Animation|Children's|Comedy      F    1          10  48067  Animation
    

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

        user_id  movie_id  gender  age  occupation  zip  cate_id
    71        2        35       2    2           2    2        1
    78        2        37       2    2           2    2        7
    94        2        43       2    2           2    2        7
    53        2        32       2    2           2    2        7
    77        2        78       2    2           2    2        5
    LabelEncoding后：
        user_id  movie_id  gender  age  occupation  zip  cate_id
    71        2        35       2    2           2    2        1
    78        2        37       2    2           2    2        7
    94        2        43       2    2           2    2        7
    53        2        32       2    2           2    2        7
    77        2        78       2    2           2    2        5
    

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
```

        user_id  gender  age  occupation  zip
    71        2       2    2           2    2
    31        1       1    1           1    1
        movie_id  cate_id
    71        35        1
    78        37        7
    94        43        7
    53        32        7
    77        78        5
    

#### 序列特征的处理
本数据集中的序列特征为观看历史，根据timestamp来生成，具体在`generate_seq_feature_match`函数中实现。参数含义如下：
- `mode`表示样本的训练方式（0 - point wise, 1 - pair wise, 2 - list wise）
- `neg_ratio`表示每个正样本对应的负样本数量，
- `min_item`限制每个用户最少的样本量，小于此值将会被抛弃，当做冷启动用户处理（框架中还未添加冷启动的处理，这里直接抛弃）
- `sample_method`表示负采样方法。

> 关于参数`mode`的一点小说明：在模型实现过程中，框架只考虑了论文中提出的样本的训练方式，用其他方式可能会报错。例如：DSSM中采用point wise的方式，即`mode=0`，如果传入别的`mode`，不保证能正确运行，但是论文中对应的训练方式是能保证正确运行的。




```python
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

    preprocess data
    

    generate sequence features: 100%|██████████| 2/2 [00:00<00:00, 1539.48it/s]

    n_train: 384, n_test: 2
    0 cold start user droped 
       user_id  movie_id                                      hist_movie_id  histlen_movie_id  label
    0        1        86  [87, 51, 25, 41, 65, 53, 91, 34, 74, 32, 5, 18...                22      0
    1        2        83                               [35, 37, 43, 32, 78]                 5      0
    2        1        15  [87, 51, 25, 41, 65, 53, 91, 34, 74, 32, 5, 18...                41      0
    3        2        19                                               [35]                 1      0
    4        2        24  [35, 37, 43, 32, 78, 36, 34, 92, 3, 79, 86, 82...                34      0
    {'user_id': array([1, 2, 1]), 'movie_id': array([86, 83, 15]), 'hist_movie_id': array([[ 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
             0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, 87, 51, 25, 41,
            65, 53, 91, 34, 74, 32,  5, 18, 23, 14, 70, 55, 58, 82, 24, 28,
            56, 57],
           [ 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
             0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
             0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, 35, 37, 43,
            32, 78],
           [ 0,  0,  0,  0,  0,  0,  0,  0,  0, 87, 51, 25, 41, 65, 53, 91,
            34, 74, 32,  5, 18, 23, 14, 70, 55, 58, 82, 24, 28, 56, 57,  4,
            26, 29, 22, 73, 42, 71, 38, 17, 77, 10, 85, 72, 64, 27, 12, 33,
            67, 47]]), 'histlen_movie_id': array([22,  5, 41]), 'label': array([0, 0, 0]), 'gender': array([1, 2, 1]), 'age': array([1, 2, 1]), 'occupation': array([1, 2, 1]), 'zip': array([1, 2, 1]), 'cate_id': array([7, 1, 7])}
    

    
    


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


```python
# 将dataframe转为dict
from torch_rechub.utils.data import df_to_dict
all_item = df_to_dict(item_profile)
test_user = x_test
print({k: v[:3] for k, v in all_item.items()})
print({k: v[0] for k, v in test_user.items()})
```

    {'movie_id': array([35, 37, 43]), 'cate_id': array([1, 7, 7])}
    {'user_id': 1, 'movie_id': 2, 'hist_movie_id': array([25, 41, 65, 53, 91, 34, 74, 32,  5, 18, 23, 14, 70, 55, 58, 82, 24,
           28, 56, 57,  4, 26, 29, 22, 73, 42, 71, 38, 17, 77, 10, 85, 72, 64,
           27, 12, 33, 67, 47,  9, 13,  1, 69, 19, 11, 20, 66, 63, 54, 48]), 'histlen_movie_id': 52, 'label': 1, 'gender': 1, 'age': 1, 'occupation': 1, 'zip': 1, 'cate_id': 3}
    

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
    

    train: 100%|██████████| 2/2 [00:21<00:00, 10.59s/it]
    

### 向量化召回 评估
- 使用trainer获取测试集中每个user的embedding和数据集中所有物品的embedding集合
- 用annoy构建物品embedding索引，对每个用户向量进行ANN（Approximate Nearest Neighbors）召回K个物品
- 查看topk评估指标，一般看recall、precision、hit



```python
import collections
import numpy as np
import pandas as pd
from torch_rechub.utils.match import Annoy
from torch_rechub.basic.metric import topk_metrics

def match_evaluation(user_embedding, item_embedding, test_user, all_item, user_col='user_id', item_col='movie_id',
                     raw_id_maps="./raw_id_maps.npy", topk=10):
    print("evaluate embedding matching on test data")
    annoy = Annoy(n_trees=10)
    annoy.fit(item_embedding)

    #for each user of test dataset, get ann search topk result
    print("matching for topk")
    user_map, item_map = np.load(raw_id_maps, allow_pickle=True)
    match_res = collections.defaultdict(dict)  # user id -> predicted item ids
    for user_id, user_emb in zip(test_user[user_col], user_embedding):
        items_idx, items_scores = annoy.query(v=user_emb, n=topk)  #the index of topk match items
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

    user inference: 100%|██████████| 1/1 [00:08<00:00,  8.61s/it]
    item inference: 100%|██████████| 1/1 [00:07<00:00,  7.80s/it]

    evaluate embedding matching on test data
    matching for topk
    generate ground truth
    compute topk metrics
    

    
    




    defaultdict(list,
                {'NDCG': ['NDCG@10: 0.0'],
                 'MRR': ['MRR@10: 0.0'],
                 'Recall': ['Recall@10: 0.0'],
                 'Hit': ['Hit@10: 0.0'],
                 'Precision': ['Precision@10: 0.0']})



### 在MovieLens-1M数据集上数据集训练一个YouTubeDNN模型

[YoutubeDNN论文链接](https://dl.acm.org/doi/pdf/10.1145/2959100.2959190)

YouTubeDNN模型虽然叫单塔模型，但也是以双塔模型的思想去构建的，所以不管是模型还是其他都很相似。
下面给出了YouTubeDNN的代码，与DSSM不同的代码会用`序号+中文`的方式标注，例如`# [0]训练方式改为List wise`，大家可以感受一下二者的区别。


```python
import os
import numpy as np
import pandas as pd
import torch
from sklearn.preprocessing import LabelEncoder
from torch_rechub.models.matching import YoutubeDNN
from torch_rechub.trainers import MatchTrainer
from torch_rechub.basic.features import SparseFeature, SequenceFeature
from torch_rechub.utils.match import generate_seq_feature_match, gen_model_input
from torch_rechub.utils.data import df_to_dict, MatchDataGenerator


torch.manual_seed(2022)

data = pd.read_csv(file_path)
data["cate_id"] = data["genres"].apply(lambda x: x.split("|")[0])
sparse_features = ['user_id', 'movie_id', 'gender', 'age', 'occupation', 'zip', "cate_id"]
user_col, item_col = "user_id", "movie_id"

feature_max_idx = {}
for feature in sparse_features:
    lbe = LabelEncoder()
    data[feature] = lbe.fit_transform(data[feature]) + 1
    feature_max_idx[feature] = data[feature].max() + 1
    if feature == user_col:
        user_map = {encode_id + 1: raw_id for encode_id, raw_id in enumerate(lbe.classes_)}  #encode user id: raw user id
    if feature == item_col:
        item_map = {encode_id + 1: raw_id for encode_id, raw_id in enumerate(lbe.classes_)}  #encode item id: raw item id
np.save(save_dir+"raw_id_maps.npy", (user_map, item_map))
user_cols = ["user_id", "gender", "age", "occupation", "zip"]
item_cols = ["movie_id", "cate_id"]
user_profile = data[user_cols].drop_duplicates('user_id')
item_profile = data[item_cols].drop_duplicates('movie_id')


#Note: mode=2 means list-wise negative sample generate, saved in last col "neg_items"
df_train, df_test = generate_seq_feature_match(data,
                                               user_col,
                                               item_col,
                                               time_col="timestamp",
                                               item_attribute_cols=[],
                                               sample_method=1,
                                               mode=2,  # [0]训练方式改为List wise
                                               neg_ratio=3,
                                               min_item=0)
x_train = gen_model_input(df_train, user_profile, user_col, item_profile, item_col, seq_max_len=50)
y_train = np.array([0] * df_train.shape[0])  # [1]训练集所有样本的label都取0。因为一个样本的组成是(pos, neg1, neg2, ...)，视为一个多分类任务，正样本的位置永远是0
x_test = gen_model_input(df_test, user_profile, user_col, item_profile, item_col, seq_max_len=50)

user_cols = ['user_id', 'gender', 'age', 'occupation', 'zip']

user_features = [SparseFeature(name, vocab_size=feature_max_idx[name], embed_dim=16) for name in user_cols]
user_features += [
    SequenceFeature("hist_movie_id",
                    vocab_size=feature_max_idx["movie_id"],
                    embed_dim=16,
                    pooling="mean",
                    shared_with="movie_id")
]

item_features = [SparseFeature('movie_id', vocab_size=feature_max_idx['movie_id'], embed_dim=16)]  # [2]物品的特征只有itemID，即movie_id一个
neg_item_feature = [
    SequenceFeature('neg_items',
                    vocab_size=feature_max_idx['movie_id'],
                    embed_dim=16,
                    pooling="concat",
                    shared_with="movie_id")
]  # [3] 多了一个neg item feature，会传入到模型中，在item tower中会用到

all_item = df_to_dict(item_profile)
test_user = x_test

dg = MatchDataGenerator(x=x_train, y=y_train)
train_dl, test_dl, item_dl = dg.generate_dataloader(test_user, all_item, batch_size=256)

model = YoutubeDNN(user_features, item_features, neg_item_feature, user_params={"dims": [128, 64, 16]}, temperature=0.02)  # [4] MLP的最后一层需保持与item embedding一致

#mode=1 means pair-wise learning
trainer = MatchTrainer(model,
                       mode=2,
                       optimizer_params={
                           "lr": 1e-4,
                           "weight_decay": 1e-6
                       },
                       n_epoch=1, #5
                       device='cpu',
                       model_path=save_dir)

trainer.fit(train_dl)

print("inference embedding")
user_embedding = trainer.inference_embedding(model=model, mode="user", data_loader=test_dl, model_path=save_dir)
item_embedding = trainer.inference_embedding(model=model, mode="item", data_loader=item_dl, model_path=save_dir)
match_evaluation(user_embedding, item_embedding, test_user, all_item, topk=10, raw_id_maps="../data/ml-1m/saved/raw_id_maps.npy")

```

    preprocess data
    

    generate sequence features: 100%|██████████| 2/2 [00:00<00:00, 2147.62it/s]
    

    n_train: 96, n_test: 2
    0 cold start user droped 
    epoch: 0
    

    train: 100%|██████████| 1/1 [00:07<00:00,  7.75s/it]
    

    inference embedding
    

    user inference: 100%|██████████| 1/1 [00:07<00:00,  7.80s/it]
    item inference: 100%|██████████| 1/1 [00:11<00:00, 11.56s/it]

    torch.Size([2, 16]) torch.Size([93, 16])
    evaluate embedding matching on test data
    matching for topk
    generate ground truth
    compute topk metrics
    

    
    




    defaultdict(list,
                {'NDCG': ['NDCG@10: 0.0'],
                 'MRR': ['MRR@10: 0.0'],
                 'Recall': ['Recall@10: 0.0'],
                 'Hit': ['Hit@10: 0.0'],
                 'Precision': ['Precision@10: 0.0']})


