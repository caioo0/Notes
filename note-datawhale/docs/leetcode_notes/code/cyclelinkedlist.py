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


