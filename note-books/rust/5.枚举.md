## 枚举与模式匹配

### 1. 枚举的定义

枚举允许我们列举所有可能的类型来定义一个类型

例如 IP 地址，目前只有 IPv4 和 IPv6 两种类型，我们可以定义这样的枚举类型并使用：

```
enum IpAddrKind {
    V4,
    V6,
}

fn main() {
    let four = IpAddrKind::V4;
    let six = IpAddrKind::V6;
    route(four);
    route(six);
    route(IpAddrKind::V6);
}

fn route(ip_type: IpAddrKind) {}
```

枚举的变体都位于标识符的命名空间下，使用两个冒号 `::` 进行分隔,这么设计的益处是现在 `IpAddrKind::V4` 和 `IpAddrKind::V6` 都是 `IpAddrKind` 类型的。

枚举类型是一种自定义的类型，因此它可以作为结构体里字段的类型，例子如下：

```
enum IpAddrKind {
    V4,
    V6,
}

struct IpAddr {
    kind: IpAddrKind,
    address: String,
}

fn main() {
    let home = IpAddr {
        kind: IpAddrKind::V4,
        address: String::from("192.168.2.1"),
    };
    let loopback = IpAddr {
    kind: IpAddrKind::V6,
    address: String::from("::1"),
	};
}

```

**将数据附加到枚举的成员中**

上述的枚举类型我们可以改为：

```
enum IpAddr {
    V4(String),
    V6(String),
}
```

优点是：不需要使用 struct，**每个成员可以拥有不同的类型以及相关联的数据**，例如

```
enum IpAddr {
    V4(u8, u8, u8, u8),
    V6(String),
}

fn main() {
    let home = IpAddrKind::V4(192, 168, 2, 1);
    let loopback = IpAddrKind::V6(String::from("::1"));
}
```

**标准库中的 IpAddr**

```
struct lpv4Addr {
    // --snip--
}
struct lpv6Addr {
    // --snip--
}
enum lpAddr {
    V4(lpv4Addr),
    V6(lpv6Addr),
}
```

**为枚举定义方法**

也使用 `impl` 这个关键字



这个枚举有四个含有不同类型的成员：

- `Quit` 没有关联任何数据。
- `Move` 包含一个匿名结构体。
- `Write` 包含单独一个 `String`。
- `ChangeColor` 包含三个 `i32`。

```
enum Message {
    Quit,
    Move {x: u32, y: u32},
    Write(String),
    ChangeColor(i32, i32, i32),
}

impl Message {
    fn call(&self) {}
}

fn main() {
    let q = Message::Quit;
    let m = Message::Move{x: 10, y: 12};
    let w = Message::Write(String::from("Hello"));
    let c = Message::ChangeColor(0, 255, 255);
    
    w.call();
}
```

### 2. Option 枚举

- 定义于标准库中

- 在 Prelude（预导入模块）中

- 描述了某个值可能存在（某种类型）或不存在的情况

  

**Rust 中没有 NULL**

其它语言中:

Null是一个值，它表示“没有值”
一个变量可以处于两种状态：空值（null）、非空
Null 引用：Billion Dollar Mistake
Null 的问题在于:当你尝试像使用非Null值那样使用Null值的时候，就会引起某种错误，但是 Null 的概念还是有用的：因某种原因而变为无效或缺失的值

Rust 中类似与 NULL 的概念的枚举：Option<T>

标准库中的定义：

```
enum Option<T> {
    Some(T),
    None,
}

```

它包含在预导入模块（Prelude）中，可以直接使用 `Option<T>`, `Some(T)`, `None`。例子如下：

```
fn main() {
    let some_num = Some(3);
    let some_string = Some("The String");
    let absent_num: Option<i32> = None;
}
```

其中 Some(3) 编译器可以推断出来 T 类型为 usize，而 None 的话编译器无法推断出来，因此需要显式指定 Option<i32>

这种设计比 NULL 好在哪？

因为 Option<T> 和 T 是不同的类型，不能将 Option<T> 当成 T 使用，例子如下：

```
fn test02() {
    let x: i8 = 5;
    let y: Option<i8> = Some(5);
    let sum = x + y;
}

```

这样会报错，提示 `cannot add Option<i8> to i8`，表示两者不是同一个类型，若想使用 `Option<T>` 中的 `T`，则必须将其手动转换为 `T`，这种设计方式可以避免代码中 NULL 值泛滥的情况。

### 3. match

**强大的控制流运算符 match**

允许一个值与一系列模式进行匹配，并执行匹配的模式对应的代码。模式可以是字面值、变量名、通配符…

```
enum Coin {
    Penny,
    Nickel,
    Dime,
    Quarter,
}

fn value_in_cents(coin: Coin) -> u8 {
    match coin {
        Coin::Penny => {
            println!("Penny!");
            1
        },
        Coin::Nickel => 5,
        Coin::Dime => 10,
        Coin::Quarter => 25,
    }
}

```

**绑定值的模式**

匹配的分支可以绑定到被匹配对象的部分值，因此可以从 enum 变体中提取值，例子如下：

```
#[derive(Debug)]
enum USState {
    California,
    Texas,
}

enum Coin {
    Penny,
    Nickel,
    Dime,
    Quarter(USState),
}

fn value_in_cents(coin: Coin) -> u8 {
    match coin {
        Coin::Penny => 1,
        Coin::Nickel => 5,
        Coin::Dime => 10,  
        Coin::Quarter(state) => {
            println!("State quarter from {:?}", state);
            25
        },

        /* Coin::Quarter(state) 也可以这样展开写 */
        Coin::Quarter(USState::Texas) => {
            println!("State quarter from {:?}", USState::Texas);
            25
        },
        Coin::Quarter(USState::California) => {
            println!("State quarter from {:?}", USState::California);
            25
        }
    }
}

fn test03() {
    let c = Coin::Quarter(USState::California);
    println!("{}", value_in_cents(c));
}

```

**匹配 Option**

```
fn test04() {
    let five = Some(5);
    let six = plus_one(five);
    let none = plus_one(None);
}

fn plus_one(x: Option<i32>) -> Option<i32> {
    match x {
        None => None,
        Some(i) => Some(i + 1)
    }
}

```

注意：match 匹配必须穷举所有的可能，可以使用 `_` 通配符替代其他没有列出的值

```
fn test05() {
    let x = 0u8;
    match x {
        1 => println!("one"),
        3 => println!("three"),
        5 => println!("five"),
        _ => ()
    }
}
```

### 4. if let

`if let` 是一种比 `match` 简单的控制流，他处理只关心一种匹配而忽略其他匹配的情况，它有更少的代码，更少的缩进，更少的模板代码，但是放弃了穷举的可能，可以把 `if let` 看作是 `match` 的语法糖。

`if let` 的格式如下：

```
if let pattern = value {
    //TODO
}

```

他也可以搭配 `else` 例子如下：

```
fn test06() {
    let v = 8u8;

    match v {
        3 => println!("Three!"),
        _ => ()
    }

    if let 3 = v {
        println!("Three")
    } else if let 5 = v {
        println!("Five!")
    } else {
        println!("Others!")
    }
}

```

