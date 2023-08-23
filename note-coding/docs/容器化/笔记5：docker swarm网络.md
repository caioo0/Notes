# Docker Swarm网络



> 资料来源：https://zhuanlan.zhihu.com/p/129258067

### Linux网络名词基础

**网络的命名空间（namespace）：**Linux在网络栈中引入网络命名空间，将独立的网络协议栈隔离到不同的命令空间中，彼此间无法通信；docker利用这一特性，实现不容器间的网络隔离。

**Veth设备对：**Veth设备对的引入是为了实现在不同网络命名空间的通信。

**Iptables/Netfilter：**Netfilter负责在内核中执行各种挂接的规则(过滤、修改、丢弃等)，运行在内核模式中；Iptables模式是在用户模式下运行的进程，负责协助维护内核中Netfilter的各种规则表；通过二者的配合来实现整个Linux网络协议栈中灵活的数据包处理机制。

**网桥：**网桥是一个二层网络设备，通过网桥可以将linux支持的不同的端口连接起来,并实现类似交换机那样的多对多的通信。

**路由：**Linux系统包含一个完整的路由功能，当IP层在处理数据发送或转发的时候，会使用路由表来决定发往哪里。

### 服务示例

为了便于说明，我这边搭建了一个简单的docker swarm集群，包含两个节点。先在集群上用docker network create 创建一个名为net1的[overlay网络](https://info.support.huawei.com/info-finder/encyclopedia/zh/Overlay%E7%BD%91%E7%BB%9C.html)，然后再创建三个服务，都加入到net1中，每个服务个包含一个运行实例。

```
docker network create --opt encrypted --subnet 100.0.0.0/24 -d overlay net1

docker service create --name redis --network net1 redis
docker service create --name node --network net1 nvbeta/node
docker service create --name nginx --network net1 -p 1080:80 nvbeta/swarm_nginxSwarm自带的Networks
```

这三个服务中，nginx为node服务提供负载均衡，将请求转发到node，node服务会访问redis获取数据，它们之间的依赖关系如下。

![image-20230719125823204](.\imgs\image-20230719125823204.png)

### Docker Swarm自带网络

Docker Swarm在启动时自己会创建一些网络，然后利用它们实现容器之间的通信与负载均衡等功能。

```
$ docker network ls
NETWORK ID          NAME                DRIVER              SCOPE
cac91f9c60ff        bridge              bridge              local
b55339bbfab9        docker_gwbridge     bridge              local
fe6ef5d2e8e8        host                host                local
f1nvcluv1xnf        ingress             overlay             swarm
8vty8k3pejm5        net1                overlay             swarm
893a1bbe3118        none                null                local
```

- **docker_gwbridge**：通过这个网络，容器可以连接到宿主机。
- **ingress：**这个网络用于将服务暴露给外部访问，docker swarm就是通过它实现的routing mesh（将外部请求路由到不同主机的容器）。

### 同节点容器通信方式

我们以节点1为例，它上面运行着两个服务如下

```
$ docker ps
CONTAINER ID        IMAGE                COMMAND                  CREATED             STATUS              PORTS               NAMES
eb03383913fb        nvbeta/node:latest   "nodemon /src/index.j"   2 hours ago         Up 2 hours          8888/tcp            node.1.10yscmxtoymkvs3bdd4z678w4
434ce2679482        redis:latest         "docker-entrypoint.sh"   2 hours ago         Up 2 hours          6379/tcp            redis.1.1a2l4qmvg887xjpfklp4d6n7y
```

由于所有服务都加入了我们创建的net1网络，那么每个服务必然存在一个连接到net1的接口。通过创建一个到docker的netns目录的软链可以查看到节点1上的所有namespace，如下

```
$ cd /var/run
$ sudo ln -s /var/run/docker/netns netns
$ sudo ip netns
be663feced43
6e9de12ede80
2-8vty8k3pej
1-f1nvcluv1x
72df0265d4af
```

通过对比namespace的名称与netwok的名称，我们猜测命名空间2-8vty8k3pej是给net1网络用的，因为它的ID是8vty8k3pej。我们可以通过查看这个命名空间的接口与这个节点上的容器的接口来验证这一点，首先看看两个服务的容器的接口列表

```
$ docker exec node.1.10yscmxtoymkvs3bdd4z678w4 ip link
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN mode DEFAULT group default
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
11040: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1450 qdisc noqueue state UP mode DEFAULT group default
    link/ether 02:42:65:00:00:03 brd ff:ff:ff:ff:ff:ff
11042: eth1: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UP mode DEFAULT group default
    link/ether 02:42:ac:12:00:04 brd ff:ff:ff:ff:ff:ff
---------------------------------------------------------------------------------------------------
$ docker exec redis.1.1a2l4qmvg887xjpfklp4d6n7y ip link
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN mode DEFAULT group default
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
11036: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1450 qdisc noqueue state UP mode DEFAULT group default
    link/ether 02:42:65:00:00:08 brd ff:ff:ff:ff:ff:ff
11038: eth1: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UP mode DEFAULT group default
    link/ether 02:42:ac:12:00:03 brd ff:ff:ff:ff:ff:ff
```

再看看命名空间的命名列表

```
$ sudo ip netns exec 2-8vty8k3pej ip link
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN mode DEFAULT group default
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
2: br0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1450 qdisc noqueue state UP mode DEFAULT group default
    link/ether 22:37:32:66:b0:48 brd ff:ff:ff:ff:ff:ff
11035: vxlan1: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1450 qdisc noqueue master br0 state UNKNOWN mode DEFAULT group default
    link/ether 2a:30:95:63:af:75 brd ff:ff:ff:ff:ff:ff
11037: veth2: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1450 qdisc noqueue master br0 state UP mode DEFAULT group default
    link/ether da:84:44:5c:91:ce brd ff:ff:ff:ff:ff:ff
11041: veth3: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1450 qdisc noqueue master br0 state UP mode DEFAULT group default
    link/ether 8a:f9:bf:c1:ec:09 brd ff:ff:ff:ff:ff:ff
```

其中br0表示Linux网桥，所有接口都会连接到它上面。docker为每个容器创建Veth设备对的逻辑是：

*位于容器内部一段的设备ID比它连接的另一端的ID小1*

所以该命名空间中veth2（11037）连接的是redis容器的eth0（11036），veth3（11041）连接的是node容器的eth0（11040）。因此节点1内部容器间的通信方式是通过直接连接到net1实现的。

```
      node 1

  +-----------+      +-----------+
  |  nodejs   |      |   redis   |
  |           |      |           |
  +--------+--+      +--------+--+
           |                  |
           |                  |
           |                  |
      +----+------------------+-------+ net1
       101.0.0.3          101.0.0.8
       101.0.0.4(vip)     101.0.0.2(vip)
```

### 容器与宿主机的通信方式

我们看看宿主机的接口列表

```
$ ip link
...
4: docker_gwbridge: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UP mode DEFAULT group default
    link/ether 02:42:24:f1:af:e8 brd ff:ff:ff:ff:ff:ff
5: docker0: <NO-CARRIER,BROADCAST,MULTICAST,UP> mtu 1500 qdisc noqueue state DOWN mode DEFAULT group default
    link/ether 02:42:e4:56:7e:9a brd ff:ff:ff:ff:ff:ff
11039: veth97d586b: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue master docker_gwbridge state UP mode DEFAULT group default
    link/ether 02:6b:d4:fc:8a:8a brd ff:ff:ff:ff:ff:ff
11043: vethefdaa0d: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue master docker_gwbridge state UP mode DEFAULT group default
    link/ether 0a:d5:ac:22:e7:5c brd ff:ff:ff:ff:ff:ff
10876: vethceaaebe: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue master docker_gwbridge state UP mode DEFAULT group default
    link/ether 3a:77:3d:cc:1b:45 brd ff:ff:ff:ff:ff:ff
...
```

可以发现宿主机上的veth97d586b (11039)连接到了redis容器上的 eth1 (11038)，vethefdaa0d (11043) 连接到了node容器上的 eth1 (11042) 。而这两个接口都位于docker_gwbridge网络（网桥）。

```text
$ brctl show
bridge name            bridge id                      STP enabled            interfaces
docker0                8000.0242e4567e9a              no
docker_gwbridge        8000.024224f1afe8              no                     veth97d586b
                                                                             vethceaaebe
                                                                             vethefdaa0d
```

这个docker_gwbridge有点类似于单机版Docker中的docker0网桥，每个容器都会肢接到上面，并且可以被外部访问。但不同的是docker_gwbridge并没有连接到外网，外部无法访问。

```
    node 1

  172.18.0.4         172.18.0.3
 +----+------------------+----------------+ docker_gwbridge
      |                  |
      |                  |
      |                  |
   +--+--------+      +--+--------+
   |  nodejs   |      |   redis   |
   |           |      |           |
   +--------+--+      +--------+--+
            |                  |
            |                  |
            |                  |
       +----+------------------+----------+ net1
        101.0.0.3          101.0.0.8
        101.0.0.4(vip)     101.0.0.2(vip)
```

### 如何被外部访问

我们再看看节点1上的命名空间列表与网络列表，很显然1-f1nvcluv1xis 是ingress网络的命名空间，但72df0265d4af是啥了？

```
$ sudo ip netns
be663feced43
6e9de12ede80
2-8vty8k3pej
1-f1nvcluv1x
72df0265d4af

$ docker network ls
NETWORK ID          NAME                DRIVER              SCOPE
cac91f9c60ff        bridge              bridge              local
b55339bbfab9        docker_gwbridge     bridge              local
fe6ef5d2e8e8        host                host                local
f1nvcluv1xnf        ingress             overlay             swarm
8vty8k3pejm5        net1                overlay             swarm
893a1bbe3118        none                null                local
```

我们查看下它的接口列表

```
$ sudo ip netns exec 72df0265d4af ip addr
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
    inet6 ::1/128 scope host
       valid_lft forever preferred_lft forever
10873: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1450 qdisc noqueue state UP group default
    link/ether 02:42:0a:ff:00:03 brd ff:ff:ff:ff:ff:ff
    inet 10.255.0.3/16 scope global eth0
       valid_lft forever preferred_lft forever
    inet6 fe80::42:aff:feff:3/64 scope link
       valid_lft forever preferred_lft forever
10875: eth1: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UP group default
    link/ether 02:42:ac:12:00:02 brd ff:ff:ff:ff:ff:ff
    inet 172.18.0.2/16 scope global eth1
       valid_lft forever preferred_lft forever
    inet6 fe80::42:acff:fe12:2/64 scope link
       valid_lft forever preferred_lft forever
```

eth1(10875) 连接到了宿主机上的vethceaaebe(10876)。那么eth0连接到了哪里了？我们看下节点1上的ingress网络与docker_gwbridge网络。

```
$ docker network inspect ingress
[
    {
        "Name": "ingress",
        "Id": "f1nvcluv1xnfa0t2lca52w69w",
        "Scope": "swarm",
        "Driver": "overlay",
        ....
        "Containers": {
            "ingress-sbox": {
                "Name": "ingress-endpoint",
                "EndpointID": "3d48dc8b3e960a595e52b256e565a3e71ea035bb5e77ae4d4d1c56cab50ee112",
                "MacAddress": "02:42:0a:ff:00:03",
                "IPv4Address": "10.255.0.3/16",
                "IPv6Address": ""
            }
        },
        ....
    }
]

$ docker network inspect docker_gwbridge
[
    {
        "Name": "docker_gwbridge",
        "Id": "b55339bbfab9bdad4ae51f116b028ad7188534cb05936bab973dceae8b78047d",
        "Scope": "local",
        "Driver": "bridge",
        ....
        "Containers": {
            ....
            "ingress-sbox": {
                "Name": "gateway_ingress-sbox",
                "EndpointID": "0b961253ec65349977daa3f84f079ec5e386fa0ae2e6dd80176513e7d4a8b2c3",
                "MacAddress": "02:42:ac:12:00:02",
                "IPv4Address": "172.18.0.2/16",
                "IPv6Address": ""
            }
        },
        ....
    }
]
```

它们的MAC/IP地址与命名空间72df0265d4af中的接口的MAC/IP一致，这个命名空间是一个隐藏的容器"ingress-sbox"的，它一边肢接到了宿主机的网络，另一边肢接到了ingress网络。

### Routing Mesh原理

Docker Swarm具有一项神奇功能叫做“routing mesh” ，对于暴露了端口的服务，无论这个服务布署在哪台机器，地可以从集群中任意一台机器通过该端口访问它。

这里以ngix服务为例，它布署在节点2，并将容器的80端口映射到了节点的1080端口。我们看看节点1上的网络配置

```
$ sudo iptables -t nat -nvL
...
...
Chain DOCKER-INGRESS (2 references)
 pkts bytes target     prot opt in     out     source               destination
    0     0 DNAT       tcp  --  *      *       0.0.0.0/0            0.0.0.0/0            tcp dpt:1080 to:172.18.0.2:1080
 176K   11M RETURN     all  --  *      *       0.0.0.0/0            0.0.0.0/0

$ sudo ip netns exec 72df0265d4af iptables -nvL -t nat
...
...
Chain PREROUTING (policy ACCEPT 0 packets, 0 bytes)
 pkts bytes target     prot opt in     out     source               destination
    9   576 REDIRECT   tcp  --  *      *       0.0.0.0/0            0.0.0.0/0            tcp dpt:1080 redir ports 80
...
...
Chain POSTROUTING (policy ACCEPT 0 packets, 0 bytes)
 pkts bytes target     prot opt in     out     source               destination
    0     0 DOCKER_POSTROUTING  all  --  *      *       0.0.0.0/0            127.0.0.11
   14   896 SNAT       all  --  *      *       0.0.0.0/0            10.255.0.0/16        ipvs to:10.255.0.3
```

可以看出，在隐藏的ingress-sbox容器中，iptables将来自1080端口的请求重定向到了80 端口，然后POSTROUTING链路将数据包发到10.255.0.3, 这是ingress网络上的接口的IP。

注意SNAT规则中的“ipvs”，它是Linux内核中自带的负载均衡器。

```
$ sudo ip netns exec 72df0265d4af iptables -nvL -t mangle
Chain PREROUTING (policy ACCEPT 144 packets, 12119 bytes)
 pkts bytes target     prot opt in     out     source               destination
   87  5874 MARK       tcp  --  *      *       0.0.0.0/0            0.0.0.0/0            tcp dpt:1080 MARK set 0x12c
...
...
Chain OUTPUT (policy ACCEPT 15 packets, 936 bytes)
 pkts bytes target     prot opt in     out     source               destination
    0     0 MARK       all  --  *      *       0.0.0.0/0            10.255.0.2           MARK set 0x12c
...
...
```

在iptables路由表中，将数据流标记为 0x12c (= 300)，而这里“ipvs”的胚子如下：

```
$ sudo ip netns exec 72df0265d4af ipvsadm -ln
IP Virtual Server version 1.2.1 (size=4096)
Prot LocalAddress:Port Scheduler Flags
  -> RemoteAddress:Port           Forward Weight ActiveConn InActConn
FWM  300 rr
  -> 10.255.0.5:0                 Masq    1      0          0
```

其中10.255.0.5是节点2上nginx服务的容器的IP。

### 结论

在docker swarm中的网络结构如下。

![img](D:\www\learning\caioo0.github.io\note-coding\docs\容器化\imgs\v2-0768daac56f8c22cd46de8b73b316c65_r.jpg)

```

```

