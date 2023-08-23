# 使用Go遇到的各种问题



# 1、Go构建项目的时候，解决missing go.sum entry for module providing package ＜package_name＞

**解决方案一：**

当在代码中使用了[第三方库](https://so.csdn.net/so/search?q=第三方库&spm=1001.2101.3001.7020) ，但是go.mod中并没有跟着更新的时候

如果直接run或者build就会报这个错误

missing go.sum entry for [module](https://so.csdn.net/so/search?q=module&spm=1001.2101.3001.7020) providing package <package_name>

可以使用go mod tidy 来整理依赖

这个命令会：

删除不需要的依赖包

下载新的依赖包

更新go.sum
 

**解决方案二：**

```shell
go build -mod=mod
```

本人遇到同样的问题，就是用方案解决的。



:::tip ⚠️注意 在windows环境如果没有安装中CGO，会出现这个问题；

```bash
E:\go-admin>go build
# github.com/mattn/go-sqlite3
cgo: exec /missing-cc: exec: "/missing-cc": file does not exist
```

or

```bash
D:\Code\go-admin>go build
# github.com/mattn/go-sqlite3
cgo: exec gcc: exec: "gcc": executable file not found in %PATH%
```

[解决cgo问题进入](https://doc.go-admin.dev/guide/other/faq.html#_5-cgo-exec-missing-cc-exec-missing-cc-file-does-not-exist)

:::