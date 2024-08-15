# 函数

**匿名函数**

匿名函数只能在函数内部存在，匿名函数可以简单理解为没有名称的函数，例如

```go
package main

import "fmt"

func main() {

	c := func(a, b int) int { // 匿名函数
		return a + b
	}(1, 2)

	fmt.Println(c) // 3

}

```

或者当函数参数是一个函数类型时，这时名称不再重要，可以直接传递一个匿名函数

```go
package main

import "fmt"

func main() {
	c := DoSum(1, 2, func(a int, b int) int {
		return a + b
	})
	fmt.Println(c)  // 结果：3 
}

func DoSum(a, b int, f func(int, int) int) int {
	return f(a, b)
}

```

**闭包**

闭包（Closure）这一概念，在一些语言中又被称为Lamda表达式，经常与匿名函数一起使用，`函数 + 环境引用 = 闭包`。看一个例子：

```go
package main

import "fmt"

func main() {
	sum := Sum(1, 2)
	fmt.Println(sum(3, 4)) // 参数不起作用
	fmt.Println(sum(5, 6)) // 参数不起作用
}

func Sum(a, b int) func(int, int) int {
	return func(int, int) int {
		return a + b
	}
}
// 结果
// 3
// 3
```

在上述代码中，无论传入什么数字，输出结果都是3，稍微修改一下代码

```go
package main

import "fmt"

func main() {
	sum := Sum(5)
	fmt.Println(sum(1, 2))
	fmt.Println(sum(1, 2))
	fmt.Println(sum(1, 2))
}

func Sum(sum int) func(int, int) int {
	return func(a, b int) int {
		sum += a + b
		return sum
	}
}

// go run test27.go
//8
//11
//14
```

