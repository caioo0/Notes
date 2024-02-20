# leetcode面试篇001-012

## 试题1:  0054.螺旋矩阵

题目：https://leetcode.cn/problems/spiral-matrix/description/

思路：

1. 取出矩阵第一行: matrix.pop(0)
2. 剩余的矩阵逆时针旋转，然后再去第一行
3. 如此循环取出第一行，直到完成

代码实现：

```python
class Solution:
    def spiralOrder(self, matrix: List[List[int]]) -> List[int]:
        res = []
        while matrix:
            res += matrix.pop(0)   # 取出第一行
            matrix = list(map(list, zip(*matrix)))[::-1] # 剩余矩阵逆时针旋转
        return res
```

