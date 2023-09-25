# **第1章 开始**

>  **本文为《C++ Primer 中文版（第五版）》和 《C++ Primer （第五版）习题集》 第1章阅读要点总结，重要知识点归以及练习题的解答。原书更为详细，本文仅作学习交流使用，未经授权禁止转载。**

## 1.1 编写一个简单的c++程序

每个c++程序都包含一个或多个函数（function）

一个简单的函数

```c++
int main()
{
	return 0; # 返回类型 int ,必须分号结束，
}
```

一个函数得定义包含四部分：返回类型（return type）、函数名（function name）、一个括号包围的形参列表（parameter list,允许为空）以及函数体（function body）。

### 编译.运行程序

常见的源文件后缀：`.cc  .cxx .cpp  .cp  .c `

**命令行运行编译器**

假定我们的main程序保存在文件`prog1.cc`中，可以用如下命令来编译它

```shell
$ cc prog1.cc 

```

编译器生成一个可执行文件。windows环境：`prog1.exe` ,unix环境可执行文件名 `a.out `

**运行 GNU 或 微软编辑器**

GNU:

```
$ g++ -o prog1 prog1.cc 
```

其中-o prog1是编译器参数，指定了可执行文件的文件名。

- 编译器通常包含一些选项，能对有问题的程序结构发出警告。在GNU编译器中可以使用-Wall选项。

运行可执行文件

```shell
# window 环境下

$ prog1
# 或者
$ .\prog1

# unix 环境下

$ a.out
#或者
$ ./a.out

```

访问main的访问值得方法依赖于系统。执行完一个程序后，都可以通过echo 命令获得其返回值

```shell
# unix 系统

$ echo $?

# windows 系统

$ echo %ERRORLEVEL%
```

### **1.1 节 练习**

**练习 1.1** 查阅你使用的编译器的文档，确定它所使用的命名约定。编译并运行第 2 页的 main 程序。

【出题思路】

熟悉编译工具和集成开发环境。

【解答】

编译指令

```shell
g++ -o prog1 prog1.cc
```

运行

```shell
./prog1
```

没有运行结果（因为函数没有输出）, 通过 `echo %ERRORLEVEL% $`命令看到返回值为0

**练习1.2** 改写程序，让它返回-1。返回值-1 通常被当作程序错误的标识。重新编译并运行你的程序，观察你的系统如何处理 main 返回的错误标识。

【出题思路】

了解 C++程序与操作系统间的交互。

【解答】

Windows 11 操作系统并不处理或报告程序返回的错误标识，直观上，返回-1 的程序与返回 0 的程序在执行效果上并无不同。

## **1.2 初识输入输出**

C++通过标准库（standard library）来提供输入输出（IO）机制。

**iostream库**

包含两个基础类型**istream**和**ostream**，分别表示输入流和输出流。一个流就是一个字符序列。术语“流”想要表达的是，随着时间的推移，字符是顺序生成或消耗的。

**标准输入输出对象**

标准库定义了四个IO对象：

- cin：istream对象，处理输入，称为标准输入
- cout：ostream对象，处理输出，称为标准输出
- cerr：ostream对象，输出警告和错误信息，称为标准错误
- clog：ostream对象，输出程序运行时的一般性信息

**一个使用IO库的程序**

通过扩展main程序，使之能提示用户输入两个数，然后输出它们的和：

```c++
#include <iostream>
int main()
{
	std::cout << "Enter two numbers:" << std::endl;
	int v1 = 0,v2 = 0;
	std::cin >> v1 >> v2;
	std::cout << "The sum of " << v1 << " and " << v2
				<< " is " << v1 + v2 << std::endl;
	return 0;
}
```

运行程序得出结果如下：

```shell
$ g++ -o prog1 prog1.cc

$ prog1
Enter two numbers:
4 2
The sum of 4 and 2 is 6
```

程序的第一行

```c++
#include <iostream>
```

尖括号中的名字指出了一个**头文件**(header)。

通常情况下，#include指令必须出现在所有函数之外。

### 向流写入数据

```c++
std::cout << "Enter two numbers: " << std::endl;
```

- <<： 输出运算符，接受两个运算对象，左侧的运算对象必须是一个ostream对象，右侧的运算对象是要打印的值，此运算符将给定的值写到给定的ostream对象中。
- 输出运算符的计算结果就是其左侧运算对象，即，计算结果就是我们写入给定值的那个ostream对象。

