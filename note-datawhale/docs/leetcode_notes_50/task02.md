# 数组基础

## 数组基础知识

### 定义

**数组(Array):** 一种线性表数据结构。它使用一组连续的内存空间，来存储一组具有相同类型的数据。

**数组**是实现线性表的顺序结构存储的基础。

![image-20230914103121126](.\img\image-20230914103121126.png)

如上图所示，假设数据元素的个数为 $n$，则数组中的每一个数据元素都有自己的下标索引，下标索引从 0 开始，到 $n$−1 结束。数组中的每一个「下标索引」，都有一个与之相对应的「数据元素」。

从上图还可以看出，数组在计算机中的表示，就是一片连续的存储单元。数组中的每一个数据元素都占有一定的存储单元，每个存储单元都有自己的内存地址，并且元素之间是紧密排列的。

>1. 线性表：线性表就是所有数据元素排成像一条线一样的结构，线性表上的数据元素都是相同类型，且每个数据元素最多只有前、后两个方向。数组就是一种线性表结构，此外，栈、队列、链表都是线性表结构。
>2. 连续的内存空间：线性表有两种存储结构：「顺序存储结构」和「链式存储结构」。其中，「顺序存储结构」是指占用的内存空间是连续的，相邻数据元素之间，物理内存上的存储位置也相邻。数组也是采用了顺序存储结构，并且存储的数据都是相同类型的。
>3. 综合这两个角度，数组就可以看做是：使用了「顺序存储结构」的「线性表」的一种实现方式。
>

### 如何随机访问数据元素

数组可以根据下标进行随机访问

计算机给一个数组分配了一组连续的存储空间，其中第一个元素开始的地址被称为 **首地址**。

每个数据元素都有对应的下标索引和内存地址，计算机通过地址来访问数据元素。当计算机需要访问数组的某个元素时，会通过 **寻址公式** 计算出对应元素的内存地址，然后访问地址对应的数据元素。

寻址公式如下：**下标 $i$ 对应的数据元素地址 = 数据首地址 + $i$ × 单个数据元素所占内存大小**。

### 二维数组

维数组是一个由 $m$ 行 $n$ 列数据元素构成的特殊结构，其本质上是以数组作为数据元素的数组，即 **数组的数组**。

二维数组的第一维度表示行，第二维度表示列。

### 不同编程语言中数组的实现

C / C++ 

```c++
int arr[3][4] = {{0, 1, 2, 3}, {4, 5, 6, 7}, {8, 9, 10, 11}};
```

JAVA

```java
int[][] arr = new int[3][]{ {1,2,3}, {4,5}, {6,7,8,9}};
```

Python

```python
arr = ['python', 'java', ['asp', 'php'], 'c']
```

### 数组的基本操作

数据结构的操作一般涉及到增、删、改、查共 4 种情况

#### 1. 访问元素

```python
# 从数组 nums 中读取下标为 i 的数据元素值
def value(nums, i):
    if 0 <= i <= len(nums) - 1:
        print(nums[i])
        
arr = [0, 5, 2, 3, 7, 1, 6]
value(arr, 3)

```

#### 2. 查找元素

```
# 从数组 nums 中查找元素值为 val 的数据元素第一次出现的位置
def find(nums, val):
    for i in range(len(nums)):
        if nums[i] == val:
            return i
    return -1

arr = [0, 5, 2, 3, 7, 1, 6]
print(find(arr, 5))

```

#### 3. 插入元素

插入元素操作分为两种：「在数组尾部插入值为 $val$ 的元素」和「在数组第 $i$ 个位置上插入值为 $val$ 的元素」。

```python
# 在数组尾部插入值为 val 的元素
arr = [0, 5, 2, 3, 7, 1, 6]
val = 4
arr.append(val)
print(arr)

#在数组第 $i$ 个位置上插入值为 $val$ 的元素
arr = [0, 5, 2, 3, 7, 1, 6]
i, val = 2, 4
arr.insert(i, val)
print(arr)
```

#### 4. 改变元素

```python
def change(nums, i, val):
    if 0 <= i <= len(nums) - 1:
        nums[i] = val
        
arr = [0, 5, 2, 3, 7, 1, 6]
i, val = 2, 4
change(arr, i, val)
print(arr)
```

##### 删除元素

```
arr = [0, 5, 2, 3, 7, 1, 6]
arr.pop()
print(arr)
```



### 数组的基础知识总结

