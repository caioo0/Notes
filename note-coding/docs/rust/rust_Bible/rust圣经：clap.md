# Rust Crate 使用：clap

## **Clap**

[Github](https://link.zhihu.com/?target=https%3A//github.com/clap-rs/clap)
[Crates.io](https://link.zhihu.com/?target=https%3A//crates.io/crates/clap)

## **介绍**

`clap`是一个简单易用，功能强大的命令行参数解析库。

### 使用

`clap` 允许多中方式指定我们的命令行。支持常规的 Rust 方法调用、宏或者YAML配置。

## **常规调用模式**

首先介绍的是Rust代码控制命令行。

```
extern crate clap;

use clap::{Arg,App};

fn main() {
	let matches = App::new("MayApp")
		.version("0.1")
		.author("kayryu")
		.about("Learn use Rust Crate!")
		.arg(Arg::with_name("verbose")
			.short("v")
			.multiple(true)
			.help("verbosity level"))
        .args_from_usage("-p,--path=[FILE] 'Target file want to change'")
        .get_matches();
        
     if let Some(f) = matches.value_of("path") {
     	println!("path:{}",f);
     }
}
```

