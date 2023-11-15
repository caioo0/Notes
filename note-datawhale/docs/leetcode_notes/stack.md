# 堆栈与单调栈
> 关于笔记，主要来自[datawhale-Leetcode算法笔记](https://datawhalechina.github.io/leetcode-notes/#/ch01/01.01/01.01.02-Algorithm-Complexity)

## 一、 堆栈

> **堆栈（Stack）**：简称为栈。一种线性表数据结构，是一种只允许在表的一端进行插入和删除操作的线性表。

栈有两种基本操作：**插入操作** 和 **删除操作**

- 插入操作又称为入栈或进栈
- 删除操作又称为出战或退栈

![image-20231022200407798](.\img\image-20231022200407798.png)

**「栈顶（top）」**: 允许插入和删除的一端；另一端则称为 **「栈底（bottom）」**。

**「空栈」**:当表中没有任何数据元素的栈。

简单来说，栈是一种 **「后进先出（Last In First Out）」** 的线性表，简称为 **「LIFO 结构」**。

### 1. 堆栈的顺序存储与链式存储

栈有两种存储表示方式：**顺序栈和链式栈**

- **顺序栈**：即堆栈的顺序存储结构。利用一组地址连续的存储单元依次存放自栈底到栈顶的元素，同时使用指针 `top` 指示栈顶元素在顺序栈中的位置。
- **链式栈**：即堆栈的链式存储结构。利用单链表的方式来实现堆栈。栈中元素按照插入顺序依次插入到链表的第一个节点之前，并使用栈顶指针 `top` 指示栈顶元素，`top` 永远指向链表的头节点位置。

#### 1.1 堆栈的基本操作

堆栈的基本操作如下：

- 初始化空栈
- 判断栈是否为空
- 判断栈是否已满
- 插入元素（进栈）
- 删除元素
- 获取栈顶元素

#### 1.2 堆栈的顺序存储实现

```python
# -*- coding: UTF-8 -*-
"""
参考网址： https://zhuanlan.zhihu.com/p/97881563
"""

class Stack(object):
    def __init__(self):
        """
        创建一个Stack类
        对栈进行初始化参数设计
        """
        self.stack = [] # 存放元素栈

    def push(self,data):
        """
        压入push: 讲新元素放在栈顶
        当新元素入栈时，栈顶上移，新元素放在栈顶。
        :param data:
        :return: null
        """
        self.stack.append(data)

    def pop(self):
        """
        弹出pop: 从栈顶移出一个数据
        - 栈顶元素拷贝出来
        - 栈顶下移
        - 拷贝出来的栈顶作为函数返回值
        :return:
        """
        # 判断是否为空栈
        if self.stack:
            return self.stack.pop()
        else:
            raise IndexError("从空栈执行弹栈操作")

    def peek(self):
        """
        查看栈顶的元素
        :return:
        """
        # 判断栈是否为空
        if self.stack:
            return self.stack[-1]

    def is_empty(self):
        """
        判断栈是否为空
        :return:
        """

        # 栈为空时，self.stack为True,再取反，为False
        return not bool(self.stack)

    def size(self):
        """
        返回栈的大小
        :return:
        """
        return len(self.stack)

```

#### 1.3 堆栈的链式存储实现

使用链表实现：

```python
class Node:
    def __init__(self, value):
        self.value = value
        self.next = None
        
class Stack:
    # 初始化空栈
    def __init__(self):
        self.top = None
    
    # 判断栈是否为空
    def is_empty(self):
        return self.top == None
    
    # 入栈操作
    def push(self, value):
        cur = Node(value)
        cur.next = self.top
        self.top = cur
    
    # 出栈操作
    def pop(self):
        if self.is_empty():
            raise Exception('Stack is empty')
        else:
            cur = self.top
            self.top = self.top.next
            del cur
    
    # 获取栈顶元素
    def peek(self):
        if self.is_empty():
            raise Exception('Stack is empty')
        else:
            return self.top.value

```

### 2. 堆栈的应用

堆栈是算法和程序中最常用的辅助结构，其的应用十分广泛。堆栈基本应用于两个方面：

- 使用堆栈可以很方便的保存和取用信息，因此长被用作算法和程序中的辅助存储结构，临时保存信息，供后面操作中使用。
  - 例如：操作系统中的函数调用栈，浏览器中的前进、后退功能。
- 堆栈的后进先出规则，可以保证特定的存取顺序。
  - 例如：翻转一组元素的顺序、铁路列车车辆调度。

### 3. 堆栈练习题

- #### [20. 有效的括号 - 力扣（LeetCode）](https://leetcode.cn/problems/valid-parentheses/)

- #### [227. 基本计算器 II - 力扣（LeetCode）](https://leetcode.cn/problems/basic-calculator-ii/)

- #### [0155. 最小栈](https://leetcode.cn/problems/min-stack/)

- #### [[0150. 逆波兰表达式求值](https://leetcode.cn/problems/evaluate-reverse-polish-notation/)

- #### [0394. 字符串解码](https://leetcode.cn/problems/decode-string/)

- #### [0946. 验证栈序列](https://leetcode.cn/problems/validate-stack-sequences/)

## 二、单调栈

> **单调栈（Monotone Stack）**：一种特殊的栈。在栈的「先进后出」规则基础上，要求「从 **栈顶** 到 **栈底** 的元素是单调递增（或者单调递减）」。其中满足从栈顶到栈底的元素是单调递增的栈，叫做「单调递增栈」。满足从栈顶到栈底的元素是单调递减的栈，叫做「单调递减栈」。

### 1. 单调递增栈

### 2. 单调递减栈

### 3. 单调栈适用场景

### 4. 单调栈模板

### 5. 单调栈应用

### 6. 单调栈练习题

- #### [0496. 下一个更大元素 I](https://leetcode.cn/problems/next-greater-element-i/)

- #### [0739. 每日温度](https://leetcode.cn/problems/daily-temperatures/)

- #### [0316. 去除重复字母](https://leetcode.cn/problems/remove-duplicate-letters/)

