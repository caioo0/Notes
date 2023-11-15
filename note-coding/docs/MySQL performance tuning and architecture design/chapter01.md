# 第2章　MySQL架构组成

## MySQL物理文件组成

![image-20231113095836151](.\img\image-20231113095836151.png)



1、非必要不需要查询缓存

2、rows_examined 

### 日志文件 

#### 错误日志：Error Log 

录了MyQL Server运行过程中所有较为严重的警告和错误信息，以及MySQL Server每次启动和关闭的详细信息
