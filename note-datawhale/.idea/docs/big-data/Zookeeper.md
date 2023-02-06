# 第十二章 Zookeeper

## 12.1 Zookeepr 介绍

Zookeeper是一个开源的分布式的，为分布式应用提供协调服务的Apache项目

### 12.1.1 Zookeepr工作机制

Zookeeper从设计模式角度来理解：是一个基于观察者模式设计的分布式服务管理框架，它**负责存储和管理大家都关心的数据**，然后**接受观察者的注册**，一旦这些数据的状态发生变化，Zookeeper就将**负责通知已经在Zookeeper上注册的那些观察者**做出相应的反应，从而实现集群中类似Master/Slave管理模式

![img.png](chapter12-01.png)

### 12.1.2 Zookeeper 特点

![img.png](chapter12-02.png)

1) Zookper: 一个领导者（Leader）,多个跟随者 （Follower）组成的集群。
2) 集群只要有半数以上节点存活，Zookeeper集群就能正常服务。👀️
3) 全局数据一致：每个Server保存一份相同的数据副本，Client无论连接到哪个Server,数据都是一致的。
4) 更新请求顺序进行，来自同一个Client 的更新请求按其发送顺序依次进行。
5) 数据更新原子性，一次数据更新要么成功，要么失败。
6) 实时性，在一定时间范围内，Client能读到最新数据。

### 12.2 数据结构

Zookeeper 能够协助解决很多的分布式难题，其底层仅依赖两个主要的组件：

- ZNode文件系统
- watch监听机制

#### ZNode文件系统

Zookeeper 数据模型的结构与**Unix文件系统很类似**，整体上可以看作是一棵树，每个节点称做一个**Znode**,每个ZNode默认能够存储**1MB**的数据，每个**ZNode**都可以**通过其路径唯一标识**。

`ZNode`既能存储数据，也能创建子`ZNode`

`ZNode`只适合存储非常小量的数据，不能超过**1MB**,最好小于**1KB**

![img.png](chapter12-03.png)

#### ZNode的分类

- 按照生命周期分为：
  - 短暂（ephemeral）(断开连接自动删除)
  - 持久（persistent）(断开连接不删除，默认)
- 按照是否自带序列编号分为：
  - SEQUENTIAL(带自增序列编号，由父节点维护)
  - 非SEQUENTIAL(不带自增序列编码，默认)

因此创建ZNode时，可以指定以下四种类型，包括：

* **PERSISTENT，持久性ZNode** 。创建后，即使客户端与服务端断开连接也不会删除，只有客户端主动删除才会消失。
* **PERSISTENT_SEQUENTIAL，持久性顺序编号ZNode** 。和持久性节点一样不会因为断开连接后而删除，并且ZNode的编号会自动增加。
* **EPHEMERAL，临时性ZNode** 。客户端与服务端断开连接，该ZNode会被删除。
* **EPEMERAL_SEQUENTIAL，临时性顺序编号ZNode** 。和临时性节点一样，断开连接会被删除，并且ZNode的编号会自动增加。
*


