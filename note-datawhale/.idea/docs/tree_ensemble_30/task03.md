# Part C: 自适应提升法

----

（本学习笔记来源于[DataWhale-树模型与集成学习](https://github.com/datawhalechina/machine-learning-toy-code)）



Bagging：独立的集成多个模型，每个模型有一定的差异，最终综合有差异的模型的结果，获得学习的最终的结果；
Boosting（增强集成学习）：集成多个模型，每个模型都在尝试增强（Boosting）整体的效果；
Stacking（堆叠）：集成 k 个模型，得到 k 个预测结果，将 k 个预测结果再传给一个新的算法，得到的结果为集成系统最终的预测结果；
Bagging和Boosting的区别：

1）样本选择上：

Bagging：训练集是在原始集中有放回选取的，从原始集中选出的各轮训练集之间是独立的。

Boosting：每一轮的训练集不变，只是训练集中每个样例在分类器中的权重发生变化。而权值是根据上一轮的分类结果进行调整。

2）样例权重：

Bagging：使用均匀取样，每个样例的权重相等

Boosting：根据错误率不断调整样例的权值，错误率越大则权重越大。

3）预测函数：

Bagging：所有预测函数的权重相等。

Boosting：每个弱分类器都有相应的权重，对于分类误差小的分类器会有更大的权重。

4）并行计算：

Bagging：各个预测函数可以并行生成

Boosting：各个预测函数只能顺序生成，因为后一个模型参数需要前一轮模型的结果。

5）bagging是减少variance，而boosting是减少bias



stacking代码实现 

```python
from sklearn.model_selection import KFold
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.linear_model import LinearRegression
from sklearn.datasets import make_regression
 
import numpy as np
import pandas as pd
 
m1=KNeighborsRegressor()
m2=DecisionTreeRegressor()
m3=LinearRegression()
 
models=[m1,m2,m3]
 
#from sklearn.svm import LinearSVR
 
final_model=DecisionTreeRegressor()
 
k,m=4,len(models)
 
if  __name__=="__main__":
    X,y=make_regression(
        n_samples=1000,n_features=8,n_informative=4,random_state=0
    )
    final_X,final_y=make_regression(
        n_samples=500,n_features=8,n_informative=4,random_state=0
    )
    
    final_train=pd.DataFrame(np.zeros((X.shape[0],m)))
    final_test=pd.DataFrame(np.zeros((final_X.shape[0],m)))
    
    kf=KFold(n_splits=k)
    for model_id in range(m):
        model=models[model_id]
        for train_index,test_index in kf.split(X):
            X_train,X_test=X[train_index],X[test_index]
            y_train,y_test=y[train_index],y[test_index]
            model.fit(X_train,y_train)
            final_train.iloc[test_index,model_id]=model.predict(X_test)
            final_test.iloc[:,model_id]+=model.predict(final_X)
        final_test.iloc[:,model_id]/=k
    final_model.fit(final_train,y)
    res=final_model.predict(final_test)


```

blending代码实现：


```python

from sklearn.model_selection import KFold
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.linear_model import LinearRegression
from sklearn.datasets import make_regression
 
import numpy as np
import pandas as pd
 
m1=KNeighborsRegressor()
m2=DecisionTreeRegressor()
m3=LinearRegression()
 
models=[m1,m2,m3]
 
final_model=DecisionTreeRegressor()
 
m=len(models)
 
if  __name__=="__main__":
    X,y=make_regression(
        n_samples=1000,n_features=8,n_informative=4,random_state=0
    )
    final_X,final_y=make_regression(
        n_samples=500,n_features=8,n_informative=4,random_state=0
    )
    
 
    X_train,X_test,y_train,y_test = train_test_split(X,y,test_size=0.5)
    
    final_train=pd.DataFrame(np.zeros((X_test.shape[0],m)))
    final_test=pd.DataFrame(np.zeros((final_X.shape[0],m)))
    
    for model_id in range(m):
        model=models[model_id]
        model.fit(X_train,y_train)
        final_train.iloc[:,model_id]=model.predict(X_test)
        final_test.iloc[:,model_id]+=model.predict(final_X)
        
    final_model.fit(final_train,y_train)
    res=final_model.predict(final_test)
```

参考：

- https://www.jianshu.com/p/0d850d85dcbd
- [加法模型和乘法模型](https://support.minitab.com/zh-cn/minitab/18/help-and-how-to/modeling-statistics/time-series/supporting-topics/time-series-models/additive-and-multiplicative-models/)
