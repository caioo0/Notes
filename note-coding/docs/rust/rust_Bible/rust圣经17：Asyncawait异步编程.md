# Async 编程介绍

### async/.await 简单入门

`async/.await` 是 Rust 内置的语言特性，可以让我们用同步的方式去编写异步的代码。

通过 `async` 标记的语法块会被转换成实现了`Future`特征的状态机。 与同步调用阻塞当前线程不同，当`Future`执行并遇到阻塞时，它会让出当前线程的控制权，这样其它的`Future`就可以在该线程中运行，这种方式完全不会导致当前线程的阻塞。

下面我们来通过例子学习 `async/.await` 关键字该如何使用，在开始之前，需要先引入 `futures` 包。编辑 `Cargo.toml` 文件并添加以下内容:

```toml
[dependencies]
futures = "0.3"
```

#### 使用 async

首先，使用 `async fn` 语法来创建一个异步函数:

```rust
async fn do_something() {
    println!("go go go !");
}
```

需要注意，**异步函数的返回值是一个 `Future`**，若直接调用该函数，不会输出任何结果，因为 `Future` 还未被执行：

```rust
fn main() {
      do_something();
}
```

运行后，`go go go`并没有打印，同时编译器给予一个提示：`warning: unused implementer of Future that must be used`，告诉我们 `Future` 未被使用，那么到底该如何使用？答案是使用一个执行器( `executor` ):

```rust
// `block_on`会阻塞当前线程直到指定的`Future`执行完成，这种阻塞当前线程以等待任务完成的方式较为简单、粗暴，
// 好在其它运行时的执行器(executor)会提供更加复杂的行为，例如将多个`future`调度到同一个线程上执行。
use futures::executor::block_on;

async fn hello_world() {
    println!("hello, world!");
}

fn main() {
    let future = hello_world(); // 返回一个Future, 因此不会打印任何输出
    block_on(future); // 执行`Future`并等待其运行完成，此时"hello, world!"会被打印输出
}
```

#### 使用.await

在上述代码的`main`函数中，我们使用`block_on`这个执行器等待`Future`的完成，让代码看上去非常像是同步代码，但是如果你要在一个`async fn`函数中去调用另一个`async fn`并等待其完成后再执行后续的代码，该如何做？例如:

```rust
use futures::executor::block_on;

async fn hello_world() {
    hello_cat();
    println!("hello, world!");
}

async fn hello_cat() {
    println!("hello, kitty!");
}
fn main() {
    let future = hello_world();
    block_on(future);
}
```

这里，我们在`hello_world`异步函数中先调用了另一个异步函数`hello_cat`，然后再输出`hello, world!`，看看运行结果：

```console
warning: unused implementer of `futures::Future` that must be used
 --> src/main.rs:6:5
  |
6 |     hello_cat();
  |     ^^^^^^^^^^^^
= note: futures do nothing unless you `.await` or poll them
...
hello, world!
```

不出所料，`main`函数中的`future`我们通过`block_on`函数进行了运行，但是这里的`hello_cat`返回的`Future`却没有任何人去执行它，不过好在编译器友善的给出了提示：```futures do nothing unless you `.await` or poll them```，两种解决方法：使用`.await`语法或者对`Future`进行轮询(`poll`)。

后者较为复杂，暂且不表，先来使用`.await`试试:

```rust
use futures::executor::block_on;

async fn hello_world() {
    hello_cat().await;
    println!("hello, world!");
}

async fn hello_cat() {
    println!("hello, kitty!");
}
fn main() {
    let future = hello_world();
    block_on(future);
}
```

为`hello_cat()`添加上`.await`后，结果立刻大为不同:

```console
hello, kitty!
hello, world!
```

输出的顺序跟代码定义的顺序完全符合，因此，我们在上面代码中**使用同步的代码顺序实现了异步的执行效果**，非常简单、高效，而且很好理解，未来也绝对不会有回调地狱的发生。

总之，在`async fn`函数中使用`.await`可以等待另一个异步调用的完成。**但是与`block_on`不同，`.await`并不会阻塞当前的线程**，而是异步的等待`Future A`的完成，在等待的过程中，该线程还可以继续执行其它的`Future B`，最终实现了并发处理的效果。

#### 一个例子

考虑一个载歌载舞的例子，如果不用`.await`，我们可能会有如下实现：

```rust
use futures::executor::block_on;

struct Song {
    author: String,
    name: String,
}

async fn learn_song() -> Song {
    Song {
        author: "周杰伦".to_string(),
        name: String::from("《菊花台》"),
    }
}

async fn sing_song(song: Song) {
    println!(
        "给大家献上一首{}的{} ~ {}",
        song.author, song.name, "菊花残，满地伤~ ~"
    );
}

async fn dance() {
    println!("唱到情深处，身体不由自主的动了起来~ ~");
}

fn main() {
    let song = block_on(learn_song());
    block_on(sing_song(song));
    block_on(dance());
}
```

当然，以上代码运行结果无疑是正确的，但。。。它的性能何在？需要通过连续三次阻塞去等待三个任务的完成，一次只能做一件事，实际上我们完全可以载歌载舞啊:

```rust
use futures::executor::block_on;

struct Song {
    author: String,
    name: String,
}

async fn learn_song() -> Song {
    Song {
        author: "曲婉婷".to_string(),
        name: String::from("《我的歌声里》"),
    }
}

async fn sing_song(song: Song) {
    println!(
        "给大家献上一首{}的{} ~ {}",
        song.author, song.name, "你存在我深深的脑海里~ ~"
    );
}

async fn dance() {
    println!("唱到情深处，身体不由自主的动了起来~ ~");
}

async fn learn_and_sing() {
    // 这里使用`.await`来等待学歌的完成，但是并不会阻塞当前线程，该线程在学歌的任务`.await`后，完全可以去执行跳舞的任务
    let song = learn_song().await;

    // 唱歌必须要在学歌之后
    sing_song(song).await;
}

async fn async_main() {
    let f1 = learn_and_sing();
    let f2 = dance();

    // `join!`可以并发的处理和等待多个`Future`，若`learn_and_sing Future`被阻塞，那`dance Future`可以拿过线程的所有权继续执行。若`dance`也变成阻塞状态，那`learn_and_sing`又可以再次拿回线程所有权，继续执行。
    // 若两个都被阻塞，那么`async main`会变成阻塞状态，然后让出线程所有权，并将其交给`main`函数中的`block_on`执行器
    futures::join!(f1, f2);
}

fn main() {
    block_on(async_main());
}
```

上面代码中，学歌和唱歌具有明显的先后顺序，但是这两者都可以跟跳舞一同存在，也就是你可以在跳舞的时候学歌，也可以在跳舞的时候唱歌。如果上面代码不使用`.await`，而是使用`block_on(learn_song())`， 那在学歌时，当前线程就会阻塞，不再可以做其它任何事，包括跳舞。

因此`.await`对于实现异步编程至关重要，它允许我们在同一个线程内并发的运行多个任务，而不是一个一个先后完成。若大家看到这里还是不太明白，强烈建议回头再仔细看一遍，同时亲自上手修改代码试试效果。

至此，读者应该对 Rust 的`async/.await`异步编程有了一个清晰的初步印象，下面让我们一起来看看这背后的原理：`Future`和任务在底层如何被执行。