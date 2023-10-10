## 10.1 栈和队列



使用数组实现栈：

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

使用链表实现栈

```python

```



## 10.2 链表

```
ADT 线性表（List）
Data
	 线性表的数据对象集合为（a1,a2,...,an）,每个元素的类型均为DataType。
	 其中，除第一个元素a1外，每一个元素有且只有一个直接前驱元素。
	 除了最后一个元素an外，每一个元素有且只有一个直接后继元素。
	 数据元素之间的关系是一对一的关系。
Operation
	InitList(*L):		初始化操作，建立一个空的线性表L。
	ListEmpty(L):		若线性表为空，返回true,否则返回false。
	ClearList(*L): 		将线性表清空。
	GetElem(L,i,*e):	将线性表L中第i个位置元素值返回给e。
	LocateElem(L,e):    在线性表L中查找与给定e相等的元素，
						如果查找成功，返回该元素在表中序号表示成功。
```

