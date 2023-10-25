# 深度优化搜索

> 关于笔记，主要来自[datawhale-Leetcode算法笔记](https://datawhalechina.github.io/leetcode-notes/#/ch01/01.01/01.01.02-Algorithm-Complexity)

**深度优化搜索算法（Depth First Search）:** 英文简称DFS, 是一种用于搜索树或图结构的算法。深度优化搜索算法采用了回溯思想，从起始节点开始，沿着一条路径尽可能深入地访问节点，直到无法继续前进时为止，然后回溯到上一个未访问的节点，继续深入搜索，直到完成整个搜索过程。

## 算法原理

深度优先搜索（Depth First Search），是图遍历算法的一种。用一句话概括就是：“一直往下走，走不通回头，换条路再走，直到无路可走”。具体算法描述为：

> 选择一个起始点 $u$ 作为 **当前结点**，执行如下操作：
> a. 访问 当前结点，并且标记该结点已被访问，然后跳转到$ b$；
> b. 如果存在一个和 当前结点 相邻并且尚未被访问的结点 $v$ ，则将 $v$ 设为 当前结点，继续执行 $a$；
> c. 如果不存在这样的 $v$，则进行回溯，回溯的过程就是回退当前结点；

上述所说的 **当前结点** 需要用一个栈来维护，每次访问到的结点入栈，回溯的时候出栈。除了栈，另一种实现深度优先搜索的方式是递归，代码更加简单，相对好理解。

【例题1】给定一个 n 个结点的无向图，要求从 0 号结点出发遍历整个图，求输出整个过程的遍历序列。其中，遍历规则为：
1）如果和 当前结点 相邻的结点已经访问过，则不能再访问；
2）每次从和 当前结点 相邻的结点中寻找一个编号最小的没有访问的结点进行访问；

![image-20231025193726856](.\img\image-20231025193726856.png)

解答步骤：

>   对上图以深度优先的方式进行遍历，起点是 0；
>
> - <1> 第一步，当前结点为 0，标记已访问，然后从相邻结点中找到编号最小的且没有访问的结点 1；
> - <2> 第二步，当前结点为 1，标记已访问，然后从相邻结点中找到编号最小的且没有访问的结点 3；
> - <3> 第三步，当前结点为 3，标记已访问，没有尚未访问的相邻结点，执行回溯，回到结点 1；
> - <4> 第四步，当前结点为 1，从相邻结点中找到编号最小的且没有访问的结点 4；
> - <5> 第五步，当前结点为 4，标记已访问，然后从相邻结点中找到编号最小的且没有访问的结点 5；
> - <6> 第六步，当前结点为 5，标记已访问，然后从相邻结点中找到编号最小的且没有访问的结点 2；
> - <7> 第七步，当前结点为 2，标记已访问，然后从相邻结点中找到编号最小的且没有访问的结点 6；
> - <8> 第八步，当前结点为 6，标记已访问，没有尚未访问的相邻结点，执行回溯，回到结点 2；
> - <9> 第九步，按照 2 => 5 => 4 => 1 => 0 的顺序一路回溯，搜索结束；

如下图所示：红色块表示往下搜索，蓝色块表示往上回溯，遍历序列为：

![v2-a1d51c918c90332cc7ccc49de788360a_b](.\img\v2-a1d51c918c90332cc7ccc49de788360a_b.webp)

```shell
0 -> 1 -> 3 -> 4 -> 5 -> 2 -> 6
```

### 算法实现

基于递归实现代码：

```python
class Solution:
    def dfs_recursive(self, graph, u, visited):
        print(u)                        # 访问节点
        visited.add(u)                  # 节点 u 标记其已访问

        for v in graph[u]:
            if v not in visited:        # 节点 v 未访问过
                # 深度优先搜索遍历节点
                self.dfs_recursive(graph, v, visited)
        

graph = {
    "A": ["B", "C"],
    "B": ["A", "C", "D"],
    "C": ["A", "B", "D", "E"],
    "D": ["B", "C", "E", "F"],
    "E": ["C", "D"],
    "F": ["D", "G"],
    "G": []
}

# 基于递归实现的深度优先搜索
visited = set()
Solution().dfs_recursive(graph, "A", visited)

```

基于堆栈实现代码：

```python
class Solution:
    def dfs_stack(self, graph, u):
        print(u)                            # 访问节点 u
        visited, stack = set(), []          # 使用 visited 标记访问过的节点, 使用栈 stack 存放临时节点
        
        stack.append([u, 0])                # 将节点 u，节点 u 的下一个邻接节点下标放入栈中，下次将遍历 graph[u][0]
        visited.add(u)                      # 将起始节点 u 标记为已访问
        
    
        while stack:
            u, i = stack.pop()              # 取出节点 u，以及节点 u 下一个将要访问的邻接节点下标 i
            
            if i < len(graph[u]):
                v = graph[u][i]             # 取出邻接节点 v
                stack.append([u, i + 1])    # 下一次将遍历 graph[u][i + 1]
                if v not in visited:        # 节点 v 未访问过
                    print(v)                # 访问节点 v
                    stack.append([v, 0])    # 下一次将遍历 graph[v][0]
                    visited.add(v)          # 将节点 v 标记为已访问                
        

graph = {
    "A": ["B", "C"],
    "B": ["A", "C", "D"],
    "C": ["A", "B", "D", "E"],
    "D": ["B", "C", "E", "F"],
    "E": ["C", "D"],
    "F": ["D", "G"],
    "G": []
}

# 基于堆栈实现的深度优先搜索
Solution().dfs_stack(graph, "A")

```

## 练习题

- [200. 岛屿数量 - 力扣（LeetCode）](https://leetcode.cn/problems/number-of-islands/)
- [133. 克隆图 - 力扣（LeetCode）](https://leetcode.cn/problems/clone-graph/)

## 参考

[^1]: https://zhuanlan.zhihu.com/p/441063468

- [深度优先搜索 - LeetBook - 力扣（LeetCode）](https://leetcode.cn/leetbook/read/dfs/egx6xc/)
- 算法数据结构：深度优先搜索（DFS） - 掘金](https://juejin.cn/post/6864348493721387021)
- [Python 图的 BFS 与 DFS - 黄蜜桃的博客 - CSDN 博客](https://blog.csdn.net/qq_37738656/article/details/83027943)
- [图的深度优先遍历（递归、非递归；邻接表，邻接矩阵）_zjq_smile 的博客 - CSDN博客](https://blog.csdn.net/zscfa/article/details/75947816)
- [200. 岛屿数量（DFS / BFS） - 岛屿数量 - 力扣（LeetCode）](https://leetcode.cn/problems/number-of-islands/solution/number-of-islands-shen-du-you-xian-bian-li-dfs-or-/)

