# 第4章　RDD编程 :id=cp_4
---

## 本章学习内容：

1、RDD的创建方法、各种操作APP以及持久化和分区方法；
2、RDD的各种操作
3、RDD编程案例实现

**RDD是什么？**

- Spark核心概念
- 一个只读的、可分区的分布式数据集
- 可全部或部分缓存在内存中，在多次计算间重用。
- RDD API 采用scala语言实现

## RDD编程基础

本节介绍RDD编程的基础知识、包括RDD的创建、操作、API、持久化和分区等。

### RDD 创建

1. 从文件系统中加载数据创建RDD

1) 本地文件系统加载数据

- pyspark交互式环境中，执行如下命令

```
>>> lines = sc.textFile("file:///opt/spark/data/word.txt")
>>> lines.foreach(print)
Spark is better                                                     (0 + 2) / 2]
Hadoop is good 
Spark is fast 

```
在上述语句中，使用了 Spark 提供的 `SparkContext` 对象，名称为 `sc`，这是 `pyspark` 启动的时候自
动创建的，在交互式编程环境中可以直接使用。如果是编写独立应用程序，则可以通过如下语句生成 `SparkContext` 对象：

```shell
from pyspark import SparkConf,SparkContext
conf = SparkConf().setMaster("local").setAppName("My App")
sc = SparkContext(conf = conf)
```