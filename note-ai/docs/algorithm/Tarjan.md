# Tarjan算法

> 参考：https://zhuanlan.zhihu.com/p/101923309

Tarjan 算法是图论中非常实用 / 常用的算法之一，能解决强连通分量，双连通分量，割点和桥，求最近公共祖先（LCA）等问题。

##  Tarjan 算法

Tarjan 算法是基于**[深度优先搜索](https://link.zhihu.com/?target=https%3A//en.wikipedia.org/wiki/Depth-first_search)**的算法，用于求解图的连通性问题。Tarjan 算法可以在线性时间内求出无向图的割点与桥，进一步地可以求解无向图的双连通分量；同时，也可以求解有向图的强连通分量、必经点与必经边。

**Tarjan 算法是基于深度优先搜索的，用于求解图的连通性问题的算法。**

