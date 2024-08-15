# sonic 

```
# 下载sonic依赖
$ go get github.com/bytedance/sonic
```

序列化和反序列化

```go
func base() {
	m := map[string]interface{}{
		"name": "z3",
		"age":  20,
	}
	
	// sonic序列化
	byt, err := sonic.Marshal(&m)
	if err != nil {
		log.Println(err)
	}
	fmt.Printf("json: %+v\n", string(byt))

	// sonic反序列化
	um := make(map[string]interface{})
	err = sonic.Unmarshal(byt, &um)
	if err != nil {
		log.Println(err)
	}
	fmt.Printf("unjson: %+v\n", um)
}

// print
// json: {"name":"z3","age":20}
// unjson: map[age:20 name:z3]
```

