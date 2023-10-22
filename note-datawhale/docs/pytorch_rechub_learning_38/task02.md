# Torch-Rechub Tutorial： DIN

- 场景：精排（CTR预测） 
- 模型：DIN
- 数据：Amazon-Electronics


- 学习目标
    - 学会使用torch-rechub调用DIN进行CTR预测
    - 学会基于torch-rechub的基础模块，使用pytorch复现DIN模型
    


- 学习材料：
    - 模型思想介绍：https://datawhalechina.github.io/fun-rec/#/ch02/ch2.2/ch2.2.4/DIN
    - rechub模型代码：https://github.com/datawhalechina/torch-rechub/blob/main/torch_rechub/models/ranking/din.py
    - 数据集详细描述：https://github.com/datawhalechina/torch-rechub/tree/main/examples/ranking



```python
#安装torch-rechub
# !pip install torch-rechub
```

    Collecting torch-rechub
      Downloading torch-rechub-0.0.2.tar.gz (33 kB)
    Requirement already satisfied: numpy>=1.19.0 in /opt/anaconda3/lib/python3.8/site-packages (from torch-rechub) (1.22.3)
    Requirement already satisfied: torch>=1.7.0 in /opt/anaconda3/lib/python3.8/site-packages (from torch-rechub) (1.10.0)
    Requirement already satisfied: pandas>=1.0.5 in /opt/anaconda3/lib/python3.8/site-packages (from torch-rechub) (1.2.4)
    Requirement already satisfied: tqdm>=4.64.0 in /opt/anaconda3/lib/python3.8/site-packages (from torch-rechub) (4.64.0)
    Requirement already satisfied: scikit_learn>=0.23.2 in /opt/anaconda3/lib/python3.8/site-packages (from torch-rechub) (0.24.1)
    Requirement already satisfied: annoy>=1.17.0 in /opt/anaconda3/lib/python3.8/site-packages (from torch-rechub) (1.17.0)
    Requirement already satisfied: python-dateutil>=2.7.3 in /opt/anaconda3/lib/python3.8/site-packages (from pandas>=1.0.5->torch-rechub) (2.8.1)
    Requirement already satisfied: pytz>=2017.3 in /opt/anaconda3/lib/python3.8/site-packages (from pandas>=1.0.5->torch-rechub) (2021.1)
    Requirement already satisfied: six>=1.5 in /opt/anaconda3/lib/python3.8/site-packages (from python-dateutil>=2.7.3->pandas>=1.0.5->torch-rechub) (1.15.0)
    Requirement already satisfied: threadpoolctl>=2.0.0 in /opt/anaconda3/lib/python3.8/site-packages (from scikit_learn>=0.23.2->torch-rechub) (2.1.0)
    Requirement already satisfied: scipy>=0.19.1 in /opt/anaconda3/lib/python3.8/site-packages (from scikit_learn>=0.23.2->torch-rechub) (1.6.2)
    Requirement already satisfied: joblib>=0.11 in /opt/anaconda3/lib/python3.8/site-packages (from scikit_learn>=0.23.2->torch-rechub) (1.0.1)
    Requirement already satisfied: typing_extensions in /opt/anaconda3/lib/python3.8/site-packages (from torch>=1.7.0->torch-rechub) (4.2.0)
    Building wheels for collected packages: torch-rechub
      Building wheel for torch-rechub (setup.py) ... [?25ldone
    [?25h  Created wheel for torch-rechub: filename=torch_rechub-0.0.2-py3-none-any.whl size=52473 sha256=104cf9b7121ee4867f6d6ceae2f89a742ccf8df2189e15b05434198712b395d3
      Stored in directory: /Users/chester/Library/Caches/pip/wheels/c0/3d/30/8ae954cd2eb76ac5347c1d34b0d48e2b621efebebd09d894c3
    Successfully built torch-rechub
    Installing collected packages: torch-rechub
    Successfully installed torch-rechub-0.0.2
    


```python
# 检查torch的安装以及gpu的使用
import torch
print(torch.__version__, torch.cuda.is_available())

import torch_rechub
import pandas as pd
import numpy as np
import tqdm
import sklearn

torch.manual_seed(2022) #固定随机种子
```

    1.10.0 False
    




    <torch._C.Generator at 0x7ff60056e5d0>



## 在自定义数据集上训练DIN模型
训练新的模型只需要三个步骤：
- 支持新数据集
- 指定特征含义
- 训练新模型


### 支持新数据集
这里我们以Amazon-Electronics为例，原数据是json格式，我们提取所需要的信息预处理为一个仅包含user_id, item_id, cate_id, time四个特征列的CSV文件。

注意：examples文件夹中仅有100行数据方便我们轻量化学习，如果需要Amazon数据集全量数据用于测试模型性能有两种方法：
1. 我们提供了处理完成的全量数据在高速网盘链接：https://cowtransfer.com/s/e911569fbb1043 ，只需要下载全量数据后替换下一行的file_path即可；
2. 前往Amazon数据集官网：http://jmcauley.ucsd.edu/data/amazon/index_2014.html ，进入后选择elextronics下载，我们同样提供了数据集处理脚本在examples/ranking/data/amazon-electronics/preprocess_amazon_electronics.py文件中。


```python
# 查看文件
file_path = '../examples/ranking/data/amazon-electronics/amazon_electronics_sample.csv'
data = pd.read_csv(file_path)
data
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>user_id</th>
      <th>item_id</th>
      <th>time</th>
      <th>cate_id</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>41064</td>
      <td>13179</td>
      <td>1396656000</td>
      <td>584</td>
    </tr>
    <tr>
      <th>1</th>
      <td>89202</td>
      <td>13179</td>
      <td>1380499200</td>
      <td>584</td>
    </tr>
    <tr>
      <th>2</th>
      <td>95407</td>
      <td>13179</td>
      <td>1364688000</td>
      <td>584</td>
    </tr>
    <tr>
      <th>3</th>
      <td>101617</td>
      <td>13179</td>
      <td>1389657600</td>
      <td>584</td>
    </tr>
    <tr>
      <th>4</th>
      <td>174964</td>
      <td>13179</td>
      <td>1363478400</td>
      <td>584</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>94</th>
      <td>2974</td>
      <td>29247</td>
      <td>1365724800</td>
      <td>339</td>
    </tr>
    <tr>
      <th>95</th>
      <td>3070</td>
      <td>29247</td>
      <td>1294790400</td>
      <td>339</td>
    </tr>
    <tr>
      <th>96</th>
      <td>3139</td>
      <td>29247</td>
      <td>1388448000</td>
      <td>339</td>
    </tr>
    <tr>
      <th>97</th>
      <td>3192</td>
      <td>29247</td>
      <td>1359590400</td>
      <td>339</td>
    </tr>
    <tr>
      <th>98</th>
      <td>3208</td>
      <td>29247</td>
      <td>1363564800</td>
      <td>339</td>
    </tr>
  </tbody>
</table>
<p>99 rows × 4 columns</p>
</div>



## 特征工程

- Dense特征：又称数值型特征，例如薪资、年龄，在DIN中我们没有用到这个类型的特征。
- Sparse特征：又称类别型特征，例如性别、学历。本教程中对Sparse特征直接进行LabelEncoder编码操作，将原始的类别字符串映射为数值，在模型中将为每一种取值生成Embedding向量。
- Sequence特征：序列特征，比如用户历史点击item_id序列、历史商铺序列等，序列特征如何抽取，是我们在DIN中学习的一个重点，也是DIN主要创新点之一。


```python
from torch_rechub.utils.data import create_seq_features
# 构建用户的历史行为序列特征，内置函数create_seq_features只需要指定数据，和需要生成序列的特征，drop_short是选择舍弃行为序列较短的用户
train, val, test = create_seq_features(data, seq_feature_col=['item_id', 'cate_id'], drop_short=0)
# 查看当前构建的序列，在这个案例中我们创建了历史点击序列，和历史类别序列
train
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>user_id</th>
      <th>history_item</th>
      <th>history_cate</th>
      <th>target_item</th>
      <th>target_cate</th>
      <th>label</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>1</td>
      <td>[2, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, ...</td>
      <td>[2, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, ...</td>
      <td>4</td>
      <td>1</td>
      <td>1</td>
    </tr>
    <tr>
      <th>1</th>
      <td>1</td>
      <td>[2, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, ...</td>
      <td>[2, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, ...</td>
      <td>1</td>
      <td>3</td>
      <td>0</td>
    </tr>
  </tbody>
</table>
</div>



### 让模型明白如何处理每一类特征
在DIN模型中，我们讲使用了两种类别的特征，分别是类别特征和序列特征。对于类别特征，我们希望模型将其输入Embedding层，而对于序列特征，我们不仅希望模型将其输入Embedding层，还需要计算target-attention分数，所以需要指定DataFrame中每一列的含义，让模型能够正确处理。


在这个案例中，因为我们使用user_id,item_id和item_cate这三个类别特征，使用用户的item_id和cate的历史序列作为序列特征。在torch-rechub我们只需要调用DenseFeature, SparseFeature, SequenceFeature这三个类，就能自动正确处理每一类特征。


```python
from torch_rechub.basic.features import DenseFeature, SparseFeature, SequenceFeature

n_users, n_items, n_cates = data["user_id"].max(), data["item_id"].max(), data["cate_id"].max()
# 这里指定每一列特征的处理方式，对于sparsefeature，需要输入embedding层，所以需要指定特征空间大小和输出的维度
features = [SparseFeature("target_item", vocab_size=n_items + 2, embed_dim=8),
            SparseFeature("target_cate", vocab_size=n_cates + 2, embed_dim=8),
            SparseFeature("user_id", vocab_size=n_users + 2, embed_dim=8)]
target_features = features
# 对于序列特征，除了需要和类别特征一样处理意外，item序列和候选item应该属于同一个空间，我们希望模型共享它们的embedding，所以可以通过shared_with参数指定
history_features = [
    SequenceFeature("history_item", vocab_size=n_items + 2, embed_dim=8, pooling="concat", shared_with="target_item"),
    SequenceFeature("history_cate", vocab_size=n_cates + 2, embed_dim=8, pooling="concat", shared_with="target_cate")
]
```

在上述步骤中，我们制定了每一列的数据如何处理、数据维度、embed后的维度，目的就是在构建模型中，让模型知道每一层的参数。

接下来我们生成训练数据，用于训练，一般情况下，我们只需要定义一个字典装入每一列特征即可。


```python
from torch_rechub.utils.data import df_to_dict, DataGenerator
# 指定label，生成模型的输入，这一步是转换为字典结构
train = df_to_dict(train)
val = df_to_dict(val)
test = df_to_dict(test)

train_y, val_y, test_y = train["label"], val["label"], test["label"]

del train["label"]
del val["label"]
del test["label"]
train_x, val_x, test_x = train, val, test

# 最后查看一次输入模型的数据格式
train_x

# 构建dataloader，指定模型读取数据的方式，和区分验证集测试集、指定batch大小
dg = DataGenerator(train_x, train_y)
train_dataloader, val_dataloader, test_dataloader = dg.generate_dataloader(x_val=val_x, y_val=val_y, x_test=test_x, y_test=test_y, batch_size=16)
```

### 训练新模型
我们封装了召回、排序、多任务等众多工业界主流的模型，基本能够做到几个参数定义一个模型。

在本案例中，我用训练一个深度兴趣网络DIN模型，我们只需要指定DIN的少数模型结构参数，和学习率等参数，就可以完成训练。


```python
from torch_rechub.models.ranking import DIN
from torch_rechub.trainers import CTRTrainer

# 定义模型，模型的参数需要我们之前的feature类，用于构建模型的输入层，mlp指定模型后续DNN的结构，attention_mlp指定attention层的结构
model = DIN(features=features, history_features=history_features, target_features=target_features, mlp_params={"dims": [256, 128]}, attention_mlp_params={"dims": [256, 128]})

# 模型训练，需要学习率、设备等一般的参数，此外我们还支持earlystoping策略，及时发现过拟合
ctr_trainer = CTRTrainer(model, optimizer_params={"lr": 1e-3, "weight_decay": 1e-3}, n_epoch=3, earlystop_patience=4, device='cpu', model_path='./')
ctr_trainer.fit(train_dataloader, val_dataloader)

# 查看在测试集上的性能
auc = ctr_trainer.evaluate(ctr_trainer.model, test_dataloader)
print(f'test auc: {auc}')
```

    epoch: 0
    

    train: 100%|██████████| 1/1 [00:09<00:00,  9.61s/it]
    validation: 100%|██████████| 1/1 [00:09<00:00,  9.79s/it]
    

    epoch: 0 validation: auc: 1.0
    epoch: 1
    

    train: 100%|██████████| 1/1 [00:09<00:00,  9.57s/it]
    validation: 100%|██████████| 1/1 [00:10<00:00, 10.10s/it]
    

    epoch: 1 validation: auc: 1.0
    epoch: 2
    

    train: 100%|██████████| 1/1 [00:10<00:00, 10.18s/it]
    validation: 100%|██████████| 1/1 [00:09<00:00,  9.92s/it]
    

    epoch: 2 validation: auc: 1.0
    

    validation: 100%|██████████| 1/1 [00:09<00:00,  9.49s/it]

    test auc: 1.0
    

    
    
