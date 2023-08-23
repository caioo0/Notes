# 简易Node.js学习



 Node.js 就是运行在服务端的 **JavaScript**。 Node.js 是一个基于 Chrome JavaScript 运行时建立的一个平台。 Node.js 是一个事件驱动 I/O 服务端 JavaScript 环境，基于 Google 的 V8 引擎，V8 引擎执行 Javascript 的速度非常快，性能非常好。

## 使用版本

我们可以使用命令查看当前的Node版本和npm版本

```
D:\>node -v
v14.17.0
D:\>npm -v
6.14.13
```

第一个node.js程序:hello,world!

**脚本模式**

```
'use strict'; # 严格模式 
console.log("Hello World");
```

保存到文件名`helloworld.js`,并通过node命令来执行:

```
node helloworld.js 
```

程序执行后，正常的话，就会在终端输出 Hello World。