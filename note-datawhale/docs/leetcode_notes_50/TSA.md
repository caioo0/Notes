# 拓扑排序

## 介绍

在图论中，拓扑排序（Topological Sorting）是一个**有向无环图（DAG, Directed Acyclic Graph）**的所有顶点的线性序列。且该序列必须满足下面两个条件：

- 每个顶点出现且只出现一次。
- 若存在一条从顶点 A 到顶点 B 的路径，那么在序列中顶点 A 出现在顶点 B 的前面。



> 注意：有向无环图（DAG）才有图的拓扑排序，无向图和有向有环图没有拓扑排序，或者说不存在拓扑排序。

例如：下面这个图：

![image-20231030165831051](.\img\image-20231030165831051.png)

它是一个 DAG 图，那么如何写出它的拓扑排序呢？这里说一种比较常用的方法：

- 从 DAG 图中选择一个 没有前驱（即入度为0）的顶点并输出。
- 从图中删除该顶点和所有以它为起点的有向边。
- 重复 1 和 2 直到当前的 DAG 图为空或当前图中不存在无前驱的顶点为止。后一种情况说明有向图中必然存在环。
  

![image-20231030165936045](.\img\image-20231030165936045.png)

于是，得到拓扑排序后的结果是 { 1, 2, 4, 3, 5 }。

通常，一个有向无环图可以有**一个或多个**拓扑排序序列。

## 实现方法

拓扑排序有两种实现方法，分别是「Kahn 算法」和「DFS 深度优先搜索算法」。接下来我们依次来看下它们是如何实现的。

### 1. khhn算法

#### **基本思想**：

1. 不断找寻有向图中入度为 $0$ 的顶点，将其输出。
2. 然后删除入度为 $0$ 的顶点和从该顶点出发的有向边。
3. 重复上述操作直到图为空，或者找不到入度为 $0$ 的节点为止。

#### 实现步骤：

1. 使用数组 $indegrees$ 用于记录图中各个顶点的入度。
2. 维护一个入度为 $0$ 的顶点集合 $S$（可使用栈、队列、优先队列）。
3. 每次从集合中选择任何一个没有前驱（即入度为 $0$）的顶点 $u$，将其输出到拓扑序列 $order$ 中。
4. 从图中删除该顶点 $u$，并且删除从该顶点出发的有向边 $<u, v>$（也就是把该顶点可达的顶点入度都减 $1$）。如果删除该边后顶点 $v$ 的入度变为 $0$，则将顶点 $v$ 放入集合 $S$ 中。
5. 重复上述过程，直到集合 $S$ 为空，或者图中还有顶点未被访问（说明一定存在环路，无法形成拓扑序列）。
6. 如果不存在环路，则 $order$ 中顶点的顺序就是拓扑排序的结果。

```python
import collections

class Solution:
    # 拓扑排序，graph 中包含所有顶点的有向边关系（包括无边顶点）
    def topologicalSortingKahn(self, graph: dict):
        indegrees = {u: 0 for u in graph}   # indegrees 用于记录所有顶点入度
        for u in graph:
            for v in graph[u]:
                indegrees[v] += 1           # 统计所有顶点入度
        
        # 将入度为 0 的顶点存入集合 S 中
        S = collections.deque([u for u in indegrees if indegrees[u] == 0])
        order = []                          # order 用于存储拓扑序列
        
        while S:
            u = S.pop()                     # 从集合中选择一个没有前驱的顶点 0
            order.append(u)                 # 将其输出到拓扑序列 order 中
            for v in graph[u]:              # 遍历顶点 u 的邻接顶点 v
                indegrees[v] -= 1           # 删除从顶点 u 出发的有向边
                if indegrees[v] == 0:       # 如果删除该边后顶点 v 的入度变为 0
                    S.append(v)             # 将其放入集合 S 中
        
        if len(indegrees) != len(order):    # 还有顶点未遍历（存在环），无法构成拓扑序列
            return []
        return order                        # 返回拓扑序列
    
    
    def findOrder(self, n: int, edges):
        # 构建图
        graph = dict()
        for i in range(n):
            graph[i] = []
            
        for u, v in edges:
            graph[u].append(v)
            
        return self.topologicalSortingKahn(graph)

```

### 2. 基于 DFS 实现拓扑排序算法

#### 基本思想：