| 序号                                                               | 节点类型              | 详解                                                                |
| -------------------------------------------------------------------- | ----------------------- | --------------------------------------------------------------------- |
| 1                                                                  | PERSISTENT            | 持久化 znode 节点，一旦创建这个 znode 节点，存储的数据不会主动      |
| 消失，除非是客户端主动 delete                                      |                       |                                                                     |
| 2                                                                  | PERSISTENT_SEQUENTIAL | 自动增加自增顺序编号的 znode 节点，比如 ClientA 去zookeeper         |
| service 上建立一个 znode 名字叫做 /zk/conf，指定了这种类型的节点   |                       |                                                                     |
| 后zk会创建 /zk/conf0000000000，ClientB 再去创建就是创建            |                       |                                                                     |
| /zk/conf0000000001，ClientC 是创建/zk/conf0000000002，以后任意     |                       |                                                                     |
| Client 来创建这个 znode 都会得到一个比当前 zookeeper 命名空间最    |                       |                                                                     |
| 大 znod e编号 +1 的znode，也就说任意一个 Client 去创建 znode 都是  |                       |                                                                     |
| 保证得到的znode 编号是递增的，而且是唯一的 znode 节点              |                       |                                                                     |
| 3                                                                  | EPHEMERAL             | 临时 znode 节点，Client 连接到 zk service 的时候会建立一个session， |
| 之后用这个 zk 连接实例在该 session 期间创建该类型的znode，一旦     |                       |                                                                     |
| Client 关闭了 zookeeper 的连接，服务器就会清除session，然后这个    |                       |                                                                     |
| session 建立的 znode 节点都会从命名空间消失。总结就是，这个类      |                       |                                                                     |
| 型的 znode 的生命周期是和 Client 建立的连接一样的。比如 ClientA 创 |                       |                                                                     |
| 建了一个 EPHEMERAL 的 /zk/conf的 znode 节点，一旦 ClientA 的       |                       |                                                                     |
| zookeeper 连接关闭，这个znode 节点就会消失。整个zookeeper          |                       |                                                                     |
| service命名空间里就会删除这个znode节点                             |                       |                                                                     |
| 4                                                                  | EPHEMERAL_SEQUENTIAL  | 临时自动编号节点znode 节点编号会自动增加但是会随session 消失而      |
| 消失                                                               |                       |                                                                     |

> **注意项**
>
> - 创建ZNode时设置顺序标识，ZNode名称后会附加一个值，顺序号时一个递增的计数器，由父节点维护。
> - 在分布式系统中，顺序号可以被用于为所有的事件进行全局排序，这样客户端可以通过顺序号推断事件的顺序。
> - EPHEMERAL 类型的节点不能有子节点，所以只能是叶子节点。
> - 客户端可以在ZNode上设置监听器。

#### stat结构体

Stat结构体就是成功创建znode节点后系统返回给客户端的信息。

znode数据信息字段解释：

- cZxid = 0x400000093 节点创建的时候的zxid
  - 在并发修改的情况下：每次修改ZooKeeper状态都会收到一个zxid形式的时间戳，也就是
    ZooKeeper事务ID。事务ID是ZooKeeper中所有修改总的次序。每个修改都有唯一的zxid，如果
- zxid1小于zxid2，那么zxid1在zxid2之前发生。
- ctime = 被创建的毫秒数(从1970年开始)
- mtime = znode最后修改的毫秒数(从1970年开始)
- mZxid = znode最后更新的事务zxid
- pZxid = 最后更新的子节点zxid
- cversion = znode子节点变化号，znode子节点修改次数
- dataVersion = 节点数据的更新次数
- aclVersion = 节点（ACL）的更新次数
- ephemeralOwner = 0x0 如果该节点为ephemeral节点, ephemeralOwner值表示与该节点绑定的
- session id. 如果该节点不是ephemeral节点, ephemeralOwner值为0
- dataLength = 节点数据的字节数
- numChildren = 子节点个数，不包含孙子节点

#### 监听机制

Watcher是基于**观察者模式**实现的一种机制。如果我们需要实现当某个ZNode节点发生变化时收到通知，就可以使用Watcher监听器。

**客户端通过设置监视点（watcher）向 ZooKeeper 注册需要接收通知的 znode，在 znode 发生变化时 ZooKeeper 就会向客户端发送消息** 。

**这种通知机制是一次性的** 。一旦watcher被触发，ZooKeeper就会从相应的存储中删除。如果需要不断监听ZNode的变化，可以在收到通知后再设置新的watcher注册到ZooKeeper。

监视点的类型有很多，如 **监控ZNode数据变化、监控ZNode子节点变化、监控ZNode 创建或删除** 。

> 思考题：注册的监听在事件响应之后就失效了。那么怎么做到连续监听？

