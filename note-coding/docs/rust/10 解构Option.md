# 解构 Option

> 资料：https://blog.csdn.net/konquerx/category_10933648.html

在枚举那章，提到过 `Option` 枚举，它用来解决 Rust 中变量是否有值的问题，定义如下：

```rust
enum Option<T> {
    Some(T),
    None,
}
```

简单解释就是：**一个变量要么有值：`Some(T)`, 要么为空：`None`**。

那么现在的问题就是该如何去使用这个 `Option` 枚举类型，根据我们上一节的经验，可以通过 `match` 来实现。

```
因为 Option，Some，None 都包含在 prelude 中，因此你可以直接通过名称来使用它们，而无需以 Option::Some 这种形式去使用，总之，千万不要因为调用路径变短了，就忘记 Some 和 None 也是 Option 底下的枚举成员！
```

## 匹配 `Option`

使用 `Option<T>`，是为了从 `Some` 中取出其内部的 `T` 值以及处理没有值的情况，为了演示这一点，下面一起来编写一个函数，它获取一个 `Option<i32>`，如果其中含有一个值，将其加一；如果其中没有值，则函数返回 `None` 值：

```rust 
#[allow(dead_code)]

fn plus_one(x:Option<i32>) -> Option<i32>{
	match x {
		None => None,
		Some(i) => Some(i+1)
	}
}
fn main() {
	let five = Some(5);
	let six = plus_one(five);
	let none = plus_one(None);

	println!("{:?}",six);
	dbg!(none);
    
}
```

