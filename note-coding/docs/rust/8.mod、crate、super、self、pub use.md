# Rust:mod、crate、super、self、pub use等模块系统用法梳理

一、packages、crates、modules

packages: 通过cargo new 创建；
crates: 通过cargo new --lib 创建。有根包和子包。即一个根包下可以包含多个子包。
modules: 通过关键字mod加模块定义

二、各种用法

src下有同个级：兄弟、父、子三个层级。

1、mod

```
往往是引入与当前文件同级的文件夹下（兄弟模块下）的文件。
```

2、crate

```
代表引用当前文件同级的文件。为同级文件时，意义和self相同。但如果是同级文件夹，不能混用。

```

3、super

```
super:代表当前文件的上一级目录（父模块） 。super后面可以直接接函数。也可以接“*”，表示所有函数。

```

4、self

```
见crate
```

5、pub use

```
Example	Explanation
mod m {}	Define a module, BK EX REF get definition from inside {}. ↓
mod m;	Define a module, get definition from m.rs or m/mod.rs. ↓
a::b	Namespace path EX REF to element b within a (mod, enum, ...).
     ::b	Search b relative to crate root. 🗑️
     crate::b	Search b relative to crate root. '18
     self::b	Search b relative to current module.
     super::b	Search b relative to parent module.
use a::b;	Use EX REF b directly in this scope without requiring a anymore.
use a::{b, c};	Same, but bring b and c into scope.
use a::b as x;	Bring b into scope but name x, like use std::error::Error as E.
use a::b as _;	Bring b anonymously into scope, useful for traits with conflicting names.
use a::*;	Bring everything from a into scope.
pub use a::b;	Bring a::b into scope and reexport from here.

```

三、桥

在src下，往往有一个子目录，比如名字叫core. 里面还有两个文件，read.rs,write.rs.此时，需要有一个文件把这两个文件串起来。
此时，可以在core目录同级，建一个core.rs文件，把core目录下的两个文件串起来，对外可见。
我称这种与目录相同的rs文件为桥（个人定义，不规范）文件。

```
pub mod a;
pub mod c;
pub use a::*; //不能省
pub use c::*;//不能省
```

./src/main.rs:

```
pub mod src_a;
pub mod src_b;
pub use self::src_a::a_echo;
pub sue self::src_b::b_echo;

fn main() {
	println!("Hello,world!");
	src_a::a_echo();
	src_b::b_echo();
}
```

![image-20230625160744342](.\img\image-20230625160744342.png)

（1）a.rs

```
pub fn a_echo(){
    println!("a_echo!");
}
```

（2）c.rs

注意，crate不能用self替换crate。

```
use crate::src_a::a::*;
pub fn c_echo(){
    println!("c_echo!");
    a_echo();
}
```

（3）b.rs

```
use crate::src_a::a_echo;
//如何引入a.rs或c.rs中的函数
pub fn b_echo(){
    println!("b_echo! => call a()!");
    a_echo();

}
```

（4）src_a.rs

```
pub mod a;
pub mod c;
pub use a::*;
pub use c::*;

```

（5）src_b.rs

```
pub mod b;
pub use b::*;


```

(6)main.rs
crate和self可以互相替代。

```
pub mod src_a;
pub mod src_b;
pub use self::src_a::*;
pub use crate::src_b::*;

fn main() {
    println!("Hello, world!");
    src_a::a_echo();
    src_b::b_echo();
}

```

2、解决的问题：

(1) c.rs =>调用a.rs 中函数
(2) b.rs =>调用a.rs 中函数
(3)main.rs =>调用a.rs; 调用c.rs中函数；必须要使用“桥”。

3、src_a.rs和src_b.rs相当于分别是a.rs和c.rs与b.rs的代理。



## 参考资料

1. https://blog.csdn.net/wowotuo/article/details/107591501