输出语句连续使用了两次<<运算符，第一个运算符的结果成为了第二个运算符的左侧运算对象。将输出请求连接起来。表达式等价于：

```c++
(std::cout << "Enter two numbers: ") << std::endl;
```

l链中每个运算符的左侧对象都是相同的，本例中是`std::cout`，也可以用两条语句生成相同的输出：

```c++
std::cout << "Enter two numbers: ";
std::cout << std::endl;
```

第一个输出运算：字符串字面值常量(string literal),用双引号包围的字符序列（双引号之间的文本被打印到标准输出）

第二个运算符：endl，这是一个**操纵符(maniplulator)**。效果是结束当前行，并将与设备关联的**缓冲区**(buffer)中的内容刷到设备中，**缓冲刷新操作**可以保证到目前为止程序所产生的所有输出都真正写入输出流中，而不是仅停留在内存中等待写入流。

### **使用标准库的名字**

程序使用std::cout和std::endl而不是直接的cout和endl

前缀std::指出名字cout和endl是定义在名为**std**的**命名空间(namespace)**中的。命名空间可以避免名字定义冲突，以及使用库中相同名字导致的冲突。

标准库定义的名字都在命名空间std中，当使用标准库中的一个名字，必须显示说明，比如写成`std::cout`

其中**`:`** 被称为作用域运算符

### **从流读取数据**

首先定义两个名为v1和v2的变量来保存输入

```c++
int v1 = 0,v2 = 0;
```

初始化为0.

初始化一个变量，就是在变量创建的同时为它赋予一个值。

下一条语句是

```
std::cin >> v1 >> v2;
```

**输入运算符 （ >> ）**与输出运算符类似。接受一个istream作为其左侧对象，接受一个对象作为其右侧对象。从给定的istream读入数据，并存入给定对象中。

同样，此表达式等价于

```
(std::cin >> v1) >> v2;
```

也可以写成两条语句

```
std::cin >> v1;
std::cin >> v2;
```

**完成程序**

打印计算结果

```
std::cout << "The sum of " << v1 << " and " << v2
            << " is " << v1 + v2 << std::endl;
```

运算对象并不都是相同类型的值。

标准库定义了不同版本的输入输出运算符，来处理这些不同类型的运算对象。

### 1.2 节 练习

**练习1.3**  编写程序，在标准输出上打印 Hello, World。

```c++
#include <iostream>
int main()
{
    std::cout << "Hello,World." << std::endl;
}
```

**练习  1.4 **：我们的程序使用加法运算符+来将两个数相加。编写程序使用乘法运算符，来打印两个数的积。

```c++
#include <iostream>
int main()
{
	std::cout << "input two numbers" << std::endl;
	int v1 = 0,v2 = 0;
	std::cin >> v1 >> v2;
	std::cout << v1 << " 和 " << v2 << "的积为"
			<< v1 * v2 << std::endl;
    return 0;
}
```

**练习 1.5：** 我们将所有输出操作放在一条很长的语句中。重写程序，将每个运算对象的打印操作放在一条独立的语句中。

```c++
#include <iostream>
int main()
{
	std::cout << "input two numbers";
	std::cout << std::endl;
	int v1,v2;
	std::cin >> v1 >> v2;
	std::cout << " 数值 " << v1;
    std::cout << " 和 " << v2 ;
    std::cout << "的积为";
	std::cout << v1 * v2 << std::endl;
    return 0;
}
```



## **1.3 注释简介**

>  当修改代码时，不要忘记修改注释。

C++ 有两种注释：

1. 单行注释：以双斜线（//）开始，以换行符结束。
2. 界定符对注释：以 /* 开始，以 */ 结束。

**注意事项**

- 注释界定符不能嵌套

  比如下面的程序会产生错误：

  ```c++
  /*
   * 注释对/**/不能嵌套
   * 不能嵌套
   */
   int main()
   {
   	return 0;
   }
  ```

  

- 最好的方式是用单行注释方式注释掉代码段的每一行。

### 1.3 节 练习

**练习 1.7：** 编译一个包含不正确的嵌套注释的程序，观察编译器返回的错误信息.

