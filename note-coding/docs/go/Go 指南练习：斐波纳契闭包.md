## 练习：斐波纳契闭包

让我们用函数做些好玩的事情。

实现一个 `fibonacci` 函数，它返回一个函数（闭包），该闭包返回一个[斐波纳契数列](https://zh.wikipedia.org/wiki/斐波那契数列) `(0, 1, 1, 2, 3, 5, ...)`。

### 实现：

1. 闭包实现：

```go
package main
 
import "fmt"
 
// fibonacci is a function that returns
// a function that returns an int.
func fibonacci() func() int {
	a,b := 0,1 //初始值为0,1
	return func () int{ 
		a,b = b,a+b //将a变为b,b变为a+b
		return b-a //此时应该返回为改变时的a, 也就是a+b-b = b-a
	}
	
}
 
func main() {
	f := fibonacci()
	for i := 0; i < 10; i++ {
		fmt.Println(f())
	}
}
```

2. 递归实现：

```go
package main
import (  
   "fmt"  
)
func fib(n int) int {  
   if n <= 1 {  
       return n  
   }  
   return fib(n-1) + fib(n-2)  
}
func main() {  
  
     for i := 0; i < 10; i++ {
        fmt.Println(fib(i))
    }
}
```

