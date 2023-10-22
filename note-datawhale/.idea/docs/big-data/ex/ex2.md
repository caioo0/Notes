# Flink基础

## 一. Flink与Spark区别:

Flink:事件驱动型,被动拉取数据(没有数据就什么也不干,阻塞到当前)

Spark:时间驱动型,主动拉取数据(即使没有数据,到达一定时间也会处理)

Flink:一切都是由流构成   (flink1.12实现了流批处理)

Spark:一切都是由批构成

Flink:在流的基础上做批处理  延迟是毫秒级

Spark:在批的基础上做流处理  延迟是秒级

Spark比Flink好的地方,吞吐量大

## 二. Yarn模式

会随机挑选一台机器运行flink提交的任务,flink webUI需要去yarn里面查看,或者在运行窗口的提示有地址值(每次启动地址值会发生改变)

### 2.1 Flink on Yarn的3种部署模式

#### Session-Cluster

适合多个小job,因为flink会在yarn中先启一个集群,后续提交的其他作业会直接运行在这个集群上,相互不隔离

#### Per-Job-Cluster

每提交一个job会在yarn中启动一个flink集群,并且这些作业是相互隔离的,同时main方法在本地上运行;

适合规模大长时间运行的作业。

#### Application Mode

Application Mode下, 用户的main函数是在集群中执行的; 并且当一个application中有多个job的话，per-job模式是一个job对应一个yarn中的application，而Application Mode则这个application中对应多个job。

### 2.2 Yarn高可用集群leader重启机制

```
yarn的高可用是同时只启动一个Jobmanager, 当这个Jobmanager挂了之后, yarn会再次启动一个, 其实是利用的yarn的重试次数来实现的高可用。
```

```
除了设置的重启次数外,还有一个时间的机制（Akka超时时间）, 如果在一定的时间内jobManager重新拉取了几次还是挂掉的话，那就会真正的挂掉。
```

## 三. Flink运行架构

### 3.1 运行架构

Flink运行时包含2种进程:1个JobManager和至少1个TaskManager

1个job ->  1个Master

多个job -> 1个JobManager

#### 3.1.1 JobManager

```
JobManager会先接收到要执行的应用程序，这个应用程序会包括：作业图（JobGraph）、逻辑数据流图（logical dataflow graph）和打包了所有的类、库和其它资源的JAR包。
```

```
JobManager会把JobGraph转换成一个物理层面的数据流图，这个图被叫做“执行图”（ExecutionGraph）,
```

```
JobManager会向资源管理器（ResourceManager）请求执行任务必要的资源，也就是任务管理器（TaskManager）上的插槽（slot）。
```

##### <font color='red'>3.1.1.1 JobManager包含的3个不同的组件:    </font>

##### ResourceManager

```
主要负责管理任务管理器（TaskManager）的插槽（slot），TaskManger插槽是Flink中定义的处理资源单元。
```

```
当JobManager申请插槽资源时，ResourceManager会将有空闲插槽的TaskManager分配给JobManager。如果ResourceManager
```

<font color='red'>没有足够的插槽</font>来满足JobManager的请求，它还可以向<font color='red'>资源提供平台发起会话(yarn模式下可以实现动态扩容)</font>，以提供启动TaskManager进程的容器。另外，ResourceManager还负责终止空闲的TaskManager，释放计算资源。

##### Dispatcher

负责接收用户提供的作业，启动一个新的JobMaster 组件. Dispatcher也会启动一个Web UI,  在架构中时非必需的, 取决于提交运行方式

##### JobMaster

```
JobMaster负责管理单个JobGraph的执行.多个Job可以同时运行在一个Flink集群中, 每个Job都有一个自己的JobMaster.
```

##### <font color='red'>3.1.1.2 总结JobManager主要作用：</font>

```

```

**1.** 接受客户端请求。

```

```

**2.** 划分任务.

```

```

**3.** 申请资源.

### 3.2. 核心概念

#### 3.2.1 **TaskManager与Slots**

