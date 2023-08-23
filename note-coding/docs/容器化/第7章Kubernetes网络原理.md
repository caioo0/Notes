# 第7章 kubernetes 网络原理

## pod连接主机

对于刚接触k8s的人来说，最令人懵逼的应该就是k8s的网络了，如何访问部署在k8s的应用，service的几种类型有什么区别，各有什么使用场景，服务的负载均衡是如何实现的，与haproxy/nginx转发有什么区别，网络策略为什么不用限制serviceIP等等

本文将站在一个初入者的角度，采用一边讲解一边实践的方式把k8s的网络相关的原理慢慢剖析清楚，并且用普通的linux命令把pod/serviceIP/nodePort等场景都模拟出来；

本文比较适合刚接触k8s，对docker有一些了解，有一定计算机基础的童鞋，在浏览本文时，各位童鞋可以准备个centos7.6的环境，安装docker和iproute2工具包，一边看一边操作，加深理解。

OK，走起！

## 一些关于linux网络的知识

在开始之前，有一些关于linux网络的知识你需要先知道，就像做数学题之前，先得理解公式一样。

### 每当linux需要向外发送一个数据包时，总是会执行以下步骤：

1. 查找到该数据包的目的地的路由信息，如果是直连路由（不知道什么是直连路由？没关系，后面会解释），则在邻居表中查找该目的地的MAC地址
2. 如果非直连路由，则在邻居表中找下一跳的MAC地址
3. 如果找不到对应的路由，则报“network is unreachable”
4. 如果在邻居表中没有查找到相应的MAC信息，则向外发送ARP请求询问
5. 发送出去的数据帧，源MAC地址为发送网卡的MAC地址，目标MAC则是下一跳的MAC，只要不经过NAT，那么源目地IP是全程不会变化的，而MAC地址则每一跳都会变化

### 每当linux收到一个数据帧时，总会执行以下步骤：

1. 如果数据帧目标MAC地址不是收包网卡的MAC，也不是ff:ff:ff:ff:ff:ff（ARP广播），且网卡未开启混杂模式，则拒绝收包；

2. 如果数据帧目标MAC为ff:ff:ff:ff:ff:ff，则进入arp请求处理流程；

3. 如果数据帧目标MAC地址是收包网卡的MAC，且是IP包，则：

4. 1. 目标IP地址在本机，则上送到上一层协议继续处理；
   2. 目标IP地址不在本机，则看net.ipv4.ip_forward是否为1，如果为1，则查找目标IP的路由信息，进行转发；
   3. 目标IP地址不在本机，且net.ipv4.ip_forward为0，则丢弃

### 一些常用的命令

```bash
ip link ##查看网卡信息
ip addr ##查看网卡IP地址
ip route ##查看路由信息
ip neigh ##查看邻居表信息

##上面的命令均可简化，就是第二个单词的首字母，例如ip link可以简化为ip l，ip addr可以简化为ip a，以此类推……

iptables-save ##查看所有iptables规则
```

**然后，我们就正式开始了，因为k8s的网络主要都是要解决怎么访问pod和pod怎么访问外面的问题，所以先来了解一下什么是pod**

## pod是什么

现在的服务器一般配置都比较高，64核256G的配置，如果一台服务器只用来跑一个java程序，显然就太浪费了，如果想资源利用率高一些，可以用qemu-kvm或vmware等软件进行虚拟化，让多个java进程分别运行在虚拟机里，这样可以相互不受影响；

但虚拟化难免会带来一些资源损耗，而且要先拉起一台虚拟机再在里面启动一个java进程也会比直接在裸金属服务器上启动一个java进程要耗费更多的时间，只是从运行几个java进程的角度来说，虚拟化并非资源利用的最优解；

如果不用虚拟化，直接同时在裸金属服务上运行多个java进程，就要解决各个进程CPU内存资源占用、端口冲突、文件系统冲突等几个问题，否则就会出现：

- 一个进程消耗了大量的内存和CPU，而另一个更重要的进程却得不到资源；
- 80端口只有一个，进程A用了，进程B就用不了
- 多个进程同时操作相同的目录或读写相同的文件，造成异常

因为需要让多个进程都能高效地相互不受影响地运行，所以容器技术出现了，其中又以docker最为流行，容器解决了多进程间的环境隔离：

- 资源隔离，使用linux control group（简称：cgroup）解决各进程cpu和内存、io的资源分配问题
- 网络隔离，使用linux network namespace（***下面开始简称：ns\***）让各个进程运行在独立的网络命名空间，使各类网络资源相互隔离（网卡、端口、防火墙规则、路由规则等）
- 文件系统隔离，使用union fs，例如：overlay2/aufs等，让各个进程运行在独立的根文件系统中

**而所谓的pod，就是共享一个ns的多个容器**

但是，什么叫“共享一个ns的多个容器”？

每当我们用docker运行一个容器，默认情况下，会给这个新的容器创建一个独立的ns，多个容器间相互访问只能使用对方IP地址

```bash
docker run -itd --name=pause busybox
docker run --name=nginx -d nginx
```

此时要在pause中访问nginx，先查找一下nginx容器的IP地址：

```bash
docker inspect nginx|grep IPAddress

"IPAddress": "172.17.0.8",
```

然后在pause容器中用刚查到的IP访问：

```bash
docker exec -it pause curl 172.17.0.8

<!DOCTYPE html>
<html>
<head>
<title>Welcome to nginx!</title>
....
</body>
</html>
```

但其实是可以让nginx容器加入pause容器的ns，用下面的命令可以模拟：

```bash
docker run -itd --name=pause busybox
docker run --name=nginx --network=container:pause -d nginx
```

此时pause容器和nginx容器在相同的ns中，相互间就可以用localhost访问对方了，可以用下面的命令验证：

```bash
docker exec -it pause curl localhost

<!DOCTYPE html>
<html>
<head>
<title>Welcome to nginx!</title>
....
</body>
</html>
```

pause容器和nginx容器就是“共享一个ns的两个容器”，所以，pause容器和nginx容器加起来，就是k8s的pod

> 在k8s集群的节点中使用docker ps，总是会发现一堆名为pause的容器，就是这个原因，pause是为多个业务容器提供共享的ns的

可以用下面的命令进入之前用docker创建的pause容器的ns

先获取pause容器的pid

```bash
docker inspect pause|grep Pid

            "Pid": 3083138,
```

用`nsenter`命令进入指定pid的ns

```bash
nsenter --net=/proc/3083138/ns/net
```

此时我们已经在pause容器的ns中了，可以查看该ns的网卡，路由表，邻居表等信息

```bash
ip addr show 

1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
605: eth0@if606: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UP group default
    link/ether 02:42:ac:11:00:02 brd ff:ff:ff:ff:ff:ff link-netnsid 0
    inet 172.17.0.7/16 brd 172.17.255.255 scope global eth0
       valid_lft forever preferred_lft forever
ip route

default via 172.17.0.1 dev eth0
172.17.0.0/16 dev eth0 proto kernel scope link src 172.17.0.2
```

从网络的角度看，一个pod就是一个独立的ns，解决了ns的网络进出问题，就解决了pod的网络问题，所以下面的讨论就都以ns为主，不再频繁创建docker容器，后面的描述不管是pod还是ns，请统一理解为ns就好

## 认识ns

对于一台linux主机来说，影响网络方面的配置主要有以下几个：

- 网卡：启动时初始化，后期可以添加虚拟设备；
- 端口：1到65535，所有进程共用
- iptables规则：配置进出主机的防火墙策略和NAT规则
- 路由表：到目标地址的路由信息
- 邻居表：与主机在同个二层网络（什么是同个二层网络？大概可以理解为在一台交换机上，彼此之间通过ARP找到对方的）的其它主机的MAC地址与IP地址的映射关系

对于每一个ns来说，这几个配置都是独立的，所以从网络的角度来说，当你创建一个新的ns，其实就相当于拥有了一台新的主机

用下面的命令创建新的ns

```bash
ip netns add ns1 
```

然后我们可以用`ip netns exec ns1`为前缀来执行命令，这样显示的结果就都是ns1的网络相关配置：

```bash
ip netns exec ns1 ip link show

1: lo: <LOOPBACK> mtu 65536 qdisc noop state DOWN mode DEFAULT group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
```

可以看到，我们用ip命令创建的ns除了一张lo网卡外，其它都是空白，这样一来她里面运行的程序访问不了外面，外面也找不到她，需要我们一点点地去组织，这就是k8s的cni要做的事情

> 上面我们用docker启动的容器中，网卡，IP，路由都是docker网络管理（cnm）给组织好的，从单节点的网络管理来看，cni和cnm做的事情还是挺像的

下面我们就一步步来完成k8s的cni做的事情，第一步是让主机和pod能相互访问

## 主机与pod相互访问

首先给ns1增加一张与主机连接的网卡，这里会用到linux虚拟网络设备veth网卡对，对于veth，基本上可以理解为中间连着线的两张网卡，一端发送会触发另一端接收，用下面的命令创建：

```bash
ip link add ns1-eth0 type veth peer name veth-ns1  ## 增加一对veth网卡，名为ns1-eth0和veth-ns1
ip link set ns1-eth0 netns ns1  ## 其中一端挪到刚才创建的ns1中，另一端留在主机端，这样主机和ns就连接起来了
ip link set veth-ns1 up ##启动主机端的网卡veth-ns1
ip netns exec ns1 ip addr add 172.20.1.10/24 dev ns1-eth0  ##此时ns1-eth0已经在ns1中了，所以要进去ns1中去执行命令设置网卡IP
ip netns exec ns1 ip link set ns1-eth0 up ##启动ns1端的网卡ns1-eth0
```

笔者使用的主机的IP是192.168.6.160，此时尝试从ns1中ping主机，能通了吗？

```bash
ip netns exec ns1 ping 192.168.6.160

connect: Network is unreachable
```

ping不通主机，此时的情况就是上面提到的linux知识点中关于发送数据包的第3点，因为没有到目的地的路由，ns1不知如何去192.168.6.160，在这里我们要给ns1增加一条默认路由：

```bash
ip netns exec ns1 ip route add default via 172.20.1.1 dev ns1-eth0
```

去看一下ns1中的路由表，已经有两条路由信息

```bash
ip netns exec ns1 ip route

default via 172.20.1.1 dev ns1-eth0  ##这是一条非直连路由，意思是默认流量走ns1-eth0网卡，下一跳为172.20.1.1
172.20.1.0/24 dev ns1-eth0 proto kernel scope link src 172.20.1.10  ## 这是一条直连路由，没有via的就是直连路由，这是我们给网卡设置IP时系统自动增加的
```

此时能通了吗？

```bash
ip netns exec ns1 ping 192.168.6.160

PING 192.168.6.160 (192.168.6.160) 56(84) bytes of data.
```

还是不行，定在那里半天没反应，又卡在哪了呢？还是linux知识点中关于发送数据包的第2点，如果是非直连路由，会先去拿下一跳的MAC地址，下一跳是172.20.1.1，能获取到它的MAC地址吗？用下面的命令查一下邻居表：

```bash
ip netns exec ns1 ip neigh

172.20.1.1 dev ns1-eth0  FAILED
```

很明显，获取不到，因为网关IP地址确实是个不存在的地址，但其实这个地址不需要是个存在的地址（所以你会看到在calico中，容器的默认网关是个168.254开头的地址），因为这个地址其实是用不到的，网关的IP是不会出现在pod发送的数据包中的，真正需要用到的是网关的mac地址，我们的目的是要得到主机端veth-ns1的mac地址，有两个方法：

- 设置对端的网卡的arp代答，ns1-eth0的对端是主机上的veth-ns1网卡

```bash
echo 1 > /proc/sys/net/ipv4/conf/veth-ns1/proxy_arp ##这样就开启了veth-ns1的arp代答，只要收到arp请求，不管目标IP是什么，veth-ns1网卡都会把自己MAC地址回复回去
```

- 把网关地址设置在对端的网卡上

这里我们用第一个方法，设置完成后再查一下邻居表：

```bash
ip netns exec ns1 ip neigh

172.20.1.1 dev ns1-eth0 lladdr b6:58:7b:0e:35:b3 REACHABLE
```

可以看到，已经拿到网关的MAC地址了，这个地址也确实就是主机端veth-ns1的地址：

```bash
ip link show veth-ns1
607: veth-ns1@if608: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UP mode DEFAULT group default qlen 1000
    link/ether b6:58:7b:0e:35:b3 brd ff:ff:ff:ff:ff:ff link-netns ns1
```

这下总该行了吧？兴高采烈地ping一下，发现依旧不行

oh shit!!

什么垃圾！！

入门到放弃！！！

先别急着崩溃，主机委屈说：数据包我收到了，只是我不知道怎么回给你，因为我这里没有到172.20.1.10的路由，所以我就把回包给了我的默认网关，于是数据包就飞了……

坚持住，只需最后一步，在主机上添加到pod的直联路由

```bash
ip route add 172.20.1.10 dev veth-ns1  ## 这也是一条直连路由，注意是添加主机的路由，所以不用ip netns exec ns1开头了
```

此时从ns1中ping主机：

```bash
ip netns exec ns1 ping -c 5 192.168.6.160

PING 192.168.6.160 (192.168.6.160) 56(84) bytes of data.
64 bytes from 192.168.6.160: icmp_seq=1 ttl=64 time=0.025 ms
64 bytes from 192.168.6.160: icmp_seq=2 ttl=64 time=0.017 ms
64 bytes from 192.168.6.160: icmp_seq=3 ttl=64 time=0.015 ms
64 bytes from 192.168.6.160: icmp_seq=4 ttl=64 time=0.017 ms
64 bytes from 192.168.6.160: icmp_seq=5 ttl=64 time=0.017 ms
--- 192.168.6.160 ping statistics ---
5 packets transmitted, 5 received, 0% packet loss, time 135ms
rtt min/avg/max/mdev = 0.015/0.018/0.025/0.004 ms
```

从主机ping ns1

```bash
ping -c 5 172.20.1.10

PING 172.20.1.10 (172.20.1.10) 56(84) bytes of data.
64 bytes from 172.20.1.10: icmp_seq=1 ttl=64 time=0.026 ms
64 bytes from 172.20.1.10: icmp_seq=2 ttl=64 time=0.015 ms
64 bytes from 172.20.1.10: icmp_seq=3 ttl=64 time=0.016 ms
64 bytes from 172.20.1.10: icmp_seq=4 ttl=64 time=0.015 ms
64 bytes from 172.20.1.10: icmp_seq=5 ttl=64 time=0.016 ms
--- 172.20.1.10 ping statistics ---
5 packets transmitted, 5 received, 0% packet loss, time 138ms
rtt min/avg/max/mdev = 0.015/0.017/0.026/0.006 ms
```

OK，成功完成第一步，pod与主机互通，此时在pod里能访问百度吗？

答案是不行，172.20.1.10这个地址，是我们随便模拟出来的，除了当前这台主机谁也不认识，所以如果他要访问外网，需要做源地址转换，这个场景跟我们办公室的PC上外网原理是一样的，当你的电脑去访问百度时，源地址肯定不是你网卡上的地址，而是你的办公网络出外网的出口IP加一个随机端口，这个源地址转换是你的出口路由器自动帮你完成的，我们在主机上也要配置针对刚才创建的pod的源地址转换规则

## pod访问外网

- 首先第一步要打开本机的ip转发功能

```bash
echo 1 > /proc/sys/net/ipv4/ip_forward
```

- 然后是设置snat规则

```bash
iptables -A POSTROUTING -t nat -s 172.20.1.10 -j MASQUERADE
```

此时再试一下已经要以ping通百度

```bash
ip netns exec ns1 ping -c 5 www.baidu.com

PING www.a.shifen.com (14.215.177.38) 56(84) bytes of data.
64 bytes from 14.215.177.38 (14.215.177.38): icmp_seq=1 ttl=54 time=9.47 ms
64 bytes from 14.215.177.38 (14.215.177.38): icmp_seq=2 ttl=54 time=9.42 ms
64 bytes from 14.215.177.38 (14.215.177.38): icmp_seq=3 ttl=54 time=9.42 ms
64 bytes from 14.215.177.38 (14.215.177.38): icmp_seq=4 ttl=54 time=9.33 ms
64 bytes from 14.215.177.38 (14.215.177.38): icmp_seq=5 ttl=54 time=9.58 ms
--- www.a.shifen.com ping statistics ---
5 packets transmitted, 5 received, 0% packet loss, time 9ms
rtt min/avg/max/mdev = 9.332/9.443/9.582/0.102 ms
```

至于上面的iptables规则和为何要开启转发，下一章解释serviceIP时再详细介绍。

## service原理

上一篇文章中我们介绍了pod与主机互通及pod访问外网的原理，在这一章我们将介绍pod与pod的相互访问以及外部服务访问pod的方式，由此引出k8s的service的几种类型、使用场景和相关的实现原理。

> 本文将继续沿用上一章的习惯，用linux network namespace（下面简称ns）来代表pod，注意我们说的pod就特指是hostNetwork为false的pod

我们将在一个节点模拟创建几个pod,用iptables的方式模拟实现clusterIP和nodeport。

开始之前，我们还是先上关于阅读本章内容需要掌握的linux网络知识。

## netfilter

linux收发包流程是一个贼复杂的过程，为了让用户可以在收发包的过程中对数据包进行修改或过滤，linux从2.4版本开始引入了netfilter子系统，在收发包的数据路径中的关键节点上提供扩展（hook）点，这些扩展点上可以编写扩展函数对数据包进行过滤和修改，扩展点一共有五个点，主要有：

- `PREROUTING`，数据包刚到达时会经过这个点，通常用来完成DNAT的功能。
- `INPUT`，数据包要进入本机的传输层时会经过这个点，通常用来完成防火墙入站检测。
- `FORWARD`，数据包要通过本机转发时会经过这个点，通常用来完成防火墙转发过滤。
- `OUTPUT`，从本机的数据包要出去的时候会经过这个点，通常用来做DNAT和防火墙出站检测。
- `POSTROUTING`，数据包离开本机前会经过这个点，通常用来做SNAT。

