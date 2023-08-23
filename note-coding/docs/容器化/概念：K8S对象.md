# 了解Kubernetes对象

- 1 了解Kubernetes对象
  - [1.1 对象（Object）规范和状态](http://docs.kubernetes.org.cn/232.html#Object)
  - [1.2 描述Kubernetes对象](http://docs.kubernetes.org.cn/232.html#Kubernetes-2)
  - [1.3 必填字段](http://docs.kubernetes.org.cn/232.html#i)
- [2 下一步？](http://docs.kubernetes.org.cn/232.html#i-2)

## 了解Kubernetes对象

Kubernetes对象是Kubernetes系统中的持久实体。Kubernetes使用这些实体来表示集群的状态。具体来说，他们可以描述:

- 容器化应用正在运行（以及在哪些节点上）

- 这些应用可以用的资源

- 关于这些应用如何运行的策略，如重新策略，升级和容错

  

Kubernetes对象是“record of intent”，一旦创建了对象，Kubernetes系统会确保对象存在。通过创建对象，可以有效地告诉Kubernetes系统你希望集群的工作负载是什么样的。

要使用Kubernetes对象（无论是创建，修改还是删除），都需要使用[Kubernetes API](http://docs.kubernetes.org.cn/31.html)。例如，当使用[kubectl命令管理工具](http://docs.kubernetes.org.cn/61.html)时，CLI会为提供Kubernetes API调用。你也可以直接在自己的程序中使用Kubernetes API，Kubernetes提供一个golang[客户端库](http://docs.kubernetes.org.cn/29.html) （其他语言库正在开发中-如Python）。

### 对象（Object）规范和状态