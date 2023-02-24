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



### 6.1.4 HBase读写流程？

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



### 6.1.6 MapReduce中的三次排序



### 6.1.7 MapReduce为什么不能产生过多小文件