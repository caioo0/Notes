# 一、基础知识

## 1. 计算机底层知识

- 机器码：在计算机内的数（称之为"机器数"）值有3种表示法：原码、反码和补码。

- 正负数：在计算机内，通常把二进制的最高位定义为符号位，用0表示正数，用1表示负数。其余表示数值。（在下面陈述种，为了方便，我们均假设机器的字长为8位）。

- 原码：原码（true form）是一种计算机中对数字的二进制定点表示方法。原码表示法在数值前面增加一个符号位（即最高位为符号位）：正数该位为0，负数该位为1（0有两种表示：+0和-0），其余位表示数值的大小。

  > 如 -1 = 1000 0001 ，1 = 0000 0001 

- 反码： 正数的反码和其原码相同；负数的反码是对其原码逐位取反，其符号位除外。一般情况下，我们需要先给定数字转化为原码，然后转化为反码。

  > 如 -1 = 1000 0000 = 1111 1110 ， 1 = 0000 0001 = 0000 0001 

- 补码：正数的补码就是其本身，负数的补码就是在其原码的基础上，符号位不变，其余各位去反，最后+1 

  > 如 *−*1 = 1000 0001 = 1111 11110 = 1111 1111 , 1 = 0000 0001 = 0000 0001 = 0000 0001 

​       如果在加1的时候出现了溢出就直接不管那个溢出的1.由于补码有利于运算，故而计算机中数都是利用补码表示的。



## 2. GNU/LINUX

### 错误码大全

