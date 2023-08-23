## 结构体

>  教程地址：https://www.rustwiki.org.cn/zh-CN/book/ch05-02-example-structs.html

## 一、结构体的使用

### 1. 定义和实例化 struct

例子：

```rust
struct User {
    username: String,
    email: String,
    sign_in_count: usize,
    active: bool,
}

```

注意：每个字段后面用逗号隔开，最后一个字段后面可以没有逗号。

实例化例子：

```
let user1 = User {
        email: String::from("cherry@gmail.com"),
        username: String::from("cherry"),
        active: true,
        sign_in_count: 244,
    };
```

先创建 struct 实例，然后为每个字段指定值，无需按照声明的顺序指定。

但是注意不能少指定字段。

用点标记法取得结构体中的字段值，一旦 struct 的实例是可变的，那么实例中的所有字段都是可变的，不会同时既存在可变的字段又存在不可变的字段。

**结构体作为函数的返回值**

```
fn struct_build() -> User {
    User {
        email: String::from("cherry@gmail.com"),
        username: String::from("cherry"),
        active: true,
        sign_in_count: 244,
    }
}
```

**字段初始化简写**

当字段名与字段值对应变量相同的时候，就可以使用字段初始化简写的方式：

```
fn struct_build(email: String, username: String) -> User {
    User {
        email,
        username,
        active: true,
        sign_in_count: 244,
    }
}
```

**struct 更新语法**

当想基于某个 struct 实例创建一个新的实例时（新的实例中某些字段可能和原先相同，某些不同），若不使用 struct 更新语法，则是这样写：

```
let user2 = User {
        email: String::from("paul@nba.cn"),
        username: String::from("Chris Paul"),
        active: user1.active,
        sign_in_count: user1.sign_in_count,
    };

```

而使用 struct 更新语法，则是这样写：

```
let user3 = User {
        email: String::from("paul@nba.cn"),
        username: String::from("Chris Paul"),
        ..user1
    };
```

用 `..user1` 表示该实例中未赋值的其他字段和实例 `user1` 中的值一致。

**uple Struct**

可以定义类似 Tuple 的 Struct，叫做 Tuple Struct。Tuple struct 整体有个名，但里面的元素没有名

适用：想给整个 tuple 起名，并让它不同于其它 tuple，而且又不需要给每个元素起名

```
struct Color(i32, i32, i32);
struct Point(i32, i32, i32);


let black(0, 0, 0) = Color;
let origin = Point(0, 0, 0);

```

black 和 origin 是不同的类型，是不同 tuple struct 的实例

**Unit-Like Struct(没有任何字段)**

可以定义没有任何字段的 struct，叫做 Unit-Like struct，因为与 () 和单元类型类似，适用于需要在某个类型上实现某个trait，但是在里面又没有想要存储的数据

**struct 数据所有权**

再来看这个例子：

```
struct User {
    username: String,
    email: String,
    sign_in_count: usize,
    active: bool,
}
```

这里的字段使用了 String 而不是 &str，原因如下：

该 struct 实例拥有其所有的数据
只要 struct 实例是有效的，那么里面的字段数据也是有效的 struct 里也可以存放引用，但这需要使用生命周期（以后讲）
若字段为 &str，当其有效作用域小于该实例的作用域，该字段被清理时，实例未清理，访问该字段属于悬垂引用（类似野指针）
生命周期保证只要 struct 实例是有效的，那么里面的引用也是有效的
如果 struct 里面存储引用，而不使用生命周期，就会报错

### 2. struct 例子

一个简单的例子：计算长方形的面积

```
fn main() {
    let width1 = 30;
    let height1 = 50;

    println!(
        "The area of the rectangle is {} square pixels.",
        area(width1, height1)
    );
}

fn area(width: u32, height: u32) -> u32 {
    width * height
}
```

上面这个例子很简单，但是长方形的长和宽没有联系起来，width 和 length 是两个分离的没有逻辑联系的变量，我们考虑用元组将其联系起来：

**使用元组重构**

```
fn main() {
    
    let rect1 = (30,50);

    println!( "The area of the rectangle is {} square pixels.",area(rect1));
}


fn area(dimensions: (u32,u32)) -> u32 {
    dimensions.0 * dimensions.1
}
```

**使用结构体重构：赋予更多意义**

```
struct Rectangle{
    width: u32,
    height: u32,
}

fn main() {
    let rect1 = Rectangle {
        width:30,
        height:50,
    };
    println!( "The area of the rectangle is {} square pixels.",area(&rect1));
}

fn area(dimensions:&Rectangle) -> u32 {
    dimensions.width * dimensions.height
}

```

**通过派生 trait 增加实用功能**

我们在结构体前添加 `#[derive(Debug)]`，使得该结构体派生与 `Debug` 这个 trait。

```
#[derive(Debug)]
struct Rectangle {
    width: u32,
    height: u32,
}
fn main() {
    let rect1 = Rectangle {
        width: 30,
        height: 50,
    };
    println!("rect1 is {:?}", rect1);
}
```

可以试一试，若在输出格式中间加入一个 `#`，结构体输出：`println!("{:?}", rect1);`

## 3. struct 方法

方法和函数类似: fn关键字、名称、参数、返回值

方法与函数不同之处:

方法是在 struct(或 enum、trait 对象）的上下文中定义
第一个参数是 self，表示方法被调用的 struct 实例
上一节我们定义了计算长方形面积的函数，但是该函数只能计算长方形的函数，无法计算其他形状的面积，因此我们希望将函数与长方形这一结构体关联起来，例子如下：

```
#[derive(Debug)]

struct Rectangle {
	width:u32,
	height:u32,
}
#[allow(dead_code)]
impl Rectangle{
	fn area(&Rectangle) -> u32 {
		Rectangle.width * Rectangle.height 
	}
}
fn main (){
	let rect1 = Rectangle{
		width:30,
		height:50,
	};

	println!("the area of the rectangele is {} square pixels.",rect1.area())
}
```

可以将 `area(self:&Rectangle)` 可以替换为`fn area(&self) ` 

在impl块里定义方法，方法的第一个参数可以是 `&self`，也可以**获得其所有权**或**可变借用**，和其他参数一样。这样写可以有更良好的代码组织。

**方法调用的运算符**

C/C++ 中 object->something() 和 (*object).something() 一样，但是 Rust 没有 → 运算符
Rust 会自动引用或解引用一在调用方法时就会发生这种行为
在调用方法时，Rust 根据情况自动添加 &、&mut 或 *，以便 object 可以匹配方法的签名
下面这两种写法效果相同

- p1.distance(&p2);
- (&p1).distance(&p2);
  

**方法参数**

```
impl Rectangle {
    fn area(&self) -> u32 {
        self.length * self.width
    }

    fn can_hold(&self, other: &Rectangle) -> bool {
        self.length > other.length && self.width > other.width 
    }
}
```

**关联函数**

可以在 impl 块里定义不把 self 作为第一个参数的函数，它们叫关联函数（不叫方法）

例如：`String::from()`

关联函数通常用于构造器，例子如下：

```
struct Rectangle {
    width: u32,
    length: u32,
}


impl Rectangle {
    fn square(size: u32) -> Rectangle {
        Rectangle {
            width: size,
            length: size,
        }
    }
}

fn main() {
    let s = Rectangle::square(20);
}

```

`::` 符号

- 关联函数
- 模块创建的命名空间