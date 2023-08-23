# 练习：Stringer



通过让 `IPAddr` 类型实现 `fmt.Stringer` 来打印点号分隔的地址。

例如，`IPAddr{1, 2, 3, 4}` 应当打印为 `"1.2.3.4"`。



```go
package main

import "fmt"

// TODO: 给 IPAddr 添加一个 "String() string" 方法
type IPAddr struct {
	X, Y, Z, Q int
}

// TODO: 给 IPAddr 添加一个 "String() string" 方法
func (p IPAddr) String() string {
	return fmt.Sprintf("%v.%v.%v.%v", p.X, p.Y, p.Z, p.Q)
}

func main() {

	hosts := map[string]IPAddr{
		"loopback": IPAddr{127, 0, 0, 1},
		"googleDNS": IPAddr{8, 8, 8, 8},
	}
	for _, ip := range hosts {
		fmt.Println(ip)
	}
}
```