```c++
#include <iostream>
/*
 * 输入两个数字v1和v2,两个数字之间输入空格/**/不能嵌套
 * 输出两个数的积 
 */
int main()
{
	std::cout << "input two numbers";
	std::cout << std::endl;
	int v1,v2;
	std::cin >> v1 >> v2;
	std::cout << " 数值 " << v1;
    std::cout << " 和 " << v2 ;
    std::cout << "的积为";
	std::cout << v1 * v2 << std::endl;
    return 0;
}
```

**练习** **1.8 **: 指出下列哪些输出语句是合法的（如果有的话）：

```c++
#include <iostream>

 int main()
 {
 	std::cout << "/*";         		// 合法
    std::cout << "*/"; 				// 合法
    std::cout << /* "*/" */; 		// 报错
    std::cout << /* "*/" /* "/*" */;// 报错
 }  
```



## **1.4 控制流**

语句是顺序执行的，语句块的第一条语句首先执行，然后是第二条语句，依此类推。

### **while语句**

while 语句的执行过程中交替地检测条件和执行关联地语句，直到条件为假。



**练习** **1.9：**编写程序，使用 while 循环将 50 到 100 的整数相加。

```c++
#include <iostream>
using namespace std;
int main()
{
    int a = 50,sum ;
    while(a<=100)
    {
        cout << "a 的值" << a << endl;
        sum += a;
        a++;
    }
    cout << "50 到 100 的整数相加的和等于" << sum << endl;
    return 0;

}
```

**练习** **1.10：**除了++运算符将运算对象的值增加 1 以外，还有一个递减运算符（--）实现将值减少 1。编写程序，使用递减运算符在循环中按递减序打印出 10 到 0 之间的整数。

```c++
#include <iostream>
using namespace std;
int main()
{
    int a = 10 ;
    while(a>=0)
    {
        cout << "a 的值" << a << endl;
        a--;
    }
    cout << endl;
    return 0;
}
```

**练习** **1.11：**编写程序，提示用户输入两个整数，打印出这两个整数所指定的范围内的所有整数。

```c++
#include <iostream>
int main()
{
	std::cout << "input two numbers";
	std::cout << std::endl;
	int v1,v2;
	std::cin >> v1 >> v2;
    int i = v1;
    if(v1>v2)
    {
        std::cout << " 第一个数字大于第二个数字，输入有误。" << std::endl; 
        return 0;
    }
	while(i<=v2 )
    {
        std::cout << i << std::endl;
        
        i++;
    }
    std::cout << std::endl;
    return 0;
}
```



### for语句

每个for语句都包含两部分：循环头和循环体

循环头控制循环体的执行次数，它由三部分组成：

- 一个初始化语句（init-statement） int val = 0, 变量val作用域只在for循环内部存在，在循环结束后是不能使用的。
- 一个循环条件（condition）val <= 10，循环体每次执行前都会先检查循环条件
- 一个表达式（expression）++val，表达式在for循环体之后执行

**练习** **1.12 ** **：**下面的 for 循环完成了什么功能？sum 的终值是多少？

```c++
int sum = 0; 
for (int i = -100; i <= 100; ++i) 
	sum += i;
```

此循环将−100 到 100 之间（包含−100 和 100）的整数相加，sum 的终值是 0。

**练习** **1.13 ** **：**使用 for 循环重做 1.4.1 节中的所有练习（第 11 页）。

```c++
// 1.9 练习题 

#include <iostream>
using namespace std;
int main()
{
    int sum ;
    for(int a = 50;a<=100;a++)
    {
        cout << "a 的值" << a << endl;
        sum += a;
    }
    cout << "50 到 100 的整数相加的和等于" << sum << endl;
    return 0;

}

// 1.10 练习题

#include <iostream>
using namespace std;
int main()
{
    int a = 10 ;
    for(int a = 10;a>=0;a--)
    {
        cout << "a 的值" << a << endl;
    }
    cout << endl;
    return 0;
}

// 1.11 练习题

#include <iostream>
int main()
{
	std::cout << "input two numbers";
	std::cout << std::endl;
	int v1,v2;
	std::cin >> v1 >> v2;
    if(v1>v2)
    {
        std::cout << " 第一个数字大于第二个数字，输入有误。" << std::endl; 
        return 0;
    }
	for(int i=v1;i<=v2;i++)
    {
        std::cout << i << std::endl;
    }
    std::cout << std::endl;
    return 0;
}
```



