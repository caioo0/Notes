**问题**

1. 使用范围 for 语句注意什么？
2. try 语句块的使用方式
3. C++ 定义了哪些异常类型

**回答**

1. 如果要写元素的话必须要使用引用方式 auto&，但是**建议不论何时都使用引用，且当不需要写时使用常量引用。**
2. throw 放在 try 块内，catch 用来捕获异常，可以使用省略号来捕获所有的异常类型。如果抛出了异常而未使用 catch 捕获，系统会调用 terminate 终止程序的运行。
3. 如 exceptIon, bad_alloc, bad_cast，runtime_error, logic_error 等。定义在头文件 exception, new, type_info, stdexcept 等头文件中。

**第5章 语句**

**5.1 简单语句**

**表达式语句**

一个表达式加上分号就是**表达式语句**。表达式的语句执行表达式并丢弃掉求值结果

​                ival + 3;//一条没有实际用处的表达式语句 cout << ival;//一条有用的表达式语句              

**空语句**

空语句是最简单的语句，只有一个分号

​                ;//空语句              

用处：用在语法上需要一条语句但逻辑上不需要的地方。比如当循环的全部工作在条件部分就可以完成时。

使用空语句应该加上注释。

**复合语句（块）**

花括号括起来的语句和声明序列都是**复合语句（块）**。一个块就是一个作用域

空块的作用等价于空语句。

**5.2 语句作用域**

可以在 if、switch、while、for 语句的控制结构内定义变量。

常见的语句有条件语句、循环语句、跳转语句三种。

**5.3 条件语句**

两种：if 语句和 switch 语句

**5.3.1 if语句**

if 语句有两种形式，一种有 else 分支，另一种没有。

c++ 规定 else 与离他最近的尚未匹配的 if 匹配。注意不要搞错。

使用 if 语句最好在所有的 if 和 else 之后都用花括号。

**5.3.2 switch语句**

switch 语句计算一个**整型表达式**的值，然后根据这个值从几条执行路径中选择一条。

case 关键字和它对应的值一起被称为 case 标签，case 标签必须为**整型常量表达式**。

**default** 也是一种特殊的 case 标签。

​                switch(ch){    case 'a': ++aCnt; break;    case 'b': ++bCnt; break; }              

注意：如果 switch 条件值于某个 case 标签匹配成功后，程序将从该 case 标签一直执行到 switch 末尾或遇到 break。

一条 case 后可以跟多条语句，不必用花括号括起来。

一般在每个 case标签后都有一条 break 语句。如果需要两个或多个值共享同一组操作，可以故意省略掉 break 语句。

c++ 程序的形式比较自由，case 标签之后不一定要换行。

​                switch(ch){    case 'a': case 'b':        ++Cnt;        break;     }              

一般不要省略 case 分支最后的 break 语句。如果没有 break 语句，最好注释一下。

如果没有任何一个 case 标签匹配 switch 表达式的值，就执行 default 分支。

即使不准备在 default 下做任何工作，最好也定义一个 default 标签。

如果要在 case 分支定义并初始化变量，应该定义在块内以约束其作用域。

**5.4 迭代语句**

三种：while 语句、for 语句（包括范围 for 语句）、do while 语句

**5.4.1 while语句**

while 的条件不能为空。条件部分可以是一个表达式或**带初始化的变量声明**。

定义在 while 条件部分或循环体内的变量每次迭代都会重新创建和销毁。

while 适合不知道循环多少次的情况。

**5.4.2 传统的for语句**

​                for(init-statement; condition; expression)    statement;              

init-statement 可以是声明语句、表达式语句或空语句。init-statement 可以定义多个对象，但是只能有一条声明语句。

expression 在每次循环之后执行。

for 语句头能省略掉三者中的任意一个或全部。

省略 condition 等于条件恒为 true。

**5.4.3 范围for语句**

范围 for 语句用来遍历容器或其他序列的所有元素。

​                for(declaration : expression)    statement              

expression 表示的必须是一个序列，可以是花括号括起来的初始值列表。这些序列的共同的是都可以返回迭代器的 begin 和 end 成员。

declaration 定义一个能从序列中元素转换过来的**变量（不是迭代器）**。最简单的方法是使用 auto 类型说明符。

如果需要对容器中的元素执行写操作，必须**将循环变量声明成引用类型**。

**循环变量可以声明为对常量的引用，不需要写时最好都声明为常量引用**

每次迭代都会**重新定义**循环控制变量，并将其初始化为序列的下一个值。

范围 for 语句不能改变序列的元素数量。因为其预存了 end() 的值，改变元素数量后 end() 的值就可能失效了。

**5.4.4 dowhile语句**

do while 语句与 while 语句的唯一区别就是它先执行循环体后检查条件。即至少执行一次循环。

注意：do while 后**不要忘了加分号。**

因为 condition 在循环体后面，所以 condition 使用的变量应该定义在循环体外面。

**5.5 跳转语句**

四种：break、continue、goto、return

**5.5.1 break语句**

break 语句终止离它最近的 while、do while、for 或 switch 语句，并从这些语句之后的第一条语句开始执行。

break 语句只能出现在迭代语句或 switch 内部。

**5.5.2 continue语句**

continue 语句终止最近的循环中的当前迭代并开始下一次迭代。

continue 适用范围比 break 少了一个 switch

