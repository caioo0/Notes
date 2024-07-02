# Protobuf语言指南

Protobuf 是 protocol buffers 的简称，它是google公司开发的一种数据描述语言，用于描述一种轻便高效的结构化数据存储格式，并于2008年对外开源。

protobuf 可以用于结构化数据串行化，或者说序列化。 非常适合用于网络通讯中的数据载体，很适合做数据存储或RPC数据交换格式。

protobuf中最基本的数据单元是message,类似GO语言中结构体的存在。

一个简单的例子

```
syntax = "proto3"

message SearchRequest {
	String query = 1;
	int32 page_number = 2;
	int32 result_per_page = 3;
}
```

- `.proto`文件的第一行指定了使用`proto3`语法。如果省略protocol buffer编译器默认使用`proto2`语法。他必须是文件中非空非注释行的第一行。
- `SearchRequest`定义中指定了三个字段(name/value键值对)，每个字段都会有名称和类型。



## Protobuf生成Go代码指南

Protobuf核心的工具集是C++语言开发的，官方的protoc编译器中并不支持Go语言，需要安装一个插件才能生成Go代码。用如下命令安装：

```
$ go get github.com/golang/protobuf/protoc-gen-go
```

提供了一个`protoc-gen-go`二进制文件，当编译器调用时传递了`--go_out`命令行标志时`protoc`就会使用它。`--go_out`告诉编译器把Go源代码写到哪里。编译器会为每个`.proto`文件生成一个单独的源代码文件。

更多详细见：https://segmentfault.com/a/1190000020418571