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



