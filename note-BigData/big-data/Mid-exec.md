# Chapter6 期中大作业

---

（本学习笔记整理自[datawhale-大数据处理技术导论](https://github.com/datawhalechina/juicy-bigdata)，部分内容来自其他相关参考教程）

## 面试题

### **6.1.1 简述Hadoop小文件弊端**

**答：**
Hadoop上大量 HDFS元数据信息存储在`NameNode`内存中,因此过多的小文件必定会压垮 `NameNode`的内存。
每个元数据对象约占 `150byte`，所以如果有 `1` 千万个小文件，每个文件占用一个`block`，则 `NameNode` 大约需要 2G 空间。 如果存储 `1` 亿个文件，则 `NameNode` 需要 `20G` 空间。 解决这个问题的方法: 合并小文件,可以选择在客户端上传时执行一定的策略先合并,或者是使用 `Hadoop 的` `CombineFileInputFormat\<K,V\>`实现小文件的合并


### **6.1.2 HDFS中DataNode挂掉如何处理？**

**答：**

客户端上传文件时与 `DataNode` 建立 `pipeline` 管道，管道的正方向是客户端向 `DataNode` 发送的数据包，管道反向是 `DataNode` 向客户端发送 `ack` 确认，也就是正确接收到数据包之后发送一个已确认接收到的应答。
当 `DataNode` 突然挂掉了，客户端接收不到这个 `DataNode` 发送的 `ack` 确认，客户端会通知 `NameNode`，`NameNode` 检查该块的副本与规定的不符，`NameNode` 会通知 `DataNode` 去复制副本，并将挂掉的 `DataNode` 作下线处理，不再让它参与文件上传与下载


### 6.1.3 HDFS中NameNode挂掉如何处理？

**答：**
方法一：
将 SecondaryNameNode 中数据拷贝到 namenode 存储数据的目录；

方法二：
使用 -importCheckpoint 选项启动 namenode 守护进程，从而将 SecondaryNameNode
中数据拷贝到 namenode 目录中。


### 6.1.4 HBase读写流程？

**答：**

Client 写入 -> 存入 MemStore，一直到 MemStore 满 -> Flush 成一个 StoreFile，
直至增长到一定阈值 -> 触发 Compact 合并操作 -> 多个 StoreFile 合并成一个
StoreFile，同时进行版本合并和数据删除 -> 当 StoreFiles Compact 后，逐步形成
越来越大的 StoreFile -> 单个 StoreFile 大小超过一定阈值后（默认 10G），触发
Split 操作，把当前 Region Split 成 2 个 Region，Region 会下线，新 Split 出的 2 个
孩子 Region 会被 HMaster 分配到相应的 HRegionServer 上，使得原先 1 个 Region
的压力得以分流到 2 个 Region 上
由此过程可知，HBase 只是增加数据，没有更新和删除操作，用户的更新和删除
都是逻辑层面的，在物理层面，更新只是追加操作，删除只是标记操作。
用户写操作只需要进入到内存即可立即返回，从而保证 I/O 高性能。

### 6.1.5 MapReduce为什么一定要有Shuffle过程

**答：**

MapReduce计算模型包括两个阶段：Map和Reduce,Map映射，负责数据的过滤分发，而Reduce规约，负责数据的计算归并。Reduce的数据来源于Map，Map的输出即Reduce的输入。
Shuffle 是来连接 Map 和 Reduce 的桥梁，一般把从 Map 产生输出开始到 Reduce 取得数据作为输入之前的过程称作shuffle。shuffle 分布在 Mapreduce 的 map 阶段和 reduce 阶段，在Map阶段包括Spill过程，在Reduce阶段包括copy和sort过程。 
由于 Shuffle 阶段涉及磁盘的读写和网络传输，因此 Shuffle 的性能直接影响整个程序的性能和吞吐量。


### 6.1.6 MapReduce中的三次排序

**答：**

MapReduced计算模型的Map任务和Reduce任务的过程中，一共发生了三次排序：

1）当map函数产生输出时，会首先写入内存的环形缓冲区，当达到设定的阀值，在刷写磁盘之前，后台线程会将缓冲区的数据划分成相应的分区。在每个分区中，后台线程按键进行内排序

2）在Map任务完成之前，磁盘上存在多个已经分好区，并排好序的，大小和缓冲区一样的溢写文件，这时溢写文件将被合并成一个已分区且已排序的输出文件。由于溢写文件已经经过第一次排序，所有合并文件只需要再做一次排序即可使输出文件整体有序。

3）在reduce阶段，需要将多个Map任务的输出文件copy到ReduceTask中后合并，由于经过第二次排序，所以合并文件时只需再做一次排序即可使输出文件整体有序

在这3次排序中第一次是内存缓冲区做的内排序，使用的算法使快速排序，第二次排序和第三次排序都是在文件合并阶段发生的，使用的是归并排序。

### 6.1.7 MapReduce为什么不能产生过多小文件

**答：**

MapReduce默认情况下使用extInputFormat 切片，其机制：  
（1）简单地按照文件的内容长度进行切片  
（2）切片大小，默认等于Block大小，可单独设置    
（3）切片时不考虑数据集整体，而是逐个针对每一个文件单独切片 MapTask  
因此如果有大量小文件，就会产生大量的MapTask，处理效率极其低下。

切片实例： 
```
（1）输入数据有两个文件：
filel.txt 320M
file2.txt 10M
（2）经过 FilelnputFormat（TextInputFormat为其实现类）的切片机制运算后，形成的切片信息如下：
filel.txt.splitl--0~128
filel.txt.split2--128～256
filel.txt.split3--256～320
file2.txt.splitl--0～10M
```

MapReduce大量小文件的优化策略：

**最优方案：** 在数据处理的最前端（预处理、采集），就将小文件合并成大文件，在上传到HDFS做后续 的分析

**补救措施：** 如果HDFS中已经存在大量的小文件了，可以使用另一种Inputformat来做切片（CombineFileInputformat），它的切片逻辑跟FileInputformat不同，它可以将多个小文件从逻辑上规划到一个切片中，这样，多个小文件就可以交给一个 MapTask 处理。

