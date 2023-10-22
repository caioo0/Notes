# Torch-Rechub Tutorial: DeepFM

- 场景：精排（CTR预测） 
- 模型：DeepFM
- 数据：Criteo广告数据集

- 学习目标
  - 学会使用torch-rechub调用DeepFM进行CTR预测
  - 学会基于torch-rechub的基础模块，使用pytorch复现DeepFM模型
  
- 学习材料：
  - 模型思想介绍：https://datawhalechina.github.io/fun-rec/#/ch02/ch2.2/ch2.2.3/DeepFM
  - rechub模型代码：https://github.com/datawhalechina/torch-rechub/blob/main/torch_rechub/models/ranking/deepfm.py
  - 数据集详细描述：https://github.com/datawhalechina/torch-rechub/tree/main/examples/ranking



```python
#安装torch-rechub
#!pip install torch-rechub
```


```python
import numpy as np
import pandas as pd
import torch
from torch_rechub.models.ranking import WideDeep, DeepFM, DCN
from torch_rechub.trainers import CTRTrainer
from torch_rechub.basic.features import DenseFeature, SparseFeature
from torch_rechub.utils.data import DataGenerator
from tqdm import tqdm
from sklearn.preprocessing import MinMaxScaler, LabelEncoder
torch.manual_seed(2022) #固定随机种子
```

### 数据集介绍
该数据集是Criteo Labs发布的在线广告数据集。 它包含数百万个展示广告的点击反馈记录，该数据可作为点击率(CTR)预测的基准。 数据集具有40个特征，第一列是标签，其中值1表示已点击广告，而值0表示未点击广告。 其他特征包含13个dense特征和26个sparse特征。


```python
data_path = '../examples/ranking/data/criteo/criteo_sample.csv'
data = pd.read_csv(data_path)  
#data = pd.read_csv(data_path, compression="gzip") #if the raw_data is .gz file
data.head()
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
      <th>label</th>
      <th>I1</th>
      <th>I2</th>
      <th>I3</th>
      <th>I4</th>
      <th>I5</th>
      <th>I6</th>
      <th>I7</th>
      <th>I8</th>
      <th>I9</th>
      <th>...</th>
      <th>C17</th>
      <th>C18</th>
      <th>C19</th>
      <th>C20</th>
      <th>C21</th>
      <th>C22</th>
      <th>C23</th>
      <th>C24</th>
      <th>C25</th>
      <th>C26</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>0</td>
      <td>0.0</td>
      <td>0</td>
      <td>104.0</td>
      <td>27.0</td>
      <td>1990.0</td>
      <td>142.0</td>
      <td>4.0</td>
      <td>32.0</td>
      <td>37.0</td>
      <td>...</td>
      <td>e5ba7672</td>
      <td>25c88e42</td>
      <td>21ddcdc9</td>
      <td>b1252a9d</td>
      <td>0e8585d2</td>
      <td>NaN</td>
      <td>32c7478e</td>
      <td>0d4a6d1a</td>
      <td>001f3601</td>
      <td>92c878de</td>
    </tr>
    <tr>
      <th>1</th>
      <td>0</td>
      <td>0.0</td>
      <td>-1</td>
      <td>63.0</td>
      <td>40.0</td>
      <td>1470.0</td>
      <td>61.0</td>
      <td>4.0</td>
      <td>37.0</td>
      <td>46.0</td>
      <td>...</td>
      <td>e5ba7672</td>
      <td>d3303ea5</td>
      <td>21ddcdc9</td>
      <td>b1252a9d</td>
      <td>7633c7c8</td>
      <td>NaN</td>
      <td>32c7478e</td>
      <td>17f458f7</td>
      <td>001f3601</td>
      <td>71236095</td>
    </tr>
    <tr>
      <th>2</th>
      <td>0</td>
      <td>0.0</td>
      <td>370</td>
      <td>4.0</td>
      <td>1.0</td>
      <td>1787.0</td>
      <td>65.0</td>
      <td>14.0</td>
      <td>25.0</td>
      <td>489.0</td>
      <td>...</td>
      <td>3486227d</td>
      <td>642f2610</td>
      <td>55dd3565</td>
      <td>b1252a9d</td>
      <td>5c8dc711</td>
      <td>NaN</td>
      <td>423fab69</td>
      <td>45ab94c8</td>
      <td>2bf691b1</td>
      <td>c84c4aec</td>
    </tr>
    <tr>
      <th>3</th>
      <td>1</td>
      <td>19.0</td>
      <td>10</td>
      <td>30.0</td>
      <td>10.0</td>
      <td>1.0</td>
      <td>3.0</td>
      <td>33.0</td>
      <td>47.0</td>
      <td>126.0</td>
      <td>...</td>
      <td>e5ba7672</td>
      <td>a78bd508</td>
      <td>21ddcdc9</td>
      <td>5840adea</td>
      <td>c2a93b37</td>
      <td>NaN</td>
      <td>32c7478e</td>
      <td>1793a828</td>
      <td>e8b83407</td>
      <td>2fede552</td>
    </tr>
    <tr>
      <th>4</th>
      <td>0</td>
      <td>0.0</td>
      <td>0</td>
      <td>36.0</td>
      <td>22.0</td>
      <td>4684.0</td>
      <td>217.0</td>
      <td>9.0</td>
      <td>35.0</td>
      <td>135.0</td>
      <td>...</td>
      <td>e5ba7672</td>
      <td>7ce63c71</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>af5dc647</td>
      <td>NaN</td>
      <td>dbb486d7</td>
      <td>1793a828</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
  </tbody>
</table>
<p>5 rows × 40 columns</p>
</div>



### 特征工程
- Dense特征：又称数值型特征，例如薪资、年龄。 本教程中对Dense特征进行两种操作：
  - MinMaxScaler归一化，使其取值在[0,1]之间
  - 将其离散化成新的Sparse特征
- Sparse特征：又称类别型特征，例如性别、学历。本教程中对Sparse特征直接进行LabelEncoder编码操作，将原始的类别字符串映射为数值，在模型中将为每一种取值生成Embedding向量。


```python
dense_cols= [f for f in data.columns.tolist() if f[0] == "I"] #以I开头的特征名为dense特征
sparse_cols = [f for f in data.columns.tolist() if f[0] == "C"]  #以C开头的特征名为sparse特征

