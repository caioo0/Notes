# Docker Swarm

> 资料来源：https://zhuanlan.zhihu.com/p/130436783

Docker Compose进行容器编排，使得我们可以一键布署存在多个容器的项目。但Docker Compose只能在单个节点上使用，而大型的项目都是运行在集群上的，这就给Docker Compose的使用带来了很大的限制，所以我们需要一个在集群上进行容器启动、停止、复制、状态监控等操作的容器编排工具。



目前可以实现这个目标的比较知名的工具主要有:

- Docker Swarm：Docker自带的编排工具，使用方便且轻量化；
- 第三方编排工具: mesos+marathon；
- kubernetes（k8s）：最流行的第三方容器编排工具，功能强大，发展迅速，但使用成本高，布署运维工作量较大，软件也越来越重。

本文将简单介绍下Docker Swarm的基本原理与使用方式。

### 基本原理

swarm是使用docker引擎内置的集群管理和编排工具。swarm集群的框架和hadoop集群或其他分布式系统类似，它也是由节点构成，每一个节点就是一台主机或者虚拟机。工作的机制也是主从模式（master/slaver）,节点分为两种，一种是负责管理的Manager，另一种是具体干活的Worker。

- 管理节点：用于 Swarm 集群的管理，docker swarm 命令基本只能在管理节点执行（节点退出集群命令 docker swarm leave 可以在工作节点执行）。为了避免单点故障，一个Swarm 集群可以有多个管理节点，但只有一个管理节点可以成为 leader，leader 通过 [raft 协议](https://zhuanlan.zhihu.com/p/27207160)实现。(关于raft协议详细，[点击此处](https://juejin.cn/post/7143541597165060109))

- 工作节点：是任务执行节点，管理节点将任务 (Task) 下发至工作节点执行。管理节点默认也作为工作节点，也可以通过配置让服务只运行在管理节点。

![image-20230719124523692](.\image-20230719124523692.png)

这样一来，多个 Docker 主机就被抽象为单个大型的虚拟 Docker 主机，在管理节点上，用户可以像在单机一样在集群上操作容器或服务。

### 基本概念

Swarm集群中管理的对象主要由三个，Task、Service与Node，其中Node上面已经介绍过，这里解释下Task与Service的概念。

**任务（Task）**

Swarm 中的最小的调度单位，目前一个Task就是一个容器。

**服务（Service）**

Service一般是由一组相同的Task组成，Service是这组Task要完成的任务的一个抽象。按照其包含的Task的布署方式分为两种：

- replicated services 按照一定规则在各个工作节点上运行指定个数的任务。
- global services 每个工作节点上运行一个任务。

这两种模式是在服务创建时通过创建命令docker service create的 --mode 参数指定的。

Service与Task以及容器的关系如下

![image-20230719124749364](.\imgs\image-20230719124749364.png)

总结成一句话就是，swarm集群（cluster）是由节点（node）组成；服务（service）一般包含若干个任务（Task），一个Task就是运行一个容器，所有这些Task都是在节点上执行的，具体在那个个节点上执行是由管理节点调度的。

### 常见操作

### 集群造作

集群初始化：在任意一台机器上执行下列命令会初始化一个集群，且当前节点为Manager.

```
docker swarm init 
docker swarm init --advertise-addr xxx.xxx.xxx.xxx #主机包含多个ip情形
```

增加工作节点：在执行集群初始化命令后会出现提示如何加入新的节点到Swarm集群，也可以通过下列命令查看如何将新的节点以Worker或Manager身份加入集群。quiet选项表示只显示token。

```
docker swarm join-token worker [--quiet]
docker swarm join-token manager [--quiet]
```

列出集群的节点

```
docker node ls
```

改变节点角色

```
docker node promote work-node1 # 将work-node1节点升级为manager
docker node demote work-node1 # 将work-node1节点降级为worker
```

### 服务操作

Swarm集群中服务的管理操作是通过 docker service [command]命令实现的，具体有哪些子命令与选项参数可查看help，常见操作如下。

创建服务：下列命令根据nginx镜像创建一个名为nginx的服务，该服务包含3个副本，服务映射到主机的80端口供外部访问。

```
docker service create --replicas 3 -p 80:80 --name nginx nginx
```

查看服务

```
docker service ls # 列出所有服务
docker service ps nginx # 查看nginx服务详情
docker service logs nginx # 查看nginx控制台日志
```

服务伸缩：通过docker service scale命令可以实时的调整服务的副本的数量，从而可以根据流量的波动弹性地伸缩服务规模，如下列命令可以将nginx服务的副本数量调整为5个。

```
docker service scale nginx=5
```

删除服务：通过docker service rm [name]实现，如删除nginx服务

```
docker service rm nginx
```

### 负载均衡模式

从使用者角度看，一个Service相当于它的所有Task的一个反向代理，它主要使用了 Linux 内核 iptables 和 IPVS 的功能来实现服务发现和负载均衡。

- iptables：Linux 内核中的包过滤技术，它可用于根据数据包的内容进行分类、修改和转发决策。
- IPVS ：Linux 内核中传输级负载均衡器。

Swarm支持三种模式的负载均衡，它们的使用方式如下：

- 基于 DNS 的负载均衡：DNS server 内嵌于 Docker 引擎，Docker DNS 解析服务名并安装随机次序返回容器 ID 地址列表，客户端通常会挑第一个 IP 访问。在服务启动时，通过指定--endpoint-mode参数为dnsrr来设定，另外服务需要加入一个覆盖网，例如

```
docker service create --endpoint-mode dnsrr --network overlay1  --replicas 3 --name nginx nginx
```

基于 VIP 的负载均衡：默认时这种模式，在服务启动时可以指定或被分配一个 IP 地址，该 IP 地址可以映射到与该服务关联的多个容器的 IP 地址。示例如下

```
docker service create --network overlay1  --replicas 3 --name nginx nginx
```

路由网格 （Routing mesh）：这种模式服务暴露的端口会暴露在 Swarm 集群中的所有工作节点，通过访问任何一台主机的ip或域名加暴露的端口号就可以访问到该服务。使用也很简单，只需要在服务创建时添加端口号映射就可以了，如下

```
docker service create --network overlay1  --replicas 3 -p 80:80 --name nginx nginx
```