```
 宏名称	键值	描述							涵义

            0	Success						执行成功
  EPERM		1	Operation not permitted		无操作权限
  ENOENT	2	No such file or directory	文件或目录不存在
  ESRCH		3	No such process				进程不存在
  EINTR		4	Interrupted system call		系统调用被中断
  EIO		5	I/O error					I/O错误
  ENXIO		6	No such device or address	设备或地址不存在
  E2BIG		7	Arg list too long			参数列表过长
  ENOEXEC	8	Exec format error			格式化执行错误
  EBADF		9	Bad file number				无效文件描述符
  ECHILD	10	No child processes			没有子进程
  EAGAIN	11	Try again					再次尝试
  ENOMEM	12	Out of memory				内存溢出
  EACCES	13	Permission denied			无访问权限
  EFAULT	14	Bad address					地址错误
  ENOTBLK	15	Block device required		块设备请求
  EBUSY		16	Device or resource busy		设备或资源已被使用
  EEXIST	17	File exists					文件已存在
  EXDEV		18	Cross-device link			无效的交叉链接
  ENODEV	19	No such device				设备不存在
  ENOTDIR	20	Not a directory				非目录文件
  EISDIR	21	Is a directory				这是一个目录文件
  EINVAL	22	Invalid argument			参数无效
  ENFILE	23	File table overflow			文件表溢出
  EMFILE	24	Too many open files			打开的文件过多
  ENOTTY	25	Not a tty device			不是一个tty设备
  ETXTBSY	26	Text file busy				文本文件被占用
  EFBIG		27	File too large				文件过大
  ENOSPC	28	No space left on device		磁盘空间不足
  ESPIPE	29	Illegal seek				非法的地址偏移
  EROFS		30	Read-only file system		只读文件系统
  EMLINK	31	Too many links				过多的链接
  EPIPE		32	Broken pipe					管道破裂
  EDOM		33	Math argument out of domain	数值结果超出范围
  ERANGE	34	Math result not representable	数值结果不具代表性
  EDEADLK	35	Resource deadlock would occur	资源死锁错误
  ENAMETOOLONG	36	Filename too long		文件名过长
  ENOLCK	37	No record locks available	没有可用的锁
  ENOSYS	38	Function not implemented	功能没有实现
  ENOTEMPTY	39	Directory not empty			目录不为空
  ELOOP		40	Too many symbolic links encountered	符号链接层次太多
  EWOULDBLOCK	41	Same as EAGAIN			与“EAGAIN”错误码类似
  ENOMSG	42	No message of desired type	没有期望类型的消息
  EIDRM		43	Identifier removed			标识符已经被删除
  ECHRNG	44	Channel number out of range	通道数目超出范围
  EL2NSYNC	45	Level 2 not synchronized	2级不同步
  EL3HLT	46	Level 3 halted				3级中断
  EL3RST	47	Level 3 reset				3级复位
  ELNRNG	48	Link number out of range	链接数超出范围
  EUNATCH	49	Protocol driver not attached协议驱动程序没有连接
  ENOCSI	50	No CSI structure available	没有可用CSI结构
  EL2HLT	51	Level 2 halted				2级中断
  EBADE		52	Invalid exchange			无效的交换
  EBADR		53	Invalid request descriptor	请求描述符无效
  EXFULL	54	Exchange full				交换空间已满
  ENOANO	55	No anode					-
  EBADRQC	56	Invalid request code		无效的请求代码
  EBADSLT	57	Invalid slot				无效的槽函数
  EDEADLOCK	58	Same as EDEADLK				与“EDEADLK”错误码类似
  EBFONT	59	Bad font file format		错误的字体文件格式
  ENOSTR	60	Device not a stream			非数据流设备
  ENODATA	61	No data available			无可用数据
  ETIME		62	Timer expired				定时器溢出
  ENOSR		63	Out of streams resources	数据流相关资源溢出
  ENONET	64	Machine is not on the network	机器未连接到网络
  ENOPKG	65	Package not installed		软件包未安装
  EREMOTE	66	Object is remote			-
  ENOLINK	67	Link has been severed		（软/硬）链接已被断开
  EADV		68	Advertise error				广播错误
  ESRMNT	69	Srmount error				-
  ECOMM		70	Communication error on send	通信状态在发送过程出错
  EPROTO	71	Protocol error				协议错误
  EMULTIHOP	72	Multihop attempted			多次尝试
  EDOTDOT	73	RFS specific error			RFS特定的错误
  EBADMSG	74	Not a data message			非有效的数据消息
  EOVERFLOW	75	Value too large for defined data type		数值超出定义的数据类型
  ENOTUNIQ	76	Name not unique on network	命名在网络中非唯一
  EBADFD	77	File descriptor in bad state文件描述符损坏
  EREMCHG	78	Remote address changed		远程地址已更改
  ELIBACC	79	Cannot access a needed shared library		无法访问必要的共享库
  ELIBBAD	80	Accessing a corrupted shared library		访问已损坏的共享库
  ELIBSCN	81	.lib section in a.out corrupted				库文件部分损坏
  ELIBMAX	82	Linking in too many shared libraries		链接共享库过多
  ELIBEXEC	83	Cannot exec a shared library directly		不能执行一个共享库
  EILSEQ	84	Illegal byte sequence						非法字节序列
  ERESTART	85	Interrupted system call should be restarted	需重新启动中断系统
  ESTRPIPE	86	Streams pipe error							管道流出错
  EUSERS	87	Too many users								访问用户过多
  ENOTSOCK	88	Socket operation on non-socket				非套接字函数访问套接字描述符
  EDESTADDRREQ	89	Destination address required			请求目的地址
  EMSGSIZE	90	Message too long							消息长度过长
  EPROTOTYPE	91	Protocol wrong type for socket			socket协议类型错误
  ENOPROTOOPT	92	Protocol not available					协议不可用
  EPROTONOSUPPORT	93	Protocol not supported				不支持的协议
  ESOCKTNOSUPPORT	94	Socket type not supported			不支持的socket类型
  EOPNOTSUPP	95	Operation not supported on transport	不支持的操作
  EPFNOSUPPORT	96	Protocol family not supported			不支持的协议族
  EAFNOSUPPORT	97	Address family not supported by protocol 协议不支持该地址
  EADDRINUSE	98	Address already in use					地址已被使用
  EADDRNOTAVAIL	99	Cannot assign requested address			无法分配请求的地址
  ENETDOWN		100	Network is down							网络已被断开
  ENETUNREACH	101	Network is unreachable					互联网不可用
  ENETRESET		102	Network dropped							网络连接丢失
  ECONNABORTED	103	Software caused connection	软件导致连接中断
  ECONNRESET	104	Connection reset by	连接被重置
  ENOBUFS		105	No buffer space available	没有可用的缓冲空间
  EISCONN		106	Transport endpoint	传输端点已经连接
  ENOTCONN		107	Transport endpoint	传输终点没有连接
  ESHUTDOWN		108	Cannot send after transport	传输后无法发送
  ETOOMANYREFS	109	Too many references	请求用户过多
  ETIMEDOUT		110	Connection timed	连接超时
  ECONNREFUSED	111	Connection refused	（远程端）拒绝连接
  EHOSTDOWN		112	Host is down	主机已关闭
  EHOSTUNREACH	113	No route to host	主机未找到路由
  EALREADY		114	Operation already	操作已执行
  EINPROGRES	115	Operation now in	操作正在执行
  ESTALE		116	Stale NFS file handle	NFS文件句柄已过期
  EUCLEAN		117	Structure needs cleaning	结构需要清除
  ENOTNAM		118	Not a XENIX-named	-
  ENAVAIL		119	No XENIX semaphores	没有“XENIX”信号量
  EISNAM		120	Is a named type file	已定义的文件类型
  EREMOTEIO		121	Remote I/O error	远程IO错误
  EDQUOT		122	Quota exceeded	超出磁盘配额
  ENOMEDIUM		123	No medium found	没有发现媒体介质
  EMEDIUMTYPE	124	Wrong medium type	媒体类型错误
  ECANCELED		125	Operation Canceled	操作被取消
  ENOKEY		126	Required key not available	所需键值不可用
  EKEYEXPIRED	127	Key has expired	键值已过期
  EKEYREVOKED	128	Key has been revoked	键值已被撤销
  EKEYREJECTED	129	Key was rejected by service	键值被拒绝
  EOWNERDEAD	130	Owner died	用户注销
  ENOTRECOVERABLE	131	State not recoverable	状态不可恢复
  ERFKILL		132	Operation not possible due to RF-kill	由于RF-kill而无法操作
  EHWPOISON		133	Memory page has hardware error	内存页存在硬件错误
            	134—139	Reserve	保留
```

