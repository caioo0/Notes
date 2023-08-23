# actix-web

## 创建项目

首先，创建一个新的二进制 Cargo 项目，并切换到新目录：

```
cargo new hello-actix
cd hello-actix
```

通过向 `Cargo.toml` 文件添加以下内容，将 `actix-web` 添加为项目的依赖项。

```
[dependencise]
actix-web = "4.3.1"
```

向`main.rs`问件添加一下内容，并且执行`cargo run`:

```
use actix_web::{get, post, web, App, HttpResponse, HttpServer, Responder};

#[get("/")]
async fn hello() -> impl Responder {
    HttpResponse::Ok().body("Hello world!")
}

#[post("/echo")]
async fn echo(req_body: String) -> impl Responder {
    HttpResponse::Ok().body(req_body+"post")
}

async fn manual_hello() -> impl Responder {
    HttpResponse::Ok().body("Hey hey!")
}
#[actix_web::main]
async fn main() -> std::io::Result<()> {
    HttpServer::new(|| {
        App::new()
            .service(hello)
            .service(echo)
            .route("/hey", web::get().to(manual_hello))
    })
    .bind("127.0.0.1:8080")?
    .run()
    .await
}
```

运行通过后，访问 `http://localhost:8080/`，或者你自定义的任何路由，以查看运行结果。git完整源码:[0.1.0]()