- 监听器的工作机制，其实是在客户端会专门创建一个监听线程，在本机的一个端口上等待
  ZooKeeper集群发送过来事件。
- 监听工作原理：ZooKeeper 的 Watcher 机制主要包括客户端线程、客户端 WatcherManager、
  Zookeeper 服务器三部分。客户端在向 ZooKeeper 服务器注册的同时，会将 Watcher 对象存储在客
  户端的 WatcherManager 当中。当 ZooKeeper 服务器触Watcher 事件后，会向客户端发送通知，客户
  端线程从 WatcherManager 中取出对应的 Watcher 对象来执行回调逻辑。

![img.png](chapter12-04.png)

- 在main线程中创建Zookeeper客户端，这时就会创建两个线程，一个负责网络连接通信(connect)，
  一个负责监听(listener)，通过connect线程将注册的监听事件添加到列表中。Zookeeper监听有数据
  或路径变化，就会将这个消息发送给listennr线程，listener线程内部调用了process()方法。

## 12.3 选举机制

Zookeeper 是一个高可用的应用框架，因为Zookeeper是支持集群的。Zookeeper在集群状态下，配置文件是不会指定Master和Slave，而是在Zookeeper服务器初始化时 就在内部进行选举，产生一台作为Leader，多台作为Follower，并且遵守半数可用原则。

由于遵守半数可用原则，所以5台服务器和6台服务器，实际上最大允许宕机数量都是3台，所以为了节约成本，**集群服务器数量一般设置为奇数**。

如果运行时，**如果长时间无法与Leader保持连接的话，则会再次进行选举，产生新的Leader，以保证服务的可用**。

![img.png](chapter12-05.png)

## 12.4 应用场景

提供的服务包括：**统一命名服务、统一配置管理、统一集群管理、服务器节点动态上下线、软负债均衡**等。

- **统一命名服务：** 在分布式环境下，经常需要对应用/服务进行统一命名，便于识别。
- **统一配置管理：**

  - 分布式环境下，配置文件同步非常常见。
    - 一般要求一个集群中，所有节点的配置信息是一致的，比如Kafka集群。
    - 对配置文件修改后，希望能够快速同步到各个节点上。
  - 配置管理可交由Zookeeper实现
    - 可将配置信息写入Zookeepr上的一个ZNode.
    - 各个客户端服务器监听这个ZNode.
    - 一旦ZNode中的数据被修改，ZooKeeper将通知各个客户端服务器。
- **统一集群管理：**

  - 分布式环境中，实时掌握每个节点的状态式必要的。
    - 可根据节点实时状态做出一些调整。
  - Zookeeper可以实现实时监控节点状态变化。
    - 可将节点信息写入ZooKeeper上的一个ZNode.
    - 监听这个ZNode可获取它的实时状态变化。
- **服务器动态上下线：** 客户端能实时洞察到服务器上下线的变化
- **软负载均衡：** 在ZooKeeper中记录每台服务器的访问数，让访问数最少的服务器去处理最新的客户端请求
  ![img.png](chapter12-06.png)

## 12.5 Zookeeper 安装

- 官网地址：http://ZooKeeper.apache.org/
- 官网快速开始地址：http://zookeeper.apache.org/doc/current/zookeeperStarted.html
- 官网API地址：http://ZooKeeper.apache.org/doc/r3.4.10/api/index.html
- 下载地址：http://mirrors.hust.edu.cn/apache/zookeeper/
- 版本号：zookeeper-3.4.14.tar.gz

### 12.5.1 单机版安装

第一步：上传和解压

```
tar -zxvf zookeeper-3.4.14.tar.gz -C ../install/
```

第二步：复制配置文件

```
cp zoo_sample.cfg zoo.cfg
```

第三步：修改配置zoo.cfg

```
tickTime=2000
initLimit=10
syncLimit=5
dataDir=/root/install/zookeeper-3.4.14/zookeeper_data
dataLogDir=/root/install/zookeeper-3.4.14/log
clientPort=2181
```