**练习** **1.14** **：**对比 for 循环和 while 循环，两种形式的优缺点各是什么？

【解答】

- 在循环次数已知的情况下，for循环的形式显然更为简洁。

- 循环次数无法预知时，用 while 循环实现更适合。用特定条件控制循环是否执行，循环体中执行的语句可能导致循环判定条件发生变化。

**练习** **1.15 ** **：**编写程序，包含第 14 页“再探编译”中讨论的常见错误。熟悉编译器生成的错误信息。

略

###  读取数量不定的输入数据



```c++
#include <iostream>
int main()
{
    int sum = 0, value = 0;
    // 读取数据直到文件尾，计算所有读入的值之和
    while (std::cin >> value)
        sum += value; //等价于 sum = sum+value 
    std::cout << "Sum is: " << sum << std::endl;
    return 0;
}
```

运行在屏幕上随意输入数值，以分号（;）也可以按ctrl+z 结束，每个数值空格区分 ，最后结果如下：

```
# 输入数字 ： 
4.4 2 2 32;
# 最终程序输出结果：
Sum is: 4
```

sum和value是int变量，均初始化为0；

while循环条件的求值就是执行表达式

```c++
std::cin >> value
```

此表达式从标准输入读取下一个数，保存在value中。**输入运算符返回其左侧运算对象**，在本例中是std::cin。

运行步骤：

1. 此循环条件检测的是std::cin。

2. 当我们使用一个istream对象作为条件时，其效果是检测流的状态，如果流是有效的，即流未遇到错误，那么检测成功。

3. 当遇到文件结束符（end-of-file），或遇到一个无效的（例如读入的值不是一个整数），istream对象的状态会变为无效。

4. 处于无效状态的istream对象会使条件变为假。

   

>  **从键盘输入文件结束符**
>
> Windows: Ctrl+Z，然后按Enter键或Return键
>
> UNIX，Mac OS X: Ctrl+D



**再探编译**

语法错误：syntax error

类型错误：type error

声明错误：declaration error

**练习** **1.16** **：**编写程序，从 cin 读取一组数，输出其和。

```cpp
#include <iostream>
int main()
{
    float sum = 0, val = 0;
    while (std::cin >> val)
        sum += val;
    std::cout << "Sum = " << sum << std::endl;
    return 0;
}
```

### if 语句

c++提供**if语句**支持条件执行：

```cpp
#include <iostream>
int main()
{
    // currVal是我们正在统计的数；我们将读入的新值存入val
    int currVal = 0, val = 0;
    // 读取第一个数，并确保确实有数据可以处理
    if (std::cin >> currVal) {
        int cnt = 1;                // 保存我们正在处理的当前值的个数
        while (std::cin >> val) {   // 读取剩余的数
            if (val == currVal)     // 如果值相同
                ++cnt;              // 将cnt加1
            else {                  // 否则，打印前一个值的个数
                std::cout << currVal << " occurs "
                        << cnt << " times" << std::endl;
                currVal = val;      // 记住新值
                cnt = 1;            // 重置计数器
            }
        }   // while循环在这里结束
        // 记住打印文件中作后一个值的个数
        std::cout << currVal << " occurs "
                << cnt << " times" << std::endl;
    }   // 最外层的if语句在这里结束
    return 0;
}
```

执行试一试 ，这个同样支持输入多个数值 比如：` 42 43 42 32 55 55 55 100 12 42 100`

结果不太智能：

```shell
42 43 42 32 55 55 55 100 12 42 100   
42 occurs 1 times
43 occurs 1 times
42 occurs 1 times
32 occurs 1 times
55 occurs 3 times
100 occurs 1 times
12 occurs 1 times
42 occurs 1 times
```

> c++用=进行赋值，用==作为相等运算符。两个运算符都可以出现在条件中。
>
> 避免：使用=判断相等，这是错误的。

**练习** **1.17** **：**如果输入的所有值都是相等的，本节的程序会输出什么？如果没有重复值，输出又会是怎样的？

```shell
如果输入的所有值都相等，则 while 循环中的 else 分支永远不会执行，直到
输入结束，while 循环退出，循环后的输出语句打印这唯一的一个值和它出现的次
数。
若没有重复值，则 while 循环中的 if 语句的真值分支永远不会执行，每读入
一个值，都会进入 else 分支，打印它的值和出现次数 1。输入结束后，while 循
环退出，循环后的输出语句打印最后一个值和出现次数 1。
```