![image-20211211115535575](https://gitee.com/jerry-chen417/picgo/raw/master/img/202112111155617.png)

##### TaskManager:

1.工作进程，任务都在TaskManager上运行
2.TaskManager中有资源（Slot）
3.需要像JobManager进行交互从而进行资源的注册和使用
4.多个TaskManager可以交换数据

##### Slots:

1.slot可以共享(Job内部), 外部共享只有一种情况（Session）。

2.slot会均分内存资源，进而达到内存隔离，相互之间不会占用内存。但cpu资源不会隔离，可以共享cpu资源。

TaskManager下的slot个数和默认并行度可以由一下参数设定

```
taskmanager.numberOfTaskSlots: 1

parallelism.default: 1
```

##### 端口占用查看: netstat -npl | grep 9999

![image-20211210102030250](https://gitee.com/jerry-chen417/picgo/raw/master/img/202112101020404.png)

#### 3.2.2 Parallelism（并行度）

并行度优先级：算子指定>env全局指定>提交参数>配置文件

##### slot个数与并行度关系：

1.默认情况下slot个数等于程序中最大算子的并行度。
2.在有共享组的情况下，slot个数等于程序每个共享组中最大算子的并行度之和。

#### 3.2.3 Operator Chains（任务链）

<font color='red'>slot个数在默认情况下等于程序中算子的最大并行度;</font>

<font color='red'>在有多个共享组的情况下,等于每个共享组中最大并行度的和</font>

##### One-to-one：

```
stream(比如在source和map operator之间)维护着分区以及元素的顺序。那意味着flatmap 算子的子任务看到的元素的个数以及顺序跟source 算子的子任务生产的元素的个数、顺序相同，map、fliter、flatMap等算子都是one-to-one的对应关系。
```

##### Redistributing：

```
stream(map()跟keyBy/window之间或者keyBy/window跟sink之间)的分区会发生改变。每一个算子的子任务依据所选择的transformation发送数据到不同的目标任务。例如，keyBy()基于hashCode重分区、broadcast和rebalance会随机重新分区，这些算子都会引起redistribute过程，而redistribute过程就类似于Spark中的shuffle过程。
```

```
相同并行度的one to one操作，Flink将这样相连的算子链接在一起形成一个task，原来的算子成为里面的一部分。
```

<font color='red'>每个task被一个线程执行.</font>

##### 链接行为的指定

```java
* 算子.startNewChain() => 与前面断开
* 算子.disableChaining() => 与前后都断开
* env.disableOperatorChaining() => 全局都不串
```

断开操作链的好处在于减少某个slot的压力。

##### 共享组设置

哪个算子设置共享组,就从该算子往后都算进一个共享组里

![image-20211211090057967](https://gitee.com/jerry-chen417/picgo/raw/master/img/202112110901201.png)

##### 任务链以及共享组总结：

1.任务链的好处，避免数据跨节点传输。
2.断开任务链的好处，减少某个slot的压力。
3.默认情况下所有算子都是同一个共享组，任务所需要的slot数量：最大算子的并行度。
4.当使用共享组时，任务所需要的slot数量：每个共享组中最大并行度的和。

## 四. Flink流处理核心编程

![image-20211214200644835](https://gitee.com/jerry-chen417/picgo/raw/master/img/202112142006880.png)

### 4.1 Source

#### 4.1.1.从Java的集合中读取数据

```
List<WaterSensor> waterSensors = Arrays.asList

env . fromCollection(waterSensors)
```

#### 4.1.2 从文件读取数据

```
env.readTextFile("input")


```

##### 1. 说明:

1.参数可以是目录也可以是文件
2.路径可以是相对路径也可以是绝对路径
3.相对路径是从系统属性user.dir获取路径: idea下是project的根目录, standalone模式下是集群节点根目录
4.也可以从hdfs目录下读取, 使用路径:hdfs://hadoop102:8020/...., 由于Flink没有提供hadoop相关依赖, 需要pom中添加相关依赖:

```
<dependency>
    <groupId>org.apache.hadoop</groupId>
    <artifactId>hadoop-client</artifactId>
    <version>3.1.3</version>
</dependency>
```

##### 2. HDFS配置高可用,填写HDFS地址

没有配置高可用,读写路径为hdfs://hadoop102:8020/

<font color='red'>配置高可用,读写路径为:hdfs://mycluster/</font>

mycluster映射了hadoop102:8020   hadoop103:8020  以及hadoop104:8020, 如果102挂掉,会自动找到对应运行的NameNode

![image-20211210144720163](https://gitee.com/jerry-chen417/picgo/raw/master/img/202112101447206.png)

![image-20211210145248213](https://gitee.com/jerry-chen417/picgo/raw/master/img/202112101452246.png)

#### 4.1.3 从Kafka读取数据

添加相应的依赖

```
<dependency>
    <groupId>org.apache.flink</groupId>
    <artifactId>flink-connector-kafka_2.12</artifactId>
    <version>1.13.0</version>
</dependency>
```

参考代码

```
import org.apache.flink.api.common.serialization.SimpleStringSchema;
import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
import org.apache.flink.streaming.connectors.kafka.FlinkKafkaConsumer;

import java.util.Properties;

public class Flink03_Source_Kafka {
    public static void main(String[] args) throws Exception {

        // 0.Kafka相关配置
        Properties properties = new Properties();
        properties.setProperty("bootstrap.servers", "hadoop102:9092,hadoop103:9092,hadoop104:9092");
        properties.setProperty("group.id", "Flink01_Source_Kafka");
        properties.setProperty("auto.offset.reset", "latest");
  
        // 1. 创建执行环境
        StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment();
        env
          .addSource(new FlinkKafkaConsumer<>("sensor", new SimpleStringSchema(), properties))
          .print("kafka source");
  
        env.execute();
    }

}
```

开启kafka生产者,测试消费

```
kafka-console-producer.sh --broker-list hadoop102:9092 --topic sensor
```

#### 4.1.4 自定义Source

自定义 SourceFunction：

1. 实现 SourceFunction相关接口
2. 重写两个方法：
   run(): 主要逻辑
   cancel(): 停止逻辑

如果希望 Source可以指定并行度，那么就 实现 ParallelSourceFunction 这个接口

```
  public static class MySource implements SourceFunction<WaterSensor> {
        private String host;
        private int port;
        private volatile boolean isRunning = true;
        private Socket socket;

        public MySource(String host, int port) {
            this.host = host;
            this.port = port;
        }


        @Override
        public void run(SourceContext<WaterSensor> ctx) throws Exception {
            // 实现一个从socket读取数据的source
            socket = new Socket(host, port);
            BufferedReader reader = new BufferedReader(new InputStreamReader(socket.getInputStream(), StandardCharsets.UTF_8));
            String line = null;
            while (isRunning && (line = reader.readLine()) != null) {
                String[] split = line.split(",");
                ctx.collect(new WaterSensor(split[0], Long.valueOf(split[1]), Integer.valueOf(split[2])));
            }
        }

        /**
         * 大多数的source在run方法内部都会有一个while循环,
         * 当调用这个方法的时候, 应该可以让run方法中的while循环结束
         */

        @Override
        public void cancel() {
            isRunning = false;
            try {
                socket.close();
            } catch (IOException e) {
                e.printStackTrace();
            }
        }
    }
}
```

### 4.2 Transform

#### 4.2.1 map

```
作用:
	将数据流中的数据进行转换, 形成新的数据流，消费一个元素并产出一个元素

参数
lambda表达式或MapFunction实现类

返回
DataStream → DataStream
```

source到map是以轮询的方式发送数据

##### Rich...Function类

1.默认生命周期方法, 初始化方法open(), 在每个并行度上只会被调用一次, 而且先被调用

2.默认生命周期方法, 最后一个方法close(), 做一些清理工作, 在每个并行度上只调用一次, 而且是最后被调用，但读文件时在每个并行度上调用两次。

3.运行时上下文getRuntimeContext()方法提供了函数的RuntimeContext的一些信息，例如函数执行的并行度，任务的名字，以及state状态. 开发人员在需要的时候自行调用获取运行时上下文对象.

#### 4.2.2 flatMap

```
作用
消费一个元素并产生零个或多个元素

参数
FlatMapFunction实现类

返回
DataStream → DataStream
```

#### 4.2.3 filter

```
作用
根据指定的规则将满足条件（true）的数据保留，不满足条件(false)的数据丢弃

参数
FlatMapFunction实现类

返回
DataStream → DataStream
```

#### 4.2.4 KeyBy

```
作用
	把流中的数据分到不同的分区中.具有相同key的元素会分到同一个分区中.一个分区中可以有多重不同的key.
	在内部是使用的hash分区来实现的.

分组与分区的区别：
    分组： 是一个逻辑上的划分，按照key进行区分，经过 keyby，同一个分组的数据肯定会进入同一个分区
    分区： 下游算子的一个并行实例（等价于一个slot），同一个分区内，可能有多个分组
  
参数
	Key选择器函数: interface KeySelector<IN, KEY>
	注意: 什么值不可以作为KeySelector的Key:
		没有覆写hashCode方法的POJO, 而是依赖Object的hashCode. 因为这样分组没有任何的意义: 每个元素都会得到一个独立无二的组.  实际情况是:可以运行, 但是分的组没有意义.
		任何类型的数组

返回
	DataStream → KeyedStream
```

##### KeyBy源码解析:

对key进行两次hash

keyGroupid通过以下方式计算得到{
computeKeyGroupForKeyHash(key.hashCode(), maxParallelism) 对key做了一次hash
MathUtils.murmurHash(keyHash) % maxParallelism; 对key又做了一次Hash
}
Group的索引通过以下方式计算得到：keyGroupId * parallelism / maxParallelism;

#### 4.2.5 Shuffle

```
作用
	把流中的元素随机打乱. 对同一个组数据, 每次只需得到的结果都不同.

参数
	无

返回
DataStream → DataStream
```

随机返回key

![image-20211211102634886](https://gitee.com/jerry-chen417/picgo/raw/master/img/202112111026942.png)

#### 4.2.6 connect

```
作用:
	连接两个保持他们类型的数据流，两个数据流被connect之后，只是被放在了一个同一个流中，内部依然保持各自的数据和形式不发生任何变化，两个流相互独立。

参数
	另外一个流

返回
	DataStream[A], DataStream[B] -> ConnectedStreams[A,B]
```

注意:
1.两个流中存储的数据类型可以不同
2.只是机械的合并在一起, 内部仍然是分离的2个流
3.只能2个流进行connect, 不能有第3个参与

#### 4.2.7 union

```
作用
	对两个或者两个以上的DataStream进行union操作，产生一个包含所有DataStream元素的新DataStream

```

##### connect与 union 区别：

1.union之前两个流的类型必须是一样，connect可以不一样
2.connect只能操作两个流，union可以操作多个。

#### 4.2.8 简单滚动聚合算子

sum,     min,    max,    minBy,    maxBy

```
作用
	KeyedStream的每一个支流做聚合。执行完成后，会将聚合的结果合成一个流返回，所以结果都是DataStream

参数
	如果流中存储的是POJO或者scala的样例类, 参数使用字段名
	如果流中存储的是元组, 参数就是位置(基于0...)

返回
KeyedStream -> SingleOutputStreamOperator
```

##### 注意:

```
滚动聚合算子： 来一条，聚合一条
        1、聚合算子在 keyby之后调用，因为这些算子都是属于 KeyedStream里的
        2、聚合算子，作用范围，都是分组内。 也就是说，不同分组，要分开算。
```

###### <font color='red'>   3、max、maxBy的区别：</font>

```
max：取指定字段的当前的最大值，如果有多个字段，其他非比较字段，以第一条为准
            maxBy：取指定字段的当前的最大值，如果有多个字段，其他字段以最大值那条数据为准；
            如果出现两条数据都是最大值，由第二个参数决定： true => 其他字段取 比较早的值； false => 其他字段，取最新的值
```

#### 4.2.8 Reduce

```
作用
	一个分组数据流的聚合操作，合并当前的元素和上次聚合的结果，产生一个新的值，返回的流中包含每一次聚合的结果，而不是只返回最后一次聚合的最终结果。

参数、
interface ReduceFunction<T>

返回
KeyedStream -> SingleOutputStreamOperator
```

##### ***\*注意:\****

```
1、 一个分组的第一条数据来的时候，不会进入reduce方法。
```

```
2、 输入和输出的 数据类型，一定要一样。
```

#### 4.2.9 process

```
作用
	process算子在Flink算是一个比较底层的算子,很多类型的流上都可以调用,可以从流中获取更多的信息(不仅仅数据本身)
```

#### 4.2.10 对流重新分区的几个算子

```
KeyBy
	先按照key分组, 按照key的双重hash来选择后面的分区
shuffle
	对流中的元素随机分区

reblance
	对流中的元素平均分布到每个区.当处理倾斜数据的时候, 进行性能优化

rescale(会分组)
同 rebalance一样, 也是平均循环的分布数据。但是要比rebalance更高效, 因为rescale不需要通过网络, 完全走的"管道"。
```

![image-20211214203600726](https://gitee.com/jerry-chen417/picgo/raw/master/img/202112142036779.png)

### 4.3 Sink

#### 4.3.1 KafkaSink

添加Kafka Connector依赖

```
<dependency>
  <groupId>org.apache.flink</groupId>
  <artifactId>flink-connector-kafka_2.12</artifactId>
  <version>1.13.0</version>
</dependency>

<dependency>
  <groupId>com.alibaba</groupId>
  <artifactId>fastjson</artifactId>
  <version>1.2.75</version>
</dependency>
```

启动Kafka集群

Sink到Kafka的示例代码

```
env.fromCollection(waterSensors)
          .map(JSON::toJSONString)
          .addSink(new FlinkKafkaProducer<String>("hadoop102:9092", "topic_sensor", new SimpleStringSchema()));
```

#### 4.3.2 redisSink

添加Redis Connector依赖

```
<!-- https://mvnrepository.com/artifact/org.apache.flink/flink-connector-redis -->
<dependency>
    <groupId>org.apache.bahir</groupId>
    <artifactId>flink-connector-redis_2.11</artifactId>
<version>1.0</version>
</dependency>
```

启动Redis服务器

Sink到Redis的示例代码

```java
    // 连接到Redis的配置
        FlinkJedisPoolConfig redisConfig = new FlinkJedisPoolConfig.Builder()
          .setHost("hadoop102")
          .setPort(6379)
          .setMaxTotal(100)
          .setTimeout(1000 * 10)
          .build();
        StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment().setParallelism(1);
        env
          .fromCollection(waterSensors)
          .addSink(new RedisSink<>(redisConfig, new RedisMapper<WaterSensor>() {
              /*
                key                 value(hash)
                "sensor"            field           value
                                    sensor_1        {"id":"sensor_1","ts":1607527992000,"vc":20}
                                    ...             ...
               */

              @Override
              public RedisCommandDescription getCommandDescription() {
                  // 返回存在Redis中的数据类型  存储的是Hash, 第二个参数是外面的key
                  return new RedisCommandDescription(RedisCommand.HSET, "sensor");
              }

              @Override
              public String getKeyFromData(WaterSensor data) {
                  // 从数据中获取Key: Hash的Key
                  return data.getId();
              }

              @Override
              public String getValueFromData(WaterSensor data) {
                  // 从数据中获取Value: Hash的value
                  return JSON.toJSONString(data);
              }
          }));
```

```java
/**
 * 当使用hash类型时，这个key指的是Hash中的小Key
 * 如果不是hash类型时，这个key指的是Redis的key
 * @param waterSensor
 * @return
 */
 @Override
 public String getKeyFromData(WaterSensor waterSensor) {
                return waterSensor.getId();
            }
```

#### 4.3.3 ElasticsearchSink

添加Elasticsearch Connector依赖

```
<!-- https://mvnrepository.com/artifact/org.apache.flink/flink-connector-elasticsearch6 -->
<dependency>
    <groupId>org.apache.flink</groupId>
    <artifactId>flink-connector-elasticsearch6_2.12</artifactId>
    <version>1.13.0</version>
</dependency>
```

启动Elasticsearch集群

Sink到Elasticsearch的示例代码

```
        List<HttpHost> esHosts = Arrays.asList(
          new HttpHost("hadoop102", 9200),
          new HttpHost("hadoop103", 9200),
          new HttpHost("hadoop104", 9200));
        StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment().setParallelism(1);
        env
          .fromCollection(waterSensors)
          .addSink(new ElasticsearchSink.Builder<WaterSensor>(esHosts, new ElasticsearchSinkFunction<WaterSensor>() {

              @Override
              public void process(WaterSensor element, RuntimeContext ctx, RequestIndexer indexer) {
                  // 1. 创建es写入请求
                  IndexRequest request = Requests
                    .indexRequest("sensor")
                    .type("_doc")
                    .id(element.getId())
                    .source(JSON.toJSONString(element), XContentType.JSON);
                  // 2. 写入到es
                  indexer.add(request);
              }
          }).build());
```

如果是无界流, 需要配置bulk的缓存 注意：<font color='red'>生产中不要这样设置为1</font>
esSinkBuilder.setBulkFlushMaxActions(1);

#### 4.3.4 自定义Sink

```
1.继承RichSinkFunction
2.重写open()  数据进入,只调用一次
 	close()   结束调用一次
 	invoke()  每条数据调用一次
```

写到Mysql的自定义Sink示例代码

```
       env.fromCollection(waterSensors)
          .addSink(new RichSinkFunction<WaterSensor>() {

             private PreparedStatement ps;
              private Connection conn;

              @Override
              public void open(Configuration parameters) throws Exception {
                  conn = DriverManager.getConnection("jdbc:mysql://hadoop102:3306/test?useSSL=false", "root", "000000");
                  ps = conn.prepareStatement("insert into sensor values(?, ?, ?)");
              }

              @Override
              public void close() throws Exception {
                ps.close();
                  conn.close();
              }

              @Override
              public void invoke(WaterSensor value, Context context) throws Exception {
                ps.setString(1, value.getId());
                  ps.setLong(2, value.getTs());
                  ps.setInt(3, value.getVc());
                  ps.execute();
              }
          });
```

#### 4.3.5 JDBCSink

添加JDBC Connector依赖

```
<dependency>
  <groupId>org.apache.flink</groupId>
  <artifactId>flink-connector-jdbc_2.12</artifactId>
  <version>1.13.0</version>
</dependency>
```

Sink到MySQL的示例代码

```
       //TODO 4.JDBCSink将数据写入MySQL
        result.addSink(JdbcSink.sink(
                "insert into sensor values (?,?,?)",
                (ps,t)->{
                    ps.setString(1,t.getId());
                    ps.setLong(2, t.getTs());
                    ps.setInt(3, t.getVc());
                },
                new JdbcExecutionOptions.Builder()
                        //设置来一条写一条与ES中相似
                .withBatchSize(1)
                .build(),
                new JdbcConnectionOptions.JdbcConnectionOptionsBuilder()
                        .withUrl("jdbc:mysql://hadoop102:3306/test?useSSL=false")
                        .withUsername("root")
                        .withPassword("000000")
                        .withDriverName(Driver.class.getName())
                .build()
        ));
```

### 4.4 运行时模式

```
执行模式有3个选择可配:
1 STREAMING(默认)
2 BATCH
3 AUTOMATIC
```

#### 4.4.1 有界数据用STREAMING和BATCH的区别

STREAMING模式下, 数据是来一条输出一次结果。
BATCH模式下, 数据处理完之后, 一次性输出结果。

Flink 1.12版本有一个bug, 聚合函数底层调用reduce,当数据只有一条时,不会进入reduce,数据会丢, 1.13修复了这个bug

#### Flink 1.12执行结果

![image-20211213090628780](https://gitee.com/jerry-chen417/picgo/raw/master/img/202112130906861.png)

#### Flink 1.13执行结果

![image-20211213090701073](https://gitee.com/jerry-chen417/picgo/raw/master/img/202112130907123.png)

## 五. Flink高阶编程

### 5.1 时间窗口源码解析：

#### 1.为什么窗口的左闭右开的？

```java
public long maxTimestamp() {  
    return end - 1;}

// 方法在TimeWindow类第行84
/**点源码的路径:
1.先点of(TumblingProcessingTimeWindows.of)
2.再到TumblingProcessingTimeWindows的69行有一个assignWindows(分配窗口)方法
3.再点开79行的TimeWindows,到TimeWindows的84行
官方关于这个方法的注解:
    @return The largest timestamp that still belongs to this window.
*/
```

这个方法的作用是获取这个窗口的最大时间戳
比如：[0,5）这个窗口中能获取到的最大时间戳4999毫秒，因此，窗口是左闭右开的。

#### 2.窗口的开启时间跟数据来的时间到底有什么关系？

timestamp - (timestamp - offset + windowSize) % windowSize;

```
源码路径:
1.先点of(TumblingProcessingTimeWindows.of)
2.再到TumblingProcessingTimeWindows的77行点getWindowStartWithOffset方法,需要方法传入的参数now,在71行有初始化final long now = context.getCurrentProcessingTime()
```

通过以上公式来计算出窗口的开始时间
比如：开启一个5秒的滚动窗口，offset设置为0，第3秒来了第一条数据，带入公式计算
3-(3-0+5)%5=0
因此，窗口开启时间是0s

#### 3.滑动窗口中，是如何判断一个元素到底属于哪些窗口的？

首先通过以下公式得到lastStart  注意：windowSize这个是滑动步长

```
timestamp - (timestamp - offset + windowSize) % windowSize;
```

比如：开启一个6秒的滑动窗口，滑动步长为3S，第2秒来了第一条数据，带入公式首先计算得到laststart=0s
再通过以下程序计算得到这个数据所属的所有窗口

```
for (long start = lastStart; start > timestamp - size; start -= slide) {
            windows.add(new TimeWindow(start, start + size));
        }
start:0        -3       -6
      0>-4?    -3>-4?   -6>-4?
Window:[0,6)  [-3,3)
```

```java
源码路径:
1.先点of方法(SlidingProcessingTimeWindows.of)
  
2.在SlidingProcessingTimeWindows的72行getWindowStartWithOffset方法先得到lastStart
  
3.然后经过73行的for循环得到对应的窗口集合
for (long start = lastStart; start > timestamp - size; start -= slide) {
            windows.add(new TimeWindow(start, start + size));
        }
```

#### 4.offset是干嘛的？

可以改变窗口的开始时间。

```
long start = TimeWindow.getWindowStartWithOffset()
offset作为getWindowStartWithOffset的间接参数影响窗口的开始时间
```

#### 5.为什么短时间内来大量的数据不会创建大量的窗口

```java
Collections.singletonList(new TimeWindow(start, start + size))
```

因为用到以上单例集合，类似于单例模式，所以不会创建大量的对象

#### 6.动态间隔会话窗口源码简单解析（了解）

TimeWindow(currentProcessingTime, currentProcessingTime + sessionTimeout))
传入数据
s1,5,1  Window(cur1Time,curTime+5s)
s1,20,1 Window(cur2Time,curTime+20s)
s1,1,1  Window(cur3Time,curTime+1s)

因为有多个窗口，在合并的时候需要符合以下规则
new TimeWindow(Math.min(start, other.start), Math.max(end, other.end))   (TimeWindow第122行)

```
源码路径:
1.点withDynamicGap (ProcessingTimeSessionWindows.withDynamicGap)

2.点withDynamicGap方法返回的DynamicProcessingTimeSessionWindows

3.在该类的106行mergeWindows方法,点开mergeWindows

4.然后TimeWindows的234行的cover方法
return new TimeWindow(Math.min(start, other.start), Math.max(end, other.end));

```

#### 7.窗口什么时候被触发

这个条件主要用于读有界数据时，当数据读完时依据数据生成的WaterMark达不到触发的标准，则用以下方式触发
if (window.maxTimestamp() <= ctx.getCurrentWatermark()) {
// if the watermark is already past the window fire immediately
return TriggerResult.FIRE;
或者
return time == window.maxTimestamp() ? TriggerResult.FIRE : TriggerResult.CONTINUE;

![image-20211214153541464](https://gitee.com/jerry-chen417/picgo/raw/master/img/202112141535540.png)

#### 8.窗口什么时候被销毁

```
窗口的最大时间戳(end-1)+允许迟到的时间
long cleanupTime = window.maxTimestamp() + allowedLateness;
达到定时清除的时间后调用一下方法
clearAllState(triggerContext.window, windowState, mergingWindows);
mergingWindows.retireWindow(window);退役窗口
```

### 5.2 时间语义

#### 5.2.1  处理时间(process time)

处理时间是指的执行操作的各个设备的时间

#### 5.2.2 事件时间(event time)

可以理解为每个事件（每条数据）所发生时间（所生成的时间）

##### **注意:**

在1.12之前默认的时间语义是处理时间, 从**<font color='red'>1.12开始</font>**, Flink内部已经把**<font color='red'>默认的语义</font>**改成了**<font color='red'>事件时间</font>**

### 5.3 WaterMark

#### 设置watermark

```
DataStream.assignTimestampsAndWatermarks(
                WatermarkStrategy
                        .<WaterSensor>forBoundedOutOfOrderness(Duration.ofSeconds(3))
                        //指定哪个字段作为事件时间字段
                        .withTimestampAssigner(new SerializableTimestampAssigner<WaterSensor>() {
                            @Override
                            public long extractTimestamp(WaterSensor element, long recordTimestamp) {
                                return element.getTs() * 1000;
                            }
                        })
        )
```

•Flink 暴露了 TimestampAssigner 接口供我们实现，使我们可以自定义如何从事件数据中抽取时间戳和生成watermark

#### 5.3.1 总结什么是WaterMark：

```
1、衡量事件时间(Event Time)的进展,可以设定延迟触发
2、是一个特殊的时间戳，生成之后随着流的流动而向后传递。
3、用来处理数据乱序的问题。
4、触发窗口的计算、关闭。
5、单调递增的（时间不能倒退）。
Flink认为，小于Watermark时间戳的数据处理完了，不应该再出现。
```

保证watermark是单调递增的(每次取最大值)

![image-20211214104556353](https://gitee.com/jerry-chen417/picgo/raw/master/img/202112141046467.png)

#### 5.3.2 Flink中WaterMark是如何产生的

有序和无序 两种本质上是一样的,outOfOrdernessMills=0(乱序程度)就是有序的

##### 1.有序流中的水印WaterMark

WatermarkStrategy.<?>forMonotonousTimestamps();

```
有序场景：
1、底层调用的也是乱序的Watermark生成器，只是乱序程度传了一个0ms。
2、Watermark = maxTimestamp – outOfOrdernessMills – 1ms
= maxTimestamp – 0ms – 1ms
=>事件时间 – 1ms
```

##### 2. 乱序流中的WaterMark:

WatermarkStrategy.<?>forBoundedOutOfOrderness(Duration.ofSeconds(10));

```
乱序场景：
1、什么是乱序 => 时间戳大的比时间戳小的先来
2、乱序程度设置多少比较合适？
	a)经验值 => 对自身集群和数据的了解，大概估算。
	b)对数据进行抽样。
	c)肯定不会设置为几小时，一般设为 秒 或者 分钟。
3、Watermark = maxTimestamp – outOfOrdernessMills – 1ms
                 =>当前最大的事件时间 – 乱序程度（等待时间）- 1ms 
```

##### 3. EventTime和WaterMark的使用

Flink内置了两个WaterMark生成器:(本质上是一个)

```
1.Monotonously Increasing Timestamps(时间戳单调增长:其实就是允许的延迟为0)
WatermarkStrategy.forMonotonousTimestamps();

2.Fixed Amount of Lateness(允许固定时间的延迟)
WatermarkStrategy.forBoundedOutOfOrderness(Duration.ofSeconds(10));
```

##### 4.设定WaterMark注意事项:

在乱序或者有序方法前面要加上泛型

<font color='red'><?></font>forMonotonousTimestamps()

<font color='red'><?></font>forBoundedOutOfOrderness()

#### 5.3.3 WaterMark源码:

##### 1.WaterMark初始值是多少？

Long的最小值

```java
// start so that our lowest watermark would be Long.MIN_VALUE.
  this.maxTimestamp = Long.MIN_VALUE + outOfOrdernessMillis + 1;
```

##### 2.为什么读有界数据的时候，所有窗口都能被关闭，当有界数据读完之后WaterMark是多少？

public static final Watermark MAX_WATERMARK = new Watermark(Long.MAX_VALUE);

##### 3.WaterMark默认是怎么生成（周期？间歇）周期的话？周期时间是多少

<font color='red'>默认是周期性生成的</font>，周期时间是200ms
private long autoWatermarkInterval = 200;

通过一下方式可以自定义生成WaterMark的周期间隔
env.getConfig().setAutoWatermarkInterval(1000);

```
如果output.emitWatermark(new Watermark(maxTimestamp - outOfOrdernessMillis - 1));这段代码
在 onEvent这个方法中定义，则是间歇性生成，每来一条数据生成一个WaterMark
在 onPeriodicEmit这个方法中定义，则是周期性生成，默认周期间隔200ms
```

<font color='red'>为什么要有周期性生成和间歇性生成这两种方式?</font>
如果说一秒来10000条数据，使用周期性生成的话，默认只生成5个WaterMark，如果用间歇性的要生成10000个WaterMark。
如果说一天来5条数据，使用周期性生成的话，要生产很多个WaterMark，如果用间歇性的话要生产5个WaterMark。

<font color='red'>为什么会有间歇性生成的WaterMark？</font>

```
public void processElement(final StreamRecord<T> element) throws Exception {
   watermarkGenerator.onEvent(event, newTimestamp, wmOutput);
 }
```

<font color='red'>结论：</font>如果短时间内有大量数据，适合用周期性生成
如果长时间内数据量很小，适合用间歇性生成

<font color='red'>为什么能够每个200ms周期性生成WaterMark</font>，主要用到了<font color='red'>定时器</font>
在TimestampsAndWatermarksOperator这类中
首先在open方法中注册一个基于处理时间的定时器，定时时间为200ms

```
  public void open() throws Exception {
    final long now = getProcessingTimeService().getCurrentProcessingTime();
            getProcessingTimeService().registerTimer(now + watermarkInterval, this);
	}
```

当open方法中的定时器被触发后会调用
onProcessingTime这个方法，这个方法中又注册了一个基于处理时间的定时器，定时时间为200ms

```
 public void onProcessingTime(long timestamp) throws Exception {
        watermarkGenerator.onPeriodicEmit(wmOutput);

        final long now = getProcessingTimeService().getCurrentProcessingTime();
        getProcessingTimeService().registerTimer(now + watermarkInterval, this);
    }
```

##### 4.WaterMark为什么只能变大不能变小->为什么是单调增长的？

maxTimestamp = Math.max(maxTimestamp, eventTimestamp);

#### 5.3.4 多并行度下WaterMark的传递

下图WaterMark传递了两条8秒的数据才关闭窗口, 因为Source发送数据是以轮询的方式发送到map算子, 而在多并行度下WaterMark是以广播的形式传递, 当第一个8秒时,此时WaterMark分别为(0, 5),取最小的一个为0, 所以当前窗口不关闭, 当下一个8秒过来时,WaterMark为(5, 5),最小为5, 关闭[ 0, 5)这个窗口  (当前例子是5秒滚动窗口, 固定延迟3秒)

![image-20211214140552503](https://gitee.com/jerry-chen417/picgo/raw/master/img/202112141405577.png)

![image-20211214192426092](https://gitee.com/jerry-chen417/picgo/raw/master/img/202112141927774.png)

![image-20211214192629757](https://gitee.com/jerry-chen417/picgo/raw/master/img/202112141926821.png)

##### 传递总结:

1.多并行度的条件下,向下游传递WaterMark的时候是以广播的方式传递的
2.总是以最小的那个WaterMark为准! 木桶原理!
3.并且当watermark值没有增长的时候不会向下游传递，注意：生成不变

### 5.4 窗口允许迟到的数据(等待时间)

![image-20211216140912488](https://gitee.com/jerry-chen417/picgo/raw/master/img/202112161409585.png)

当触发了窗口计算后, 会先计算当前的结果, 但是此时并不会关闭窗口.以后每来一条迟到数据, 则触发一次这条数据所在窗口计算(增量计算).

```
那么什么时候会真正的
```

<font color='red'>关闭窗口</font>呢?  <font color='red'>wartermark 超过了窗口结束时间+等待时间</font>
.window(TumblingEventTimeWindows.of(Time.seconds(5)))
.allowedLateness(Time.seconds(3))
注意:
<font color='red'>允许迟到只能运用在event time上</font>

### 5.5 侧输出流(sideOutput)

```java
OutputTag<String> outputTag = new OutputTag<String>("报警信息") {};
```

#### 5.5.1 处理窗口关闭之后的迟到数据

<font color='red'>注意填入参数时, 大括号不要丢, 传入的是一个匿名内部类, 因为直接new会导致类型擦除, 而匿名内部类会带着泛型</font>

.sideOutputLateData( new OutputTag<WaterSensor>("side_1") { } )

##### 允许迟到数据+侧输出流作用：

```
尽量快速提供一个近似准确结果，为了保证时效性，然后加上允许迟到数据+侧输出流得到最终的数据，这样也不用维护大量的窗口，性能也就会好很多。
```

#### 5.5.2 使用侧输出流把一个流拆成多个流

```
split算子可以把一个流分成两个流, 从1.12开始已经被移除了. 官方建议我们用侧输出流来替换split算子的功能.
```

```java
SingleOutputStreamOperator<WaterSensor> result =
  env
    .socketTextStream("hadoop102", 9999)  // 在socket终端只输入毫秒级别的时间戳
    .map(new MapFunction<String, WaterSensor>() {
        @Override
        public WaterSensor map(String value) throws Exception {
            String[] datas = value.split(",");
            return new WaterSensor(datas[0], Long.valueOf(datas[1]), Integer.valueOf(datas[2]));

        }
    })
    .keyBy(ws -> ws.getTs())
    .process(new KeyedProcessFunction<Long, WaterSensor, WaterSensor>() {
        @Override
        public void processElement(WaterSensor value, Context ctx, Collector<WaterSensor> out) throws Exception {
            out.collect(value);
            if (value.getVc() > 5) { //水位大于5的写入到侧输出流
                ctx.output(new OutputTag<WaterSensor>("警告") {}, value);
            }
        }
    });

result.print("主流");
result.getSideOutput(new OutputTag<WaterSensor>("警告"){}).print("警告");
```

### 5.6 定时器

```
基于处理时间或者事件时间处理过一个元素之后, 注册一个定时器, 然后指定的时间执行，定时器只能用于keyedStream中，即keyby之后使用.
```

```
Context和OnTimerContext所持有的TimerService对象拥有以下方法:
currentProcessingTime(): Long 返回当前处理时间

currentWatermark(): Long 返回当前watermark的时间戳

registerProcessingTimeTimer(timestamp: Long): Unit 会注册当前key的processing time的定时器。当processing time到达定时时间时，触发timer。

registerEventTimeTimer(timestamp: Long): Unit 会注册当前key的event time 定时器。当水位线大于等于定时器注册的时间时，触发定时器执行回调函数。

deleteProcessingTimeTimer(timestamp: Long): Unit 删除之前注册处理时间定时器。如果没有这个时间戳的定时器，则不执行。

deleteEventTimeTimer(timestamp: Long): Unit 删除之前注册的事件时间定时器，如果没有此时间戳的定时器，则不执行。
```

#### 5.6.1 基于处理时间的定时器

```java
.process(new KeyedProcessFunction<String, WaterSensor, String>() {
      @Override
      public void processElement(WaterSensor value, Context ctx, Collector<String> out) throws Exception {
          // 处理时间过后5s后触发定时器
          ctx.timerService().registerProcessingTimeTimer(ctx.timerService().currentProcessingTime() + 5000);
          out.collect(value.toString());
      }


      // 定时器被触发之后, 回调这个方法
      // 参数1: 触发器被触发的时间
      @Override
      public void onTimer(long timestamp, OnTimerContext ctx, Collector<String> out) throws Exception {
          System.out.println(timestamp);
          out.collect("我被触发了....");
      }
  })
  .print();
```

#### 5.6.2 基于事件时间的定时器(时间进展依据的是watermark)

```java
 .process(new KeyedProcessFunction<String, WaterSensor, String>() {
      @Override
      public void processElement(WaterSensor value, Context ctx, Collector<String> out) throws Exception {
          System.out.println(ctx.timestamp());
          ctx.timerService().registerEventTimeTimer(ctx.timestamp() + 5000);
          out.collect(value.toString());
      }

      @Override
      public void onTimer(long timestamp, OnTimerContext ctx, Collector<String> out) throws Exception {
          System.out.println("定时器被触发.....");
      }
  })
  .print();
```

```
定时器是事件时间窗口时, WaterMark需要减 1ms , 而定时器是没有减1 ms的, 所以触发6秒的定时器需要传入 大于等于6秒的WaterMark, 即传入时间(10 - 3)
```

![image-20211214151400879](https://gitee.com/jerry-chen417/picgo/raw/master/img/202112141514950.png)

onEventTime这个方法是基于事件时间定时器触发之后调用的
onProcessingTime这个方式是基于处理时间定时器触发之后调用的
processElement每个数据来的时候调用一次

### 5.7 **状态编程**

**Flink中的状态**

•由一个任务维护，并且用来计算某个结果的所有数据，都属于这个任务的状态

•可以认为状态就是一个本地变量，可以被任务的业务逻辑访问

•Flink 会进行状态管理，包括状态一致性、故障处理以及高效存储和访问，以便开发人员可以专注于应用程序的逻辑

•在 Flink 中，状态始终与特定算子相关联

•为了使运行时的 Flink 了解算子的状态，算子需要预先注册其状态

#### 5.7.1 Flink中的状态分类

Flink包括两种基本类型的状态Managed State和Raw State


|                        | ***\*Managed\**** ***\*State\****                     | ***\*Raw\**** ***\*State\*******\*（了解）\**** |
| ------------------------ | ------------------------------------------------------- | ------------------------------------------------- |
| ***\*状态管理方式\**** | Flink Runtime托管, 自动存储, 自动恢复, 自动伸缩       | 用户自己管理                                    |
| ***\*状态数据结构\**** | Flink提供多种常用数据结构, 例如:ListState, MapState等 | 字节数组: byte[]                                |
| ***\*使用场景\****     | 绝大数Flink算子                                       | 所有算子                                        |

#### 5.7.2 Managed State的分类

对Managed State继续细分，它又有两种类型

```
a) Keyed State(键控状态)。
```

```
•算子状态的作用范围限定为算子任务
```

```
b)Operator State(算子状态)。
```

```
•根据输入数据流中定义的键（key）来维护和访问
```


|                          | ***\*Operator\**** ***\*State\****                               | ***\*Keyed\**** ***\*State\****                                    |
| -------------------------- | ------------------------------------------------------------------ | -------------------------------------------------------------------- |
| ***\*适用用算子类型\**** | 可用于所有算子: 常用于source, 例如 FlinkKafkaConsumer            | 只适用于KeyedStream上的算子                                        |
| ***\*状态分配\****       | 一个算子的子任务对应一个状态                                     | 一个Key对应一个State: 一个算子会处理多个Key, 则访问相应的多个State |
| ***\*创建和访问方式\**** | 实现CheckpointedFunction或ListCheckpointed(已经过时)接口         | 重写RichFunction, 通过里面的RuntimeContext访问                     |
| ***\*横向扩展\****       | 并行度改变时有多种重新分配方式可选: 均匀分配和合并后每个得到全量 | 并发改变, State随着Key在实例间迁移                                 |
| ***\*支持的数据结构\**** | ListState和BroadCastState                                        | ValueState, ListState,MapState ReduceState, AggregatingState       |

##### 1. 键控状态的使用

•键控状态是根据输入数据流中定义的键（key）来维护和访问的

•Flink 为每个 key 维护一个状态实例，并将具有相同键的所有数据，都分区到同一个算子任务中，这个任务会维护和处理这个 key 对应的状态

•当任务处理一条数据时，它会自动将状态的访问范围限定为当前数据的 key

![image-20211216110433971](https://gitee.com/jerry-chen417/picgo/raw/master/img/202112161104103.png)

Keyed State很类似于一个分布式的key-value map数据结构，只能用于KeyedStream（keyBy算子处理之后）。

##### 2. 键控状态支持的数据类型

	<font color='red'>ValueState<T> </font>
保存单个值. 每个key有一个状态值.  设置使用 update(T), 获取使用 T value()

```java
// 在匿名类里声明, open方法里初始化
.process(new KeyedProcessFunction<String, WaterSensor, String>() {
              private ValueState<Integer> state;
              @Override
              public void open(Configuration parameters) throws Exception {
                  state = getRuntimeContext().getState(new ValueStateDescriptor<Integer>("state", Integer.class));
              }

```

	<font color='red'>ListState<T> </font>
保存元素列表.
添加元素: add(T)  addAll(List<T>)
获取元素: Iterable<T> get()
覆盖所有元素: update(List<T>)

```java
.process(new KeyedProcessFunction<String, WaterSensor, List<Integer>>() {
              private ListState<Integer> vcState;

              @Override
              public void open(Configuration parameters) throws Exception {
                  vcState = getRuntimeContext().getListState(new ListStateDescriptor<Integer>("vcState", Integer.class));
              }

```

	ReducingState<T>:
存储单个值, 表示把所有元素的聚合结果添加到状态中.  与ListState类似, 但是当使用add(T)的时候ReducingState会使用指定的ReduceFunction进行聚合.
	AggregatingState<IN, OUT>:
存储单个值. 与ReducingState类似, 都是进行聚合. 不同的是, AggregatingState的聚合的结果和元素类型可以不一样.

	<font color='red'>MapState<UK, UV>: </font>
存储键值对列表.
添加键值对:  put(UK, UV) or putAll(Map<UK, UV>)
根据key获取值: get(UK)
获取所有: entries(), keys() and values()
检测是否为空: isEmpty()

<font color='red'>注意:</font>
	所有的类型都有clear(), 清空当前key的状态
	这些状态对象仅用于用户与状态进行交互.
	状态不是必须存储到内存, 也可以存储在磁盘或者任意其他地方
	从状态获取的值与输入元素的key相关

##### 3.	算子状态的使用

```
Operator State可以用在所有算子上，每个算子子任务或者说每个算子实例共享一个状态，流入这个算子子任务的数据可以访问和更新这个状态。
```

注意: <font color='red'>算子子任务之间的状态不能互相访问</font>

```
经常被用在Source或Sink等算子上，用来保存流入数据的偏移量或对输出数据做缓存，以
```

<font color='red'>保证Flink应用的Exactly-Once语义</font>。

Flink为算子状态提供三种基本数据结构：
	列表状态（List state）
将状态表示为一组数据的列表
	联合列表状态（Union list state）
也将状态表示为数据的列表。它与常规列表状态的区别在于，在发生故障时，或者从保存点（savepoint）启动应用程序时如何恢复。
一种是均匀分配(List state)，另外一种是将所有 State 合并为全量 State 再分发给每个实例(Union list state)。
	<font color='red'>广播状态（Broadcast state）</font>
是一种特殊的算子状态. 如果一个算子有多项任务，而它的每项任务状态又都相同，那么这种特殊情况最适合应用广播状态。

### **公司集群三套分类**:

测试集群, 3台

预发布集群, 6-8台

生产集群, 10台

### **5.8 状态后端**

•每传入一条数据，有状态的算子任务都会读取和更新状态

•由于有效的状态访问对于处理数据的低延迟至关重要，因此每个并行任务都会在本地维护其状态，以确保快速的状态访问

•状态的存储、访问以及维护，由一个可插入的组件决定，这个组件就叫做**状态后端**（state backend）

•状态后端主要负责两件事：
本地的状态管理
将检查点（checkpoint）状态写入远程存储

#### 5.8.1 状态后端的分类

##### MemoryStateBackend

内存级别的状态后端,
存储方式:本地状态存储在TaskManager的内存中, checkpoint 存储在JobManager的内存中。
特点:快速, 低延迟, 但不稳定
使用场景: 1. 本地测试 2. 几乎无状态的作业(ETL) 3. JobManager不容易挂, 或者挂了影响不大. 4. 不推荐在生产环境下使用

##### FsStateBackend

存储方式: 本地状态在TaskManager内存, <font color='red'>Checkpoint存储在文件系统中</font>
特点: 拥有内存级别的本地访问速度, 和更好的容错保证
使用场景: 1. 常规使用状态的作业. 例如分钟级别窗口聚合, join等 2. 需要开启HA的作业 3. 可以应用在生产环境中

##### RocksDBStateBackend

将所有的状态序列化之后, 存入本地的RocksDB数据库中.(一种NoSql数据库, KV形式存储)

**存储方式:** 1. 本地状态存储在TaskManager的RocksDB数据库中(实际是内存+磁盘) 2. Checkpoint在外部文件系统中.

**使用场景:** 1. 超大状态的作业, 例如天级的窗口聚合 2. 需要开启HA的作业 3. 对读写状态性能要求不高的作业 4. 可以使用在生产环境

#### 5.8.2  **配置状态后端**

##### 	**1. 全局配置状态后端(配置文件)**

在flink-conf.yaml文件中设置默认的全局后端

![image-20211215203506973](https://gitee.com/jerry-chen417/picgo/raw/master/img/202112152035035.png)

###### Memory:

```
state.backend: hashmap

# Optional, Flink will automatically default to JobManagerCheckpointStorage
# when no checkpoint directory is specified.

state.checkpoint-storage: jobmanager

```

###### Filesystem:

```
state.backend: hashmap
state.checkpoints.dir: file:///checkpoint-dir/

# Optional, Flink will automatically default to FileSystemCheckpointStorage
# when a checkpoint directory is specified.

state.checkpoint-storage: filesystem

```

###### RockDB:

```
state.backend: rocksdb
state.checkpoints.dir: file:///checkpoint-dir/

# Optional, Flink will automatically default to FileSystemCheckpointStorage
# when a checkpoint directory is specified.

state.checkpoint-storage: filesystem

```

##### 2. 在代码中配置状态后端

可以在代码中单独为这个Job设置状态后端.

###### Memory：

```
//1.12老版设置方法
env.setStateBackend(new MemoryStateBackend());

//1.13新版设置方法
env.setStateBackend(new HashMapStateBackend());
//在新版本需要额外声明一下做Checkpoint时的存储位置
env.getCheckpointConfig().setCheckpointStorage(new JobManagerCheckpointStorage());
```

###### Fs：

```
//老版本写法
env.setStateBackend(new FsStateBackend("hdfs://hadoop102:8020/....."));

//新版本写法
env.setStateBackend(new HashMapStateBackend());
env.getCheckpointConfig().setCheckpointStorage("hdfs://hadoop102:8020/.....");
```

###### RocksDB：

RocksDBBackend, 需要先引入依赖:

```
<dependency>
    <groupId>org.apache.flink</groupId>
    <artifactId>flink-statebackend-rocksdb_2.12</artifactId>
    <version>1.13.0</version>
    <scope>provided</scope>
</dependency>

```

```
//老版本写法
env.setStateBackend(new RocksDBStateBackend("hdfs://hadoop102:8020/rocksDb/....."));

//新版本写法
env.setStateBackend(new EmbeddedRocksDBStateBackend());
env.getCheckpointConfig().setCheckpointStorage("hdfs://hadoop102:8020/rocksDb/.....");
```

### **5.9 Flink容错机制**

- 一致性检查点（checkpoint）
- 从检查点恢复状态
- Flink 检查点算法
- 保存点（save points）

#### 5.9.1状态的一致性

```
1.有状态的流处理，内部每个算子任务都可以有自己的状态
2.对于流处理器内部来说，所谓的状态一致性，其实就是我们所说的计算结果要保证准确。
3.一条数据不应该丢失，也不应该重复计算
4.在遇到故障时可以恢复状态，恢复以后的重新计算，结果应该也是完全正确的
```

##### 1. 一致性级别

###### Ø **at-most-once(最多变一次):**

这其实是没有正确性保障的委婉说法——故障发生之后，计数结果可能丢失。

###### Ø **at-least-once(至少一次):**

这表示计数结果可能大于正确值，但绝不会小于正确值。也就是说，计数程序在发生故障后**可能多算**，但是**绝不会少算。**

###### Ø **exactly-once(精准一次性):**

这指的是系统保证在发生故障后得到的计数结果与正确值一致.既不多算也不少算。

##### 2. 端到端的状态一致性

```
端到端的一致性保证，意味着结果的正确性贯穿了整个流处理应用的始终；每一个组件都保证了它自己的一致性，
```

<font color='red'>整个端到端的一致性级别取决于所有组件中一致性最弱的组件。</font>

具体划分如下:

###### Ø source端

需要外部源可重设数据的读取位置.

目前我们使用的Kafka Source具有这种特性: 读取数据的时候可以指定offset

###### Ø flink内部

依赖checkpoint机制

###### Ø sink端

需要保证从故障恢复时，数据不会重复写入外部系统. 有2种实现形式:

a)  幂等（Idempotent）写入

```
所谓幂等操作，是说一个操作，可以重复执行很多次，但只导致一次结果更改，也就是说，后面再重复执行就不起作用了。
```

###### b)  <font color='red'>事务性（Transactional）写入</font>

**•事务（Transaction）**

```
Ø应用程序中一系列严密的操作，所有操作必须成功完成，否则在每个操作中所作的所有更改都会被撤消
```

```
Ø具有原子性：一个事务中的一系列的操作要么全部成功，要么一个都不做
```

**•实现思想：**构建的事务对应着 checkpoint，等到 checkpoint 真正完成的时候，才把所有对应的结果写入 sink 系统中

**•实现方式**

```
Ø预写日志
```

```
		把结果数据先当成状态保存，然后在收到 checkpoint 完成的通知时，一次性写入 sink 系统

		简单易于实现，由于数据提前在状态后端中做了缓存，所以无论什么 sink 系统，都能用这种方式一批搞定，但是这样就像批处理一样。

		DataStream API 提供了一个模板类：GenericWriteAheadSink，来实现这种事务性 sink

```

```
Ø
```

<font color='red'>两阶段提交</font>

##### 3.两阶段提交

- 对于每个 checkpoint，sink 任务会启动一个事务，并将接下来所有接收的数据添加到事务里
- 然后将这些数据写入外部 sink 系统，但不提交它们 —— 这时只是“预提交”
- 当它收到 checkpoint 完成的通知时，它才正式提交事务，实现结果的真正写入
- 这种方式真正实现了 exactly-once，它需要一个提供事务支持的外部 sink 系统。Flink 提供了 TwoPhaseCommitSinkFunction 抽象类。

###### 3.1  2PC 对外部 sink 系统的要求

- 外部 sink 系统必须提供事务支持，或者 sink 任务必须能够模拟外部系统上的事务
- 在 checkpoint 的间隔期间里，必须能够开启一个事务并接受数据写入
- 在收到 checkpoint 完成的通知之前，事务必须是“等待提交”的状态。在故障恢复的情况下，这可能需要一些时间。如果这个时候sink系统关闭事务（例如超时了），那么未提交的数据就会丢失
- sink 任务必须能够在进程失败后恢复事务
- 提交事务必须是幂等操作

###### 3.2 Flink+Kafka 端到端状态一致性的保证

- 内部 —— 利用 checkpoint 机制，把状态存盘，发生故障的时候可以恢复，保证内部的状态一致性
- source —— kafka consumer 作为 source，可以将偏移量保存下来，如果后续任务出现了故障，恢复的时候可以由连接器重置偏移量，重新消费数据，保证一致性
- sink —— kafka producer 作为sink，采用两阶段提交 sink，需要实现一个 TwoPhaseCommitSinkFunction

###### 3.3 Exactly-once 两阶段提交步骤

![image-20211216114343544](https://gitee.com/jerry-chen417/picgo/raw/master/img/202112161143613.png)

- jobmanager 触发 checkpoint 操作，barrier 从 source 开始向下传递，遇到 barrier 的算子将状态存入状态后端，并通知 jobmanager
- 第一条数据来了之后，开启一个 kafka 的事务（transaction），正常写入 kafka 分区日志但标记为未提交，这就是“预提交”

![image-20211216114624240](https://gitee.com/jerry-chen417/picgo/raw/master/img/202112161146311.png)

- sink 连接器收到 barrier，保存当前状态，存入 checkpoint，通知 jobmanager，并开启下一阶段的事务，用于提交下个检查点的数据
- jobmanager 收到所有任务的通知，发出确认信息，表示 checkpoint 完成
- sink 任务收到 jobmanager 的确认信息，正式提交这段时间的数据
- 外部kafka关闭事务，提交的数据可以正常消费了。

![image-20211216114725903](https://gitee.com/jerry-chen417/picgo/raw/master/img/202112161147973.png)

#### 5.9.2 Checkpoint原理

- Flink 故障恢复机制的核心，就是应用状态的一致性检查点
- 有状态流应用的一致检查点，其实就是所有任务的状态，在某个时间点的一份拷贝（一份快照）；这个时间点，应该是所有任务都恰好处理完一个相同的输入数据的时候

##### 1. Flink检查点算法:

1. 简单算法--暂停应用, 然后开始做检查点, 再重新恢复应用
2. Flink的改进Checkpoint算法. Flink的checkpoint机制原理来自"Chandy-Lamport algorithm"算法(分布式快照算法)的一种变体: 异步 barrier 快照（asynchronous barrier snapshotting）

##### 2. 检查点分界线（Checkpoint Barrier）

- Flink 的检查点算法用到了一种称为分界线（<font color='red'>barrier</font>）的特殊数据形式，用来把一条流上数据按照不同的检查点分开
- <font color='red'>分界线之前</font>到来的数据导致的状态更改，都会被包含在<font color='red'>当前分界线所属</font>的检查点中；而基于<font color='red'>分界线之后</font>的数据导致的所有更改，就会被包含在<font color='red'>之后的检查点中</font>

![image-20211215151033546](https://gitee.com/jerry-chen417/picgo/raw/master/img/202112151512757.png)

#### 5.9.3 CheckPoint提交过程:

Ø 第一步: Checkpoint Coordinator 向所有 source 节点 trigger Checkpoint. 然后Source Task会在数据流中安插CheckPoint barrier

Ø 第二步: source 节点向下游广播 barrier，这个 barrier 就是实现 Chandy-Lamport 分布式快照算法的核心，下游的 task 只有收到所有 input 的 barrier 才会执行相应的 Checkpoint

Ø第三步: 当 task 完成 state 备份后，会将备份数据的地址（state handle）通知给 Checkpoint coordinator。

Ø第四步: 下游的 sink 节点收集齐上游两个 input 的 barrier 之后，会执行本地快照

Ø第五步: 同样的，sink 节点在完成自己的 Checkpoint 之后，会将 state handle 返回通知 Coordinator。

Ø 第六步: 最后，当 Checkpoint coordinator 收集齐所有 task 的 state handle，就认为这一次的 Checkpoint 全局完成了，向持久化存储中再备份一个 Checkpoint meta 文件。

##### CheckPoint默认是Barrier对齐

设置不对齐Checkpoint

```
env.getCheckpointConfig().enableUnalignedCheckpoints();
```

单个Source:

![image-20211215152725156](https://gitee.com/jerry-chen417/picgo/raw/master/img/202112151527251.png)

多个Source:

##### 严格一次语义: barrier对齐

在多并行度下, 如果要实现严格一次, 则要执行**<font color='red'>barrier对齐</font>**。

Barrier没到齐的情况下会把数据缓存, 有OOM的可能, 使用背压机制解决,但是会降低效率

![image-20211216144154082](https://gitee.com/jerry-chen417/picgo/raw/master/img/202112161441180.png)

1. 当算子收到barrier n时, 它就不再处理barrier n之后的数据, 但是会接收流数据到缓存区暂存起来
2. 当另外一条流的barrier n到达时会对之前处理的数据做快照, 然后把barrier n往下游发送,然后再处理缓存中的数据
3. sink端会把接收到的数据先预提交, 一但接收到barrier n之后, 会做一个快照, 返回给 Checkpoint coordinator快照完成讯息, 这样一次完整的checkPoint就完成了,然后再把数据提交到下游Kafka(二次提交)

##### 至少一次语义: barrier不对齐

![image-20211216165859672](https://gitee.com/jerry-chen417/picgo/raw/master/img/202112161658759.png)

当数字流CheckPoint barrier n先到, 这时Operator不会等另外一条流的barrier n, 会直接做快照, 继续处理数字流barrier n+1的数据,恢复数据时就会造成n+1那部分数据重复

#### 5.9.4 Savepoint原理

1. Flink 还提供了可以自定义的镜像保存功能，就是保存点（savepoints）
2. 原则上，创建保存点使用的算法与检查点完全相同，因此保存点可以认为就是具有一些额外元数据的检查点
3. Flink不会自动创建保存点，因此用户（或外部调度程序）必须明确地触发创建操作
4. 保存点是一个强大的功能。除了故障恢复外，保存点可以用于：有计划的手动备份，更新应用程序，版本迁移，暂停和重启应用，等等

##### 从SavePoint和CK恢复任务步骤：

//启动任务

```
bin/flink run -d -m hadoop102:8081 -c com.atguigu.day06.Flink10_SavePoint ./flink-0108-1.0-SNAPSHOT.jar
```

###### 1. Standalone模式提交savepoint

```
bin/flink savepoint -m hadoop102:8081 JobId hdfs://hadoop102:8020/flink/save
```

###### 2.Yarn模式提交savepoint

```
bin/flink savepoint :jobId [:targetDirectory] -yid :yarnAppId

bin/flink savepoint jobId hdfs://hadoop102:8020/flink/save -yid yarnAppId
```

//关闭任务并从保存点恢复任务

```
bin/flink run -s hdfs://hadoop102:8020/flink/save/savepoint-(jobId前六位)... -m hadoop102:8081 -c com.atguigu.WordCount xxx.jar
```

![image-20211222200638198](https://gitee.com/jerry-chen417/picgo/raw/master/img/202112222006391.png)

//从CK位置恢复数据，在代码中开启cancel的时候不会删除checkpoint信息这样就可以根据checkpoint来回复数据了

```
env.getCheckpointConfig()
.enableExternalizedCheckpoints(
	CheckpointConfig
	  .ExternalizedCheckpointCleanup
	  .RETAIN_ON_CANCELLATION);
```

-s指定恢复的地址

```
bin/flink run -s hdfs://hadoop102:8020/flink/ck/Jobid/chk-960 -m hadoop102:8081 -c com.atguigu.WordCount  xxx.jar
```

### 5.10  Flink+Kafka 实现端到端严格一次

Flink + Kafka的数据管道系统（Kafka进、Kafka出）实现exactly-once:

```
Ø 内部 —— 利用checkpoint机制，把状态存盘，发生故障的时候可以恢复，保证部的状态一致性
```

```
Ø source —— kafka consumer作为source，可以将偏移量保存下来，如果后续任务出现了故障，恢复的时候可以由连接器重置偏移量，重新消费数据，保证一致性
```

```
Ø sink —— kafka producer作为sink，采用两阶段提交 sink，需要实现一个 TwoPhaseCommitSinkFunction
```

![image-20211216150841402](https://gitee.com/jerry-chen417/picgo/raw/master/img/202112161508498.png)

#### 具体的两阶段提交步骤总结如下：

1) jobmanager 触发 checkpoint 操作，barrier 从 source 开始向下传递，遇到 barrier 的算子将状态存入状态后端，并通知 jobmanagerr
2) 第一条数据来了之后，开启一个 kafka 的事务（transaction），正常写入 kafka 分区日志但标记为未提交，这就是“预提交”
3) sink 连接器收到 barrier，保存当前状态，存入 checkpoint，通知 jobmanager，并开启下一阶段的事务，用于提交下个检查点的数据
4) jobmanager 收到所有任务的通知，发出确认信息，表示 checkpoint 完成
5) sink 任务收到 jobmanager 的确认信息，正式提交这段时间的数据
6) 外部kafka关闭事务，提交的数据可以正常消费了

## 六. FlinkCEP

```
FlinkCEP(Complex event processing for Flink) 是在Flink实现的
```

**复杂事件处理**库. 它可以让你在无界流中检测出特定的数据，有机会掌握数据中重要的那部分。

\1.    **目标：**从有序的简单事件流中发现一些高阶特征

\2.    **输入：**一个或多个由简单事件构成的事件流

\3.    **处理：**识别简单事件之间的内在联系，多个符合一定规则的简单事件构成复杂事件

\4.    **输出：**满足规则的复杂事件

### 6.1 CEP使用依赖

```
<dependency>
 	<groupId>org.apache.flink</groupId>
    <artifactId>flink-cep_2.11</artifactId>
    <version>1.13.3</version>
</dependency>

```

### 6.2 CEP定义步骤:

1. 定义模式

   ```
   Pattern<WaterSensor, WaterSensor> pattern = Pattern
           .<WaterSensor>begin("start")
           .where(new SimpleCondition<WaterSensor>() {
               @Override
               public boolean filter(WaterSensor value) throws Exception {
                   return "sensor_1".equals(value.getId());
               }
           });
   ```
2. 在流上应用模式

   ```
   PatternStream<WaterSensor> waterSensorPS = CEP.pattern(waterSensorStream, pattern);
   ```
3. 获取匹配的结果

   ```
   waterSensorPS
               .select(new PatternSelectFunction<WaterSensor, String>() {
                   @Override
                   public String select(Map<String, List<WaterSensor>> pattern) throws Exception {
                       return pattern.toString();
                   }
               })
               .print();

   ```

### 6.3   模式API

Ø 模式:

比如找拥有相同属性事件序列的模式(前面案例中的拥有相同的id), 我们一般把简单模式称之为模式
**注意:**

\1. 每个模式必须有一个独一无二的名字，你可以在后面使用它来识别匹配到的事件。(比如前面的start模式)

\2. 模式的名字不能包含字符`":"`

Ø 模式序列

```
每个复杂的模式序列包括多个简单的模式，也叫模式序列. 你可以把模式序列看作是这样的模式构成的图， 这些模式基于用户指定的条件从一个转换到另外一个
```
Ø 匹配

```
输入事件的一个序列，这些事件通过一系列有效的模式转换，能够访问到复杂模式图中的所有模式。
```
#### 6.3.1单个模式

1.单例模式:

```
单例模式只接受
```
**一个事件.** 默认情况模式都是单例模式.

2.循环模式

循环模式可以接受**多个事件.** 单例模式配合上<font color='red'>量词</font>就是循环模式.(非常类似正则表达式)

```
Ø 固定次数     		pattern.
```
<font color='red'>times(2)</font>;

```
Ø 范围内的次数     pattern.
```
<font color='red'>times(2, 4)</font>;

```
Ø 一次或多次		 pattern
```
<font color='red'>.oneOrMore()</font>;

```
Ø 多次及多次以上 pattern
```
<font color='red'>.timesOrMore(2)</font>;

3.条件

```
对每个模式你可以指定一个条件来决定一个进来的事件是否被接受进入这个模式，例如前面用到的where就是一种条件
```
```
Ø 迭代条件
```
<font color='red'>IterativeCondition</font>

```
.where(new IterativeCondition<WaterSensor>() {
        @Override
        public boolean filter(WaterSensor value, Context<WaterSensor> ctx) throws Exception {
            return "sensor_1".equals(value.getId());
        }
    });

```
```
Ø 简单条件
```
<font color='red'>SimpleCondition</font>  其实就是迭代条件的低配版

```
.where(new SimpleCondition<WaterSensor>() {
        @Override
        public boolean filter(WaterSensor value) throws Exception {
            System.out.println(value);
            return "sensor_1".equals(value.getId());
        }
    });
```
```
Ø 组合条件
```
```
把多个条件结合起来使用. 依次调用where()来组合条件。 最终的结果是每个单一条件的结果的逻辑AND。如果想使用OR来组合条件，你可以像下面这样使用or()方法。
```
```
.where(new SimpleCondition<WaterSensor>() {
        @Override
        public boolean filter(WaterSensor value) throws Exception {
            return value.getVc() > 30;
        }
    })
    .or(new SimpleCondition<WaterSensor>() {
        @Override
        public boolean filter(WaterSensor value) throws Exception {
            return value.getTs() > 3000;
        }
    });
```
```
Ø 停止条件
```
<font color='red'>until</font>

满足了给定的条件的事件出现后，就不会再有事件被接受进入模式了。

```
.<WaterSensor>begin("start")
    .where(new IterativeCondition<WaterSensor>() {
        @Override
        public boolean filter(WaterSensor value, Context<WaterSensor> ctx) throws Exception {
            return "sensor_1".equals(value.getId());
        }
    })
    .timesOrMore(2)
    .until(new SimpleCondition<WaterSensor>() {
        @Override
        public boolean filter(WaterSensor value) throws Exception {
            return value.getVc() >= 40;
        }
    });
```
#### 6.3.2 组合模式(模式序列)

```
把多个单个模式组合在一起就是组合模式. 组合模式由一个初始化模式(.begin(...))开头
```
- 严格连续   <font color='red'>next</font>

  期望所有匹配的事件严格的一个接一个出现，中间没有任何不匹配的事件

```
.<WaterSensor>begin("start")
    .where(new SimpleCondition<WaterSensor>() {
        @Override
        public boolean filter(WaterSensor value) throws Exception {
            return "sensor_1".equals(value.getId());
        }
    })
    .next("end")
    .where(new SimpleCondition<WaterSensor>() {
        @Override
        public boolean filter(WaterSensor value) throws Exception {
            return "sensor_2".equals(value.getId());
        }
    });
```
- 松散连续   **<font color='red'>followedBy</font>**

忽略匹配的事件之间的不匹配的事件。

```
.<WaterSensor>begin("start")
    .where(new SimpleCondition<WaterSensor>() {
        @Override
        public boolean filter(WaterSensor value) throws Exception {
            return "sensor_1".equals(value.getId());
        }
    })
    .followedBy("end")
    .where(new SimpleCondition<WaterSensor>() {
        @Override
        public boolean filter(WaterSensor value) throws Exception {
            return "sensor_2".equals(value.getId());
        }
    });
```
- 非确定的松散连续    **<font color='red'>followedByAny</font>**

更进一步的松散连续，允许忽略掉一些匹配事件的附加匹配

当且仅当数据为a,c,b,b时，对于followedBy模式而言命中的为{a,b}，对于followedByAny而言会有两次命中{a,b},{a,b}

```
.<WaterSensor>begin("start")
    .where(new SimpleCondition<WaterSensor>() {
        @Override
        public boolean filter(WaterSensor value) throws Exception {
            return "sensor_1".equals(value.getId());
        }
    })
    .followedByAny("end")
    .where(new SimpleCondition<WaterSensor>() {
        @Override
        public boolean filter(WaterSensor value) throws Exception {
            return "sensor_2".equals(value.getId());
        }
    });
```
#### 6.3.3 模式知识补充

1.循环模式的连续性

```
Ø 严格连续
```
<font color='red'>.consecutive()</font>

```
.<WaterSensor>begin("start")
    .where(new SimpleCondition<WaterSensor>() {
        @Override
        public boolean filter(WaterSensor value) throws Exception {
            return "sensor_1".equals(value.getId());
        }
    })
    .times(2)
    .consecutive();
```
```
Ø 松散连续    默认是松散连续
```
```
Ø 非确定的松散连续
```
<font color='red'>.allowCombinations()</font>;

2.循环模式的贪婪性      <font color='red'>greedy</font>

```
在组合模式情况下, 对次数的处理尽快能获取最多个的那个次数, 就是
```
**贪婪**!当一个事件***同时满足两个模式\***的时候起作用.

```
Pattern<WaterSensor, WaterSensor> pattern = Pattern
    .<WaterSensor>begin("start")
    .where(new SimpleCondition<WaterSensor>() {
        @Override
        public boolean filter(WaterSensor value) throws Exception {
            return "sensor_1".equals(value.getId());
        }
    }).times(2, 3).greedy()
    .next("end")
    .where(new SimpleCondition<WaterSensor>() {
        @Override
        public boolean filter(WaterSensor value) throws Exception {
            return value.getVc() == 30;
        }
    });
```
数据:

sensor_1,1,10
sensor_1,2,20
**sensor_1,3,30**
sensor_2,4,30
sensor_1,4,40
sensor_2,5,50
sensor_2,6,60

结果:

```
{start=[WaterSensor(id=sensor_1, ts=1, vc=10), WaterSensor(id=sensor_1, ts=2, vc=20), WaterSensor(id=sensor_1, ts=3, vc=30)], end=[WaterSensor(id=sensor_2, ts=4, vc=30)]}

{start=[WaterSensor(id=sensor_1, ts=2, vc=20), WaterSensor(id=sensor_1, ts=3, vc=30)], end=[WaterSensor(id=sensor_2, ts=4, vc=30)]}
```
分析:
<font color='red'>sensor_1,3,30  </font>在匹配的的时候, 既能匹配第一个模式也可以匹配的第二个模式, 由于第一个模式使用量词则使用greedy的时候会优先匹配第一个模式, 因为<font color='red'>要尽可能多的次数</font>
注意:

1. 一般<font color='red'>贪婪比非贪婪的结果要少</font>!
2. 模式组不能设置为greedy

3.模式可选性

可以使用pattern.optional()方法让所有的模式变成可选的，不管是否是循环模式

```
Pattern
    .<WaterSensor>begin("start")
    .where(new SimpleCondition<WaterSensor>() {
        @Override
        public boolean filter(WaterSensor value) throws Exception {
            return "sensor_1".equals(value.getId());
        }
    }).times(2).optional()  // 0次或2次
```
start模式可能会没有!

#### 6.3.4模式组

```
在前面的代码中次数只能用在某个模式上, 比如: .begin(...).where(...).next(...).where(...).times(2) 这里的次数只会用在next这个模式上, 而不会用在begin模式上.
```
如果需要用在多个模式上,可以使用**模式组(相当于SQL子查询)**!

```
Pattern
    .begin(Pattern
               .<WaterSensor>begin("start")
               .where(new SimpleCondition<WaterSensor>() {
                   @Override
                   public boolean filter(WaterSensor value) throws Exception {
                       return "sensor_1".equals(value.getId());
                   }
               })
               .next("next")
               .where(new SimpleCondition<WaterSensor>() {
                   @Override
                   public boolean filter(WaterSensor value) throws Exception {
                       return "sensor_2".equals(value.getId());
                   }
               }))
    .times(2);
```
#### 6.3.5 超时数据

当一个模式上通过`within`加上窗口长度后，部分匹配的事件序列就可能因为超过窗口长度而被丢弃。

```
Pattern
    .<WaterSensor>begin("start")
    .where(new SimpleCondition<WaterSensor>() {
        @Override
        public boolean filter(WaterSensor value) throws Exception {
            return "sensor_1".equals(value.getId());
        }
    })
    .next("end")
    .where(new SimpleCondition<WaterSensor>() {
        @Override
        public boolean filter(WaterSensor value) throws Exception {
            return "sensor_2".equals(value.getId());
        }
    })
    .within(Time.seconds(2));
```
6.3.6 匹配后跳过策略

```
AfterMatchSkipStrategy skipStrategy = ...
Pattern.begin("patternName", skipStrategy);

```
为了控制一个事件会分配到多少个匹配上，你需要指定跳过策略AfterMatchSkipStrategy

·    ***NO_SKIP\***: 每个成功的匹配都会被输出。（人话：不跳过）

·    ***SKIP_TO_NEXT\***: 丢弃以相同事件开始的所有部分匹配。（人话:事件相同开头只保留一个）

·    ***SKIP_PAST_LAST_EVENT\***: 丢弃起始在这个匹配的开始和结束之间的所有部分匹配。（人话：丢弃匹配开始后每个已经做过匹配的事件的匹配）

·    ***SKIP_TO_FIRST\***: 丢弃起始在这个匹配的开始和第一个出现的名称为*PatternName*事件之间的所有部分匹配。（人话：以第一个事件匹配为准，丢弃匹配开始后包含这个事件之前的匹配）

***SKIP_TO_LAST\***: 丢弃起始在这个匹配的开始和最后一个出现的名称为*PatternName*事件之间的所有部分匹配。（人话：以最后一个事件匹配为准，丢弃匹配开始后包含这个事件之前的匹配）

![image-20211217205217863](https://gitee.com/jerry-chen417/picgo/raw/master/img/202112172052009.png)

![image-20211217205244397](https://gitee.com/jerry-chen417/picgo/raw/master/img/202112172052477.png)

# FlinkSQL&TableAPI

![image-20211223102617085](https://gitee.com/jerry-chen417/picgo/raw/master/img/202112231026656.png)

1. 将流转换为动态表。
2. 在动态表上计算一个连续查询，生成一个新的动态表。
3. 生成的动态表被转换回流。

## 一. Flink Table API

### 1.1 导入依赖

```
//老版官方提供的依赖没有融合blink的
<dependency>
    <groupId>org.apache.flink</groupId>
    <artifactId>flink-table-planner_${scala.binary.version}</artifactId>
    <version>${flink.version}</version>
</dependency>

//blink二次开发之后的依赖
<dependency>
    <groupId>org.apache.flink</groupId>
    <artifactId>flink-table-planner-blink_${scala.binary.version}</artifactId>
    <version>${flink.version}</version>
</dependency>
<dependency>
    <groupId>org.apache.flink</groupId>
    <artifactId>flink-csv</artifactId>
    <version>${flink.version}</version>
</dependency>
<dependency>
    <groupId>org.apache.flink</groupId>
    <artifactId>flink-json</artifactId>
    <version>${flink.version}</version>
</dependency>
```
依赖冲突:

![image-20211220144224924](https://gitee.com/jerry-chen417/picgo/raw/master/img/202112201442094.png)

### 1.2 基本使用:表与DataStream的混合使用

```
public class Flink01_TableApi_BasicUse {
    public static void main(String[] args) {
        StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment();
        env.setParallelism(1);
        DataStreamSource<WaterSensor> waterSensorStream =
            env.fromElements(new WaterSensor("sensor_1", 1000L, 10),
                             new WaterSensor("sensor_1", 2000L, 20),
                             new WaterSensor("sensor_2", 3000L, 30),
                             new WaterSensor("sensor_1", 4000L, 40),
                             new WaterSensor("sensor_1", 5000L, 50),
                             new WaterSensor("sensor_2", 6000L, 60));

        // 1. 创建表的执行环境
        StreamTableEnvironment tableEnv = StreamTableEnvironment.create(env);
        // 2. 创建表: 将流转换成动态表. 表的字段名从pojo的属性名自动抽取
        Table table = tableEnv.fromDataStream(waterSensorStream);
        // 3. 对动态表进行查询
        Table resultTable = table
            .where($("id").isEqual("sensor_1"))
            .select($("id"), $("ts"), $("vc"));
        // 4. 把动态表转换成流
        DataStream<Row> resultStream = tableEnv.toAppendStream(resultTable, Row.class);
        resultStream.print();
        try {
            env.execute();
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
```
1.3 基本使用:聚合操作

```
// 3. 对动态表进行查询
Table resultTable = table
    .where($("vc").isGreaterOrEqual(20))
    .groupBy($("id"))
    .aggregate($("vc").sum().as("vc_sum"))
    .select($("id"), $("vc_sum"));

//或者
//Table resultTbale = table
//        .where($("vc").isGreaterOrEqual(20))
//       .groupBy($("id"))
//        .select($("id"),$("vc").sum().as("vcSum"));

// 4. 把动态表转换成流 如果涉及到数据的更新和改变, 要用到撤回流. 多个了一个boolean标记
DataStream<Tuple2<Boolean, Row>> resultStream = tableEnv.toRetractStream(resultTable, Row.class);
```
### 1.4  表到流的转换

#### 1.4.1 Append-only 流（只追加流）

```
仅通过 INSERT 操作修改的动态表可以通过输出插入的行转换为流。
```
#### 1.4.2 Retract 流（撤回流）

```
retract 流包含两种类型的 message：
```
<font color='red'>add messages</font>和 <font color='red'>retract messages</font>。通过将<font color='red'>INSERT </font>操作编码为 <font color='red'>add message</font>、将<font color='red'> DELETE</font> 操作编码为<font color='red'> retract message</font>、将 UPDATE 操作编码为更新(先前)行的 retract message 和更新(新)行的 add message，将动态表转换为 retract 流。下图显示了将动态表转换为 retract 流的过程。

![image-20211223105855202](https://gitee.com/jerry-chen417/picgo/raw/master/img/202112231101587.png)

<font color='red'>更新过程：</font>
<font color='red'>1） 旧的结果，标记为 撤回，用 false 表示</font>
<font color='red'>2） 新的结果，标记为 插入，用 true 表示</font>

#### 1.4.3 Upsert 流

```
upsert 流包含两种类型的 message：
```
<font color='red'> upsert messages</font> 和<font color='red'>delete messages</font>。转换为 upsert 流的动态表需要(可能是组合的)唯一键。通过将 <font color='red'>INSERT 和 UPDATE 操作编码为 upsert message</font>，将<font color='red'> DELETE 操作编码为 delete message</font> ，将具有唯一键的动态表转换为流。消费流的算子需要知道唯一键的属性，以便正确地应用 message。<font color='red'>与 retract 流的主要区别在于 UPDATE 操作是用单个 message 编码的</font>，因此效率更高。下图显示了将动态表转换为 upsert 流的过程。

![image-20211223110424068](https://gitee.com/jerry-chen417/picgo/raw/master/img/202112231104164.png)

<font color='red'>注意:</font>

```

```
<font color='red'>在将动态表转换为 DataStream 时，只支持 append 流和 retract 流。</font>

### 1.5 通过Connector声明读入数据

#### 1.5.1 File source

```
// 2. 创建表
// 2.1 表的元数据信息
Schema schema = new Schema()
    .field("id", DataTypes.STRING())
    .field("ts", DataTypes.BIGINT())
    .field("vc", DataTypes.INT());
// 2.2 连接文件, 并创建一个临时表, 其实就是一个动态表
tableEnv.connect(new FileSystem().path("input/sensor.txt"))
    .withFormat(new Csv().fieldDelimiter(',').lineDelimiter("\n"))
    .withSchema(schema)
    .createTemporaryTable("sensor");
// 3. 做成表对象, 然后对动态表进行查询
Table sensorTable = tableEnv.from("sensor");
Table resultTable = sensorTable
    .groupBy($("id"))
    .select($("id"), $("id").count().as("cnt"));
// 4. 把动态表转换成流. 如果涉及到数据的更新, 要用到撤回流. 多个了一个boolean标记
DataStream<Tuple2<Boolean, Row>> resultStream = tableEnv.toRetractStream(resultTable, Row.class);
resultStream.print();

```
通过 connect直接 将 外部系统 抽象成 动态表,作为数据源

1. 调用 connect方法，传入一个外部系统的描述器，还有一些参数
2. 调用 withFormat方法，指定数据的存储格式： 列分隔符、行分隔符，等等
3. 调用 withSchema方法，指定 表的结构信息：  列名、列的类型
4. 调用 createTemporaryTable方法，创建一张临时表，并且指定表名

#### 1.5.2  Kafka Source

```java
// 2. 创建表
// 2.1 表的元数据信息
Schema schema = new Schema()
    .field("id", DataTypes.STRING())
    .field("ts", DataTypes.BIGINT())
    .field("vc", DataTypes.INT());
// 2.2 连接文件, 并创建一个临时表, 其实就是一个动态表
tableEnv
    .connect(new Kafka()
                 .version("universal") //kafka通用版本
                 .topic("sensor")
                 .startFromLatest()
                 .property("group.id", "bigdata")
                 .property("bootstrap.servers", "hadoop102:9092,hadoop103:9092,hadoop104:9092"))
    .withFormat(new Json())
    .withSchema(schema)
    .createTemporaryTable("sensor");
// 3. 对动态表进行查询
Table sensorTable = tableEnv.from("sensor");
Table resultTable = sensorTable
    .groupBy($("id"))
    .select($("id"), $("id").count().as("cnt"));
// 4. 把动态表转换成流. 如果涉及到数据的更新, 要用到撤回流. 多个了一个boolean标记
DataStream<Tuple2<Boolean, Row>> resultStream = tableEnv.toRetractStream(resultTable, Row.class);
resultStream.print();
```
启动kafka生产者生产数据

kafka-console-producer.sh --broker-list hadoop102:9092 --topic sensor

### 1.6 通过Connector声明写出数据

#### Kafka Sink

```
package com.atguigu.flink.java.chapter_11;

import com.atguigu.flink.java.chapter_5.WaterSensor;
import org.apache.flink.streaming.api.datastream.DataStreamSource;
import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
import org.apache.flink.table.api.DataTypes;
import org.apache.flink.table.api.Table;
import org.apache.flink.table.api.bridge.java.StreamTableEnvironment;
import org.apache.flink.table.descriptors.Json;
import org.apache.flink.table.descriptors.Kafka;
import org.apache.flink.table.descriptors.Schema;

import static org.apache.flink.table.api.Expressions.$;

public class Flink03_TableApi_ToKafka {
    public static void main(String[] args) {
        StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment();
        env.setParallelism(1);
        DataStreamSource<WaterSensor> waterSensorStream =
            env.fromElements(new WaterSensor("sensor_1", 1000L, 10),
                             new WaterSensor("sensor_1", 2000L, 20),
                             new WaterSensor("sensor_2", 3000L, 30),
                             new WaterSensor("sensor_1", 4000L, 40),
                             new WaterSensor("sensor_1", 5000L, 50),
                             new WaterSensor("sensor_2", 6000L, 60));
        // 1. 创建表的执行环境
        StreamTableEnvironment tableEnv = StreamTableEnvironment.create(env);

        Table sensorTable = tableEnv.fromDataStream(waterSensorStream);
        Table resultTable = sensorTable
            .where($("id").isEqual("sensor_1"))
            .select($("id"), $("ts"), $("vc"));

        // 创建输出表
        Schema schema = new Schema()
            .field("id", DataTypes.STRING())
            .field("ts", DataTypes.BIGINT())
            .field("vc", DataTypes.INT());
        tableEnv
            .connect(new Kafka()
                         .version("universal")
                         .topic("sensor")
                         .sinkPartitionerRoundRobin()
                         .property("bootstrap.servers", "hadoop102:9092,hadoop103:9092,hadoop104:9092"))
            .withFormat(new Json())
            .withSchema(schema)
            .createTemporaryTable("sensor");

        // 把数据写入到输出表中
        resultTable.executeInsert("sensor");
    }
}
```
### 1.7其他Connector用法

参考官方文档: https://ci.apache.org/projects/flink/flink-docs-release-1.12/zh/dev/table/connect.html

## 二.Flink SQL

### 2.1 查询未注册的表

```java
package com.atguigu.flink.java.chapter_11;

import com.atguigu.flink.java.chapter_5.WaterSensor;
import org.apache.flink.streaming.api.datastream.DataStreamSource;
import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
import org.apache.flink.table.api.Table;
import org.apache.flink.table.api.bridge.java.StreamTableEnvironment;
import org.apache.flink.types.Row;

public class Flink05_SQL_BaseUse {
    public static void main(String[] args) throws Exception {
        StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment();
        env.setParallelism(1);
        DataStreamSource<WaterSensor> waterSensorStream =
            env.fromElements(new WaterSensor("sensor_1", 1000L, 10),
                             new WaterSensor("sensor_1", 2000L, 20),
                             new WaterSensor("sensor_2", 3000L, 30),
                             new WaterSensor("sensor_1", 4000L, 40),
                             new WaterSensor("sensor_1", 5000L, 50),
                             new WaterSensor("sensor_2", 6000L, 60));

        StreamTableEnvironment tableEnv = StreamTableEnvironment.create(env);
        // 使用sql查询未注册的表
        Table inputTable = tableEnv.fromDataStream(waterSensorStream);
        Table resultTable = tableEnv.sqlQuery("select * from " + inputTable + " where id='sensor_1'");
        tableEnv.toAppendStream(resultTable, Row.class).print();
    
        env.execute();
    }
}
```
### 2.2 查询已注册的表

```
package com.atguigu.flink.java.chapter_11;

import com.atguigu.flink.java.chapter_5.WaterSensor;
import org.apache.flink.streaming.api.datastream.DataStreamSource;
import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
import org.apache.flink.table.api.Table;
import org.apache.flink.table.api.bridge.java.StreamTableEnvironment;
import org.apache.flink.types.Row;

public class Flink05_SQL_BaseUse_2 {
    public static void main(String[] args) throws Exception {
        StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment();
        env.setParallelism(1);
        DataStreamSource<WaterSensor> waterSensorStream =
            env.fromElements(new WaterSensor("sensor_1", 1000L, 10),
                             new WaterSensor("sensor_1", 2000L, 20),
                             new WaterSensor("sensor_2", 3000L, 30),
                             new WaterSensor("sensor_1", 4000L, 40),
                             new WaterSensor("sensor_1", 5000L, 50),
                             new WaterSensor("sensor_2", 6000L, 60));

        StreamTableEnvironment tableEnv = StreamTableEnvironment.create(env);
        // 使用sql查询一个已注册的表
        // 1. 从流得到一个表
        Table inputTable = tableEnv.fromDataStream(waterSensorStream);
        // 2. 把注册为一个临时视图
        tableEnv.createTemporaryView("sensor", inputTable);
        // 3. 在临时视图查询数据, 并得到一个新表
        Table resultTable = tableEnv.sqlQuery("select * from sensor where id='sensor_1'");
        // 4. 显示resultTable的数据
        tableEnv.toAppendStream(resultTable, Row.class).print();
        env.execute();
    }
}

方式二：直接从流，转换成表，并注册表名(没有 Table的对象)
tableEnv.createTemporaryView("inputTable", waterSensorStream);
// 这种方式，如果需要 Table对象，可以从表名获取
 Table sensorTable = tableEnv.from("inputTable");

```
<font color='red'>pt_time as PROCTIME()</font> 为声明处理时间字段

```
tableEnv.executeSql("create table sensor(id string,ts bigint,vc int,pt_time as PROCTIME()) with("
                                + "'connector' = 'filesystem',"
                                + "'path' = 'input/sensor.txt',"
                                + "'format' = 'csv'"
                                + ")");
```
### 2.3  Kafka到Kafka

```java
//使用sql从Kafka读数据, 并写入到Kafka中
package com.atguigu.flink.java.chapter_11;

import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
import org.apache.flink.table.api.bridge.java.StreamTableEnvironment;

public class Flink05_SQL_Kafka2Kafka {
    public static void main(String[] args) throws Exception {
        StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment();
        env.setParallelism(1);
        StreamTableEnvironment tableEnv = StreamTableEnvironment.create(env);

        // 1. 注册SourceTable: source_sensor
        tableEnv.executeSql("create table source_sensor (id string, ts bigint, vc int) with("
                                + "'connector' = 'kafka',"
                                + "'topic' = 'topic_source_sensor',"
                                + "'properties.bootstrap.servers' = 'hadoop102:9092,hadoop103:9092,hadoop104:9092',"
                                + "'properties.group.id' = 'atguigu',"
                                + "'scan.startup.mode' = 'latest-offset',"
                                + "'format' = 'csv'"
                                + ")");

        // 2. 注册SinkTable: sink_sensor
        tableEnv.executeSql("create table sink_sensor(id string, ts bigint, vc int) with("
                                + "'connector' = 'kafka',"
                                + "'topic' = 'topic_sink_sensor',"
                                + "'properties.bootstrap.servers' = 'hadoop102:9092,hadoop103:9092,hadoop104:9092',"
                                + "'format' = 'csv'"
                                + ")");

        // 3. 从SourceTable 查询数据, 并写入到 SinkTable
        tableEnv.executeSql("insert into sink_sensor select * from source_sensor where id='sensor_1'");
    }
}
```
使用 sql 关联外部系统：
语法 ：create table 表名 （字段名 字段类型，字段名 字段类型.....） with （ 参数名=参数值，参数名=参数值.....）
注意 ： 去官网查看 参数名 有哪些，有一些是必需的，有一些是可选的

https://ci.apache.org/projects/flink/flink-docs-release-1.12/dev/table/connectors/kafka.html

## 四.时间属性

### 4.1处理时间

#### 4.1.1 DataStream 到 Table 转换时定义

处理时间属性可以在schema定义的时候用.proctime后缀来定义。时间属性一定不能定义在一个已有字段上，所以它只能定义在schema定义的最后

```
StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment();
env.setParallelism(1);
DataStreamSource<WaterSensor> waterSensorStream =
    env.fromElements(new WaterSensor("sensor_1", 1000L, 10),
                     new WaterSensor("sensor_1", 2000L, 20),
                     new WaterSensor("sensor_2", 3000L, 30),
                     new WaterSensor("sensor_1", 4000L, 40),
                     new WaterSensor("sensor_1", 5000L, 50),
                     new WaterSensor("sensor_2", 6000L, 60));
// 1. 创建表的执行环境
StreamTableEnvironment tableEnv = StreamTableEnvironment.create(env);

// 声明一个额外的字段来作为处理时间字段
Table sensorTable = tableEnv.fromDataStream(waterSensorStream, $("id"), $("ts"), $("vc"), $("pt").proctime());

sensorTable.execute().print();
```
#### 4.1.2 在创建表的 DDL 中定义

```
package com.atguigu.flink.java.chapter_11;

import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
import org.apache.flink.table.api.TableResult;
import org.apache.flink.table.api.bridge.java.StreamTableEnvironment;

public class Flink06_TableApi_ProcessTime {
    public static void main(String[] args) throws Exception {
        StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment();
        env.setParallelism(1);
        // 1. 创建表的执行环境
        StreamTableEnvironment tableEnv = StreamTableEnvironment.create(env);
        // 创建表, 声明一个额外的列作为处理时间
        tableEnv.executeSql("create table sensor(id string,ts bigint,vc int,pt_time as PROCTIME()) with("
                                + "'connector' = 'filesystem',"
                                + "'path' = 'input/sensor.txt',"
                                + "'format' = 'csv'"
                                + ")");

        TableResult result = tableEnv.executeSql("select * from sensor");
        result.print();
    }

}
```
### 4.2事件时间

#### 4.2.1 DataStream 到 Table 转换时定义

```
事件时间属性可以用.rowtime后缀在定义DataStream schema 的时候来定义。
```
<font color='red'>时间戳和watermark</font>在这之前一定是<font color='red'>在DataStream上已经定义好了</font>。

```
在从DataStream到Table转换时定义事件时间属性有两种方式。取决于用 .rowtime 后缀修饰的字段名字是否是已有字段，事件时间字段可以是：
		在 schema 的结尾追加一个新的字段。
		替换一个已经存在的字段。
```
```
不管在哪种情况下，事件时间字段都表示DataStream中定义的事件的时间戳。
```
```java
package com.atguigu.flink.java.chapter_11;

import com.atguigu.flink.java.chapter_5.WaterSensor;
import org.apache.flink.api.common.eventtime.WatermarkStrategy;
import org.apache.flink.streaming.api.datastream.SingleOutputStreamOperator;
import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
import org.apache.flink.table.api.Table;
import org.apache.flink.table.api.bridge.java.StreamTableEnvironment;

import java.time.Duration;

import static org.apache.flink.table.api.Expressions.$;

public class Flink07_TableApi_EventTime {
    public static void main(String[] args) throws Exception {
        StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment();
        env.setParallelism(1);
        SingleOutputStreamOperator<WaterSensor> waterSensorStream = env
            .fromElements(new WaterSensor("sensor_1", 1000L, 10),
                          new WaterSensor("sensor_1", 2000L, 20),
                          new WaterSensor("sensor_2", 3000L, 30),
                          new WaterSensor("sensor_1", 4000L, 40),
                          new WaterSensor("sensor_1", 5000L, 50),
                          new WaterSensor("sensor_2", 6000L, 60))
            .assignTimestampsAndWatermarks(
                WatermarkStrategy
                    .<WaterSensor>forBoundedOutOfOrderness(Duration.ofSeconds(5))
                    .withTimestampAssigner((element, recordTimestamp) -> element.getTs())
            );

        StreamTableEnvironment tableEnv = StreamTableEnvironment.create(env);
        Table table = tableEnv
            // 用一个额外的字段作为事件时间属性
            .fromDataStream(waterSensorStream, $("id"), $("ts"), $("vc"), $("et").rowtime());
        table.execute().print();
        env.execute();

    }

}


// 使用已有的字段作为时间属性
.fromDataStream(waterSensorStream, $("id"), $("ts").rowtime(), $("vc"));
```
#### 4.2.2 在创建表的 DDL 中定义

```
事件时间属性可以用 WATERMARK 语句在 CREATE TABLE DDL 中进行定义。WATERMARK 语句在一个已有字段上定义一个 watermark 生成表达式，同时标记这个已有字段为时间属性字段。
```
```java
package com.atguigu.flink.java.chapter_11;

import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
import org.apache.flink.table.api.bridge.java.StreamTableEnvironment;

public class Flink07_TableApi_EventTime_2 {
    public static void main(String[] args) throws Exception {
        StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment();
        env.setParallelism(1);

        StreamTableEnvironment tEnv = StreamTableEnvironment.create(env);
        // 作为事件时间的字段必须是 timestamp(3) 类型, 所以根据 long 类型的 ts 计算出来一个 t
        tEnv.executeSql("create table sensor(" +
                            "id string," +
                            "ts bigint," +
                            "vc int, " +
                            "t as to_timestamp(from_unixtime(ts/1000,'yyyy-MM-dd HH:mm:ss'))," +
                            "watermark for t as t - interval '5' second)" +
                            "with("
                            + "'connector' = 'filesystem',"
                            + "'path' = 'input/sensor.txt',"
                            + "'format' = 'csv'"
                            + ")");

        tEnv.sqlQuery("select * from sensor").execute().print();

    }
}
```
<font color='red'>说明:</font>
1.把一个现有的列定义为一个为表标记事件时间的属性。该列的类型必须为 TIMESTAMP(3)，且是 schema 中的顶层列，它也可以是一个计算列。

![image-20211223112843727](https://gitee.com/jerry-chen417/picgo/raw/master/img/202112231128822.png)

```
2.严格递增时间戳： WATERMARK FOR rowtime_column AS rowtime_column。
	3.递增时间戳： WATERMARK FOR rowtime_column AS rowtime_column - INTERVAL '0.001' SECOND。
	4.有界乱序时间戳： WATERMARK FOR rowtime_column AS rowtime_column - INTERVAL 'string' timeUnit。
	5.当发现时区所导致的时间问题时，可设置本地使用的时区：
Configuration configuration = tableEnv.getConfig().getConfiguration();
configuration.setString("table.local-time-zone", "GMT");
	6.参考官网https://ci.apache.org/projects/flink/flink-docs-release-1.12/dev/table/sql/create.html#watermark
```
设置时区:

![image-20211218144746825](https://gitee.com/jerry-chen417/picgo/raw/master/img/202112181447915.png)