第四步：配置环境变量

```
ZOOKEEPER_HOME=/root/install/zookeeper-3.4.14
```

加入PATH
第五步：启动zookeeper

```
zkServer.sh start
Using config: /root/install/zookeeper-3.4.14/bin/../conf/zoo.cfg
Starting zookeeper ... STARTED
[root@hadoop5 ~]# zkServer.sh status
ZooKeeper JMX enabled by default
Using config: /root/install/zookeeper-3.4.14/bin/../conf/zoo.cfg
Mode: standalone
```

查看进程是否启动

```
[root@hadoop5 ~]# jps
4020 Jps
4001 QuorumPeerMain
```

可视化界面的话，我推荐使用`ZooInspector`，操作比较简便：

**使用java连接ZooKeeper**

首先引入Maven依赖：

```md
<dependency>
    <groupId>org.apache.zookeeper</groupId>
    <artifactId>zookeeper</artifactId>
    <version>3.4.14</version>
</dependency>
```

写一个Main方法，进行操作：

```md
//连接地址及端口号
    private static final String SERVER_HOST = "hadoop5:2181";

    //会话超时时间
    private static final int SESSION_TIME_OUT = 2000;

    public static void main(String[] args) throws Exception {
        //参数一：服务端地址及端口号
        //参数二：超时时间
        //参数三：监听器
        ZooKeeper zooKeeper = new ZooKeeper(SERVER_HOST, SESSION_TIME_OUT, new Watcher() {
            @Override
            public void process(WatchedEvent watchedEvent) {
                //获取事件的状态
                Event.KeeperState state = watchedEvent.getState();
                //判断是否是连接事件
                if (Event.KeeperState.SyncConnected == state) {
                    Event.EventType type = watchedEvent.getType();
                    if (Event.EventType.None == type) {
                        System.out.println("zk客户端已连接...");
                    }
                }
            }
        });
        zooKeeper.create("/java", "Hello World".getBytes(), ZooDefs.Ids.OPEN_ACL_UNSAFE, CreateMode.PERSISTENT);
        System.out.println("新增ZNode成功");
        zooKeeper.close();
    }
```

创建一个持久性ZNode，路径是/java，值为"Hello World"

### 12.5.2 分布式安装

下载地址：http://mirrors.hust.edu.cn/apache/zookeeper/
版本号：`zookeeper-3.4.14.tar.gz`

解压缩安装到自己的安装目录

```
tar -zxvf zookeeper-3.4.14.tar.gz -C ../install/ 
```

```
修改配置文件： cp zoo_sample.cfg zoo.cfg
vi zoo.cfg
tickTime=2000 
initLimit=10 
syncLimit=5 
dataDir=/root/install/zookeeper-3.4.14/data
dataLogDir=/root/install/zookeeper-3.4.14/log 
clientPort=2181 
server.1=hadoop1:2888:3888 
server.2=hadoop2:2888:3888 
server.3=hadoop3:2888:3888 
#分发安装包到其他节点 
scp -r zookeeper-3.4.14/ hadoop2:/root/install/
scp -r zookeeper-3.4.14/ hadoop3:/root/install/
#添加服务器id 
#在dataDir指定的数据目录里面新建一个文件，文件名叫myid，里面存放的内容就是服务器的server.id
 
hadoop1 echo 1 > myid 
hadoop2 echo 2 > myid 
hadoop3 echo 3 > myid
```

**配置参数解析**

tickTime：基本事件单元，以毫秒为单位。它用来控制心跳和超时，默认情况下最小的会话超时时

间为两倍的TickTime

initLimit：此配置表示，允许Follower（相对于leader而言的“客户端”）连接并同步到leader的初始化

连接时间，它以tickTime的倍数来表示。当超过设置倍数的tickTime时间，则连接失败。

