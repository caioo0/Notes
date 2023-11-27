# **第1章 理解网络编程和套接字**

## **1.1 理解网络编程和套接字**

### **服务器端套接字**

套接字编程所用的各函数

```c
#include <sys/socket.h>
int socket(int domain, int type, int protocol);       
                // 功能：创建套接字。
                // 参数：domain：采取的协议族，一般为 PF_INET；type：数据传输方式，一般为 SOCK_STREAM；protocol：一般设为 0 即可。
                // 返回值：成功时返回文件描述符，失败时返回 -1
int bind(int sockfd, struct sockaddr *myaddr, socklen_t addrlen);  
                // 功能：为套接字分配地址信息。
                // 参数：sockfd：要分配地址信息的套接字文件描述符；myaddr：存有地址信息的结构体变量指针；addrlen：第二个参数的长度。
                // 返回值：成功时返回 0，失败时返回 -1
int listen(int sockfd, int backlog);  
                // 功能：将套接字转换为可接收连接的状态。
                // 参数：sock：希望进入等待连接请求状态的套接字文件描述符；backlog：连接请求等待队列的长度，最多使 backlog 个连接请求进入队列。
                // 返回值：成功时返回 0，失败时返回 -1
int accept(int sockfd, struct sockaddr *addr, socklen_t addrlen);  
                // 功能：受理连接请求等待队列中待处理的连接请求。
                // 参数：sock：服务器套接字的文件描述符；addr：用于保存发起连接请求的客户端地址信息；addrlen：第二个参数的长度。
                // 返回值：成功时返回创建的套接字文件描述符，失败时返回 -1
```

**接受连接请求的服务器端套接字编程流程：**

1. 调用 socket 函数创建套接字；
2. 调用 bind 函数为套接字分配 IP 地址与端口号；
3. 调用 listen 函数将套接字转换为可接收状态；
4. 调用 accept 函数受理连接请求。accept 会阻塞，直到有连接请求才会返回；
5. 调用 read/write 函数进行数据交换；
6. 调用 close 函数断开连接；

### **客户端套接字**

```c
#include <sys/socket.h>
int connect(int sockfd, struct sockaddr *serv_addr, socklen_t addrlen);  
                // 功能：请求连接。
                // 参数：sock：客户端套接字的文件描述符；serv_addr：保存目标服务器端地址信息的结构体指针；addrlen：第二个参数的长度（单位是字节）
                // 返回值：成功时返回 0，失败时返回 -1
```

**客户端请求连接步骤：**

1. 调用 socket 函数创建套接字；
2. 调用 connect 函数请求连接；
3. 调用 read/write 函数进行数据交换；
4. 调用 close 函数断开连接；

> 客户端的 IP 地址和端口在调用 connect 函数时自动分配，无需调用 bind 函数。

## **1.2 基于Linux的文件操作**

Linux 中**套接字描述符也是文件**，因此通过套接字发送、接收数据就和读写文件一样，通过 read、write 这些函数来接收、发送数据。

文件描述符是系统分配给文件或套接字的整数。

**0、1、2 分别由系统分配给了标准输入、标准输出和标准错误。**

文件和套接字创建时才会被分配文件描述符。它们的文件描述符会从 3 开始按序递增。

> Windows 系统中术语**”句柄“**和 Linux 中的文件描述符含义相同。

```C
#include<fcntl.h>       // fcntl.h 和 unistd.h 包含的内容有些相似，包括 open 函数等。总之使用文件函数时将 fcntl.h 和 unistd.h 都 include 就可以了
#include<unistd.h>
int open(const char *path, int flag);                   
                        // 功能：按 flag 指定的模式打开文件。
                        // 参数：path：文件名的地址；flag：文件打开的模式。
                        // 返回值：成功时返回文件描述符，失败时返回 -1
int close(int fd);
                        // 功能：关闭 fd 对应的文件或套接字。当关闭一个套接字时会向对方发送 EOF。
                        // 参数：fd：文件或套接字的文件描述符。
                        // 返回值：成功时返回 0，失败时返回 -1
ssize_t read(int fd, void* buf, size_t nbytes);  
                        // 功能：从文件 fd 读取数据。read 函数会阻塞，直到读取到数据或 EOF 才返回。
                        // 参数：fd：文件描述符；buf：保存要接收的数据；nbytes：要接收的最大字节数。
                        // 返回值：成功时返回接收的字节数（遇到文件尾则返回 0），失败时返回 -1
ssize_t write(int fd, const void* buf, size_t nbytes);  
                        // 功能：向文件 fd 输出数据。
                        // 参数：fd：文件描述符；buf：要传输的数据；nbytes：要传输的字节数。
                        // 返回值：成功时返回写入的字节数，失败时返回 -1
```

