```
#![allow(unused)]
#[derive(Debug)]
enum SpreadsheetCell {
    Int(i32),
    Float(f64),
    Text(String),
}

fn main() {
   let row = vec![
    SpreadsheetCell::Int(3),
    SpreadsheetCell::Text(String::from("blue")),
    SpreadsheetCell::Float(10.12),
    ];
    println!("The first element is: {:?}", row);
  
}
```

## trait特征

类型实现特征

首先来为 `Post` 和 `Weibo` 实现 `Summary` 特征：

```

#![allow(unused)]
fn main() {
pub trait Summary {
    fn summarize(&self) -> String;
}
pub struct Post {
    pub title: String, // 标题
    pub author: String, // 作者
    pub content: String, // 内容
}

impl Summary for Post {
    fn summarize(&self) -> String {
        format!("文章{}, 作者是{}", self.title, self.author)
    }
}

pub struct Weibo {
    pub username: String,
    pub content: String
}

impl Summary for Weibo {
    fn summarize(&self) -> String {
        format!("{}发表了微博{}", self.username, self.content)
    }
}
}
fn main() {
    let post = Post{title: "Rust语言简介".to_string(),author: "choi".to_string(), content: "Rust棒极了!".to_string()};
    let weibo = Weibo{username: "sunface".to_string(),content: "好像微博没Tweet好用".to_string()};

    println!("{}",post.summarize());
    println!("{}",weibo.summarize());
}
```

结果：

```
文章Rust语言简介, 作者是Sunface
sunface发表了微博好像微博没Tweet好用
```

特征定义与实现的位置(孤儿规则)

```
pub trait Summary {
    fn summarize(&self) -> String {
        String::from("(Read more...)")
    }
}
impl Summary for Post {}

impl Summary for Weibo {
    fn summarize(&self) -> String {
        format!("{}发表了微博{}", self.username, self.content)
    }
}
```

完整代码：

```
#![allow(unused)]

pub trait Summary {
    fn summarize(&self) -> String {
        String::from("(Read more...)")
    }
}
pub struct Post {
    pub title: String, // 标题
    pub author: String, // 作者
    pub content: String, // 内容
}

impl Summary for Post {
}

pub struct Weibo {
    pub username: String,
    pub content: String
}

impl Summary for Weibo {
    fn summarize(&self) -> String {
        format!("{}发表了微博{}", self.username, self.content)
    }
}


fn main() {
    let post = Post{title: "Rust语言简介".to_string(),author: "Sunface".to_string(), content: "Rust棒极了!".to_string()};
    let weibo = Weibo{username: "sunface".to_string(),content: "好像微博没Tweet好用".to_string()};

    println!("{}",post.summarize());
    println!("{}",weibo.summarize());
}
```

```
#![allow(unused)]

pub trait Summary {
    fn summarize_author(&self) -> String;

    fn summarize(&self) -> String {
        format!("(Read more from {}...)", self.summarize_author())
    }
}

pub struct Post {
    pub title: String, // 标题
    pub author: String, // 作者
    pub content: String, // 内容
}

impl Summary for Post {
     fn summarize_author(&self) -> String {
        format!("@{}", self.author)
    }
}

pub struct Weibo {
    pub username: String,
    pub content: String
}

impl Summary for Weibo {
     fn summarize_author(&self) -> String {
        format!("@{}", self.username)
    }
}


fn main() {
    let post = Post{title: "Rust语言简介".to_string(),author: "Sunface".to_string(), content: "Rust棒极了!".to_string()};
    let weibo = Weibo{username: "sunface".to_string(),content: "好像微博没Tweet好用".to_string()};

    println!("{}",post.summarize());
    println!("{}",weibo.summarize());
}
```

## [使用特征作为函数参数](https://course.rs/basic/trait/trait.html#使用特征作为函数参数)

之前提到过，特征如果仅仅是用来实现方法，那真的有些大材小用，现在我们来讲下，真正可以让特征大放光彩的地方。

现在，先定义一个函数，使用特征作为函数参数：

```
pub fn notify(item: &impl Summary) {
    println!("Breaking news! {}", item.summarize());
}
```



### `Add` ：

```
use std::ops::Add;

#[derive(Debug, Copy, Clone, PartialEq)]
struct Point {
    x:i32,
    y:i32,
}

impl Add for Point {
    type Output = Self;

    fn add(self, other:Self) -> Self {
        Self {
            x:self.x + other.x,
            y:self.y + other.y,
        }
    }
}

assert_eq!(Point { x:1, y:0 } + Point { x:2, y:3 },
           Point { x:3, y:3 });
```



### 使用泛型实现`Add`

这是使用泛型实现 `Add` 特征的相同 `Point` 结构的示例。

```
use std::ops::Add;

#[derive(Debug, Copy, Clone, PartialEq)]
struct Point<T> {
    x:T,
    y:T,
}

// Notice that the implementation uses the associated type `Output`.
impl<T:Add<Output = T>> Add for Point<T> {
    type Output = Self;

    fn add(self, other:Self) -> Self::Output {
        Self {
            x:self.x + other.x,
            y:self.y + other.y,
        }
    }
}

assert_eq!(Point { x:1, y:0 } + Point { x:2, y:3 },
           Point { x:3, y:3 });
```

