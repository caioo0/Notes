# Gorm操作Mysql数据库：连接、指定表名、表前缀、禁用表名复数、读取

## 指定表名

```go
type Stu struct{
	ID int
	Name string
	Age int
	Sex string
}

// tablename 指定表明

func (stu) TableName() string{
	return "student"
}
```

查询时指定表名

另一种指定表名的方式是使用Table方法。

```go
db.Table("student").First(&student)
```

