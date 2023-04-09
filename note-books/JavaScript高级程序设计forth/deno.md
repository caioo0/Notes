## **了不起的 Deno 入门篇**

### **一、Deno 简介**

Deno 是一个 JavaScript/TypeScript 的运行时，默认使用安全环境执行代码，有着卓越的开发体验。Deno 含有以下功能亮点：

- 默认安全。外部代码没有文件系统、网络、环境的访问权限，除非显式开启。
- 支持开箱即用的 TypeScript 的环境。
- 只分发一个独立的可执行文件（deno）。
- 有着内建的工具箱，比如一个依赖信息查看器（deno info）和一个代码格式化工具（deno fmt）。
- 有一组经过审计的 标准模块，保证能在 Deno 上工作。
- 脚本代码能被打包为一个单独的 JavaScript 文件。

Deno 是一个跨平台的运行时，即基于 Google V8 引擎的运行时环境，该运行时环境是使用 Rust 语言开发的，并使用 Tokio 库来构建事件循环系统。Deno 建立在 V8、Rust 和 Tokio 的基础上，它的架构如下：

![img](https://pic2.zhimg.com/80/v2-7e2c633b45c9400732079edf786285e1_720w.webp)

（图片来源：[https://deno.land/manual/contributing/architecture](https://link.zhihu.com/?target=https%3A//deno.land/manual/contributing/architecture)）

### **1.1 Rust**

Rust 是由 Mozilla 主导开发的通用、编译型编程语言。设计准则为 “安全、并发、实用”，支持函数式、并发式、过程式以及面向对象的编程风格。Deno 使用 Rust 语言来封装 V8 引擎，通过 `libdeno` 绑定，我们就可以在 JavaScript 中调用隔离的功能。

### **1.2 Tokio**

Tokio 是 Rust 编程语言的异步运行时，提供异步事件驱动平台，构建快速，可靠和轻量级网络应用。利用 Rust 的所有权和并发模型确保线程安全。Tokio 构建于 Rust 之上，提供极快的性能，使其成为高性能服务器应用程序的理想选择。在 Deno 中 Tokio 用于并行执行所有的异步 IO 任务。

### **1.3 V8**

V8 是一个由 Google 开发的开源 JavaScript 引擎，用于 Google Chrome 及 Chromium 中。V8 在运行之前将JavaScript 编译成了机器代码，而非字节码或是解释执行它，以此提升性能。更进一步，使用了如内联缓存（inline caching）等方法来提高性能。有了这些功能，JavaScript 程序与 V8 引擎的速度媲美二进制编译。在 Deno 中，V8 引擎用于执行 JavaScript 代码。

### **二、安装 Deno**

Deno 能够在 macOS、Linux 和 Windows 上运行。Deno 是一个单独的可执行文件，它没有额外的依赖。你可以通过以下方式来安装它：

- 使用 Shell (macOS 和 Linux)：

```text
curl -fsSL https://deno.land/x/install/install.sh | sh
```

- 使用 PowerShell (Windows)：

```text
iwr https://deno.land/x/install/install.ps1 -useb | iex
```

- 使用 **[Scoop](https://link.zhihu.com/?target=https%3A//scoop.sh/)** (Windows)：

```text
scoop install deno
```

- 使用 **[Chocolatey](https://link.zhihu.com/?target=https%3A//chocolatey.org/packages/deno)** (Windows)：

```text
choco install deno
```

- 使用 **[Homebrew](https://link.zhihu.com/?target=https%3A//formulae.brew.sh/formula/deno)** (macOS)：

```text
brew install deno
```

- 使用 **[Cargo](https://link.zhihu.com/?target=https%3A//crates.io/crates/deno)** (Windows，macOS，Linux)：

```text
cargo install deno
```

Deno 也可以手动安装，只需从 **[github.com/denoland/deno/releases](https://link.zhihu.com/?target=https%3A//github.com/denoland/deno/releases)** 下载一个 zip 文件。它仅包含一个单独的可执行文件。在 macOS 和 Linux 上，你需要为它设置执行权限。当你成功安装之后，可以通过执行 `deno --version` 命令来查看已安装的 Deno 版本：

```text
$ deno --version
deno 1.0.0
v8 8.4.300
typescript 3.9.2
```

### **2.1 deno_install**

在安装过程中，如果遇到问题的话，大家可以试试 **justjavac（迷渡）**大神提供的安装脚本 —— **deno_install**。该脚本通过单行命令将 Deno 安装到系统中（国内加速）。

### **2.1.1 安装最新版**

使用 Shell：

```text
curl -fsSL https://x.deno.js.cn/install.sh | sh
```

使用 PowerShell：

```text
iwr https://x.deno.js.cn/install.ps1 -useb -outf install.ps1; .\install.ps1
# iwr https://x.deno.js.cn/install.ps1 -useb | iex
```

### **2.1.2 安装某个特定版本**

使用 Shell：

```text
curl -fsSL https://x.deno.js.cn/install.sh | sh -s v0.41.0
```

使用 PowerShell：

```text
iwr https://x.deno.js.cn/install.ps1 -useb -outf install.ps1; .\install.ps1 v0.41.0
```

> 更多详细的信息可以浏览 **[x.deno.js.cn](https://link.zhihu.com/?target=https%3A//x.deno.js.cn/)** 站点。

### **三、Deno 初体验**

### **3.1 welcome demo**

相信一些读者安装完 Deno 已经迫不及待了，现在我们立马来体验一下 Deno 应用程序。首先打开你熟悉的命令行，然后在命令行输入以下命令：

```text
$ deno run https://deno.land/std/examples/welcome.ts
Download https://deno.land/std/examples/welcome.ts
Warning Implicitly using master branch https://deno.land/std/examples/welcome.ts
Compile https://deno.land/std/examples/welcome.ts
Welcome to Deno  
```

通过观察以上输出，我们可以知道当运行 `deno run https://deno.land/std/examples/welcome.ts` 命令之后，Deno 会先从 `https://deno.land/std/examples/welcome.ts` URL 地址下载 `welcome.ts` 文件，该文件的内容是：

```text
console.log("Welcome to Deno  ");
```

当文件下载成功后，Deno 会对 `welcome.ts` 文件进行编译，即编译成 `welcome.ts.js` 文件，然后再通过 V8 引擎来执行编译生成的 JavaScript 文件。需要注意的是，如果你在命令行重新运行上述命令，则会执行缓存中已生成的文件，并不会再次从网上下载 `welcome.ts` 文件。

```text
$ deno run https://deno.land/std/examples/welcome.ts
Welcome to Deno  
```

那如何证明再次执行上述命令时， Deno 会优先执行缓存中编译生成的 JavaScript 文件呢？这里我们要先介绍一下 `deno info` 命令，该命令用于显示有关缓存或源文件相关的信息：

```text
$ deno info
DENO_DIR location: "/Users/fer/Library/Caches/deno"
Remote modules cache: "/Users/fer/Library/Caches/deno/deps"
TypeScript compiler cache: "/Users/fer/Library/Caches/deno/gen"
```

在上述的输出信息中，我们看到了 **TypeScript compiler cache** 这行记录，很明显这是 TypeScript 编译器缓存的目录，进入该目录后，通过一层层的查找，我们最终在 `examples` 目录下找到了 `welcome.ts.js` 文件：

```text
➜  examples ls
welcome.ts.js     welcome.ts.js.map welcome.ts.meta
```

打开目录中 `welcome.ts.js` 文件，我们可以看到以下内容：

```text
"use strict";
console.log("Welcome to Deno  ");<br/>//# sourceMappingURL=file:///Users/fer/Library/Caches/deno/gen/https/deno.land/std/examples/welcome.ts.js.map
```

下面我们来修改该文件，在文件中添加一行输出信息 `console.log("Hello Semlinker, from Cache");`，具体如下：

```text
"use strict";
console.log("Hello Semlinker, from Cache");
console.log("Welcome to Deno  ");<br/>//# sourceMappingURL=file:///Users/fer/Library/Caches/deno/gen/https/deno.land/std/examples/welcome.ts.js.map
```

接着我们在命令行中重新执行以下命令：

```text
$ deno run https://deno.land/std/examples/welcome.ts
Hello Semlinker, from Cache
Welcome to Deno  
```

那么现在问题又来了，如何强制刷新缓存，即重新编译 TypeScript 代码呢？针对这个问题，在运行 `deno run` 命令时，我们需要添加 `--reload` 标志，来告诉 Deno 需要重新刷新指定文件：

```text
$ deno run --reload https://deno.land/std/examples/welcome.ts
Download https://deno.land/std/examples/welcome.ts
Warning Implicitly using master branch https://deno.land/std/examples/welcome.ts
Compile https://deno.land/std/examples/welcome.ts
Welcome to Deno  
```

除了 `--reload` 标志之外，Deno run 命令还支持很多其他的标志，感兴趣的读者可以运行 `deno run --help` 命令来查看更多的信息。

### **3.2 TCP echo server**

前面我们已经介绍了如何运行官方的 **welcome** 示例，下面我们来介绍如何使用 Deno 创建一个简单的 TCP echo 服务器。首先我们创建一个 **learn-deno** 项目，然后在该项目下新建一个 **quickstart** 目录，接着新建一个 `echo_server.ts` 文件并输入以下代码：

```text
const listener = Deno.listen({ port: 8080 });
console.log("listening on 0.0.0.0:8080");
for await (const conn of listener) {
  Deno.copy(conn, conn);
}
```

> for await...of 语句会在异步或者同步可迭代对象上创建一个迭代循环，包括 String，Array，Array-like 对象（比如 arguments 或者 NodeList)，TypedArray，Map， Set 和自定义的异步或者同步可迭代对象。
> for await...of 的语法如下：
> for await (variable of iterable) { statement }

输入完以上代码之后，相信很多读者会跟我一样，直接在命令行运行以下命令：

```text
➜  quickstart deno run ./echo_server.ts 
Compile file:///Users/fer/LearnProjects/learn-deno/quickstart/echo_server.ts
error: Uncaught PermissionDenied: network access to "0.0.0.0:8080", run again with the --allow-net flag
    at unwrapResponse ($deno$/ops/dispatch_json.ts:43:11)
    at Object.sendSync ($deno$/ops/dispatch_json.ts:72:10)
    at Object.listen ($deno$/ops/net.ts:51:10)
    at Object.listen ($deno$/net.ts:152:22)
    at file:///Users/fer/LearnProjects/learn-deno/quickstart/echo_server.ts:1:23
```

很明显是权限错误，从错误信息中，Deno 告诉我们需要设置 `--allow-net` 标志，以允许网络访问。为什么会这样呢？这是因为 Deno 是一个 JavaScript/TypeScript 的运行时，默认使用安全环境执行代码。下面我们添加 `--allow-net` 标志，然后再次运行 `echo_server.ts` 文件：

```text
➜  quickstart deno run --allow-net ./echo_server.ts
listening on 0.0.0.0:8080
```

当服务器成功运行之后，我们使用 `nc` 命令来测试一下服务器的功能：

```text
➜  ~ nc localhost 8080
hell semlinker
hell semlinker
```

介绍完如何使用 Deno 创建一个简单的 TCP echo 服务器，我们再来介绍一下如何使用 Deno 创建一个简单的 HTTP 服务器。

### **3.3 HTTP Server**

与 TCP Server 一样，在 **quickstart** 目录下，我们新建一个 `http_server.ts` 文件并输入以下内容：

```text
import { serve } from "https://deno.land/std@v0.50.0/http/server.ts";

const PORT = 8080;
const s = serve({ port: PORT });

console.log(` Listening on <http://localhost>:${PORT}/`);

for await (const req of s) {
  req.respond({ body: "Hello Semlinker\\n" });
}
```

> 友情提示：在实际开发过程中，你可以从 [https://deno.land/std](https://link.zhihu.com/?target=https%3A//deno.land/std) 地址获取所需的标准库版本。示例中我们显式指定了版本，当然你也可以不指定版本，比如这样：[https://deno.land/std/http/server.ts](https://link.zhihu.com/?target=https%3A//deno.land/std/http/server.ts) 。

在上述代码中，我们导入了 Deno 标准库 http 模块中 serve 函数，然后使用该函数快速创建 HTTP 服务器，该函数的定义如下：

```text
// std/http/server.ts
export function serve(addr: string | HTTPOptions): Server {
  if (typeof addr === "string") {
    const [hostname, port] = addr.split(":");
    addr = { hostname, port: Number(port) };
  }

  const listener = listen(addr);
  return new Server(listener);
}
```

serve 函数接收一个参数，其类型是 `string | HTTPOptions`，其中 HTTPOptions 接口的定义如下：

```text
/** Options for creating an HTTP server. */
export type HTTPOptions = Omit<Deno.ListenOptions, "transport">;

export interface ListenOptions {
    /** The port to listen on. */
    port: number;
    /** A literal IP address or host name that can be resolved to an IP address.
     * If not specified, defaults to `0.0.0.0`. */
    hostname?: string;
}
```

当输入的参数类型是字符串时，serve 函数会使用 `:` 冒号对字符串进行切割，获取 hostname 和 port，然后包装成对象赋值给 addr 参数，接着使用 addr 参数继续调用 `listen` 函数进一步创建 `listener` 对象，最终调用 `new Server(listener)` 创建 HTTP 服务器。

创建完 HTTP 服务器，我们来启动该服务器，打开命令行输入以下命令：

```text
➜  quickstart deno run --allow-net ./http_server.ts 
Compile file:///Users/fer/LearnProjects/learn-deno/quickstart/http_server.ts
 Listening on <http://localhost>:8080/
```

接着打开浏览器，在地址栏上输入 http://localhost:8080/ 地址，之后在当前页面中会看到以下内容：

```text
Hello World\n
```

### **四、调试 Deno**

Deno 支持 **[V8 Inspector Protocol](https://link.zhihu.com/?target=https%3A//v8.dev/docs/inspector)**。使用 Chrome Devtools 或其他支持该协议的客户端（比如 VSCode）能够调试 Deno 程序。要启用调试功能，用 `--inspect` 或 `--inspect-brk` 选项运行 Deno，对应的选项描述如下：

```text
--inspect=<HOST:PORT>
  activate inspector on host:port (default: 127.0.0.1:9229)

--inspect-brk=<HOST:PORT>
  activate inspector on host:port and break at start of user script
```

`--inspect` 选项允许在任何时间点连接调试器，而 `--inspect-brk` 选项会等待调试器连接，在第一行代码处暂停执行。

### **4.1 Chrome Devtools**

让我们用 Chrome 开发者工具来调试一个简单的程序，我们将使用来自 `std` 的 **[file_server.ts](https://link.zhihu.com/?target=https%3A//deno.land/std%40v0.50.0/http/file_server.ts)**，这是一个简单的静态文件服务。

使用 `--inspect-brk` 选项，在第一行代码处暂停执行。

```text
$ deno run --inspect-brk --allow-read --allow-net https://deno.land/std@v0.50.0/http/file_server.ts
Debugger listening on ws://127.0.0.1:9229/ws/1e82c406-85a9-44ab-86b6-7341583480b1
Download https://deno.land/std@v0.50.0/http/file_server.ts
Compile https://deno.land/std@v0.50.0/http/file_server.ts
...
```

打开 `chrome://inspect`，点击 Target 旁边的 `Inspect`。

> 进一步了解更详细的调试说明，可访问 [https://deno.land/manual/tools/debugger](https://link.zhihu.com/?target=https%3A//deno.land/manual/tools/debugger) URL 地址。

### **4.2 VSCode**

Deno 可以在 VSCode 中调试。插件的官方支持正在开发中 [https://github.com/denoland/vscode_deno/issues/12](https://link.zhihu.com/?target=https%3A//github.com/denoland/vscode_deno/issues/12)，当然我们也可以通过手动提供 `launch.json` 配置，来连接调试器：

```text
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Deno",
      "type": "node",
      "request": "launch",
      "cwd": "${workspaceFolder}",
      "runtimeExecutable": "deno",
      "runtimeArgs": ["run", "--inspect-brk", "-A", "<entry_point>"],
      "port": 9229
    }
  ]
}
```

**注意**：将 `<entry_point>` 替换为实际的脚本名称。

下面让我们来尝试一下调试本地源文件，创建 `server.ts`：

```text
import { serve } from "https://deno.land/std@v0.50.0/http/server.ts";
const s = serve({ port: 8000 });
console.log("http://localhost:8000/");

for await (const req of s) {
  req.respond({ body: "Hello World\n" });
}
```

将 `<entry_point>` 改为 `server.ts`，然后运行。

![img](https://pic2.zhimg.com/80/v2-9556f91a641e9086aec724bf96cab1e5_720w.webp)

（图片来源：[https://deno.land/manual/tools/debugger](https://link.zhihu.com/?target=https%3A//deno.land/manual/tools/debugger)）

![img](https://pic1.zhimg.com/80/v2-b6b29a51435fdac1e85fb74cf491a8d8_720w.webp)

（图片来源：[https://deno.land/manual/tools/debugger](https://link.zhihu.com/?target=https%3A//deno.land/manual/tools/debugger)）

> 若想进一步了解 Deno 与 Node.js 的 区别，可以阅读 **超杰_** **[Deno 正式发布，彻底弄明白和 node 的区别](https://link.zhihu.com/?target=https%3A//juejin.im/post/5ebcad19f265da7bb07656c7)** 这篇文章。

## **了不起的 Deno 实战篇**

### **五、Oak 简介**

相信接触过 Node.js 的读者对 Express、Hapi、Koa 这些 Web 应用开发框架都不会陌生，在 Deno 平台中如果你也想做 Web 应用开发，可以考虑直接使用以下现成的框架：

- **[deno-drash](https://link.zhihu.com/?target=https%3A//github.com/drashland/deno-drash)**：A REST microframework for Deno with zero dependencies。
- **[deno-express](https://link.zhihu.com/?target=https%3A//github.com/NMathar/deno-express)**：Node Express way for Deno。
- **[oak](https://link.zhihu.com/?target=https%3A//github.com/oakserver/oak)**：A middleware framework for Deno's net server 。
- **[pogo](https://link.zhihu.com/?target=https%3A//github.com/sholladay/pogo)**：Server framework for Deno。
- **[servest](https://link.zhihu.com/?target=https%3A//github.com/keroxp/servest)**： A progressive http server for Deno 。

写作本文时，目前 Star 数最高的项目是 Oak，加上我的一个 Star，刚好 720。 下面我们来简单介绍一下 **[Oak](https://link.zhihu.com/?target=https%3A//oakserver.github.io/oak/)**：

> A middleware framework for Deno's **[http](https://link.zhihu.com/?target=https%3A//github.com/denoland/deno_std/tree/master/http%23http)** server, including a router middleware.
> This middleware framework is inspired by **[Koa](https://link.zhihu.com/?target=https%3A//github.com/koajs/koa)** and middleware router inspired by **[koa-router](https://link.zhihu.com/?target=https%3A//github.com/alexmingoia/koa-router/)**.

很显然 Oak 的的灵感来自于 Koa，而路由中间件的灵感来源于 koa-router 这个库。如果你以前使用过 Koa 的话，相信你会很容易上手 Oak。不信的话，我们来看个示例：

```text
import { Application } from "https://deno.land/x/oak/mod.ts";

const app = new Application();

app.use((ctx) => {
  ctx.response.body = "Hello Semlinker!";
});

await app.listen({ port: 8000 });
```

以上示例对于每个 HTTP 请求，都会响应 **"Hello Semlinker!"**。只有一个中间件是不是感觉太 easy 了，下面我们来看一个更复杂的示例（使用多个中间件）：

```text
import { Application } from "https://deno.land/x/oak/mod.ts";

const app = new Application();

// Logger
app.use(async (ctx, next) => {
  await next();
  const rt = ctx.response.headers.get("X-Response-Time");
  console.log(`${ctx.request.method} ${ctx.request.url} - ${rt}`);
});

// Timing
app.use(async (ctx, next) => {
  const start = Date.now();
  await next();
  const ms = Date.now() - start;
  ctx.response.headers.set("X-Response-Time", `${ms}ms`);
});

// Hello World!
app.use((ctx) => {
  ctx.response.body = "Hello World!";
});

await app.listen({ port: 8000 });
```

为了更好地理解 Oak 中间件流程控制，我们来一起回顾一下 Koa 大名鼎鼎的 “洋葱模型”：

![img](https://pic1.zhimg.com/80/v2-c1636a6344675643e3f3758974e3aacc_720w.webp)

从 “洋葱模型” 示例图中我们可以很清晰的看到一个请求从外到里一层一层的经过中间件，响应时从里到外一层一层的经过中间件。上述代码成功运行后，我们打开浏览器，然后访问 http://localhost:8000/ URL 地址，之后在控制台会输出以下结果：

```text
➜  learn-deno deno run --allow-net oak/oak-middlewares-demo.ts
GET http://localhost:8000/ - 0ms
GET http://localhost:8000/favicon.ico - 0ms
```

好了，介绍完 Oak 的基本使用，接下来我们开始进入正题，即使用 Oak 开发 REST API。

### **六、Oak 实战**

本章节我们将介绍如何使用 Oak 来开发一个 Todo REST API，它支持以下功能：

- 添加新的 Todo
- 显示 Todo 列表
- 获取指定 Todo 的详情
- 移除指定 Todo
- 更新指定 Todo

小伙伴们，你们准备好了没？让我们一起步入 Oak 的世界！

### **6.1 初始化项目结构**

首先我们在 **learn-deno** 项目中，创建一个新的 todos 目录，然后分别创建以下子目录和 TS 文件：

- **handlers 目录：**存放路由处理器；
- **middlewares 目录：** 存放中间件，用于处理每个请求；
- **models 目录：** 存放模型定义，在我们的示例中只包含 Todo 接口；
- **services 目录：** 存放服务层程序；
- **db 目录：** 作为本地数据库，存放 Todo 数据；
- **config.ts：** 包含应用的全局配置信息；
- **index.ts：** 应用的入口文件；
- **routing.ts：** 包含 API 路由信息。

完成项目初始化之后，todos 项目的目录结构如下所示：

```text
└── todos
    ├── config.ts
    ├── db
    ├── handlers
    ├── index.ts
    ├── middlewares
    ├── models
    ├── routing.ts
    └── services
```

如你所见，这个目录结构看起来像一个小型 Node.js Web 应用程序。下一步，我们来创建 Todo 项目的入口文件。

### **6.2 创建入口文件**

**index.ts**

```text
import { Application } from "https://deno.land/x/oak/mod.ts";
import { APP_HOST, APP_PORT } from "./config.ts";
import router from "./routing.ts";
import notFound from "./handlers/notFound.ts";
import errorMiddleware from "./middlewares/error.ts";

const app = new Application();

app.use(errorMiddleware);
app.use(router.routes());
app.use(router.allowedMethods());
app.use(notFound);

console.log(`Listening on ${APP_PORT}...`);

await app.listen(`${APP_HOST}:${APP_PORT}`);
```

在第一行代码中，我们使用了 Deno 所提供的功能特性，即直接从网络上导入模块。除此之外，这里没有什么特别的。我们创建一个应用程序，添加中间件，路由，最后启动服务器。整个流程就像开发普通的 Express/Koa 应用程序一样。

### **6.3 创建配置文件**

**config.ts**

```text
const env = Deno.env.toObject();
export const APP_HOST = env.APP_HOST || "127.0.0.1";
export const APP_PORT = env.APP_PORT || 3000;
export const DB_PATH = env.DB_PATH || "./db/todos.json";
```

为了提高项目的灵活性，我们支持从环境中读取配置信息，同时我们也为每个配置项都提供了相应的默认值。其中 `Deno.env()` 相当于Node.js 平台中的 `process.env`。

### **6.4 添加 Todo 模型**

**models/todo.ts**

```text
export interface Todo {
  id: number;
  userId: number;
  title: string;
  completed: boolean;
}
```

在 Todo 模型中，我们定义了 id、userId、title 和 completed 四个属性，分别表示 todo 编号、用户编号、todo 标题和 todo 完成状态。

### **6.5 添加路由**

**routing.ts**

```text
import { Router } from "https://deno.land/x/oak/mod.ts";

import getTodos from "./handlers/getTodos.ts";
import getTodoDetail from "./handlers/getTodoDetail.ts";
import createTodo from "./handlers/createTodo.ts";
import updateTodo from "./handlers/updateTodo.ts";
import deleteTodo from "./handlers/deleteTodo.ts";

const router = new Router();

router
  .get("/todos", getTodos)
  .get("/todos/:id", getTodoDetail)
  .post("/todos", createTodo)
  .put("/todos/:id", updateTodo)
  .delete("/todos/:id", deleteTodo);

export default router;
```

同样，没有什么特别的，我们创建一个 router 并添加 routes。它看起来几乎与 Express.js 应用程序一模一样。

### **6.6 添加路由处理器**

**handlers/getTodos.ts**

```text
import { Response } from "https://deno.land/x/oak/mod.ts";
import { getTodos } from "../services/todos.ts";

export default async ({ response }: { response: Response }) => {
  response.body = await getTodos();
};
```

**getTodos 处理器用于返回所有的 Todo**。如果你从未使用过 Koa，则 response 对象类似于 Express 中的 res 对象。在 Express 应用中我们会调用 res 对象的 json 或 send 方法来返回响应。而在 Koa/Oak 中，我们需要将响应值赋给 response.body 属性。

------

**handlers/getTodoDetail.ts**

```text
import { Response, RouteParams } from "https://deno.land/x/oak/mod.ts";
import { getTodo } from "../services/todos.ts";

export default async ({
  params,
  response,
}: {
  params: RouteParams;
  response: Response;
}) => {
  const todoId = params.id;

  if (!todoId) {
    response.status = 400;
    response.body = { msg: "Invalid todo id" };
    return;
  }

  const foundedTodo = await getTodo(todoId);
  if (!foundedTodo) {
    response.status = 404;
    response.body = { msg: `Todo with ID ${todoId} not found` };
    return;
  }

  response.body = foundedTodo;
};
```

**getTodoDetail 处理器用于返回指定 id 的 Todo**，如果找不到指定 id 对应的 Todo，会返回 404 和相应的错误消息。

------

**handlers/createTodo.ts**

```text
import { Request, Response } from "https://deno.land/x/oak/mod.ts";
import { createTodo } from "../services/todos.ts";

export default async ({
  request,
  response,
}: {
  request: Request;
  response: Response;
}) => {
  if (!request.hasBody) {
    response.status = 400;
    response.body = { msg: "Invalid todo data" };
    return;
  }

  const {
    value: { userId, title, completed = false },
  } = await request.body();

  if (!userId || !title) {
    response.status = 422;
    response.body = {
      msg: "Incorrect todo data. userId and title are required",
    };
    return;
  }

  const todoId = await createTodo({ userId, title, completed });

  response.body = { msg: "Todo created", todoId };
};
```

**createTodo 处理器用于创建新的 Todo**，在执行新增操作前，会验证是否缺少 `userId` 和 `title` 必填项。

------

**handlers/updateTodo.ts**

```text
import { Request, Response } from "https://deno.land/x/oak/mod.ts";
import { updateTodo } from "../services/todos.ts";

export default async ({
  params,
  request,
  response,
}: {
  params: any;
  request: Request;
  response: Response;
}) => {
  const todoId = params.id;

  if (!todoId) {
    response.status = 400;
    response.body = { msg: "Invalid todo id" };
    return;
  }

  if (!request.hasBody) {
    response.status = 400;
    response.body = { msg: "Invalid todo data" };
    return;
  }

  const {
    value: { title, completed, userId },
  } = await request.body();

  await updateTodo(todoId, { userId, title, completed });

  response.body = { msg: "Todo updated" };
};
```

**updateTodo 处理器用于更新指定的 Todo**，在执行更新前，会判断指定的 Todo 是否存在，当存在的时候才会执行更新操作。

------

**handlers/deleteTodo.ts**

```text
import { Response, RouteParams } from "https://deno.land/x/oak/mod.ts";
import { deleteTodo, getTodo } from "../services/todos.ts";

export default async ({
  params,
  response
}: {
  params: RouteParams;
  response: Response;
}) => {
  const todoId = params.id;

  if (!todoId) {
    response.status = 400;
    response.body = { msg: "Invalid todo id" };
    return;
  }

  const foundTodo = await getTodo(todoId);
  if (!foundTodo) {
    response.status = 404;
    response.body = { msg: `Todo with ID ${todoId} not found` };
    return;
  }

  await deleteTodo(todoId);
  response.body = { msg: "Todo deleted" };
};
```

**deleteTodo 处理器用于删除指定的 Todo**，在执行删除前会校验 todoId 是否为空和对应 Todo 是否存在。

------

除了上面已经定义的处理器，我们还需要处理不存在的路由并返回一条错误消息。

**handlers/notFound.ts**

```text
import { Response } from "https://deno.land/x/oak/mod.ts";

export default ({ response }: { response: Response }) => {
  response.status = 404;
  response.body = { msg: "Not Found" };
};
```

### **6.7 添加服务**

在创建 Todo 服务前，我们先来创建两个小的 `helper`（辅助）服务。

**services/util.ts**

```text
import { v4 as uuid } from "https://deno.land/std/uuid/mod.ts";

export const createId = () => uuid.generate();
```

在 `util.ts` 文件中，我们使用 Deno 标准库的 uuid 模块来为新建的 Todo 生成一个唯一的 id。

------

**services/db.ts**

```text
import { DB_PATH } from "../config.ts";
import { Todo } from "../models/todo.ts";

export const fetchData = async (): Promise<Todo[]> => {
  const data = await Deno.readFile(DB_PATH);

  const decoder = new TextDecoder();
  const decodedData = decoder.decode(data);

  return JSON.parse(decodedData);
};

export const persistData = async (data: Todo[]): Promise<void> => {
  const encoder = new TextEncoder();
  await Deno.writeFile(DB_PATH, encoder.encode(JSON.stringify(data)));
};
```

在我们的示例中，`db.ts` 文件用于实现数据的管理，数据持久化方式使用的是本地的 JSON 文件。为了获取所有的 Todo，我们根据 `DB_PATH` 设置的路径，读取对应的文件内容。 readFile 函数返回一个 Uint8Array 对象，该对象在解析为 JSON 对象之前需要转换为字符串。 Uint8Array 和 TextDecoder 都来自核心 JavaScript API。同样，在存储数据时，需要先把字符串转换为 Uint8Array。

为了让大家更好地理解上面表述的内容，我们来分别看一下 Deno 命名空间下 `readFile` 和 `writeFile` 这两个方法的定义：

**1. Deno.readFile**

```text
 export function readFile(path: string): Promise<Uint8Array>;
```

Deno.readFile 使用示例：

```text
const decoder = new TextDecoder("utf-8");
const data = await Deno.readFile("hello.txt");
console.log(decoder.decode(data));
```

**2. Deno.writeFile**

```text
export function writeFile(
    path: string,
    data: Uint8Array,
    options?: WriteFileOptions
): Promise<void>;
```

Deno.writeFile 使用示例：

```text
const encoder = new TextEncoder();
const data = encoder.encode("Hello world\n");
// overwrite "hello1.txt" or create it
await Deno.writeFile("hello1.txt", data);
// only works if "hello2.txt" exists
await Deno.writeFile("hello2.txt", data, {create: false});  
// set permissions on new file
await Deno.writeFile("hello3.txt", data, {mode: 0o777});  
// add data to the end of the file
await Deno.writeFile("hello4.txt", data, {append: true});  
```

接着我们来定义最核心的 todos.ts 服务，该服务用于实现 Todo 的增删改查。

**services/todos.ts**

```text
import { fetchData, persistData } from "./db.ts";
import { Todo } from "../models/todo.ts";
import { createId } from "../services/util.ts";

type TodoData = Pick<Todo, "userId" | "title" | "completed">;

// 获取Todo列表
export const getTodos = async (): Promise<Todo[]> => {
  const todos = await fetchData();
  return todos.sort((a, b) => a.title.localeCompare(b.title));
};

// 获取Todo详情
export const getTodo = async (todoId: string): Promise<Todo | undefined> => {
  const todos = await fetchData();

  return todos.find(({ id }) => id === todoId);
};

// 新建Todo
export const createTodo = async (todoData: TodoData): Promise<string> => {
  const todos = await fetchData();

  const newTodo: Todo = {
    ...todoData,
    id: createId(),
  };

  await persistData([...todos, newTodo]);

  return newTodo.id;
};

// 更新Todo
export const updateTodo = async (
  todoId: string,
  todoData: TodoData
): Promise<void> => {
  const todo = await getTodo(todoId);

  if (!todo) {
    throw new Error("Todo not found");
  }

  const updatedTodo = {
    ...todo,
    ...todoData,
  };

  const todos = await fetchData();
  const filteredTodos = todos.filter((todo) => todo.id !== todoId);

  persistData([...filteredTodos, updatedTodo]);
};

// 删除Todo
export const deleteTodo = async (todoId: string): Promise<void> => {
  const todos = await getTodos();
  const filteredTodos = todos.filter((todo) => todo.id !== todoId);

  persistData(filteredTodos);
};
```

### **6.8 添加异常处理中间件**

如果用户服务出现错误，会发生什么情况？这将可能导致整个应用程序奔溃。为了避免出现这种情况，我们可以在每个处理程序中添加 `try/catch` 块，但其实还有一个更好的解决方案，即在所有路由之前添加异常处理中间件，在该中间件内部来捕获所有异常。

**middlewares/error.ts**

```text
import { Response } from "https://deno.land/x/oak/mod.ts";

export default async (
  { response }: { response: Response },
  next: () => Promise<void>
) => {
  try {
    await next();
  } catch (err) {
    response.status = 500;
    response.body = { msg: err.message };
  }
};
```

### **6.9 功能验证**

Todo 功能开发完成后，我们可以使用 HTTP 客户端来进行接口测试，这里我使用的是 VSCode IDE 下的 **[REST Client](https://link.zhihu.com/?target=https%3A//marketplace.visualstudio.com/items%3FitemName%3Dhumao.rest-client)** 扩展，首先我们在项目根目录下新建一个 `todo.http` 文件，然后复制以下内容：

```text
### 获取Todo列表
GET http://localhost:3000/todos HTTP/1.1

### 获取Todo详情

GET http://localhost:3000/todos/${todoId}

### 新增Todo

POST http://localhost:3000/todos HTTP/1.1
content-type: application/json

{
    "userId": 666,
    "title": "Learn Deno"
}

### 更新Todo
PUT http://localhost:3000/todos/${todoId} HTTP/1.1
content-type: application/json

{
    "userId": 666,
    "title": "Learn Deno",
    "completed": true  
}

### 删除Todo
DELETE  http://localhost:3000/todos/${todoId} HTTP/1.1
```

> 友情提示：**需要注意的是 `todo.http` 文件中的 `${todoId}` 需要替换为实际的 Todo 编号，该编号可以先通过新增 Todo，然后从 `db/todos.json` 文件中获取。**

万事具备只欠东风，接下来就是启动我们的 Todo 应用了，进入 Todo 项目的根目录，然后在命令行中运行 `deno run -A index.ts` 命令：

```text
$ deno run -A index.ts
Listening on 3000...
```

在以上命令中的 `-A` 标志，与 `--allow-all` 标志是等价的，表示允许所有权限。

```text
-A, --allow-all
        Allow all permissions
        --allow-env
            Allow environment access
        --allow-hrtime
            Allow high resolution time measurement
        --allow-net=<allow-net>
            Allow network access
        --allow-plugin
            Allow loading plugins
        --allow-read=<allow-read>
            Allow file system read access
        --allow-run
            Allow running subprocesses
        --allow-write=<allow-write>
            Allow file system write access
```

可能有一些读者还没使用过 **[REST Client](https://link.zhihu.com/?target=https%3A//marketplace.visualstudio.com/items%3FitemName%3Dhumao.rest-client)** 扩展，这里我来演示一下如何新增 Todo：

![img](https://pic3.zhimg.com/80/v2-7ed0edf0dd923b4ac21379e9cb320242_720w.webp)

从返回的 HTTP 响应报文，我们可以知道 **Learn Deno** 的 Todo 已经新增成功了，安全起见让我们来打开 Todo 根目录下的 **db** 目录中的 **todos.json** 文件，验证一下是否 “入库” 成功，具体如下图所示：

![img](https://pic1.zhimg.com/80/v2-3b3bb102874bca80f2c2735f609ec464_720w.webp)

从图可知 **Learn Deno** 的 Todo 的确新增成功了，对于其他的接口有兴趣的读者可以自行测试一下。

> Deno 实战之 Todo 项目源码：[https://github.com/semlinker/deno-todos-api](https://link.zhihu.com/?target=https%3A//github.com/semlinker/deno-todos-api)

### **七、参考资源**

- **[Deno 中文手册](https://link.zhihu.com/?target=https%3A//nugine.github.io/deno-manual-cn/introduction.html)**
- **[Github - oak](https://link.zhihu.com/?target=https%3A//github.com/oakserver/oak)**
- **[the-deno-handbook](https://link.zhihu.com/?target=https%3A//www.freecodecamp.org/news/the-deno-handbook/)**
- **[deno-first-approach](https://link.zhihu.com/?target=https%3A//dev.to/lsagetlethias/deno-first-approach-4d0)**
- **[the-deno-handbook](https://link.zhihu.com/?target=https%3A//www.freecodecamp.org/news/the-deno-handbook)**
- **[write-a-small-api-using-deno](https://link.zhihu.com/?target=https%3A//dev.to/kryz/write-a-small-api-using-deno-1cl0)**



来源：https://zhuanlan.zhihu.com/p/141832695