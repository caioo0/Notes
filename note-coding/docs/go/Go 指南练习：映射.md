## 练习：映射

实现 `WordCount`。它应当返回一个映射，其中包含字符串 `s` 中每个“单词”的个数。函数 `wc.Test` 会对此函数执行一系列测试用例，并输出成功还是失败。

你会发现 [strings.Fields](https://go-zh.org/pkg/strings/#Fields) 很有帮助。



### 解题

- 用strings.Fields获取字符串的分割信息；
- 以位形式返回；
- 计算字符串中单个单词出现的次数。

`main.go`代码：

```go
package main

import (
    "golang.org/x/tour/wc"
    "strings"
)

func WordCount(s string) map[string]int {
    m := make(map[string]int)  // 创建映射
    c := strings.Fields(s)  // 以[]byte形式返回
    for _, v := range c {  //每出现相同的单词（字符串）
        m[v] += 1  //出现次数就 + 1         
    }
    return m
}
func main() {
    wc.Test(WordCount)
}
```

运行：

1.  go get golang.org/x/tour/wc
2. go run main.go

```bash
PASS
 f("I am learning Go!") =
  map[string]int{"Go!":1, "I":1, "am":1, "learning":1}
PASS
 f("The quick brown fox jumped over the lazy dog.") =
  map[string]int{"The":1, "brown":1, "dog.":1, "fox":1, "jumped":1, "lazy":1, "over":1, "quick":1, "the":1}
PASS
 f("I ate a donut. Then I ate another donut.") =
  map[string]int{"I":2, "Then":1, "a":1, "another":1, "ate":2, "donut.":2}
PASS
 f("A man a plan a canal panama.") =
  map[string]int{"A":1, "a":2, "canal":1, "man":1, "panama.":1, "plan":1}
```

