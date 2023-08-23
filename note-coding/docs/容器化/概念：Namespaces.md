# Kubernetes 组件

> 来源：http://docs.kubernetes.org.cn/230.html

- 1 Master 组件
  - [1.1 kube-apiserver](http://docs.kubernetes.org.cn/230.html#kube-apiserver)
  - [1.2 ETCD](http://docs.kubernetes.org.cn/230.html#ETCD)
  - [1.3 kube-controller-manager](http://docs.kubernetes.org.cn/230.html#kube-controller-manager)
  - [1.4 cloud-controller-manager](http://docs.kubernetes.org.cn/230.html#cloud-controller-manager)
  - [1.5 kube-scheduler](http://docs.kubernetes.org.cn/230.html#kube-scheduler)
  - 1.6 插件 addons
    - [1.6.1 DNS](http://docs.kubernetes.org.cn/230.html#DNS)
    - [1.6.2 用户界面](http://docs.kubernetes.org.cn/230.html#i)
    - [1.6.3 容器资源监测](http://docs.kubernetes.org.cn/230.html#i-2)
    - [1.6.4 Cluster-level Logging](http://docs.kubernetes.org.cn/230.html#Cluster-level_Logging)
- 2 节点（Node）组件
  - [2.1 kubelet](http://docs.kubernetes.org.cn/230.html#kubelet)
  - [2.2 kube-proxy](http://docs.kubernetes.org.cn/230.html#kube-proxy)
  - [2.3 docker](http://docs.kubernetes.org.cn/230.html#docker)
  - [2.4 RKT](http://docs.kubernetes.org.cn/230.html#RKT)
  - [2.5 supervisord](http://docs.kubernetes.org.cn/230.html#supervisord)
  - [2.6 fluentd](http://docs.kubernetes.org.cn/230.html#fluentd)

本文介绍了Kubernetes集群所需的各种二进制组件。

## Master 组件

Master组件提供集群的管理控制中心。

Master组件可以在集群中任何节点上运行。但是为了简单起见，通常在一台VM/机器上启动所有Master组件，并且不会在此VM/机器上运行用户容器。请参考 [构建高可用群集](https://kubernetes.io/docs/admin/high-availability)以来构建multi-master-VM。

### kube-apiserver

[kube-apiserver](https://kubernetes.io/docs/admin/kube-apiserver)用于暴露Kubernetes API。任何的资源请求/调用操作都是通过kube-apiserver提供的接口进行。请参阅[构建高可用群集](https://kubernetes.io/docs/admin/high-availability)。

### ETCD

[etcd](https://kubernetes.io/docs/admin/etcd)是Kubernetes提供默认的存储系统，保存所有集群数据，使用时需要为etcd数据提供备份计划。



### kube-controller-manager

[kube-controller-manager](https://kubernetes.io/docs/admin/kube-controller-manager)运行管理控制器，它们是集群中处理常规任务的后台线程。逻辑上，每个控制器是一个单独的进程，但为了降低复杂性，它们都被编译成单个二进制文件，并在单个进程中运行。

具体控制器包括：

- [节点（Node）控制器](http://docs.kubernetes.org.cn/304.html)。
- 副本（Replication）控制器：负责维护系统中每个副本中的pod。
- 端点（Endpoints）控制器：填充Endpoints对象（即连接Services＆Pods）。
- [Service Account](http://docs.kubernetes.org.cn/84.html)和Token控制器：为新的[Namespace](http://docs.kubernetes.org.cn/242.html) 创建默认帐户访问API Token。

### cloud-controller-manager

云控制器管理器负责与底层云提供商的平台交互。云控制器管理器是Kubernetes版本1.6中引入的，目前还是Alpha的功能。

云控制器管理器仅运行云提供商特定的（controller loops）控制器循环。可以通过将`--cloud-provider` flag设置为external启动kube-controller-manager ，来禁用控制器循环。

cloud-controller-manager 具体功能：

- 节点（Node）控制器
- 路由（Route）控制器
- Service控制器
- 卷（Volume）控制器

### kube-scheduler

kube-scheduler 监视新创建没有分配到[Node](http://docs.kubernetes.org.cn/304.html)的[Pod](http://docs.kubernetes.org.cn/312.html)，为Pod选择一个Node。

### 插件 addons

插件（addon）是实现集群pod和Services功能的 。Pod由[Deployments](http://docs.kubernetes.org.cn/317.html)，ReplicationController等进行管理。Namespace 插件对象是在kube-system Namespace中创建。

#### DNS

虽然不严格要求使用插件，但Kubernetes集群都应该具有集群 DNS。

群集 DNS是一个DNS服务器，能够为 Kubernetes services提供 DNS记录。

由Kubernetes启动的容器自动将这个DNS服务器包含在他们的DNS searches中。

了解[更多详情](https://www.kubernetes.org.cn/542.html)

#### 用户界面

kube-ui提供集群状态基础信息查看。更多详细信息，请参阅[使用HTTP代理访问Kubernetes API](https://kubernetes.io/docs/tasks/access-kubernetes-api/http-proxy-access-api/)

#### 容器资源监测

[容器资源监控](https://kubernetes.io/docs/user-guide/monitoring)提供一个UI浏览监控数据。

#### Cluster-level Logging

[Cluster-level logging](https://kubernetes.io/docs/user-guide/logging/overview)，负责保存容器日志，搜索/查看日志。

## 节点（Node）组件

节点组件运行在[Node](http://docs.kubernetes.org.cn/304.html)，提供Kubernetes运行时环境，以及维护Pod。

### kubelet

[kubelet](https://kubernetes.io/docs/admin/kubelet)是主要的节点代理，它会监视已分配给节点的pod，具体功能：

- 安装Pod所需的volume。
- 下载Pod的Secrets。
- Pod中运行的 docker（或experimentally，rkt）容器。
- 定期执行容器健康检查。
- Reports the status of the pod back to the rest of the system, by creating a *mirror pod* if necessary.
- Reports the status of the node back to the rest of the system.

### kube-proxy

[kube-proxy](https://kubernetes.io/docs/admin/kube-proxy)通过在主机上维护网络规则并执行连接转发来实现Kubernetes服务抽象。

### docker

docker用于运行容器。

### RKT

rkt运行容器，作为docker工具的替代方案。

### supervisord

supervisord是一个轻量级的监控系统，用于保障kubelet和docker运行。

### fluentd

fluentd是一个守护进程，可提供[cluster-level logging](https://kubernetes.io/docs/concepts/overview/components/#cluster-level-logging).。