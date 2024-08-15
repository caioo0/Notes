# 练习：切片



在Go中，数组和切片两者看起来长得几乎一模一样，但功能有着不小的区别，数组是定长的数据结构，长度被指定后就不能被改变，而切片是不定长的，切片在容量不够时会自行扩容。



## 数组 

数组的声明是长度只能是一个常量，不能是变量 

```go
var a [5]int   # 初始化
nums :=[5]int{1,2,3,4,5}  #元素初始化
nums :=new([5]int)  // new获取指针

nums[0] = 1
len(nums)  
cap(nums)

nums := [5]int{1, 2, 3, 4, 5}
nums[1:] // 子数组范围[1,5) -> [2 3 4 5]
nums[:5] // 子数组范围[0,5) -> [1 2 3 4 5]
nums[2:3] // 子数组范围[2,3) -> [3]
nums[1:3] // 子数组范围[1,3) -> [2 3]

```

## 切片

**初始化**

切片的初始化方式有以下几种

```go
var nums []int // 值  默认为nil 
nums := []int{1, 2, 3} // 值
nums := make([]int, 0, 0) // 值   //推荐使用make函数，三个参数分别代表:类型，长度，容量 
nums := new([]int) // 指针
```

**长度和容量**

```go
package main

import (
	"fmt"
)

func main() {
	nums := make([]int, 0, 0)
	nums = append(nums, 1, 2, 3, 4, 5, 6, 7, 8)
	fmt.Println(len(nums), cap(nums), nums)
}
```

## append 插入

```go
package main

import "fmt"

func main() {

	nums := []int{1, 2, 3, 4, 5, 6, 7, 8, 9, 10}

	// nums = append([]int{-1, 0}, nums...) // 从头部插入元素
	// fmt.Println(nums)                    // [-1 0 1 2 3 4 5 6 7 8 9 10]

	// 从中间下标i插入元素
	// i := 3
	// nums = append(nums[:i+1], append([]int{999, 999}, nums[i+1:]...)...)
	// fmt.Println(nums) // i=3，[1 2 3 4 999 999 5 6 7 8 9 10]

	// 从尾部插入元素
	nums = append(nums, []int{99, 100}...) //...表示拆开切片，再添加
	fmt.Println(nums)                      // [1 2 3 4 5 6 7 8 9 10 99 100]

}

```

使用make创建切片时，用append（）添加元素 容易犯错

```go
package main

import "fmt"

func main(){
	var a = make([]int, 5, 10)
	fmt.Println(a)
	fmt.Printf("%p\n",a)
	for i := 0; i <10; i++ {
		a = append(a,i)
    //%p 打印切片地址
		fmt.Printf("%v,%p,cap(a):%d\n",a,a,cap(a))
	} 
}

```

```
# 结果 
[0 0 0 0 0]
0xc0000180a0
[0 0 0 0 0 0],0xc0000180a0,cap(a):10
[0 0 0 0 0 0 1],0xc0000180a0,cap(a):10
[0 0 0 0 0 0 1 2],0xc0000180a0,cap(a):10
[0 0 0 0 0 0 1 2 3],0xc0000180a0,cap(a):10
[0 0 0 0 0 0 1 2 3 4],0xc0000180a0,cap(a):10
[0 0 0 0 0 0 1 2 3 4 5],0xc00007c000,cap(a):20
[0 0 0 0 0 0 1 2 3 4 5 6],0xc00007c000,cap(a):20
[0 0 0 0 0 0 1 2 3 4 5 6 7],0xc00007c000,cap(a):20
[0 0 0 0 0 0 1 2 3 4 5 6 7 8],0xc00007c000,cap(a):20
[0 0 0 0 0 0 1 2 3 4 5 6 7 8 9],0xc00007c000,cap(a):20

```

**拷贝**

切片在拷贝时需要确保目标切片有足够的长度，例如：

```go
func main() {
	dest := make([]int, 0)
	src := []int{1, 2, 3, 4, 5, 6, 7, 8, 9}
	fmt.Println(src, dest)
	fmt.Println(copy(dest, src))
	fmt.Println(src, dest)
}
```

**多维切片**

```go
package main

import "fmt"

func main() {

	slices := make([][]int, 5)

	fmt.Println(len(slices), slices)

	for i := 0; i < len(slices); i++ {
		slices[i] = make([]int, 5)
	}
	for _, slice := range slices {
		fmt.Println(slice)
	}
}

```

clear `go1.21`新增内置函数

```go
package main

import (
    "fmt"
)

func main() {
    s := []int{1, 2, 3, 4}
    clear(s)  // 也可以这么操作： s = s[:0:0]
    fmt.Println(s)
}

// 输出： [0 0 0 0]

```