数组是最基础、最简单的数据结构。数组是实现线性表的顺序结构存储的基础。它使用一组连续的内存空间，来存储一组具有相同类型的数据。

数组的最大特点的支持随机访问。访问数组元素、改变数组元素的时间复杂度为 $O(1)$，在数组尾部插入、删除元素的时间复杂度也是 $O(1)$，普通情况下插入、删除元素的时间复杂度为 $O(n)$。



### 练习题



#### [1.](https://datawhalechina.github.io/leetcode-notes/#/ch01/01.02/01.02.02-Exercises?id=_1-0066-加一)[0066. 加一](https://leetcode.cn/problems/plus-one/)

```python

def plusOne(self, digits: List[int]) -> List[int]:
    num = 0
    for i in range(len(digits)):  # 把列表转换成数字
        num = num * 10 + digits[i]
        num += 1  # 加一
        num_str = str(num)  # 把数字转换成字符串
        L = []
        for i in range(len(num_str)):  # 把字符串存入列表
            L.append(int(num_str[i]))
            return L

```

#### [2.](https://datawhalechina.github.io/leetcode-notes/#/ch01/01.02/01.02.02-Exercises?id=_2-0724-寻找数组的中心下标)[0724. 寻找数组的中心下标](https://leetcode.cn/problems/find-pivot-index/)

```python

def pivotIndex(self, nums: List[int]) -> int:
    total = sum(nums)
    left = 0
    for i in range(len(nums)):
        if left == (total - left - nums[i]):
            return i
        left += nums[i]
    else:
        return -1

```

#### [3.](https://datawhalechina.github.io/leetcode-notes/#/ch01/01.02/01.02.02-Exercises?id=_3-0189-轮转数组)[0189. 轮转数组](https://leetcode.cn/problems/rotate-array/)

```python

def rotate(self, nums: List[int], k: int) -> None:
    num = [0 for i in range(len(nums))]
    for i in range(len(nums)):
        num[(i+k) % len(nums)] = nums[i]
        nums[:] = num[:]

```

#### [4. 0048. 旋转图像](https://leetcode.cn/problems/rotate-image/)

```python
def rotate(self, matrix):  
        matrix[:] = map(list,zip(*matrix[::-1]))
```

#### [5.](https://datawhalechina.github.io/leetcode-notes/#/ch01/01.02/01.02.03-Exercises?id=_2-0054-螺旋矩阵)[0054. 螺旋矩阵](https://leetcode.cn/problems/spiral-matrix/)

```python
# 螺旋矩阵
def spiralMatrix(self, matrix):
    res = []
    if len(matrix) == 0: 
        return res
    top,bottom,left,right = 0,len(matrix)-1,0,len(matrix[0])-1 
    while top <= bottom and left <= right:
        for i in range(left, right+1): 
            res.append(matrix[top][i])
            top += 1 
            for i in range(top, bottom+1): 
                res.append(matrix[i][right])
                right -= 1 
                if top > bottom or left > right: 
                    break
                    for i in range(right, left-1, -1): 
                        res.append(matrix[bottom][i])
                        bottom -= 1 # 向左走完此轮，bottom++
                        for i in range(bottom, top-1, -1): 
                            res.append(matrix[i][left])
                            left += 1 # 向上走完此轮，left++
                            return res
 
```

#### [6.](https://datawhalechina.github.io/leetcode-notes/#/ch01/01.02/01.02.03-Exercises?id=_3-0498-对角线遍历)[0498. 对角线遍历](https://leetcode.cn/problems/diagonal-traverse/)

```python

    def findDiagonalOrder(self, matrix: List[List[int]]) -> List[int]:
        if not matrix or not matrix[0]:
            return []

        m, n = len(matrix), len(matrix[0])
        i, j, d1, d2 = 0, 0, -1, 1

        ans = []

        while len(ans) < m * n:
            ans.append(matrix[i][j])
            if 0 <= i + d1 < m and 0 <= j + d2 < n:
                i, j = i + d1, j + d2
            else:
                if j + d2 >= n:
                    i += 1
                elif i + d1 < 0:
                    j += 1
                elif i + d1 >= m:
                    j += 1
                elif j + d2 < 0:
                    i += 1
                d1, d2 = d2, d1

        return ans

```



## 附加数组基础知识题

#### [数组操作题目](https://datawhalechina.github.io/leetcode-notes/#/ch01/01.02/01.02.04-Array-Basic-List?id=数组操作题目)

