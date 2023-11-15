# Go学习：Goroutines和channels

练习1 ：

```go
// test.go 

package main

import (
	"fmt"
	"time"
)

func main() {
	go spinner(100 * time.Millisecond)

	const n = 45

	time.Sleep(10 * time.Second)

	fibN := fib(n) //

	fmt.Printf("\rFibonacci（%的） = %d \b", n, fibN)
}

func spinner(delay time.Duration) {
	for {
		for _, r := range `-\|/` {
			fmt.Printf("\r%c", r)
			fmt.Printf("\r%c", r)
			time.Sleep(delay)
		}
	}
}

func fib(x int) int {
	if x < 2 {
		return x
	}
	return fib(x-1) + fib(x-2)

}

// 运行: go run test.go 
```

练习2：

```go
// test.go 

package main

import (
	"io"
	"log"
	"net"
	"time"
)

func main() {
	listener, err := net.Listen("tcp", "localhost:8000")
	if err != nil {
		log.Fatal(err)
	}
	for {
		conn, err := listener.Accept()
		if err != nil {
			log.Print(err)
			continue
		}
		handleConn(conn)
	}

}

func handleConn(c net.Conn) {
	defer c.Close() // 延迟执行

	for {
		_, err := io.WriteString(c, time.Now().Format("15:04:05\n"))
		if err != nil {
			return
		}
		time.Sleep(1 * time.Second)
	}

}

/**
1. 安装netcat   https://eternallybored.org/misc/netcat/
2. cmd1运行：step1 > go build test.go    step2 > ./test &
3. cmd2运行： nc localhost 8000
*/

```

