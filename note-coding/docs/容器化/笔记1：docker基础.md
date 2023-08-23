# 容器技术（一）：docker基础

> 笔记来源：https://zhuanlan.zhihu.com/p/120341980

### docker原理

容器技术先于docker而存在，docker提供了容器技术的封装，让使用者可以很方便的操作容器，而不用关心其底层实现原理。

 **docker利用Linux内核中的资源分配机制CGroup与命名空间namespace来实现进程级别的资源隔离**。

- Linux CGroup可以用来限制、控制与分离一个进程组群的物理资源（如CPU、内存、磁盘IO等）。

- Linux namespace的主要目的之一就是实现轻量级虚拟化（容器）服务，处于同一个namespace下的进程可以互相感知，而对外部的进程却一无所知，这样就实现了容器内部进程的隔离。docker主要利用了namesapce API的clone，unshare与sentns函数来实现将各个进程隔离在相应容器内部。

### docker image 与 container

docker把应用程序与所需要的环境依赖全部都打包在image（镜像）文件里面，根据image文件可以启动docker容器来运行你的服务。

这个过程有点类似于开机时把操作系统从硬盘加载到内存的过程。可以根据同一个image文件启动多个容器。



image 由一层层的文件系统组成的，被称为 Union FS（联合文件系统）。

 联合文件系统-可以将几层目录挂载到一起，形成一个虚拟文件系统。 虚拟文件系统的目录结构就像普通 linux 的目录结构一样，docker 通过这些文件再加上宿主机的内核提供了一个 linux 的虚拟环境。

每一层文件系统我们叫做一层 layer。在docker image中每一个layer都是只读的，所以image是不可更改的。 构建镜像的时候，从一个最基本的操作系统开始，每个构建的操作相当于做一层修改，即增加一层文件系统。一层层往上叠加，上层的修改会覆盖底层的可见性，就像上层把底层遮住了一样。 当你使用的时候，你只会看到最终的修改结果，你不知道包含了多少层的修改，也无法知道每一层具体修改了什么什么。 最后，当从一个镜像启动容器时，docker会在镜像的最顶层加载一个读写文件系统，只有最顶层的的容器部分是可读写的。当容器运行后，文件系统发生变化都会体现在这一层，当改变一个文件的时候，这个文件首先会从下面的只读层复制到读写层，然后读写层对该文件的操作会隐藏在只读层的该文件，这就是传说中的copy on write。

![img](.\imgs\v2-c2d16ff4e20f957b702f32328d7842f5_1440w.webp)

所以说容器是可写的，镜像是只读的。如果有很多镜像的话，比如本地主机有很多很多的镜像，如果在这些镜像之间有些层是一样的，这些层只会占用一个空间，所以在构建镜像时多用相同的基础镜像可以达到节省空间的目的。

![img](.\imgs\v2-d28984c965c54f0759ac33b62acee597_1440w.webp)

其实image的构建过程有点类似于git更改的提交，每次commit相当于增加一个layer。一般docker的安装目录位于/var/lib/docker，而这些layer位于/var/lib/docker/aufs/diff， 之所以用diff这个词作为目录名称，我想layer的实际含义不言而喻了。

### docker应用

目前Docker的主要应用有：

（1）提供一次性的环境。比如，本地测试他人的软件，持续集成布署时提供单元测试和构建的环境。

（2）提供scalable的云计算服务。因为 Docker 容器可以随开随关，结合容器编排工具，可以很方便的实现水平动态扩容和缩容，非常适合流量存在业务波动的互联网公司。

（3）组建微服务架构。应该说，docker如此火爆，微服务的流行也是一大推手，通过启动多个多个容器，一台机器可以跑多个服务，因此在本机就可以模拟出微服务架构。

### docker使用

### docker 安装版本

docker是开源产品，包括社区版（CE）与企业版（EE）两个版本，其中企业版功能更多但收费，一般用免费的社区版就够了，[官网](https://link.zhihu.com/?target=https%3A//docs.docker.com/)提供了各个系统的安装方式，这里不再赘述。

安装完成后在控制台输入如下命令，如果显示版本号则表示成功

```
docker version
```

### 启动docker守护进程

```
sudo service docker start # service命令
sudo systemctl start docker # systemctl命令
```

docker命令需要有sudo权限才能执行，为了避免每次操作都要sudo，[官方](https://link.zhihu.com/?target=https%3A//docs.docker.com/install/linux/linux-postinstall/%23manage-docker-as-a-non-root-user) 给出的解决办法是创建docker用户组，然后把你的用户名加入docker用户组

```
sudo groupadd docker
sudo usermod -aG docker $USER_NAME
newgrp docker
```

### 编写Dockerfile 文件

官方docker镜像仓库已经提供了，很多常见的镜像，但有时候这些镜像并不能满足我们的需求，我们需要在这些镜像的基础上做一些修改，制作出满足我们的需求镜像。这一过程就是 Dockerfile 文件来描述的。

```
FROM openjdk:8
COPY . /app
WORKDIR /app
ENTRYPOINT java -jar app.jar
EXPOSE 8888
```

含义为

- *FROM openjdk:8： FROM后面跟的是基础镜像，表示该image文件是在[官方](https://link.zhihu.com/?target=https%3A//hub.docker.com/)的openjdk image上构建的，openjdk后面的冒号跟着标签号。；*
- *COPY . /app：将当前目录下的所有文件（除了.dockerignore排除的路径），都拷贝进入 image 文件的/app目录。*
- *WORKDIR /app：指定接下来的工作路径为/app；*
- *ENTRYPOINT java -jar app.jar： 定义容器启动后要做的事情，即在/app目录下，运行java -jar app.jar启动你的应用。app.jar是你的java应用程序；*
- *EXPOSE 3000： 将容器8888端口暴露出来， 允许外部访问这个端口。 然后在Dockerfile文件所在目录用 docker image build命令就可以根据Dockerfile文件创建你所需要的iamge。*

### 制作镜像与启动容器

shell命令，常见如下：

#### 常用命令

#### 镜像操作

从远程仓库(默认仓库为[docker hub](https://link.zhihu.com/?target=https%3A//hub.docker.com/))拉取镜像文件到本地

```
docker image pull [imagename:tag]
```

创建镜像文件

```
docker image build -t koa-demo . 
```

列出所有镜像文件

```
docker image ls
```

删除镜像文件

```
 docker image rm [imageName] 
```