data[dense_cols] = data[dense_cols].fillna(0) #填充空缺值
data[sparse_cols] = data[sparse_cols].fillna('-996')


#criteo比赛冠军分享的一种离散化思路，不用纠结其原理，大家也可以试试别的离散化手段
def convert_numeric_feature(val):
    v = int(val)
    if v > 2:
        return int(np.log(v)**2)
    else:
        return v - 2
        
for col in tqdm(dense_cols):  #将离散化dense特征列设置为新的sparse特征列
    sparse_cols.append(col + "_sparse")
    data[col + "_sparse"] = data[col].apply(lambda x: convert_numeric_feature(x))

scaler = MinMaxScaler()  #对dense特征列归一化
data[dense_cols] = scaler.fit_transform(data[dense_cols])

for col in tqdm(sparse_cols):  #sparse特征编码
    lbe = LabelEncoder()
    data[col] = lbe.fit_transform(data[col])

#重点：将每个特征定义为torch-rechub所支持的特征基类，dense特征只需指定特征名，sparse特征需指定特征名、特征取值个数(vocab_size)、embedding维度(embed_dim)
dense_features = [DenseFeature(feature_name) for feature_name in dense_cols]
sparse_features = [SparseFeature(feature_name, vocab_size=data[feature_name].nunique(), embed_dim=16) for feature_name in sparse_cols]
y = data["label"]
del data["label"]
x = data
```

    100%|██████████| 13/13 [00:00<00:00, 855.60it/s]
    100%|██████████| 39/39 [00:00<00:00, 2674.02it/s]
    


```python
# 构建模型输入所需要的dataloader，区分验证集、测试集，指定batch大小
#split_ratio=[0.7,0.1] 指的是训练集占比70%，验证集占比10%，剩下的全部为测试集
dg = DataGenerator(x, y) 
train_dataloader, val_dataloader, test_dataloader = dg.generate_dataloader(split_ratio=[0.7, 0.1], batch_size=256, num_workers=8)
```

    the samples of train : val : test are  80 : 11 : 24
    

### 训练模型

训练一个DeepFM模型，只需要指定DeepFM的模型结构参数，学习率等训练参数。
对于DeepFM而言，主要参数如下：

- deep_features指用deep模块训练的特征（兼容dense和sparse），
- fm_features指用fm模块训练的特征，只能传入sparse类型
- mlp_params指定deep模块中，MLP层的参数




```python
from torch_rechub.models.ranking import DeepFM
from torch_rechub.trainers import CTRTrainer

#定义模型
model = DeepFM(
        deep_features=dense_features+sparse_features,
        fm_features=sparse_features,
        mlp_params={"dims": [256, 128], "dropout": 0.2, "activation": "relu"},
    )

# 模型训练，需要学习率、设备等一般的参数，此外我们还支持earlystoping策略，及时发现过拟合
ctr_trainer = CTRTrainer(
    model,
    optimizer_params={"lr": 1e-4, "weight_decay": 1e-5},
    n_epoch=1,
    earlystop_patience=3,
    device='cpu', #如果有gpu，可设置成cuda:0
    model_path='./', #模型存储路径
)
ctr_trainer.fit(train_dataloader, val_dataloader)

