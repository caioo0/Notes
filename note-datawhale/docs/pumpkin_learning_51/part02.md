# 二、第3章 线性模型

> 学习笔记来源 datawhale-吃瓜教程，视频：[B站南瓜书教学](https://www.bilibili.com/video/BV1Mh411e7VU/?p=2&vd_source=17fa4774c3617361fe8378798cb196a2)



## 1 基本形式

概念：给定由$d$个属性描述的实例$x=(x_1;x_2;\dots ;x_d)$，其中$x_i$是$x$在第$i$个属性上的取值，线性模型试图学得一个通过属性的线性组合来进行预测的函数，即
$$
  f(x)=w_1x_1+w_2x_2+\cdot+w_dx_d+b
$$

一般用向量形式：
$$
f(x)=w^Tx+b
$$

其中$w=(w_1;w_2;\cdot;w_d)$，当向量中的元素用分号“；”分隔时表示此向量为列向量，用逗号“，”分割时表示为行向量。

## 2 线性回归

- 属性值转换：对离散属性，若属性值之间存在“序关系”，则可以将其转化为连续值；若属性值之间不存在“序关系”，则通常将其转化为向量的形式

- 确定$w$和$b$
  - 目标：最小化$f(x)$与$y$均方误差，试图学得
  $$
  \hat{y} = f(x_i) = wx_i + b, 使得f(x_i) \approx y_i
  $$
  - 输入属性只有一个（最小二乘法）：首先计算出每个样本预测值与真实值之间的误差并求和，通过最小化均方误差MSE，使用求偏导等于零的方法计算出拟合直线$y=wx+b$的两个参数$w$和$b$。
  
  - 输入属性有多个（多元线性回归）：可类似于最小二乘法，将数据集$D$表示为一个$m\times (d+1)$大小的矩阵，再表示为向量形式，最后通过计算$\hat{w}$偏导，得到最优解。
  
  - 目标/损失函数：
  
    $$
    L = \frac{1}{n}\sum^{n}_{i=1}(\hat{y_i} - y_i)^2
    $$
  
    即预测值与真实值之间的平均距离,（MEA）均方误差。将函数带入得到
  - 
    $$
    L(w,b) = \frac{1}{n}\sum_{n=1}{^n}(wb_i+b-y_i)^2
    $$
     求解最小化L时$w和b$的值，
  
    即核心目标优化式为：
    $$
    (w^*,b^*) = arg  \underset{(w,b)}{min}\sum_{i=1}^n(wx_i +b -y_i)^2
    $$
    求解方式有两种：
  
    1）最小二乘法（least square method）
  
    ​		求解 w 和 b 是使损失函数最小化的过程，在统计中，称为线性回归模型的最小二乘“参数估计”(parameter estimation)。我们可以将 L(w,b) 分别对 w 和 b 求导，得到:
    $$
    \frac{\partial{L}}{\partial{w}} = 2 (w\sum_{i=1}^n x^2 - \sum_{i=1}^n x_i(y_i-b))
    $$
  
    $$
    \frac{\partial{L}}{\partial{b}} = 2 (nb - \sum_{i=1}(y_i-wx_i))
    $$
  
    令上述俩式为0，可得到 w 和 b 最优解的闭式(closed-form)解：
    $$
    w = \frac{\sum_{i=1}^n y_i (x_i -\overline{x})}{\sum_{i=1}^n x^2_i - \frac{1}{n}(\sum_{i=1}^n x_i)^2}
    $$
  
    $$
     b = \frac{1}{n}\sum_{i=1}^n (y_i - wx_i)
    $$
  
    2) 梯度下降（gradient descent）
  
    梯度下降核心内容是对自变量进行不断的更新（针对w和b求偏导），使得目标函数不断逼近最小值的过程：
    $$
    w \leftarrow w - a \frac{\partial{L}}{\partial{w}}
    $$
  
    $$
    b \rightarrow b - a \frac{\partial{L}}{\partial{b}}
    $$
  
    
  
- 简写形式：$y=w^Tx+b$

- 广义线性模型：$y=g^{-1}(w^Tx_b)$，其中$g(\cdot)$时单调可微函数。

  

## 3 对数几率回归

