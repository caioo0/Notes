# 结构体struct 

两种不同的使用方式：

第一种：

```go
package main

import "fmt"

type Programmer struct {
	Name     string
	Age      int
	Job      string
	Language []string
}

func NewProgrammer() Programmer {
	return Programmer{
		"jack",
		19,
		"coder",
		[]string{"Go", "C++"}}
}

func main() {

	fmt.Println(NewProgrammer())
}

```

第二种：

```go
package main

import "fmt"

type Programmer struct {
	Name     string
	Age      int
	Job      string
	Language []string
}

func main() {

	programmer := Programmer{
		Name:     "jack",
		Age:      19,
		Job:      "coder",
		Language: []string{"Go", "C++"},
	}
	fmt.Println(programmer)
}

```

## 组合

匿名：

```go
package main

import "fmt"

type Person struct {
	name string
	age  int
}

type Student struct {
	Person
	school string
}

type Employee struct {
	Person
	job string
}

func main() {

	student := Student{
		Person: Person{name: "jack", age: 18},
		school: "lili school",
	}
	fmt.Println(student.name, student)

}


```

显示：

```go
package main

import "fmt"

type Person struct {
	name string
	age  int
}

type Student struct {
	p      Person
	school string
}

type Employee struct {
	p   Person
	job string
}

func main() {

	student := Student{
		p:      Person{name: "jack", age: 18},
		school: "lili school",
	}
	fmt.Println(student.p.name, student)

}

```

**指针**

对于结构体指针而言，不需要解引用就可以直接访问结构体的内容，例子如下：

```go
package main

import "fmt"

type Person struct {
	name string
	age  int
}

type Student struct {
	p      Person
	school string
}

type Employee struct {
	p   Person
	job string
}

func main() {

	student := Student{
		p:      Person{name: "jack", age: 18},
		school: "lili school",
	}
	fmt.Println(student.p.name, student)

	p := &Person{
		name: "jack",
	}
	fmt.Println(p.age, p.name)

}

```

