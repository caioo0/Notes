# DOCKER基础技术：LINUX NAMESPACE（上）

> 笔记来源：https://coolshell.cn/articles/17010.html

基础系列：

[Docker基础技术：Linux Namespace（上） | | 酷 壳 - CoolShell](http%3A//coolshell.cn/articles/17010.html)
[Docker基础技术：Linux Namespace（下） | | 酷 壳 - CoolShell](http%3A//coolshell.cn/articles/17029.html)
[Docker基础技术：Linux CGroup | | 酷 壳 - CoolShell](http%3A//coolshell.cn/articles/17049.html)
[Docker基础技术：AUFS | | 酷 壳 - CoolShell](http%3A//coolshell.cn/articles/17061.html)

#### 简介

Linux Namespace是Linux提供的一种内核级别环境隔离的方法。

很早以前的Unix有一个叫chroot的系统调用（通过修改根目录把用户jail到一个特定目录下）

chroot提供了一种简单的隔离模式：**chroot内部的文件系统无法访问外部的内容。**

Linux Namespace在此基础上，提供了对`UTS、IPC、mount、PID、network、User`等的隔离机制。

**Linux Namespace 有如下种类**，官方文档在这里《[Namespace in Operation](http://lwn.net/Articles/531114/)》

| 分类                   | 系统调用参数  | 相关内核版本                                                 |
| :--------------------- | :------------ | :----------------------------------------------------------- |
| **Mount namespaces**   | CLONE_NEWNS   | [Linux 2.4.19](http://lwn.net/2001/0301/a/namespaces.php3)   |
| **UTS namespaces**     | CLONE_NEWUTS  | [Linux 2.6.19](http://lwn.net/Articles/179345/)              |
| **IPC namespaces**     | CLONE_NEWIPC  | [Linux 2.6.19](http://lwn.net/Articles/187274/)              |
| **PID namespaces**     | CLONE_NEWPID  | [Linux 2.6.24](http://lwn.net/Articles/259217/)              |
| **Network namespaces** | CLONE_NEWNET  | [始于Linux 2.6.24 完成于 Linux 2.6.29](http://lwn.net/Articles/219794/) |
| **User namespaces**    | CLONE_NEWUSER | [始于 Linux 2.6.23 完成于 Linux 3.8)](http://lwn.net/Articles/528078/) |

主要是三个系统调用:

- `clone() `- 实现线程的系统调用，用来创建一个新的进程，并可以通过设计上述参数达到隔离。
- `unshare()` - 使某进程脱离某个namespace。
- `setns() `- 把某进程加入到某个namespace。

>    推荐阅读：
>
> 1. [unshare命令详情及案例](https://juejin.cn/post/6987564689606180900) 
> 2. [Linux手册翻译 - setns](https://zhuanlan.zhihu.com/p/614760400)

这里对clone() 展开讨论：

#### clone()系统调用

首先，我们来看一下一个最简单的clone()系统调用的示例，（后面，我们的程序都会基于这个程序做修改）：

```c
#define _GNU_SOURCE
#include <sys/types.h>
#include <sys/wait.h>
#include <stdio.h>
#include <sched.h>
#include <signal.h>
#include <unistd.h>

/* 定义一个给 clone 用的栈，栈大小1M */
#define STACK_SIZE (1024 * 1024)
static char container_stack[STACK_SIZE];

char* const container_args[] = {
    "/bin/bash",
    NULL
};

int container_main(void* arg)
{
    printf("Container - inside the container!\n");
    /* 直接执行一个shell，以便我们观察这个进程空间里的资源是否被隔离了 */
    execv(container_args[0], container_args); 
    printf("Something's wrong!\n");
    return 1;
}

int main()
{
    printf("Parent - start a container!\n");
    /* 调用clone函数，其中传出一个函数，还有一个栈空间的（为什么传尾指针，因为栈是反着的） */
    int container_pid = clone(container_main, container_stack+STACK_SIZE, SIGCHLD, NULL);
    /* 等待子进程结束 */
    waitpid(container_pid, NULL, 0);
    printf("Parent - container stopped!\n");
    return 0;
}
```

从上面的程序，我们可以看到，这和pthread基本上是一样的玩法。但是，对于上面的程序，父子进程的进程空间是没有什么差别的，父进程能访问到的子进程也能。

下面， 让我们来看几个例子看看，Linux的Namespace是什么样的。

#### UTS Namespace

下面的代码，我略去了上面那些头文件和数据结构的定义，只有最重要的部分。

```c
int container_main(void* arg)
{
    printf("Container - inside the container!\n");
    sethostname("container",10); /* 设置hostname */
    execv(container_args[0], container_args);
    printf("Something's wrong!\n");
    return 1;
}

int main()
{
    printf("Parent - start a container!\n");
    int container_pid = clone(container_main, container_stack+STACK_SIZE, 
            CLONE_NEWUTS | SIGCHLD, NULL); /*启用CLONE_NEWUTS Namespace隔离 */
    waitpid(container_pid, NULL, 0);
    printf("Parent - container stopped!\n");
    return 0;
}
```

```
运行上面的程序你会发现（需要root权限），子进程的hostname变成了 container。
```

```
hchen@ubuntu:~$ sudo ./uts
Parent - start a container!
Container - inside the container!
root@container:~# hostname
container
root@container:~# uname -n
container
```

#### IPC Namespace

IPC全称 Inter-Process Communication，是Unix/Linux下进程间通信的一种方式，IPC有共享内存、信号量、消息队列等方法。所以，为了隔离，我们也需要把IPC给隔离开来，这样，只有在同一个Namespace下的进程才能相互通信。如果你熟悉IPC的原理的话，你会知道，IPC需要有一个全局的ID，即然是全局的，那么就意味着我们的Namespace需要对这个ID隔离，不能让别的Namespace的进程看到。

要启动IPC隔离，我们只需要在调用clone时加上CLONE_NEWIPC参数就可以了。

