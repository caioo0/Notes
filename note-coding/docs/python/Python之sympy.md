# sympy之diff

> 官方在线文档：[http://docs.sympy.org/0.7.1/guide.html#guide](https://link.jianshu.com/?t=http%3A%2F%2Fdocs.sympy.org%2F0.7.1%2Fguide.html%23guide)

sympy是一个Python的科学计算库，用一套强大的符号计算体系完成诸如多项式求值、求极限、解方程、求积分、微分方程、级数展开、矩阵运算等等计算问题。

## 安装sympy库

```shell
pip install sympy
```



## 1. diff 求导数

`diff(func,x,n)`

其中，func是要求导的函数，x是要对其求导的变量，n是可选的，表示求n阶导数，默认为1阶导数。

**例子1：**求一阶导数

```python
from sympy import diff
from sympy import symbols #需要先导入

def func(x):
    return x**4

x = symbols("x")
print(diff(func(x),x))

```

结果为：$4x^3$

**例子2：（求多阶导数）**

```python
from sympy import diff
from sympy import symbols
def func(x):
    return x**4

x = symbols("x")
print(diff(func(x),x,2))
```

结果为：$12x^2$

**例子3：（对多变量函数求偏导）**

```python
from sympy import diff
from sympy import symbols

def func(x,y):
    return x**4+y**3
    
x,y = symbols("x,y")
print(diff(func(x,y),x))
```

结果为：$4x^3$

**例子4:（将导数带入具体的值求某一点处的导数）**

```python
from sympy import diff
from sympy import symbols
def func(x,y):
    return x**4
x = symbols("x")
print(diff(func(x),x).subs(x,2))   # 表示将x = 2，带入导函数4*x**3中

```

结果为：32



**更多参见：**https://www.jianshu.com/p/339c91ae9f41

