# 树与二叉树
> 关于笔记，主要来自[datawhale-Leetcode算法笔记](https://datawhalechina.github.io/leetcode-notes/#/ch03/03.03/03.03.01-Binary-Tree-Basic)

## 1. 树

### 1.1 定义

**树（Tree）** 是`n(n>=0)`个结点的有限集。`n=0`时称为空树。在任意一颗非空树中：

1. 有且仅有一个特定的称为根（Root）的结点；
2. 当n>1时，其余结点可分为`m(m>0)`个互不相交的有限集T1、T2、......、Tn，其中每一个集合本身又是一棵树，并且称为根的子树。

此外，树的定义还需要强调以下两点：

1. `n>0`时根结点是唯一的，不可能存在多个根结点，数据结构中的树只能有一个根结点。
2. `m>0`时，子树的个数没有限制，但它们一定是互不相交的。

### 1.2 节点

节点是数据结构中的基础，是构成复杂数据结构的基本组成单位。



### 1.3 节点的度

结点拥有的子树数目称为结点的**度**。

![image-20231122105445950](.\img\image-20231122105445950.png)

### 1.4 节点间关系

一个节点的子树的根节点称为该节点的 **「孩子节点」**，相应的，该节点称为孩子的 **「父亲节点」**。同一个父亲节点的孩子节点之间互称为 **「兄弟节点」**。

![image-20231122105531829](.\img\image-20231122105531829.png)

### 1.5  树结构有关的术语

1. **节点的层次**：从根节点开始定义，根为第 1 层，根的子节点为第 2 层，以此类推。

2. **树的深度（高度）**：所有节点中最大的层数。例如图中树的深度为 4。

3. **堂兄弟节点**：父节点在同一层的节点互为堂兄弟。例如图中 `G`、`K` 互为堂兄弟节点。

4. **路径**：树中两个节点之间所经过的节点序列。例如图中 `E` 到 `G` 的路径为 `E - B - A - D - G`。

5. **路径长度**：两个节点之间路径上经过的边数。例如图中 `E` 到 `G` 的路径长度为 4。

6. **节点的祖先**：从该节点到根节点所经过的所有节点，被称为该节点的祖先。例如图中 `H` 的祖先为 `E`、`B`、`A`。

7. **节点的子孙**：节点的子树中所有节点被称为该节点的子孙。例如图中 `D` 的子孙为 `F`、`G`、`K`。

   


![image-20231122105651003](.\img\image-20231122105651003.png)

### 1.6 树的分类

根据节点的子树是否可以互换位置，树分为两种类型：「有序树」 和 「无序树」。

如果将树中节点的各个子树看做是从左到右是依次有序的（即不能互换），则称该树为 「有序树」。反之，如果节点的各个子树可以互换位置，则成该树为 「无序树」。

- 有序树：节点的各个⼦树从左⾄右有序， 不能互换位置。有序树又分为二叉树和非二叉树
- 无序树：节点的各个⼦树可互换位置。

## 2. 二叉树

⼆叉树定义：特殊的树，它最多有两个⼦树，分别为左⼦树和右⼦树，并且两个子树是有序的，不可以互换。也就是说，在⼆叉树中不存在度⼤于 2 的节点。

二叉树在逻辑上可以分为 5 种基本形态：

![image-20231122101659686](.\img\image-20231122101659686.png)

### 2.1 满二叉树

**满二叉树（Full Binary Tree）**：如果所有分支节点都存在左子树和右子树，并且所有叶子节点都在同一层上，则称该二叉树为满二叉树。



![image-20231122101856779](.\img\image-20231122101856779.png)

### 2.2 完全二叉树

**完全二叉树（Complete Binary Tree）**：如果叶子节点只能出现在最下面两层，并且最下层的叶子节点都依次排列在该层最左边的位置上，具有这种特点的二叉树称为完全二叉树。

![image-20231122102122859](.\img\image-20231122102122859.png)

### 2.3 二叉搜索树

**二叉搜索树（Binary Search Tree）**：也叫做二叉查找树、有序二叉树或者排序二叉树。

是指一棵**空树**或者满足下列性质的**二叉树**：

- 如果任意节点的左子树不为空，则**左子树上所有节点的值均小于它的根节点的值**。
- 如果任意节点的右子树不为空，则**右子树上所有节点的值均大于它的根节点的值**。
- 任意节点的左子树、右子树均为二叉搜索树。

![image-20231122102358279](.\img\image-20231122102358279.png)

```python
def search(self, num: int) -> TreeNode | None:
    """查找节点"""
    cur = self._root
    # 循环查找，越过叶节点后跳出
    while cur is not None:
        # 目标节点在 cur 的右子树中
        if cur.val < num:
            cur = cur.right
        # 目标节点在 cur 的左子树中
        elif cur.val > num:
            cur = cur.left
        # 找到目标节点，跳出循环
        else:
            break
    return cur

```

#### 二叉搜索树常见应用

- 用作系统中的多级索引，实现高效的查找、插入、删除操作。
- 作为某些搜索算法的底层数据结构。
- 用于存储数据流，以保持其有序状态。

### 2.4 平衡二叉搜索树

**平衡二叉搜索树（Balanced Binary Tree）**：一种结构平衡的二叉搜索树。即**叶节点高度差的绝对值不超过 1**，并且左右两个子树都是一棵平衡二叉搜索树。平衡二叉树可以在 O(logn) 内完成插入、查找和删除操作。最早被发明的平衡二叉搜索树为 **「AVL 树（Adelson-Velsky and Landis Tree））」**。

AVL 树满足以下性质：

- 空二叉树是一棵 AVL 树。
- 如果 T 是一棵 AVL 树，那么其左右子树也是 AVL 树，并且 |h(ls)−h(rs)|≤1，h(ls) 是左子树的高度，h(rs)是右子树的高度。
- AVL 树的高度为 O(logn)。

![image-20231122102924275](.\img\image-20231122102924275.png)
$$
如图所示，第三棵树左右子树高度差超过了 
1，所以不是非平衡二叉搜索树
$$

## 3. 二叉树存储结构

二叉树存储结构分为：**顺序存储结构和链式存储结构**。

- 完全二叉树（尤其是满二叉树）能充分利用存储空间，适合顺序存储结构: 

- 当树的形态和大小经常发生动态变化时，更适合采用链式存储结构

### 3.1 二叉树顺序存储结构

二叉树的顺序存储结构使用**一维数组来存储二叉树中的节点**，节点存储位置则采用完全二叉树的**节点层次**编号，**按照层次从上至下，每一层从左至右的顺序依次存放二叉树的数据元素**。

在进行顺序存储时，如果对应的二叉树节点不存在，则设置为「空节点」

> 堆排序、优先队列中的二叉堆结构，采用的就是二叉树的顺序存储结构

![image-20231122104119614](.\img\image-20231122104119614.png)

节点之间的逻辑:

- 如果某二叉树节点（非叶子节点）的下标为 i，那么其左孩子节点下标为 2∗i+1，右孩子节点下标为 2∗i+2。
- 如果某二叉树节点（非根结点）的下标为 i，那么其根节点下标为 (i−1)//2。`// 表示整除`



```python
class TreeNode:
    """二叉树节点类"""
    def __init__(self, val: int):
        self.val: int = val                # 节点值
        self.left: TreeNode | None = None  # 左子节点引用
        self.right: TreeNode | None = None # 右子节点引用
            
    def list_to_tree_dfs(arr: list[int], i: int) -> TreeNode | None:
        """将列表反序列化为二叉树：递归"""
        # 如果索引超出数组长度，或者对应的元素为 None ，则返回 None
        if i < 0 or i >= len(arr) or arr[i] is None:
            return None
        # 构建当前节点
        root = TreeNode(arr[i])
        # 递归构建左右子树
        root.left = list_to_tree_dfs(arr, 2 * i + 1)
        root.right = list_to_tree_dfs(arr, 2 * i + 2)
        return root

```



### 3.2 二叉树链式存储结构

二叉树采用链式存储结构时，每个链节点包含一个用于数据域 `val`，存储节点信息；还包含两个指针域 `left` 和 `right`，分别指向左右两个孩子节点，当左孩子或者右孩子不存在时，相应指针域值为空。二叉链节点结构如下图所示：

![image-20231122110000173](.\img\image-20231122110000173.png)

对应代码：

```python
class TreeNode:
    """二叉树节点类"""
    def __init__(self, val: int):
        self.val: int = val                # 节点值
        self.left: TreeNode | None = None  # 左子节点引用
        self.right: TreeNode | None = None # 右子节点引用
```

> 更多知识点：https://www.hello-algo.com/chapter_tree/avl_tree/

## 4. 二叉树的遍历

二叉树常见的遍历方式包括层序遍历、前序遍历、中序遍历和后序遍历。

- 前序遍历：visit（node），preorder(left Subtree)， preorder(right Subtree)。

- 中序遍历：in-order(left Subtree)，visit（node），in-order(right Subtree)。

- 后序遍历：post-order(left Subtree)，post-order(right Subtree)，visit（node）。

- 层级遍历：一层层访问每个节点。

### 4.1  层序遍历

**层序遍历 （level-order traversal）**：从顶部到底部逐层遍历二叉树，并在每一层按照从左到右的顺序访问节点。

层序遍历本质上属于**广度优先遍历 （breadth-first traversal）**，它体现了一种一圈一圈向外扩展”的逐层遍历方式。

![image-20231122111008048](.\img\image-20231122111008048.png)

二叉树的层序遍历是通过队列来实现的。具体步骤如下：

1. 判断二叉树是否为空，为空则直接返回。
2. 令根节点入队。
3. 当队列不为空时，求出当前队列长度 $s_i$。
4. 依次从队列中取出这 $s_i$ 个元素，并对这 $s_i$ 个元素依次进行访问。然后将其左右孩子节点入队，然后继续遍历下一层节点。
5. 当队列为空时，结束遍历。



```python
def level_order(root: TreeNode | None) -> list[int]:
    """层序遍历"""
    # 初始化队列，加入根节点
    queue: deque[TreeNode] = deque()
    queue.append(root)
    # 初始化一个列表，用于保存遍历序列
    res = []
    while queue:
        node: TreeNode = queue.popleft()  # 队列出队
        res.append(node.val)  # 保存节点值
        if node.left is not None:
            queue.append(node.left)  # 左子节点入队
        if node.right is not None:
            queue.append(node.right)  # 右子节点入队
    return res
```

### 4.2 前序遍历

从二叉树的前序遍历规则可以看出：前序遍历过程是一个递归过程。在遍历任何一棵子树时仍然是按照先访问根节点，然后遍历子树根节点的左子树，最后再遍历子树根节点的右子树的顺序进行遍历。

二叉树的前序遍历规则为：

如果二叉树为空，则返回。

如果二叉树不为空，则：

1. 访问根节点。
2. 以前序遍历的方式遍历根节点的左子树。
3. 以前序遍历的方式遍历根节点的右子树。

![image-20231122135538683](.\img\image-20231122135538683.png)

该二叉树的中序遍历顺序为：`H - D - I - B - E - A - F - J - C - K - G`。

### 4.3 中序遍历

从二叉树的中序遍历规则可以看出：中序遍历过程也是一个递归过程。在遍历任何一棵子树时仍然是按照先遍历子树根节点的左子树，然后访问根节点，最后再遍历子树根节点的右子树的顺序进行遍历。

二叉树的中序遍历规则为：

如果二叉树为空，则返回。

如果二叉树不为空，则：

1. 以中序遍历的方式遍历根节点的左子树。
2. 访问根节点。
3. 以中序遍历的方式遍历根节点的右子树。



![image-20231122140027637](.\img\image-20231122140027637.png)

### 4.4 、后序遍历

从二叉树的后序遍历规则可以看出：后序遍历过程也是一个递归过程。在遍历任何一棵子树时仍然是按照先遍历子树根节点的左子树，然后遍历子树根节点的右子树，最后再访问根节点的顺序进行遍历。

二叉树的后序遍历规则为：

如果二叉树为空，则返回。

如果二叉树不为空，则：

1. 以后序遍历的方式遍历根节点的左子树。
2. 以后序遍历的方式遍历根节点的右子树。
3. 访问根节点。

![image-20231122140051278](.\img\image-20231122140051278.png)



深度优先搜索通常基于递归实现：

```python
def pre_order(root: TreeNode | None):
    """前序遍历"""
    if root is None:
        return
    # 访问优先级：根节点 -> 左子树 -> 右子树
    res.append(root.val)
    pre_order(root=root.left)
    pre_order(root=root.right)

def in_order(root: TreeNode | None):
    """中序遍历"""
    if root is None:
        return
    # 访问优先级：左子树 -> 根节点 -> 右子树
    in_order(root=root.left)
    res.append(root.val)
    in_order(root=root.right)

def post_order(root: TreeNode | None):
    """后序遍历"""
    if root is None:
        return
    # 访问优先级：左子树 -> 右子树 -> 根节点
    post_order(root=root.left)
    post_order(root=root.right)
    res.append(root.val)

```

## 5.二叉树还原

pip install --upgrade --force-reinstall --no-cache-dir jupyter --user

二叉树还原： 是指二叉树的遍历序列，还原出对应的二叉树

> 给定一棵非空二叉树，它的前序、中序、后序遍历序列唯一，反过来是否也唯一？
>
> - 根据前序和中序，树唯一
>
> - 知道中序和后序，树唯一
> - 知道谦虚和后序，树不唯一

![image-20231123095849356](.\img\image-20231123095849356.png)

总结：**前序或后序可以确立每一个子树的root，而中序则可以划分左右子树，然后迭代**就可以复原一棵树。

## 6.练习题

### [1.](https://datawhalechina.github.io/leetcode-notes/#/ch03/03.03/03.03.03-Exercises?id=_1-0144-二叉树的前序遍历)[0144. 二叉树的前序遍历](https://leetcode.cn/problems/binary-tree-preorder-traversal/)

解：

```python
class Solution:
    def preorderTraversal(self, root: Optional[TreeNode]) -> List[int]:
        res = []
        # 利用栈进行前序遍历
        if root is None:
            return []
        stack = [root]  # 先将根节点入栈
        while stack:
            node = stack.pop()
            res.append(node.val)
            if node.right != None:
                stack.append(node.right)
            if node.left != None:
                stack.append(node.left)
        return res
```



### [2.](https://datawhalechina.github.io/leetcode-notes/#/ch03/03.03/03.03.03-Exercises?id=_2-0094-二叉树的中序遍历)[0094. 二叉树的中序遍历](https://leetcode.cn/problems/binary-tree-inorder-traversal/)

解：

```python
class Solution:
    def inorderTraversal(self, root: Optional[TreeNode]) -> List[int]:
        
         # 注意：根节点为空，直接返回空列表
        if not root:
            return []

        stack = []
        res = []

        while root or stack:
            # 一直向左子树走，每一次将当前节点保存到栈中
            if root:
                stack.append(root)
                root = root.left
            # 当前节点为空，证明走到了最左边，从栈中弹出节点加入结果数组
            # 开始对右子树重复上述过程。
            else:
                cur = stack.pop()
                res.append(cur.val)
                root = cur.right

        return res

```



### [3.](https://datawhalechina.github.io/leetcode-notes/#/ch03/03.03/03.03.03-Exercises?id=_3-0145-二叉树的后序遍历)[0145. 二叉树的后序遍历](https://leetcode.cn/problems/binary-tree-postorder-traversal/)

解：

```python
class Solution:
     def postOrder(self, root: TreeNode, res):
        if root == None:
            return

        self.postOrder(root.left, res)
        self.postOrder(root.right, res)
        res.append(root.val)

     def postorderTraversal(self, root: TreeNode) -> List[int]:
        res = []
        self.postOrder(root, res)
        return res

```



### [4.](https://datawhalechina.github.io/leetcode-notes/#/ch03/03.03/03.03.04-Exercises?id=_1-0102-二叉树的层序遍历)[0102. 二叉树的层序遍历](https://leetcode.cn/problems/binary-tree-level-order-traversal/)

### [5.](https://datawhalechina.github.io/leetcode-notes/#/ch03/03.03/03.03.04-Exercises?id=_2-0104-二叉树的最大深度)[0104. 二叉树的最大深度](https://leetcode.cn/problems/maximum-depth-of-binary-tree/)

### [6.](https://datawhalechina.github.io/leetcode-notes/#/ch03/03.03/03.03.04-Exercises?id=_3-0112-路径总和)[0112. 路径总和](https://leetcode.cn/problems/path-sum/)

### [7.](https://datawhalechina.github.io/leetcode-notes/#/ch03/03.03/03.03.07-Exercises?id=_1-0105-从前序与中序遍历序列构造二叉树)[0105. 从前序与中序遍历序列构造二叉树](https://leetcode.cn/problems/construct-binary-tree-from-preorder-and-inorder-traversal/)

### [8.](https://datawhalechina.github.io/leetcode-notes/#/ch03/03.03/03.03.07-Exercises?id=_2-0106-从中序与后序遍历序列构造二叉树)[0106. 从中序与后序遍历序列构造二叉树](https://leetcode.cn/problems/construct-binary-tree-from-inorder-and-postorder-traversal/)

### [9.](https://datawhalechina.github.io/leetcode-notes/#/ch03/03.03/03.03.07-Exercises?id=_3-0889-根据前序和后序遍历构造二叉树)[0889. 根据前序和后序遍历构造二叉树](https://leetcode.cn/problems/construct-binary-tree-from-preorder-and-postorder-traversal/)



更多练：https://datawhalechina.github.io/leetcode-notes/#/ch03/03.03/03.03.05-Binary-Tree-Traverse-List

## 6.参考资料

1. [深入理解(二叉树、平衡二叉树、B-Tree、B+Tree )的区别](https://zhuanlan.zhihu.com/p/270389432)
2. [hello 算法之树](https://www.hello-algo.com/chapter_tree/avl_tree/)
3. https://blog.csdn.net/ten_sory/article/details/112002857
4. https://www.cnblogs.com/Eleven-Qian-Shan/p/13072122.html