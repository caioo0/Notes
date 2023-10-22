# Torch-Rechub Tutorial：Multi-Task

- 场景：精排（多任务学习）
- 模型：ESMM、MMOE
- 数据：Ali-CCP数据集
- 学习目标

  - 学会使用torch-rechub训练一个ESMM模型
  - 学会基于torch-rechub训练一个MMOE模型
- 学习材料：

  - 多任务模型介绍：https://datawhalechina.github.io/fun-rec/#/ch02/ch2.2/ch2.2.5/2.2.5.0
  - Ali-CCP数据集官网：https://tianchi.aliyun.com/dataset/dataDetail?dataId=408
- 注意事项：本教程模型部分的超参数并未调优，欢迎小伙伴在学完教程后参与调参和在全量数据上进行测评工作

```python
#安装torch-rechub
!pip install torch-rechub
```

## Ali-CCP数据集介绍

- [原始数据](https://tianchi.aliyun.com/dataset/dataDetail?dataId=408)：原始数据采集自手机淘宝移动客户端的推荐系统日志，一共有23个sparse特征，8个dense特征，包含“点击”、“购买”两个标签，各特征列的含义参考学习材料中的Ali-CCP数据集官网上的详细描述
- [全量数据](https://cowtransfer.com/s/1903cab699fa49)：我们已经完成对原始数据集的处理，包括对sparse特征进行Lable Encode，dense特征采用归一化处理等。预处理脚本见torch-rechub/examples/ranking/data/ali-ccp/preprocess_ali_ccp.py
- [采样数据](https://github.com/datawhalechina/torch-rechub/tree/main/examples/ranking/data/ali-ccp)：从全量数据集采样的小数据集，供大家调试代码和学习使用，因此本次教程使用采样数据

```python
#使用pandas加载数据
import pandas as pd
data_path = '../examples/ranking/data/ali-ccp' #数据存放文件夹
df_train = pd.read_csv(data_path + '/ali_ccp_train_sample.csv') #加载训练集
df_val = pd.read_csv(data_path + '/ali_ccp_val_sample.csv') #加载验证集
df_test = pd.read_csv(data_path + '/ali_ccp_test_sample.csv') #加载测试集
print("train : val : test = %d %d %d" % (len(df_train), len(df_val), len(df_test)))
#查看数据，其中'click'、'purchase'为标签列，'D'开头为dense特征列，其余为sparse特征，各特征列的含义参考官网描述
print(df_train.head(5)) 
```

train : val : test = 100 50 50
   click  purchase  101  121  122  124  125  126  127  128  ...  127_14  \
0      0         0    1    1    1    1    1    0    1    1  ...       1   
1      0         0    1    1    1    1    1    0    1    1  ...       1   
2      1         1    1    1    1    1    1    0    1    1  ...       1   
3      0         0    1    1    1    1    1    0    1    1  ...       1   
4      0         0    1    1    1    1    1    0    1    1  ...       1   

   150_14  D109_14  D110_14  D127_14  D150_14     D508   D509    D702     D853  
0       1   0.4734    0.562   0.0856   0.1902  0.07556  0.000  0.0000  0.00000  
1       1   0.4734    0.562   0.0856   0.1902  0.00000  0.000  0.0000  0.00000  
2       1   0.4734    0.562   0.0856   0.1902  0.56050  0.256  0.4626  0.34400  
3       1   0.4734    0.562   0.0856   0.1902  0.26150  0.000  0.0000  0.12213  
4       1   0.4734    0.562   0.0856   0.1902  0.35910  0.000  0.0000  0.00000  

[5 rows x 33 columns]
### 使用torch-rechub训练ESMM模型

#### 数据预处理

在数据预处理过程通常需要:

- 对稀疏分类特征进行Lable Encode
- 对于数值特征进行分桶或者归一化

由于本教程中的采样数据以及全量数据已经进行预处理，因此加载数据集可以直接使用。

本次的多任务模型的任务是预测点击和购买标签，是推荐系统中典型的CTR和CVR预测任务。

```python
train_idx, val_idx = df_train.shape[0], df_train.shape[0] + df_val.shape[0]
data = pd.concat([df_train, df_val, df_test], axis=0)
#task 1 (as cvr): main task, purchase prediction
#task 2(as ctr): auxiliary task, click prediction
data.rename(columns={'purchase': 'cvr_label', 'click': 'ctr_label'}, inplace=True)
data["ctcvr_label"] = data['cvr_label'] * data['ctr_label']
```
#### 定义模型

定义一个模型需要指定模型结构参数,需要哪些参数可查看对应模型的定义部分。
对于ESMM而言，主要参数如下：

- user_features指用户侧的特征，只能传入sparse类型（论文中需要分别对user和item侧的特征进行sum_pooling操作）
- item_features指用item侧的特征，只能传入sparse类型
- cvr_params指定CVR Tower中MLP层的参数
- ctr_params指定CTR Tower中MLP层的参数

```python
from torch_rechub.models.multi_task import ESMM
from torch_rechub.basic.features import DenseFeature, SparseFeature

col_names = data.columns.values.tolist()
dense_cols = ['D109_14', 'D110_14', 'D127_14', 'D150_14', 'D508', 'D509', 'D702', 'D853']
sparse_cols = [col for col in col_names if col not in dense_cols and col not in ['cvr_label', 'ctr_label']]
print("sparse cols:%d dense cols:%d" % (len(sparse_cols), len(dense_cols)))
label_cols = ['cvr_label', 'ctr_label', "ctcvr_label"]  #the order of 3 labels must fixed as this
used_cols = sparse_cols #ESMM only for sparse features in origin paper
item_cols = ['129', '205', '206', '207', '210', '216']  #assumption features split for user and item
user_cols = [col for col in used_cols if col not in item_cols]
user_features = [SparseFeature(col, data[col].max() + 1, embed_dim=16) for col in user_cols]
item_features = [SparseFeature(col, data[col].max() + 1, embed_dim=16) for col in item_cols]

model = ESMM(user_features, item_features, cvr_params={"dims": [16, 8]}, ctr_params={"dims": [16, 8]})
```
#### 构建dataloader

构建dataloader通常由

1. 构建输入字典（字典的键为定义模型时采用的特征名，值为对应特征的数据）
2. 通过字典构建相应的dataset和dataloader

```python
from torch_rechub.utils.data import DataGenerator

x_train, y_train = {name: data[name].values[:train_idx] for name in used_cols}, data[label_cols].values[:train_idx]
x_val, y_val = {name: data[name].values[train_idx:val_idx] for name in used_cols}, data[label_cols].values[train_idx:val_idx]
x_test, y_test = {name: data[name].values[val_idx:] for name in used_cols}, data[label_cols].values[val_idx:]
dg = DataGenerator(x_train, y_train)
train_dataloader, val_dataloader, test_dataloader = dg.generate_dataloader(x_val=x_val, y_val=y_val, 
                                      x_test=x_test, y_test=y_test, batch_size=1024)
```
#### 训练模型及测试

- 训练模型通过相应的trainer进行，对于多任务的MTLTrainer需要设置任务的类型、优化器的超参数和优化策略等。
- 完成模型训练后对测试集进行测试

```python
import torch
import os
from torch_rechub.trainers import MTLTrainer
device = 'cuda' if torch.cuda.is_available() else 'cpu'
learning_rate = 1e-3
epoch = 1 #10
weight_decay = 1e-5
save_dir = '../examples/ranking/data/ali-ccp/saved'
if not os.path.exists(save_dir):
    os.makedirs(save_dir)
task_types = ["classification", "classification"] #CTR与CVR均为二分类任务
mtl_trainer = MTLTrainer(model, task_types=task_types, 
              optimizer_params={"lr": learning_rate, "weight_decay": weight_decay}, 
              n_epoch=epoch, earlystop_patience=1, device=device, model_path=save_dir)
mtl_trainer.fit(train_dataloader, val_dataloader)
auc = mtl_trainer.evaluate(mtl_trainer.model, test_dataloader)
print(f'test auc: {auc}')
```
train: 100%|██████████| 1/1 [00:11<00:00, 11.81s/it]


train loss:  {'task_0:': 0.8062036633491516, 'task_1:': 0.7897741794586182}


validation: 100%|██████████| 1/1 [00:08<00:00,  8.44s/it]


epoch: 0 validation scores:  [0.9183673469387755, 0.553191489361702]


validation: 100%|██████████| 1/1 [00:07<00:00,  7.99s/it]

test auc: [0.4693877551020408, 0.8333333333333333]
### 使用torch-rechub训练MMOE模型

训练MMOE模型的流程与ESMM模型十分相似

需要注意的是MMOE模型同时支持dense和sparse特征作为输入,以及支持分类和回归任务混合

```python
from torch_rechub.models.multi_task import MMOE
# 定义模型
used_cols = sparse_cols + dense_cols
features = [SparseFeature(col, data[col].max()+1, embed_dim=4)for col in sparse_cols] \
                   + [DenseFeature(col) for col in dense_cols]
model = MMOE(features, task_types, 8, expert_params={"dims": [16]}, tower_params_list=[{"dims": [8]}, {"dims": [8]}])
#构建dataloader
label_cols = ['cvr_label', 'ctr_label']
x_train, y_train = {name: data[name].values[:train_idx] for name in used_cols}, data[label_cols].values[:train_idx]
x_val, y_val = {name: data[name].values[train_idx:val_idx] for name in used_cols}, data[label_cols].values[train_idx:val_idx]
x_test, y_test = {name: data[name].values[val_idx:] for name in used_cols}, data[label_cols].values[val_idx:]
dg = DataGenerator(x_train, y_train)
train_dataloader, val_dataloader, test_dataloader = dg.generate_dataloader(x_val=x_val, y_val=y_val, 
                                      x_test=x_test, y_test=y_test, batch_size=1024)
#训练模型及评估
mtl_trainer = MTLTrainer(model, task_types=task_types, optimizer_params={"lr": learning_rate, "weight_decay": weight_decay}, n_epoch=epoch, earlystop_patience=30, device=device, model_path=save_dir)
mtl_trainer.fit(train_dataloader, val_dataloader)
auc = mtl_trainer.evaluate(mtl_trainer.model, test_dataloader)
```
train: 100%|██████████| 1/1 [00:07<00:00,  7.90s/it]


train loss:  {'task_0:': 0.732882022857666, 'task_1:': 0.6457288861274719}


validation: 100%|██████████| 1/1 [00:07<00:00,  7.84s/it]


epoch: 0 validation scores:  [0.9591836734693877, 0.5354609929078014]


validation: 100%|██████████| 1/1 [00:07<00:00,  7.62s/it]