更多细节参见[The GNU C Library Reference Manuel](https://link.jianshu.com/?t=http%3A%2F%2Fwww.gnu.org%2Fsoftware%2Flibc%2Fmanual%2Fhtml_node%2Findex.html)



**其中，基本错误码（asm-generic/errno-base.h）**

```
#ifndef _ASM_GENERIC_ERRNO_BASE_H
#define _ASM_GENERIC_ERRNO_BASE_H

#define EPERM        1  /* Operation not permitted */
#define ENOENT       2  /* No such file or directory */
#define ESRCH        3  /* No such process */
#define EINTR        4  /* Interrupted system call */
#define EIO      5  /* I/O error */
#define ENXIO        6  /* No such device or address */
#define E2BIG        7  /* Argument list too long */
#define ENOEXEC      8  /* Exec format error */
#define EBADF        9  /* Bad file number */
#define ECHILD      10  /* No child processes */
#define EAGAIN      11  /* Try again */
#define ENOMEM      12  /* Out of memory */
#define EACCES      13  /* Permission denied */
#define EFAULT      14  /* Bad address */
#define ENOTBLK     15  /* Block device required */
#define EBUSY       16  /* Device or resource busy */
#define EEXIST      17  /* File exists */
#define EXDEV       18  /* Cross-device link */
#define ENODEV      19  /* No such device */
#define ENOTDIR     20  /* Not a directory */
#define EISDIR      21  /* Is a directory */
#define EINVAL      22  /* Invalid argument */
#define ENFILE      23  /* File table overflow */
#define EMFILE      24  /* Too many open files */
#define ENOTTY      25  /* Not a typewriter */
#define ETXTBSY     26  /* Text file busy */
#define EFBIG       27  /* File too large */
#define ENOSPC      28  /* No space left on device */
#define ESPIPE      29  /* Illegal seek */
#define EROFS       30  /* Read-only file system */
#define EMLINK      31  /* Too many links */
#define EPIPE       32  /* Broken pipe */
#define EDOM        33  /* Math argument out of domain of func */
#define ERANGE      34  /* Math result not representable */

#endif
```

**扩展错误码（asm-generic/errno.h）**

```
#ifndef _ASM_GENERIC_ERRNO_H
#define _ASM_GENERIC_ERRNO_H

#include <asm-generic/errno-base.h>

#define EDEADLK     35  /* Resource deadlock would occur */
#define ENAMETOOLONG    36  /* File name too long */
#define ENOLCK      37  /* No record locks available */
#define ENOSYS      38  /* Function not implemented */
#define ENOTEMPTY   39  /* Directory not empty */
#define ELOOP       40  /* Too many symbolic links encountered */
#define EWOULDBLOCK EAGAIN  /* Operation would block */
#define ENOMSG      42  /* No message of desired type */
#define EIDRM       43  /* Identifier removed */
#define ECHRNG      44  /* Channel number out of range */
#define EL2NSYNC    45  /* Level 2 not synchronized */
#define EL3HLT      46  /* Level 3 halted */
#define EL3RST      47  /* Level 3 reset */
#define ELNRNG      48  /* Link number out of range */
#define EUNATCH     49  /* Protocol driver not attached */
#define ENOCSI      50  /* No CSI structure available */
#define EL2HLT      51  /* Level 2 halted */
#define EBADE       52  /* Invalid exchange */
#define EBADR       53  /* Invalid request descriptor */
#define EXFULL      54  /* Exchange full */
#define ENOANO      55  /* No anode */
#define EBADRQC     56  /* Invalid request code */
#define EBADSLT     57  /* Invalid slot */

#define EDEADLOCK   EDEADLK

#define EBFONT      59  /* Bad font file format */
#define ENOSTR      60  /* Device not a stream */
#define ENODATA     61  /* No data available */
#define ETIME       62  /* Timer expired */
#define ENOSR       63  /* Out of streams resources */
#define ENONET      64  /* Machine is not on the network */
#define ENOPKG      65  /* Package not installed */
#define EREMOTE     66  /* Object is remote */
#define ENOLINK     67  /* Link has been severed */
#define EADV        68  /* Advertise error */
#define ESRMNT      69  /* Srmount error */
#define ECOMM       70  /* Communication error on send */
#define EPROTO      71  /* Protocol error */
#define EMULTIHOP   72  /* Multihop attempted */
#define EDOTDOT     73  /* RFS specific error */
#define EBADMSG     74  /* Not a data message */
#define EOVERFLOW   75  /* Value too large for defined data type */
#define ENOTUNIQ    76  /* Name not unique on network */
#define EBADFD      77  /* File descriptor in bad state */
#define EREMCHG     78  /* Remote address changed */
#define ELIBACC     79  /* Can not access a needed shared library */
#define ELIBBAD     80  /* Accessing a corrupted shared library */
#define ELIBSCN     81  /* .lib section in a.out corrupted */
#define ELIBMAX     82  /* Attempting to link in too many shared libraries */
#define ELIBEXEC    83  /* Cannot exec a shared library directly */
#define EILSEQ      84  /* Illegal byte sequence */
#define ERESTART    85  /* Interrupted system call should be restarted */
#define ESTRPIPE    86  /* Streams pipe error */
#define EUSERS      87  /* Too many users */
#define ENOTSOCK    88  /* Socket operation on non-socket */
#define EDESTADDRREQ    89  /* Destination address required */
#define EMSGSIZE    90  /* Message too long */
#define EPROTOTYPE  91  /* Protocol wrong type for socket */
#define ENOPROTOOPT 92  /* Protocol not available */
#define EPROTONOSUPPORT 93  /* Protocol not supported */
#define ESOCKTNOSUPPORT 94  /* Socket type not supported */
#define EOPNOTSUPP  95  /* Operation not supported on transport endpoint */
#define EPFNOSUPPORT    96  /* Protocol family not supported */
#define EAFNOSUPPORT    97  /* Address family not supported by protocol */
#define EADDRINUSE  98  /* Address already in use */
#define EADDRNOTAVAIL   99  /* Cannot assign requested address */
#define ENETDOWN    100 /* Network is down */
#define ENETUNREACH 101 /* Network is unreachable */
#define ENETRESET   102 /* Network dropped connection because of reset */
#define ECONNABORTED    103 /* Software caused connection abort */
#define ECONNRESET  104 /* Connection reset by peer */
#define ENOBUFS     105 /* No buffer space available */
#define EISCONN     106 /* Transport endpoint is already connected */
#define ENOTCONN    107 /* Transport endpoint is not connected */
#define ESHUTDOWN   108 /* Cannot send after transport endpoint shutdown */
#define ETOOMANYREFS    109 /* Too many references: cannot splice */
#define ETIMEDOUT   110 /* Connection timed out */
#define ECONNREFUSED    111 /* Connection refused */
#define EHOSTDOWN   112 /* Host is down */
#define EHOSTUNREACH    113 /* No route to host */
#define EALREADY    114 /* Operation already in progress */
#define EINPROGRESS 115 /* Operation now in progress */
#define ESTALE      116 /* Stale file handle */
#define EUCLEAN     117 /* Structure needs cleaning */
#define ENOTNAM     118 /* Not a XENIX named type file */
#define ENAVAIL     119 /* No XENIX semaphores available */
#define EISNAM      120 /* Is a named type file */
#define EREMOTEIO   121 /* Remote I/O error */
#define EDQUOT      122 /* Quota exceeded */

#define ENOMEDIUM   123 /* No medium found */
#define EMEDIUMTYPE 124 /* Wrong medium type */
#define ECANCELED   125 /* Operation Canceled */
#define ENOKEY      126 /* Required key not available */
#define EKEYEXPIRED 127 /* Key has expired */
#define EKEYREVOKED 128 /* Key has been revoked */
#define EKEYREJECTED    129 /* Key was rejected by service */

/* for robust mutexes */
#define EOWNERDEAD  130 /* Owner died */
#define ENOTRECOVERABLE 131 /* State not recoverable */

#define ERFKILL     132 /* Operation not possible due to RF-kill */

#define EHWPOISON   133 /* Memory page has hardware error */

#endif
```

#### **返回指针是否错误的[内联函数]**

linux内核中判断返回指针是否错误的内联函数主要有：**ERR_PTR、PTR_ERR、IS_ERR和IS_ERR_OR_NULL**等。
其源代码见include/linux/err.h

```
#include <linux/compiler.h>
#include <linux/types.h>

#include <asm/errno.h>

/*
 * Kernel pointers have redundant information, so we can use a
 * scheme where we can return either an error code or a normal
 * pointer with the same return value.
 *
 * This should be a per-architecture thing, to allow different
 * error and pointer decisions.
 */
#define MAX_ERRNO   4095

#ifndef __ASSEMBLY__

#define IS_ERR_VALUE(x) unlikely((x) >= (unsigned long)-MAX_ERRNO)

static inline void * __must_check ERR_PTR(long error)
{
    return (void *) error;
}

static inline long __must_check PTR_ERR(__force const void *ptr)
{
    return (long) ptr;
}

static inline bool __must_check IS_ERR(__force const void *ptr)
{
    return IS_ERR_VALUE((unsigned long)ptr);
}

static inline bool __must_check IS_ERR_OR_NULL(__force const void *ptr)
{
    return !ptr || IS_ERR_VALUE((unsigned long)ptr);
}
```

要想明白上述的代码，首先要理解内核空间。所有的驱动程序都是运行在内核空间，内核空间虽然很大，但总是有限的，而在这有限的空间中，其最后一个 page 是专门保留的，也就是说一般人不可能用到内核空间最后一个 page 的指针。换句话说，你在写设备驱动程序的过程中，涉及到的任何一个指针，必然有三种情况：**有效指针；NULL，空指针；错误指针，或者说无效指针**。

错误指针：指其已经到达了最后一个 page，即内核用最后一页捕捉错误。比如对于 32bit 的系统来说，内核空间最

高地址 0xffffffffffffff，那么最后一个 page 就是指的 0xfffffffff000 0xffffffffffffffff(假设 4k 一个 page)，这段地址是被保留的。内核空间为什么留出最后一个 page？我们知道一个 page 可能是 4k，也可能是更多，比如 8k，但至少它也是 4k，留出一个 page 出来就可以让我们把内核空间的指针来记录错误了。内核返回的指针一般是指向页面的边界 (4k 边界)，即ptr & 0xfff == 0。如果你发现你的一个指针指向这个范围中的某个地址，那么你的代码肯定出错了。IS_ERR() 就是判断指针是否有错，如果指针并不是指向最后一个 page，那么没有问题；如果指针指向了最后一个page，那么说明实际上这不是一个有效的指针，这个指针里保存的实际上是一种错误代码。而通常很常用的方法就是先用 IS_ERR() 来判断是否是错误，然后如果是，那么就调用 PTR_ERR() 来返回这个错误代码。因此，判断一个指针是不是有效的，我们可以调用宏 IS_ERR_VALUE，即判断指针是不是在（0xfffffffff000，0xffffffffffffffff) 之间，因此，可以用 IS_ERR() 来判断内核函数的返回值是不是一个有效的指针。注意这里用 unlikely()的用意！