**5.5.3 goto语句**

goto 语句的作用是从 goto 语句无条件跳转到**同一函数内**的另一条语句。

​                label: int a = 1; goto label;              

label 是用于标识一条语句的标示符

标签标示符独立于变量或其他标示符的名字，标签标示符可以和程序中其他实体的标示符使用同一个名字而不会相互干扰。

如果 goto 语句跳回了一条变量的定义之前意味着系统将会销毁该变量，然后重新创建它。

**不要使用 goto**，它会令程序又难理解又难修改。

**5.6 try语句块和异常处理**

异常是指存在于运行时的反常行为，典型的异常有失去数据库连接和遇到意外输入等。处理异常可能是设计系统时最难的一部分。

当程序检测到一个无法处理的问题时，就需要**异常处理**，此时检测到问题的部分应该发出检测信号。

如果程序里有可能引发异常的代码，也应该有专门的代码处理问题。

C++ 的异常处理机制为**异常检测**和**异常处理**提供支持，它包括：

1. **throw 表达式：**异常检测部分使用 throw 表达式来表示遇到了无法处理的问题。称为 throw 引发了异常。
2. **try 语句块：**异常处理部分使用 try 语句块处理异常。try 语句块以关键字 try 开始，以一个或多个 catch 子句结束。
3. **一套异常类：**用于在 throw 表达式和相关的 catch 子句间传递异常的具体信息。

**5.6.1 throw 表达式**

throw 表达式包含关键字 throw 和紧随其后的一个表达式，表达式的类型就是抛出的异常类型。

即 throw 后面跟一个异常类型的对象（必须同时使用 string 或 C 风格字符串对其初始化）。

​                throw runtime_error("Data must be same as size");//使用 throw 表达式抛出一个运行时错误。              

**5.6.2 try语句块**

跟在 try 块后面的是一个或多个 catch 子句。catch 子句包括三部分：关键字 catch、括号内一个异常类型的对象的声明（叫做异常声明）、一个块。

当 try 语句块中抛出了一个异常，如果该异常类型与 catch 子句括号中的异常类型相同，就会执行该 catch 子句。

catch 一旦完成，程序就跳转到 try 语句块最后一个 catch 子句之后的那条语句继续执行。

在 catch 后面的括号里使用省略号(...)可以让 catch 捕获所有类型的异常。

每个标准库异常类都有一个 **what 成员函数**，它没有参数，返回初始化该对象时所用的 C 风格字符串。

​                try{   throw runtime_error("Data must be same as size");//try 语句块抛出了一个异常 } catch(runtime_error err)//在 catch 后面的括号中声明了一个“runtime_error”类型的对象，与 try 抛出的异常类型相同，接下来执行此子句。 {    cout << err.what();//输出 "Data must be same as size" }//              

**函数在寻找处理代码的过程中退出**

throw 语句可能出现在嵌套的 try 语句块中或在 try 语句块中调用的某个函数内。当异常被抛出，程序会**从内到外一层层寻找相应类型的 catch 子句。**如果最后还是没找到，系统会**调用 terminate 函数并终止当前程序的执行。**

如果 throw 语句外就没有 try 语句块，也会执行 terminate 函数。

理解：异常中断了程序的正常流程。当发生异常，程序执行到一半就中断了，可能会存在如资源没有正常释放，对象没有处理完成等情况。异常安全的代码要求在异常发生时能正确执行清理工作。这个非常困难。

**5.6.3 标准异常**

C++ 标准库定义了一组异常类，用于报告标准库函数遇到的问题。他们定义在 4 个头文件中。

定义在 **stdexcept** 头文件中的类型必须使用 string 对象或 C 风格字符串来初始化他们。其他 3 个头文件中的 3 中类型则只能默认初始化，不能提供初始值。

异常类型只有一个 what 成员函数，该函数没有参数，返回是一个 C 风格字符串的指针，目的是提供关于异常的文本信息。

对于无初始值的异常类型，what 返回的内容由编译器决定，有初始值的返回初始值。

​                'exception头文件' exception      // 异常类 exception 是最通用的异常类。它只报告异常的发生，不提供额外信息。 'new头文件' bad_alloc      // 异常类 bad_alloc。在使用 new 分配动态内存失败时抛出 'type_info头文件' bad_cast      // 异常类型 bad_cast。经常发生在使用 dynamic_cast 时发生。 'stdexcept头文件' exception runtime_error    // 只有在运行时才能检测出的问题 range_error     // 运行时错误：生成的结果超出了有意义的值域范围 overflow_error   // 运行时错误：计算上溢 underflow_error   // 运行时错误：计算下溢 logic_error     // 程序逻辑错误 domain_error    // 逻辑错误：参数对象的结果值不存在 invalid_argument  // 逻辑错误：无效参数 length_error    // 逻辑错误：试图创建一个超出该类型最大长度的对象 out_of_range    // 逻辑错误：使用一个超出有效范围的值              

上面的异常类之间存在继承关系，其中 exception 是所有其他类的基类，总的继承关系如下图

​    ![0](https://note.youdao.com/yws/public/resource/80ef131f62e5733164aa3fd1f11c9b29/xmlnote/8A824B95651E4A219BAB42B0D3803B49/33842)

例子

​                void StrBlob::check(size_type i, const string& msg) { if (i >= data->size())        throw out_of_range(msg); }              