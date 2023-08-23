# 第10节.Apache HBase进阶及性能优化

---

## 10.1 HBase Java API

### 10.1.1 环境准备

新建项目后在pom.xml中添加依赖：

```java
<dependency>
    <groupId>org.apache.hbase</groupId>
    <artifactId>hbase-server</artifactId>
    <version>1.2.12</version>
</dependency>

<dependency>
    <groupId>org.apache.hbase</groupId>
    <artifactId>hbase-client</artifactId>
    <version>1.2.12</version>
</dependency>

```

### 10.1.2 HBaseAPI

#### 10.1.2.1 获取Configuration对象

```java
public static Configuration conf;
static{
	//使用HBaseConfiguration的单例方法实例化
	conf = HBaseConfiguration.create();
        conf.set("hbase.zookeeper.quorum", "192.192.72.130");
        conf.set("hbase.zookeeper.property.clientPort", "2181");
}
```

#### 10.1.2.2 判断表是否存在

````java
public static boolean isTableExist(String tableName) throws MasterNotRunningException,
 ZooKeeperConnectionException, IOException{
	//在HBase中管理、访问表需要先创建HBaseAdmin对象
        //Connection connection = ConnectionFactory.createConnection(conf);
        //HBaseAdmin admin = (HBaseAdmin) connection.getAdmin();
	HBaseAdmin admin = new HBaseAdmin(conf);
	return admin.tableExists(tableName);
}

````

#### 10.1.2.3 创建表

````java
public static void createTable(String tableName, String... columnFamily) throws
 MasterNotRunningException, ZooKeeperConnectionException, IOException{
	HBaseAdmin admin = new HBaseAdmin(conf);
	//判断表是否存在
	if(isTableExist(tableName)){
		System.out.println("表" + tableName + "已存在");
		//System.exit(0);
	}else{
		//创建表属性对象,表名需要转字节
		HTableDescriptor descriptor = new HTableDescriptor(TableName.valueOf(tableName));
		//创建多个列族
		for(String cf : columnFamily){
			descriptor.addFamily(new HColumnDescriptor(cf));
		}
		//根据对表的配置，创建表
		admin.createTable(descriptor);
		System.out.println("表" + tableName + "创建成功！");
	}
}

````

#### 10.1.2.4 删除表

```java
public static void dropTable(String tableName) throws MasterNotRunningException,
 ZooKeeperConnectionException, IOException{
	HBaseAdmin admin = new HBaseAdmin(conf);
	if(isTableExist(tableName)){
		admin.disableTable(tableName);
		admin.deleteTable(tableName);
		System.out.println("表" + tableName + "删除成功！");
	}else{
		System.out.println("表" + tableName + "不存在！");
	}
}
```

#### 10.1.2.5 向表中插入数据

```java
public static void addRowData(String tableName, String rowKey, String columnFamily, String
 column, String value) throws IOException{
	//创建HTable对象
	HTable hTable = new HTable(conf, tableName);
	//向表中插入数据
	Put put = new Put(Bytes.toBytes(rowKey));
	//向Put对象中组装数据
	put.add(Bytes.toBytes(columnFamily), Bytes.toBytes(column),Bytes.toBytes(value));
	hTable.put(put);
	hTable.close();
	System.out.println("插入数据成功");
}
```

#### 10.1.2.6 删除多行数据

````java
public static void deleteMultiRow(String tableName, String... rows) throws IOException{
	HTable hTable = new HTable(conf, tableName);
	List<Delete> deleteList = new ArrayList<Delete>();
	for(String row : rows){
		Delete delete = new Delete(Bytes.toBytes(row));
		deleteList.add(delete);
	}
	hTable.delete(deleteList);
	hTable.close();
}
````

#### 10.1.2.7 获取所有数据

```java
public static void getAllRows(String tableName) throws IOException{
	HTable hTable = new HTable(conf, tableName);
	//得到用于扫描region的对象
	Scan scan = new Scan();
	//使用HTable得到resultcanner实现类的对象
	ResultScanner resultScanner = hTable.getScanner(scan);
	for(Result result : resultScanner){
		Cell[] cells = result.rawCells();
		for(Cell cell : cells){
			//得到rowkey
			System.out.println("行键:" + Bytes.toString(CellUtil.cloneRow(cell)));
			//得到列族
			System.out.println("列族" + Bytes.toString(CellUtil.cloneFamily(cell)));
			System.out.println("列:" + Bytes.toString(CellUtil.cloneQualifier(cell)));
			System.out.println("值:" + Bytes.toString(CellUtil.cloneValue(cell)));
		}
	}
}
```

#### 10.1.2.8 获取某一行数据

```java
public static void getRow(String tableName, String rowKey) throws IOException{
	HTable table = new HTable(conf, tableName);
	Get get = new Get(Bytes.toBytes(rowKey));
	//get.setMaxVersions();显示所有版本
    //get.setTimeStamp();显示指定时间戳的版本
	Result result = table.get(get);
	for(Cell cell : result.rawCells()){
		System.out.println("行键:" + Bytes.toString(result.getRow()));
		System.out.println("列族" + Bytes.toString(CellUtil.cloneFamily(cell)));
		System.out.println("列:" + Bytes.toString(CellUtil.cloneQualifier(cell)));
		System.out.println("值:" + Bytes.toString(CellUtil.cloneValue(cell)));
		System.out.println("时间戳:" + cell.getTimestamp());
	}
}
```

