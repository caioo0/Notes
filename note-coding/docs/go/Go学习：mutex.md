# Mutex 和 RWMutex

GO 提供channel 来保证协程的通信，但是某些场景用锁来显示保证协程的安全更清晰易懂。

Go有两种锁：

- Mutex 互斥锁
- RWMutex 读写锁



## Mutex (互斥锁)

Mutex：互斥锁，也叫排他锁，是并发控制的一个基本手段，同一时刻一段代码只能被一个线程运行，使用时只需要关注方法Lock（加锁）和UnLock（解锁）即可。

临界区：Lock() 和 unlock() 之间的代码段称为资源的临界区（critical section）,临界区是一种防止多个线程同时执行一个特定代码节的机制.

```go
/*
源码：https://www.cnblogs.com/chenqionghe/p/13919427.html
*/
package main

import (
	"fmt"
	"sync"
)

func main() {
	var count = 0
	var wg sync.WaitGroup
	var mu sync.Mutex // 加互斥锁
	//十个协程数量
	n := 10
	wg.Add(n)
	for i := 0; i < n; i++ {
		go func() {
			defer wg.Done()
			//1万叠加
			for j := 0; j < 10000; j++ {
				mu.Lock() //
				count++
				mu.Unlock() //
			}
		}()
	}
	wg.Wait()
	fmt.Println(count)
}

```

### 实际使用

实际运用中，mutex嵌套在struct中使用，作为结构体的一部分。

如果嵌入的struct 有多个字段，我们一般会把mutex放在要控制的字段上面，然后使用空格把字段分割开来。

甚至可以把获取锁，释放锁，计数加一的逻辑封装成一个方法。



```go

package main

import (
	"fmt"
	"sync"
)

// 线程安全的计数器
type Counter struct {
	CounterType int
	Name        string

	mu    sync.Mutex
	count uint64
}

// 加一方法
func (c *Counter) Incr() {
	c.mu.Lock()
	defer c.mu.Unlock() //延迟调用
	c.count++
}

// 取数值方法 线程也需要受保护
func (c *Counter) Count() uint64 {
	c.mu.Lock()
	defer c.mu.Unlock() //延迟调用
	return c.count
}

func main() {

	var counter Counter
	var wg sync.WaitGroup
	//十个协程数量
	n := 10
	wg.Add(n)

	for i := 0; i < n; i++ {
		go func() {
			defer wg.Done()
			//1万叠加
			for j := 0; j < 10000; j++ {
				counter.Incr()
			}
		}()
	}
	wg.Wait()
	fmt.Printf("%d\b", counter.Count())
}

```



Mutex的架构演进目前分为四个阶段：

![img](.\img\wb3FzbX3bZ.jpeg!large)

mutext 演化过程

- 

## RWMutex （读写锁）

mutex 在大量并发的情况下，会造成锁等待，对性能的影响比较大。

如果某个读操作的协程加了锁，其他的协程没必要处于等待状态，可以并发地访问共享变量，这样就让读操作并行，提高读性能。

RWLock就是用来干这个的，这种锁在某一时刻能由什么问题数量的reader持有，或者被一个writer持有。

主要遵循以下规则：

- 读写锁的读锁可以重入，在已经有读锁的情况下，可以任意加读锁。
- 
