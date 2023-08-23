# 第6章 存储原理



 K8S CSI 系统架构图

![image-20230721203802050](.\imgs\image-20230721203802050.png)

## 2 相关解释

CSI是`Container Storage Interface`（容器存储接口）的简写。

CSI 的目的是定义行业标准“容器存储接口”，使存储供应商能够开发一个符合CSI标准的插件并使其可以在多个容器编排系统中工作。

CSI组件一般采用容器化部署，减少了环境依赖。



## 3 K8S对象

### 3.1 PersistentVolume

集群级别的资源，持久存储卷，由 集群管理员 或者 External Provisioner 创建。

PV 的生命周期独立于使用 PV 的 Pod，PV 的 `.Spec` 中保存了存储设备的详细信息。

回收策略

- retain：保留策略，当删除PVC的时候，PV与外部存储资源仍然存在。
- delete：删除策略，当与PV绑定的PVC被删除的时候，会从K8S集群中删除PV对象，并执行外部存储资源的删除操作。
- resycle（已废弃）

包含状态：

- Available
- Bound
- Released

### 3.2 PersistentVolumeClaim

持久存储卷声明，命名空间（namespace）级别的资源，由 用户 或者 StatefulSet 控制器(根据VolumeClaimTemplate) 创建。

PVC 类似于 Pod，Pod 消耗 Node 资源，PVC 消耗 PV 资源。Pod 可以请求特定级别的资源(CPU 和内存)，而 PVC 可以请求特定存储卷的大小及访问模式(Access Mode)

```yaml
yaml复制代码apiVersion: v1
kind: PersistentVolumeClaim
metadata:
   name: nginx-pvc
spec:
   storageClassName: cbs
   accessModes:
     - ReadWriteOnce
   resources:
     requests:
       storage: 10Gi
```

包含状态：

- Pending
- Bound

### 3.3 StorageClass

StorageClass 是集群级别的资源，由集群管理员创建。定义了创建pv的模板信息，用于动态创建PV。

```yaml
yaml复制代码apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: cbs
parameters:
  type: cbs
provisioner: cloud.tencent.com/qcloud-cbs
reclaimPolicy: Delete
volumeBindingMode: Immediate
```

### 3.4 VolumeAttachment

记录了PV的相关挂载信息，如挂载到哪个node节点，由哪个`volume plugin`来挂载等。

`AD Controller` 创建一个`VolumeAttachment`，而 `External-attacher` 则通过观察该 `VolumeAttachment`，根据其状态属性来进行存储的挂载和卸载操作。

### 3.5 CSINode

CSINode 记录了`csi plugin`的相关信息（如nodeId、driverName、拓扑信息等）。

当Node Driver Registrar向kubelet注册一个csi plugin后，会创建（或更新）一个CSINode对象，记录csi plugin的相关信息

```yaml
yaml复制代码apiVersion: storage.k8s.io/v1beta1
kind: CSINode
metadata:
  name: 10.1.2.11
spec:
  drivers:
  - allocatable:
      count: 18
    name: com.tencent.cloud.csi.cbs
    nodeID: ins-ig73rt44
    topologyKeys:
    - topology.com.tencent.cloud.csi.cbs/zone
```

## 4 存储组件及作用

### 4.1 Volume Plugin

扩展各种存储类型的卷的管理能力，实现第三方存储的各种操作能力与k8s存储系统的结合。

调用第三方存储的接口或命令，从而提供数据卷的创建/删除、attach/detach、mount/umount的具体操作实现，可以认为是第三方存储的代理人。前面分析组件中的对于数据卷的创建/删除、attach/detach、mount/umount操作，全是调用volume plugin来完成。

根据源码所在位置，`volume plugin`分为**in-tree**与**out-of-tree**

- in-tree

在K8S源码内部实现，和K8S一起发布、管理，更新迭代慢、灵活性差。

- out-of-tree

代码独立于K8S，由存储厂商实现，有CSI、flexvolume两种实现。

