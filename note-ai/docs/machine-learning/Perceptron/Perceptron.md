# 感知机

1．感知机是根据输入实例的特征向量$x$对其进行二类分类的线性分类模型：

$$
f(x)=\operatorname{sign}(w \cdot x+b)

$$

感知机模型对应于输入空间（特征空间）中的分离超平面$w \cdot x+b=0$。

2．感知机学习的策略是极小化损失函数：

$$
\min _{w, b} L(w, b)=-\sum_{x_{i} \in M} y_{i}\left(w \cdot x_{i}+b\right)

$$

损失函数对应于误分类点到分离超平面的总距离。

3．感知机学习算法是基于随机梯度下降法的对损失函数的最优化算法，有原始形式和对偶形式。算法简单且易于实现。原始形式中，首先任意选取一个超平面，然后用梯度下降法不断极小化目标函数。在这个过程中一次随机选取一个误分类点使其梯度下降。

4．当训练数据集线性可分时，感知机学习算法是收敛的。感知机算法在训练数据集上的误分类次数$k$满足不等式：

$$
k \leqslant\left(\frac{R}{\gamma}\right)^{2}

$$

当训练数据集线性可分时，感知机学习算法存在无穷多个解，其解由于不同的初值或不同的迭代顺序而可能有所不同。

### sigmod 函数

$$
\sigma(z) = \frac{1}{1+e^{-z}}

$$

sigmoid 函数是一个常用的逻辑函数，形状类似于字母 S。在 Python 中，我们可以使用 NumPy 库中的 exp 函数来实现它。

以下是一个简单的 Python 函数，用于计算 sigmoid 函数：

```python
import numpy as np  
  
def sigmoid(x):  
    return 1 / (1 + np.exp(-x))
```

也可以使用原生语句实现：

```python
import math  
  
def sigmoid(x):  
    return 1 / (1 + math.exp(-x))
```

### 二分类模型

$f(x) = sign(w\cdot x + b)$

