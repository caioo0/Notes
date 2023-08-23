# 【译】Rust中的Move、Copy和Clone

## **简介(Introduction)**

move 和 copy 是 Rust 中的基础概念。这对于来自 Ruby、Python 或 C#等垃圾回收语言的程序员来说可能是完全陌生的。这些术语在 C++中也确实存在，但它们在 Rust 中的含义却有微妙的不同。在本文中，我将解释对值进行 move、copy 和 clone 在 Rust 中到底意味着什么？让我们开始吧。

## **Move**

正如在**Memory safety in Rust - part 2[1]**所展示的，把一个变量赋值给另一个变量会把所有权(ownership)转移给受让者：

```rust
let v:Vec<i32> = Vec::new();
let v1 = v;//v1 is the new owner
```

在上面的例子中，`v`被move到`v1`。但是move `v`意味着什么？要想理解这个问题，我们需要先来看一下一个`Vec`在内存中是如何布局的：

![img](https://pic1.zhimg.com/80/v2-eaf3b413286ec2fb84826e0f4d8cc4cc_1440w.webp)

`Vec`不得不维护一个动态增长或收缩(shrinking)的缓冲区(buffer)。这个缓冲区被分配在堆上，包含`Vec`里真正的元素。此外，`Vec`还在栈上有一个小的对象。这个对象包含某些内务信息：一个指向堆上缓冲区的*指针(pointer)* ，缓存区的*容量(capacity)* 和*长度(length)* (比如，当前被填满的容量是多少)。

当变量`v`被move到`v1`时，栈上的对象被逐位拷贝(bitwise copy)：

![img](https://pic4.zhimg.com/80/v2-1c0caa3a4645c387c22cc182b5bb859b_1440w.webp)

> “ 在前面的例子中，本质上发生的是一个浅拷贝(shallow copy)。这与C++形成了鲜明的对比，当一个向量被赋值给另一个变量时，C++会进行深拷贝(deep copy)。

堆上的缓冲区保持不变。这确实是一个move：现在`v1`负责释放缓冲区，`v`不能接触这个缓冲区。

```rust
let v: Vec<i32> = Vec::new();
let v1 = v;
println!("v's length is {}", v.len());//error: borrow of moved value: `v`
```

这个所有权的改变很好，因为如果`v`和`v1`都被允许访问，那么就有两个栈上的对象指向相同的堆缓冲区。

## **简介(Introduction)**

move 和 copy 是 Rust 中的基础概念。这对于来自 Ruby、Python 或 C#等垃圾回收语言的程序员来说可能是完全陌生的。这些术语在 C++中也确实存在，但它们在 Rust 中的含义却有微妙的不同。在本文中，我将解释对值进行 move、copy 和 clone 在 Rust 中到底意味着什么？让我们开始吧。

## **Move**

正如在**Memory safety in Rust - part 2[1]**所展示的，把一个变量赋值给另一个变量会把所有权(ownership)转移给受让者：

```rust
let v:Vec<i32> = Vec::new();
let v1 = v;//v1 is the new owner
```

在上面的例子中，`v`被move到`v1`。但是move `v`意味着什么？要想理解这个问题，我们需要先来看一下一个`Vec`在内存中是如何布局的：

![vector memory layout](.\img\vector-layout.svg)

`Vec`不得不维护一个动态增长或收缩(shrinking)的缓冲区(buffer)。这个缓冲区被分配在堆上，包含`Vec`里真正的元素。此外，`Vec`还在栈上有一个小的对象。这个对象包含某些内务信息：一个指向堆上缓冲区的*指针(pointer)* ，缓存区的*容量(capacity)* 和*长度(length)* (比如，当前被填满的容量是多少)。

当变量`v`被move到`v1`时，栈上的对象被逐位拷贝(bitwise copy)：

![what happens when a vector is moved](.\img\vector-layout-moved.svg)

> “ 在前面的例子中，本质上发生的是一个浅拷贝(shallow copy)。这与C++形成了鲜明的对比，当一个向量被赋值给另一个变量时，C++会进行深拷贝(deep copy)。

堆上的缓冲区保持不变。**这确实是一个move：现在`v1`负责释放缓冲区，`v`不能接触这个缓冲区**。

```rust
#[allow(unused_variables)]
fn main() {

	let v: Vec<i32> = Vec::new();
	let v1 = v;
	println!("v's length is {}", v.len());
	//println!("v1's length is {}", v1.len());
}
```

报错：

```rust
error[E0382]: borrow of moved value: `v`
 --> hello.rs:6:31
  |
4 |     let v: Vec<i32> = Vec::new();
  |         - move occurs because `v` has type `Vec<i32>`, which does not implement the `Copy` trait
5 |     let v1 = v;
  |              - value moved here
6 |     println!("v's length is {}", v.len());
  |                                  ^^^^^^^ value borrowed here after move
  |
help: consider cloning the value if the performance cost is acceptable
  |
5 |     let v1 = v.clone();
  |               ++++++++

error: aborting due to previous error
```

这个所有权的改变很好，因为如果`v`和`v1`都被允许访问，那么就有两个栈上的对象指向相同的堆缓冲区。

![if two vectors  shared a buffer](.\img\vector-layout-shared-buffer.svg)

这种情况，应该由哪个对象释放缓冲区呢？因为这是不清晰的，所以Rust从根本上避免了这种情况的出现。