**练习** **1.18** **：**编译并运行本节的程序，给它输入全都相等的值。再次运行程序，输入没有重复的值。

```shell
输入：
1 1 1 1 1 
程序输出：
1 occurs 5 times 
输入：
1 2 3 4 5 
程序输出：
1 occurs 1 times 
2 occurs 1 times 
3 occurs 1 times 
4 occurs 1 times 
5 occurs 1 times
```

注意，不要忘了用 Ctrl+Z 表示输入结束。



**练习** **1.19** **：**修改你为 1.4.1 节练习 1.10（第 11 页）所编写的程序（打印一个范围内的数），使其能处理用户输入的第一个数比第二个数小的情况。

```cpp
#include <iostream>
int main()
{
    std::cout << "Enter two numbers" << std::endl;
    int v1 = 0, v2 = 0;
    std::cin >> v1 >> v2;

    if (v1 >= v2) {
        for (int val = v1; val >= v2; --val)
            std::cout << val << " ";
    }
    else {
        for (int val = v2; val >= v1; --val)
            std::cout << val << " ";
    }
    std::cout << std::endl;
    return 0;
}
```



## **1.5 类简介**

类是 c++ 最重要的特性之一，我们通过定义一个类（class）来定义自己的数据结构。

为了使用类，我们需要了解三件事情：

- 类名是什么？
- 它是在哪里定义的？
- 它支持什么操作？

以书店程序来说，假定类名为 sales_item，头文件sales_item.h 中已经定义了这个类。

### 类型：Sales_item类

作用：表示一本书的总销售额、售出册数和平均售价。

**每个类实际上都定义了一个新的类型，其类型名就是类名。**

使用定义类类型的变量

```
Sales_item item;
```

读取**Sales_item**

```cpp
#include <iostream>
#include "Sales_item.h"
int main()
{
    Sales_item book;
    // 读入ISBN号、售出的册数以及销售价格
    std::cin >> book;
    // 写入ISBN、售出的册数、总销售额和平均价格
    std::cout << book << std::endl;
    return 0;
}
```

对于不属于标准库的头文件，用**双引号（""）**。

如果输入：

```
0-201-70545-x 4 24.99 
```

则输出为：

```
0-201-70545-x 4  99.96 24.99  
```

**Sales_item**对象的加法：

```cpp
#include <iostream>
#include "Sales_item.h"
int main()
{
    Sales_item item1,item2;
    // 读入ISBN号、售出的册数以及销售价格
    std::cin >> item1 >> item2;
    // 写入ISBN、售出的册数、总销售额和平均价格
    std::cout << item1 + item2 << std::endl;
    return 0;
}
```

如果输入：

```cpp
0-201-70545-x 3 20
0-201-70545-x 2 25
```

则输出为：

```shell
0-201-70545-x 5 110 22
```

>  知识点：这里运用了对象相加“和”的概念。

**使用文件重定向**

测试程序时反复从键盘输入销售记录很麻烦

功能：允许我们将标准输入和标准输出与命名文件关联起来.

```
$ addItems <infile> outfile
```

从一个infile的文件读取销售记录，并将输出结果写入到一个名为outfile的文件中，两个文件都位于当前目录中。

运行结果：不在终端输出，结果保存在outfile文件里。



**练习** **1.20** **：**在网站 http://www.informit.com/title/0321714113 上，第 1 章的代码目录中包含了头文件 Sales_item.h。将它拷贝到你自己的工作目录中。用它编写一个程序，读取一组书籍销售记录，将每条记录打印到标准输出上。

```cpp
#include <iostream>
#include "Sales_item.h"
int main()
{
    Sales_item item;
    while (std::cin >> item) {
        std::cout << item << std::endl;
    }
    return 0;
}
```

相关文件：

1. Version_test.h

```cpp
#ifdef lround
inline long lround(double d)
{
    return (d >= 0) ?  long(d + 0.5) : long(d - 0.5);
}
#endif
```

2. Sales_item.h

