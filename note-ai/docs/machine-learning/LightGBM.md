![](img/LightGBM/LightGBM.PNG)



# LightGBM面试题

## 1. 简单介绍一下LightGBM？

LightGBM是一个梯度 boosting 框架，使用基于学习算法的决策树。 它可以说是分布式的，高效的。

从 LightGBM 名字我们可以看出其是轻量级（Light）的梯度提升机（GBM），其相对 XGBoost 具有训练速度快、内存占用低的特点。

LightGBM 是为解决GBDT训练速度慢，内存占用大的缺点，此外还提出了：

- 基于Histogram的决策树算法

- 单边梯度采样 Gradient-based One-Side Sampling(GOSS)

- 互斥特征捆绑 Exclusive Feature Bundling(EFB)

- 带深度限制的Leaf-wise的叶子生长策略

- 直接支持类别特征(Categorical Feature)

- 支持高效并行

- Cache命中率优化

## 2. 介绍一下直方图算法？

 直方图算法就是使用直方图统计，将大规模的数据放在了直方图中，分别是每个bin中**样本的梯度之和** 还有就是每个bin中**样本数量**

- 首先确定对于每一个特征需要多少个箱子并为每一个箱子分配一个整数；

- 将浮点数的范围均分成若干区间，区间个数与箱子个数相等

- 将属于该箱子的样本数据更新为箱子的值

- 最后用直方图表示

优点：

**内存占用更小**：相比xgb不需要额外存储预排序，且只保存特征离散化后的值(整型)

**计算代价更小**: 相比xgb不需要遍历一个特征值就需要计算一次分裂的增益，只需要计算k次(k为箱子的个数)

**直方图做差加速**：一个叶子的直方图可以由它的父亲节点的直方图与它兄弟的直方图做差得到，在速度上可以提升一倍

## 3. 介绍一下Leaf-wise和 Level-wise？

XGBoost 采用 Level-wise，策略遍历一次数据可以同时分裂同一层的叶子，容易进行多线程优化，也好控制模型复杂度，不容易过拟合。但实际上Level-wise是一种低效的算法，因为它不加区分的对待同一层的叶子，实际上很多叶子的分裂增益较低，没必要进行搜索和分裂

LightGBM采用Leaf-wise的增长策略，该策略每次从当前所有叶子中，找到分裂增益最大的一个叶子，然后分裂，如此循环。因此同Level-wise相比，Leaf-wise的优点是：在分裂次数相同的情况下，Leaf-wise可以降低更多的误差，得到更好的精度；Leaf-wise的缺点是：可能会长出比较深的决策树，产生过拟合。因此LightGBM会在Leaf-wise之上增加了一个最大深度的限制，在保证高效率的同时防止过拟合

## 4. 介绍一下单边梯度采样算法(GOSS)？

GOSS算法从减少样本的角度出发，排除大部分小梯度的样本，仅用剩下的样本计算信息增益，它是一种在减少数据量和保证精度上平衡的算法。与此同时，未了不改变数据的总体分布，GOSS对要进行分裂的特征按照绝对值大小进行排序，选取最大的a个数据，在剩下梯度小的数据中选取b个，这b个数据乘以权重$\frac{1-a}{b}$,最后使用这a+b个数据计算信息增益。

## 5. 介绍互斥特征捆绑算法(EFB)？

互斥特征捆绑算法（Exclusive Feature Bundling, EFB）指出如果将一些特征进行融合绑定，则可以降低特征数量。
LightGBM的EFB算法将这个问题转化为图着色的问题来求解，将所有的特征视为图的各个顶点，将不是相互独立的特征用一条边连接起来，边的权重就是两个相连接的特征的总冲突值，这样需要绑定的特征就是在图着色问题中要涂上同一种颜色的那些点（特征）。另外，算法可以允许一小部分的冲突，我们可以得到更少的绑定特征，进一步提高计算效率。

## 6. 特征之间如何捆绑？

比如，我们在bundle中绑定了两个特征A和B，A特征的原始取值为区间 $[0,10)$，B特征的原始取值为区间$[0,20)$，我们可以在B特征的取值上加一个偏置常量10，将其取值范围变为$[10,30)$，绑定后的特征取值范围为$[0,30)$

## 7. LightGBM是怎么支持类别特征？

