# 广度优先遍历

> 关于笔记，主要来自[datawhale-Leetcode算法笔记](https://datawhalechina.github.io/leetcode-notes/#/ch02/02.05/02.05.01-BFS)

## 广度优先遍历

广度优先遍历：一种由近到远的遍历方式，从某个节点出发，始终优先访问距离最近的顶点，并一层层向外扩张。

![image-20231029172751681](.\img\image-20231029172751681.png)

> 不唯一。广度优先遍历只要求按“由近及远”的顺序遍历，**而多个相同距离的顶点的遍历顺序是允许被任意打乱的**。以图 1 为例，顶点 1、3 的访问顺序可以交换、顶点 2、4、6 的访问顺序也可以任意交换。

### 算法实现

BFS 通常借助队列来实现。队列具有“先入先出”的性质，这与 BFS 的“由近及远”的思想异曲同工。

1. 将遍历起始顶点 `startVet` 加入队列，并开启循环。
2. 在循环的每轮迭代中，弹出队首顶点并记录访问，然后将该顶点的所有邻接顶点加入到队列尾部。
3. 循环步骤 `2.` ，直到所有顶点被访问完成后结束。

```python
def graph_bfs(graph: GraphAdjList, start_vet: Vertex) -> list[Vertex]:
    """广度优先遍历 BFS"""
    # 使用邻接表来表示图，以便获取指定顶点的所有邻接顶点
    # 顶点遍历序列
    res = []
    # 哈希表，用于记录已被访问过的顶点
    visited = set[Vertex]([start_vet])
    # 队列用于实现 BFS
    que = deque[Vertex]([start_vet])
    # 以顶点 vet 为起点，循环直至访问完所有顶点
    while len(que) > 0:
        vet = que.popleft()  # 队首顶点出队
        res.append(vet)  # 记录访问顶点
        # 遍历该顶点的所有邻接顶点
        for adj_vet in graph.adj_list[vet]:
            if adj_vet in visited:
                continue  # 跳过已被访问过的顶点
            que.append(adj_vet)  # 只入队未访问的顶点
            visited.add(adj_vet)  # 标记该顶点已被访问
    # 返回顶点遍历序列
    return res

```

### 复杂度分析

**时间复杂度：** 所有顶点都会入队并出队一次，使用 $O(|V|)$ 时间；在遍历邻接顶点的过程中，由于是无向图，因此所有边都会被访问 2 次，使用 $O(2|E|)$ 时间；总体使用 $O(|V|+|E|)$ 时间。

**空间复杂度：** 列表 `res` ，哈希表 `visited` ，队列 `que` 中的顶点数量最多为$ |V|$ ，使用 $O(|V|) $空间。

## 深度优先遍历

**深度优先遍历是一种优先走到底、无路可走再回头的遍历方式**

![image-20231029173356898](.\img\image-20231029173356898.png)

### 算法实现

这种“走到尽头再返回”的算法范式通常基于递归来实现。与广度优先遍历类似，在深度优先遍历中我们也需要借助一个哈希表 `visited` 来记录已被访问的顶点，以避免重复访问顶点。

```python
def dfs(graph: GraphAdjList, visited: set[Vertex], res: list[Vertex], vet: Vertex):
    """深度优先遍历 DFS 辅助函数"""
    res.append(vet)  # 记录访问顶点
    visited.add(vet)  # 标记该顶点已被访问
    # 遍历该顶点的所有邻接顶点
    for adjVet in graph.adj_list[vet]:
        if adjVet in visited:
            continue  # 跳过已被访问过的顶点
        # 递归访问邻接顶点
        dfs(graph, visited, res, adjVet)

def graph_dfs(graph: GraphAdjList, start_vet: Vertex) -> list[Vertex]:
    """深度优先遍历 DFS"""
    # 使用邻接表来表示图，以便获取指定顶点的所有邻接顶点
    # 顶点遍历序列
    res = []
    # 哈希表，用于记录已被访问过的顶点
    visited = set[Vertex]()
    dfs(graph, visited, res, start_vet)
    return res

```

深度优先遍历的算法流程:

- **直虚线代表向下递推**，表示开启了一个新的递归方法来访问新顶点。
- **曲虚线代表向上回溯**，表示此递归方法已经返回，回溯到了开启此递归方法的位置。

### 2.  复杂度分析

**时间复杂度：** 所有顶点都会被访问 1 次，使用$ O(|V|) $时间；所有边都会被访问 2 次，使用 $O(2|E|)$ 时间；总体使用 $O(|V|+|E|)$ 时间。

**空间复杂度：** 列表 `res` ，哈希表 `visited` 顶点数量最多为$ |V|$ ，递归深度最大为$ |V|$ ，因此使用 $O(|V|)$ 空间。

## 练习题目

### [1.](https://datawhalechina.github.io/leetcode-notes/#/ch02/02.05/02.05.02-Exercises?id=_1-0463-岛屿的周长)[0463. 岛屿的周长](https://leetcode.cn/problems/island-perimeter/)

### [2.](https://datawhalechina.github.io/leetcode-notes/#/ch02/02.05/02.05.02-Exercises?id=_2-0752-打开转盘锁)[0752. 打开转盘锁](https://leetcode.cn/problems/open-the-lock/)

### [3.](https://datawhalechina.github.io/leetcode-notes/#/ch02/02.05/02.05.02-Exercises?id=_3-0279-完全平方数)[0279. 完全平方数](https://leetcode.cn/problems/perfect-squares/)

### [4.](https://datawhalechina.github.io/leetcode-notes/#/ch02/02.05/02.05.03-Exercises?id=_1-0542-01-矩阵)[0542. 01 矩阵](https://leetcode.cn/problems/01-matrix/)

### [5.](https://datawhalechina.github.io/leetcode-notes/#/ch02/02.05/02.05.03-Exercises?id=_2-0322-零钱兑换)[0322. 零钱兑换](https://leetcode.cn/problems/coin-change/)

### [6.](https://datawhalechina.github.io/leetcode-notes/#/ch02/02.05/02.05.03-Exercises?id=_3-剑指-offer-13-机器人的运动范围)[剑指 Offer 13. 机器人的运动范围](https://leetcode.cn/problems/ji-qi-ren-de-yun-dong-fan-wei-lcof/)

