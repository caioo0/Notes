# Linux的进程模型及CFS调度器算法分析

## **1. 关于进程**

## **1.1. 进程的定义**

进程：指在系统中能独立运行并作为资源分配的基本单位，它是由一组机器指令、数据和堆栈等组成的，是一个能独立运行的活动实体。

1. 进程是程序的一次执行
2. 进程是可以和别的计算并行执行
3. 进程是程序在一个数据集合上运行的过程，它是系统进行资源分配和调度的一个独立单位

## **1.2. 进程的特征**

1.动态性：进程的实质是程序的一次执行过程，进程是动态产生，动态消亡的。
2.并发性：任何进程都可以同其他进程一起并发执行。
3.独立性：进程是一个能独立运行的基本单位，同时也是系统分配资源和调度的独立单位。

4.异步性：由于进程间的相互制约，使进程具有执行的间断性，即进程按各自独立的、不可预知的速度向前推进。

## **2. 关于进程的组织**

task_struct 是Linux内核的一种数据结构，它被装在到RAM里并且包含着进程的信息。每个进程都把它的信息放在 task_struct 这个数据结构中， task_struct 包含了以下内容：

标识符：描述本进程的唯一标识符，用来区别其他进程。

状态：任务状态，退出代码，退出信号等。

优先级：相对于其他进程的优先级。

程序计数器：程序中即将被执行的下一条指令的地址。

内存指针：包括程序代码和进程相关数据的指针，还有和其他进程共享的内存块的指针。

上下文数据：进程执行时处理器的寄存器中的数据。

I/O状态信息：包括显示的I/O请求，分配给进程的I/O设备和被进程使用的文件列表。

记账信息：可以包括处理器时间总和，使用的时钟数总和，时间限制，记账号等。

保存进程信息的数据结构叫做 task_struct ，并且可以在 include/linux/sched.h 里找到它。所以运行在系统里的进程都以 task_struct 链表的形式存在于内核中。

## **2.1. 进程状态**

**2.1.1. 进程状态**

```
volatile long state;  
int exit_state;
```

**2.1.2. state成员的可能取值**

```
#define TASK_RUNNING        0  
#define TASK_INTERRUPTIBLE  1  
#define TASK_UNINTERRUPTIBLE    2  
#define __TASK_STOPPED      4  
#define __TASK_TRACED       8  
/* in tsk->exit_state */  
#define EXIT_ZOMBIE     16  
#define EXIT_DEAD       32  
/* in tsk->state again */  
#define TASK_DEAD       64  
#define TASK_WAKEKILL       128  
#define TASK_WAKING     256
```

**2.1.3. 进程的各个状态**

![在这里插入图片描述](D:\www\learning\caioo0.github.io\note-coding\docs\容器化\imgs\watermark,type_ZHJvaWRzYW5zZmFsbGJhY2s,shadow_50,text_Q1NETiBA5bCP5LiA77yB,size_20,color_FFFFFF,t_70,g_se,x_16)

**2.1.4. 状态转换图**

![image-20230718110331005](.\imgs\image-20230718110331005.png)

## **2.2. 进程标识符（pid）**

**2.2.1. 标识符定义**

pid_t pid; //进程的标识符

**2.2.2. 关于标识符**

pid是 Linux 中在其命名空间中唯一标识进程而分配给它的一个号码，称做进程ID号，简称PID。

程序一运行系统就会自动分配给进程一个独一无二的PID。进程中止后PID被系统回收，可能会被继续分配给新运行的程序。

是暂时唯一的：进程中止后，这个号码就会被回收，并可能被分配给另一个新进程。



### 参考

1. https://blog.csdn.net/qq_49613557/article/details/120294908