$\operatorname{sign}(x)=\left\{\begin{array}{ll}{+1,} & {x \geqslant 0} \\ {-1,} & {x<0}\end{array}\right.$

给定训练集：

$T=\left\{\left(x_{1}, y_{1}\right),\left(x_{2}, y_{2}\right), \cdots,\left(x_{N}, y_{N}\right)\right\}$

定义感知机的损失函数

$L(w, b)=-\sum_{x_{i} \in M} y_{i}\left(w \cdot x_{i}+b\right)$

---

#### 算法

随即梯度下降法 Stochastic Gradient Descent

随机抽取一个误分类点使其梯度下降。

$w = w + \eta y_{i}x_{i}$

$b = b + \eta y_{i}$

当实例点被误分类，即位于分离超平面的错误侧，则调整$w$, $b$的值，使分离超平面向该无分类点的一侧移动，直至误分类点被正确分类

### iris实例：

[iris数据集](https://scikit-learn.org/stable/modules/generated/sklearn.datasets.load_iris.html)

**pandas**

- Pandas 官网 https://pandas.pydata.org/
- Pandas 源代码：https://github.com/pandas-dev/pandas

```python
import pandas as pd
import numpy as np 
from sklearn.datasets import load_iris
import matplotlib.pyplot as plt
%matplotlib inline
```

```python
# load data 

iris = load_iris()
df = pd.DataFrame(iris.data,columns = iris.feature_names)
df
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
      <th>sepal length (cm)</th>
      <th>sepal width (cm)</th>
      <th>petal length (cm)</th>
      <th>petal width (cm)</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>5.1</td>
      <td>3.5</td>
      <td>1.4</td>
      <td>0.2</td>
    </tr>
    <tr>
      <th>1</th>
      <td>4.9</td>
      <td>3.0</td>
      <td>1.4</td>
      <td>0.2</td>
    </tr>
    <tr>
      <th>2</th>
      <td>4.7</td>
      <td>3.2</td>
      <td>1.3</td>
      <td>0.2</td>
    </tr>
    <tr>
      <th>3</th>
      <td>4.6</td>
      <td>3.1</td>
      <td>1.5</td>
      <td>0.2</td>
    </tr>
    <tr>
      <th>4</th>
      <td>5.0</td>
      <td>3.6</td>
      <td>1.4</td>
      <td>0.2</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>145</th>
      <td>6.7</td>
      <td>3.0</td>
      <td>5.2</td>
      <td>2.3</td>
    </tr>
    <tr>
      <th>146</th>
      <td>6.3</td>
      <td>2.5</td>
      <td>5.0</td>
      <td>1.9</td>
    </tr>
    <tr>
      <th>147</th>
      <td>6.5</td>
      <td>3.0</td>
      <td>5.2</td>
      <td>2.0</td>
    </tr>
    <tr>
      <th>148</th>
      <td>6.2</td>
      <td>3.4</td>
      <td>5.4</td>
      <td>2.3</td>
    </tr>
    <tr>
      <th>149</th>
      <td>5.9</td>
      <td>3.0</td>
      <td>5.1</td>
      <td>1.8</td>
    </tr>
  </tbody>
</table>
<p>150 rows × 4 columns</p>
</div>

```python
df['label'] = iris.target
df
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
      <th>sepal length (cm)</th>
      <th>sepal width (cm)</th>
      <th>petal length (cm)</th>
      <th>petal width (cm)</th>
      <th>label</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>5.1</td>
      <td>3.5</td>
      <td>1.4</td>
      <td>0.2</td>
      <td>0</td>
    </tr>
    <tr>
      <th>1</th>
      <td>4.9</td>
      <td>3.0</td>
      <td>1.4</td>
      <td>0.2</td>
      <td>0</td>
    </tr>
    <tr>
      <th>2</th>
      <td>4.7</td>
      <td>3.2</td>
      <td>1.3</td>
      <td>0.2</td>
      <td>0</td>
    </tr>
    <tr>
      <th>3</th>
      <td>4.6</td>
      <td>3.1</td>
      <td>1.5</td>
      <td>0.2</td>
      <td>0</td>
    </tr>
    <tr>
      <th>4</th>
      <td>5.0</td>
      <td>3.6</td>
      <td>1.4</td>
      <td>0.2</td>
      <td>0</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>145</th>
      <td>6.7</td>
      <td>3.0</td>
      <td>5.2</td>
      <td>2.3</td>
      <td>2</td>
    </tr>
    <tr>
      <th>146</th>
      <td>6.3</td>
      <td>2.5</td>
      <td>5.0</td>
      <td>1.9</td>
      <td>2</td>
    </tr>
    <tr>
      <th>147</th>
      <td>6.5</td>
      <td>3.0</td>
      <td>5.2</td>
      <td>2.0</td>
      <td>2</td>
    </tr>
    <tr>
      <th>148</th>
      <td>6.2</td>
      <td>3.4</td>
      <td>5.4</td>
      <td>2.3</td>
      <td>2</td>
    </tr>
    <tr>
      <th>149</th>
      <td>5.9</td>
      <td>3.0</td>
      <td>5.1</td>
      <td>1.8</td>
      <td>2</td>
    </tr>
  </tbody>
</table>
<p>150 rows × 5 columns</p>
</div>

```python
df.columns = [
    'sepal length', 'sepal width', 'petal length', 'petal width', 'label'
]
df.label.value_counts()
```
0    50
1    50
2    50
Name: label, dtype: int64
```python
plt.scatter(df[:50]['sepal length'], df[:50]['sepal width'], label='0')
plt.scatter(df[50:100]['sepal length'], df[50:100]['sepal width'], label='1')
plt.xlabel('sepal length')
plt.ylabel('sepal width')
plt.legend()
```
<matplotlib.legend.Legend at 0x19ba5dd96f0>
![png](output_10_1.png)

```python
data = np.array(df.iloc[:100,[0,1,-1]]) # 通过位置选择前100行的数据
```
```python
X,y = data[:,:-1],data[:,-1]
```
```python
y = np.array([1 if i == 1 else -1 for i in y])
```
### Perceptron

```python
# 数据线性可分，二分类数据 
# 此处为一元一次线性方程


# 定义单层感知机
class Model:
    def __init__(self):
        self.w = np.ones(len(data[0]) - 1, dtype=np.float32)
        self.b = 0
        self.l_rate = 0.01
        # self.data = data

    def sign(self, x, w, b):
        y = np.dot(x, w) + b
        return y

    # 随机梯度下降法
    def fit(self, X_train, y_train):
        is_wrong = False
        while not is_wrong:
            wrong_count = 0
            for d in range(len(X_train)):
                X = X_train[d]
                y = y_train[d]
                if y * self.sign(X, self.w, self.b) <= 0:
                    self.w = self.w + self.l_rate * np.dot(y, X)
                    self.b = self.b + self.l_rate * y
                    wrong_count += 1
            if wrong_count == 0:
                is_wrong = True
        return 'Perceptron Model!'

    def score(self):
        pass
```
```python
perceptron = Model()
perceptron.fit(X, y)
```
'Perceptron Model!'
```python
perceptron.w
```
array([ 0.78, -1.  ])
```python
perceptron.b
```
-1.2100000000000009
```python
x_points = np.linspace(4, 7, 10)
y_ = -(perceptron.w[0] * x_points + perceptron.b) / perceptron.w[1]
plt.plot(x_points, y_)

plt.plot(data[:50, 0], data[:50, 1], 'bo', color='blue', label='0')
plt.plot(data[50:100, 0], data[50:100, 1], 'bo', color='orange', label='1')
plt.xlabel('sepal length')
plt.ylabel('sepal width')
plt.legend()

```
C:\Users\Jochoi\AppData\Local\Temp\ipykernel_27564\1528903297.py:5: UserWarning: color is redundantly defined by the 'color' keyword argument and the fmt string "bo" (-> color='b'). The keyword argument will take precedence.
  plt.plot(data[:50, 0], data[:50, 1], 'bo', color='blue', label='0')
C:\Users\Jochoi\AppData\Local\Temp\ipykernel_27564\1528903297.py:6: UserWarning: color is redundantly defined by the 'color' keyword argument and the fmt string "bo" (-> color='b'). The keyword argument will take precedence.
  plt.plot(data[50:100, 0], data[50:100, 1], 'bo', color='orange', label='1')





<matplotlib.legend.Legend at 0x19ba83e1930>
![png](output_19_2.png)

### scikit-learn实例

```python
import sklearn
from sklearn.linear_model import Perceptron
```
```python
sklearn.__version__
```
'1.2.1'
```python
clf =Perceptron(fit_intercept =True,max_iter=1000,shuffle=True)

clf.fit(X,y)
```
<style>#sk-container-id-1 {color: black;background-color: white;}#sk-container-id-1 pre{padding: 0;}#sk-container-id-1 div.sk-toggleable {background-color: white;}#sk-container-id-1 label.sk-toggleable__label {cursor: pointer;display: block;width: 100%;margin-bottom: 0;padding: 0.3em;box-sizing: border-box;text-align: center;}#sk-container-id-1 label.sk-toggleable__label-arrow:before {content: "▸";float: left;margin-right: 0.25em;color: #696969;}#sk-container-id-1 label.sk-toggleable__label-arrow:hover:before {color: black;}#sk-container-id-1 div.sk-estimator:hover label.sk-toggleable__label-arrow:before {color: black;}#sk-container-id-1 div.sk-toggleable__content {max-height: 0;max-width: 0;overflow: hidden;text-align: left;background-color: #f0f8ff;}#sk-container-id-1 div.sk-toggleable__content pre {margin: 0.2em;color: black;border-radius: 0.25em;background-color: #f0f8ff;}#sk-container-id-1 input.sk-toggleable__control:checked~div.sk-toggleable__content {max-height: 200px;max-width: 100%;overflow: auto;}#sk-container-id-1 input.sk-toggleable__control:checked~label.sk-toggleable__label-arrow:before {content: "▾";}#sk-container-id-1 div.sk-estimator input.sk-toggleable__control:checked~label.sk-toggleable__label {background-color: #d4ebff;}#sk-container-id-1 div.sk-label input.sk-toggleable__control:checked~label.sk-toggleable__label {background-color: #d4ebff;}#sk-container-id-1 input.sk-hidden--visually {border: 0;clip: rect(1px 1px 1px 1px);clip: rect(1px, 1px, 1px, 1px);height: 1px;margin: -1px;overflow: hidden;padding: 0;position: absolute;width: 1px;}#sk-container-id-1 div.sk-estimator {font-family: monospace;background-color: #f0f8ff;border: 1px dotted black;border-radius: 0.25em;box-sizing: border-box;margin-bottom: 0.5em;}#sk-container-id-1 div.sk-estimator:hover {background-color: #d4ebff;}#sk-container-id-1 div.sk-parallel-item::after {content: "";width: 100%;border-bottom: 1px solid gray;flex-grow: 1;}#sk-container-id-1 div.sk-label:hover label.sk-toggleable__label {background-color: #d4ebff;}#sk-container-id-1 div.sk-serial::before {content: "";position: absolute;border-left: 1px solid gray;box-sizing: border-box;top: 0;bottom: 0;left: 50%;z-index: 0;}#sk-container-id-1 div.sk-serial {display: flex;flex-direction: column;align-items: center;background-color: white;padding-right: 0.2em;padding-left: 0.2em;position: relative;}#sk-container-id-1 div.sk-item {position: relative;z-index: 1;}#sk-container-id-1 div.sk-parallel {display: flex;align-items: stretch;justify-content: center;background-color: white;position: relative;}#sk-container-id-1 div.sk-item::before, #sk-container-id-1 div.sk-parallel-item::before {content: "";position: absolute;border-left: 1px solid gray;box-sizing: border-box;top: 0;bottom: 0;left: 50%;z-index: -1;}#sk-container-id-1 div.sk-parallel-item {display: flex;flex-direction: column;z-index: 1;position: relative;background-color: white;}#sk-container-id-1 div.sk-parallel-item:first-child::after {align-self: flex-end;width: 50%;}#sk-container-id-1 div.sk-parallel-item:last-child::after {align-self: flex-start;width: 50%;}#sk-container-id-1 div.sk-parallel-item:only-child::after {width: 0;}#sk-container-id-1 div.sk-dashed-wrapped {border: 1px dashed gray;margin: 0 0.4em 0.5em 0.4em;box-sizing: border-box;padding-bottom: 0.4em;background-color: white;}#sk-container-id-1 div.sk-label label {font-family: monospace;font-weight: bold;display: inline-block;line-height: 1.2em;}#sk-container-id-1 div.sk-label-container {text-align: center;}#sk-container-id-1 div.sk-container {/* jupyter's `normalize.less` sets `[hidden] { display: none; }` but bootstrap.min.css set `[hidden] { display: none !important; }` so we also need the `!important` here to be able to override the default hidden behavior on the sphinx rendered scikit-learn.org. See: https://github.com/scikit-learn/scikit-learn/issues/21755 */display: inline-block !important;position: relative;}#sk-container-id-1 div.sk-text-repr-fallback {display: none;}</style><div id="sk-container-id-1" class="sk-top-container"><div class="sk-text-repr-fallback"><pre>Perceptron()</pre><b>In a Jupyter environment, please rerun this cell to show the HTML representation or trust the notebook. <br />On GitHub, the HTML representation is unable to render, please try loading this page with nbviewer.org.</b></div><div class="sk-container" hidden><div class="sk-item"><div class="sk-estimator sk-toggleable"><input class="sk-toggleable__control sk-hidden--visually" id="sk-estimator-id-1" type="checkbox" checked><label for="sk-estimator-id-1" class="sk-toggleable__label sk-toggleable__label-arrow">Perceptron</label><div class="sk-toggleable__content"><pre>Perceptron()</pre></div></div></div></div></div>

```python
# Weights assigned to the features.
print(clf.coef_)
```
[[ 23.2 -38.7]]
```python
# 截距 Constants in decision function.
print(clf.intercept_)
```
[-5.]
```python
# 画布大小
plt.figure(figsize=(10,10))

# 中文标题
plt.rcParams['font.sans-serif']=['SimHei']
plt.rcParams['axes.unicode_minus'] = False
plt.title('鸢尾花线性数据示例')

plt.scatter(data[:50, 0], data[:50, 1], c='b', label='Iris-setosa',)
plt.scatter(data[50:100, 0], data[50:100, 1], c='orange', label='Iris-versicolor')

# 画感知机的线
x_ponits = np.arange(4, 8)
y_ = -(clf.coef_[0][0]*x_ponits + clf.intercept_)/clf.coef_[0][1]
plt.plot(x_ponits, y_)

# 其他部分
plt.legend()  # 显示图例
plt.grid(False)  # 不显示网格
plt.xlabel('sepal length')
plt.ylabel('sepal width')
plt.legend()
```
<matplotlib.legend.Legend at 0x19ba8763f70>
![png](output_26_1.png)

**注意 !**

在上图中，有一个位于左下角的蓝点没有被正确分类，这是因为 SKlearn 的 Perceptron 实例中有一个`tol`参数。

`tol` 参数规定了如果本次迭代的损失和上次迭代的损失之差小于一个特定值时，停止迭代。所以我们需要设置 `tol=None` 使之可以继续迭代：

```python
clf = Perceptron(fit_intercept=True, 
                 max_iter=1000,
                 tol=None,
                 shuffle=True)
clf.fit(X, y)

# 画布大小
plt.figure(figsize=(10,10))

# 中文标题
plt.rcParams['font.sans-serif']=['SimHei']
plt.rcParams['axes.unicode_minus'] = False
plt.title('鸢尾花线性数据示例')

plt.scatter(data[:50, 0], data[:50, 1], c='b', label='Iris-setosa',)
plt.scatter(data[50:100, 0], data[50:100, 1], c='orange', label='Iris-versicolor')

# 画感知机的线
x_ponits = np.arange(4, 8)
y_ = -(clf.coef_[0][0]*x_ponits + clf.intercept_)/clf.coef_[0][1]
plt.plot(x_ponits, y_)

# 其他部分
plt.legend()  # 显示图例
plt.grid(False)  # 不显示网格
plt.xlabel('sepal length')
plt.ylabel('sepal width')
plt.legend()
```
<matplotlib.legend.Legend at 0x19ba8821390>
![png](output_28_1.png)

## mnist实例

《神经网络和深度学习》练习代码：git@github.com:MichalDanielDobrzanski/DeepLearningPython.git

这里给出另一种写法：

mnist数据集由6万张训练数据和1万张测试数据组成，这里提供百度网盘下载地址：

链接: https://pan.baidu.com/s/1eI0G5a6j_v7k9XRho4v0PQ?pwd=hzxy

提取码: hzxy 

```python
# mnist_loader.py

# -*- coding: utf-8 -*-
"""
Author: Caioo
"""


import torch
import torchvision.datasets as dsets
import torchvision.transforms as transforms

batch_size = 64


def load_data():
    """通过调用torchvision中datasets模块来导入MNIST数据集中的训练集和测试集，
    将导入的训练集通过DataLoader加载为train_loader，
    测试集总共有10，000的样本数，分别取5，000作为验证集和测试集，对验证机和测试
    集中样本打乱通过DataLoader加载为validation_loader和test_loader
    """
    train_dataset = dsets.MNIST(root='./data', train=True, transform=transforms.ToTensor(), download=True)
    test_dataset = dsets.MNIST(root='./data', train=False, transform=transforms.ToTensor())

    train_loader = torch.utils.data.DataLoader(dataset=train_dataset, batch_size=batch_size, shuffle=True)

    indices = range(len(test_dataset))
    indices_val = indices[:5000]
    indices_test = indices[5000:]

    sampler_val = torch.utils.data.sampler.SubsetRandomSampler(indices_val)
    sampler_test = torch.utils.data.sampler.SubsetRandomSampler(indices_test)

    validation_loader = torch.utils.data.DataLoader(dataset=test_dataset, batch_size=batch_size, shuffle=False,
                                                    sampler=sampler_val)
    test_loader = torch.utils.data.DataLoader(dataset=test_dataset, batch_size=batch_size, shuffle=False,
                                              sampler=sampler_test)

    return train_loader, validation_loader, test_loader
```
```python

## network.py

# -*- coding: utf-8 -*-
"""通过pytorch中神经网络的模块和函数来构建对MNIST数据集网络的构建、
训练、验证、和测试，整个过程使用了三层的神经元的网络来建立网络；最后
测试集中的正确率有94.36%左右，通过增加网络层数，调整参数，迭代次数，
损失函数等等都能对提高正确率起一定效果

Author: Caioo0
"""

import torch
import torch.nn as nn
from torch.autograd import Variable
import torch.optim as optim
import mnist_loader


class Network(nn.Module):
    """这里以[784 30 10]三层神经网络为例
    """
    def __init__(self, sizes):
        super(Network, self).__init__()
        self.sizes = sizes
        self.layer1 = nn.Linear(sizes[0], sizes[1])
        self.layer2 = nn.Linear(sizes[1], sizes[2])

    def forward(self, a):
        a = a.view(-1, self.sizes[0])  # view函数将输入Tensor转换成（64, 784）
        a = self.layer1(a)
        a = self.layer2(a)
        a = torch.log_softmax(a, dim=1)
        return a


def rightness(output, target):
    """输入网络的输出Tensor和目标Tensor，
    比较网络的输出Tensor和目标Tensor中对应相等的结果，
    返回比较结果中匹配正确的个数和整个输出或者目标Tensor
    的长度
    """
    rights = 0
    for index in range(len(target.data)):
        if torch.argmax(output[index]) == target.data[index]:
            rights += 1
    return rights, len(target.data)


def train_model(train_loader, epochs, eta):
    """本函数的功能是训练模型，使用交叉熵的损失函数，和
    随机梯度下降的优化算法，学习率为0.001，动量为0.9
    开始训练循环
    """
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.SGD(net.parameters(), lr=eta, momentum=0.9)

    for epoch in range(epochs):
        train_rights = []  # 记录每次迭代正确的结果和总样本

        for batch_idx, (data, target) in enumerate(train_loader):
            data, target = Variable(data), Variable(target)
            net.train()

            output = net(data)
            loss = criterion(output, target)
            optimizer.zero_grad()  # 清空梯度
            loss.backward()  # 反向传播
            optimizer.step()  # 一步随机梯度下降算法
            right = rightness(output, target)  # 计算一批次准确率中（正确样例数， 总样本数）
            train_rights.append(right)

            if batch_idx % 100 == 0:
                validation_model(validation_loader)

        # 求得整个训练样本中正确的样例总数， 和总样本数，可以通过两者得到训练的正确率
        train_r = (sum([tup[0] for tup in train_rights]), sum([tup[1] for tup in train_rights]))
        print("Epoch {0}: {1}/{2}".format(epoch, train_r[0], train_r[1]))


def validation_model(validation_loader):
    """验证模型
    """
    net.eval()
    val_rights = []

    for data, target in validation_loader:
        data, target = Variable(data), Variable(target)
        output = net(data)
        right = rightness(output, target)
        val_rights.append(right)

    val_r = (sum([tup[0] for tup in val_rights]), sum([tup[1] for tup in val_rights]))
    print("验证集的正确率为{:.2f}%".format(100.0 * val_r[0] / val_r[1]))


def test_model(test_loader):
    """测试模型
    """
    net.eval()
    vals = []
    for data, target in test_loader:
        data, target = Variable(data), Variable(target)
        output = net(data)
        val = rightness(output, target)
        vals.append(val)

    rights = (sum([tup[0] for tup in vals]), sum([tup[1] for tup in vals]))
    print("测试集的正确率为{:.2f}%".format(100.0 * rights[0] / rights[1]))


train_loader, validation_loader, test_loader = mnist_loader.load_data()
net = Network([784, 30, 10])
train_model(train_loader, 20, 0.001)
test_model(test_loader)
```
### 练习题

#### 问题1  假设把一个感知机网络中的所有权重和偏置乘以一个正的常数c ，请证明该网络的行为不会改变。

**解答：**

为了证明把一个感知机网络中的所有权重和偏置乘以一个正的常数c不会改变该网络的行为，我们需要知道感知机的基本工作原理。感知机是一种二元线性分类器，它的基本形式是：

$$
g(x) = sign(w·x + b)

$$

其中，w和b是权重和偏置，x是输入，sign是符号函数，它将w·x + b的值映射到+1或-1两个类别之一。
现在，如果我们将所有的权重和偏置乘以c，得到的新的感知机为：

$$
g_c(x) = sign(c·w·x + c·b)

$$

显然，`c·w·x + c·b`仍然是一个线性函数，并且它的斜率和原来的斜率相同（因为c是常数），因此，它仍然是一个线性分类器。所以，该网络的行为不会改变。

```python

```
