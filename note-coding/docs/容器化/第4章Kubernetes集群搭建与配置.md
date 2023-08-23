# 第4章 Kubernetes集群搭建与配置

### Kubernetes 部署利器：Kubeadm

#### Kubeadm初尝试

通过两条指令即可部署一个Kubernetesj集群：

```
# 创建一个Master 节点
kubeadm init

# 将一个Node节点加入当前集群
kubeadm join <Master 节点的IP和端口>

```

#### Kubeadm 安装



为什么不用容器部署Kubernetes呢？

事实上，在Kubernetes早期的部署脚本里，确实有一个脚本就是用Docker部署Kubernetes项目的，这个脚本相比于SaltStack等的部署方式，也的确简单了不少。
但是，这样做会带来一个很麻烦的问题，即：如何容器化kubelet。
我在上一篇文章中，已经提到kubelet是Kubernetes项目用来操作Docker等容器运行时的核心组件。可是，除了跟容器运行时打交道外，kubelet在配置容器网络、管理容器数据卷时，都需要直接操作宿主机。
而如果现在kubelet本身就运行在一个容器里，那么直接操作宿主机就会变得很麻烦。对于网络配置来说还好，kubelet容器可以通过不开启Network Namespace（即Docker的host network模式）的方式，直接共享宿主机的网络栈。可是，要让kubelet隔着容器的Mount Namespace和文件系统，操作宿主机的文件系统，就有点儿困难了。
比如，如果用户想要使用NFS做容器的持久化数据卷，那么kubelet就需要在容器进行绑定挂载前，在宿主机的指定目录上，先挂载NFS的远程目录。
可是，这时候问题来了。由于现在kubelet是运行在容器里的，这就意味着它要做的这个“mount -F nfs”命令，被隔离在了一个单独的Mount Namespace中。即，kubelet做的挂载操作，不能被“传播”到宿主机上。
对于这个问题，有人说，可以使用setns()系统调用，在宿主机的Mount Namespace中执行这些挂载操作；也有人说，应该让Docker支持一个–mnt=host的参数。
但是，到目前为止，在容器里运行kubelet，依然没有很好的解决办法，我也不推荐你用容器去部署Kubernetes项目。
正因为如此，kubeadm选择了一种妥协方案：
把kubelet直接运行在宿主机上，然后使用容器部署其他的Kubernetes组件。
所以，你使用kubeadm的第一步，是在机器上手动安装kubeadm、kubelet和kubectl这三个二进制文件。当然，kubeadm的作者已经为各个发行版的Linux准备好了安装包，所以你只需要执行：

```
# kubeadm:

$ curl -s https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key add -$ cat <<EOF > /etc/apt/sources.list.d/kubernetes.listdeb http://apt.kubernetes.io/ kubernetes-xenial mainEOF$ apt-get update$ apt-get install -y docker.io kubeadm

# gpb报错找不到可以试试下面的方法：
wget https://download.docker.com/linux/ubuntu/gpg
sudo apt-key add gpg
```

就可以了。
接下来，你就可以使用“kubeadm init”部署Master节点了。

详细安装说明见：[官方安装手册](https://kubernetes.io/docs/setup/production-environment/tools/kubeadm/install-kubeadm/)

#### Kubeadm 的工作原理

#### kubeadm init

当你执行kubeadm init指令后，

1. 首先要做的，是一系列环境检查工作，称之为preflight checks。包括操作系统内核，Cgroup是否可用，是否标准（在Kubernetes项目里，机器的名字以及一切存储在Etcd中的API对象，需标准DNS命名），户安装的kubeadm和kubelet的版本是否匹配？
   机器上是不是已经安装了Kubernetes的二进制文件？
   Kubernetes的工作端口10250/10251/10252端口是不是已经被占用？
   ip、mount等Linux指令是否存在，docker是否安装等等
2. 生成证书，kube api 的访问默认是tls的，证书会存放在/etc/kubernetes/pki目录下，如果想使用自己生成的证书，只需提前将证书拷贝到pki/ca.crt, /pki/ca.key，kubeadm就会跳过此步骤
3. 接下来，会生成为其他组件访问api server的配置文件，路径是/etc/kubernetes,文件包括admin.conf, controller-manager.conf, kubelet.conf , scheduler.conf，其中admin是给kubectl操作时用的，告诉kubectl去连接哪个api server去操作。(还记得搭建master节点的某一个步是copy admin.conf到.kube目录下吗？). 这些文件里的内容大体上相似，如master节点的地址，端口，证书目录等信息。
4. 接下来，会为api server, controller manager, scheduler, etcd生成pod配置文件，放在/etc/kubernetes/manifests路径下，kubelet会更具该路径下的配置文件，启动相应的pod.
5. 此时master组件基本上启动了，kubeadm会检查 localhost:6443/healthz这个url，等待master组件完全启动。启动完成后，会为集群生成一个bootstrap token,后续节点拿到这个token后才能通过kubeadm join来加入这个集群。这个token会被保存在etcd中。
6. 最后一步，安装默认插件kube-proxy和dns。他们是为整个集群提供服务发现和dns解析用的。这两个也是以pod的方式启动。

此外，我们也可以自己编写kubeadm.yaml文件来定制化kubeadm的启动过程和一些配置。关于yaml的编写方法会在后续专门写一篇来介绍。启动命令为kubeadm init --config kubeadm.yaml

#### kubeadm join

join的流程相比init来说简单不少，任何一台机器想要加入集群，必须要拿到server端的ca证书才能和其建立tls连接，那么如何在不手动拷贝的情况下拿到server的ca证书，这就需要指定一个token来证明node的合法性。于是便需要以下这样的命令来加入集群。加入后，ca.crt证书文件也将被存放到/etc/kubenetes/pki目录下。

```shell
kubeadm join 192.168.0.233:6443 --token sd8a51.017go0q0mj7kiu4p \
    --discovery-token-ca-cert-hash sha256:94e0877bd0852665528c7fd124f6fdd8559283451e30747df3a35a3bc7dec1f2
```