```cpp
/*
 * This file contains code from "C++ Primer, Fifth Edition", by Stanley B.
 * Lippman, Josee Lajoie, and Barbara E. Moo, and is covered under the
 * copyright and warranty notices given in that book:
 * 
 * "Copyright (c) 2013 by Objectwrite, Inc., Josee Lajoie, and Barbara E. Moo."
 * 
 * 
 * "The authors and publisher have taken care in the preparation of this book,
 * but make no expressed or implied warranty of any kind and assume no
 * responsibility for errors or omissions. No liability is assumed for
 * incidental or consequential damages in connection with or arising out of the
 * use of the information or programs contained herein."
 * 
 * Permission is granted for this code to be used for educational purposes in
 * association with the book, given proper citation if and when posted or
 * reproduced.Any commercial use of this code requires the explicit written
 * permission of the publisher, Addison-Wesley Professional, a division of
 * Pearson Education, Inc. Send your request for permission, stating clearly
 * what code you would like to use, and in what specific way, to the following
 * address: 
 * 
 *     Pearson Education, Inc.
 *     Rights and Permissions Department
 *     One Lake Street
 *     Upper Saddle River, NJ  07458
 *     Fax: (201) 236-3290
*/ 

/* This file defines the Sales_item class used in chapter 1.
 * The code used in this file will be explained in 
 * Chapter 7 (Classes) and Chapter 14 (Overloaded Operators)
 * Readers shouldn't try to understand the code in this file
 * until they have read those chapters.
*/

#ifndef SALESITEM_H
// we're here only if SALESITEM_H has not yet been defined 
#define SALESITEM_H

#include "Version_test.h" 

// Definition of Sales_item class and related functions goes here
#include <iostream>
#include <string>

class Sales_item {
// these declarations are explained section 7.2.1, p. 270 
// and in chapter 14, pages 557, 558, 561
friend std::istream& operator>>(std::istream&, Sales_item&);
friend std::ostream& operator<<(std::ostream&, const Sales_item&);
friend bool operator<(const Sales_item&, const Sales_item&);
friend bool 
operator==(const Sales_item&, const Sales_item&);
public:
    // constructors are explained in section 7.1.4, pages 262 - 265
    // default constructor needed to initialize members of built-in type
#if defined(IN_CLASS_INITS) && defined(DEFAULT_FCNS)
    Sales_item() = default;
#else
    Sales_item(): units_sold(0), revenue(0.0) { }
#endif
    Sales_item(const std::string &book):
              bookNo(book), units_sold(0), revenue(0.0) { }
    Sales_item(std::istream &is) { is >> *this; }
public:
    // operations on Sales_item objects
    // member binary operator: left-hand operand bound to implicit this pointer
    Sales_item& operator+=(const Sales_item&);
    
    // operations on Sales_item objects
    std::string isbn() const { return bookNo; }
    double avg_price() const;
// private members as before
private:
    std::string bookNo;      // implicitly initialized to the empty string
#ifdef IN_CLASS_INITS
    unsigned units_sold = 0; // explicitly initialized
    double revenue = 0.0;
#else
    unsigned units_sold;  
    double revenue;       
#endif
};

// used in chapter 10
inline
bool compareIsbn(const Sales_item &lhs, const Sales_item &rhs) 
{ return lhs.isbn() == rhs.isbn(); }

// nonmember binary operator: must declare a parameter for each operand
Sales_item operator+(const Sales_item&, const Sales_item&);

inline bool 
operator==(const Sales_item &lhs, const Sales_item &rhs)
{
    // must be made a friend of Sales_item
    return lhs.units_sold == rhs.units_sold &&
           lhs.revenue == rhs.revenue &&
           lhs.isbn() == rhs.isbn();
}

inline bool 
operator!=(const Sales_item &lhs, const Sales_item &rhs)
{
    return !(lhs == rhs); // != defined in terms of operator==
}

// assumes that both objects refer to the same ISBN
Sales_item& Sales_item::operator+=(const Sales_item& rhs) 
{
    units_sold += rhs.units_sold; 
    revenue += rhs.revenue; 
    return *this;
}

// assumes that both objects refer to the same ISBN
Sales_item 
operator+(const Sales_item& lhs, const Sales_item& rhs) 
{
    Sales_item ret(lhs);  // copy (|lhs|) into a local object that we'll return
    ret += rhs;           // add in the contents of (|rhs|) 
    return ret;           // return (|ret|) by value
}

std::istream& 
operator>>(std::istream& in, Sales_item& s)
{
    double price;
    in >> s.bookNo >> s.units_sold >> price;
    // check that the inputs succeeded
    if (in)
        s.revenue = s.units_sold * price;
    else 
        s = Sales_item();  // input failed: reset object to default state
    return in;
}

std::ostream& 
operator<<(std::ostream& out, const Sales_item& s)
{
    out << s.isbn() << " " << s.units_sold << " "
        << s.revenue << " " << s.avg_price();
    return out;
}

double Sales_item::avg_price() const
{
    if (units_sold) 
        return revenue/units_sold; 
    else 
        return 0;
}
#endif

```

