# GO学习：并发编程

> https://juejin.cn/post/7225230646246981692

## 什么是 Golang 通道？

通道：一种高效、安全、灵活的并发机制，用于在并发环境下实现数据的同步和传递。

通道提供了一各线程安全的队列，只允许一个goroutine进行读操作、另一个goroutine进行写操作。通过这种方式，通道可以有效地解决并发编程中的竞态条件、锁问题等常见问题。

>  竞态条件：是指多个进程（线程、协程）读写某些共享数据，而最后的结果取决于进程运行的准确时序。也就是当多个进程（线程、协程）竞争同一资源时，如果对资源的访问顺序敏感，就称存在竞态条件。

通道有两种类型：**有缓冲通道和无缓冲通道**。

在通道创建时，可以指定通道的容量，即通道缓冲区的大小，如果不指定则默认为无缓冲通道。

### Golang 通道的基本语言

Golang通道的基本语法非常简单，使用`make`函数来创建一个通道：

```go
ch :=make(chan int)  //无缓冲通道
```

这行代码创建了一个名为ch的通道，通道的数据类型为int。通道的读写操作可以使用箭头$<- , <-$ 表示从通道中读取数据，$->$ 表示向通道中写入数据。例如：

```go
ch := make(chan int)    
ch <- 1			// 向通道中写入数据
x  := <- ch     // 从通道中
```

- 通道的缓冲区可以存储一定量的数据，当缓冲区满时，向通道写入数据将阻塞。
- 当通道缓冲区为空时，从通道读取数据将阻塞。
- 缓冲区大小为 0 的通道称为无缓冲通道。无缓冲通道的发送和接收操作都是阻塞的，发送者和接收者准备好接收才能进行发送操作，这种机制确保了通道的同步性，即在通道操作前后，发送者和接收者都会被阻塞，直到对方做好准备。

### 有缓冲通道

```go
 ch := make(chan int, 3)
```

创建了一个名为 ch 的通道，通道的数据类型为 int，通道缓冲区的大小为 3.

### 无缓冲通道

```go
 ch := make(chan int)
```

创建了一个名为ch的通道，通道的数据类型为 int，通道缓冲区的大小为 0。

## Golang 通道的超时和计时器

在并发编程中，需要对通道进行超时和计时操作。Golang 中提供了 time 包来实现**超时和计时器**。

### 超时机制

在 Golang 中，可以使用 `select` 语句和 `time.After` 函数来实现通道的超时操作。例如：

```go
select {
	case data := <-ch:
		fmt.Println(data)
	case <-time.After(time.Second):
		fmt.Println("timeout")
}
```

这段代码中，select 语句监听了通道 ch 和 time.After(time.Second) 两个信道，如果 ch 中有数据可读，则读取并输出数据；如果等待 1 秒钟后仍然没有数据，则超时并输出 timeout。

### 计时器机制

Golang 中提供了 time 包来实现计时器机制。可以使用 time.NewTimer(duration) 函数创建一个计时器，计时器会在 duration 时间后触发一个定时事件。例如：

```go
 timer := time.NewTimer(time.Second * 2)
 <-timer.C
 fmt.Println("Timer expired")

```

创建了一个计时器，设定时间为 2 秒钟，当计时器到达 2 秒钟时，会向 timer.C 信道中发送一个定时事件，程序通过 <-timer.C 语句等待定时事件的到来，并在接收到定时事件后输出 “Timer expired”。

## Golang 通道的传递

在 Golang 中，通道是一种引用类型，可以像普通变量一样进行传递。例如：

```go
 func worker(ch chan int) {
     data := <-ch
     fmt.Println(data)
 }
 ​
 func main() {
     ch := make(chan int)
     go worker(ch)
     ch <- 1
     time.Sleep(time.Second)
 }

```

## 单向通道

在 Golang 中，可以通过使用单向通道来限制通道的读写操作。单向通道只允许读或写操作，不允许同时进行读写操作。例如：