# 查看在测试集上的性能
auc = ctr_trainer.evaluate(ctr_trainer.model, test_dataloader)
print(f'test auc: {auc}')
```

    epoch: 0
    

    train: 100%|██████████| 1/1 [00:08<00:00,  8.24s/it]
    validation: 100%|██████████| 1/1 [00:13<00:00, 13.86s/it]
    

    epoch: 0 validation: auc: 0.3333333333333333
    

    validation: 100%|██████████| 1/1 [00:07<00:00,  7.94s/it]

    test auc: 0.768421052631579
    

    
    

### 使用其他的排序模型训练Criteo


```python
#定义相应的模型，用同样的方式训练
model = WideDeep(wide_features=dense_features, deep_features=sparse_features, mlp_params={"dims": [256, 128], "dropout": 0.2, "activation": "relu"})

model = DCN(features=dense_features + sparse_features, n_cross_layers=3, mlp_params={"dims": [256, 128]})
```

### 从调包到自定义自己的模型
恭喜朋友成功运行了DeepFM模型，并得到了CTR推荐的结果。
接下来我们考虑如何实现自己的DeepFM模型。
由于FM，MLP，LR，Embedding等基础模块被许多推荐模型共用，因此torch_rechub也帮我们集成好了这些小模块。我们在basic.layers中import即可。



```python
from torch_rechub.basic.layers import FM, MLP, LR, EmbeddingLayer

```

有了基础的模块之后，搭建自己的模型就会很方便了，torch-rechub是基于pytorch的因此我们可以像传统的torch模型一样，定义一个model类，然后写好初始化和farward函数即可。


```python
class MyDeepFM(torch.nn.Module):
  # Deep和FM为两部分，分别处理不同的特征，因此传入的参数要有两种特征，由此我们得到参数deep_features,fm_features
  # 此外神经网络类的模型中，基本组成原件为MLP多层感知机，多层感知机的参数也需要传进来，即为mlp_params
  def __init__(self, deep_features, fm_features, mlp_params):
    super().__init__()
    self.deep_features = deep_features
    self.fm_features = fm_features
    self.deep_dims = sum([fea.embed_dim for fea in deep_features])
    self.fm_dims = sum([fea.embed_dim for fea in fm_features])
    # LR建模一阶特征交互
    self.linear = LR(self.fm_dims)
    # FM建模二阶特征交互
    self.fm = FM(reduce_sum=True)
    # 对特征做嵌入表征
    self.embedding = EmbeddingLayer(deep_features + fm_features)
    self.mlp = MLP(self.deep_dims, **mlp_params)

  def forward(self, x):
    input_deep = self.embedding(x, self.deep_features, squeeze_dim=True)  #[batch_size, deep_dims]
    input_fm = self.embedding(x, self.fm_features, squeeze_dim=False)  #[batch_size, num_fields, embed_dim]

    y_linear = self.linear(input_fm.flatten(start_dim=1))
    y_fm = self.fm(input_fm)
    y_deep = self.mlp(input_deep)  #[batch_size, 1]
    # 最终的预测值为一阶特征交互，二阶特征交互，以及深层模型的组合
    y = y_linear + y_fm + y_deep
    # 利用sigmoid来将预测得分规整到0,1区间内
    return torch.sigmoid(y.squeeze(1))
```

同样的，可以使用torch-rechub提供的trainer进行模型训练和模型评估


```python
model = MyDeepFM(
        deep_features=dense_features+sparse_features,
        fm_features=sparse_features,
        mlp_params={"dims": [256, 128], "dropout": 0.2, "activation": "relu"},
    )
# 模型训练，需要学习率、设备等一般的参数，此外我们还支持earlystoping策略，及时发现过拟合
ctr_trainer = CTRTrainer(
    model,
    optimizer_params={"lr": 1e-4, "weight_decay": 1e-5},
    n_epoch=1,
    earlystop_patience=3,
    device='cpu',
    model_path='./',
)
ctr_trainer.fit(train_dataloader, val_dataloader)

# 查看在测试集上的性能
auc = ctr_trainer.evaluate(ctr_trainer.model, test_dataloader)
print(f'test auc: {auc}')
```

    epoch: 0
    

    train: 100%|██████████| 1/1 [00:07<00:00,  7.67s/it]
    validation: 100%|██████████| 1/1 [00:10<00:00, 10.79s/it]
    

    epoch: 0 validation: auc: 0.5
    

    validation: 100%|██████████| 1/1 [00:14<00:00, 14.61s/it]

    test auc: 0.25263157894736843
    

    
    
