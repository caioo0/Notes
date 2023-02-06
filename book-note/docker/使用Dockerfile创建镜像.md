# 使用Dockerfile创建镜像



[Docker](https://so.csdn.net/so/search?q=Docker&spm=1001.2101.3001.7020)提供了两种构建镜像的方法：dokcer commit 命令与docker文件

## Dockerfile 解析

Dockerfile是一个文本格式的配置文件，用户可以使用Dockerfile来快速创建自定义的镜像。

- 官网：https://docs.docker.com/engine/reference/builder/
- 构建步骤
  - 编写Dockerfile文件
  - docker bulid 命令构建镜像
  - docker run 依镜像运行容器示例

### Dockerfile构建过程解析

- docker执行docker的大致流程
  - docker从基础镜像运行一个容器
  - 执行一条指令并对容器做出修改
  - 执行类型