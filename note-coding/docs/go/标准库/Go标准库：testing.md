# Go语言单元测试与基准测试

> https://cloud.tencent.com/developer/article/2414278

### 一、单元测试基础

#### 1.1 测试文件与命名规范

单元测试通常放置在与被测试文件同目录下的`_test.go`文件中。测试函数必须以`Test`开头，后接被测试函数名，接受一个`t *testing.T`参数。

```go
// example_test.go
package example

import "testing"

func TestAdd(t *testing.T) {
    result := Add(2, 3)
    if result != 5 {
        t.Errorf("Add(2, 3) = %d; want 5", result)
    }
}
```

#### 1.2 常用断言方法

- `t.Error`和`t.Fatal`：报告错误，后者还会终止测试。
- `t.Logf`：记录日志信息。
- `t.Errorf`：当条件不满足时，记录错误并继续执行后续测试。

### 二、基准测试

基准测试用于评估代码性能，函数名以`Benchmark`开头，同样接受一个`*testing.B`参数。

```go
gofunc BenchmarkAdd(b *testing.B) {
    for i := 0; i < b.N; i++ {
        Add(2, 3)
    }
}
```

`b.N`会自动调整以获得稳定的运行时间。

### 三、常见问题与避免策略

#### 3.1 忽视初始化与清理

**问题**：测试之间状态可能相互影响，因为默认情况下每个测试函数共享同一个测试环境。

**解决**：使用`setup`和`teardown`逻辑。可以利用`t.Cleanup`函数注册一个或多个函数，在每次测试结束时执行。

```
func TestExample(t *testing.T) {
    db := setupDB()
    t.Cleanup(func() { db.Close() })
    // ... 测试逻辑 ...
}
```

#### 3.2 忽略并发测试的同步

**问题**：并发测试时，如果没有正确同步，可能会导致竞态条件或测试结果不可预测。

**解决**：使用`t.Parallel()`标记并发安全的测试，并确保并发访问资源时有适当的锁或其他同步机制。

```
func TestConcurrent(t *testing.T) {
    t.Parallel()
    // 并发安全的测试逻辑
}
```

#### 3.3 过度依赖外部服务

**问题**：直接依赖外部服务可能导致测试不稳定或缓慢。

**解决**：采用模拟（mock）或存根（stub）技术隔离外部依赖，或使用测试替身（test doubles）。

```
type MockService struct{}

func (m *MockService) GetData() []byte {
    return []byte("mocked data")
}

func TestFunctionWithExternalDependency(t *testing.T) {
    mockSvc := &MockService{}
    // 使用mock对象进行测试
}
```

#### 3.4 忽视测试覆盖率

**问题**：只关注测试的存在，而不关心覆盖范围，可能导致未测试到的代码路径存在bug。

**解决**：定期检查测试覆盖率，使用`go test -coverprofile=coverage.out`生成覆盖率报告，并分析改进。

### 四、总结

Go语言的`testing`包提供了强大的工具来支持单元测试和基准测试。通过遵循最佳实践，如正确命名测试函数、利用初始化与清理机制、管理并发测试、隔离外部依赖，以及关注测试覆盖率，开发者可以显著提升代码质量与稳定性。记住，良好的测试习惯是软件开发不可或缺的一部分，它能够帮助我们快速定位问题，确保代码变更的安全性，最终促进项目的可持续发展。

### 五、其他参考

1. https://geektutu.com/post/quick-go-test.html