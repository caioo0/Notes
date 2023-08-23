# 名词解释 kubelet

## 简介[ ](https://kubernetes.io/zh-cn/docs/reference/command-line-tools-reference/kubelet/#简介)



![image-20230718134642937](./imgs/image-20230718134642937.png)

[kubelet](./名词解释：kubelet.md)，作为计算节点最核心部分，它负责容器运行时（比如docker项目）交互，而这种交互所依赖的一个称作CRI(container runtime interface)的远程调用接口，该接口定义了容器运行时的各种核心操作，比如启动一个容器需要的所有参数。



kubelet 是在每个节点上运行的主要“节点代理”。它可以使用以下方式之一向API服务器注册：

- 主机名（hostname）
- 覆盖主机名的参数
- 特定于某云驱动的逻辑

kubelet 是基于 PodSpec 来工作的。每个 PodSpec 是一个描述 Pod 的 YAML 或 JSON 对象。 kubelet 接受通过各种机制（主要是通过 apiserver）提供的一组 PodSpec，并确保这些 PodSpec 中描述的容器处于运行状态且运行状况良好。 kubelet 不管理不是由 Kubernetes 创建的容器。

除了来自 API 服务器的 PodSpec 之外，还可以通过以下两种方式将容器清单（manifest）提供给 kubelet。

- 文件（File）：利用命令行参数传递路径。kubelet 周期性地监视此路径下的文件是否有更新。 监视周期默认为 20s，且可通过参数进行配置。

- HTTP 端点（HTTP endpoint）：利用命令行参数指定 HTTP 端点。 此端点的监视周期默认为 20 秒，也可以使用参数进行配置。

```
kubelet [flags]
```
