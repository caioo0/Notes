# Part C: 自适应提升法

----

（本学习笔记来源于[DataWhale-树模型与集成学习](https://github.com/datawhalechina/machine-learning-toy-code)）

知识点归纳如下：
- Adaboost概述
- Adaboost处理分类和回归任务的算法原理，包括SAMME算法、SAMME.R算法和Adaboost.R2算法。


## Adaboost概述

**自适应提升算法（Adaboost）** 英文全称为：$Adaptive Boosting$ ,**自适应**是指Adaboost会根据本轮样本的误差结果来分配下一轮模型训练时样本在模型中的相对权重，即对错误的或偏差大的样本适度“重视”，对正确的或偏差小的样本适度“放松”

“重视”和“放松”具体体现在：Adaboost的`损失函数设计`以及`样本权重的更新策略`；

