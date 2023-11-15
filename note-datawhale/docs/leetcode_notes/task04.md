# task04: 数组二分查询

>  关于笔记，主要来自[datawhale-Leetcode算法笔记](https://datawhalechina.github.io/leetcode-notes/#/ch01/01.01/01.01.02-Algorithm-Complexity)

## 算法解释

二分查找算法(Binary Search Algorithm) : 也叫折半查找算法，对数查找算法，每次查找时通过将待查找区间分成两部分并只取一部分继续查找，将查询的复杂度大大减少。对于一个长度为$O(n)$的数组，二分查找的时间复杂度$0(logn)$。

#### **二分查找前提**

1. 查找的**数据目标**需要是**有顺序的储存结构**，比如Python中的列表`list`。
2. 这个**数据目标**还需要**按一个顺序排列**（升序or降序）
3. 二分查找区间的左右端取**开区间或者闭区间**在绝大多数时候都可以,一般建议采用"双闭区间"的写法。

## 实现逻辑

**用一个动画来体现，这个动画效果揭示了可能找不到答案：**



![动图](https://pic3.zhimg.com/v2-580def5b0d44690823114c1203435b4a_b.webp)





#### **二分查找的局限性**

- 二分查找依赖数组结构

- 二分查找针对的是有序数据

- 数据量太小不适合二分查找

- 数据量太大不适合二分查找


## **代码实现**

### 1. 非递归直接法

直接法思想是再循环体中找到元素后直接返回结果。可谓简单粗暴：

```python
def binary_search(list,item):

    # 列表的头和尾，代表着数组范围的最小和最大
    low = 0
    high = len(list) - 1

    # 当找到item的时候，low是小于high，也有可能相等
    while low <= high:
        mid = (low + high)//2  # // 所代表的含义是「中间数向下取整」
        # 取数组的中间值
        guess = list[mid]
        # 如果中间值等于索引值，那么就返回中间值的下标
        if guess == item:
            return mid
        # 如果中间值>索引值，因为不包含中间值，所以最大范围high=中间值的下标往左移1位
        if guess > item:
            high = mid - 1
        # 如果中间值<索引值，因为不包含中间值，所以最小范围low=中间值的下标往右移1位
        else:
            low = mid + 1   
    return None
    
my_list = [1, 3, 5, 7,8, 9]
print(binary_search(my_list,3))
```

**时间复杂度$O(logn)$：**在二分循环中，区间每轮缩小一半，循环次数为 $log_2⁡n$ 。

**空间复杂度 $O(1)$** ：指针 low 和 high 使用常数大小空间。

### 2.递归实现

递归思想

```python
def binary_search(list,data):
    n = len(list)
    mid = n // 2
    if list[mid] > data:
        return binary_search(list[0:mid],data)
    elif list[mid] < data:
        return binary_search(list[mid+1:],data)
    else:
        return mid
```

## 练习题

#### [704. 二分查找](https://leetcode.cn/problems/binary-search/)



```python
class Solution:
    def search(self, nums: List[int], target: int) -> int:
        left, right = 0, len(nums) - 1
        
        # 在区间 [left, right] 内查找 target
        while left <= right:
            # 取区间中间节点
            mid = (left + right) // 2
            # 如果找到目标值，则直接返回中心位置
            if nums[mid] == target:
                return mid
            # 如果 nums[mid] 小于目标值，则在 [mid + 1, right] 中继续搜索
            elif nums[mid] < target:
                left = mid + 1
            # 如果 nums[mid] 大于目标值，则在 [left, mid - 1] 中继续搜索
            else:
                right = mid - 1
        # 未搜索到元素，返回 -1
        return -1

```

#### [0035. 搜索插入位置](https://leetcode.cn/problems/search-insert-position/)

```python
class Solution:
    def searchInsert(self, nums: List[int], target: int) -> int:


        low, high = 0, len(nums) - 1

        # 在 [low, high] 找 target
        while low <= high:

            mid = (low + high) // 2

            # 如果 target 找到，直接返回位置
            if nums[mid] == target:
                return mid
            # 如果 target 大于中间数，则 target 可能在右区间
            # 在 [mid + 1, left] 中找
            elif nums[mid] < target:
                low = mid + 1
            # 如果 target 小于中间数，则 target 可能在左区间
            # 在 [left, mid -1] 中找
            else:
                high = mid - 1
        
        # 如果在数组中没找到，则返回需要插入数值的位置
        return high + 1
```

#### [0374. 猜数字大小](https://leetcode.cn/problems/guess-number-higher-or-lower/)

```python
class Solution:
    def guessNumber(self, n: int) -> int:
        left,right = 1,n
        while left <= right:
            mid = (left + right)//2
            if guess(mid) == 0:
                return mid
            elif guess(mid) == 1:
                left = mid + 1
            else:
                right = mid - 1
        return -1
```

#### [0069. x 的平方根](https://leetcode.cn/problems/sqrtx/)

```
class Solution:
    def mySqrt(self, x: int) -> int:
        # 明显是二分查找
        l, r = 0, x

        while l < r:
            mid = (l + r + 1) >> 1
            if mid * mid <= x:
                l = mid
            else:
                r = mid - 1
        
        return l

```

#### [0167. 两数之和 II - 输入有序数组](https://leetcode.cn/problems/two-sum-ii-input-array-is-sorted/)

```python
class Solution:
    def twoSum(self, numbers: List[int], target: int) -> List[int]:
        n = len(numbers)
        for i in range(n):
            left, right = i+1, n  # 采用左闭右开区间[left,right),left+1避免重复
            while left < right: # 右开所以不能有=,区间不存在
                mid = (right - left) // 2 + left # 防止溢出
                if numbers[mid] == target - numbers[i]: # 数组中存在重复元素,必须判断相等
                    return [i + 1, mid + 1] # 返回的下标从1开始,都+1
                elif numbers[mid] > target - numbers[i]:
                    right = mid # 右开,真正右端点为mid-1
                else:
                    left = mid + 1 # 左闭,所以要+1
        
        return [-1, -1]
```



#### [1011. 在 D 天内送达包裹的能力](https://leetcode.cn/problems/capacity-to-ship-packages-within-d-days/)

```python
class Solution:
    def shipWithinDays(self, weights: List[int], days: int) -> int:
        total = sum(weights)
        left, right = max(weights), total

        while left <= right:
            mid = (left+right)//2

            # 计算天数
            cur = 0
            summ = 0
            day = 1
            while cur < len(weights):
                summ += weights[cur]
                if summ > mid: # 注意这里，如果下一个物体上船会超载的话，只能第二天再装，因此天数+1
                    summ = weights[cur]
                    day += 1
                cur += 1

            # 二分迭代条件
            if day > days:
                left = mid + 1
            else:
                right = mid - 1

        return left
```



#### [0278. 第一个错误的版本](https://leetcode.cn/problems/first-bad-version/)

```python
class Solution:
    def firstBadVersion(self, n):
        """
        :type n: int
        :rtype: int
        """
        left, right = 1, n
        while left < right:
            mid = (left + right) // 2
            if isBadVersion(mid):
                right = mid
            else:
                left = mid + 1
        return left
```



#### [0033. 搜索旋转排序数组](https://leetcode.cn/problems/search-in-rotated-sorted-array/)

```python
class Solution:
    def search(self, nums: List[int], target: int) -> int:
        n = len(nums) #计算nums的长度
        if n == 1 and nums[0] == target: #首先判断特殊情况，只有一个元素的情况
            return 0
        p, q = 0, n - 1 #二分法设定边界
        while p < q: #开始二分寻找
            mid = p + (q - p) // 2 #首先计算二分点，为了防止（p + q）溢出，均是利用这样的公式获取中间点
            if nums[0] <= nums[mid]: #这就说明mid的左边没有旋转后的数据，因为一旦旋转了，数组的第一个数nums[0]必然要比mid位置的值大，此时说明mid左边的值是有序的
                p = mid + 1 #此时说明拐点在mid的右边，更新左边界
            else:#反之更新右边界，继续寻找拐点
                q = mid 
        if nums[0] <= target <= nums[p - 1]: #此时得到的p就是最小值所在的索引，此时判断一下target在那个区间中
            i, j = 0, p - 1 #如果在最小值的左边，则将左边的边界设为左右边界
        elif nums[p] <= target <= nums[n - 1]:
            i, j = p, n - 1 #反之右边的边界设为左右边界
        else:
            return -1 #说明target不在这个范围，返回-1
        while i < j: #进行二分法判断
            mid = i + (j - i) // 2 # #首先计算二分点，为了防止（p + q）溢出，均是利用这样的公式获取中间点
            if nums[mid] > target: #如果target比nums[mid]小，更新右边界
                j = mid - 1
            elif nums[mid] == target:#反之更新左边界
                return mid
            else:
                i = mid + 1
        if nums[j] == target: #此时判断一下我们得到的j处索引的值是否与target相等
            return j
        return -1
```



#### [0153. 寻找旋转排序数组中的最小值](https://leetcode.cn/problems/find-minimum-in-rotated-sorted-array/)

```python
class Solution:
    def findMin(self, nums: List[int]) -> int:
        left = 0
        right = len(nums) - 1 
        while left < right:
            mid = left + (right - left) // 2
            if nums[right] < nums[mid]:
                left = mid + 1
            else:
                right = mid 
        return nums[left]

```



# 二分查找题目

#### 二分下标题目

| 题号 | 标题                                                         | 题解                                                         | 标签                       | 难度 |
| :--- | :----------------------------------------------------------- | :----------------------------------------------------------- | :------------------------- | :--- |
| 0704 | [二分查找](https://leetcode.cn/problems/binary-search/)      | [网页链接](https://datawhalechina.github.io/leetcode-notes/#/solutions/0704)、[Github 链接](https://github.com/datawhalechina/leetcode-notes/blob/main/docs/solutions/0704.md) | 数组、二分查找             | 简单 |
| 0374 | [猜数字大小](https://leetcode.cn/problems/guess-number-higher-or-lower/) | [网页链接](https://datawhalechina.github.io/leetcode-notes/#/solutions/0374)、[Github 链接](https://github.com/datawhalechina/leetcode-notes/blob/main/docs/solutions/0374.md) | 二分查找、交互             | 简单 |
| 0035 | [搜索插入位置](https://leetcode.cn/problems/search-insert-position/) | [网页链接](https://datawhalechina.github.io/leetcode-notes/#/solutions/0035)、[Github 链接](https://github.com/datawhalechina/leetcode-notes/blob/main/docs/solutions/0035.md) | 数组、二分查找             | 简单 |
| 0034 | [在排序数组中查找元素的第一个和最后一个位置](https://leetcode.cn/problems/find-first-and-last-position-of-element-in-sorted-array/) | [网页链接](https://datawhalechina.github.io/leetcode-notes/#/solutions/0034)、[Github 链接](https://github.com/datawhalechina/leetcode-notes/blob/main/docs/solutions/0034.md) | 数组、二分查找             | 中等 |
| 0167 | [两数之和 II - 输入有序数组](https://leetcode.cn/problems/two-sum-ii-input-array-is-sorted/) | [网页链接](https://datawhalechina.github.io/leetcode-notes/#/solutions/0167)、[Github 链接](https://github.com/datawhalechina/leetcode-notes/blob/main/docs/solutions/0167.md) | 数组、双指针、二分查找     | 中等 |
| 0153 | [寻找旋转排序数组中的最小值](https://leetcode.cn/problems/find-minimum-in-rotated-sorted-array/) | [网页链接](https://datawhalechina.github.io/leetcode-notes/#/solutions/0153)、[Github 链接](https://github.com/datawhalechina/leetcode-notes/blob/main/docs/solutions/0153.md) | 数组、二分查找             | 中等 |
| 0154 | [寻找旋转排序数组中的最小值 II](https://leetcode.cn/problems/find-minimum-in-rotated-sorted-array-ii/) | [网页链接](https://datawhalechina.github.io/leetcode-notes/#/solutions/0154)、[Github 链接](https://github.com/datawhalechina/leetcode-notes/blob/main/docs/solutions/0154.md) | 数组、二分查找             | 困难 |
| 0033 | [搜索旋转排序数组](https://leetcode.cn/problems/search-in-rotated-sorted-array/) | [网页链接](https://datawhalechina.github.io/leetcode-notes/#/solutions/0033)、[Github 链接](https://github.com/datawhalechina/leetcode-notes/blob/main/docs/solutions/0033.md) | 数组、二分查找             | 中等 |
| 0081 | [搜索旋转排序数组 II](https://leetcode.cn/problems/search-in-rotated-sorted-array-ii/) | [网页链接](https://datawhalechina.github.io/leetcode-notes/#/solutions/0081)、[Github 链接](https://github.com/datawhalechina/leetcode-notes/blob/main/docs/solutions/0081.md) | 数组、二分查找             | 中等 |
| 0278 | [第一个错误的版本](https://leetcode.cn/problems/first-bad-version/) | [网页链接](https://datawhalechina.github.io/leetcode-notes/#/solutions/0278)、[Github 链接](https://github.com/datawhalechina/leetcode-notes/blob/main/docs/solutions/0278.md) | 二分查找、交互             | 简单 |
| 0162 | [寻找峰值](https://leetcode.cn/problems/find-peak-element/)  | [网页链接](https://datawhalechina.github.io/leetcode-notes/#/solutions/0162)、[Github 链接](https://github.com/datawhalechina/leetcode-notes/blob/main/docs/solutions/0162.md) | 数组、二分查找             | 中等 |
| 0852 | [山脉数组的峰顶索引](https://leetcode.cn/problems/peak-index-in-a-mountain-array/) | [网页链接](https://datawhalechina.github.io/leetcode-notes/#/solutions/0852)、[Github 链接](https://github.com/datawhalechina/leetcode-notes/blob/main/docs/solutions/0852.md) | 数组、二分查找             | 中等 |
| 1095 | [山脉数组中查找目标值](https://leetcode.cn/problems/find-in-mountain-array/) | [网页链接](https://datawhalechina.github.io/leetcode-notes/#/solutions/1095)、[Github 链接](https://github.com/datawhalechina/leetcode-notes/blob/main/docs/solutions/1095.md) | 数组、二分查找、交互       | 困难 |
| 0744 | [寻找比目标字母大的最小字母](https://leetcode.cn/problems/find-smallest-letter-greater-than-target/) | [网页链接](https://datawhalechina.github.io/leetcode-notes/#/solutions/0744)、[Github 链接](https://github.com/datawhalechina/leetcode-notes/blob/main/docs/solutions/0744.md) | 数组、二分查找             | 简单 |
| 0004 | [寻找两个正序数组的中位数](https://leetcode.cn/problems/median-of-two-sorted-arrays/) | [网页链接](https://datawhalechina.github.io/leetcode-notes/#/solutions/0004)、[Github 链接](https://github.com/datawhalechina/leetcode-notes/blob/main/docs/solutions/0004.md) | 数组、二分查找、分治       | 困难 |
| 0074 | [搜索二维矩阵](https://leetcode.cn/problems/search-a-2d-matrix/) | [网页链接](https://datawhalechina.github.io/leetcode-notes/#/solutions/0074)、[Github 链接](https://github.com/datawhalechina/leetcode-notes/blob/main/docs/solutions/0074.md) | 数组、二分查找、矩阵       | 中等 |
| 0240 | [搜索二维矩阵 II](https://leetcode.cn/problems/search-a-2d-matrix-ii/) | [网页链接](https://datawhalechina.github.io/leetcode-notes/#/solutions/0240)、[Github 链接](https://github.com/datawhalechina/leetcode-notes/blob/main/docs/solutions/0240.md) | 数组、二分查找、分治、矩阵 | 中等 |

#### 二分答案题目

| 题号 | 标题                                                         | 题解                                                         | 标签                           | 难度 |
| :--- | :----------------------------------------------------------- | :----------------------------------------------------------- | :----------------------------- | :--- |
| 0069 | [x 的平方根](https://leetcode.cn/problems/sqrtx/)            | [网页链接](https://datawhalechina.github.io/leetcode-notes/#/solutions/0069)、[Github 链接](https://github.com/datawhalechina/leetcode-notes/blob/main/docs/solutions/0069.md) | 数学、二分查找                 | 简单 |
| 0287 | [寻找重复数](https://leetcode.cn/problems/find-the-duplicate-number/) | [网页链接](https://datawhalechina.github.io/leetcode-notes/#/solutions/0287)、[Github 链接](https://github.com/datawhalechina/leetcode-notes/blob/main/docs/solutions/0287.md) | 位运算、数组、双指针、二分查找 | 中等 |
| 0050 | [Pow(x, n)](https://leetcode.cn/problems/powx-n/)            | [网页链接](https://datawhalechina.github.io/leetcode-notes/#/solutions/0050)、[Github 链接](https://github.com/datawhalechina/leetcode-notes/blob/main/docs/solutions/0050.md) | 递归、数学                     | 中等 |
| 0367 | [有效的完全平方数](https://leetcode.cn/problems/valid-perfect-square/) | [网页链接](https://datawhalechina.github.io/leetcode-notes/#/solutions/0367)、[Github 链接](https://github.com/datawhalechina/leetcode-notes/blob/main/docs/solutions/0367.md) | 数学、二分查找                 | 简单 |
| 1300 | [转变数组后最接近目标值的数组和](https://leetcode.cn/problems/sum-of-mutated-array-closest-to-target/) | [网页链接](https://datawhalechina.github.io/leetcode-notes/#/solutions/1300)、[Github 链接](https://github.com/datawhalechina/leetcode-notes/blob/main/docs/solutions/1300.md) | 数组、二分查找、排序           | 中等 |
| 0400 | [第 N 位数字](https://leetcode.cn/problems/nth-digit/)       | [网页链接](https://datawhalechina.github.io/leetcode-notes/#/solutions/0400)、[Github 链接](https://github.com/datawhalechina/leetcode-notes/blob/main/docs/solutions/0400.md) | 数学、二分查找                 | 中等 |

#### 复杂的二分查找问题

| 题号 | 标题                                                         | 题解                                                         | 标签                                                   | 难度 |
| :--- | :----------------------------------------------------------- | :----------------------------------------------------------- | :----------------------------------------------------- | :--- |
| 0875 | [爱吃香蕉的珂珂](https://leetcode.cn/problems/koko-eating-bananas/) |                                                              | 数组、二分查找                                         | 中等 |
| 0410 | [分割数组的最大值](https://leetcode.cn/problems/split-array-largest-sum/) |                                                              | 贪心、数组、二分查找、动态规划、前缀和                 | 困难 |
| 0209 | [长度最小的子数组](https://leetcode.cn/problems/minimum-size-subarray-sum/) | [网页链接](https://datawhalechina.github.io/leetcode-notes/#/solutions/0209)、[Github 链接](https://github.com/datawhalechina/leetcode-notes/blob/main/docs/solutions/0209.md) | 数组、二分查找、前缀和、滑动窗口                       | 中等 |
| 0658 | [找到 K 个最接近的元素](https://leetcode.cn/problems/find-k-closest-elements/) |                                                              | 数组、双指针、二分查找、排序、滑动窗口、堆（优先队列） | 中等 |
| 0270 | [最接近的二叉搜索树值](https://leetcode.cn/problems/closest-binary-search-tree-value/) |                                                              | 树、深度优先搜索、二叉搜索树、二分查找、二叉树         | 简单 |
| 0702 | [搜索长度未知的有序数组](https://leetcode.cn/problems/search-in-a-sorted-array-of-unknown-size/) |                                                              | 数组、二分查找、交互                                   | 中等 |
| 0349 | [两个数组的交集](https://leetcode.cn/problems/intersection-of-two-arrays/) | [网页链接](https://datawhalechina.github.io/leetcode-notes/#/solutions/0349)、[Github 链接](https://github.com/datawhalechina/leetcode-notes/blob/main/docs/solutions/0349.md) | 数组、哈希表、双指针、二分查找、排序                   | 简单 |
| 0350 | [两个数组的交集 II](https://leetcode.cn/problems/intersection-of-two-arrays-ii/) |                                                              | 数组、哈希表、双指针、二分查找、排序                   | 简单 |
| 0287 | [寻找重复数](https://leetcode.cn/problems/find-the-duplicate-number/) | [网页链接](https://datawhalechina.github.io/leetcode-notes/#/solutions/0287)、[Github 链接](https://github.com/datawhalechina/leetcode-notes/blob/main/docs/solutions/0287.md) | 位运算、数组、双指针、二分查找                         | 中等 |
| 0719 | [找出第 K 小的数对距离](https://leetcode.cn/problems/find-k-th-smallest-pair-distance/) |                                                              | 数组、双指针、二分查找、排序                           | 困难 |
| 0259 | [较小的三数之和](https://leetcode.cn/problems/3sum-smaller/) |                                                              | 数组、双指针、二分查找、排序                           | 中等 |
| 1011 | [在 D 天内送达包裹的能力](https://leetcode.cn/problems/capacity-to-ship-packages-within-d-days/) | [网页链接](https://datawhalechina.github.io/leetcode-notes/#/solutions/1011)、[Github 链接](https://github.com/datawhalechina/leetcode-notes/blob/main/docs/solutions/1011.md) | 数组、二分查找                                         | 中等 |
| 1482 | [制作 m 束花所需的最少天数](https://leetcode.cn/problems/minimum-number-of-days-to-make-m-bouquets/) |                                                              | 数组、二分查找                                         | 中等 |

## 参考资料

1.[Hello-算法](https://www.hello-algo.com/chapter_computational_complexity/time_complexity/#234)

2.[datawhale-Leetcode算法笔记](https://datawhalechina.github.io/leetcode-notes/#/ch01/01.01/01.01.02-Algorithm-Complexity)