至于 PTR_ERR(), ERR_PTR()，只是强制转换以下而已。而 PTR_ERR() 只是返回错误代码，也就是提供一个信息给调用者，如果你只需要知道是否出错，而不在乎因为什么而出错，那你当然不用调用 PTR_ERR() 了。如果指针指向了最后一个 page，那么说明实际上这不是一个有效的指针。这个指针里保存的实际上是一种错误代码。而通常很常用的方法就是先用 IS_ERR() 来判断是否是错误，然后如果是，那么就调用 PTR_ERR() 来返回这个错误代码。

**调用位置见**： TCP建立连接中  [tcp_v4_connect 调用 IS_ERR](./)相对应的方法。

### 调用函数

##### BUG_ON

```c
#define BUG_ON(condition) do { 
 if (unlikely((condition)!=0)) BUG(); 
} while(0)
```

如果在程序的执行过程中，觉得该 condition 下是一个 BUG，可以添加此调试信息，查看对应堆栈内容。

##### **WARN_ON**

而 WARN_ON 则是调用 dump_stack，打印堆栈信息，不会 OOPS

```c
#define WARN_ON(condition) do { 
	if (unlikely((condition)!=0)) { 
		printk("Badness in %s at %s:%d/n", __FUNCTION__, __FILE__,__LINE__); 
		dump_stack(); 
	} 
} while (0)
```