**csi plugin**

**external plugin**

external plugin包括了external-provisioner、external-attacher、external-resizer、external-snapshotter等，external plugin辅助csi plugin组件，共同完成了存储相关操作。external plugin负责watch pvc、volumeAttachment等对象，然后调用volume plugin来完成存储的相关操作。如external-provisioner watch pvc对象，然后调用csi plugin来创建存储，最后创建pv对象；external-attacher watch volumeAttachment对象，然后调用csi plugin来做attach/dettach操作；external-resizer watch pvc对象，然后调用csi plugin来做存储的扩容操作等。

### 4.2 kube-controller-manager

#### PV controller

负责pv、pvc的绑定与生命周期管理（如创建/删除底层存储，创建/删除pv对象，pv与pvc对象的状态变更）。

创建/删除底层存储、创建/删除pv对象的操作，由PV controller调用volume plugin（in-tree）来完成。

#### AD controller

AD Cotroller全称Attachment/Detachment 控制器，主要负责创建、删除VolumeAttachment对象，并调用volume plugin来做存储设备的Attach/Detach操作（将数据卷挂载到特定node节点上/从特定node节点上解除挂载），以及更新node.Status.VolumesAttached等。

不同的volume plugin的Attach/Detach操作逻辑有所不同，如通过out-tree volume plugin来使用存储，则的Attach/Detach操作只是修改VolumeAttachment对象的状态，而不会真正的将数据卷挂载到节点/从节点上解除挂载，真正的节点存储挂载/解除挂载操作由kubelet中volume manager调用。

### 4.3 kubelet

#### volume manager

主要是管理卷的Attach/Detach（与AD controller作用相同，通过kubelet启动参数控制哪个组件来做该操作）、mount/umount等操作。

## 5 流程分析

### 5.1 创建与挂载

#### 5.1.1 in-tree