1. 对于一个顶点 $u$，深度优先遍历从该顶点出发的有向边 $<u, v>$。如果从该顶点 $u$ 出发的所有相邻顶点 $v$ 都已经搜索完毕，则回溯到顶点 $u$ 时，该顶点 $u$ 应该位于其所有相邻顶点 $v$ 的前面（拓扑序列中）。
2. 这样一来，当我们对每个顶点进行深度优先搜索，在回溯到该顶点时将其放入栈中，则最终从栈顶到栈底的序列就是一种拓扑排序。

#### 实现步骤：

1. 使用集合 $visited$ 用于记录当前顶点是否被访问过，避免重复访问。
2. 使用集合 $onStack$ 用于记录同一次深度优先搜索时，当前顶点是否被访问过。如果当前顶点被访问过，则说明图中存在环路，无法构成拓扑序列。
3. 使用布尔变量 $hasCycle$ 用于判断图中是否存在环。
4. 从任意一个未被访问的顶点 $u$ 出发。
   1. 如果顶点 $u$ 在同一次深度优先搜索时被访问过，则说明存在环。
   2. 如果当前顶点被访问或者有环时，则无需再继续遍历，直接返回。
5. 将顶点 $u$ 标记为被访问过，并在本次深度优先搜索中标记为访问过。然后深度优先遍历从顶点 $u$ 出发的有向边 $<u, v>$。
6. 当顶点 $u$ 的所有相邻顶点 $v$ 都被访问后，回溯前记录当前节点 $u$（将当前节点 $u$ 输出到拓扑序列 $order$ 中）。
7. 取消本次深度优先搜索时，顶点 $u$ 的访问标记。
8. 对其他未被访问的顶点重复 $4 \sim 7$ 步过程，直到所有节点都遍历完，或者出现环。
9. 如果不存在环路，则将 $order$ 逆序排序后，顶点的顺序就是拓扑排序的结果。

```python
import collections

class Solution:
    # 拓扑排序，graph 中包含所有顶点的有向边关系（包括无边顶点）
    def topologicalSortingDFS(self, graph: dict):
        visited = set()                     # 记录当前顶点是否被访问过
        onStack = set()                     # 记录同一次深搜时，当前顶点是否被访问过
        order = []                          # 用于存储拓扑序列
        hasCycle = False                    # 用于判断是否存在环
        
        def dfs(u):
            nonlocal hasCycle
            if u in onStack:                # 同一次深度优先搜索时，当前顶点被访问过，说明存在环
                hasCycle = True
            if u in visited or hasCycle:    # 当前节点被访问或者有环时直接返回
                return
            
            visited.add(u)                  # 标记节点被访问
            onStack.add(u)                  # 标记本次深搜时，当前顶点被访问
    
            for v in graph[u]:              # 遍历顶点 u 的邻接顶点 v
                dfs(v)                      # 递归访问节点 v
                    
            order.append(u)                 # 后序遍历顺序访问节点 u
            onStack.remove(u)               # 取消本次深搜时的 顶点访问标记
        
        for u in graph:
            if u not in visited:
                dfs(u)                      # 递归遍历未访问节点 u
        
        if hasCycle:                        # 判断是否存在环
            return []                       # 存在环，无法构成拓扑序列
        order.reverse()                     # 将后序遍历转为拓扑排序顺序
        return order                        # 返回拓扑序列
    
    def findOrder(self, n: int, edges):
        # 构建图
        graph = dict()
        for i in range(n):
            graph[i] = []
        for v, u in edges:
            graph[u].append(v)
        
        return self.topologicalSortingDFS(graph)

```

## 练习题目

### [1.](http://localhost/datawhale/leetcode-notes/docs/#/ch02/02.06/02.06.02-Exercises?id=_1-0207-课程表)[0207. 课程表](https://leetcode.cn/problems/course-schedule/)

### [2.](http://localhost/datawhale/leetcode-notes/docs/#/ch02/02.06/02.06.02-Exercises?id=_2-0210-课程表-ii)[0210. 课程表 II](https://leetcode.cn/problems/course-schedule-ii/)

### [3.](http://localhost/datawhale/leetcode-notes/docs/#/ch02/02.06/02.06.02-Exercises?id=_3-0802-找到最终的安全状态)[0802. 找到最终的安全状态](https://leetcode.cn/problems/find-eventual-safe-states/)

### [4.0851][喧闹和富有](https://leetcode.cn/problems/loud-and-rich/)