**EOF** 即表示文件尾。

**size_t** 的类型是 unsigned int，**ssize_t** 的类型是 signed int。

![image-20231117110433021](D:\www\learning\caioo0.github.io\note-coding\docs\TCPIP网络编程\img\image-20231117110433021.png)

### **1.3 基于Windows平台的实现**

Windows 套接字（简称 winsock）大部分是参考 UNIX 套接字设计的，与 Linux 套接字很相似但不完全相同。

大多数项目都是在 Linux 系统下开发服务器端，在 Windows 平台下开发客户端。

**为 Windows 套接字编程设置头文件和库**

设置前置：

1. 链接 **ws2_32.lib** 库。在 VS 中通过：项目=》属性=》配置属性=》链接器=》输入=》附加依赖项 添加 ws2_32.lib 库即可。
2. 导入头文件 **WinSock2.h**。Windows 中有一个 winsock.h 和一个 WinSock2.h。其中 WinSock2.h 是较新版本，用来代替前者的。

>  实际上在 windows 上还需要通过：项目=》属性=》配置属性=》C++ 将 **SDL 检查**设为否，否则运行会出错。

**Winsock的初始化**

进行 Winsock 编程时，必须首先调用 WSAStartup 函数，设置程序中用到的 Winsock 版本，并初始化相应版本的库。

```c
#include <WinSock2.h>
int WSAStartup(WORD wVersionRequested, LPWSADATA lpWSAData);  // wVersionRequested：要用的 Winsock版本信息，lpWSAData：WSADATA 结构体变量的地址值
                             // 成功时返回 0，失败时返回非 0 的错误代码值
```

两个参数的详细介绍：

1. WORD wVersionRequested：WORD 类型是通过 typedef 定义的 unsigned short 类型。Winsock 中存在多个套接字版本，要选择需要的版本，0x0202 表示 2.2 版本。

2. 1. 可以用 MAKEWORD(2, 2) 来构造版本号，它构造了 2.2 版本的表示值，即返回 0x0202。

3. LPWSADATA lpWSAData：LPWSADATA 是 WSADATA 类型的指针类型。没有特殊含义，只是为了调用函数，必须传递 WSADATA 类型变量的地址。

**WSAStartup 函数的调用过程**

下面这段代码几乎是 Winsock 编程的公式。在进行 Winsock 编程时直接按下述方式编写即可。

```c
int main(int argc, char* argv[])
{
    WSADATA wsaData;
    ...
    if(WSAStartup(MAKEWORD9(2, 2), &wsaData) != 0)
        ErrorHandling("WSAStartup() error");
    ...
    return 0;    
}
```

**注销**

```c
#include <WinSock2.h>
int WSACleanup(void);  // 调用此函数，Winsock 相关库将还给操作系统，无法再调用 Winsock 相关函数。
                // 成功时返回 0，失败时返回 SOCKET_ERROR
```

### **1.4 基于Windows的套接字相关函数及示例**

**基于 Windows 的套接字相关函数**

SOCKET 是 typedef 定义的整型类型

```c
#include <WinSock2.h>
SOCKET socket(int af, int type, int protocol);                   // 成功时返回套接字句柄，失败时返回 INVALID_SOCKET
int bind(SOCKET s, const struct sockaddr* name, int namelen);    // 成功时返回 0，失败时返回 SOCKET_ERROR
int listen(SOCKET s, int backlog);                               // 成功时返回 0，失败时返回 SOCKET_ERROR
SOCKET accept(SOCKET s, struct sockaddr* addr, int* addrlen);    // 成功时返回套接字句柄，失败时返回 INVALID_SOCKET
int connect(SOCKET s, const struct sockaddr* name, int namelen); // 成功时返回 0，失败时返回 SOCKET_ERROR
int closesocket(SOCKET s);                                       // 成功时返回 0，失败时返回 SOCKET_ERROR
```

