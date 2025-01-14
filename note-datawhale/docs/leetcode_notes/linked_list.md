# 链表
> 关于笔记，主要来自[datawhale-Leetcode算法笔记](https://datawhalechina.github.io/leetcode-notes/#/ch01/01.01/01.01.02-Algorithm-Complexity)

## 1.1 链表基础知识

「链表 linked list」是一种线性数据结构，其中的每个元素都是一个节点对象，各个节点通过“引用”相连接。引用记录了下一个节点的内存地址，通过它可以从当前节点访问到下一个节点。

链表的设计使得各个节点可以被分散存储在内存各处，它们的内存地址是无须连续的。

![image-20231007145627128](.\img\image-20231007145627128.png)
$$
链表定义和存储方式
$$
链表的组成单位是「节点 node」对象。每个节点都包含两项数据：节点的“值”和指向下一节点的“引用”。

- 链表的首个节点被称为“头节点”，最后一个节点被称为“尾节点”。
- 尾节点指向的是“空”，它在 Java、C++ 和 Python 中分别被记为 null、nullptr 和 None 。
- 在 C、C++、Go 和 Rust 等支持指针的语言中，上述的“引用”应被替换为“指针”。

链表节点 `ListNode` 除了包含值，还需额外保存一个引用（指针）。在相同数据量下，**链表比数组占用更多的内存空间**。

```python
class ListNode:
	"""链表节点类"""
	def __init__(self,val:int):
		self.val:int = val 		           # 节点值
        self.next:ListNode | None = None   # 指向下一节点的引用
```



### **1. 单向链表**

- 每个节点包含一个数据元素和一个指向下一个节点的指针，具体实现如下：

```python
# -*- coding:utf-8 -*-
"""
@author: caioo0
@file: singlelinkedlist.py
@time: 2023/10/07
"""
class Node:
    # 定义节点类，每个节点包含数据和指向下一个节点的指针
    def __init__(self, data):
        self.data = data  # 节点的数据
        self.next = None  # 指向下一个节点的指针，初始化为 None

class SingleLinkList:
    # 继续添加其他方法  
    def __init__(self):
        self.head = None

    def add(self, data):
        # 添加节点的方法，如果链表为空，则将新节点设置为头指针  
        # 否则，遍历链表直到找到最后一个节点，并将新节点添加到链表的末尾  
        new_node = Node(data)  # 创建新节点  
        if not self.head:  # 如果链表为空  
            self.head = new_node  # 将新节点设置为头指针  
        else:
            current = self.head  # 定义指向当前节点的变量  
            while current.next:  # 遍历链表直到找到最后一个节点  
                current = current.next  # 移动指针到下一个节点  
            current.next = new_node  # 将新节点添加到链表的末尾  

    def remove(self, data):
        # 删除节点的方法，首先找到前一个节点，然后将当前节点的指针指向下一个节点  
        if not self.head:  # 如果链表为空  
            return  # 直接返回  
        if self.head.data == data:  # 如果头节点就是要删除的节点  
            self.head = self.head.next  # 将头指针指向下一个节点  
            return  # 直接返回  
        current = self.head  # 定义指向当前节点的变量  
        while current.next:  # 遍历链表直到找到最后一个节点或找到要删除的节点  
            if current.next.data == data:  # 如果找到了要删除的节点  
                current.next = current.next.next  # 将当前节点的指针指向下一个节点的下一个节点  
                return  # 直接返回  
            current = current.next  # 移动指针到下一个节点  

    def search(self, data):
        # 查找节点的方法，遍历链表，如果找到了目标节点则返回True，否则返回False  
        current = self.head  # 定义指向当前节点的变量  
        while current:  # 遍历链表  
            if current.data == data:  # 如果找到了目标节点  
                return True  # 返回True  
            current = current.next  # 移动指针到下一个节点  
        return False  # 如果遍历完链表都没有找到目标节点，返回False  

    def display(self):
        # 遍历链表并打印每个节点的数据  
        current = self.head  # 定义指向当前节点的变量  
        while current:  # 遍历链表  
            print(current.data, end=' ')  # 打印当前节点的数据  
            current = current.next  # 移动指针到下一个节点  
        print()  # 打印完链表后换行  

    def insert_after_node(self, prev_node_data, new_data):
        # 在给定节点后插入新节点的操作  
        new_node = Node(new_data)  # 创建新节点  
        if not self.head:  # 如果链表为空  
            print("链表为空，无法插入节点")  # 打印错误信息  
            return  # 直接返回  
        if self.head.data == prev_node_data:  # 如果头节点就是要插入的位置  
            self.head = new_node  # 将新节点设置为头指针  
            return  # 直接返回  
        current = self.head  # 定义指向当前节点的变量  
        while current and current.next.data != prev_node_data:  # 遍历链表找到前一个节点  
            current = current.next  # 移动指针到下一个节点  
        if not current:  # 如果遍历完链表都没有找到前一个节点  
            print("未找到指定的节点，无法插入新节点")  # 打印错误信息  
            return  # 直接返回  
        current.next = new_node  # 将新节点添加到前一个节点的后面  


    def delete_node(self, key):
        # 根据键值删除节点的操作
        cur = self.head
        if cur and cur.data == key:  # 如果头节点就是要删除的节点
            self.head = cur.next  # 将头指针指向下一个节点
            cur = None  # 销毁当前节点
            return
        prev = None  # 保存前一个节点
        while cur and cur.data != key:  # 遍历链表找到要删除的节点
            prev = cur
            cur = cur.next
        if not cur:  # 如果遍历完链表都没有找到要删除的节点
            print("链表中没有键值为 %s 的节点" % key)
            return
        prev.next = cur.next  # 将前一个节点的指针指向当前节点的下一个节点
        cur = None  # 销毁当前节点

    def get_node(self, index):
        # 根据索引获取节点数据
        cur = self.head
        count = 0
        while cur:
            if count == index:
                return cur.data
            cur = cur.next
            count += 1
        print("链表中没有索引为 %d 的节点" % index)
        return None

    def append(self, data):
        # 在链表末尾添加新节点的操作
        new_node = Node(data)
        if not self.head:
            self.head = new_node
            return
        last = self.head
        while last.next:
            last = last.next
        last.next = new_node

    def prepend(self, data):
        # 在链表头部添加新节点的操作
        new_node = Node(data)
        new_node.next = self.head
        self.head = new_node

    def print_list(self):
        # 打印链表所有节点数据的操作
        node = self.head
        print("-------")
        while node:
            print(node.data, end="")
            node = node.next
        print("\n--------")

    def length(self):
        """链表长度"""
        node = self.head
        count = 0
        while node:
            count += 1
            node = node.next
        return count

    def insert(self, pos, item):
        """指定位置插入元素，第一个元素位置为0"""
        if pos <= 0:
            self.add(item)
        elif pos > self.length() - 1:
            self.append(item)
        else:
            pre = self.head
            count = 0
            while count < pos - 1:
                count += 1
                pre = pre.next
            node = Node(item)
            node.next = pre.next
            pre.next = node

if __name__ == '__main__':
    single_link_list = SingleLinkList()
    single_link_list.add('元素1')
    single_link_list.add('元素2')

    print(">>遍历链表：")
    single_link_list.print_list()       # 元素2	元素1
    print(single_link_list.length())    # 2
    print(">>指定位置插入元素后遍历链表：")
    single_link_list.insert(1, '元素n')
    single_link_list.print_list()           # 元素2	元素n	元素1
    print(">>查找元素位置：")
    print(single_link_list.search('元素n'))   # True
    print(">>移除元素后遍历链表：")
    single_link_list.remove('元素1')
    single_link_list.print_list()            # 元素2	元素n

```

### **2. 双向链表**

- 每个节点包含一个数据元素，2个指针指向上一个和下一个节点，具体实现如下：

```python
#!usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author: caioo0
@file: doublelinkedlist.py
@time: 2023/10/07
"""

class Node(object):
    """双向链表节点"""

    def __init__(self, item):
        # item 存放数据元素
        self.item = item
        # next 存放下一个节点的标识
        self.next = None
        # prev 存放上一个节点的标识
        self.prev = None


class DLinkList:
    """双向链表操作"""
    def __init__(self, node=None):
        self.__head = node

    def is_empty(self):
        """链表是否为空"""
        return self.__head is None

    def length(self):
        """链表长度"""
        cur = self.__head
        count = 0
        while cur is not None:
            count += 1
            cur = cur.next
        return count

    def travel(self):
        """遍历并打印链表元素"""
        cur = self.__head
        while cur is not None:
            print(cur.item, end='\t')
            cur = cur.next
        print()

    def add(self, item):
        """链表头部插入元素"""
        node = Node(item)
        node.next = self.__head
        self.__head = node
        if node.next:
            node.next.prev = node

    def append(self, item):
        """链表尾部插入元素"""
        node = Node(item)
        if self.is_empty():
            self.__head = node
        else:
            cur = self.__head
            while cur.next is not None:
                cur = cur.next
            cur.next = node
            node.prev = cur

    def insert(self, pos, item):
        """指定位置之前插入元素"""
        if pos <= 0:
            self.add(item)
        elif pos >= self.length():
            self.append(item)
        else:
            cur = self.__head
            count = 0
            while count < pos:
                count += 1
                cur = cur.next
            node = Node(item)
            node.next = cur
            cur.prev.next = node
            node.prev = cur.prev
            cur.prev = node

    def search(self, item):
        """查找元素"""
        cur = self.__head
        while cur is not None:
            if cur.item == item:
                return True
            else:
                cur = cur.next
        return False

    def remove(self, item):
        """删除元素"""
        cur = self.__head
        pre = None
        while cur is not None:
            if cur.item == item:
                if cur == self.__head:   # 头部
                    self.__head = cur.next
                    if cur.next:
                        cur.next.prev = None
                else:
                    cur.next.prev = cur.prev
                    cur.prev.next = cur.next
                return True
            cur = cur.next
        return False


if __name__ == '__main__':
    dl = DLinkList()
    print(dl.is_empty())   # True

    dl.add('元素1')
    dl.add('元素2')         
    dl.append('元素3')
    dl.append('元素4')    
    dl.travel()            # 元素2	元素1	元素3	元素4
    print(dl.length())     # 4

    dl.insert(1, '元素n')   
    dl.travel()            # 元素2	元素n	元素1	元素3	元素4

    print(dl.search('元素n'))  # True

    dl.remove('元素1')  
    dl.travel()            # 元素2	元素n	元素3	元素4



```



### **3. 单向循环链表**

```python
#!usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author: caioo0
@file: cyclelinkedlist.py
@time: 2023/10/07
"""

class Node(object):
    """链表节点"""

    def __init__(self, item):
        # item 存放数据元素
        self.item = item
        # next 存放下一个节点的标识
        self.next = None


class CycleSingleLinkList:
    """单向循环链表操作"""
    def __init__(self, node=None):
        self.__head = node

    def is_empty(self):
        """链表是否为空"""
        return self.__head is None

    def length(self):
        """链表长度"""
        if self.is_empty():
            return 0
        cur = self.__head
        count = 1
        while cur.next != self.__head:
            count += 1
            cur = cur.next
        return count

    def travel(self):
        """遍历并打印链表元素"""
        if self.is_empty():
            return
        cur = self.__head
        while cur.next != self.__head :
            print(cur.item, end='\t')
            cur = cur.next
        print(cur.item, end='\t')
        print()

    def add(self, item):
        """链表头部插入元素"""
        node = Node(item)
        if self.is_empty():
            self.__head = node
            node.next = node
        # 寻找尾节点
        else:
            cur = self.__head
            while cur.next != self.__head:
                cur = cur.next
            node.next = self.__head
            self.__head = node
            cur.next = self.__head

    def append(self, item):
        """链表尾部插入元素"""
        node = Node(item)
        if self.is_empty():
            self.__head = node
            node.next = node
        else:
            cur = self.__head
            while cur.next != self.__head:
                cur = cur.next
            # 退出循环时，cur指向尾节点
            cur.next = node
            node.next = self.__head

    def insert(self, pos, item):
        """指定位置插入元素，第一个元素位置为0"""
        if pos <= 0:
            self.add(item)
        elif pos >= self.length():
            self.append(item)
        else:
            cur = self.__head
            count = 0
            while count < pos-1:
                count += 1
                cur = cur.next
            node = Node(item)
            node.next = cur.next
            cur.next = node

    def remove(self, item):
        """删除元素"""
        if self.is_empty():  # 链表为空
            return
        cur = self.__head
        pre = None
        while cur.next != self.__head:   # 非最后一个节点
            if cur.item == item:
                if cur == self.__head:   # 第一个元素即为要删除的元素
                    rear = self.__head
                    while rear.next != self.__head:
                        rear = rear.next
                    self.__head = cur.next
                    rear.next = self.__head
                else:                    # 非第一个和最后一个元素
                    pre.next = cur.next
                return
            else:
                pre = cur
                cur = cur.next
        if cur.item == item:             # 最后一个节点
            if cur == self.__head:  # 链表只有一个节点
                self.__head = None
            else:
                pre.next = self.__head
            return

    def search(self, item):
        """查找元素"""
        if self.is_empty():
            return False
        cur = self.__head
        while cur.next != self.__head:
            if cur.item == item:
                return True
            cur = cur.next
        # 在最后一个元素退出循环
        if cur.item == item:
            return True
        return False

    # # 单向循环链表-约瑟夫环
    # def josephu(self, k=None):
    #     count = 1
    #     cur = self.__head
    #     while not self.is_empty():
    #         if count == k:
    #             print(cur.item, end='\t')
    #             self.remove(cur.item)
    #             count = 0
    #         cur = cur.next
    #         count += 1


if __name__ == '__main__':
    single_link_list = CycleSingleLinkList()
    single_link_list.add('元素1')
    single_link_list.add('元素2')
    single_link_list.append('元素3')
    single_link_list.append('元素4')
    single_link_list.travel()            # 元素2	元素1	元素3	元素4
    print(single_link_list.length())     # 4

    single_link_list.insert(1, '元素n')
    single_link_list.travel()            # 元素2	元素n	元素1	元素3	元素4

    print(single_link_list.search('元素n'))   # True

    single_link_list.remove('元素1')
    single_link_list.travel()            # 元素2	元素n	元素3	元素4



```

## 1.2 链表基础练习题

### [1.](https://datawhalechina.github.io/leetcode-notes/#/ch02/02.01/02.01.02-Exercises?id=_1-0707-设计链表)[0707. 设计链表](https://leetcode.cn/problems/design-linked-list/)

### [2.](https://datawhalechina.github.io/leetcode-notes/#/ch02/02.01/02.01.02-Exercises?id=_2-0206-反转链表)[0206. 反转链表](https://leetcode.cn/problems/reverse-linked-list/)

### [3.](https://datawhalechina.github.io/leetcode-notes/#/ch02/02.01/02.01.02-Exercises?id=_3-0203-移除链表元素)[0203. 移除链表元素](https://leetcode.cn/problems/remove-linked-list-elements/)

### [4.](https://datawhalechina.github.io/leetcode-notes/#/ch02/02.01/02.01.03-Exercises?id=_1-0328-奇偶链表)[0328. 奇偶链表](https://leetcode.cn/problems/odd-even-linked-list/)

### [5.](https://datawhalechina.github.io/leetcode-notes/#/ch02/02.01/02.01.03-Exercises?id=_2-0234-回文链表)[0234. 回文链表](https://leetcode.cn/problems/palindrome-linked-list/)

### [6.](https://datawhalechina.github.io/leetcode-notes/#/ch02/02.01/02.01.03-Exercises?id=_3-0138-复制带随机指针的链表)[0138. 复制带随机指针的链表](https://leetcode.cn/problems/copy-list-with-random-pointer/)



## 2.1 链表排序

### 1. 链表排序介绍

适合链表排序与不适合链表排序的算法：

- 适合链表的排序算法：**冒泡排序**、**选择排序**、**插入排序**、**归并排序**、**快速排序**、**计数排序**、**桶排序**、**基数排序**。
- 不适合链表的排序算法：**希尔排序**。
- 可以用于链表排序但不建议使用的排序算法：**堆排序**。

### 2. 链表冒泡排序

### 3. 链表选择排序

### 4. 链表插入排序

### 5. 链表归并排序

### 6. 链表快速排序

### 7. 链表计数排序

### 8. 链表桶排序

### 9. 链表基数排序

## 2.2 链表排序练习题

### [0147. 对链表进行插入排序](https://leetcode.cn/problems/insertion-sort-list/)

### [0021. 合并两个有序链表](https://leetcode.cn/problems/merge-two-sorted-lists/)

### [0148. 排序链表](https://leetcode.cn/problems/sort-list/)

## 3.1 链表双指针

### 1. 双指针简介

### 2. 起点不一致的快慢指针

### 3. 长度不一致的快慢指针

### 4. 分离双指针



## 3.2 链表双指针练习题

### [0141. 环形链表](https://leetcode.cn/problems/linked-list-cycle/)

### [0142. 环形链表 II](https://leetcode.cn/problems/linked-list-cycle-ii/)

### [0019. 删除链表的倒数第 N 个结点](https://leetcode.cn/problems/remove-nth-node-from-end-of-list/)