![img](https://p3-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/b18b5e64578e4330ab33f1415b76b0b5~tplv-k3u1fbpfcp-zoom-in-crop-mark:4536:0:0:0.awebp)

[1] 用户创建pvc

[2] PV controller watch到PVC的创建，寻找合适的PV与之绑定

[3、4] 当找不到合适的PV时，将调用volume plugin来创建volume，并创建PV对象，之后该PV对象与PVC对象绑定

[5] 用户创建挂载PVC的pod

[6] kube-scheduler watch到pod的创建，为其寻找合适的node调度

[7、8] Pod调度完成后，AD controller/volume manager watch到pod声明的volume没有进行attach操作，将调用volume plugin来做attach操作

[9] volume plugin进行attach操作，将volume挂载到pod所在node节点，成为如`/dev/vdb`的设备

[10、11] attach操作完成后，volume manager watch到pod声明的volume没有进行mount操作，将调用volume plugin来做mount操作

[12] volume plugin进行mount操作，将node节点上的第[9]步得到的/dev/vdb设备挂载到指定目录

#### 5.1.2 Out-tree

![img](https://p3-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/b35ed9bd32864c5e95395220b7d47854~tplv-k3u1fbpfcp-zoom-in-crop-mark:4536:0:0:0.awebp)

[1] 用户创建PVC

[2] PV controller watch到PVC的创建，寻找合适的PV与之绑定。当寻找不到合适的PV时，将更新PVC对象，添加`annotation: volume.beta.kubernetes.io/storage-provisioner`，让external-provisioner组件开始开始创建存储与PV对象的操作

[3] external-provisioner组件watch到PVC的创建，判断annotation：volume.beta.kubernetes.io/storage-provisioner的值，即判断是否是自己来负责做创建操作，是则调用csi-plugin ControllerServer来创建存储，并创建PV对象

[4] PV controller watch到PVC，寻找合适的PV（上一步中创建）与之绑定

[5] 用户创建挂载PVC的Pod

[6] kube-scheduler watch到Pod的创建，为其寻找合适的node调度

[7、8] pod调度完成后，AD controller/volume manager watch到pod声明的volume没有进行attach操作，将调用csi-attacher来做attach操作，实际上只是创建volumeAttachement对象

[9] external-attacher组件watch到volumeAttachment对象的新建，调用csi-plugin进行attach操作

[10] csi-plugin ControllerServer进行attach操作，将volume挂载到Pod所在node节点，成为如/dev/vdb的设备

[11、12] attach操作完成后，volume manager watch到Pod声明的volume没有进行mount操作，将调用csi-mounter来做mount操作

[13] csi-mounter调用csi-plugin NodeServer进行mount操作，将node节点上的第（10）步得到的/dev/vdb设备挂载到指定目录

## kubernetes的临时存储

显然，了解临时存储对解答前文中的问题没有任何帮助（x），但为了文章以及个人知识体系的完整性，我打算先就临时存储写一个段落

### emptydir——临时存储

当pod的存储方案设定为emptydir的时候，pod启动时，就会在pod所在节点的磁盘空间开辟出一块空卷，最开始里面是什么都没有的，pod启动后容器产生的数据会存放到那个空卷中。空卷变成了一个临时卷。

供pod内的容器读取和写入数据，一旦pod容器消失，节点上开辟出的这个临时卷就会随着pod的销毁而销毁。

emptydir的用途

- 充当临时存储空间，当pod内容器产生的数据不需要做持久化存储的时候用emptydir
- 设制检查点以从崩溃事件中恢复未执行完毕的长计算

一般来说emptydir的用途都是用来充当临时存储空间，例如一些不需要数据持久化的微服务，我们都可以用emptydir来当做微服务pod的存储方案。

使用步骤如下：

首先，需要在pod内声明了一个名称为`nginxdata`的`volume`

```
volumes:
  - name: nginxdata
    emptyDir: {}
```

然后，才能在容器中挂在这个volume

```yaml
yaml复制代码volumeMounts:
  # mountPath即volume在容器内的挂载点路径
  - mountPath: /var/www/html
    name: nginxdata
```

测试`yaml`:

```yaml
yaml复制代码apiVersion: apps/v1
kind: Deployment
metadata:
  name: test-dp
spec:
  replicas: 1
  selector:
    matchLabels:
      app: test-dp
  template:
    metadata:
      labels:
        app: test-dp
    spec:
      containers:
      - name: nginx
        image: nginx:1.19.5
        volumeMounts:
          - mountPath: /var/www/html
            name: nginxdata
      volumes:
        - name: nginxdata
          emptyDir: {}
```

按照以上的配置文件创建了`Pod`之后，可以在宿主机上的`/var/lib/kubelet/pods/<pod uid>/volumes/kubernetes.io~empty-dir`目录下查看到新生成的名为`nginxdata`的目录。

如果登录到该Pod创建的容器中，也可以看到名为`/var/www/html`的目录，这个目录与宿主机上的`nginxdata`目录是同一个。

## 借助本地储存实现的持久化存储——hostPath

k8s的hostPath存储方式，是一种映射本地的文件或目录进入pod中的方式，这种方式与docker的Data volume存储方式非常相似。

使用hostPath存储的好处在于，在Pod挂掉之后，可以重新拉去镜像制作新的Pod并接回原有的hostPath，此时不会造成硬盘数据的丢失。

其缺点在于，在云原生的大趋势下，一种借助宿主机本地存储的存储方案显然不应成为最优方案，将数据持久化在本地不便于“上云”，这种不易于迁移到其它节点的设计违背了云原生设计的初衷。

```
apiVersion: apps/v1
kind: Deployment
metadata:
  name: test-dp
spec:
  replicas: 1
  selector:
    matchLabels:
      app: test-dp
  template:
    metadata:
      labels:
        app: test-dp
    spec:
      containers:
      - name: nginx
        image: nginx:1.19.5
        volumeMounts:
          - mountPath: /var/www/html
            name: nginxdata
      volumes:
        - name: nginxdata
          hostPath:
            path: /data

```

