# Gorm hook的使用

## hook介绍

hook 钩子函数，是指当满足一定的触发条件时会自动触发的函数，我们能借助 Gorm 框架对数据库进行 CRUD 操作，对于这些操作，我们能绑定特定的 hook 函数，进行方法的加强。

## 钩子的概述

Gorm 提供的多种钩子函数：

`BeforeSave`: 在保存数据之前触发的钩子函数

`AfterSave`: 在保存数据之后触发的钩子函数

`BeforeDelete`: 在删除数据之前触发的钩子函数

`AfterDelete`: 在删除数据之后触发的钩子函数

`BeforeLoad`: 在加载数据之前触发的钩子函数

`AfterLoad`: 在加载数据之后触发的钩子函数

## hook的使用

需要注意的是，Gorm 中的 hook 是绑定在 model 对象而不是 gorm.DB 上的。

```go
package main

import (
   "fmt"
   "gorm.io/driver/sqlite"
   "gorm.io/gorm"
)

type Product struct {
   gorm.Model
   Code  string
   Price uint
}

func (p *Product) BeforeCreate(tx *gorm.DB) (err error) {
   fmt.Print("BeforeCreate......")
   return
}

func main() {
   db, err := gorm.Open(sqlite.Open("test.db"), &gorm.Config{})
   if err != nil {
      panic("failed to connect database")
   }

   // Create
   db.Create(&Product{Code: "D41", Price: 100})

}

```

## 参考资料

1. https://juejin.cn/post/7122022777845973029