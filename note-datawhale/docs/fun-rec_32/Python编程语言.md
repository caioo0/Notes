# 变量、运算符与数据类型

## 1. 注释

1. `#`符号表示整行注释
2. 三引号`'''\nline\n'''`或`""" line """`表示区间注释，引号中间的内容被注释

【例子】单行注释


```python
# 计算A
A= 1+2
print("A =",A)
# 答案 3
```

    A = 3
    

【例子】 多行注释


```python
'''
这是多行注释，用三个单引号
这是多行注释，用三个单引号
这是多行注释，用三个单引号
'''
print("Hello china") 
# Hello china

"""
这是多行注释，用三个双引号
这是多行注释，用三个双引号 
这是多行注释，用三个双引号
"""
print("hello china") 
# hello china
```

    Hello china
    hello china
    

## 2. 运算符

举个例子：

```python
4 + 5 = 9
```
例子中，$4$和$5$被称为操作数，`+`称为**运算符**。

python支持的运算符：

- 算术运算符
- 比较（关系）运算符
- 赋值运算符
- 逻辑运算符
- 位运算符
- 成员运算符
- 身份运算符
- 运算符优先级

### 2.1 算术运算符


以下假设变量 a=10，变量 b=21：

|运算符|名称|示例|
|  :----:  | :----  |: ----  |
|`+`| 加 - 两个对象相加 | `a+b`输出结果$31$|
|`-`| 减 - 第一个数减去另一个数| `a-b` 输出结果$-11$|
|`*`| 乘 - 两个数相乘或是返回一个被重复若干次的字符串| `a*b`输出结果$210$|
|`/`| 除 - x除以y | `b/a`输出结果$2.1$|
|`//`| 取整除 - 向下取接近商的整数| `9//2`输出结果 $4$， `-9//2`输出结果 $-5$|
|`%`| 取余/取模 - 返回除法的余数|b % a 输出结果 1|
|`**`| 幂 - 返回x的y次幂| 	$a**b$ 为10的21次方|
        

  [在线测试]([https://www.runoob.com/try/runcode.php?filename=test_operator&type=python)



### 2.2 比较运算符

比较运算符包含：`大于`,`大于等于`,`小于`,`小于等于`,`等于`,`不等于`

以下假设变量a为10，变量b为20：

|操作符|名称|示例|
|  :----:  | :----  |:----  |
|`>`| 大于 - 返回x是否大于y | (a > b) 返回 False。|
|`>=`| 大于等于 - 返回x是否大于等于y。| (a >= b) 返回 False。|
|`<`| 小于 - 返回x是否小于y。所有比较运算符返回1表示真，返回0表示假。这分别与特殊的变量True和False等价。注意，这些变量名的大写。| (a < b) 返回 True。|
|`<=`| 小于等于 - 返回x是否小于等于y。| 	(a <= b) 返回 True。|
|`==`| 等于 - 比较对象是否相等|	(a == b) 返回 False。|
|`!=`| 不等于 - 比较两个对象是否不相等| (a != b) 返回 True。|

【例子】


```python
print(2 > 1)  # True
print(2 >= 4)  # False
print(1 < 2)  # True
print(5 <= 2)  # False
print(3 == 4)  # False
print(3 != 5)  # True
```

    True
    False
    True
    False
    False
    True
    

###  2.3 赋值运算符

以下假设变量a为10，变量b为20：

|操作符|名称|示例|
|  :----:  | :----  |:----  |
|`=`| 简单的赋值运算符| c= a + b 将 a + b 的运算结果赋值为 c|
|`+=`| 加法赋值运算符| c += a 等效于 c = c + a |
|`-=`| 减法赋值运算符。| c -= a 等效于 c = c - a|
|`*=`| 乘法赋值运算符| 	`c *=  a` 等效于` c = c *a`|
|`/=`| 除法赋值运算符|	c /= a 等效于 c = c / a|
|`%=`| 取模赋值运算符| c %= a 等效于 c = c % a|
|`**=`| 幂赋值运算符| $c **= a$ 等效于 $c = c ** a$|
|`//=`| 取整赋值运算符| c //= a 等效于 c = c // a|
|`:=`| 海象运算符，可在表达式内部为变量赋值。`Python3.8 版本新增运算符。`| 在这个示例中，赋值表达式可以避免调用 len() 两次:|

【例子】海象运算符，摘自[Python 中海象运算符的三种用法 ](https://www.cnblogs.com/wongbingming/p/12743802.html)


```python
a = [1,2,3,4,5,5,6,7] 

# 1. 第一个用法：if/else 

if (n := len(a)) > 3:
    print(f"List is too long ({n} elements, expected <= 10)")
    
  
if (age:= 20) > 18:print("已经成年了")
    
 
# 2. 第二个用法：while
while (p := input("Enter the password: ")) != "youpassword":continue
        
```

    List is too long (8 elements, expected <= 10)
    已经成年了
    Enter the password: 3
    Enter the password: 3
    Enter the password: youpassword
    


```python
# 查出所有会员中过于肥胖的人的 bmi 指数
# 3. 第三个用法：推导式
members = [
    {"name": "小五", "age": 23, "height": 1.75, "weight": 72},
    {"name": "小李", "age": 17, "height": 1.72, "weight": 63},
    {"name": "小陈", "age": 20, "height": 1.78, "weight": 82},
]

count = 0

def get_bmi(info):
    global count
    count += 1

    print(f"执行了 {count} 次")

    height = info["height"]
    weight = info["weight"]

    return weight / (height**2)

fat_bmis = [bmi for m in members if (bmi := get_bmi(m)) > 24]

print(fat_bmis)
```

    执行了 1 次
    执行了 2 次
    执行了 3 次
    [25.88057063502083]
    

### 2.4 位运算符

下表中变量 a 为 60，b 为 13二进制格式如下：

```python
a = 0011 1100

b = 0000 1101

-----------------

a&b = 0000 1100

a|b = 0011 1101

a^b = 0011 0001

~a  = 1100 0011
```

|运算符|描述|示例|
|  :----:  | :----  |:----  |
|`&`| 按位与运算符：参与运算的两个值,如果两个相应位都为1,则该位的结果为1,否则为0| (a & b) 输出结果 12 ，二进制解释： 0000 1100|
|`\|`| 按位或运算符：只要对应的二个二进位有一个为1时，结果位就为1 | `(a \| b) `输出结果 61 ，二进制解释： 0011 1101 |
|`^`| 按位异或运算符：当两对应的二进位相异时，结果为1 | (a ^ b) 输出结果 49 ，二进制解释： 0011 0001|
|`~`| 按位取反运算符：对数据的每个 二进制取反，即把1变为0，把0变为1。`~x`类似于`-x-1`| 	(~a ) 输出结果 -61 ，二进制解释： 1100 0011， 在一个有符号二进制数的补码形式。|
|`<<`| 左移动运算符：运算数的各二进位全部左移若干位，由"<<"右边的数指定移动的位数，高位丢弃，低位补0。|a << 2 输出结果 240 ，二进制解释： 1111 0000|
|`>>`|右移动运算符：把">>"左边的运算数的各二进位全部右移若干位，">>"右边的数指定移动的位数|a >> 2 输出结果 15 ，二进制解释： 0000 1111
|



【实例】


```python
#!/usr/bin/python3
 
a = 60            # 60 = 0011 1100 
b = 13            # 13 = 0000 1101 
c = 0
 
c = a & b        # 12 = 0000 1100
print ("1 - c 的值为：", c)
 
c = a | b        # 61 = 0011 1101 
print ("2 - c 的值为：", c)
 
c = a ^ b        # 49 = 0011 0001
print ("3 - c 的值为：", c)
 
c = ~a           # -61 = 1100 0011
print ("4 - c 的值为：", c)
 
c = a << 2       # 240 = 1111 0000
print ("5 - c 的值为：", c)
 
c = a >> 2       # 15 = 0000 1111
print ("6 - c 的值为：", c)
```

    1 - c 的值为： 12
    2 - c 的值为： 61
    3 - c 的值为： 49
    4 - c 的值为： -61
    5 - c 的值为： 240
    6 - c 的值为： 15
    

### 2.5 逻辑运算符

Python语言支持逻辑运算符，以下假设变量 a 为 10, b为 20:

|运算符|逻辑表达式|描述|示例|
|  :----:  | :----  |:----  |:----  |
|`and`| x and y  | 布尔"与" - 如果 x 为 False，x and y 返回 x 的值，否则返回 y 的计算值。 |(a and b) 返回 20。|
|`or`| x or y  | 布尔"或" - 如果 x 是 True，它返回 x 的值，否则它返回 y 的计算值。 |(a or b) 返回 10。|
|`not`| not x  | 布尔"非" - 如果 x 为 True，返回 False 。如果 x 为 False，它返回 True。 |not(a and b) 返回 False。|




```python
a = 10
b = 20
 
if ( a and b ):
   print ("1 - 变量 a 和 b 都为 true")
else:
   print ("1 - 变量 a 和 b 有一个不为 true")
 
if ( a or b ):
   print ("2 - 变量 a 和 b 都为 true，或其中一个变量为 true")
else:
   print ("2 - 变量 a 和 b 都不为 true")
 
# 修改变量 a 的值
a = 0
if ( a and b ):
   print ("3 - 变量 a 和 b 都为 true")
else:
   print ("3 - 变量 a 和 b 有一个不为 true")
 
if ( a or b ):
   print ("4 - 变量 a 和 b 都为 true，或其中一个变量为 true")
else:
   print ("4 - 变量 a 和 b 都不为 true")
 
if not( a and b ):
   print ("5 - 变量 a 和 b 都为 false，或其中一个变量为 false")
else:
   print ("5 - 变量 a 和 b 都为 true")
```

    1 - 变量 a 和 b 都为 true
    2 - 变量 a 和 b 都为 true，或其中一个变量为 true
    3 - 变量 a 和 b 有一个不为 true
    4 - 变量 a 和 b 都为 true，或其中一个变量为 true
    5 - 变量 a 和 b 都为 false，或其中一个变量为 false
    

### 2.6 成员运算符

|运算符|描述|示例|
|  :----:  | :----  |:----  |
|`in`| 如果在指定的序列中找到值返回 True，否则返回 False。 |x 在 y 序列中 , 如果 x 在 y 序列中返回 True。|
|`not in`| 如果在指定的序列中没有找到值返回 True，否则返回 False。	 |x 不在 y 序列中 , 如果 x 不在 y 序列中返回 True。|


### 2.7 身份运算符


|运算符|描述|示例|
|  :----:  | :----  |:----  |
|`is`| is 是判断两个标识符是不是引用自一个对象。 |x is y, 类似 id(x) == id(y) , 如果引用的是同一个对象则返回 True，否则返回 False。|
|`is not `| is not 是判断两个标识符是不是引用自不同对象。	 |x is not y ， 类似 id(a) != id(b)。如果引用的不是同一个对象则返回结果 True，否则返回 False。|

注： [`id()`](https://www.runoob.com/python/python-func-id.html) 函数用于获取对象内存地址。


### 2.8 三元运算符

【例子】


```python
x, y = 4, 5

if x < y:
    small = x
else:
    small = y
    
print(small) # 4
```

    4
    

三元操作符的条件表达式：


```python
x,y,z = 4,5,6
small = z if x<y else y

print(small) # 4
```

    4
    

## 3. 变量和赋值


- Python 中的变量不需要声明,每个变量在使用之前，必须赋值，变量赋值以后该变量才会被创建。
- 变量名可以包括字母、数字、下划线、但变量名不能以数字开头。
- Python 变量名是大小写敏感的，foo != Foo。
- 在 Python 中，变量就是变量，它没有类型，我们所说的"类型"是变量所指的内存中对象的类型。

等号（=）用来给变量赋值。

等号（=）运算符左边是一个变量名,等号（=）运算符右边是存储在变量中的值。例如：




```python
#!/usr/bin/python3

counter = 100          # 整型变量
miles   = 1000.0       # 浮点型变量
name    = "runoob"     # 字符串

print (counter)
print (miles)
print (name)
```

    100
    1000.0
    runoob
    

**多个变量赋值**

Python允许你同时为多个变量赋值。例如：


```python
a, b, c = 1, 2, "runoob"
```

以上实例，两个整型对象 1 和 2 的分配给变量 a 和 b，字符串对象 "runoob" 分配给变量 c。

## 4. 数据类型

python3 中有六个标准的数据类型：

- Number(数字) 
- String(字符串)
- List(列表)
- Tuple(元组)
- Set(集合)
- Dictionary(字典)


**基本类型：**整型、浮点型、布尔型  
**容器类型：**字符串、元组、列表、字典和集合  

在Python 3里，只有一种整数类型 int，表示为长整型，没有 python2 中的 Long。

六个标准数据类型中：

- **不可变数据(3个)：** Number（数字）、String（字符串）、Tuple（元组）；

- **可变数据(3个):**List（列表）、Dictionary（字典）、Set（集合）。


### 4.1 数字(Number)

数字数据类型用于存储数值

数据类型是不允许改变的,这就意味着如果改变数字数据类型的值，将重新分配内存空间。

var1 = 1
var2 = 10

您也可以使用del语句删除一些数字对象的引用。

```md
del var1[,var2[,var3[....,varN]]]
```

<b>获取类型信息</b>

`type(object)` 获取类型信息

`isinstance(object, classinfo)` 判断一个对象是否是一个已知的类型。

```python
print(isinstance(1, int))  # True

```


- `type()` 不会认为子类是一种父类类型，不考虑继承关系。
- `isinstance()` 会认为子类是一种父类类型，考虑继承关系。

如果要判断两个类型是否相同推荐使用 `isinstance()`。

**类型转换**

- 转换为整型 `int(x, base=10)`
- 转换为字符串 `str(object='')`
- 转换为浮点型 `float(x)`

## 5. print() 函数

```python
print(*objects, sep=' ', end='\n', file=sys.stdout, flush=False)
```

- 将对象以字符串表示的方式格式化输出到流文件对象file里。其中所有非关键字参数都按`str()`方式进行转换为字符串输出；
- 关键字参数`sep`是实现分隔符，比如多个参数输出时想要输出中间的分隔字符；
- 关键字参数`end`是输出结束时的字符，默认是换行符`\n`；
- 关键字参数`file`是定义流输出的文件，可以是标准的系统输出`sys.stdout`，也可以重定义为别的文件；
- 关键字参数`flush`是立即把内容输出到流文件，不作缓存。

举几个例子：[详细参考](https://www.runoob.com/python3/python3-inputoutput.html)


```python
print('{}网址： "{}!"'.format('菜鸟教程', 'www.runoob.com'))
```

    菜鸟教程网址： "www.runoob.com!"
    


```python
print('{0} 和 {1}'.format('Google', 'Runoob'))
```

    Google 和 Runoob
    


```python
print('{name}网址： {site}'.format(name='菜鸟教程', site='www.runoob.com'))
```

    菜鸟教程网址： www.runoob.com
    


```python
print('站点列表 {0}, {1}, 和 {other}。'.format('Google', 'Runoob', other='Taobao'))
```

    站点列表 Google, Runoob, 和 Taobao。
    

## 练习题1：

**[问题1]** 怎样对python中的代码进行注释？

  解答：  
  python注释可使用 整行注释符`#` 或 三引号区间注释符号，`'''txt'''`或`""" txt """` ，引号中间的`txt`指具体注释内容，替换为您的具体注释描述内容。


**[问题2]**python有哪些运算符，这些运算符的优先级是怎样的？

  解答：
  
 运算符的优先级规律：
 
 - 一元运算符优于二元运算符。例如 `3 ** -2` 等价于 `3 ** (-2)`
 - 先算术运算，后移位运算，最后位运算。例如 `1 << 3 + 2 & 7`等价于 `(1 << (3 + 2)) & 7`。
 - 逻辑运算最后结合。例如`3 < 4 and 4 < 5`等价于`(3 < 4) and (4 < 5)`。
 
 
|运算符|	描述|
|----|----|
|**	|指数 (最高优先级)|
|~ + -	|按位翻转, 一元加号和减号 (最后两个的方法名为 +@ 和 -@)|
|* / % //|	乘，除，求余数和取整除|
|+ -	|加法减法|
|>> <<	|右移，左移运算符|
|&	|位 'AND'|
|^ \|	|位运算符|
|<= < > >=	|比较运算符|
|== !=	|等于运算符|
|= %= /= //= -= += `*=`, `**=`	|赋值运算符|


**[问题3]**python 中 `is`, `is not` 与 `==`, `!=` 的区别是什么？

 解答：  

 1. `is`,`is not`对比的是两个变量的内存地址；
 2. `==`, `!=`对比的是两个变量的值；
 3. 当两个变量指向的都是地址不变的类型（str）时，`is`, `is not` 与 `==`, `!=` 是完全等价的。
 4. 当两个变量指向的是地址可变的类型(list,dict)时，则两者不同。


```python
a = "hello"
b = "hello"
print(a is b, a == b)  # True True
print(a is not b, a != b)  # False False
```

    True True
    False False
    


```python
a = ["hello"]
b = ["hello"]
print(a is b, a == b)  # False True
print(a is not b, a != b)  # True False
```

    False True
    True False
    

**[问题4]** python 中包含哪些数据类型？这些数据类型之间如何转换？

解答：

python3的数据类型有六种：  
- 基本类型：(Number)数字->整型，浮点型，布尔型，复数
- 容器类型：列表(List)、字典(dict)、元组(Tuple)、字符串(string)和集合(set）

数据类型转换：

我们需要对数据内置的类型进行转换，数据类型的转换，你只需要将数据类型作为函数名即可。

- int(x) 将x转换为一个整数。

- float(x) 将x转换到一个浮点数。

- complex(x) 将x转换到一个复数，实数部分为 x，虚数部分为 0。

- complex(x, y) 将 x 和 y 转换到一个复数，实数部分为 x，虚数部分为 y。x 和 y 是数字表达式。





## 参考资料：

1. [Python编程时光](http://pythontime.iswbm.com/en/latest/)


```python

```
