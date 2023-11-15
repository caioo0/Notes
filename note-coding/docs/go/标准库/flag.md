# flag 使用

> 参考：https://juejin.cn/post/7098245145744965663

```go
package main

import (
	"flag"
	"fmt"
)

var (
	host     string
	dbName   string
	port     int
	user     string
	password string
)

func main() {

	flag.StringVar(&host, "host", "", "数据库地址")
	flag.StringVar(&dbName, "db_name", "", "数据库名称")
	flag.StringVar(&user, "user", "", "数据库用户")
	flag.StringVar(&password, "password", "", "数据库密码")
	flag.IntVar(&port, "port", 3306, "数据库端口")

	flag.Parse()

	fmt.Printf("数据库地址:%s\n", host)
	fmt.Printf("数据库名称:%s\n", dbName)
	fmt.Printf("数据库用户:%s\n", user)
	fmt.Printf("数据库密码:%s\n", password)
	fmt.Printf("数据库端口:%d\n", port)

}
```

```shell
go run main.go -host=localhost -user=test -password=123456 -db_name=test -port=3306
```

```go
package main

import (
	"flag"
	"fmt"
)

func main() {

	host := flag.String("host", "", "数据库地址")
	dbName := flag.String("db_name", "", "数据库名称")
	user := flag.String("user", "", "数据库用户")
	password := flag.String("password", "", "数据库密码")
	port := flag.Int("port", 3306, "数据库端口")

	flag.Parse()

	fmt.Printf("数据库地址:%s\n", *host)
	fmt.Printf("数据库名称:%s\n", *dbName)
	fmt.Printf("数据库用户:%s\n", *user)
	fmt.Printf("数据库密码:%s\n", *password)
	fmt.Printf("数据库端口:%d\n", *port)
}
```

```go
go run main.go --help
Usage of main:
  -db_name string
        数据库名称
  -host string
        数据库地址
  -password string
        数据库密码
  -port int
        数据库端口 (default 3306)
  -user string
        数据库用户
```

`Duration`类型的参数接收可以被`time.ParseDuration()`解析的参数。



