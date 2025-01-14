## 练习：切片

实现 `Pic`。它应当返回一个长度为 `dy` 的切片，其中每个元素是一个长度为 `dx`，元素类型为 `uint8` 的切片。当你运行此程序时，它会将每个整数解释为灰度值（好吧，其实是蓝度值）并显示它所对应的图像。

图像的选择由你来定。几个有趣的函数包括 `(x+y)/2`, `x*y`, `x^y`, `x*log(y)` 和 `x%(y+1)`。

（提示：需要使用循环来分配 `[][]uint8` 中的每个 `[]uint8`；请使用 `uint8(intValue)` 在类型之间转换；你可能会用到 `math` 包中的函数。）



### 实现：

- 外层切片的长度为dy；
- 内层切片的长度为dx；
- 内层切片中的每个元素值为 (x+y)/2，x*y...；
- 使用嵌套循环的方式计算颜色值。

以`x^y`为例：		

```go
package main

import "golang.org/x/tour/pic"

func Pic(dx, dy int) [][]uint8 {
    a := make([][]uint8,dy)  //外层切片
    for x := range a{
        b := make([]uint8,dx)  //里层切片
        for y := range b{
            b[y] = uint8(repdx(x,y) - 1)  //给里层切片里的每一个元素赋值。其中x*y可以替换成别的函数
        }
        a[x] = b  //给外层切片里的每一个元素赋值
    }
    return a
}
func repdx(x,y int) int {
	return x^y
}

func main() {
    pic.Show(Pic)
}
```

