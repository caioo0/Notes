# vite 

## vite 初体验

你可以通过 [StackBlitz](https://vite.new/) 在线试用 vite。它直接在浏览器中运行基于 Vite 的构建，因此它与本地开发几乎无差别，同时无需在你的机器上安装任何东西。你可以浏览 `vite.new/{template}` 来选择你要使用的框架。



### 搭建第一个vite项目

> 兼容性注意
>
> Vite 需要 [Node.js](https://nodejs.org/en/) 版本 14.18+，16+。然而，有些模板需要依赖更高的 Node 版本才能正常运行，当你的包管理器发出警告时，请注意升级你的 Node 版本。

```
 yarn create vite
 npm create vite@latest
 pnpm create vite
```

运行三种方法之一，然后按照提示操作即可！

你还可以通过附加的命令行选项直接指定项目名称和你想要使用的模板。例如，要构建一个 Vite + react+ts 项目，运行:

```
  yarn create vite vite-project --template react
  cd vite-project
  yarn           
  yarn dev
```