#### 10.1.2.9 获取某一行指定“列族:列”的数据

````java
public static void getRowQualifier(String tableName, String rowKey, String family, String
 qualifier) throws IOException{
	HTable table = new HTable(conf, tableName);
	Get get = new Get(Bytes.toBytes(rowKey));
	get.addColumn(Bytes.toBytes(family), Bytes.toBytes(qualifier));
	Result result = table.get(get);
	for(Cell cell : result.rawCells()){
		System.out.println("行键:" + Bytes.toString(result.getRow()));
		System.out.println("列族" + Bytes.toString(CellUtil.cloneFamily(cell)));
		System.out.println("列:" + Bytes.toString(CellUtil.cloneQualifier(cell)));
		System.out.println("值:" + Bytes.toString(CellUtil.cloneValue(cell)));
	}
}

````

## 10.2 HBase Rest API

包含的REST服务器可以作为守护程序运行，该守护程序启动嵌入式Jetty servlet容器并将servlet部署到其中。使用以下命令之一在前台或后台启动REST服务器。端口是可选的，默认为8080。

```java
# Foreground
$ bin/hbase rest start -p <port>

# Background, logging to a file in $HBASE_LOGS_DIR
$ bin/hbase-daemon.sh start rest -p <port>
```

要停止REST服务器，请在前台运行时使用Ctrl-C，如果在后台运行则使用以下命令。

```java
$ bin/hbase-daemon.sh stop rest
```

```java


# 创建表 curl -v -X PUT 'http://sandbox-hdp.hortonworks.com:9081/contact/schema' -H
"Accept: application/json" -H "Content-Type: application/json" -d
'{"@name":"contact","ColumnSchema":[{"name":"data"}]}'

#插入数据 
TABLE='contact' 
FAMILY='data' 
KEY=$(echo 'rowkey1' | tr -d "\n" | base64) 
COLUMN=$(echo 'data:test' | tr -d "\n" | base64) 
DATA=$(echo 'some data' | tr -d "\n" | base64)

curl -v -X PUT 'http://sandbox-hdp.hortonworks.com:9081/contact/rowkey1/data:test'
-H "Accept: application/json" -H "Content-Type: application/json" -d '{"Row": [{"key":"'$KEY'","Cell":[{"column":"'$COLUMN'","$":"'$DATA'"}]}]}'

# 获取指定rowkey的数据 
curl -v -X GET 'http://localhost:9081/contact/rowkey1/' -H "Accept: application/json"

# 删除表
curl -v -X DELETE 'http://localhost:9081/contact/schema' -H "Accept: application/json"

curl -v -X PUT 'http://hadoop5:9081/contact/schema' -H "Accept: application/json"
-H "Content-Type: application/json" -d '{"@name":"contact","ColumnSchema": [{"name":"data1"},{"name":"data2"}]}'

curl -v -X PUT 'http://hadoop5:9081/contact/rowkey1/data:test' -H "Accept: application/json" -H "Content-Type: application/json" -d '{"Row": [{"key":"'$KEY'","Cell":[{"column":"'$COLUMN'","$":"'$DATA'"}]}]}'


```

## 10.3 与Hive的集成

### 10.3.1 HBase与Hive的对比

1．Hive

(1) 数据仓库

Hive的本质其实就相当于将HDFS中已经存储的文件在Mysql中做了一个双射关系，以方便使用HQL去管理查询。

(2) 用于数据分析、清洗

Hive适用于离线的数据分析和清洗，延迟较高。

(3) 基于HDFS、MapReduce

Hive存储的数据依旧在DataNode上，编写的HQL语句终将是转换为MapReduce代码执行。

2．HBase

(1) 数据库

是一种面向列族存储的非关系型数据库。

(2) 用于存储结构化和非结构化的数据

适用于单表非关系型数据的存储，不适合做关联查询，类似JOIN等操作。

(3) 基于HDFS

数据持久化存储的体现形式是HFile，存放于DataNode中，被ResionServer以region的形式进行管理。

(4) 延迟较低，接入在线业务使用

面对大量的企业数据，HBase可以直线单表大量数据的存储，同时提供了高效的数据访问速度。

### 10.3.2 HBase与Hive集成使用

## 10.4 HBase优化

### 10.4.1 高可用

在HBase中HMaster负责监控HRegionServer的生命周期，均衡RegionServer的负载，如果HMaster挂掉了，那么整个HBase集群将陷入不健康的状态，并且此时的工作状态并不会维持太久。所以HBase支持对HMaster的高可用配置。

1）关闭HBase集群（如果没有开启则跳过此步）

```shell
$ bin/stop-hbase.sh
```

2) 在conf目录下创建backup-masters文件

```shell
$ touch conf/backup-masters
```

3 在backup-masters文件中配置高可用HMaster节点

```shell
$ echo hadoop2 > conf/backup-masters
```

4 将整个conf目录scp到其他节点

```shell
scp -r conf/ hadoop3:/opt/module/hbase
scp -r conf/ hadoop4:/opt/module/hbase
```

5．打开页面测试查看

[http://hadooo2:16010](http://linux01:16010)

## 学习资料

1. https://www.w3cschool.cn/hbase_doc/hbase_doc-r6ew2vvl.html
