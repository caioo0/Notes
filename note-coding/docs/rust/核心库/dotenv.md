# dotenv ？ dotenvy?

在项目中，我们通常需要设置一些环境变量，用来保存一些凭证或其它数据，这时我们可以使用 dotenv 这个 crate。



## dotenv

**具体用法：**

1、首先在项目中添加dotenv这个依赖：

```rust
[dependencise]
dotenv = "0.15.0"
```

例如在下面这个项目中，需要设置数据库连接字符串和 Debug 等级这两个环境变量。

2、 在开发环境下，我们可以在项目根目录下创建 `.env` 这个文件：

```rust
LOG_LEVEL = debug
DB_URL=postgres://user:pwd@localhost:5432/mydb
```

 3、main.rs代码如下，也可以注释dotenv相关代码看看效果:

```rust
use std::env;
use dotenv::dotenv; //可注释比较

fn main() {

    dotenv().ok();  //可注释比较

    for (k,v) in env::vars() {
        println!("{}:{}",k,v);
    }

    println!("PATH:{}",env::var("PATH").unwrap());
    println!("DB:{}",env::var("PATH").unwrap());
    println!("LOG:{}",env::var("PATH").unwrap());
}
```

## dotenvy

**具体用法：**

1、首先在项目中添加dotenv这个依赖：

```rust
[dependencise]
dotenvy = "0.15"。
```

2、 main.rs代码如下：

```rust
use std::env;
use std::error::Error;

fn main() -> Result<(), Box<dyn Error>> {
    // Load environment variables from .env file.
    // Fails if .env file not found, not readable or invalid.
    dotenvy::dotenv()?;

    for (key, value) in env::vars() {
        println!("{key}: {value}");
    }

    Ok(())
}
```