![img](https://pic4.zhimg.com/80/v2-31548b6762793b952b8adc2bc4239a1f_1440w.webp)

图一：netfilter

为什么要了解这个netfilter呢？因为k8s的serviceIP实现（无论是iptables和ipvs）、NetworkPolicy的实现都与这个netfilter的流程息息相关，对于netfilter需要get到几个关键的流程：

- 主机的应用程序接收外部的数据包会经过的点：PREROUTING -> INPUT

![img](https://pic4.zhimg.com/80/v2-101d03810e39facffa05f06961a52903_1440w.webp)

图2:主机应用程序接收包流程

- 主机的应用程序发送数据包到外部会经过的点：OUTPUT -> POSTROUTING

![img](https://pic1.zhimg.com/80/v2-79ce8f7b1f50f14c34759e8dcb019b2c_1440w.webp)

图3:主机应用程序发送包流程

- 主机上的pod发送的数据包去外部或去主机的另一个pod：PREROUTING -> FORWARD -> POSTROUTING

![img](https://pic2.zhimg.com/80/v2-db0e9b78412691df8879cd35db36288d_1440w.webp)

图4:主机上的pod发送数据去外部或主机的另一个pod的流程

> 主机上运行的pod虽然也是主机上的一个进程，但pod发送数据包出去的流程却和主机的其它进程不一样，这个点刚开始笔者也曾经困惑过，因为pod在新的ns中，所以它的发包流程是和主机收到另一台主机的数据然后转发的流程一样的；

- 另外注意图中的IPIsLocal点，会判断数据包的目标IP是否为本机IP，如果是，则往INPUT点走；当IP不是本机IP，就会看net.ipv4.ip_forward是否为1,是则继续走朝FORWARD走，为0则丢弃，所以要设置为1才能为主机上的pod提供流量转发功能；

掌握这几个流程对于我们后面使用iptables及理解k8s的service的实现很有帮助，下面的内容我们会多次用到这几个流程

虽然linux为我们预留了5个扩展点，但编写扩展函数的难度贼大，需要了解很多上下文，随便一个错误就会让主机蓝屏死机什么的，贼刺激，所以我们要找个更容易使用的工具，iptables就是这个工具，它在netfilter子系统的扩展点上已经实现了对数据包的匹配和修改，然后提供命令行让用户可以轻松地制定规则，我们只需要告诉它怎么匹配和把包修改成什么就行了，有了iptables，数据包的拦截与修改就变得容易了。

## iptables

大多数linux发行版都默认集成了iptables，先通过一个简单的iptables命令来了解一下：

```bash
iptables -A INPUT -t filter -s 192.168.1.10 -j DROP
```

上面的命令是一条防火墙入站规则，意思是指不允许来源为192.168.1.10的IP访问本机的服务；

我们来详细解释下上面的命令，iptables是命令的固定前缀

- `-A` 是指后面追加一条规则，其它：

- - `-I`是前面插入规则，优先级更高
  - `-D`是删除规则
  - `-N`是新增加链
  - `-F`清除链上的所有规则或所有链
  - `-X`删除一条用户自定义链
  - `-P`更改链的默认策略
  - `-L`展示指定的链上的规则

- `INPUT`是iptables链的名称，指示当前规则工作在哪个netfilter的扩展点，iptables有五条固定的链，与netfilter子系统的扩展点一一对应，分别是：INPUT、OUTPUT、PREROUTING、FORWARD、POSTROUTING；根据上面对netfilter的扩展点的功能解释，防火墙规则一般只工作在INPUT/OUTPUT/FORWARD三个扩展点，而我们是要限制访问本机运行的服务，而INPUT点专门负责入站检测规则，所以选择了INPUT点；所以说我们要先了解netfilter子系统的五个点才能更好地使用iptables；

- `-t`指定当前命令操作所属的表，主要有：

- - filter表，主要用于拦截或放行，不修改包；如果不指定，则默认为filter表
  - nat表，主要用于修改IP包的源/目标地址
  - mangle表，主要用于给数据包打标记
  - raw表，没用过不知道干什么的哈哈
  - security表，没用过

- `-s`是数据包的匹配规则，配置规则可以一个或多个，多个是与的效果，这里`-s`是匹配来源IP的意思，还有其它：

- - `-d`是匹配目标IP
  - `--sport`是匹配来源端口
  - `--dport`是匹配目标端口
  - `-p tcp`是匹配协议类型

- `-j DROP`是执行的动作，这里是跳转到`DROP`链，iptables有几个预定义的链：

- - `DROP`丢弃进入该链的包
  - `ACCEPT`接受进入该链的包
  - `RETURN`返回上一级链
  - `SNAT`源地址转换，要指定转换后的源地址，下面会有示例
  - `DNAT`目标地址转换，要指定转换后目标地址
  - `MASQUERADE`对进入该链的包进行源地址转换，与SNAT类似，但不用指定具体的转换后的源地址，会自动应用发送网卡的地址作为源地址，通常都用这条链完成SNAT

再来看几个iptables的命令：

- 把本机应用发往10.96.0.100的数据包的目标地址换成10.244.3.10上，注意是要影响本机应用，所以用的是OUTPUT链（注意图3），clusterIP主要就是使用下面的这条规则完成：

```bash
iptables -A OUTPUT -t nat -d 10.96.0.100 -j DNAT --to-distination 10.244.3.10
```

- 上面的规则只对本机的应用程序发送的流量有影响，对于本机的pod发出的流量没有影响，如果要影响本机的pod，还要再加一条，规则都一样，就是工作在PREROUTING链（注意图4）：

```bash
iptables -A PREROUTING -t nat -d 10.96.0.100 -j DNAT --to-distination 10.244.3.10
```

- 对本机发送的数据包中来源IP为172.20.1.10的数据包进行源地址伪装，注意修改源地址只有一个点可以用，就是POSTROUTING，下面的规则就是配置pod上外网时使用的：

```bash
iptables -A POSTROUTING -t nat -s 172.20.1.10 -j MASQUERADE
```

- 允许来源IP为192.168.6.166并访问本机的TCP80端口：

```bash
iptables -A INPUT -t filter -s 192.168.8.166 -p tcp --dport 80 -j ACCEPT
```

为了使数据包能够尽量正常地处理与转发，iptables上的规则创建会有一些限制，例如我们不能在POSTROUTING链上创建DNAT的规则，因为在POSTROUTING之前，数据包要进行路由判决，内核会根据当前的目的地选择一个最合适的出口，而POSTROUTING链的规则是在路由判决后发生，在这里再修改数据包的目的地，会造成数据包不可到达的后果，所以当我们用iptables执行如下命令时：

```bash
iptables -A POSTROUTING -t nat -d 192.168.8.163 -j DNAT --to-distination 192.168.8.162

iptables:Invalid argument. Run `dmesg` for more information.

##执行dmesg命令会看到iptables提示：DNAT模块只能在PREROUTING或OUTPUT链中使用
##x_tables:iptables:DNAT target:used from hooks POSTROUTING,but only usable from PREROUTING/OUTPUT
```

简单了解iptables后，我们再来看看为什么k8s会设计service这个东西。

## 为什么k8s会设计service

主要是因为下面两个原因：

- pod的特性是快速创建快速销毁，所以pod的IP是不固定的，要让调用方有个固定依赖，所以需要一个VIP出来代表一个服务

> pod的IP为什么不固定？一般的cni给pod分配IP时都是一个集群节点占用一个24位子网（就是NODE-CIDR，通常我们会在安装k8s集群时指定一个POD-CIDR，例如：10.244.0.0/16，然后k8s会给每一个集群节点分配一个24位的子网，例如：10.244.2.0/24，然后所有10.244.2开头的POD都是在这个节点上运行的），podIP固定就意味着pod必须在一个固定的k8s集群节点，如果那个节点挂了，那pod就永远起不来了，这与k8s的设计相悖，k8s是要应用不要依赖具体的硬件资源；
> 当然也不是说pod的IP就一定不能固定，这要看具体的cni而言，比如flannel就是上面说的那种情况，但也有能实现的，比如我们的mustang，就实现了有状态应用的固定IP（广告一波：）

- 一般来说为了追求应用的高可用，一个应用会部署多个pod，这时需要一个VIP充当多个pod的流量负载均衡器

## service的几种类型分别有什么使用场景

- ***clusterIP\***：只能在集群的节点和pod中访问，解决的就是集群内应用间的相互访问的问题；
- ***nodeport\***：通过节点的地址和端口把pod暴露到集群外，让集群外的应用能访问集群内的应用，设置服务类型为nodeport时，是在clusterIP的基础上再给节点开个端口转发（是特定节点还是每一个节点要看externalTrafficPolicy的值，Cluster是每一个节点都开，Local是只在pod运行的节点开），所以nodeport的服务也会有一个clusterIP
- ***loadBalancer\***：因为使用nodeport方式时，免不了要在应用的调用方写死一个集群节点的IP，这并非高可用的方式，所以又有了使用第三方负载均衡器的方式，转发到多个节点的nodeport，这种类型通常需要用户扩展个控制器与云平台或所属IDC机房的负载均衡器打通才能生效，普通安装的k8s集群一般类型为loadBalancer的服务都是pending状态；loadBalancer是在nodeport的基础之上再创建个lb，所以也是会先分配一个clusterIP，再创建节点的端口转发。
- ***headless\***：应用内多个副本彼此间互相访问，比如要部署到mysql的主从，从的副本想要找主的副本；
- ***externalName\***：其实只是相当于coredns里的cname记录

了解这些以后，我们试着用iptables模拟一个k8s的service吧，我们会在一个节点创建两个pod，分别叫pod-a、pod-b，然后用iptables模拟一个VIP和nodeport，这个VIP会把流量转给pod-b，最后试着在节点和pod-a中使用这个VIP访问pod-b，最后再试试在pod-b中用VIP访问自身会是什么情况，以此来解释hairpin flow的场景

## 先在主机创建两个pod

在我们测试的主机上创建两个pod，pod与主机连接的配置过程我们上一章已经介绍过，这里我们就直接上命令，不再一一解释：

- 创建pod-a（10.244.1.10）

```bash
ip netns add pod-a
ip link add eth0 type veth peer name veth-pod-a  
ip link set eth0 netns pod-a  
ip link set veth-pod-a up 
ip netns exec pod-a ip addr add 10.244.1.10/24 dev eth0 
ip netns exec pod-a ip link set eth0 up 

ip netns exec pod-a ip route add default via 169.254.10.24 dev eth0 onlink
echo 1 > /proc/sys/net/ipv4/conf/veth-pod-a/proxy_arp
ip route add 10.244.1.10 dev veth-pod-a
```

- 创建pod-b（10.244.1.11）

```bash
ip netns add pod-b
ip link add eth0 type veth peer name veth-pod-b  
ip link set eth0 netns pod-b  
ip link set veth-pod-b up 
ip netns exec pod-b ip addr add 10.244.1.11/24 dev eth0 
ip netns exec pod-b ip link set eth0 up 

ip netns exec pod-b ip route add default via 169.254.10.24 dev eth0 onlink
echo 1 > /proc/sys/net/ipv4/conf/veth-pod-b/proxy_arp
ip route add 10.244.1.11 dev veth-pod-b
```

为了确保两个pod能ping通，还需要：

```bash
echo 1 > /proc/sys/net/ipv4/ip_forward
iptables -I FORWARD -s 10.244.0.0/16 -d 10.244.0.0/16 -j ACCEPT
```

如无意外，应该可以在pod-a中ping通pod-b了

```bash
ip netns exec pod-a ping -c 5 10.244.1.11

PING 10.244.1.11 (10.244.1.11) 56(84) bytes of data.
64 bytes from 10.244.1.11: icmp_seq=1 ttl=63 time=0.090 ms
64 bytes from 10.244.1.11: icmp_seq=2 ttl=63 time=0.081 ms
64 bytes from 10.244.1.11: icmp_seq=3 ttl=63 time=0.062 ms
64 bytes from 10.244.1.11: icmp_seq=4 ttl=63 time=0.062 ms
64 bytes from 10.244.1.11: icmp_seq=5 ttl=63 time=0.054 ms
--- 10.244.1.11 ping statistics ---
5 packets transmitted, 5 received, 0% packet loss, time 136ms
rtt min/avg/max/mdev = 0.054/0.069/0.090/0.017 ms
```

我们用iptables搞起来！

## 用iptables模拟实现k8s服务

### 模拟cluterIP

用iptables模拟VIP：10.96.0.100，并把流量转到pod-b，命令如下：

```bash
iptables -A PREROUTING -t nat -d 10.96.0.100 -j DNAT --to-destination 10.244.1.11
```

好了，可以跑去pod-a中试试用clusterIP去ping一下pod-b了

```bash
ip netns exec pod-a ping -c 5 10.96.0.100

PING 10.96.0.100 (10.96.0.100) 56(84) bytes of data.
64 bytes from 10.96.0.100: icmp_seq=1 ttl=63 time=0.112 ms
64 bytes from 10.96.0.100: icmp_seq=2 ttl=63 time=0.084 ms
64 bytes from 10.96.0.100: icmp_seq=3 ttl=63 time=0.064 ms
64 bytes from 10.96.0.100: icmp_seq=4 ttl=63 time=0.084 ms
64 bytes from 10.96.0.100: icmp_seq=5 ttl=63 time=0.054 ms
--- 10.96.0.100 ping statistics ---
5 packets transmitted, 5 received, 0% packet loss, time 135ms
rtt min/avg/max/mdev = 0.054/0.079/0.112/0.022 ms
```

> 咦，记得在iptables模式下，clusterIP都是ping不通的啊？
> 其实只是kube-proxy在实现时只根据ip+端口+协议精确匹配才转发，这才导致clusterIP不能ping，我们上面只是IP匹配，所以icmp协议也会正常转，当然也就可以ping得通了。

这个时候在测试主机上用clusterIP能ping通pod-b吗？

```bash
ping -c 5 10.96.0.100

PING 10.96.0.100 (10.96.0.100) 56(84) bytes of data.
--- 10.96.0.100 ping statistics ---
5 packets transmitted, 0 received, 100% packet loss, time 133ms
```

答案是不行？为什么呢？回忆一下上面提过的netfilter流程，本机应用程序的包出去时只比过OUTPUT和POSTROUTING（注意图2），而我们刚刚的命令只在PREROUTING上生效，为了在测试主机上也能访问clusterIP，还要再增加一条规则：

```bash
iptables -A OUTPUT -t nat -d 10.96.0.100 -j DNAT --to-destination 10.244.1.11
```

然后在测试主机上也可以ping通了

### hairpin flow

如果在pod-b中用clusterIP去ping它自己呢？

```bash
ip netns exec pod-b ping -c 5 10.96.0.100

PING 10.96.0.100 (10.96.0.100) 56(84) bytes of data.
--- 10.96.0.100 ping statistics ---
5 packets transmitted, 0 received, 100% packet loss, time 129ms
```

不通，因为从pod-b出来的数据包，经过目标地址转换后，又回到了pod-b，这时来源IP也是pod-b，pod-b的的eth0网卡一般会有一个开关：

```bash
ip netns exec pod-b bash ## 进入pod-b的ns中运行bash
sysctl net.ipv4.conf.eth0.accept_local  ## 显示的结果是：net.ipv4.conf.eth0.accept_local = 0
```

这个开关指示是否允许eth0网卡接收源IP为本机IP的数据包，默认是不允许，于是内核协议栈会把这个包丢掉，所以就不通了；

为了能ping通，我们需要让进入pod-b的数据包的源IP转换成非pod-b的IP，就是说我们要在netfilter流程中对数据包做一次源地址转换，iptables中能做SNAT的点只有一个，就是POSTROUTING，于是：

```bash
iptables -A POSTROUTING -t nat -d 10.244.1.11 -s 10.244.1.11 -j MASQUERADE
```

经过上面的命令配置后，在pod-b中也能用vip ping自身了

```bash
ip netns exec pod-b ping -c 5 10.96.0.100

PING 10.96.0.100 (10.96.0.100) 56(84) bytes of data.
64 bytes from 10.96.0.100: icmp_seq=1 ttl=63 time=0.059 ms
64 bytes from 10.96.0.100: icmp_seq=2 ttl=63 time=0.081 ms
64 bytes from 10.96.0.100: icmp_seq=3 ttl=63 time=0.068 ms
64 bytes from 10.96.0.100: icmp_seq=4 ttl=63 time=0.082 ms
64 bytes from 10.96.0.100: icmp_seq=5 ttl=63 time=0.065 ms
--- 10.96.0.100 ping statistics ---
5 packets transmitted, 5 received, 0% packet loss, time 82ms
rtt min/avg/max/mdev = 0.059/0.071/0.082/0.009 ms
```

***这就是我们说的hairpin flow的场景：pod通过clusterIP访问自已\***

### k8s中kube-proxy中如何用iptables处理hairpin flow场景？

在使用iptables实现service的k8s集群的节点上，截取一段iptables规则：（用iptables-save命令，为了显示简洁均把注释省略，链的名称也简化为-1后缀了）

```bash
-A PREROUTING  -j KUBE-SERVICES  ##基操，就像上面例子一样，接管从pod过来的流量
-A OUTPUT  -j KUBE-SERVICES      ##基操，就像上面例子一样，接管从主机应用出来的流量

-A KUBE-SERVICES -d 10.96.252.6/32 -p tcp -m tcp --dport 80 -j KUBE-SVC-1  ##基操，每个服务都有一条这样的规则

-A KUBE-SVC-1  -j KUBE-SEP-1 ##这条链一开始看着感觉很多余，为什么不直接DNAT呢？

-A KUBE-SEP-1 -s 10.90.2.233/32  -j KUBE-MARK-MASQ ##把来源为自身的做了标记
-A KUBE-SEP-1 -p tcp  -m tcp -j DNAT --to-destination 10.90.2.233:80 ##这也是基操
```

注意上面显示的规则中第4条，为什么不直接转给最后一条，而是要在中间加一个来源地址为自身时跳到`KUBE-MARK-MASQ`？

来看看`KUBE-MARK-MASQ`是干什么的？

```bash
-A KUBE-MARK-MASQ -j MARK --set-xmark 0x4000/0x4000
```

先是标记了一下，然后在POSTROUTING的点进行了源地址转换：

```bash
-A KUBE-POSTROUTING -m mark --mark 0x4000/0x4000 -j MASQUERADE
```

在PREROUTING点中先标记一下，这是hairpin flow的流量（因为PREROUTING中还不能做SNAT，所以只能先记下），然后在POSTROUTING点中再对标记过的流量进行SNAT，这一系列的操作其实就是为了实现上面说的hairpin flow的场景

### 模拟NodePort

因为是具体到IP+端口了，所以也只能转到IP+端口，所以不能用ping来验证了，下面模拟把访问主机的tcp33888端口的流量都转给pod-b的80端口：

```bash
iptables -A OUTPUT -t nat -m addrtype --dst-type LOCAL -m tcp -p tcp --dport 33888 -j DNAT --to-destination 10.244.1.11:80
iptables -A PREROUTING -t nat -m addrtype --dst-type LOCAL -m tcp -p tcp --dport 33888 -j DNAT --to-destination 10.244.1.11:80
```

> 上面因为我们要接管两个点的流量，所以配置两条规则，实际的k8s的kube-proxy在实现时会设计更加合理的链来避免规则大量重复定义，上面只是为了演示效果

`-m addrtype --dst-type LOCAL`的意思是匹配主机所有IP（笔者使用的主机用vbox虚拟的虚拟机，有两个IP，192.168.6.160和10.0.2.15）

验证前，先在pod-b用socat启动一个服务监听80端口，这个服务会把把收到的内容原样返回

```bash
ip netns exec pod-b nohup socat TCP4-LISTEN:80,fork exec:cat 2>&1 &  
```

接着在主机上用nc访问：（笔者的主机IP为：192.168.6.160）

```bash
nc 192.168.6.160 33888   ## 或者 nc 10.0.2.15 33888 也是可以的
hello ##这是我发送的内容
hello ##这是服务返回的内容，符合预期
```

在pod-a中验证：

```bash
ip netns exec pod-a nc 10.0.2.15 33888
hello world
hello world
```

> 然后nodeport下的hairpin flow的处理方式和clusterIP是一样的，其实kube-proxy是引到同一条链上去处理的

## 一些误解

- 相对于直接访问podIP，使用clusterIP来访问因为多一次转发，会慢一些；

> 其实只是在发送的过程中修改了数据包的目标地址，两者走的转发路径是一模一样的，没有因为使用clusterIP而多一跳，当然因为要做nat会有一些些影响，但影响不大

- 使用nodeport因为比clusterIP又多一次转发，所以更慢；

> 没有，nodeport是一次直接就转成了podIP，并没有先转成clusterIP再转成podIP。

## 为什么NetworkPolicy不用限制serviceIP却又能生效？

我们用NetworkPolicy限制不允许pod-a使用pod-b的IP访问pod-b，但没有限制pod-a用clusterIP访问pod-b，怎么用clusterIP也访问不了pod-b呢？

因为：

- 在pod中使用clusterIP访问另一个pod时，防火墙策略的应用是在所在主机的FORWARD点，而把clusterIP转成podIP是在之前的PREROUTING点就完成了（注意图4)
- 在主机中使用clusterIP访问一个pod时，防火墙策略的应用是在主机的OUTPUT点，而把clusterIP转成podIP也是在OUTPUT点，不过在防火墙策略之前（注意图2)

***所以，防火墙策略其实从来都不会遇到clusterIP，因为在到达防火墙策略前，clusterIP都已经被转成podIP了，所以我们的网络策略只需要专心限制podIP即可\***

## 问题

1. 使用ipvs模式时，k8s集群的每个节点会有一张叫kube-ipvs0的网卡，网卡下挂着所有的clusterIP，有什么作用？
2. 下面这条iptables规则到底有什么作用？

```bash
-A KUBE-FORWARD -m conntrack --ctstate RELATED,ESTABLISHED -j ACCEPT
```

## 跨主机pod连接

在之前的两篇文章中分别介绍了pod与主机连接并且上外网的原理及service的clusterIP和nodeport的实现原理，对于组织pod的网络这件事来说，还有最后一环需要打通，就是分布在不同集群节点的pod之间如何相互通信，本章我们来解决这最后一环的问题

> 在这里我们继续用linux network namespace(ns)代表pod

我们将用下面三种方式实现跨主机的pod通信：

1. 主机路由
2. ip tunnel
3. vxlan

我准备了两台节点：

- host1（ip:10.57.4.20）
- host2（ip:10.57.4.21）

先在两台节点中分别创建一个pod，并与节点能相互通信，创建pod并与节点通信的相关原理在第一章已经介绍过，这里不再一一解释，直接上命令：

- host1中创建pod-a（ip:192.168.10.10）

```bash
ip netns add pod-a
ip link add eth0 type veth peer name veth-pod-a
ip link set eth0 netns pod-a
ip netns exec pod-a ip addr add 192.168.10.10/24 dev eth0
ip netns exec pod-a ip link set eth0 up
ip netns exec pod-a ip route add default via 169.254.10.24 dev eth0 onlink
ip link set veth-pod-a up
echo 1 > /proc/sys/net/ipv4/conf/veth-pod-a/proxy_arp
echo 1 > /proc/sys/net/ipv4/ip_forward
iptables -I FORWARD -s 192.168.0.0/16 -d 192.168.0.0/16 -j ACCEPT
ip route add 192.168.10.10 dev veth-pod-a scope link
```

- host2上创建pod-b（ip:192.168.11.10）

```bash
ip netns add pod-b
ip link add eth0 type veth peer name veth-pod-b
ip link set eth0 netns pod-b
ip netns exec pod-b ip addr add 192.168.11.10/24 dev eth0
ip netns exec pod-b ip link set eth0 up
ip netns exec pod-b ip route add default via 169.254.10.24 dev eth0 onlink
ip link set veth-pod-b up
echo 1 > /proc/sys/net/ipv4/conf/veth-pod-b/proxy_arp
echo 1 > /proc/sys/net/ipv4/ip_forward
iptables -I FORWARD -s 192.168.0.0/16 -d 192.168.0.0/16 -j ACCEPT
ip route add 192.168.11.10 dev veth-pod-b scope link
```

如无意外，host1应该能ping通pod-a，host2也能ping通pod-b了，环境准备完成，下面我们介绍主机路由模式，这是flannel的host-gw模式的原理。

## 主机路由

其实每一台linux主机本身就是一台路由器，可以用ip route命令配置主机上的路由表，要让pod-a和pod-b相互通信，只需要在两台主机上加一条路由即可：

- host1:

```bash
ip route add 192.168.11.0/24 via 10.57.4.21 dev eth0 onlink # 这个eth0是host1连接host2的网卡，要根据你的测试节点的情况调整
```

- host2:

```bash
ip route add 192.168.10.0/24 via 10.57.4.20 dev eth0 onlink # 这个eth0是host2连接host1的网卡，要根据你的测试节点的情况调整
```

> 注意上面我们加的路由是针对24位网络地址相同的子网段的，一般来说k8s集群的每个节点会独占一个24位的网络地址的子网段，所以每增加一个集群节点，其它节点加一条路由就可以了，但如果不是这样设计，像之前提过的pod要固定IP，又想要能在整个集群的任意节点运行，这个主机路由条目就会比较多，因为每条路由都是针对单个pod的

此时在pod-a中去ping pod-b应该是通了的，假设在pod-b的8080端口运行着一个http服务，在pod-a中请求这个服务，在主机路由的模式下，host1发往host2的数据包是长这样的：

![img](https://pic4.zhimg.com/80/v2-a1b51be7eff2291ab7a6d0c8d7ebbb53_1440w.webp)

图一：主机路由

注意图中的源IP和目标IP是容器的，但MAC地址却是主机的，我们在第一章中提到的linux网络知识的发送包的第5点说起过，数据包发送过程中，除非经过NAT，否则IP不会变化，始终标明通信双方，但MAC地址是每一段都会变化，数据包从pod-a到pod-b一共会经历三段：

1. 从pod-a发往host1时，源mac是pod-a的eth0网卡的mac，而目标mac是pod-a的默认网关（169.254.10.24）的mac，因为主机的veth-pod-a开启了arp代答，所以目标mac其实是主机上veth-pod-a的mac地址。
2. 从host1去往host2的过程中，所以源MAC是host1的eth0网卡的mac，目标MAC是host2的eth0网卡的mac。
3. 从host2发往pod-b，源mac是host2上veth-pod-b网卡的mac，目标mac是pod-b的eth0网卡mac

这是跨节点容器通信方式中最简单高效的方式，没有封包拆包带来的额外消耗，但这种方式的使用场景有一些限制：

- 集群节点必须在相同网段，因为主机路由的下一跳必须是二层可达的地址，如果在不同网段也想要使用非overlay的方式，那就需要把上面的路由信息同步到节点所在机房的路由器了，这就是calico BGP的方式

- 云平台的虚拟机一般有源/目地址检查，流量从虚拟机出来时，如果源IP或源MAC与虚拟机不符，则丢包；我们使用主机路由时，源MAC是虚拟机的，但源IP是pod的，所以就被丢包了；实在是想要在云平台使用主机路由的话：

- - 关闭“源/目地址检查”（华为云），VPC路由表要加路由（阿里云、腾讯云）
  - ECS所属的安全组策略中要放开pod的网段

> 云平台的虚拟机为什么要做源/目地址检查呢？因为要防止IP spoofing

因为以上限制，host-gw通常在idc机房且节点数不多都在同一子网的情况下使用，或者与别的模式混合使用，比如flannel的DirectRouting开启时，相同网段的用host-gw，跨网段用vxlan；

有没有节点跨网段也能使用的模式呢？接下来介绍的ip tunnel（就是常说的ipip模式）就是了。

## ip tunnel（ipip）

ipip模式并不是像主机路由那样，修改数据包的mac地址，而是在原ip包的前面再加一层ip包，然后链路层是以外层ip包的目标地址封装以太网帧头，而原来的那层ip包更像是被当成了外层包的数据，完成这个封包过程的是linux 虚拟网络设备tunnel网卡，它的工作原理是用节点路由表中匹配原ip包的路由信息中的下一跳地址为外层IP包的目标地址，以本节点的IP地址为源地址，再加一层IP包头，所以使用ip tunnel的模式下，我们需要做两件事情：

- 在各个主机上建立一个one-to-many的ip tunnel，（所谓的one-to-many，就是创建ip tunnel设备时，不指定remote address，这样一个节点只需要一张tunnel网卡）
- 维护节点的路由信息，目标地址为集群的每一个的node-cidr，下一跳为node-cidr所在节点的IP，跟上面的主机路由很像，只不过出口网卡就不再是eth0了，而是新建的ip tunnel设备；

我们接着上面的环境继续操作：

- 首先删除上面使用主机路由时在两台主机上增加的路由条目

host1:

```bash
ip route del 192.168.11.0/24 via 10.57.4.21 dev eth0 onlink
```

host2:

```bash
ip route del 192.168.10.0/24 via 10.57.4.20 dev eth0 onlink
```

- 然后在两台主机上分别创建ip tunnel设备

host1:

```bash
ip tunnel add mustang.tun0 mode ipip local 10.57.4.20 ttl 64
ip link set mustang.tun0 mtu 1480 ##因为多一层IP头，占了20个字节，所以MTU也要相应地调整
ip link set mustang.tun0 up
ip route add 192.168.11.0/24 via 10.57.4.21 dev mustang.tun0 onlink
ip addr add 192.168.10.1/32 dev mustang.tun0 ## 这个地址是给主机请求跨节点的pod时使用的
```

host2:

```bash
ip tunnel add mustang.tun0 mode ipip local 10.57.4.21 ttl 64
ip link set mustang.tun0 mtu 1480
ip link set mustang.tun0 up
ip route add 192.168.10.0/24 via 10.57.4.20 dev mustang.tun0 onlink
ip addr add 192.168.11.1/32 dev mustang.tun0
```

这时候两个pod应该已经可以相互ping通了，还是假设pod-a请求pod-b的http服务，此时host1发往host2的数据包是长这样的：

![img](https://pic3.zhimg.com/80/v2-6546d348c2dc8501fc8f6df6bd4d951a_1440w.webp)

图二：ipip

因为主机协议栈工作时是由下往上识别每一层包，所以ipip包对于主机协议栈而言，与正常主机间通信的包并没有什么不同，帧头中的源/目标mac是主机的，ip包头中源/目标ip也是节点的，这让节点所处的物理网络也感觉这是正常的节点流量，所以 这个模式相对于主机路由来说对环境的适应性更广，起码跨网段的节点也是可以通的，但是在云平台上使用这种模式还是要注意下，留意图二中外层IP包中的传输层协议号是不一样的（是IPPROTO_IPIP），正常的IP包头，这应该是TCP/UDP/ICMP，这样有可能也会被云平台的安全组策略拦截掉，在linux内核源码中可以看到：

```c
//include/uapi/linux/in.h
enum {
...
  IPPROTO_ICMP = 1,     /* Internet Control Message Protocol    */
#define IPPROTO_ICMP        IPPROTO_ICMP

  IPPROTO_IPIP = 4,     /* IPIP tunnels (older KA9Q tunnels use 94) */
#define IPPROTO_IPIP        IPPROTO_IPIP

  IPPROTO_TCP = 6,      /* Transmission Control Protocol    */
#define IPPROTO_TCP     IPPROTO_TCP

  IPPROTO_UDP = 17,     /* User Datagram Protocol       */
#define IPPROTO_UDP     IPPROTO_UDP
...
```

一般而言我们在云平台安全组设置规则时，传输层协议都只有三个可选项，就是：TCP、UDP、ICMP（没有IPIP），所以最好是在云平台上把安全组内的主机间的所有协议都放开，会不会真的被拦截掉要看具体云平台，华为云是会限制的；

> 笔者曾经试过在华为云上使用ipip模式，总会出现pod-a ping不通ping-b，卡着的时候，在pod-b上ping pod-a，然后两边就同时通了，这是典型的有状态防火墙的现象； 之后我们把集群节点都加入一个安全组，在安全组的规则配置中，把组内所有节点的所有端口所有协议都放开后，问题消失，说明默认对IPIP协议是没有放开的

在host1中执行：

```bash
ip netns exec pod-a ping -c 5 192.168.11.10
```

在host2的eth0用tcpdump打印一下流量，就能看到有两层ip头：

```bash
tcpdump -n -i eth0|grep 192.168.11.10

tcpdump: verbose output suppressed, use -v or -vv for full protocol decode
listening on eth0, link-type EN10MB (Ethernet), capture size 262144 bytes
18:03:35.048106 IP 10.57.4.20 > 10.57.4.21: IP 192.168.10.10 > 192.168.11.10: ICMP echo request, id 3205, seq 1, length 64 (ipip-proto-4)
18:03:35.049483 IP 10.57.4.21 > 10.57.4.20: IP 192.168.11.10 > 192.168.10.10: ICMP echo reply, id 3205, seq 1, length 64 (ipip-proto-4)
18:03:36.049147 IP 10.57.4.20 > 10.57.4.21: IP 192.168.10.10 > 192.168.11.10: ICMP echo request, id 3205, seq 2, length 64 (ipip-proto-4)
18:03:36.049245 IP 10.57.4.21 > 10.57.4.20: IP 192.168.11.10 > 192.168.10.10: ICMP echo reply, id 3205, seq 2, length 64 (ipip-proto-4)
```

calico的ipip模式就是这种，ip tunnel解决了主机路由不能在跨网段中使用的问题，在idc机房部署k8s集群的场景下，会拿host-gw和ipip两种模式混合使用，节点在相同网段则用host-gw，不同网段则用ipip，思路和flannel的directrouting差不多，只不过ipip比vxlan性能要好一些；

ip tunnel仍然有一些小小的限制，像上面说的云平台安全组对协议限制的问题，下面再介绍一种终极解决方案，只要节点网络是通的，容器就能通，完全没有限制，这就是vxlan模式；

## vxlan

主机路由是按普通路由器的工作原理，每一跳修改MAC地址；ipip模式是给需要转发的数据包前面加一层IP包；而vxlan模式则是把pod的数据帧（注意这里是帧，就是包含二层帧头）封装在主机的UDP包的payload中，数据包封装的工作由linux虚拟网络设备vxlan完成，vxlan设备可以用下面的命令创建：

```bash
ip link add vxlan0 type vxlan id 100 dstport 4789 local 10.57.4.20 dev eth0
##设备名为vxlan0
##vxlan id 为 100
##dstport指示使用哪个udp端口
##eth0指示封装好vxlan包后通过哪个主机网卡发送
```

vxlan设备在封包时是根据目标MAC地址来决定外层包的目标IP，所以需要主机提供目标MAC地址与所属节点IP的映射关系，这些映射关系存在主机的fdb表（forwarding database）中，fdb记录可以用下面的命令查看：

```bash
bridge fdb show|grep vxlan0

8a:e7:df:c0:84:07 dev vxlan0 dst 10.57.4.21 self permanent
```

上面的记录的意思是说去往MAC地址为`8a:e7:df:c0:84:07`的pod在节点IP为`10.57.4.21`的节点上，fdb的信息可以手工维护，也可以让vxlan设备自动学习；

- 手工添加一条fdb记录的命令如下：

```bash
bridge fdb append 8a:e7:df:c0:84:07 dev vxlan0 dst 10.57.4.21 self permanent
```

- 如果需要让vxlan设备去学习fdb记录，可以创建vxlan设备时设置多播地址，并开启learning选项：

```bash
ip link add vxlan0 type vxlan id 100 dstport 4789 group 239.1.1.1 dev eth0 learning
```

所有集群的节点都加入这个多播组，这样就能自动学习fdb记录了，当然这需要底层网络支持多播；

- 也可以通过增加全0的fdb记录来告诉vxlan设备遇到不知道下一跳的MAC应该向哪些节点广播：

```bash
bridge fdb append  00:00:00:00:00:00 dev vxlan0 dst 10.57.4.21 self permanent
```

我们接着上面的环境继续往下做，先把mustang.tun0删除，在两个节点上执行：

```bash
ip link del mustang.tun0
```

然后 host1：

```bash
ip link add vxlan0 type vxlan id 100 dstport 4789 local 10.57.4.20 dev eth0 learning  ## 这个eth0要根据你自己测试节点的网卡调整
ip addr add 192.168.10.1/32 dev vxlan0
ip link set vxlan0 up
ip route add 192.168.11.0/24 via 192.168.11.1 dev vxlan0 onlink
bridge fdb append  00:00:00:00:00:00 dev vxlan0 dst 10.57.4.21 self permanent
```

host2：

```bash
ip link add vxlan0 type vxlan id 100 dstport 4789 local 10.57.4.21 dev eth0 learning  ## 这个eth0要根据你自己测试节点的网卡调整
ip addr add 192.168.11.1/32 dev vxlan0
ip link set vxlan0 up
ip route add 192.168.10.0/24 via 192.168.10.1 dev vxlan0 onlink
bridge fdb append  00:00:00:00:00:00 dev vxlan0 dst 10.57.4.20 self permanent
```

这时候两台主机的pod应该可以相互ping通了

```bash
ip netns exec pod-b ping -c 5 192.168.10.10
PING 192.168.10.10 (192.168.10.10) 56(84) bytes of data.
64 bytes from 192.168.10.10: icmp_seq=1 ttl=62 time=0.375 ms
64 bytes from 192.168.10.10: icmp_seq=2 ttl=62 time=0.497 ms
64 bytes from 192.168.10.10: icmp_seq=3 ttl=62 time=0.502 ms
64 bytes from 192.168.10.10: icmp_seq=4 ttl=62 time=0.386 ms
64 bytes from 192.168.10.10: icmp_seq=5 ttl=62 time=0.390 ms
--- 192.168.10.10 ping statistics ---
5 packets transmitted, 5 received, 0% packet loss, time 4000ms
rtt min/avg/max/mdev = 0.375/0.430/0.502/0.056 ms
```

此时pod-a请求pod-b的http服务，数据包从host-1发往host-2时是长这样的：

![img](https://pic1.zhimg.com/80/v2-563db7319a1235f297ae020b076cc790_1440w.webp)

图三：vxlan

可以看到，vxlan包是把整个pod-a发往pod-b最原始的帧都装进了一个udp数据包的payload中，整个流程简述如下：

- 1､pod-a数据包到达host-1，源ip为pod-a，目标ip为pod-b，源mac为pod-a，目标mac为host-1中的veth-pod-a
- 2､主机因为开启了转发，所以查找路由表中去往pod-b的下一跳，查到匹配的路由信息如下：

```bash
192.168.11.0/24 via 192.168.11.1 dev vxlan0 onlink  
## 这是我们在上面的host1执行的命令中的第四条命令添加的
```

- 3､于是主机把数据包给了vxlan0，并且下一跳为192.168.11.1，此时vxlan0需要得到192.168.11.1的mac地址，但主机的邻居表中不存在，于是vxlan0发起arp广播去询问，vxlan0的广播范围是由我们配置的，这个范围就是我们给他加的全0 fdb记录标识的dstIP，就是上面命令中的：

```bash
bridge fdb append  00:00:00:00:00:00 dev vxlan0 dst 10.57.4.21 self permanent
```

所以，这里找到的目标只有一个，就是10.57.4.21，然后vxlan就借助host1的eth0发起了这个广播，只不过eth0发起的不是广播，而是有明确目标IP的udp数据包，如果上面我们是配置了多个全0的fdb记录，这里eth0就会发起多播。

- 4､192.168.11.1这个地址是我们配置在host2上的vxlan0的网卡地址，于是host2会响应arp请求，host1的vxlan设备得到192.168.11.1的mac地址后，vxlan会从主机的fdb表中查找该mac的下一跳的主机号，发现找不到，于是又发起学习，问谁拥有这个mac，host-2再次应答，于是vxlan0就拥有了封包需要的全部信息，于是把包封装成图三的样子，扔给了host1的eth0网卡；
- 5､host2收到这个包后，因为是一个普通的udp包，于是一直上送到传输层，传输层对于这个端口会有个特殊处理，这个特殊处理会把udp包里payload的信息抠出来扔给协议栈，重新走一遍收包流程。（vxlan的原理后面有机会专门写一篇文章）

> vxlan学习fdb的方式难免会在主机网络间产生广播风暴，所以flannel的vxlan模式下，是关闭了vxlan设备的learning机制，然后用控制器维护fdb记录和邻居表记录的

可以看到这个过程中两次都需要用到全0的fdb记录，我们也可以在host1上查看vxlan0学习到的fdb记录和邻居表信息：

```bash
bridge fdb|grep vxlan0

00:00:00:00:00:00 dev vxlan0 dst 10.57.4.21 self permanent ## 这是我们手工添加的
6e:39:38:33:7c:24 dev vxlan0 dst 10.57.4.21 self   ## 这是vxlan0自动学习的，6e:39:38:33:7c:24 正是host2中vxlan0的地址
```

邻居表记录：

```bash
ip n

192.168.11.1 dev vxlan0 lladdr 6e:39:38:33:7c:24 STALE
```

在pod-b中ping pod-a的时候，在host1打开网卡监听，拦截的数据如下：

```bash
tcpdump -n -i eth0 src 10.57.4.21

tcpdump: verbose output suppressed, use -v or -vv for full protocol decode
listening on eth0, link-type EN10MB (Ethernet), capture size 262144 bytes
10:21:01.050849 IP 10.57.4.21.55255 > 10.57.4.20.otv: OTV, flags [I] (0x08), overlay 0, instance 1
IP 192.168.11.10 > 192.168.10.10: ICMP echo request, id 26972, seq 15, length 64
10:21:02.051894 IP 10.57.4.21.55255 > 10.57.4.20.otv: OTV, flags [I] (0x08), overlay 0, instance 1
IP 192.168.11.10 > 192.168.10.10: ICMP echo request, id 26972, seq 16, length 64
......
```

可以看到也是两层包头，外层包头显示这是otv（overlay transport virtualization）包，对于otv，用一句话解释：

***OTV is a "MAC in IP" technique to extend Layer 2 domains over any transport\***

从上面的过程可以看出来，vxlan模式依赖udp协议和默认的4789端口，所以在云平台的ECS上使用vxlan模式，还是需要在安全组上把udp 4789端口放开

> 什么终极解决方案，弄了半天也是要设置安全组的哈哈哈！！

## 一些误解

1. 是不是用了隧道模式，网络策略就不起效了？

不是的，不管是ipip还是vxlan模式下，主机协议栈把外层包头摘掉后，会把原始数据包重新扔回协议栈，重走一遍netfilter的几个点，所以针对podIP的防火墙策略依旧会生效的；

## 对比几种常用的cni

- flannel

- - vxlan模式兼容性强，但速度差一点
  - host-gw模式：只有二层直联的环境才能用，节点不能在多个子网，速度最快
  - 不支持network policy

- calico

- - bgp在idc机房较合适，云平台不支持
  - ipip模式，兼容性强，速度比vxlan好，最推荐
  - 支持network policy

- cilium

- - 性能好，也支持network policy，但对linux内核有要求（推荐是4.18以上）
  - 对于运维来说比较有难度，因为一切都是新的，没有iptables/ipvs，以前的排错经验用不上

## 解答上一篇问题

- 使用ipvs模式时，k8s集群的每个节点会有一张叫kube-ipvs0的网卡，网卡下挂着所有的clusterIP，有什么作用？

看回上一篇文章的图一，ipvs工作在netfilter扩展点中的LOCAL_IN点（也就是INPUT点），之前的内容中提过，流量在经过IPIsLocal时，会判断目标IP是否为本机地址，如果是则会走INPUT点，否则走FORWATD；为了让ipvs能操作流量，必须先让流量先到达INPUT点，于是就把所有clusterIP都挂在kube-ipvs0上，所有访问clusterIP的流量到达IPIsLocal点时，主机协议栈都会认为这是去往本机的流量，转到INPUT点去；

- 下面这条iptables规则到底有什么作用？

```bash
-A KUBE-FORWARD -m conntrack --ctstate RELATED,ESTABLISHED -j ACCEPT
```

首先要了解，现在的防火墙技术都是基于连接状态的基础之上的，就是常说的***有状态的防火墙\***；

拿上面的pod-a和pod-b来举例，假设我们不允许pod-a访问pod-b，于是在host1上创建一条这样的iptables规则：

```bash
iptables -A FORWARD -t filter -s 192.168.10.10 -d 192.168.11.10 -j DROP
```

好了，这时候pod-a中去ping pod-b已经不通了，但是，pod-b中去ping pod-a也不通了，因为pod-a回pod-b的包也命中了上面那条策略；

当我们说：***不允许pod-a访问pod-b，只是说不允许pod-a主动访问pod-b，但是允许pod-a被动访问pod-b\***

这个听着有点绕，类似你跟你的二逼朋友说：平时没事别主动给老子打电话，但老子打你电话你要接！

好了，问题来了，怎么标识这是主动和流量还是被动的流量呢？这个问题linux内核协议栈已经帮我们解决好了，linux内核协议栈会悄悄维护连接的状态：

- 当pod-a向pod-b主动发送数据包时，到达pod-b时，连接状态为NEW；
- 当pod-b主动向pod-a发送数据包，pod-a回给pod-b的数据包到达pod-b时，连接状态为ESTABLISHED；

于是我们只要优先放过所有的连接状态为ESTABLISHED的包就可以了，问题中的命令的作用正是这个：

```bash
-A KUBE-FORWARD -m conntrack --ctstate RELATED,ESTABLISHED -j ACCEPT
```

`-m conntrack`是说使用连接追踪模块标识的数据包状态，`--ctstate`是connection track state（连接追踪状态）的简称，状态值有：NEW/ESTABLISHED/INVALID/RELATED等，各种状态的解释自行google；

上面这条规则的优先级一般都是最高的，如果放在其它限制规则的后面就没有意义了，不单是容器平台的防火墙策略，大多数云平台网络中ACL、安全组的策略也是这种玩法；

## pod流量控制

在前面的几篇文章中，我们解决了pod连接主机、pod连接外网、pod与相同节点或不同节点的pod连接、用clusterIP和nodeport的方式访问pod等几个问题，可以说，对于组织pod的网络的每一环都已经完成了。

和CPU、内存这类资源一样，我们肯定希望网络资源对于每个pod来说也是平均分配的，起码能做到每个pod的数据包发送与接收的速度都能控制在一定的范围内，节点的带宽不能被某个pod耗光而影响其它的pod，所以这一章我们来讨论如何控制pod的进出流量速率。

首先我们来看看这回linux给我们准备了哪些工具；

## TC（traffic control）

linux自带流量控制框架，这个框架允许用户在数据发送前配置数据包排队规则qdisc（queueing discipline），对流量进行限制或整形，linux的tc只控制发送速率不控制接收速率，当然要控制接收速率也是有办法实现的。

对于限制网卡的发送速率，一般有两种方式：

1. 第一种是对整个网卡的发送速率进行简单粗暴的限制，例如eth0网卡的发送速率限制100mbit；
2. 第二种是对网卡发出的流量先进行分类，再分别对每一分类的的速率单独限制，例如访问mysql的流量限制80mbit，访问http服务的流量限制20mbit；

对于第一种方式，我们选择无类别队列，对于第二种方式，我们选择可分类队列。

### 无类别队列

主要有：

- pfifo/bfifo（First In First Out）：先进先出队列，只需设置队列的长度，pfifo是以数据包的个数为单位，bfifo是以字节数为单位；
- pfifo_fast：数据包是按照TOS被分配多三个波段里，band0优先级最高，band1次之，band2最低，按优先级从高到低发送，在每个波段里面，使用先进先出规则；
- tbf（Token Bucket Filter）：针对数据字节数进行限制，适合于把流速降低到某个值，但允许短暂突发流量超过设定值，我们限制pod的发送速率主要就用这个队列；
- red（Random Early Detection）：当带宽的占用接近于规定的带宽时，系统会随机地丢弃一些数据包
- sfq（Stochastic Fairness Queueing）：它按照会话为流量进行排序，然后循环发送每个会话的数据包。
- FQ (Fair Queue)：公平队列

在这里我们只介绍下如何创建tbf队列，因为后面主要是使用这个队列来限制pod的发送速率，下面的命令可以控制eth0的发送速率为100mbit：

```bash
tc qdisc add dev eth0 root tbf rate 100mbit burst 100mbit limit 100mbit

## rate：传输速率
## burst：桶的大小
## limit：确定最多有多少数据（byte）在队列中等待令牌
```

> 流量控制单位
> \- kbps：千字节／秒
> \- mbps：兆字节／秒
> \- kbit：KBits／秒
> \- mbit：MBits／秒
> \- bps：字节数／秒（如果不带单位，则默认单位是这个）

### 可分类队列

不同于无分类队列，可分类队列使用时步骤稍微复杂些，产要分三步：

1. 给网卡创建一个队列
2. 创建队列的分类，在各个分类里可以设置不同的流量策略
3. 创建分类规则，把流量导到第二步创建的分类

可分类队列主要有：

- cbq(class based queueing:基于类别排队)：没用过，自行google
- htb(hierarchy token bucket:层级令牌桶)：看下面的示例

示例配置：访问mysql的速率限制80mbit，访问http服务的速率限制20mbit

- 创建htb队列：

```bash
tc qdisc add dev eth0 root handle 1: htb default 11 ##使用htb队列，默认流量去分类11
```

- 创建队列分类：

```bash
tc class add dev eth0 parent 1: classid 1:11 htb rate 80mbit ceil 80mbit  ## 创建分类11，速率限制80mbit
tc class add dev eth0 parent 1: classid 1:12 htb rate 20mbit ceil 20mbit  ## 创建分类12，速率限制20mbit
```

- 引导流量到分类：

```bash
tc filter add dev eth0 protocol ip parent 1:0 prio 1 u32 match ip dport 3306 0xffff flowid 1:11  ## 所有访问3306端口的流量导到分类11中
tc filter add dev eth0 protocol ip parent 1:0 prio 1 u32 match ip dport 80 0xffff flowid 1:12  ## 所有访问80端口的流量导到分类12中
```

也可以通过来源IP+目标端口来引导流量

```bash
tc filter add dev eth0 protocol ip parent 1:0 prio 1 u32 match ip src 192.168.6.160 match ip dport 23 oxffff flowid 1:11
```

也可以通过数据标记来引导流量：

```bash
iptables -t mangle -A POSTROUTING -d 10.244.1.10 -j MARK –set-mark 100 ## 用iptables给数据打标记
tc filter add dev eth0 protocol ip parent 1:0 prio 2 handle 100 fw flowid 1:11  ## 标记了100的数据包引导到分类11中
```

## pod的流量限制

首先还是在测试的主机上创建一个pod：(笔者的测试主机IP为192.168.6.160)

```bash
ip netns add pod-a
ip link add eth0 type veth peer name veth-pod-a
ip link set eth0 netns pod-a
ip netns exec pod-a ip addr add 192.168.10.10/24 dev eth0
ip netns exec pod-a ip link set eth0 up
ip netns exec pod-a ip route add default via 169.254.10.24 dev eth0 onlink
ip link set veth-pod-a up
echo 1 > /proc/sys/net/ipv4/conf/veth-pod-a/proxy_arp
echo 1 > /proc/sys/net/ipv4/ip_forward
iptables -I FORWARD -s 192.168.0.0/16 -d 192.168.0.0/16 -j ACCEPT
ip route add 192.168.10.10 dev veth-pod-a scope link
```

然后在主机上安装iperf3：

```bash
yum install iperf3
```

在pod-a中启动服务端：

```bash
ip netns exec pod-a iperf3 -s
```

再开一个终端，测试一下限速前的速度：

```bash
iperf3 -c 192.168.10.10 -i 1 -t 10

Connecting to host 192.168.10.10, port 5201
[  5] local 192.168.6.160 port 50768 connected to 192.168.10.10 port 5201
[ ID] Interval           Transfer     Bitrate         Retr  Cwnd
[  5]   0.00-1.00   sec  8.19 GBytes  70.3 Gbits/sec    0   1.35 MBytes
[  5]   1.00-2.00   sec  8.27 GBytes  71.0 Gbits/sec    0   1.35 MBytes
[  5]   2.00-3.00   sec  8.18 GBytes  70.3 Gbits/sec    0   1.35 MBytes
[  5]   3.00-4.00   sec  8.36 GBytes  71.8 Gbits/sec    0   1.35 MBytes
[  5]   4.00-5.00   sec  8.46 GBytes  72.7 Gbits/sec    0   1.35 MBytes
[  5]   5.00-6.00   sec  8.40 GBytes  72.2 Gbits/sec    0   1.35 MBytes
[  5]   6.00-7.00   sec  8.50 GBytes  73.1 Gbits/sec    0   1.42 MBytes
[  5]   7.00-8.00   sec  8.25 GBytes  70.8 Gbits/sec    0   1.57 MBytes
[  5]   8.00-9.00   sec  8.53 GBytes  73.2 Gbits/sec    0   1.57 MBytes
[  5]   9.00-10.00  sec  8.45 GBytes  72.6 Gbits/sec    0   1.57 MBytes
- - - - - - - - - - - - - - - - - - - - - - - - -
[ ID] Interval           Transfer     Bitrate         Retr
[  5]   0.00-10.00  sec  83.6 GBytes  71.8 Gbits/sec    0             sender
[  5]   0.00-10.04  sec  83.6 GBytes  71.5 Gbits/sec                  receiver
iperf Done.
```

可以看到，限制前的速度为71G/秒；

因为pod使用的是veth网卡对，所以我们可以通过主机端的网卡，达到控制pod流量的目的；

### 控制pod的接收速率

我们控制主机网卡`veth-pod-a`的发送速率，就相当于是控制pod的接收速率，我们试一下限制pod的接收速率为100mbit：

```bash
tc qdisc add dev veth-pod-a root tbf rate 100mbit burst 100mbit limit 100mbit
```

此时再测：

```bash
iperf3 -c 192.168.10.10 -i 1 -t 10

Connecting to host 192.168.10.10, port 5201
[  5] local 192.168.6.160 port 50626 connected to 192.168.10.10 port 5201
[ ID] Interval           Transfer     Bitrate         Retr  Cwnd
[  5]   0.00-1.00   sec  24.9 MBytes   209 Mbits/sec    0    389 KBytes
[  5]   1.00-2.00   sec  11.6 MBytes  97.5 Mbits/sec    0    389 KBytes
[  5]   2.00-3.00   sec  11.6 MBytes  97.5 Mbits/sec    0    389 KBytes
[  5]   3.00-4.00   sec  11.7 MBytes  98.0 Mbits/sec    0    389 KBytes
[  5]   4.00-5.00   sec  10.8 MBytes  90.2 Mbits/sec    0    389 KBytes
[  5]   5.00-6.00   sec  11.7 MBytes  98.0 Mbits/sec    0    389 KBytes
[  5]   6.00-7.00   sec  11.6 MBytes  97.5 Mbits/sec    0    389 KBytes
[  5]   7.00-8.00   sec  11.0 MBytes  92.3 Mbits/sec    0    389 KBytes
[  5]   8.00-9.00   sec  11.6 MBytes  97.5 Mbits/sec    0    389 KBytes
[  5]   9.00-10.00  sec  11.6 MBytes  97.5 Mbits/sec    0    389 KBytes
- - - - - - - - - - - - - - - - - - - - - - - - -
[ ID] Interval           Transfer     Bitrate         Retr
[  5]   0.00-10.00  sec   128 MBytes   107 Mbits/sec    0             sender
[  5]   0.00-10.05  sec   126 MBytes   105 Mbits/sec                  receiver
iperf Done.
```

看到限速后的结果为105mbit/秒左右，符合预期

删除接收限速：

```bash
tc qdisc del dev veth-pod-a root tbf rate 100mbit burst 100mbit limit 100mbit
```

### 控制pod的发包速率

因为linux的tc框架控发不控收，所以我们不能像上面一样，通过控制主机端`veth-pod-a`网卡的接收速率来控制pod发送速率的目的，但也不是完全没有办法：

### 在pod内直接限制发送速率

虽然不能在主机端控制pod的发送，但是可以直接在容器里控制，命令和上面的一样，只不过是在pod-a的ns中执行：

```bash
ip netns exec pod-a tc qdisc add dev eth0 root tbf rate 100mbit burst 100mbit limit 100mbit
```

因为是测试从容器发送的速率，所以我们要把iperf3的服务端调整一下，服务端跑在主机上，然后再在容器中进行发送测试：

```bash
ip netns exec pod-a iperf3 -c 192.168.6.160 -i 1 -t 10

Connecting to host 192.168.6.160, port 5201
[  5] local 192.168.10.10 port 49224 connected to 192.168.6.160 port 5201
[ ID] Interval           Transfer     Bitrate         Retr  Cwnd
[  5]   0.00-1.00   sec  26.6 MBytes   223 Mbits/sec    0    641 KBytes
[  5]   1.00-2.00   sec  11.2 MBytes  94.4 Mbits/sec    0    641 KBytes
[  5]   2.00-3.00   sec  11.2 MBytes  94.4 Mbits/sec    0    641 KBytes
[  5]   3.00-4.00   sec  11.2 MBytes  94.4 Mbits/sec    0    641 KBytes
[  5]   4.00-5.00   sec  11.2 MBytes  94.4 Mbits/sec    0    641 KBytes
[  5]   5.00-6.00   sec  12.5 MBytes   105 Mbits/sec    0    641 KBytes
[  5]   6.00-7.00   sec  11.2 MBytes  94.4 Mbits/sec    0    641 KBytes
[  5]   7.00-8.00   sec  11.2 MBytes  94.4 Mbits/sec    0    641 KBytes
[  5]   8.00-9.00   sec  11.2 MBytes  94.4 Mbits/sec    0    641 KBytes
[  5]   9.00-10.00  sec  11.2 MBytes  94.4 Mbits/sec    0    641 KBytes
- - - - - - - - - - - - - - - - - - - - - - - - -
[ ID] Interval           Transfer     Bitrate         Retr
[  5]   0.00-10.00  sec   129 MBytes   108 Mbits/sec    0             sender
[  5]   0.00-10.04  sec   126 MBytes   105 Mbits/sec                  receiver
iperf Done.
```

结果是105mbit/秒，也是符合预期

删除限制：

```bash
ip netns exec pod-a tc qdisc del dev eth0 root tbf rate 100mbit burst 100mbit limit 100mbit
```

通常我们会把容器的命令执行权限开给业务方，这样他们就有可能在容器里把这个速率限制取消，有没有一种办法是在主机端限制pod的发送速率呢？有。

### 在主机端用ifb网卡的方式限制收包速率

ifb网卡也是linux虚拟网络设备，类似于tun/tap/veth，只不过ifb的原理要简单得多，可以看作是一张只有tc过滤功能的虚拟网卡，而且它不会改变数据包的流向，比如把某张网卡接收流量导给ifb网卡，经过ifb的流量控制过滤后，继续走原网卡的接收流程，发送也是如此；这样我们就可以把pod在主机一端的网卡的接收重定向到ifb网卡，然后通过控制ifb网卡的发送速率，来间接控制pod的发送速率。

首先要确认内核有加载ifb模块，如果没有则加载

```bash
modprobe ifb    //需要加载ifb模块
```

然后创建ifb网卡，并设置发送队列长度为1000：

```bash
ip link add ifb0 type ifb
ip link set dev ifb0 up txqueuelen 1000
```

把`veth-pod-a`的接收重定向到ifb网卡上：

```bash
tc qdisc add dev veth-pod-a ingress handle ffff: 
tc filter add dev veth-pod-a parent ffff: protocol ip u32 match u32 0 0 flowid 1:1 action mirred egress redirect dev ifb0   //重定向流量到ifb
```

设置ifb0的发送速率：

```bash
tc qdisc add dev ifb0 root tbf rate 100mbit burst 100mbit limit 100mbit
```

此时再测：

```bash
ip netns exec pod-a  iperf3 -c 192.168.6.160 -i 1 -t 10

Connecting to host 192.168.6.160, port 5201
[  5] local 192.168.10.10 port 54762 connected to 192.168.6.160 port 5201
[ ID] Interval           Transfer     Bitrate         Retr  Cwnd
[  5]   0.00-1.00   sec  26.5 MBytes   223 Mbits/sec    0    700 KBytes
[  5]   1.00-2.00   sec  11.2 MBytes  94.4 Mbits/sec    0    700 KBytes
[  5]   2.00-3.00   sec  11.2 MBytes  94.4 Mbits/sec    0    700 KBytes
[  5]   3.00-4.00   sec  11.2 MBytes  94.4 Mbits/sec    0    700 KBytes
[  5]   4.00-5.00   sec  12.5 MBytes   105 Mbits/sec    0    700 KBytes
[  5]   5.00-6.00   sec  11.2 MBytes  94.4 Mbits/sec    0    700 KBytes
[  5]   6.00-7.00   sec  11.2 MBytes  94.4 Mbits/sec    0    700 KBytes
[  5]   7.00-8.00   sec  11.2 MBytes  94.4 Mbits/sec    0    700 KBytes
[  5]   8.00-9.00   sec  11.2 MBytes  94.4 Mbits/sec    0    700 KBytes
[  5]   9.00-10.00  sec  11.2 MBytes  94.4 Mbits/sec    0    700 KBytes
- - - - - - - - - - - - - - - - - - - - - - - - -
[ ID] Interval           Transfer     Bitrate         Retr
[  5]   0.00-10.00  sec   129 MBytes   108 Mbits/sec    0             sender
[  5]   0.00-10.05  sec   126 MBytes   105 Mbits/sec                  receiver
iperf Done.
```

105mbit/秒，符合预期，改一下速率限制，从100mbit改为200mbit：

```bash
tc qdisc replace dev ifb0 root tbf rate 200mbit burst 200mbit limit 200mbit
```

然后再测：

```bash
ip netns exec pod-a  iperf3 -c 192.168.6.160 -i 1 -t 10

Connecting to host 192.168.6.160, port 5201
[  5] local 192.168.10.10 port 56044 connected to 192.168.6.160 port 5201
[ ID] Interval           Transfer     Bitrate         Retr  Cwnd
[  5]   0.00-1.00   sec  48.0 MBytes   403 Mbits/sec    0    354 KBytes
[  5]   1.00-2.00   sec  23.1 MBytes   194 Mbits/sec    0    354 KBytes
[  5]   2.00-3.00   sec  23.1 MBytes   194 Mbits/sec    0    354 KBytes
[  5]   3.00-4.00   sec  22.4 MBytes   188 Mbits/sec    0    354 KBytes
[  5]   4.00-5.00   sec  23.1 MBytes   194 Mbits/sec    0    354 KBytes
[  5]   5.00-6.00   sec  22.4 MBytes   188 Mbits/sec    0    354 KBytes
[  5]   6.00-7.00   sec  23.1 MBytes   194 Mbits/sec    0    354 KBytes
[  5]   7.00-8.00   sec  23.1 MBytes   194 Mbits/sec    0    354 KBytes
[  5]   8.00-9.00   sec  22.4 MBytes   188 Mbits/sec    0    354 KBytes
[  5]   9.00-10.00  sec  23.1 MBytes   194 Mbits/sec    0    354 KBytes
- - - - - - - - - - - - - - - - - - - - - - - - -
[ ID] Interval           Transfer     Bitrate         Retr
[  5]   0.00-10.00  sec   254 MBytes   213 Mbits/sec    0             sender
[  5]   0.00-10.04  sec   252 MBytes   210 Mbits/sec                  receiver
iperf Done.
```

210mbit/秒，都符合预期。

删除pod-a的发送限速：

```bash
tc qdisc del dev veth-pod-a ingress
tc qdisc del dev ifb0 root tbf rate 200mbit burst 200mbit limit 200mbit
ip link del ifb0
```

OK，pod的流量控制也就说完了。

到目前为止，我们已经解决了一个常规则的k8s的cni需要解决的一切问题，但直到现在，也没见过go语言的影子，所以说k8s都是负责粘合功能的胶水代码，真正工作的是linux系统，与其说学习k8s的网络，不如说在学习linux提供的各种虚拟网络设备及内核协议栈的工作机制。

## flannel原理

flannel有udp、vxlan和host-gw三种模式，udp模式因为性能较低现在已经比较少用到，host-gw我们在前面简单介绍过，因为使用场景比较受限，所以vxlan模式是flannel使用最多的模式，本章我们来介绍一下vxlan模式的原理。

我们在第三篇文章中已经详细介绍过vxlan如何完成跨主机pod通信，所以在这我们主要介绍flannel的几个组件的工作原理，最后也会简要介绍一下udp模式。

在vlan模式下，每个节点会有一个符合cni规范的二进制可执行文件flannel（下面简称flannel-cni），一个以k8s的daemonset方式运行的kube-flannel，下面来分别介绍下它们是干啥的：

## flannel-cni

flannel文件存放在每个节点的/opt/cni/bin目录下，这个目录下还有cni官方默认提供的其它插件，这些cni插件分为三类：

- ipam，负责地址分配，主要有：host-local、dhcp、static
- main，负责主机和容器网络的编织，主要有：bridge、ptp、ipvlan、macvlan、host-device、
- meta，其它，主要有：flannel、bandwidth、firewall、portmap、tuning、sbr

这些文件是我们在安装kubeadm和kubelet时自动安装的，如果发现这个目录为空，也可以用下面的命令手动安装：

```bash
yum install kubernetes-cni -y
```

这个文件不做具体的容器网络编织的工作，而是生成其它cni插件需要的配置文件，然后调用其它的cni插件（通常是bridge和host-local），完成主机内容器到主机的网络互通，这个flannel-cni文件的源码已经不在flannel项目上了，而是在cni的plugins中，地址如下：

[[https://github.com/containernetworking/plugins/tree/master/plugins/meta/flannel](https://link.zhihu.com/?target=https%3A//github.com/containernetworking/plugins/tree/master/plugins/meta/flannel)]

### flannel-cni工作流程

kubelet创建一个pod时，先会创建一个pause容器，然后用pause容器的网络命名空间为入参（类似：/var/run/docker/netns/xxxx，用docker inspect nginx|grep Sandbox能获取到），加上其它一些参数，调用/etc/cni/net.d/目录下的配置文件指定的cni插件，内容如下：

```bash
cat /etc/cni/net.d/10-flannel.conflist

{
  "name": "cbr0",
  "cniVersion": "0.3.1",
  "plugins": [
    {
      "type": "flannel",
      "delegate": {
        "hairpinMode": true,
        "isDefaultGateway": true
      }
    },
    {
      "type": "portmap",
      "capabilities": {
        "portMappings": true
      }
    }
  ]
}
```

> 这个配置文件是kube-flannel启动时复制进去的，我们编写cni时也要生成这个文件

这个文件中指定的cni插件叫flannel，于是kubelet就调用了/opt/cni/bin/flannel文件，这个文件先会读取/run/flannel/subnet.env文件，里面主要包含当前节点的子网信息，内容如下：

```bash
cat /run/flannel/subnet.env

FLANNEL_NETWORK=10.244.0.0/16
FLANNEL_SUBNET=10.244.1.1/24
FLANNEL_MTU=1450
FLANNEL_IPMASQ=true
```

> 这个文件也是kube-flannel启动时写入的

flannel读取该文件内容后，紧接着会生成一个符合cni标准的配置文件，内容如下：

```json
{
  "cniVersion": "0.3.0",
  "name": "networks",
  "type": "bridge",
  "bridge": "cni0",
  "isDefaultGateway": true,
  "ipam": {
    "type": "host-local",
    "subnet": "10.244.1.0/24",
    "dataDir": "/var/lib/cni/",
    "routes": [{ "dst": "0.0.0.0/0" }]
  }
}
```

> 其实可以一步到位，直接生成这个格式的文件放在/etc/cni/net.d/目录下，flannel这样处理应该是为了节点子网发生变化时不用重启kubelet吧

然后像kubelet调用flannel的方式一样调用另一个cni插件bridge，并把上面的配置文件的内容用标准输入的方式传递过去，调用方式如下：

```bash
echo '{ "cniVersion": "0.3.0", "name": "network", "type":"bridge","bridge":"cni0", "ipam":{"type":"host-local","subnet": "10.244.1.0/24","dataDir": "/var/lib/cni/","routes": [{ "dst": "0.0.0.0/0" }]}}' | CNI_COMMAND=ADD
CNI_CONTAINERID=xxx 
CNI_NETNS=/var/run/docker/netns/xxxx 
CNI_IFNAME=xxx 
CNI_ARGS='IgnoreUnknown=1;K8S_POD_NAMESPACE=applife;K8S_POD_NAME=redis-59b4c86fd9-wrmr9' 
CNI_PATH=/opt/cni/bin/ 
./bridge
```

> 后面我们动手编写cni插件时，可以用上述的方式来模拟kubelet调用cni，这样测试会方便很多

剩余的工作就会由/opt/cni/bin/bridge插件完成，它会：

- 在主机上创建一个名为cni0的linux bridge，然后把子网的第一个地址（如示例中：10.244.1.1）绑到cni0上，这样cni0同时也是该节点上所有pod的默认网关；
- 在主机上创建一条主机路由：`ip route add 10.244.1.0/24 dev cni0 scope link src 10.244.1.1`，这样一来，节点到本节点所有的pod就都会走cni0了；
- 创建veth网卡对，把一端插到新创建的pod的ns中，另一端插到cni0网桥上；
- 在pod的ns为刚刚创建的veth网卡设置IP，IP为host-local分配的值，默认网关设置为cni0的IP地址：10.244.1.1；
- 设置网卡的mtu，这个很关键，跟使用哪种跨节点通信方案相关，如果使用vxlan，一般就是1460，如果是host-gw，就是1500；

然后pod到主机、同主机的pod的通信就完成了，这就是flannel-cni完成的工作，只负责同节点pod的通信，对于跨节点pod通信由kube-flannel完成。

> host-local是以写本地文件的方式来标识哪些IP已经被占用，它会在/var/lib/cni/network/host-local/（这个目录其实是上面的dataDir参数指定的）目录下生成一些文件，文件名为已分配的IP，文件内容为使用该IP的容器ID，有一个指示当前已分配最新的IP的文件。

## kube-flannel

kube-flannel以k8s的daemonset方式运行，主要负责编织跨节点pod通信，启动后会完成以下几件事情：

- 启动容器会把/etc/kube-flannel/cni-conf.json文件复制到/etc/cni/net.d/10-flannel.conflist，这个文件是容器启动时从配置项挂载到容器上的，可以通过修改flannel部署的yaml文件来修改配置，选择使用其它的cni插件。
- 运行容器会从api-server中获取属于本节点的pod-cidr，然后写一个配置文件/run/flannel/subnet.env给flannel-cni用
- 如果是vxlan模式，则创建一个名为flannel.1的vxlan设备（关闭了自动学习机制），把这个设备的MAC地址和IP以及本节点的IP记录到节点的注解中。
- 启动一个协程，不断地检查本机的路由信息是否被删除，如果检查到缺失，则重新创建，防止误删导致网络不通的情况。
- 从api-server或etcd订阅资源变化的事件，维护路由表项、邻居表项、fdb表项

接下来介绍一下当kube-flannel收到节点新增事件时会完成的事情。

假设现在有一个k8s集群拥有master、node1和node2三个节点，这时候新增了一个节点node3，node3的IP为：192.168.3.10，node3上的kube-flannel为node3创建的vxlan设备IP地址为10.244.3.0，mac地址为：02:3f:39:67:7d:f9 ，相关的信息已经保存在节点的annotation上，用kubectl查看node3的节点信息如下：

```bash
[root@node1]# kubectl describe node node3

Name:               node3
...
Annotations:        flannel.alpha.coreos.com/backend-data: {"VtepMAC":"02:3f:39:67:7d:f9"}
                    flannel.alpha.coreos.com/backend-type: vxlan
                    flannel.alpha.coreos.com/kube-subnet-manager: true
                    flannel.alpha.coreos.com/public-ip: 192.168.3.10
...
PodCIDR: 10.244.3.0/24
```

node1上的kube-flannel收到node3的新增事件，会完成以下几件事：

- 新增一条到10.244.3.0/24的主机路由，并指示通过flannel.1设备走，下一跳为node3上的vxlan设备的IP地址`10.244.3.0`：

```bash
ip route add 10.244.3.0/24 via 10.244.3.0 dev flannel.1 onlink
```

- 新增一条邻居表信息，指示node3的vxlan设备10.244.3.0的mac地址为：`02:3f:39:67:7d:f9`,并用`nud permanent`指明该arp记录不会过期，不用做存活检查：

```bash
ip neigh add 10.244.3.0 lladdr 02:3f:39:67:7d:f9 dev flannel.1 nud permanent
```

- 新增一条fdb（forwarding database)记录，指明到node3的vxlan设备的mac地址的下一跳主机为node3的ip：

```bash
bridge fdb append  02:3f:39:67:7d:f9 dev vxlan0 dst 192.168.3.10 self permanent
```

- 如果在配置中启用了Directrouting，那么在这里会判断新增节点与当前节点是否在同一子网，如果是，则前面三步都不会发生，取而代之的是：

```bash
ip route add 10.244.3.0/24 via 192.168.3.10 dev eth0 onlink
```

> 注意这里的下一跳node3的节点IP，出口设备为eth0，这就是主机路由与vxlan模式下kube-flannel的主要区别

下面我们通过一个例子来介绍一下上面新增的这些记录的实际用途，假设：

- pod1运行在节点node1上，pod1的IP为`10.244.1.3`；
- pod2运行在节点node3，pod2的IP为`10.244.3.3`；

来看一下在vxlan模式下从pod1发送数据包到pod2的详细流程；

### 发送

1. 数据包从pod1出来，到达node1的协议栈，node1发现目标地址并非本机地址，且本机开启了流量转发功能，于是查找路由并转发；
2. 目标IP为`10.244.3.3`,主机路由匹配到应该走flannel.1设备，下一跳为`10.244.3.0`（上面的node3新增时，步骤一添加的路由表项就用上了）
3. 数据包到达flannel.1设备，它会先查找下一跳IP`10.244.3.0`的mac地址，在arp表中找到了匹配的记录为`02:3f:39:67:7d:f9`（上面节点新增时，步骤二添加的ARP记录在这里就用上了）,然后完成mac头封装，准备发送。
4. 因为是vxlan设备，发送方法与普通的网卡有些区别（详见下面的代码`vxlan_xmit`），数据包没有被提交到网卡的发送队列，而是由vxlan设备进一步封装成一个udp数据包，它会根据目标mac地址来反查下一跳的主机地址以决定把这个udp数据包发给哪个主机，这时候就会用到上面提到的fdb表了，它查到去往`02:3f:39:67:7d:f9`的下一跳主机地址为`192.168.3.10`（节点新增时，步骤三添加的FDB记录就用上了）,于是封装udp包，走`ip_local_out`，发往node3 。

```c
// linux-4.18\drivers\net\vxlan.c
static netdev_tx_t vxlan_xmit(struct sk_buff *skb, struct net_device *dev)
{
    ...
    //取链路层头部
    eth = eth_hdr(skb);
    // 根据目标mac地址查找fdb表项
    f = vxlan_find_mac(vxlan, eth->h_dest, vni);
    ...
    vxlan_xmit_one(skb, dev, vni, fdst, did_rsc);
}

static void vxlan_xmit_one(struct sk_buff *skb, struct net_device *dev,
               __be32 default_vni, struct vxlan_rdst *rdst,bool did_rsc)
{
...
        // 封装vxlan头
        err = vxlan_build_skb(skb, ndst, sizeof(struct iphdr),
                      vni, md, flags, udp_sum);
        if (err < 0)
            goto tx_error;

        // 封装UDP头、外部IP头，最后走ip_local_out
        udp_tunnel_xmit_skb(rt, sock4->sock->sk, skb, local_ip.sin.sin_addr.s_addr,
                    dst->sin.sin_addr.s_addr, tos, ttl, df,
                    src_port, dst_port, xnet, !udp_sum);
...
}
```

### 接收

1. node3接收到udp包后，走主机协议栈，发现目标地址为本机，于是走INPUT方向，最终发到UDP层处理。
2. 当我们创建vxlan设备时，vxlan的设备驱动会注册一个UDP的socket，端口默认为4789，然后为这个udp的socket的接收流程注册一个vxlan的接收函数；当linux协议栈的收包流程走到`udp_rcv`时，会调用`vxlan_rcv`处理，`vxlan_rcv`做的事情就是剥去vxlan头，将内部的一个完整的二层包重新送入主机协议栈（见下面的源码）。
3. 剥去vxlan头部后的包重新来到主机协议栈，此时包的目标地址是10.244.3.3，经过路由判决时，发现不是本机地址，走转发，找到合适的路由，最终发往pod2。

```c
// linux-4.18\drivers\net\vxlan.c
//创建vxlan设备时，会调用vxlan_open -> vxlan_sock_add -> __vxlan_sock_add -> vxlan_socket_create，最终会在这个方法中创建一个udp的socket，然后把vxlan的收包函数注册进来
static struct vxlan_sock *vxlan_socket_create(struct net *net, bool ipv6,
                          __be16 port, u32 flags)
{
...
    tunnel_cfg.encap_rcv = vxlan_rcv;   //这是最关键的点，收包的时候，会把vxlan的包给vxlan_rcv处理
...
}

int udp_rcv(struct sk_buff *skb)
{
    return __udp4_lib_rcv(skb, &udp_table, IPPROTO_UDP);
}

//udp包接收方法，从udp_rcv -> __udp4_lib_rcv -> udp_queue_rcv_skb，在这里，如果是vxlan设备创建的端口收的包，会给vxlan_rcv处理
static int udp_queue_rcv_skb(struct sock *sk, struct sk_buff *skb)
{
...
        /* if we're overly short, let UDP handle it */
        encap_rcv = READ_ONCE(up->encap_rcv);
        if (encap_rcv) {
            int ret;

            /* Verify checksum before giving to encap */
            if (udp_lib_checksum_complete(skb))
                goto csum_error;

            ret = encap_rcv(sk, skb);  //这里就会走到vxlan_rcv函数去
            if (ret <= 0) {
                __UDP_INC_STATS(sock_net(sk),
                        UDP_MIB_INDATAGRAMS,
                        is_udplite);
                return -ret;
            }
        }
...
}

/* Callback from net/ipv4/udp.c to receive packets */
static int vxlan_rcv(struct sock *sk, struct sk_buff *skb)
{
    //剥vxlan头    
    if (__iptunnel_pull_header(skb, VXLAN_HLEN, protocol, raw_proto,
                   !net_eq(vxlan->net, dev_net(vxlan->dev))))
            goto drop;
     ...
     gro_cells_receive(&vxlan->gro_cells, skb);
     ...
}

int gro_cells_receive(struct gro_cells *gcells, struct sk_buff *skb)
{
    ...
    if (!gcells->cells || skb_cloned(skb) || netif_elide_gro(dev))
        //非NAPI收包处理，linux虚拟网络设备接收如果需要软中断触发通常会走这里
        return netif_rx(skb);
    ...
}
```

## udp模式

在udp模式下，每个节点还运行了一个叫`flanneld`的守护进程，这个守护进程并非以容器的方式运行，而且是实实在在地参与数据包的转发工作，这个守护进程要是挂了，通信就会中断；

这个守护进程会：

- 开启一个unix domain socket服务，接受来自kube-flannel同步的路由信息；
- 打开/dev/net/tun文件；
- 打开一个udp端口并监听（默认是8285）
- 并且总会把udp端口收到的数据写到tun文件，从tun文件读到的数据，通过udp发出去；

每个节点同样存在一个名叫flannel.1的虚拟设备，只不过不是vxlan设备，而是一个tun设备，tun设备的工作原理是：用户态程序打开/dev/net/tun文件，主机就会多一张名为tun0的网卡，任何时候往这个打开的文件写的内容都会直接被内核协议栈收包，效果就是相当于上面代码中调用了`netif_rx(skb)`的效果，而发往这个tun0网卡的数据，都会被打开/dev/net/tun文件的用户程序读到，读到的内容包含IP包头及以上的全部内容（如果想读到链路层的帧头，这里就应该打开一个tap设备，tun/tap的主要区别就在这）；

udp模式下，kube-flannel也不再写fdb表和邻居表，而是通过unix domain socket 与本节点的`flanneld`守护进程通信，把从etcd订阅到的路由信息同步给flanneld。

我们继续用上面的场景举例，说明一下udp模式下的数据包发送流程：

- pod1发送给pod2的数据给会被主机路由引导通过tun设备（flannel.1）发送；
- `flanneld`进程从打开的/dev/net/tun文件收到来自pod1的数据包，目标地址是10.244.3.3，于是它要查找去往这个目标的下一跳是哪里，这个信息kube-flannel已同步，kube-flannel通过etcd可以获取到每一个pod在哪个节点中，并把pod和节点的IP的映射关系同步给flanneld；
- 它知道下一跳是node3后，就把从tun设备收到的包作为payload向node3的`flanneld`（端口8285）发送udp包，跟vxlan的封包的区别就是这里是没有链路层包头的相关信息的（上面说了，tun只能拿到三层及以上）
- node3运行的flanneld守护进程会收到这个来自node1的包，然后把payload向打开的/dev/net/tun文件写，根据tun设备的工作原理，它的另一端flannel.1网卡会收到这个包，然后就通过主机协议栈转发到pod2。

flanneld是由c语言直接实现的，关键代码在/backend/udp/proxy_adm64.c

```c
//tun网卡的包通过udp发给对端
static int tun_to_udp(int tun, int sock, char *buf, size_t buflen) {
  struct iphdr *iph;
  struct sockaddr_in *next_hop;
  ssize_t pktlen = tun_recv_packet(tun, buf, buflen);
  if( pktlen < 0 )
    return 0;
  iph = (struct iphdr *)buf;
  next_hop = find_route((in_addr_t) iph->daddr);
  if( !next_hop ) {
    send_net_unreachable(tun, buf);
    goto _active;
  }

  if( !decrement_ttl(iph) ) {
    /* TTL went to 0, discard.
     * TODO: send back ICMP Time Exceeded
     */
    goto _active;
  }
  sock_send_packet(sock, buf, pktlen, next_hop);
_active:
  return 1;
}

//从对端收到的包写到tun网卡
static int udp_to_tun(int sock, int tun, char *buf, size_t buflen) {
  struct iphdr *iph;
  ssize_t pktlen = sock_recv_packet(sock, buf, buflen);
  if( pktlen < 0 )
    return 0;
  iph = (struct iphdr *)buf;
  if( !decrement_ttl(iph) ) {
    /* TTL went to 0, discard.
     * TODO: send back ICMP Time Exceeded
     */
    goto _active;
  }
  tun_send_packet(tun, buf, pktlen);
_active:
  return 1;
}
```

udp模式中守护进程`flanneld`发挥的作用与vxlan设备很接近，都是在封包拆包，只不过vxlan封包拆包全程在内核态完成，而udp模式会经过4次用户与内核态切换，性能就下降了，而且udp模式下，flanneld挂了，通信就会中断；

## 0.9.0之前的版本

特别介绍一下flannel在0.9.0版本之前，用的策略完全不一样：

- kube-flannel不会在新增节点的时候就增加arp表和fdb表，而是在数据包传递的过程中，需要目标ip的mac地址但没有找到时会发送一个l3miss的消息（RTM_GETNEIGH）给用户态的进程，让用户进程补充邻居表信息；
- 在封装udp包时，在fdb表找不到mac地址对应的fdb表项时，会发送一个l2miss消息给用户态进程，让用户态的进程补充fdb表项，让流程接着往下走。

它启动时会打开下面的标志位：

```bash
echo 3 > /proc/sys/net/ipv4/neigh/flannel.1/app_solicit
```

这样vxlan在封包过程中如果缺少arp记录和fdb记录就会往用户进程发送消息

从0.9.0版本开始，flannel取消了监听netlink消息：

[[https://github.com/coreos/flannel/releases/tag/v0.9.0](https://link.zhihu.com/?target=https%3A//github.com/coreos/flannel/releases/tag/v0.9.0)]



可以看出，从0.9.0版本后的flannel在vxlan模式下，容器的通信完全由linux内核完成，已经不用kube-flannel参与了，这就意味着，哪怕在运行的过程中，kube-flannel挂掉了，也不会影响现有容器的通信，只会影响新加入的节点和新创建的容器。

## 同主机pod连接的几种方式及性能对比

本来说这一篇是要撸个cni出来的，但感觉这个没什么好说的，cni的源码github一大堆了，大概的套路也就是把前面说的命令用go语言实现一下，于是本着想到啥写啥的原则，我决定介绍一下相同主机的pod连接的另外几种方式及性能对比。

在本系列的第一篇文章中，我们介绍过pod用veth网卡连接主机，其实同主机的pod的连接方式一共有以下几种：

- veth连接主机，把主机当路由器用，第一篇文章就是介绍的这种方式，（下面我们简称：veth方式）
- 用linux bridge连接各个pod，把网关地址挂在linux bridge，flannel就是使用这种方式
- macvlan，使用场景有些限制
- ipvlan，对内核有要求，默认3.10是不支持的
- 开启eBPF支持

在这一章中我们专门来对比一下上面这几种方式的区别和性能。

因为eBPF对内核版本有要求，所以我使用的环境linux内核版本是4.18，普通的PC机，8核32G的配置；

> 在执行下面的命令时，注意创建的网卡名不要与主机的物理网卡冲突，笔者使用的主机网卡是eno2，所以我都是创建名为叫eth0的网卡，但这个网卡名在你的环境中可能很容易冲突，所以注意先修改一下

## veth方式

这种方式在第一篇文章中详细介绍过，所以就直接上命令了；

创建pod-a和pod-b：

```bash
ip netns add pod-a
ip link add eth0 type veth peer name veth-pod-a
ip link set eth0 netns pod-a
ip netns exec pod-a ip addr add 192.168.10.10/24 dev eth0
ip netns exec pod-a ip link set eth0 up
ip netns exec pod-a ip route add default via 169.254.10.24 dev eth0 onlink
ip link set veth-pod-a up
echo 1 > /proc/sys/net/ipv4/conf/veth-pod-a/proxy_arp
ip route add 192.168.10.10 dev veth-pod-a scope link

ip netns add pod-b
ip link add eth0 type veth peer name veth-pod-b
ip link set eth0 netns pod-b
ip netns exec pod-b ip addr add 192.168.10.11/24 dev eth0
ip netns exec pod-b ip link set eth0 up
ip netns exec pod-b ip route add default via 169.254.10.24 dev eth0 onlink
ip link set veth-pod-b up
echo 1 > /proc/sys/net/ipv4/conf/veth-pod-b/proxy_arp
ip route add 192.168.10.11 dev veth-pod-b scope link


echo 1 > /proc/sys/net/ipv4/ip_forward
iptables -I FORWARD -s 192.168.0.0/16 -d 192.168.0.0/16 -j ACCEPT
```

在pod-a中启动iperf3服务：

```bash
ip netns exec pod-a iperf3 -s
```

另开一个终端，在pod-b中请求pod-a，测试连接性能：

```bash
ip netns exec pod-b iperf3 -c 192.168.10.10 -i 1 -t 10

Connecting to host 192.168.10.10, port 5201
[  5] local 192.168.10.11 port 35014 connected to 192.168.10.10 port 5201
[ ID] Interval           Transfer     Bitrate         Retr  Cwnd
[  5]   0.00-1.00   sec  7.32 GBytes  62.9 Gbits/sec    0    964 KBytes
[  5]   1.00-2.00   sec  7.90 GBytes  67.8 Gbits/sec    0    964 KBytes
[  5]   2.00-3.00   sec  7.79 GBytes  66.9 Gbits/sec    0   1012 KBytes
[  5]   3.00-4.00   sec  7.92 GBytes  68.0 Gbits/sec    0   1012 KBytes
[  5]   4.00-5.00   sec  7.89 GBytes  67.8 Gbits/sec    0   1012 KBytes
[  5]   5.00-6.00   sec  7.87 GBytes  67.6 Gbits/sec    0   1012 KBytes
[  5]   6.00-7.00   sec  7.68 GBytes  66.0 Gbits/sec    0   1.16 MBytes
[  5]   7.00-8.00   sec  7.79 GBytes  66.9 Gbits/sec    0   1.27 MBytes
[  5]   8.00-9.00   sec  7.75 GBytes  66.5 Gbits/sec    0   1.47 MBytes
[  5]   9.00-10.00  sec  7.90 GBytes  67.8 Gbits/sec    0   1.47 MBytes
- - - - - - - - - - - - - - - - - - - - - - - - -
[ ID] Interval           Transfer     Bitrate         Retr
[  5]   0.00-10.00  sec  77.8 GBytes  66.8 Gbits/sec    0             sender
[  5]   0.00-10.04  sec  77.8 GBytes  66.6 Gbits/sec                  receiver
```

因为大多数时候，在部署在容器的应用间相互访问都是使用clusterIP的，所以也要测试一下用clusterIP访问，先用iptables创建clusterIP，这个我们在第二篇文章介绍过：

```bash
iptables -A PREROUTING -t nat -d 10.96.0.100 -j DNAT --to-destination 192.168.10.10
```

> 为了保证测试结果不受其它因素的干扰，最好确保主机上只有一条nat规则，这条nat规则可以全程使用，后面不再反复地删除并创建了

结果如下：

```bash
ip netns exec pod-b iperf3 -c 10.96.0.100 -i 1 -t 10

Connecting to host 10.96.0.100, port 5201
[  5] local 192.168.10.11 port 44528 connected to 10.96.0.100 port 5201
[ ID] Interval           Transfer     Bitrate         Retr  Cwnd
[  5]   0.00-1.00   sec  6.41 GBytes  55.0 Gbits/sec    0    725 KBytes
[  5]   1.00-2.00   sec  7.21 GBytes  61.9 Gbits/sec    0    902 KBytes
[  5]   2.00-3.00   sec  7.99 GBytes  68.6 Gbits/sec    0    902 KBytes
[  5]   3.00-4.00   sec  7.88 GBytes  67.7 Gbits/sec    0    902 KBytes
[  5]   4.00-5.00   sec  7.94 GBytes  68.2 Gbits/sec    0    947 KBytes
[  5]   5.00-6.00   sec  7.86 GBytes  67.5 Gbits/sec    0    947 KBytes
[  5]   6.00-7.00   sec  7.79 GBytes  66.9 Gbits/sec    0    947 KBytes
[  5]   7.00-8.00   sec  8.04 GBytes  69.1 Gbits/sec    0    947 KBytes
[  5]   8.00-9.00   sec  7.85 GBytes  67.5 Gbits/sec    0    996 KBytes
[  5]   9.00-10.00  sec  7.88 GBytes  67.7 Gbits/sec    0    996 KBytes
- - - - - - - - - - - - - - - - - - - - - - - - -
[ ID] Interval           Transfer     Bitrate         Retr
[  5]   0.00-10.00  sec  76.9 GBytes  66.0 Gbits/sec    0             sender
[  5]   0.00-10.04  sec  76.9 GBytes  65.8 Gbits/sec                  receiver
```

可以看到，在veth方式下，使用podIP或通过clusterIP访问pod在性能上区别是不大的，当然在iptables的规则很多的时候（例如2000个k8s服务），性能就会有影响了，但这并不是我们这一篇文章的重点；

清理一下现场，先停止iperf3服务，然后删除ns（上面的iptables规则留着）：

```bash
ip netns del pod-a
ip netns del pod-b
```

我们接着来试一下bridge方式。

## bridge方式

如果把bridge当成纯二层的交换机来负责两个pod的连接性能是很不错的，比上面用veth的方式要好，但是因为要支持k8s的serviceIP，所以有必要让数据包走一遍主机的iptables规则，所以一般都会给bridge挂个网关的IP，一来能响应pod的ARP请求，这样也就不用开启veth网卡对主机这一端的arp代答，再来这样能让数据包走一遍主机的netfilter的扩展函数，这样iptables规则就能生效了。

> 按理说linux bridge作为交换机是工作在二层，可是从源码中可以看到bridge是实实在在地执行了netfilter的几个hook点的函数的（PREROUTING/INPUT/FORWARD/OUTPUT/POSTROUTING），当然也有开关可以关闭这个功能（net.bridge.bridge-nf-call-iptables）

下面我们来测一下用bridge连接两个pod时的性能，创建br0的bridge然后把pod-a和pod-b都接上去：

```bash
ip link add br0 type bridge 
ip addr add 192.168.10.1 dev br0  ## 给br0挂pod的默认网关的IP
ip link set br0 up

ip netns add pod-a
ip link add eth0 type veth peer name veth-pod-a
ip link set eth0 netns pod-a
ip netns exec pod-a ip addr add 192.168.10.10/24 dev eth0
ip netns exec pod-a ip link set eth0 up
ip netns exec pod-a ip route add default via 192.168.10.1 dev eth0 onlink  ## 默认网关是br0的地址
ip link set veth-pod-a master br0  ## veth网卡主机这一端插到bridge上
ip link set veth-pod-a up

ip netns add pod-b
ip link add eth0 type veth peer name veth-pod-b
ip link set eth0 netns pod-b
ip netns exec pod-b ip addr add 192.168.10.11/24 dev eth0
ip netns exec pod-b ip link set eth0 up
ip netns exec pod-b ip route add default via 192.168.10.1 dev eth0 onlink
ip link set veth-pod-b master br0
ip link set veth-pod-b up

ip route add 192.168.10.0/24 via 192.168.10.1 dev br0 scope link  ## 主机到所有的pod的路由，下一跳为br0
```

再次在pod-a中运行iperf3：

```bash
ip netns exec pod-a iperf3 -s
```

在pod-b中测试连接性能：

```bash
ip netns exec pod-b iperf3 -c 192.168.10.10 -i 1 -t 10

Connecting to host 192.168.10.10, port 5201
[  5] local 192.168.10.11 port 38232 connected to 192.168.10.10 port 5201
[ ID] Interval           Transfer     Bitrate         Retr  Cwnd
[  5]   0.00-1.00   sec  7.64 GBytes  65.6 Gbits/sec    0    642 KBytes
[  5]   1.00-2.00   sec  7.71 GBytes  66.2 Gbits/sec    0    642 KBytes
[  5]   2.00-3.00   sec  7.49 GBytes  64.4 Gbits/sec    0    786 KBytes
[  5]   3.00-4.00   sec  7.61 GBytes  65.3 Gbits/sec    0    786 KBytes
[  5]   4.00-5.00   sec  7.54 GBytes  64.8 Gbits/sec    0    786 KBytes
[  5]   5.00-6.00   sec  7.71 GBytes  66.2 Gbits/sec    0    786 KBytes
[  5]   6.00-7.00   sec  7.66 GBytes  65.8 Gbits/sec    0    826 KBytes
[  5]   7.00-8.00   sec  7.63 GBytes  65.5 Gbits/sec    0    826 KBytes
[  5]   8.00-9.00   sec  7.64 GBytes  65.7 Gbits/sec    0    826 KBytes
[  5]   9.00-10.00  sec  7.71 GBytes  66.2 Gbits/sec    0    826 KBytes
- - - - - - - - - - - - - - - - - - - - - - - - -
[ ID] Interval           Transfer     Bitrate         Retr
[  5]   0.00-10.00  sec  76.3 GBytes  65.6 Gbits/sec    0             sender
[  5]   0.00-10.04  sec  76.3 GBytes  65.3 Gbits/sec                  receiver
```

与veth差距并不大，反复测了几次，都差不多，对于这个结果我觉得有点不科学，从源码上看，bridge转发的流程肯定要比走一遍主机的协议栈转发要快的，于是我想了一下，是不是把bridge执行netfilter扩展函数关闭会好一点呢？于是：

```bash
sysctl -w net.bridge.bridge-nf-call-iptables=0
```

再次试了一下：

```bash
ip netns exec pod-b iperf3 -c 192.168.10.10 -i 1 -t 10

Connecting to host 192.168.10.10, port 5201
[  5] local 192.168.10.11 port 40658 connected to 192.168.10.10 port 5201
[ ID] Interval           Transfer     Bitrate         Retr  Cwnd
[  5]   0.00-1.00   sec  8.55 GBytes  73.4 Gbits/sec    0    810 KBytes
[  5]   1.00-2.00   sec  8.86 GBytes  76.1 Gbits/sec    0    940 KBytes
[  5]   2.00-3.00   sec  8.96 GBytes  77.0 Gbits/sec    0    940 KBytes
[  5]   3.00-4.00   sec  9.04 GBytes  77.6 Gbits/sec    0    940 KBytes
[  5]   4.00-5.00   sec  8.89 GBytes  76.4 Gbits/sec    0    987 KBytes
[  5]   5.00-6.00   sec  9.18 GBytes  78.9 Gbits/sec    0    987 KBytes
[  5]   6.00-7.00   sec  9.09 GBytes  78.1 Gbits/sec    0    987 KBytes
[  5]   7.00-8.00   sec  9.10 GBytes  78.1 Gbits/sec    0   1.01 MBytes
[  5]   8.00-9.00   sec  8.98 GBytes  77.1 Gbits/sec    0   1.12 MBytes
[  5]   9.00-10.00  sec  9.13 GBytes  78.4 Gbits/sec    0   1.12 MBytes
- - - - - - - - - - - - - - - - - - - - - - - - -
[ ID] Interval           Transfer     Bitrate         Retr
[  5]   0.00-10.00  sec  89.8 GBytes  77.1 Gbits/sec    0             sender
[  5]   0.00-10.04  sec  89.8 GBytes  76.8 Gbits/sec                  receiver
```

果然，是会快许多的，但这结果多少令我也有点吃惊，我已经确保主机上只有一条iptables规则，只是开启了bridge执行netfilter扩展函数居然前后会相差10Gbits/sec。

但是，这个标志是不能关的，前面说了，要执行iptables规则把clusterIP转成podIP，所以还是要开起来：

```bash
sysctl -w net.bridge.bridge-nf-call-iptables=1
```

这时候用clusterIP试试：

```bash
ip netns exec pod-b iperf3 -c 10.96.0.100 -i 1 -t 10

Connecting to host 10.96.0.100, port 5201
[  5] local 192.168.10.11 port 47414 connected to 10.96.0.100 port 5201
[ ID] Interval           Transfer     Bitrate         Retr  Cwnd
[  5]   0.00-1.00   sec  7.02 GBytes  60.3 Gbits/sec    0    669 KBytes
[  5]   1.00-2.00   sec  7.23 GBytes  62.1 Gbits/sec    0    738 KBytes
[  5]   2.00-3.00   sec  7.17 GBytes  61.6 Gbits/sec    0    899 KBytes
[  5]   3.00-4.00   sec  7.21 GBytes  62.0 Gbits/sec    0    899 KBytes
[  5]   4.00-5.00   sec  7.31 GBytes  62.8 Gbits/sec    0    899 KBytes
[  5]   5.00-6.00   sec  7.19 GBytes  61.8 Gbits/sec    0   1008 KBytes
[  5]   6.00-7.00   sec  7.24 GBytes  62.2 Gbits/sec    0   1008 KBytes
[  5]   7.00-8.00   sec  7.22 GBytes  62.0 Gbits/sec    0   1.26 MBytes
[  5]   8.00-9.00   sec  6.99 GBytes  60.0 Gbits/sec    0   1.26 MBytes
[  5]   9.00-10.00  sec  7.07 GBytes  60.8 Gbits/sec    0   1.26 MBytes
- - - - - - - - - - - - - - - - - - - - - - - - -
[ ID] Interval           Transfer     Bitrate         Retr
[  5]   0.00-10.00  sec  71.6 GBytes  61.5 Gbits/sec    0             sender
[  5]   0.00-10.04  sec  71.6 GBytes  61.3 Gbits/sec                  receiver
```

反复试了几次，大概都是这个值，可以看到，使用clusterIP比直接用podIP访问性能下降了8%；

接着来测macvlan，先清理一下现场：

```bash
ip netns del pod-a
ip netns del pod-b
ip link del br0
```

## macvlan

macvlan模式是从一个物理网卡虚拟出多个虚拟网络接口，每个虚拟的接口都有单独的mac地址，可以给这些虚拟接口配置IP地址，在bridge模式下（其它几种模式不适用，所以不作讨论），父接口作为交换机来完成子接口间的通信，子接口可以通过父接口访问外网；

我们使用bridge模式：

```bash
ip link add link eno2 name eth0 type macvlan mode bridge  ## eno2是我的物理网卡名称，eth0是我虚拟出来的接口名，请根据你的实际情况修改
ip netns add pod-a
ip l set eth0 netns pod-a
ip netns exec pod-a ip addr add 192.168.10.10/24 dev eth0
ip netns exec pod-a ip link set eth0 up
ip netns exec pod-a ip route add default via 192.168.10.1 dev eth0  

ip link add link eno2 name eth0 type macvlan mode bridge
ip netns add pod-b
ip l set eth0 netns pod-b
ip netns exec pod-b ip addr add 192.168.10.11/24 dev eth0
ip netns exec pod-b ip link set eth0 up
ip netns exec pod-b ip route add default via 192.168.10.1 dev eth0

ip link add link eno2 name eth0 type macvlan mode bridge
ip addr add 192.168.10.1/24 dev eth0  ## 多创建一个子接口，留在主机上，把pod的默认网关的IP挂这里，这样pod里面请求clusterIP的流量会走到主机来，主机协议栈的iptables规则就有机会执行了
ip link set eth0 up

iptables -A POSTROUTING -t nat -s 192.168.10.0/24 -d 192.168.10.0/24 -j MASQUERADE  ## 要让回包也经过主机协议栈，所以要做源地址转换
```

测试结果：

```bash
ip netns exec pod-b iperf3 -c 192.168.10.10 -i 1 -t 10

Connecting to host 192.168.10.10, port 5201
[  5] local 192.168.10.11 port 47050 connected to 192.168.10.10 port 5201
[ ID] Interval           Transfer     Bitrate         Retr  Cwnd
[  5]   0.00-1.00   sec  9.47 GBytes  81.3 Gbits/sec    0    976 KBytes
[  5]   1.00-2.00   sec  9.81 GBytes  84.3 Gbits/sec    0    976 KBytes
[  5]   2.00-3.00   sec  9.74 GBytes  83.6 Gbits/sec    0   1.16 MBytes
[  5]   3.00-4.00   sec  9.77 GBytes  83.9 Gbits/sec    0   1.16 MBytes
[  5]   4.00-5.00   sec  9.73 GBytes  83.6 Gbits/sec    0   1.16 MBytes
[  5]   5.00-6.00   sec  9.69 GBytes  83.2 Gbits/sec    0   1.16 MBytes
[  5]   6.00-7.00   sec  9.75 GBytes  83.7 Gbits/sec    0   1.22 MBytes
[  5]   7.00-8.00   sec  9.78 GBytes  84.0 Gbits/sec    0   1.30 MBytes
[  5]   8.00-9.00   sec  9.81 GBytes  84.3 Gbits/sec    0   1.30 MBytes
[  5]   9.00-10.00  sec  9.84 GBytes  84.5 Gbits/sec    0   1.30 MBytes
- - - - - - - - - - - - - - - - - - - - - - - - -
[ ID] Interval           Transfer     Bitrate         Retr
[  5]   0.00-10.00  sec  97.4 GBytes  83.6 Gbits/sec    0             sender
[  5]   0.00-10.04  sec  97.4 GBytes  83.3 Gbits/sec                  receiver
```

直接用podIP访问是非常快的，几种方式中最快的；

用clusterIP试试：

```bash
ip netns exec pod-b iperf3 -c 10.96.0.100 -i 1 -t 10

Connecting to host 10.96.0.100, port 5201
[  5] local 192.168.10.11 port 35780 connected to 10.96.0.100 port 5201
[ ID] Interval           Transfer     Bitrate         Retr  Cwnd
[  5]   0.00-1.00   sec  7.16 GBytes  61.5 Gbits/sec    0    477 KBytes
[  5]   1.00-2.00   sec  7.18 GBytes  61.7 Gbits/sec    0    477 KBytes
[  5]   2.00-3.00   sec  7.13 GBytes  61.2 Gbits/sec    0    608 KBytes
[  5]   3.00-4.00   sec  7.18 GBytes  61.7 Gbits/sec    0    670 KBytes
[  5]   4.00-5.00   sec  7.16 GBytes  61.5 Gbits/sec    0    670 KBytes
[  5]   5.00-6.00   sec  7.30 GBytes  62.7 Gbits/sec    0    822 KBytes
[  5]   6.00-7.00   sec  7.34 GBytes  63.1 Gbits/sec    0    822 KBytes
[  5]   7.00-8.00   sec  7.30 GBytes  62.7 Gbits/sec    0   1.00 MBytes
[  5]   8.00-9.00   sec  7.19 GBytes  61.8 Gbits/sec    0   1.33 MBytes
[  5]   9.00-10.00  sec  7.15 GBytes  61.4 Gbits/sec    0   1.33 MBytes
- - - - - - - - - - - - - - - - - - - - - - - - -
[ ID] Interval           Transfer     Bitrate         Retr
[  5]   0.00-10.00  sec  72.1 GBytes  61.9 Gbits/sec    0             sender
[  5]   0.00-10.04  sec  72.1 GBytes  61.7 Gbits/sec                  receiver
```

走一遍主机的内核协议栈就下降了将近25%；

清理一下现场：

```bash
ip netns del pod-a
ip netns del pod-b
iptables -D POSTROUTING -t nat -s 192.168.10.0/24 -d 192.168.10.0/24 -j MASQUERADE
```

## ipvlan

与macvlan类似，ipvlan也是在一个物理网卡上虚拟出多个子接口，与macvlan不同的是，ipvlan的每一个子接口的mac地址是一样的，IP地址不同；

ipvlan有l2和l3模式，l2模式下，与macvlan的工作原理类似，父接口作为交换机来转发子接口的数据包，不同的是，ipvlan的流量转发时是通过dmac==smac来判断这是子接口间的通信的；

l2模式：

```bash
ip l add link eno2 name eth0 type ipvlan mode l2
ip netns add pod-a
ip l set eth0 netns pod-a
ip netns exec pod-a ip addr add 192.168.10.10/24 dev eth0
ip netns exec pod-a ip link set eth0 up
ip netns exec pod-a ip route add default via 192.168.10.1 dev eth0

ip l add link eno2 name eth0 type ipvlan mode l2
ip netns add pod-b
ip l set eth0 netns pod-b
ip netns exec pod-b ip addr add 192.168.10.11/24 dev eth0
ip netns exec pod-b ip link set eth0 up
ip netns exec pod-b ip route add default via 192.168.10.1 dev eth0

ip link add link eno2 name eth0 type ipvlan mode l2
ip link set eth0 up
ip addr add 192.168.10.1/24 dev eth0

iptables -A POSTROUTING -t nat -s 192.168.10.0/24 -d 192.168.10.0/24 -j MASQUERADE  ##跟上面的一样，也是要让回包经过主机协议栈，所以要做源地址转换
```

测试结果：

```bash
ip netns exec pod-b iperf3 -c 192.168.10.10 -i 1 -t 10

Connecting to host 192.168.10.10, port 5201
[  5] local 192.168.10.11 port 59580 connected to 192.168.10.10 port 5201
[ ID] Interval           Transfer     Bitrate         Retr  Cwnd
[  5]   0.00-1.00   sec  9.70 GBytes  83.3 Gbits/sec    0    748 KBytes
[  5]   1.00-2.00   sec  9.71 GBytes  83.4 Gbits/sec    0    748 KBytes
[  5]   2.00-3.00   sec  10.1 GBytes  86.9 Gbits/sec    0    748 KBytes
[  5]   3.00-4.00   sec  9.84 GBytes  84.5 Gbits/sec    0    826 KBytes
[  5]   4.00-5.00   sec  9.82 GBytes  84.3 Gbits/sec    0    826 KBytes
[  5]   5.00-6.00   sec  9.74 GBytes  83.6 Gbits/sec    0   1.19 MBytes
[  5]   6.00-7.00   sec  9.77 GBytes  83.9 Gbits/sec    0   1.19 MBytes
[  5]   7.00-8.00   sec  9.53 GBytes  81.8 Gbits/sec    0   1.41 MBytes
[  5]   8.00-9.00   sec  9.56 GBytes  82.1 Gbits/sec    0   1.41 MBytes
[  5]   9.00-10.00  sec  9.54 GBytes  82.0 Gbits/sec    0   1.41 MBytes
- - - - - - - - - - - - - - - - - - - - - - - - -
[ ID] Interval           Transfer     Bitrate         Retr
[  5]   0.00-10.00  sec  97.3 GBytes  83.6 Gbits/sec    0             sender
[  5]   0.00-10.04  sec  97.3 GBytes  83.3 Gbits/sec                  receiver
```

结果显示，ipvlan的l2模式下，同主机的pod通信的性能和macvlan差不多，l3模式下也差不多，所以就不展示了；

使用clusterIP访问：

```bash
ip netns exec pod-b iperf3 -c 10.96.0.100 -i 1 -t 10

Connecting to host 10.96.0.100, port 5201
[  5] local 192.168.10.11 port 38540 connected to 10.96.0.100 port 5201
[ ID] Interval           Transfer     Bitrate         Retr  Cwnd
[  5]   0.00-1.00   sec  7.17 GBytes  61.6 Gbits/sec    0    611 KBytes
[  5]   1.00-2.00   sec  7.22 GBytes  62.0 Gbits/sec    0    708 KBytes
[  5]   2.00-3.00   sec  7.31 GBytes  62.8 Gbits/sec    0    708 KBytes
[  5]   3.00-4.00   sec  7.29 GBytes  62.6 Gbits/sec    0    833 KBytes
[  5]   4.00-5.00   sec  7.27 GBytes  62.4 Gbits/sec    0    833 KBytes
[  5]   5.00-6.00   sec  7.36 GBytes  63.3 Gbits/sec    0    833 KBytes
[  5]   6.00-7.00   sec  7.26 GBytes  62.4 Gbits/sec    0    874 KBytes
[  5]   7.00-8.00   sec  7.19 GBytes  61.8 Gbits/sec    0    874 KBytes
[  5]   8.00-9.00   sec  7.17 GBytes  61.6 Gbits/sec    0    874 KBytes
[  5]   9.00-10.00  sec  7.28 GBytes  62.5 Gbits/sec    0    874 KBytes
- - - - - - - - - - - - - - - - - - - - - - - - -
[ ID] Interval           Transfer     Bitrate         Retr
[  5]   0.00-10.00  sec  72.5 GBytes  62.3 Gbits/sec    0             sender
[  5]   0.00-10.04  sec  72.5 GBytes  62.0 Gbits/sec                  receiver
```

可以看到，使用clusterIP访问相比直接用podIP，性能下降了25%，而且还有个问题，同主机pod之间的访问不需要经过iptables规则，所以network policy无法生效，如果在ipvlan或macvlan的模式下，能很好解决clusterIP的问题就好了，下面我们来试试直接在pod内给网卡附加eBPF程序解决clusterIP的问题

## ipvlan模式下附加eBPF程序

下面的方式因为需要附加我们自定义的eBPF程序（mst_lxc.o），所以各位就不能跟着做了，看个结果吧；

pod-b的eth0网卡的tc ingress和tc egress附加eBPF程序（因为是在pod里面，所以附加的程序刚好是反过来的，因为eBPF程序写的时候，针对的是主机的网卡）：

```bash
ip netns exec pod-b bash
ulimit -l unlimited
tc qdisc add dev eth0 clsact
tc filter add dev eth0 ingress prio 1 handle 1 bpf da obj mst_lxc.o sec lxc-egress   #ingress方向附加lxc-egress，主要完成rev-DNAT：podIP->clusterIP
tc filter add dev eth0 egress prio 1 handle 1 bpf da obj mst_lxc.o sec lxc-ingress   #egress方向完成DNAT：clusterIP->podIP
```

增加svc及后端（功能和上面的iptables的DNAT规则的功能是类似的）

```bash
mustang svc add --service=10.96.0.100:5201 --backend=192.168.10.10:5201

I0908 09:51:35.754539    5694 bpffs_linux.go:260] Detected mounted BPF filesystem at /sys/fs/bpf
I0908 09:51:35.891046    5694 service.go:578] Restored services from maps
I0908 09:51:35.891103    5694 bpf_svc_add.go:86] created success,id:1
```

查看一下配置（mustang工具是我们自定义的用户态工具，用来操作eBPF的map）

```bash
mustang svc ls

==========================================================================
Mustang Service count:1
==========================================================================
id      pro     service         port    backends
--------------------------------------------------------------------------
1       NONE    10.96.0.100     5201    192.168.10.10:5201,
==========================================================================
```

一切准备就绪，这时候再来测试用clusterIP访问pod-a：

```bash
ip netns exec pod-b iperf3 -c 10.96.0.100 -i 1 -t 10

Connecting to host 10.96.0.100, port 5201
[  5] local 192.168.10.11 port 57152 connected to 10.96.0.100 port 5201
[ ID] Interval           Transfer     Bitrate         Retr  Cwnd
[  5]   0.00-1.00   sec  8.96 GBytes  77.0 Gbits/sec    0   1.04 MBytes
[  5]   1.00-2.00   sec  8.83 GBytes  75.8 Gbits/sec    0   1.26 MBytes
[  5]   2.00-3.00   sec  9.13 GBytes  78.4 Gbits/sec    0   1.46 MBytes
[  5]   3.00-4.00   sec  9.10 GBytes  78.2 Gbits/sec    0   1.46 MBytes
[  5]   4.00-5.00   sec  9.37 GBytes  80.5 Gbits/sec    0   1.46 MBytes
[  5]   5.00-6.00   sec  9.44 GBytes  81.1 Gbits/sec    0   1.46 MBytes
[  5]   6.00-7.00   sec  9.14 GBytes  78.5 Gbits/sec    0   1.46 MBytes
[  5]   7.00-8.00   sec  9.36 GBytes  80.4 Gbits/sec    0   1.68 MBytes
[  5]   8.00-9.00   sec  9.11 GBytes  78.3 Gbits/sec    0   1.68 MBytes
[  5]   9.00-10.00  sec  9.29 GBytes  79.8 Gbits/sec    0   1.68 MBytes
- - - - - - - - - - - - - - - - - - - - - - - - -
[ ID] Interval           Transfer     Bitrate         Retr
[  5]   0.00-10.00  sec  91.7 GBytes  78.8 Gbits/sec    0             sender
[  5]   0.00-10.04  sec  91.7 GBytes  78.5 Gbits/sec                  receiver
```

可以看到，在ipvlan模式下，附加eBPF程序来实现clusterIP后性能大大提升了，相对于直接用podIP来访问，性能只是有不到5%的损耗，相对于用主机的iptables规则实现clusterIP性能提升了20%，也是上述所有方案中最优的一种，我们自研的cni（mustang）支持这种方式，同时也支持veth方式上附加eBPF程序的方式，下面是veth附加eBPF程序的测试结果；

> 这里要先清理一下现场

## veth方式附加eBPF程序

还是先创建pod-a和pod-b：

```bash
ip netns add pod-a
ip link add eth0 type veth peer name veth-pod-a
ip link set eth0 netns pod-a
ip netns exec pod-a ip addr add 192.168.10.10/24 dev eth0
ip netns exec pod-a ip link set eth0 up
ip netns exec pod-a ip route add default via 169.254.10.24 dev eth0 onlink
ip link set veth-pod-a up
echo 1 > /proc/sys/net/ipv4/conf/veth-pod-a/proxy_arp
ip route add 192.168.10.10 dev veth-pod-a scope link

ip netns add pod-b
ip link add eth0 type veth peer name veth-pod-b
ip link set eth0 netns pod-b
ip netns exec pod-b ip addr add 192.168.10.11/24 dev eth0
ip netns exec pod-b ip link set eth0 up
ip netns exec pod-b ip route add default via 169.254.10.24 dev eth0 onlink
ip link set veth-pod-b up
echo 1 > /proc/sys/net/ipv4/conf/veth-pod-b/proxy_arp
ip route add 192.168.10.11 dev veth-pod-b scope link

echo 1 > /proc/sys/net/ipv4/ip_forward
```

附加eBPF程序

给pod-a和pod-b主机一端的网卡的tc ingress和tc egress都附加eBPF程序：

```bash
tc qdisc add dev veth-pod-b clsact
tc filter add dev veth-pod-b ingress prio 1 handle 1 bpf da obj mst_lxc.o sec lxc-ingress  ## 因为这是附加在主机一端的网卡，与附加在容器时的方向是反的
tc filter add dev veth-pod-b egress prio 1 handle 1 bpf da obj mst_lxc.o sec lxc-egress

tc qdisc add dev veth-pod-a clsact
tc filter add dev veth-pod-a ingress prio 1 handle 1 bpf da obj mst_lxc.o sec lxc-ingress
tc filter add dev veth-pod-a egress prio 1 handle 1 bpf da obj mst_lxc.o sec lxc-egress
```

增加svc和增加endpoint（为了对数据包进行快速重定向）：

```bash
mustang svc add --service=10.96.0.100:5201 --backend=192.168.10.10:5201
mustang ep add --ifname=eth0 --netns=/var/run/netns/pod-a
mustang ep add --ifname=eth0 --netns=/var/run/netns/pod-b
```

查看一下配置

```bash
mustang svc ls
==========================================================================
Mustang Service count:1
==========================================================================
id      pro     service         port    backends
--------------------------------------------------------------------------
1       NONE    10.96.0.100     5201    192.168.10.10:5201,
==========================================================================

mustang ep ls
==========================================================================
Mustang Endpoint count:2
==========================================================================
Id      IP              Host    IfIndex         LxcMAC                  NodeMAC
--------------------------------------------------------------------------
1       192.168.10.10   false   653             76:6C:37:2C:81:05       3E:E9:02:96:60:D6
2       192.168.10.11   false   655             6A:CD:11:13:76:2C       72:90:74:4A:CB:84
==========================================================================
```

可以开测了，老套路，pod-a跑服务端，在pod-b上测，先试试用clusterIP：

```bash
ip netns exec pod-b iperf3 -c 10.96.0.100 -i 1 -t 10
Connecting to host 10.96.0.100, port 5201
[  5] local 192.168.10.11 port 36492 connected to 10.96.0.100 port 5201
[ ID] Interval           Transfer     Bitrate         Retr  Cwnd
[  5]   0.00-1.00   sec  8.52 GBytes  73.2 Gbits/sec    0   1.07 MBytes
[  5]   1.00-2.00   sec  8.54 GBytes  73.4 Gbits/sec    0   1.07 MBytes
[  5]   2.00-3.00   sec  8.64 GBytes  74.2 Gbits/sec    0   1.07 MBytes
[  5]   3.00-4.00   sec  8.57 GBytes  73.6 Gbits/sec    0   1.12 MBytes
[  5]   4.00-5.00   sec  8.61 GBytes  73.9 Gbits/sec    0   1.18 MBytes
[  5]   5.00-6.00   sec  8.48 GBytes  72.8 Gbits/sec    0   1.18 MBytes
[  5]   6.00-7.00   sec  8.57 GBytes  73.6 Gbits/sec    0   1.18 MBytes
[  5]   7.00-8.00   sec  9.11 GBytes  78.3 Gbits/sec    0   1.18 MBytes
[  5]   8.00-9.00   sec  8.86 GBytes  76.1 Gbits/sec    0   1.18 MBytes
[  5]   9.00-10.00  sec  8.71 GBytes  74.8 Gbits/sec    0   1.18 MBytes
- - - - - - - - - - - - - - - - - - - - - - - - -
[ ID] Interval           Transfer     Bitrate         Retr
[  5]   0.00-10.00  sec  86.6 GBytes  74.4 Gbits/sec    0             sender
[  5]   0.00-10.04  sec  86.6 GBytes  74.1 Gbits/sec                  receiver
```

再试试直接用podIP：

```bash
ip netns exec pod-b iperf3 -c 192.168.10.10 -i 1 -t 10
Connecting to host 192.168.10.10, port 5201
[  5] local 192.168.10.11 port 56460 connected to 192.168.10.10 port 5201
[ ID] Interval           Transfer     Bitrate         Retr  Cwnd
[  5]   0.00-1.00   sec  8.76 GBytes  75.3 Gbits/sec    0    676 KBytes
[  5]   1.00-2.00   sec  8.87 GBytes  76.2 Gbits/sec    0    708 KBytes
[  5]   2.00-3.00   sec  8.78 GBytes  75.5 Gbits/sec    0    708 KBytes
[  5]   3.00-4.00   sec  8.99 GBytes  77.2 Gbits/sec    0    708 KBytes
[  5]   4.00-5.00   sec  8.85 GBytes  76.1 Gbits/sec    0    782 KBytes
[  5]   5.00-6.00   sec  8.98 GBytes  77.1 Gbits/sec    0    782 KBytes
[  5]   6.00-7.00   sec  8.64 GBytes  74.2 Gbits/sec    0   1.19 MBytes
[  5]   7.00-8.00   sec  8.40 GBytes  72.2 Gbits/sec    0   1.55 MBytes
[  5]   8.00-9.00   sec  8.16 GBytes  70.1 Gbits/sec    0   1.88 MBytes
[  5]   9.00-10.00  sec  8.16 GBytes  70.1 Gbits/sec    0   1.88 MBytes
- - - - - - - - - - - - - - - - - - - - - - - - -
[ ID] Interval           Transfer     Bitrate         Retr
[  5]   0.00-10.00  sec  86.6 GBytes  74.4 Gbits/sec    0             sender
[  5]   0.00-10.04  sec  86.6 GBytes  74.1 Gbits/sec                  receiver
```

可以看到，附加eBPF程序后，用PodIP访问比原来性能提升了12%左右（见最上面veth方式的测试结果，66Gbits/sec），且clusterIP访问和podIP访问几乎没有差异；

## 总结

- veth ：（PODIP）66Gbits/sec （clusterIP）66Gbits/sec
- bridge : （PODIP）77Gbits/sec （clusterIP）61Gbits/sec
- macvlan ：（PODIP）83Gbits/sec （clusterIP）62Gbits/sec
- ipvlan ：（PODIP）83Gbits/sec （clusterIP）62Gbits/sec
- ipvlan+eBPF：（PODIP）83Gbits/sec （clusterIP）78Gbits/sec
- veth+eBPF ：（PODIP）74Gbits/sec （clusterIP）74Gbits/sec

![img](https://pic3.zhimg.com/80/v2-6b30907e6a04cfb6479117e731ec6a8a_1440w.webp)

同主机pod连接方式的性能对比

综上所述：

- macvlan和ipvlan在使用podIP访问时性能是所有方案中最高的，但clusterIP的访问因为走了主机协议栈，降了25%，有eBPF加持后又提升了20%，不过macvlan在无线网卡不支持，且单网卡mac数量有限制，不支持云平台源目的检查等，所以一般都较为推荐ipvlan+eBPF方式，不过这种方式下附加eBPF程序还是有点点麻烦，上面演示时为了简洁直接把eBPF的map在pod里创建了，实际是在主机上创建eBPF的map，然后让所有的pod共享这份eBPF的map；
- veth方式附加eBPF程序后，用serviceIP和直接用podIP性能上没有差异，且比不附加eBPF程序性能有12%的提升，而且还可以用主机上的iptables防火墙规则，在主机端附加eBPF程序比较简单，所以这是我们的mustang默认的方案；
- bridge在podIP访问时性能是比veth方式高的，但因为执行iptables规则性能被拖低了，所以在不附加eBPF的情况下，还是比较推荐veth方式，这是calico的默认方案；bridge方式是flannel的默认方案