syncLimit：此配置表示，leader与follower之间发送消息，请求和应答时间长度。如果follower在设

置的时间内不能与leader进行通信，那么此follower将被丢弃。

dataDir：存储内存中数据库快照的位置。

注意：如果需要保留日志信息，那么可以考虑配置dataLogDir的位置，这个位置就是日志的存

储目录。通常情况下是分开存储的。并且应该谨慎地选择日志存放的位置，使用专用的日志存

储设备能够大大地提高系统的性能，如果将日志存储在比较繁忙的存储设备上，那么将会在很

大程度上影响系统的性能。

clientPort：监听客户端连接的端口，默认是2181

server.id=主机名:心跳端口:选举端口 【只有在集群模式下需要】

例子：server.1=hadoop1:2888:3888

其中id虽然可以随便写，但是有两点要求，第一不能重复，第二范围是1-255，并且对应服务

器列表上还得存在对应的id文件，具体看下面操作

**启动集群**

```md

配置环境变量和生效 
ZOOKEEPER_HOME=/root/install/zookeeper-3.4.14 PATH=$PATH:$JAVA_HOME/bin:$HADOOP_HOME:$SCALA_HOME:$SPARK_HOME:$FLINK_HOME:$HADOOP _HOME/bin:$HADOOP_HOME/sbin:$ZOOKEEPER_HOME/bin 

启动集群 

启动命令： zkServer.sh start 
关闭命令： zkServer.sh stop 
查看集群节点状态和角色命令： zkServer.sh status 

注意：关于 zookeeper 集群， 记住，并没有一键启动集群的启动脚本，需要每个服务节点各自单独启动。 在每台服务节点中，都会运行一个 QuorumPeerMain 的 Java 进程，所以也还可以使用 JPS 命令来 检查该进程是否正常启动。 会在执行启动命令的目录下生产zookeeper.out文件，保存了启动的日志信息，如果没有启动成功，就检 查该日志中的异常信息


启动完成后查看状态信息：2台follower和1台leader 

[root@hadoop1 install]# zkServer.sh status 
ZooKeeper JMX enabled by default 
Using config: /root/install/zookeeper-3.4.14/bin/../conf/zoo.cfg
Mode: follower 

[root@hadoop2 zookeeper-3.4.14]# zkServer.sh status 

ZooKeeper JMX enabled by default
Using config: /root/install/zookeeper-3.4.14/bin/../conf/zoo.cfg
Mode: leader 

[root@hadoop3 zookeeper-3.4.14]# zkServer.sh status 
ZooKeeper JMX enabled by default 
Using config: /root/install/zookeeper-3.4.14/bin/../conf/zoo.cfg
Mode: follower


```

**集群的命令使用**

```md
# 连接本机
zkCli.sh

#连接其他服务器的
zkCli.sh -server hadoop1:2181

#查看帮助
help
```

命令

作用

ls / ls /zookeeper

查看znode子节点列表

create /zk "myData"

创建znode节点

get /zk

get /zk/node1

获取znode数据

set /zk "myData1"

设置znode数据

ls /zk watch

对一个节点的子节点变化事件注册了监听

get /zk watch

对一个节点的数据内容变化事件注册了监听

create -e /zk "myData"

创建临时znode节点

create -s /zk "myData"

创建顺序znode节点

create -e -s /zk "myData"

创建临时的顺序znode节点

delete /zk

只能删除没有子znode的znode

rmr /zk

不管里头有多少znode，统统删除

stat/zk

查看/zk节点的状态信息

conf

输出相关服务配置的详细信息

cons

列出所有连接到服务器的客户端的完全的连接/会话的详细信息。包括“接受/发送”的包数

量、会话 id、操作延迟、最后的操作执行等等信息

dump

列出未经处理的会话和临时节点

envi

输出关于服务环境的详细信息（区别于 conf 命令）

reqs

列出未经处理的请求

ruok