## C 语言

#### 结构体初始化

```
typedef struct{
 int a;
char ch;
}flag;
 /*
目的是将 a 初始化为 1,ch 初始化为'u'.
 */
 /* 法一：分别初始化 */
 flag tmp;
 tmp.a=1;
 tmp.ch='u';

 /* 法二：点式初始化 */
flag tmp={.a=1,.ch='u'}; //注意两个变量之间使用 , 而不是;
 /* 法三：*/
 flag tmp={
 a:1,
 ch:'u'
 };
```

当然，我们也可以使用上述任何一种方法只对结构体中的某几个变量进行初始化。

### 位字段

在存数空间极为宝贵的情况下，有可能需要将多个对象保存在要给机器字中。而在linux开发的早期，那时确实空间极其宝贵。于是乎，那一帮黑客们就发明了各种各样的办法。一种常见的办法是使用类似于编译器符号表的单个二进制位标志集合，即定位一系列的2的指数次方的数，即定义一系列的2的指数次方的数，此方法确实有效。但是，仍然十分浪费空间。而且有可能很多位都利用不到。于是乎，他们提出了另一个新的思路即为字段。我们可以利用如下方式定义一个包含3的变量。

```
struct {
	unsigned int a:1;
	unsigned int b:1;
	unsigned int c:1;
}flages;
```

字段可以不命名，无名字段，即只有一个冒号和宽度，起到填充作用。特殊宽度 0可以用来强制在下一个字边界上对齐，一般位于结构体的尾部。
冒号后面表示相应字段的宽度 (二进制宽度)，即不一定非得是 1 位。字段被声明为unsigned int类型，以确保它们是无符号量。
当然我们需要注意，机器是分大端和小端存储的。因此，我们在选择外部定义数据的情况下，必须仔细考虑那一端优先的问题。

同时，字段不是数组，并且没有地址，因此不能对它们使用&运算符

## GCC

## Sparse

## 操作系统

## CPU



## 存储系统