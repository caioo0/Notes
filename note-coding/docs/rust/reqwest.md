#  reqwest库

reqwest 是一个简单而强大的 RUST HTTP 客户端，用于浏览器异步 HTTP 请求。支持 xmlHttpRequest, JSONP, CORS, 和 CommonJS 约束。

### 一、安装与引用

1. 在项目的 Cargo.toml 中添加依赖。reqwest 的 [async](https://so.csdn.net/so/search?q=async&spm=1001.2101.3001.7020) 使用的是 Tokio 的，所以要同时加入 Tokio 的依赖。

```
[dependencies]
reqwest = { version = "0.11", features = ["json"] }
tokio = { version = "1", features = ["full"] }
```

2. 编写GET代码

```
use std::collections::HashMap;


async fn get() -> Result<HashMap<String, String>, reqwest::Error>{
    Ok(reqwest::get("https://httpbin.org/ip").await?.json::<HashMap<String, String>>().await?)
}

#[tokio::main]
async fn main() {
    if let Ok(resp) = get().await {
        println!("{:#?}", resp);
    }
}


```

返回当前请求浏览器的ip地址，也就是你当前的ip地址。



如果是单个请求，可以使用get方法,如果你还要进行其他的多个请求，最好创建个`Client`进行复用。



### 二、POST请求

1、POST请求，用到了serde_json，所以在 Cargo.toml 中要加入 serde_json。

```
[dependencies]
reqwest = { version = "0.10", features = ["json"] }
tokio = { version = "0.2", features = ["full"] }
serde_json = "1.0"

```

2、编写POST代码

```
use std::collections::HashMap;
use reqwest::header::HeaderMap;
use serde_json::value::Value;

async fn post() -> Result<HashMap<String, Value>, reqwest::Error>{
    // post 请求要创建client
    let client = reqwest::Client::new();

    // 组装header
    let mut headers = HeaderMap::new();
    headers.insert("Content-Type", "application/json".parse().unwrap());

    // 组装要提交的数据
    let mut data = HashMap::new();
    data.insert("user", "tangjz");
    data.insert("password", "dev-tang.com");

    // 发起post请求并返回
    Ok(client.post("https://httpbin.org/post").headers(headers).json(&data).send().await?.json::<HashMap<String, Value>>().await?)
}

#[tokio::main]
async fn main() {
    if let Ok(res) = post().await {
        println!("{:#?}", res);
    }
}
```

POST 请求比 GET 稍微复杂那么一点点。先看 use 引用，比 GET 请求多了两个 use，分别是 reqwest::header::HeaderMap、serde_json::value::Value，后面简称HeaderMap、Value。

### 三、完整代码

Cargo.toml

```
[dependencies]
reqwest = { version = "0.10", features = ["json"] }
tokio = { version = "0.2", features = ["full"] }
serde_json = "1.0"

```

main.rs

```
use std::collections::HashMap;
use reqwest::header::HeaderMap;
use serde_json::value::Value;


async fn get() -> Result<HashMap<String, String>, reqwest::Error>{
    Ok(reqwest::get("https://httpbin.org/ip").await?.json::<HashMap<String, String>>().await?)
}

async fn post() -> Result<HashMap<String, Value>, reqwest::Error>{
    // post 请求要创建client
    let client = reqwest::Client::new();

    // 组装header
    let mut headers = HeaderMap::new();
    headers.insert("Content-Type", "application/json".parse().unwrap());

    // 组装要提交的数据
    let mut data = HashMap::new();
    data.insert("user", "zhangsan");
    data.insert("password", "https://docs.rs/serde_json/1.0.59/serde_json/");

    // 发起post请求并返回
    Ok(client.post("https://httpbin.org/post").headers(headers).json(&data).send().await?.json::<HashMap<String, Value>>().await?)
}

#[tokio::main]
async fn main() {
    if let Ok(resp) = get().await {
        println!("{:#?}", resp);
    }

    if let Ok(res) = post().await {
        println!("{:#?}", res);
    }
}

```

### 四、HTML网页转markdown

这个程序的需求很简单，通过 HTTP 请求 Rust 官网首页，然后把获得的 HTML 转换成Markdown 保存起来。

1. Cargo.toml 

   阻塞客户端将阻塞要当前线程的执行，而不是直接返回继续执行。但是reqwest::blocking中的功能不能在异步运行时内执行，否则在尝试阻塞时会死机。

   ```
   [dependencies]
   reqwest = {version="0.11",features = ["blocking"]}
   html2md = "0.2"
   ```

2. main.rs

   ```
   use std::fs;
   
   fn main() {
       let url = "https://www.rust-lang.org/";
       let output ="rust.md";
   
       println!("Fetching url:{}",url);
       let body = reqwest::blocking::get(url).unwrap().text().unwrap();
       
       println!("Converting html to markdown ...");
       let md = html2md::parse_html(&body);
       fs::write(output,md.as_bytes()).unwrap();
       println!("Converted markdown has been saved in {}.",output);
   }
   
   ```

   

### 五、参考资料：

1. https://zhuanlan.zhihu.com/p/572150411