测试服务是否处于正确状态。如果确实如此，那么服务返回“imok ”，否则不做任何相应

stat

输出关于性能和连接的客户端的列表

wchs

列出服务器 watch 的详细信息

wchc

通过 session 列出服务器 watch 的详细信息，它的输出是一个与watch 相关的会话的列表

wchp

通过路径列出服务器 watch 的详细信息。它输出一个与 session相关的路径

## 12.6 Java API 使用

### 前提

1. IDE 创建一个maven工程
2. 添加pom文件

   ```md
   <dependencies>
   		<dependency>
   			<groupId>junit</groupId>
   			<artifactId>junit</artifactId>
   			<version>RELEASE</version>
   		</dependency>
   		<dependency>
   			<groupId>org.apache.logging.log4j</groupId>
   			<artifactId>log4j-core</artifactId>
   			<version>2.8.2</version>
   		</dependency>
   		<!-- https://mvnrepository.com/artifact/org.apache.zookeeper/zookeeper -->
   		<dependency>
   			<groupId>org.apache.zookeeper</groupId>
   			<artifactId>zookeeper</artifactId>
   			<version>3.4.16</version>
   		</dependency>
   </dependencies>
   ```
3. og4j.properties文件到项目根目录 需要在项目的src/main/resources目录下，新建一个文件，命名为“log4j.properties”，在文件中填入

```md
   log4j.rootLogger=INFO, stdout  
   log4j.appender.stdout=org.apache.log4j.ConsoleAppender  
   log4j.appender.stdout.layout=org.apache.log4j.PatternLayout  
   log4j.appender.stdout.layout.ConversionPattern=%d %p [%c] - %m%n  
   log4j.appender.logfile=org.apache.log4j.FileAppender  
   log4j.appender.logfile.File=target/spring.log  
   log4j.appender.logfile.layout=org.apache.log4j.PatternLayout  
   log4j.appender.logfile.layout.ConversionPattern=%d %p [%c] - %m%n  
```

4. 创建ZooKeeper客户端

```md
private static String connectString =
 "hadoop1:2181,hadoop2:2181,hadoop3:2181";
	private static int sessionTimeout = 2000;
	private ZooKeeper zkClient = null;

	@Before
	public void init() throws Exception {

	zkClient = new ZooKeeper(connectString, sessionTimeout, new Watcher() {

			@Override
			public void process(WatchedEvent event) {

				// 收到事件通知后的回调函数（用户的业务逻辑）
				System.out.println(event.getType() + "--" + event.getPath());

				// 再次启动监听
				try {
					zkClient.getChildren("/", true);
				} catch (Exception e) {
					e.printStackTrace();
				}
			}
		});
	}
```

### 12.6.1 创建 (create)

```
public String create(final String path, byte data[], List<ACL> acl, CreateMode createMode)

```

参数解释：

- path ZNode路径
- data ZNode存储的数据
- acl ACL权限控制
- createMode ZNode类型

ACL权限控制，有三个是ZooKeeper定义的常用权限，在ZooDefs.Ids类中：

```md
/**
 * This is a completely open ACL.
 * 完全开放的ACL，任何连接的客户端都可以操作该属性znode
 */
public final ArrayList<ACL> OPEN_ACL_UNSAFE = new ArrayList<ACL>(Collections.singletonList(new ACL(Perms.ALL, ANYONE_ID_UNSAFE)));

/**
 * This ACL gives the creators authentication id's all permissions.
 * 只有创建者才有ACL权限
 */
public final ArrayList<ACL> CREATOR_ALL_ACL = new ArrayList<ACL>(Collections.singletonList(new ACL(Perms.ALL, AUTH_IDS)));

/**
 * This ACL gives the world the ability to read.
 * 只能读取ACL
 */
public final ArrayList<ACL> READ_ACL_UNSAFE = new ArrayList<ACL>(Collections.singletonList(new ACL(Perms.READ, ANYONE_ID_UNSAFE)));
```

