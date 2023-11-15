#!usr/bin/env python
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
