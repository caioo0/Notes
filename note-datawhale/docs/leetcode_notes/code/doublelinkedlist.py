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