createMode就是前面讲过的四种ZNode类型：

```md
public enum CreateMode {
    /**
     * 持久性ZNode
     */
    PERSISTENT (0, false, false),
    /**
     * 持久性自动增加顺序号ZNode
     */
    PERSISTENT_SEQUENTIAL (2, false, true),
    /**
     * 临时性ZNode
     */
    EPHEMERAL (1, true, false),
    /**
     * 临时性自动增加顺序号ZNode
     */
    EPHEMERAL_SEQUENTIAL (3, true, true);
}
```

### 12.6.2 查询 (getData)

```md
//同步获取节点数据
public byte[] getData(String path, boolean watch, Stat stat){
    ...
}

//异步获取节点数据
public void getData(final String path, Watcher watcher, DataCallback cb, Object ctx){
    ...
}
```

同步getData()方法中的stat参数是用于接收返回的节点描述信息：

```md
public byte[] getData(final String path, Watcher watcher, Stat stat){
    //省略...
    GetDataResponse response = new GetDataResponse();
    //发送请求到ZooKeeper服务器，获取到response
    ReplyHeader r = cnxn.submitRequest(h, request, response, wcb);
    if (stat != null) {
        //把response的Stat赋值到传入的stat中
        DataTree.copyStat(response.getStat(), stat);
    }
}
```

使用同步getData()获取数据：

```md
 //数据的描述信息，包括版本号，ACL权限，子节点信息等等
    Stat stat = new Stat();
    //返回结果是byte[]数据，getData()方法底层会把描述信息复制到stat对象中
    byte[] bytes = zooKeeper.getData("/java", false, stat);
    //打印结果
    System.out.println("ZNode的数据data:" + new String(bytes));//Hello World
    System.out.println("获取到dataVersion版本号:" + stat.getVersion());//默认数据版本号是0
```

### 12.6.3 更新

```md
public Stat setData(final String path, byte data[], int version){
    ...
}
```

值得注意的是第三个参数version，使用CAS机制，这是为了防止多个客户端同时更新节点数据，所以需要在更新时传入版本号，每次更新都会使版本号+1，如果服务端接收到版本号，对比发现不一致的话，则会抛出异常。

所以，在更新前需要先查询获取到版本号，否则你不知道当前版本号是多少，就没法更新：

```md
 //获取节点描述信息
    Stat stat = new Stat();
    zooKeeper.getData("/java", false, stat);
    System.out.println("更新ZNode数据...");
    //更新操作，传入路径，更新值，版本号三个参数,返回结果是新的描述信息
    Stat setData = zooKeeper.setData("/java", "fly!!!".getBytes(), stat.getVersion());
    System.out.println("更新后的版本号为：" + setData.getVersion());//更新后的版本号为：1
```

如果传入的版本参数是"-1"，就是告诉zookeeper服务器，客户端需要基于数据的最新版本进行更新操作。但是-1并不是一个合法的版本号，而是一个标识符。

### 12.6.4 删除

```md
public void delete(final String path, int version){
    ...
}
```

- path 删除节点的路径
- version 版本号
  这里也需要传入版本号，调用getData()方法即可获取到版本号，很简单：

```md
Stat stat = new Stat();
zooKeeper.getData("/java", false, stat);
//删除ZNode
zooKeeper.delete("/java", stat.getVersion());
```

### 12.6.5 watcher机制

在上面第三点提到，ZooKeeper是可以使用通知监听机制，当ZNode发生变化会收到通知消息，进行处理。基于watcher机制，ZooKeeper能玩出很多花样。怎么使用？

ZooKeeper的通知监听机制，总的来说可以分为三个过程：

- 客户端注册 Watcher
- 服务器处理 Watcher
- 客户端回调 Watcher客户端。

注册 watcher 有 4 种方法，new ZooKeeper()、getData()、exists()、getChildren()。下面演示一下使用exists()方法注册watcher：