* 离散特征建立直方图的过程 

  统计该特征下每一种离散值出现的次数，并从高到低排序，并过滤掉出现次数较少的特征值, 然后为每一个特征值，建立一个bin容器。

* 计算分裂阈值的过程 

  * 先看该特征下划分出的bin容器的个数，如果bin容器的数量小于4，直接使用one vs other方式, 逐个扫描每一个bin容器，找出最佳分裂点;

  * 对于bin容器较多的情况, 先进行过滤，只让子集合较大的bin容器参加划分阈值计算, 对每一个符合条件的bin容器进行公式计算
    $$
    \frac{该bin容器下所有样本的一阶梯度之和 }{ 该bin容器下所有样本的二阶梯度之和} + 正则项 
    $$
    
* **这里为什么不是label的均值呢？其实"label的均值"只是为了便于理解，只针对了学习一棵树且是回归问题的情况， 这时候一阶导数是Y, 二阶导数是1**)，得到一个值，根据该值对bin容器从小到大进行排序，然后分从左到右、从右到左进行搜索，得到最优分裂阈值。但是有一点，没有搜索所有的bin容器，而是设定了一个搜索bin容器数量的上限值，程序中设定是32，即参数max_num_cat。
  
* LightGBM中对离散特征实行的是many vs many 策略，这32个bin中最优划分的阈值的左边或者右边所有的bin容器就是一个many集合，而其他的bin容器就是另一个many集合。
  
* 对于连续特征，划分阈值只有一个，对于离散值可能会有多个划分阈值，每一个划分阈值对应着一个bin容器编号，当使用离散特征进行分裂时，只要数据样本对应的bin容器编号在这些阈值对应的bin集合之中，这条数据就加入分裂后的左子树，否则加入分裂后的右子树。

## 8. LightGBM的优缺点

优点：

- 直方图算法极大的降低了时间复杂度；
- 单边梯度算法过滤掉梯度小的样本，减少了计算量；
- 基于 Leaf-wise 算法的增长策略构建树，减少了计算量；
- 直方图算法将存储特征值转变为存储 bin 值，降低了内存消耗
- 互斥特征捆绑算法减少了特征数量，降低了内存消耗

缺点：

- LightGBM在Leaf-wise可能会长出比较深的决策树，产生过拟合
- LightGBM是基于偏差的算法，所以会对噪点较为敏感；



## 9. GBDT是如何做回归和分类的

- **回归**

  生成每一棵树的时候，第一棵树的一个叶子节点内所有样本的label的均值就是这个棵树的预测值，后面根据残差再预测，最后根据将第一棵树的预测值+权重*(其它树的预测结果)

  ![image-20210629173116854](../../../../../Library/Application Support/typora-user-images/image-20210629173116854.png)

* **分类**

  分类时针对样本有三类的情况，

  * 首先同时训练三颗树。
    - 第一棵树针对样本 x 的第一类，输入为（x, 0）。
    - 第二棵树输入针对样本 x 的第二类，假设 x 属于第二类，输入为（x, 1）。
    - 第三棵树针对样本 x 的第三类，输入为（x, 0）。
    - 参照 CART 的生成过程。输出三棵树对 x 类别的预测值 f1(x), f2(x), f3(x)。
  * 在后面的训练中，我们仿照多分类的逻辑回归，使用 softmax 来产生概率。
    - 针对类别 1 求出残差 f11(x) = 0 − f1(x)；
    - 类别 2 求出残差 f22(x) = 1 − f2(x)；
    - 类别 3 求出残差 f33(x) = 0 − f3(x)。
  * 然后第二轮训练，
    - 第一类输入为(x, f11(x))
    - 第二类输入为(x, f22(x))
    - 第三类输入为(x, f33(x))。
  * 继续训练出三棵树，一直迭代 M 轮，每轮构建 3 棵树。当训练完毕以后，新来一个样本 x1，我们需要预测该样本的类别的时候，便可使用 softmax 计算每个类别的概率。

  

## 参考资料

深入理解LightGBM https://mp.weixin.qq.com/s/zejkifZnYXAfgTRrkMaEww

决策树（下）——XGBoost、LightGBM（非常详细） - 阿泽的文章 - 知乎 https://zhuanlan.zhihu.com/p/87885678

Lightgbm如何处理类别特征： https://blog.csdn.net/anshuai_aw1/article/details/83275299

LightGBM 直方图优化算法：https://blog.csdn.net/jasonwang_/article/details/80833001