#  练习：Reader

实现一个 `Reader` 类型，它产生一个 ASCII 字符 `'A'` 的无限流。



### 分析：

`io` 包指定了 `io.Reader` 接口，它表示从数据流的末尾进行读取。

`Read` 用数据填充给定的字节切片并返回填充的字节数和错误值。在遇到数据流的结尾时，它会返回一个 `io.EOF` 错误。

```
package main

import "golang.org/x/tour/reader"

type MyReader struct{}

// TODO: 给 MyReader 添加一个 Read([]byte) (int, error) 方法
func (r MyReader) Read(b []byte) (int,error){
    //赋值并返回
    b[0] = 'A'
    return 1,nil
}
func main() {
	reader.Validate(MyReader{})
}

```