首先需要实现Watcher接口，新建一个监听器：

```md
public class MyWatcher implements Watcher {
    @Override
    public void process(WatchedEvent event) {
        //获取事件类型
        Event.EventType eventType = event.getType();
        //通知状态
        Event.KeeperState eventState = event.getState();
        //节点路径
        String eventPath = event.getPath();
        System.out.println("监听到的事件类型:" + eventType.name());
        System.out.println("监听到的通知状态:" + eventState.name());
        System.out.println("监听到的ZNode路径:" + eventPath);
    }
}
```

然后调用exists()方法，注册监听器：

```md
zooKeeper.exists("/java", new MyWatcher());
//对ZNode进行更新数据的操作，触发监听器
zooKeeper.setData("/java", "fly".getBytes(), -1);
```

然后在控制台就可以看到打印的信息：
![img_4.png](chapter12-07.png)

这里我们可以看到 **Event.EventType对象就是事件类型** ，我们可以对事件类型进行判断，再配合 **Event.KeeperState通知状态** ，做相关的业务处理，事件类型有哪些？

打开EventType、KeeperState的源码查看：

```
//事件类型是一个枚举
public enum EventType {
    None (-1),//无
    NodeCreated (1),//Watcher监听的数据节点被创建
    NodeDeleted (2),//Watcher监听的数据节点被删除
    NodeDataChanged (3),//Watcher监听的数据节点内容发生变更
    NodeChildrenChanged (4);//Watcher监听的数据节点的子节点列表发生变更
}

//通知状态也是一个枚举
public enum KeeperState {
    Unknown (-1),//属性过期
    Disconnected (0),//客户端与服务端断开连接
    NoSyncConnected (1),//属性过期
    SyncConnected (3),//客户端与服务端正常连接
    AuthFailed (4),//身份认证失败
    ConnectedReadOnly (5),//返回这个状态给客户端，客户端只能处理读请求
    SaslAuthenticated(6),//服务器采用SASL做校验时
    Expired (-112);//会话session失效
}
```

### watcher的特性

- 一次性:一旦watcher被触发，ZK都会从相应的存储中移除.

```md
 zooKeeper.exists("/java", new Watcher() {
        @Override
        public void process(WatchedEvent event) {
            System.out.println("我是exists()方法的监听器");
        }
    });
    //对ZNode进行更新数据的操作，触发监听器
    zooKeeper.setData("/java", "fly".getBytes(), -1);
    //企图第二次触发监听器
    zooKeeper.setData("/java", "spring".getBytes(), -1);
```

![img.png](chapter12-08.png)

- 串行执行:客户端Watcher回调的过程是一个串行同步的过程，这是为了保证顺序。

```md
zooKeeper.exists("/java", new Watcher() {
        @Override
        public void process(WatchedEvent event) {
            System.out.println("我是exists()方法的监听器");
        }
    });
    Stat stat = new Stat();
    zooKeeper.getData("/java", new Watcher() {
        @Override
        public void process(WatchedEvent event) {
            System.out.println("我是getData()方法的监听器");
        }
    }, stat);
    //对ZNode进行更新数据的操作，触发监听器
    zooKeeper.setData("/java", "fly".getBytes(), stat.getVersion());
```

打印结果，说明先调用exists()方法的监听器，再调用getData()方法的监听器。因为exists()方法先注册了。
![img.png](chapter12-09.png)

- 轻量级。WatchedEvent是ZK整个Watcher通知机制的最小通知单元。WatchedEvent包含三部分：通知状态，事件类型，节点路径。Watcher通知仅仅告诉客户端发生了什么事情，而不会说明事件的具体内容。

## 12.7 参考资料

1. https://mp.weixin.qq.com/s/BPiycGUGq61ZD63lm2ojoQ
2. https://mp.weixin.qq.com/s/fS-GlvOJNFRr4UGRlQC2mQ
3. https://zhuanlan.zhihu.com/p/59669985