**练习** **1.21** **：**编写程序，读取两个 ISBN 相同的 Sales_item 对象，输出它们的和。

```cpp
#include <iostream>
#include "Sales_item.h"
int main()
{
    Sales_item item1,item2;
    // 读入ISBN号、售出的册数以及销售价格
    std::cin >> item1 >> item2;
    // 写入ISBN、售出的册数、总销售额和平均价格
    std::cout << item1 + item2 << std::endl;
    return 0;
}
```

**练习** **1.22** **：**编写程序，读取多个具有相同 ISBN 的销售记录，输出所有记录的和。

```cpp
#include <iostream>
#include "Sales_item.h"
int main()
{
    Sales_item total, trans;
    std::cout << "请输入几条 ISBN 相同的销售记录："
              << std::endl;
    if (std::cin >> total) {
        while (std::cin >> trans)
            if (compareIsbn(total, trans)) // ISBN 相同
                total = total + trans;
            else { // ISBN 不同
                std::cout << "ISBN 不同" << std::endl;
                return -1;
            }
        std::cout << "汇总信息：ISBN、售出本数、销售额和平均售价为 "
                  << total << std::endl;
    }
    else {
        std::cout << "没有数据" << std::endl;
        return -1;
    }
    return 0;
}
```



### **初识成员函数**



```cpp
#include <iostream>
#include "Sales_item.h"
int main()
{
    Sales_item itemSum;
    if (std::cin >> itemSum) {
        Sales_item item;
        while (std::cin >> item) {
            itemSum += item;
        }
    }
    
    std::cout << itemSum << std::endl;
}
```

成员函数是定义为类的一部分的函数，也被称为方法。

通常以类对象的名义来调用成员函数：Item.isbn()。即使用点运算符(.)

**练习** **1.23** **：**编写程序，读取多条销售记录，并统计每个 ISBN（每本书）有几条销售记录。

```cpp
#include <iostream>
#include "Sales_item.h"
int main()
{
    Sales_item trans1, trans2;
    int num = 1;
    std::cout << "请输入若干销售记录："
              << std::endl;
    if (std::cin >> trans1) {
        while (std::cin >> trans2)
        if (compareIsbn(trans1, trans2)) // ISBN 相同
            num++;
        else { // ISBN 不同
            std::cout << trans1.isbn() << "共有"
                      << num << "条销售记录" << std::endl;
            trans1 = trans2;
            num = 1;
        }
        std::cout << trans1.isbn() << "共有"
                  << num << "条销售记录" << std::endl;
    }
    else {
        std::cout << "没有数据" << std::endl;
        return -1;
    }
    return 0;
}
```

**练习** **1.24** **：**输入表示多个 ISBN 的多条销售记录来测试上一个程序，每个 ISBN的记录应该聚在一起。

【解答】

在网站 http://www.informit.com/title/0321714113 上，第 1 章的代码目录中包含了一些数据文件，可以将这些文件重定向到此程序进行测试，也可自己创建销售记录文件进行测试。



**练习** **1.25** **：**借助网站上的 Sales_item.h 头文件，编译并运行本节给出的书店程序。



## **1.6 问题集**

1. 四个标准输入输出流是什么
2. cout 和 cerr 的两点区别
3. 缓冲区有什么作用？可以通过什么刷新缓冲区
4. while(cin>>value)什么情况下会停止
5. windows 的文件结束符是什么

**回答**

1. cin、cout、cerr、clog
2. cout 可重定向，通过缓冲区；cerr 不可重定向，不通过缓冲区
3. 缓冲区能减少刷屏的次数，每个 endl 都会刷新一次缓冲区
4. 遇到文件结束符或输入错误
5. **先 ctrl+z 后 enter** 

## **1.7 参考资料**

[C++ Primer学习笔记 第一章 开始](https://zhuanlan.zhihu.com/p/414900872)

