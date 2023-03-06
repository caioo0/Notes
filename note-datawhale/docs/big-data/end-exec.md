# task08: 期末大作业

---

（本学习笔记整理自[datawhale-大数据处理技术导论](https://github.com/datawhalechina/juicy-bigdata)，部分内容来自其他相关参考教程）

## 面试题


### 10.1.1 hive外部表和内部表的区别

托管表(内部表)和外部表是Hive中的两种不同类型的表，在这篇文章中，我们将讨论Hive中表的类型以及它们之间的差异以及如何创建这些表以及何时将这些表用于特定的数据集。

1. 内部表
   托管表(Managed TABLE)也称为内部表(Internal TABLE)。这是Hive中的默认表。当我们在Hive中创建一个表，没有指定为外部表时，默认情况下我们创建的是一个内部表。如果我们创建一个内部表，那么表将在HDFS中的特定位置创建。默认情况下，表数据将在HDFS的/usr/hive/warehouse目录中创建。如果我们删除了一个内部表，那么这个表的表数据和元数据都将从HDFS中删除。
2. 当数据在Hive之外使用时，创建外部表(EXTERNAL TABLE)来在外部使用。无论何时我们想要删除表的元数据，并且想保留表中的数据，我们使用外部表。外部表只删除表的schema。

详细参见：[task06之一：数据仓库Hive基础关于表的知识点](https://caioo0.github.io/note-datawhale/#/docs/big-data/Hive?id=_64-hive%e6%95%b0%e6%8d%ae%e7%b1%bb%e5%9e%8b)

### 10.1.2 简述对Hive桶的理解？



### 10.1.3 HBase和Hive的区别？



### 10.1.4 简述Spark宽窄依赖



### 10.1.5 Hadoop和Spark的相同点和不同点



### 10.1.6 Spark为什么比MapReduce块？



### 10.1.7 说说你对Hadoop生态的认识

