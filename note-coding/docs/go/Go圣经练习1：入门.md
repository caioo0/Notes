# GO语言圣经之入门



**- 练习 1.1：** 修改 `echo` 程序，使其能够打印 `os.Args[0]`，即被执行命令本身的名字。

**- 练习 1.2：** 修改 `echo` 程序，使其打印每个参数的索引和值，每个一行。

**- 练习 1.3：** 做实验测量潜在低效的版本和使用了 `strings.Join` 的版本的运行时间差异。（[1.6 节](https://gopl-zh.github.io/ch1/ch1-06.html)讲解了部分 `time` 包，[11.4 节](https://gopl-zh.github.io/ch11/ch11-04.html)展示了如何写标准测试程序，以得到系统性的性能评测。）

**- 练习 1.4：** 修改 `dup2`，出现重复的行时打印文件名称。



### **练习 1.1：** 修改 `echo` 程序，使其能够打印 `os.Args[0]`，即被执行命令本身的名字。

代码文件`main.go` ,执行命令：` go run main.go 1 3 -X ?`

```go
package main
import (
    "fmt"
    "os"
)

func main () {
    for _, arg := range os.Args[0:1] { 
        fmt.Println("os.Args[0]=", arg)
    }
}
```

### **- 练习 1.2：** 修改 `echo` 程序，使其打印每个参数的索引和值，每个一行。

代码文件`main.go` ,执行命令：` go run main.go 1 3 -X ?`

```
package main
import (
    "fmt"
    "os"
)

func main () {
    for idx, arg := range os.Args { 
        fmt.Println(idx,"=", arg)
    }
}
```

### 练习 1.3：做实验测量潜在低效的版本和使用了 `strings.Join` 的版本的运行时间差异。（[1.6 节](https://gopl-zh.github.io/ch1/ch1-06.html)讲解了部分 `time` 包，[11.4 节](https://gopl-zh.github.io/ch11/ch11-04.html)展示了如何写标准测试程序，以得到系统性的性能评测。）

代码文件`main.go` ,执行命令：` go run main.go 1 3 -X ?`

```go
package main

import (
    "fmt"
    "os"
    "strings"
    "time"
)

func main() {
    s, sep := "", "\r\n"

    now := time.Now()
    for _, arg := range os.Args[:] {
        s += arg + sep
    }
    fmt.Println(s)
    end := time.Now()
    fmt.Println("低效方式运行时间", end.Sub(now))

    now2 := time.Now()
    fmt.Println(strings.Join(os.Args[:], "\r\n"))
    end2 := time.Now()
    fmt.Println("`strings.Join`运行时间", end2.Sub(now2))
}


```

### **练习 1.4：** 修改 `dup2`，出现重复的行时打印文件名称。

```
// 出现重复行时打印重复行、重复次数、出现重复行的文件名称
func main() {
	counts := make(map[string]int)
	fileNameMap := make(map[string]string)
	for _, path := range os.Args[1:] {
		file, err := os.Open(path)
		if err != nil {
			_, _ = fmt.Fprintf(os.Stderr, err.Error())
		}
		countLine(file, counts, fileNameMap)
		_ = file.Close()
	}
	fmt.Println(counts)
	for data, number := range counts {
		if number > 1 {
			fmt.Printf("重复行：%s，出现重复行的文件名称：%s，重复次数：%d\r\n", data, fileNameMap[data], number)
		}
	}
}

func countLine(file *os.File, counts map[string]int, nameMap map[string]string) {
	input := bufio.NewScanner(file)
	for input.Scan() {
		counts[input.Text()]++
		nameMap[input.Text()] = file.Name()
	}
}
```

