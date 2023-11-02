# Task05 详读西瓜书+南瓜书第6章

支持向量机的目标是确定一个对样本的分类结果最鲁棒的线性分类器，即找到一个具有最大间隔的划分超平面。为此以间隔为优化目标，可将其转化为一个凸二次规划问题。

## 1. 间隔与支持向量

分类学习最基本的想法就是基于训练集D在样本空间中找到一个划分超平面，将不同类别的样本分开。

![image-20231101001140408](.\img\image-20231101001140408.png)

两类训练样本“正中间”的划分超平面所产生的分类结果是最鲁棒的，对未见示例的泛化能力最强。

![image-20231101001234620](.\img\image-20231101001234620.png)

距离超平面最近的这几个训练样本点被称为**“支持向量” (support vector)**，两个异类支持向量到超平面的距离之和为**“间隔”（margin）**

- 支持向量的概念：  
  &emsp;&emsp;假设超平面$(w,b)$能将训练样本正确分类，即对于$(x_i,y_i) \in D$，若$y_i=+1$，则有$w^Tx_i+b>0$，若$y_i=-1$，则有$w^Tx_i+b<0$，令：
  $$\left \{ 
  \begin{array}{ccc}
   w^Tx_i+b \geqslant +1, \quad y_i=+1 \\
   w^Tx_i+b \leqslant -1, \quad y_i=-1
  \end{array} \right .$$
  距离超平面最近的这几个训练样本点使得上式成立，则这些样本点被称为支持向量。
- 间隔：两个异类支持向量超平面的距离之和$\displaystyle \gamma=\frac{2}{\|w\|}$ 
- 支持向量机（SVM）基本型：  
  &emsp;&emsp;找到最大间隔的划分超平面，需要求解参数$w$和$b$使得$\gamma$最大，目标函数如下：$$\begin{array}{l} \min \limits_{w,b} & \displaystyle \frac{1}{2}\|w\|^2 \\ 
\text { s.t. } & y_{i}(w^T x_i+b ) \geqslant 1, \quad i=1,2, \ldots, m \end{array}$$

## 2. 对偶问题
- 拉格朗日函数：$\displaystyle L(w, b, \alpha)=\frac{1}{2}\|w\|^2 + \sum_{i=1}^m \alpha_i\left(1- y_i (w^T x_i+b ) \right)$

- 对偶问题：$$\begin{array}{ll} \displaystyle \max_{\alpha} & \displaystyle \sum_{i=1}^m \alpha_i-\frac{1}{2} \sum_{i=1}^m \sum_{j=1}^m \alpha_i \alpha_j y_i y_j x_i^T x_j \\ 
  {\text { s.t. }} & {\displaystyle \sum_{i=1}^m \alpha_i y_i=0} \\ 
  {} & {\alpha_i \geqslant 0, i=1,\ldots, m}
  \end{array}$$

- KKT条件：$$\left \{ \begin{array}{ll}
  \alpha_i \geqslant 0 \\
  y_i f(x_i) - 1 \geqslant 0 \\
  \alpha_i(y_i f(x_i) - 1) = 0
  \end{array}\right .$$

- 支持向量机特点：训练完成后，大部分的训练样本都不需保留，最终模型仅与支持向量有关

- SMO算法思路：
  1. 选取一对需要更新的变量$\alpha_i$和$\alpha_j$
  2. 固定$\alpha_i$和$\alpha_j$以外的参数，求解对偶问题，获得更新后的$\alpha_i$和$\alpha_j$
  3. 重复上述2个步骤，直至收敛
  
- SMO采用一个启发式：使选取的两变量所对应样本之间的间隔最大。

  SMO的基本思路：先固定αi之外的所有参数，然后求αi上的极值.由于存在约束若固定αi之外的其他变量，则αi可由其他变量导出。于是，SMO每次选择两个变量αi和αj并固定其他参数。这样，在参数初始化后，SMO不断执行如下两个步骤直至收敛：

  - 选取一对需更新的变量αi和αj；
  - 固定αi和αj以外的参数，求解式(6.2)获得更新后的αi和αj

  SMO算法之所以高效，恰由于在固定其他参数后，仅优化两个参数的过程能做到非常高效。

## 3. 核函数

**核函数：**巧妙地解决了在高维空间中的内积运算，从而很好地解决了非线性分类问题。

核函数的选择包括两部分工作：

1 是核函数类型的选择，

2 是确定核函数类型后相关参数的选择．

### 常用的核函数：

- **线性核（Linear Kernel）**
- **多项式核（Polynomial Kernel）**
- **字符串核函数**
- **傅立叶核**
- **样条核**

### 核函数的选择

**1.先验知识**

一是利用专家的先验知识预先选定核函数；

**2.交叉验证**

二是采用Cross-Validation方法，即在进行核函数选取时，分别试用不同的核函数，归纳误差最小的核函数就是最好的核函数．如针对傅立叶核、RBF核，结合信号处理问题中的函数回归问题，通过仿真实验，对比分析了在相同数据条件下，采用傅立叶核的SVM要比采用RBF核的SVM误差小很多．

**3.混合核函数**

三是采用由Smits等人提出的混合核函数方法，该方法较之前两者是目前选取核函数的主流方法，也是关于如何构造核函数的又一开创性的工作．将不同的核函数结合起来后会有更好的特性，这是混合核函数方法的基本思想

## 4. 软间隔与正则化

为缓解由于过拟合而产生貌似线性可分的结果，可允许支持向量机在一些样本上出错。为此，要引入**“软间隔” (soft margin)**的概念

![image-20231101001916547](.\img\image-20231101001916547.png)

- 软间隔：允许某项样本不满足约束$y_i(w^Tx_i+b) \geqslant 1$，在最大化间隔的同时，不满足约束的样本应该尽可能少
- 目标函数：$$\begin{array}{l}
\displaystyle \min_{w, b} & \displaystyle \frac{1}{2}\|w\|^2+C \sum_{i=1}^m \ell_{0/1} \left( y_i(w^T x_i+b) -1 \right) \\ 
& {\ell_{0/1}(z)=\left\{\begin{array}{ll}
{1,} & {\text { if } z<0 ;} \\ 
{0,} & {\text { otherwise }} \end{array}\right.}
\end{array}$$
- 损失函数：
  1. hinge损失：$\ell_{hinge}(z)=\max(0,1-z)$  
  2. 指数损失（exponential loss）: $\ell_{exp}(z)=\exp (-z)$  
  3. 对率损失（logistic loss）：$\ell_{log}(z)=log(1+\exp(-z))$
- 常用的软间隔支持向量机：
$$\begin{array}{ll}
\displaystyle \min \limits_{w,b,\xi} & \displaystyle \frac{1}{2}\|w\|^2 + C \sum_{i=1}^m \xi_i \\ 
\text{s.t.} & y_i (w^T x_i+b) \geqslant 1-\xi_i \\
& \xi_i \geqslant 0, \quad i=1, \ldots, m 
\end{array}$$
- 软间隔支持向量机的对偶问题：
$$\begin{array}{cl}
{\displaystyle \max \limits_{\alpha}} & {\displaystyle \sum_{i=1}^m \alpha_i-\frac{1}{2} \sum_{i=1}^m \sum_{j=1}^m \alpha_i \alpha_j y_i y_j x_i^T x_j} \\ 
{\text {s.t.}} & {\displaystyle \sum_{i=1}^m \alpha_i y_i=0}  \\
{} & {0 \leqslant \alpha_i \leqslant C, i=1,2, \ldots, m}
\end{array}$$
- 软间隔支持向量机的KKT条件：
$$\left \{ \begin{array}{l}
\alpha_i \geqslant 0, \quad \mu_i \geqslant 0 \\
y_i f(x_i) - 1 + \xi_i \geqslant 0 \\
\alpha_i (y_i f(x_i) - 1 + \xi_i) = 0 \\
\xi_i \geqslant 0, \quad \mu_i \xi_i = 0
\end{array}\right .$$
- 软间隔支持向量机的最终模型仅与支持向量有关，即通过采用hinge损失函数仍保持了稀疏性
- 正则化问题：$$\min \limits_{f} \Omega(f) + C \sum_{i=1}^m \ell(f(x_i), y_i)$$在该式中，$\Omega(f)$称为正则化项，$C$称为正则化参数
  1. $L_p$范数使常用的正则化项
  2. $L_2$范数$\|w\|_2$倾向于$w$的分量取值尽量均衡，即非零分量个数尽量稠密
  3. $L_0$范数$\|w\|_0$和$L_1$范数$\|w\|_1$倾向于$w$的分量尽量系数，即非零分量个数尽量少

## 5 支持向量回归
- 损失计算规则：以$f(x)$为中心，构建一个宽度为$2\epsilon$的间隔带，若训练样本落入此间隔带，则不计算损失，认为是被预测正确
- SVR目标函数：$$\begin{array}{l}
\displaystyle \min_{w, b, \xi_i,\hat{\xi}_i} & \displaystyle \frac{1}{2}\|w\|^2 + C \sum_{i=1}^m (\xi_i + \hat{\xi}_i) \\ 
\text{s.t.} & f(x_i) - y_i \leqslant \epsilon + \xi_i \\
& y_i - f(x_i) \leqslant \epsilon + \hat{\xi}_i \\
& \xi_i \geqslant 0, \hat{\xi}_i \geqslant 0, i=1,2,\ldots,m
\end{array}$$
- SVR对偶问题：
$$\begin{array}{l}
\max \limits_{\alpha, \hat{\alpha}} &\displaystyle \sum_{i=1}^{m} y_{i}(\hat{\alpha}_{i}-\alpha_{i})-\epsilon(\hat{\alpha}_{i}+\alpha_{i}) -\frac{1}{2} \sum_{i=1}^{m} \sum_{j=1}^{m} (\hat{\alpha}_{i}-\alpha_{i})(\hat{\alpha}_{j}-\alpha_{j}) x_i^T x_j \\
\text { s.t. } &\displaystyle \sum_{i=1}^{m} (\hat{\alpha}_{i}-\alpha_{i})=0 \\
& 0 \leqslant \alpha_{i}, \hat{\alpha}_{i} \leqslant C
\end{array}$$
- SVR的KKT条件：
$$\left\{\begin{array}{l}
\alpha_i (f(x_i) - y_i - \epsilon - \xi_i)=0 \\
\hat{\alpha}_i (y_i -f(x_i) - \epsilon - \hat{\xi}_i)=0 \\
\alpha_i \hat{\alpha}_i=0, \quad \xi_i \hat{\xi}_i=0 \\
(C-\alpha_i ) \xi_i=0, \quad (C-\hat{\alpha}_i) \hat{\xi}_i=0
\end{array}\right.$$
- SVR的解：$$f(x)=\sum_{i=1}^m (\hat{\alpha}_i - \alpha_i) x_i^T x + b
$$其中：$$b = y_i + \epsilon - \sum_{i=1}^m (\hat{\alpha}_i - \alpha_i) x_i^T x \\
w = \sum_{i=1}^m (\hat{\alpha}_i - \alpha_i ) \phi (x_i)$$



## 6. 代码实现

```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
```

```python
mean1, mean2 = np.array([0, 2]), np.array([2, 0])
covar = np.array([[1.5, 1.0], [1.0, 1.5]])
X1 = np.random.multivariate_normal(mean1, covar, 100)
y1 = np.ones(X1.shape[0])
X2 = np.random.multivariate_normal(mean2, covar, 100)
y2 = -1 * np.ones(X2.shape[0])
X_train = np.vstack((X1[:80], X2[:80]))
y_train = np.hstack((y1[:80], y2[:80]))
X_test = np.vstack((X1[80:], X2[80:]))
y_test = np.hstack((y1[80:], y2[80:]))
print(X_train.shape, y_train.shape, X_test.shape, y_test.shape)
```

```python
# 设置颜色参数
colors = {1:'r', -1:'g'}
# 绘制二分类数据集的散点图
plt.scatter(X_train[:,0], X_train[:,1], marker='o', c=pd.Series(y_train).map(colors))
plt.show();
```

```python
### 定义一个线性核函数
def linear_kernel(x1, x2):
    '''
    输入:
    x1: 向量1
    x2: 向量2
    输出:
    np.dot(x1, x2): 两个向量的点乘
    '''
    return np.dot(x1, x2)
```

```python
from cvxopt import matrix, solvers

### 定义近似线性可分支持向量机
### 软间隔最大化策略
class Soft_Margin_SVM:
    ### 定义基本参数
    def __init__(self, kernel=linear_kernel, C=None):
        # 软间隔svm核函数，默认为线性核函数
        self.kernel = kernel
        # 惩罚参数
        self.C = C
        if self.C is not None: 
            self.C = float(self.C)
    
    ### 定义线性支持向量机拟合方法
    def fit(self, X, y):
        # 训练样本数和特征数
        m, n = X.shape
        
        # 基于线性核计算Gram矩阵
        K = self._gram_matrix(X)
                
        # 初始化二次规划相关变量：P/q/G/h
        P = matrix(np.outer(y,y) * K)
        q = matrix(np.ones(m) * -1)
        A = matrix(y, (1, m))
        b = matrix(0.0)
        
        # 未设置惩罚参数时的G和h矩阵
        if self.C is None:
            G = matrix(np.diag(np.ones(m) * -1))
            h = matrix(np.zeros(m))
        # 设置惩罚参数时的G和h矩阵
        else:
            tmp1 = np.diag(np.ones(m) * -1)
            tmp2 = np.identity(m)
            G = matrix(np.vstack((tmp1, tmp2)))
            tmp1 = np.zeros(m)
            tmp2 = np.ones(m) * self.C
            h = matrix(np.hstack((tmp1, tmp2)))

        # 构建二次规划求解
        sol = solvers.qp(P, q, G, h, A, b)
        # 拉格朗日乘子
        a = np.ravel(sol['x'])

        # 寻找支持向量
        spv = a > 1e-5
        ix = np.arange(len(a))[spv]
        self.a = a[spv]
        self.spv = X[spv]
        self.spv_y = y[spv]
        print('{0} support vectors out of {1} points'.format(len(self.a), m))

        # 截距向量
        self.b = 0
        for i in range(len(self.a)):
            self.b += self.spv_y[i]
            self.b -= np.sum(self.a * self.spv_y * K[ix[i], spv])
        self.b /= len(self.a)

        # 权重向量
        self.w = np.zeros(n,)
        for i in range(len(self.a)):
            self.w += self.a[i] * self.spv_y[i] * self.spv[i]

    ### 定义Gram矩阵计算函数
    def _gram_matrix(self, X):
        m, n = X.shape
        K = np.zeros((m, m))
        # 遍历计算Gram矩阵
        for i in range(m):
            for j in range(m):
                K[i,j] = self.kernel(X[i], X[j])
        return K
    
    ### 定义映射函数
    def project(self, X):
        if self.w is not None:
            return np.dot(X, self.w) + self.b
    
    ### 定义模型预测函数
    def predict(self, X):
        return np.sign(np.dot(self.w, X.T) + self.b)


```

```python
from sklearn.metrics import accuracy_score
soft_margin_svm = Soft_Margin_SVM(C=0.1)
soft_margin_svm.fit(X_train, y_train)
y_pred = soft_margin_svm.predict(X_test)
# 计算测试集准确率
print('Accuracy of soft margin svm based on cvxopt: ', 
      accuracy_score(y_test, y_pred))
```

```python
def plot_classifier(X1_train, X2_train, clf):
    plt.plot(X1_train[:,0], X1_train[:,1], "ro")
    plt.plot(X2_train[:,0], X2_train[:,1], "go")
    plt.scatter(soft_margin_svm.spv[:,0], soft_margin_svm.spv[:,1], 
                s=100, c="", edgecolors="b", label="support vector")

    X1, X2 = np.meshgrid(np.linspace(-4,4,50), np.linspace(-4,4,50))
    X = np.array([[x1, x2] for x1, x2 in zip(np.ravel(X1), np.ravel(X2))])
    Z = soft_margin_svm.project(X).reshape(X1.shape)
    plt.contour(X1, X2, Z, [0.0], colors='k', linewidths=1, origin='lower')
    plt.contour(X1, X2, Z + 1, [0.0], colors='grey', linewidths=1, origin='lower')
    plt.contour(X1, X2, Z - 1, [0.0], colors='grey', linewidths=1, origin='lower')
    plt.legend()
    plt.show()
    
plot_classifier(X_train[y_train==1], X_train[y_train==-1], soft_margin_svm)
```