| 题号 | 标题                                                         | 题解                                                         | 标签               | 难度 |
| ---- | ------------------------------------------------------------ | ------------------------------------------------------------ | ------------------ | ---- |
| 0189 | [轮转数组](https://leetcode.cn/problems/rotate-array/)       | [网页链接](https://datawhalechina.github.io/leetcode-notes/#/solutions/0189)、[Github 链接](https://github.com/datawhalechina/leetcode-notes/blob/main/docs/solutions/0189.md) | 数组、数学、双指针 | 中等 |
| 0066 | [加一](https://leetcode.cn/problems/plus-one/)               | [网页链接](https://datawhalechina.github.io/leetcode-notes/#/solutions/0066)、[Github 链接](https://github.com/datawhalechina/leetcode-notes/blob/main/docs/solutions/0066.md) | 数组、数学         | 简单 |
| 0724 | [寻找数组的中心下标](https://leetcode.cn/problems/find-pivot-index/) | [网页链接](https://datawhalechina.github.io/leetcode-notes/#/solutions/0724)、[Github 链接](https://github.com/datawhalechina/leetcode-notes/blob/main/docs/solutions/0724.md) | 数组、前缀和       | 简单 |
| 0485 | [最大连续 1 的个数](https://leetcode.cn/problems/max-consecutive-ones/) | [网页链接](https://datawhalechina.github.io/leetcode-notes/#/solutions/0485)、[Github 链接](https://github.com/datawhalechina/leetcode-notes/blob/main/docs/solutions/0485.md) | 数组               | 简单 |
| 0238 | [除自身以外数组的乘积](https://leetcode.cn/problems/product-of-array-except-self/) | [网页链接](https://datawhalechina.github.io/leetcode-notes/#/solutions/0238)、[Github 链接](https://github.com/datawhalechina/leetcode-notes/blob/main/docs/solutions/0238.md) | 数组、前缀和       | 中等 |

#### [二维数组题目](https://datawhalechina.github.io/leetcode-notes/#/ch01/01.02/01.02.04-Array-Basic-List?id=二维数组题目)

| 题号 | 标题                                                         | 题解                                                         | 标签               | 难度 |
| ---- | ------------------------------------------------------------ | ------------------------------------------------------------ | ------------------ | ---- |
| 0498 | [对角线遍历](https://leetcode.cn/problems/diagonal-traverse/) | [网页链接](https://datawhalechina.github.io/leetcode-notes/#/solutions/0498)、[Github 链接](https://github.com/datawhalechina/leetcode-notes/blob/main/docs/solutions/0498.md) | 数组、矩阵、模拟   | 中等 |
| 0048 | [旋转图像](https://leetcode.cn/problems/rotate-image/)       | [网页链接](https://datawhalechina.github.io/leetcode-notes/#/solutions/0048)、[Github 链接](https://github.com/datawhalechina/leetcode-notes/blob/main/docs/solutions/0048.md) | 数组、数学、矩阵   | 中等 |
| 0073 | [矩阵置零](https://leetcode.cn/problems/set-matrix-zeroes/)  | [网页链接](https://datawhalechina.github.io/leetcode-notes/#/solutions/0073)、[Github 链接](https://github.com/datawhalechina/leetcode-notes/blob/main/docs/solutions/0073.md) | 数组、哈希表、矩阵 | 中等 |
| 0054 | [螺旋矩阵](https://leetcode.cn/problems/spiral-matrix/)      | [网页链接](https://datawhalechina.github.io/leetcode-notes/#/solutions/0054)、[Github 链接](https://github.com/datawhalechina/leetcode-notes/blob/main/docs/solutions/0054.md) | 数组、矩阵、模拟   | 中等 |
| 0059 | [螺旋矩阵 II](https://leetcode.cn/problems/spiral-matrix-ii/) | [网页链接](https://datawhalechina.github.io/leetcode-notes/#/solutions/0059)、[Github 链接](https://github.com/datawhalechina/leetcode-notes/blob/main/docs/solutions/0059.md) | 数组、矩阵、模拟   | 中等 |
| 0289 | [生命游戏](https://leetcode.cn/problems/game-of-life/)       | [网页链接](https://datawhalechina.github.io/leetcode-notes/#/solutions/0289)、[Github 链接](https://github.com/datawhalechina/leetcode-notes/blob/main/docs/solutions/0289.md) | 数组、矩阵、模拟   | 中等 |