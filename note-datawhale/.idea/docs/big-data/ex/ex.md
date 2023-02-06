
1. Hadoop五个守护进程?

```angular2html

namenode  datanode  secondarynamenode  resourcemanager   nodemanager

```

2. bootstrap数据是什么意思？

```
bootstrap统计抽样方法：有放回地从总共N个样本中抽样n个样本。
基于bootstrap，有以下常用的机器学习方法
boosting
bagging
random forest（RF, 随机森林）
```

3. 判别式模型和生成模型分别有哪些？

```md

判别式模型(Discriminative Model)：直接对条件概率p(y|x)进行建模，

常见判别模型有：线性回归、决策树、支持向量机SVM、k近邻、神经网络等；

生成式模型(Generative Model)：对联合分布概率p(x,y)进行建模，

常见生成式模型有：隐马尔可夫模型HMM、朴素贝叶斯模型、高斯混合模型GMM、LDA等；

生成式模型更普适；判别式模型更直接，目标性更强
生成式模型关注数据是如何产生的，寻找的是数据分布模型；判别式模型关注的数据的差异性，寻找的是分类面
由生成式模型可以产生判别式模型，但是由判别式模式没法形成生成式模型 
```

4. KMeans聚类算法？

```md
（1）适当选择c个类的初始中心；
（2）在第k次迭代中，对任意一个样本，求其到c个中心的距离，将该样本归到距离最短的中心所在的类；
（3）利用均值等方法更新该类的中心值；
（4）对于所有的c个聚类中心，如果利用（2）（3）的迭代法更新后，值保持不变，则迭代结束，否则继续迭代。
以上是KMeans（C均值）算法的具体步骤，可以看出需要选择类别数量，但初次选择是随机的，最终的聚类中心是不断迭代稳定以后的聚类中心。
```

5. 常见的六种容错机制：Fail-Over、Fail-Fast、Fail-Back、Fail-Safe，Forking 和 Broadcast

参考：https://www.cnblogs.com/shoufeng/p/14974891.html