```go
func producer(ch chan<- int){
	ch <- 1
}

func consumer(ch <-chan int){
	data :=<-ch
	fmt.Println(data)
}
func main(){
	ch := make(chan int)
	go producer(ch)
	go consumer(ch)
	time.Sleep(time.Second)
}
```

这段代码中，produce r函数和 consumer 函数分别用于向通道中写入数据和从通道中读取数据。在函数的参数中，使用了单向通道限制参数的读写操作。在 main 函数中，创建了一个名为 ch 的通道，并启动了一个 producer goroutine 和一个 consumer goroutine，producer 向 ch 通道中写入数据1，consumer 从 ch 通道中读取数据并输出到控制台中。

## 关闭通道

在 Golang 中，可以使用 close 函数来关闭通道。关闭通道后，通道的读写操作将会失败，读取通道将会得到零值，写入通道将会导致 panic 异常。例如：

```go
package main

import (
	"fmt"
)

func main() {
	ch := make(chan int)

	go func() {
		for i := 0; i < 5; i++ {
			ch <- i
		}
		close(ch)
	}()

	for data := range ch {
		fmt.Println(data)
	}
}
```

这段代码中，创建了一个名为 ch 的通道，并在一个 goroutine 中向通道中写入数据 0 到 4，并通过 close 函数关闭通道。在主 goroutine 中，通过 for...range 语句循环读取通道中的数据，并输出到控制台中，当通道被关闭时，for...range 语句会自动退出循环。

在关闭通道后，仍然可以从通道中读取已经存在的数据，例如：

```go
package main

import (
	"fmt"
)

func main() {
	ch := make(chan int)

	go func() {
		for i := 0; i < 5; i++ {
			ch <- i
		}
		close(ch)
	}()

	for {
		data, ok := <-ch
		if !ok {
			break
		}
		fmt.Println(data)
	}
}

```

这段代码中，通过循环读取通道中的数据，并判断通道是否已经被关闭。当通道被关闭时，读取操作将会失败，ok 的值将会变为 false，从而退出循环。

## 常见的应用场景

通道是 Golang 并发编程中的重要组成部分，其常见的应用场景包括：

### 同步数据传输

通道可以被用来在不同的 goroutine 之间同步数据。当一个 goroutine 需要等待另一个goroutine 的结果时，可以使用通道进行数据的传递。例如：

```go
package main

import (
	"fmt"
)

func calculate(a, b int, result chan int) {
	result <- a + b
}

func main() {
	result := make(chan int)
	go calculate(10, 20, result)
	fmt.Println(<-result)
}

```

在这个例子中，我们使用通道来进行 a+b 的计算，并将结果发送给主函数。在主函数中，我们等待通道中的结果并输出。

### 协调多个goroutine

通道也可以用于协调多个 goroutine 之间的操作。例如，在一个生产者-消费者模式中，通道可以作为生产者和消费者之间的缓冲区，协调数据的生产和消费。例如：

```go
package main

import "fmt"

func worker(id int, jobs <-chan int, results chan<- int) {
	for j := range jobs {
		fmt.Println("worker", id, "processing job", j)
		results <- j * 2
	}
}

func main() {
	jobs := make(chan int, 100)
	results := make(chan int, 100)

	// 开启三个worker goroutine
	for w := 1; w <= 3; w++ {
		go worker(w, jobs, results)
	}

	//发送9个任务到jobs通道中
	for j := 1; j <= 9; j++ {
		jobs <- j
	}
	close(jobs)

	//输出每个任务的结果
	for a := 1; a <= 9; a++ {
		<-results
	}
}

```

### 控制并发访问

当多个 goroutine 需要并发访问某些共享资源时，通道可以用来控制并发访问。通过使用通道，可以避免出现多个 goroutine 同时访问共享资源的情况，从而提高程序的可靠性和性能。例如：

```

```

