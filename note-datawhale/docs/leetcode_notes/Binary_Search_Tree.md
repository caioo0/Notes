# 二叉搜索树

> 关于笔记，主要来自[datawhale-Leetcode算法笔记](https://datawhalechina.github.io/leetcode-notes/#/ch03/03.02/03.02.10-Trie)

## 1.定义

二叉搜索树（BST，Binary Search Tree），也二叉排序树或二叉查找树。
二叉搜索树：一棵二叉树，可以为空；如果不为空，满足以下性质：

1. 非空左子树的所有键值小于其根结点的键值。
2. 非空右子树的所有键值大于其根结点的键值。
3. 左、右子树都是二叉搜索树。

![image-20231123101150343](.\img\image-20231123101150343.png)

叉树具有一个特性，即：$左子树的节点值 < 根节点值 < 右子树的节点值$。



## 2.二叉搜索树的查找

> 在二叉搜索树中查找值为`val`的节点

**查找步骤：**

1. 判断树为空 ， 则返回空指针`none`,查找结束
2. 判断树不为空，将`val` 与根节点比较判断是左子树或右子树
3. 如果等于，返回成功
4. 如果不等于，利用递归查找左子树或者右子树。

![image-20231123101553870](D:\www\learning\caioo0.github.io\note-datawhale\docs\leetcode_notes\img\image-20231123101553870.png)
$$
查找 9 的节点。
$$


```python
class Solution:
    def searchBST(self, root: TreeNode, val: int) -> TreeNode:
        if not root:
            return None
        
        if val == root.val:
            return root
        elif val < root.val:
            return self.searchBST(root.left, val)
        else:
            return self.searchBST(root.right, val)

```

## 3.二叉搜索树的常用操作

### 3.1 插入

代码实现：

```python
class Solution:
    def insertIntoBST(self, root: TreeNode, val: int) -> TreeNode:
        if root == None:
            return TreeNode(val)

        if val < root.val:
            root.left = self.insertIntoBST(root.left, val)
        if val > root.val:
            root.right = self.insertIntoBST(root.right, val)
        return root

```

### 3.2 创建

代码实现：

```python
class Solution:
    def insertIntoBST(self, root: TreeNode, val: int) -> TreeNode:
        if root == None:
            return TreeNode(val)

        if val < root.val:
            root.left = self.insertIntoBST(root.left, val)
        if val > root.val:
            root.right = self.insertIntoBST(root.right, val)
        return root
    def buildBST(self, nums) -> TreeNode:
        root = TreeNode(val)
        for num in nums:
            self.insertIntoBST(root, num)
        return root

```

### 3.3 删除

代码实现：

```python
class Solution:
    def deleteNode(self, root: TreeNode, val: int) -> TreeNode:
        if not root:
            return root

        if root.val > val:
            root.left = self.deleteNode(root.left, val)
            return root
        elif root.val < val:
            root.right = self.deleteNode(root.right, val)
            return root
        else:
            if not root.left:
                return root.right
            elif not root.right:
                return root.left
            else:
                curr = root.right
                while curr.left:
                    curr = curr.left
                curr.left = root.left
                return root.right

```

## 4. 练习题

### [1.](https://datawhalechina.github.io/leetcode-notes/#/ch03/03.04/03.04.02-Exercises?id=_1-0700-二叉搜索树中的搜索)[0700. 二叉搜索树中的搜索](https://leetcode.cn/problems/search-in-a-binary-search-tree/)

### [2.](https://datawhalechina.github.io/leetcode-notes/#/ch03/03.04/03.04.02-Exercises?id=_2-0701-二叉搜索树中的插入操作)[0701. 二叉搜索树中的插入操作](https://leetcode.cn/problems/insert-into-a-binary-search-tree/)

### [3.](https://datawhalechina.github.io/leetcode-notes/#/ch03/03.04/03.04.02-Exercises?id=_3-0450-删除二叉搜索树中的节点)[0450. 删除二叉搜索树中的节点](https://leetcode.cn/problems/delete-node-in-a-bst/)

### [4.](https://datawhalechina.github.io/leetcode-notes/#/ch03/03.04/03.04.03-Exercises?id=_1-0098-验证二叉搜索树)[0098. 验证二叉搜索树](https://leetcode.cn/problems/validate-binary-search-tree/)

### [5.](https://datawhalechina.github.io/leetcode-notes/#/ch03/03.04/03.04.03-Exercises?id=_2-0108-将有序数组转换为二叉搜索树)[0108. 将有序数组转换为二叉搜索树](https://leetcode.cn/problems/convert-sorted-array-to-binary-search-tree/)

### [6.](https://datawhalechina.github.io/leetcode-notes/#/ch03/03.04/03.04.03-Exercises?id=_3-0235-二叉搜索树的最近公共祖先)[0235. 二叉搜索树的最近公共祖先](https://leetcode.cn/problems/lowest-common-ancestor-of-a-binary-search-tree/)