单位阶跃函数：若预测值$z$大于零判为正例，小于零判为反例，预测值为临界值零则可任意判别。

$$
y = \left \{
\begin{matrix}
 0,   z<0; \\
 0.5, z=0; \\
 1,   z>0 
\end{matrix}
\right.
$$
对数几率函数：

$$
y=\frac{1}{1+e^{-z}}
$$

从图3.2 可以看出单位阶跃函数不连续，

![image-20231021125907389](.\img\image-20231021125907389.png)

- 概念：若将$y$看做样本为正例的概率，$(1-y)$看做样本为反例的概率，则使用线性回归模型的预测结果器逼近真实标记的对数几率
- 思路：使用最大似然估计的方法来计算出$w$和$b$两个参数的取值
  $\displaystyle \ln \frac{p(y=1 | x)}{p(y=0 | x)}=w^T x + b $
  $\because p(y=1|x)=1-p(y=0|x)$
  正例：$\displaystyle p(y=1|x) = \frac{e^{w^T x + b}}{1 + e^{w^T x + b}}$
  负例：$\displaystyle p(y=0|x) = \frac{1}{1 + e^{w^T x + b}}$
  似然函数：$\displaystyle \ell(w, b)=\sum_{i=1}^m \ln p(y_i | x_i ; w, b)$，对数变乘为加，即所有样本出现真实值的概率乘积最大。

## 4 线性判别分析

- 线性判别分析（LDA）基本思想：将训练样本投影到一条直线上，使得同类的样例尽可能近，不同类的样例尽可能远。对新样本进行分类时，投影到同一条直线上，根据投影点的位置确定新样本的类别。
- 具体步骤：

  1. 给定数据集$D=\{(x_i,y_i)\}_{i=1}^m, y_i \in \{0,1\}$，令$X_i,\mu_i, \Sigma_i$分别表示第$i \in \{0,1\}$类示例的集合、均值向量、协方差矩阵。
  2. 若将数据投影到直线$w$上，则两类样本的中心在直线上的投影分别为$w^T \mu_0$和$w^T \mu_1$；若将所有样本点都投影到直线上，则两类样本的协方差分别为$w^T \Sigma_0 w$和$w^T \Sigma_1 w$。
  3. 使得各类的协方差之和尽可能小，不同类之间中心的距离尽可能大。
  4. 计算类内散度矩阵：

  $$



$$
\begin{aligned} S_w &=\Sigma_0+\Sigma_1 \\
&=\sum_{x \in X_0} (x-\mu_0) (x-\mu_0)^T+ \sum_{x \in X_1}(x-\mu_1)(x-\mu_1)^T \end{aligned}
$$
5. 计算类间散度矩阵：
    
    
    $$
    S_b=(\mu_0-\mu_1)(\mu_0-\mu_1)^T
    $$
     

6. 计算LDA最大化的目标函数：

   

   J=\frac{w^T S_b w}{w^T S_w w}

$$
7. $W$的闭式解是$S_w^{-1}S_b$的$N-1$个最大广义特征值所对应的特征向量组成的矩阵

- LDA常被视为一种经典的监督降维技术。

## 5. 多分类学习

- “拆分”策略：将多分类问题拆解为多个二分类问题，训练出多个二分类学习器，最后将多个分类结果进行集成得出结论。
- “一对一”（OvO）：给定数据集$D$，假定其中有$N$个真实类别，将这$N$个类别进行两两配对（一个正类/一个反类），从而产生$N(N-1)/2$个二分类学习器，在测试阶段，将新样本提交给所有学习器，得出$N(N-1)$个结果，最终通过投票产生最终的分类结果。
- “一对其余”（OvR）：给定数据集$D$，假定其中有$N$个真实类别，每次取出一个类作为正类，剩余的所有类别作为一个新的反类，从而产生$N$个二分类学习器，在测试阶段，得出$N$个结果，若仅有一个学习器预测为正类，则对应的类标作为最终分类结果。
- “多对多”（MvM）：给定数据集$D$，假定其中有$N$个真实类别，每次取若干个类作为正类，若干个类作为反类（通过ECOC码给出，编码），若进行了$M$次划分，则生成了$M$个二分类学习器，在测试阶段（解码），得出$M$个结果组成一个新的编码，最终通过将预测编码与每个类别各自的编码进行比较，选择距离最小的类别作为最终分类结果。

## 6. 类别不平衡问题

- 概念：指分类问题中不同类别的训练样本相差悬殊的情况
- 常用方法：
  1. 对训练样本较多的类别中进行“欠采样”（undersampling），使得正反例数目接近，常见的算法有：EasyEnsemble。
  2. 对训练样本较少的类别中进行“过采样”（oversampling），增加较少类的数量，使得正反例数目接近，常见的算法有SMOTE。
  3. 直接基于原数据集进行学习，对预测值进行“再缩放”处理。其中“再缩放”也是“代价敏感学习”的基础。

$$
\frac{y'}{1-y'}=\frac{y}{1-y} \times \frac{m^{-}}{m^{+}} = \frac{y}{1-y} \times \frac{\text{cost} (+>-)}{\text{cost} (->+)}\quad
$$


## 7. 代码实现

文件1：LinerRegression.py
```python
# -*- coding: utf-8 -*-

import numpy as np


class LinerRegression(object):

    def __init__(self, learning_rate=0.01, max_iter=100, seed=None):
        np.random.seed(seed)
        self.lr = learning_rate
        self.max_iter = max_iter
        self.w = np.random.normal(1, 0.1)
        self.b = np.random.normal(1, 0.1)
        self.loss_arr = []

    def fit(self, x, y):
        self.x = x
        self.y = y
        for i in range(self.max_iter):
            self._train_step()
            self.loss_arr.append(self.loss())
            # print('loss: \t{:.3}'.format(self.loss()))
            # print('w: \t{:.3}'.format(self.w))
            # print('b: \t{:.3}'.format(self.b))

    def _f(self, x, w, b):
        return x * w + b

    def predict(self, x=None):
        if x is None:
            x = self.x
        y_pred = self._f(x, self.w, self.b)
        return y_pred

    def loss(self, y_true=None, y_pred=None):
        if y_true is None or y_pred is None:
            y_true = self.y
            y_pred = self.predict(self.x)
        return np.mean((y_true - y_pred)**2)

    def _calc_gradient(self):
        d_w = np.mean((self.x * self.w + self.b - self.y) * self.x)
        d_b = np.mean(self.x * self.w + self.b - self.y)
        return d_w, d_b

    def _train_step(self):
        d_w, d_b = self._calc_gradient()
        self.w = self.w - self.lr * d_w
        self.b = self.b - self.lr * d_b
        return self.w, self.b

```
文件2：train.py

```python
# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
from liner_regression import *


def show_data(x, y, w=None, b=None):
    plt.scatter(x, y, marker='.')
    if w is not None and b is not None:
        plt.plot(x, w*x+b, c='red')
    plt.show()


# data generation
np.random.seed(272)
data_size = 100
x = np.random.uniform(low=1.0, high=10.0, size=data_size)
y = x * 20 + 10 + np.random.normal(loc=0.0, scale=10.0, size=data_size)

# plt.scatter(x, y, marker='.')
# plt.show()

# train / test split
shuffled_index = np.random.permutation(data_size)
x = x[shuffled_index]
y = y[shuffled_index]
split_index = int(data_size * 0.7)
x_train = x[:split_index]
y_train = y[:split_index]
x_test = x[split_index:]
y_test = y[split_index:]

# visualize data
# plt.scatter(x_train, y_train, marker='.')
# plt.show()
# plt.scatter(x_test, y_test, marker='.')
# plt.show()

# train the liner regression model
regr = LinerRegression(learning_rate=0.01, max_iter=10, seed=314)
regr.fit(x_train, y_train)
print('cost: \t{:.3}'.format(regr.loss()))
print('w: \t{:.3}'.format(regr.w))
print('b: \t{:.3}'.format(regr.b))
show_data(x, y, regr.w, regr.b)

# plot the evolution of cost
plt.scatter(np.arange(len(regr.loss_arr)), regr.loss_arr, marker='o', c='green')
plt.show()
```
## 7. 参考资料

[1].[算法笔记-线性回归](https://www.cnblogs.com/geo-will/p/10468253.html)