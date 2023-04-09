# async

> **“async函数是使用`async`关键字声明的函数。 async函数是`AsyncFunction`构造函数的实例， 并且其中允许使用`await`关键字。`async`和`await`关键字让我们可以用一种更简洁的方式写出基于`Promise`的异步行为，而无需刻意地链式调用`promise`。”**



简单的来说 async await 就是[promise](https://so.csdn.net/so/search?q=promise&spm=1001.2101.3001.7020)的语法糖，可以认知为promise的简写，另外你可以将它是异步转同步的那么一个解决方案。

## 语法

```
async function name(param0) {
  statements
}
async function name(param0, param1) {
  statements
}
async function name(param0, param1, /* … ,*/ paramN) {
  statements
}

```

### [参数](https://developer.mozilla.org/zh-CN/docs/Web/JavaScript/Reference/Statements/async_function#参数)

- `name`

  函数名称。

- `param` 可选

  要传递给函数的参数的名称。

- `statements` 可选

  包含函数主体的表达式。可以使用 `await` 机制。

### [返回值](https://developer.mozilla.org/zh-CN/docs/Web/JavaScript/Reference/Statements/async_function#返回值)

一个 [`Promise`](https://developer.mozilla.org/zh-CN/docs/Web/JavaScript/Reference/Global_Objects/Promise)，这个 promise 要么会通过一个由 async 函数返回的值被解决，要么会通过一个从 async 函数中抛出的（或其中没有被捕获到的）异常被拒绝。

> **备注：** `await`关键字只在 async 函数内有效。如果你在 async 函数体之外使用它，就会抛出语法错误 [`SyntaxError`](https://developer.mozilla.org/zh-CN/docs/Web/JavaScript/Reference/Global_Objects/SyntaxError) 。

> **备注：** `async`/`await`的目的为了简化使用基于 promise 的 API 时所需的语法。`async`/`await` 的行为就好像搭配使用了生成器和 promise。

async 函数一定会返回一个 promise 对象。如果一个 async 函数的返回值看起来不是 promise，那么它将会被隐式地包装在一个 promise 中。

```
//立即执行函数，不了解的话可以去查一下资料
const a = (async () => {
  return 111
})()
console.log(a) // Promise { 111 }

```



## 简单例子

```
function resolveAfter2Seconds() {
  console.log("starting slow promise");
  return new Promise((resolve) => {
    setTimeout(() => {
      resolve("slow");
      console.log("slow promise is done");
    }, 2000);
  });
}

function resolveAfter1Second() {
  console.log("starting fast promise");
  return new Promise((resolve) => {
    setTimeout(() => {
      resolve("fast");
      console.log("fast promise is done");
    }, 1000);
  });
}

async function sequentialStart() {
  console.log("==SEQUENTIAL START==");

  // 1. Execution gets here almost instantly
  const slow = await resolveAfter2Seconds();
  console.log(slow); // 2. this runs 2 seconds after 1.

  const fast = await resolveAfter1Second();
  console.log(fast); // 3. this runs 3 seconds after 1.
}

async function concurrentStart() {
  console.log("==CONCURRENT START with await==");
  const slow = resolveAfter2Seconds(); // starts timer immediately
  const fast = resolveAfter1Second(); // starts timer immediately

  // 1. Execution gets here almost instantly
  console.log(await slow); // 2. this runs 2 seconds after 1.
  console.log(await fast); // 3. this runs 2 seconds after 1., immediately after 2., since fast is already resolved
}

function concurrentPromise() {
  console.log("==CONCURRENT START with Promise.all==");
  return Promise.all([resolveAfter2Seconds(), resolveAfter1Second()]).then(
    (messages) => {
      console.log(messages[0]); // slow
      console.log(messages[1]); // fast
    }
  );
}

async function parallel() {
  console.log("==PARALLEL with await Promise.all==");

  // Start 2 "jobs" in parallel and wait for both of them to complete
  await Promise.all([
    (async () => console.log(await resolveAfter2Seconds()))(),
    (async () => console.log(await resolveAfter1Second()))(),
  ]);
}

sequentialStart(); // after 2 seconds, logs "slow", then after 1 more second, "fast"

// wait above to finish
setTimeout(concurrentStart, 4000); // after 2 seconds, logs "slow" and then "fast"

// wait again
setTimeout(concurrentPromise, 7000); // same as concurrentStart

// wait again
setTimeout(parallel, 10000); // truly parallel: after 1 second, logs "fast", then after 1 more second, "slow"

```



#### await 和并行

在 `sequentialStart` 中，程序在第一个 `await` 停留了 2 秒，然后又在第二个 `await` 停留了 1 秒。直到第一个计时器结束后，第二个计时器才被创建。程序需要 3 秒执行完毕。

在 `concurrentStart` 中，两个计时器被同时创建，然后执行 `await`。这两个计时器同时运行，这意味着程序完成运行只需要 2 秒，而不是 3 秒，即最慢的计时器的时间。

但是 `await` 仍旧是顺序执行的，第二个 `await` 还是得等待第一个执行完。在这个例子中，这使得先运行结束的输出出现在最慢的输出之后。

如果你希望并行执行两个或更多的任务，你必须像在`parallel`中一样使用`await Promise.all([job1(), job2()])`。





资料来源：https://developer.mozilla.org/zh-CN/docs/Web/JavaScript/Reference/Statements/async_function