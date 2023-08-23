

## spark的特点

1）运行速度快
- Spark基于内存计算，速度要比磁盘计算快得多
- spark程序运行是基于线程模型，线程方式运行作业远比进程模式开销小
- spark框架有优化器，可以优化作业的执行，提高作业的执行效率

2）易用性
- 支持Java、python和scala的API
- 支持超过80种高级算法，用户可以快速构建不同的应用。
- 支持交互式python和scala的shell

3）支持复杂查询
- spark除了支持Map和Reduce操作意外，还支持sql查询、流式计算、机器学习和图计算，同时，用户可以在同一个工作流中无缝搭配这些计算范式。

4）实时的流处理~~~~
- spark streaming主要用来对数据进行实时处理

5）容错性
- spark引进了弹性分布式数据集（Resilient Distributed Dataset,RDD）,它是分布在一组节点中的只读对象集合。这些对象集合是弹性的，如果丢失了一部分对象集合，spark则可以根据父RDD对它们进行计算。另外在对RDD进行转换计算时，可以通过CheckPoint方法将数据持久化（比如可以持久化的HDFS）,从而实现容错。

## 弹性分布式数据集RDD

- RDD: 分布式的元素集合。
- spark数据操作包括：创建RDD,转化已有的RDD，调用RDD操作进行求值。
- spark会自动将RDD中的数据分发到集群上，并将操作并行化执行。

### 1. RDD 简介

Spark数据存储的核心是RDD.r



## 示例测试

### Spark shell测试运行单词词频统计
```shell
[root@hadoop5 spark-2.4.5-bin-hadoop2.7]# ls
bin  conf  data  examples  jars  kubernetes  LICENSE  licenses  logs  NOTICE  python  R  README.md  RELEASE  sbin  work  yarn
[root@hadoop5 spark-2.4.5-bin-hadoop2.7]# mkdir test
[root@hadoop5 spark-2.4.5-bin-hadoop2.7]# cd test
[root@hadoop5 test]# touch djt.log
[root@hadoop5 test]# ls
djt.log
[root@hadoop5 test]# cat djt.log
hadoop hadoop hadoop
spark spark spark
[root@hadoop5 spark-2.4.5-bin-hadoop2.7]# bing/spark-shell
scala> val line = sc.textFile("/root/install/spark-2.4.5-bin-hadoop2.7/test/djt.log")
line: org.apache.spark.rdd.RDD[String] = /root/install/spark-2.4.5-bin-hadoop2.7/test/djt.log MapPartitionsRDD[3] at textFile at <console>:24
scala> line.flatMap(_.split(" ")).map((_,1)).reduceByKey(_+_).collect().foreach(println)
(spark,3)                                                                       
(hadoop,3)


```