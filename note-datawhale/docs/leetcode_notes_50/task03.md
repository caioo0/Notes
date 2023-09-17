# task02数据排序

## 1. 冒泡排序

#### 定义：

经过多次迭代，通过相邻元素之间的比较与交换，使值较小的元素逐步从后面移到前面，值较大的元素从前面移到后面，这个过程就像气泡从底部升到顶部一样，因此得名冒泡排序。



#### 实现逻辑

- 比较相邻的元素。如果第一个比第二个大，就交换他们两个。
- 对每一对相邻元素作同样的工作，从开始第一对到结尾的最后一对。在这一点，最后的元素应该会是最大的数。
- 针对所有的元素重复以上的步骤，除了最后一个。
- 持续每次对越来越少的元素重复上面的步骤，直到没有任何一对数字需要比较。

通过两层循环控制：

- 第一个循环（外循环），负责把需要冒泡的那个数字排除在外；

- 第二个循环（内循环），负责两两比较交换。

  

![动图](.\img\v2-33a947c71ad62b254cab62e5364d2813_b.webp)

#### 代码实现：

```python
def bubble_sort(nums: list[int]):
    """冒泡排序"""
    n = len(nums)
    # 外循环：未排序区间为 [0, i]
    for i in range(n - 1, 0, -1):
        # 内循环：将未排序区间 [0, i] 中的最大元素交换至该区间的最右端
        for j in range(i):
            if nums[j] > nums[j + 1]:
                # 交换 nums[j] 与 nums[j + 1]
                nums[j], nums[j + 1] = nums[j + 1], nums[j]

```

泡排序的最差和平均时间复杂度仍为 $O(n^2)$ ；但当输入数组完全有序时，可达到最佳时间复杂度 $O(n)$ 

## 2. 选择排序

> 工作原理：开启一个循环，每轮从未排序区间选择最小的元素，将其放到已排序区间的末尾。

**选择排序(Selection sort)**是一种简单直观的排序算法。

#### 实现逻辑

> ① 第一轮从下标为 1 到下标为 n-1 的元素中选取最小值，若小于第一个数，则交换
> ② 第二轮从下标为 2 到下标为 n-1 的元素中选取最小值，若小于第二个数，则交换
> ③ 依次类推下去……

![动图](.\img\v2-1c7e20f306ddc02eb4e3a50fa7817ff4_b.webp)



#### 代码实现：

```python
def selection_sort(nums: list[int]):
    """选择排序"""
    n = len(nums)
    # 外循环：未排序区间为 [i, n-1]
    for i in range(n - 1):
        # 内循环：找到未排序区间内的最小元素
        k = i
        for j in range(i + 1, n):
            if nums[j] < nums[k]:
                k = j  # 记录最小元素的索引
        # 将该最小元素与未排序区间的首个元素交换
        nums[i], nums[k] = nums[k], nums[i]

```

## 3. 插入排序

#### 定义：

将数组分为两个区间：左侧为有序区间，右侧为无序区间。每趟从无序区间取出一个元素，然后将其插入到有序区间的适当位置。

插入排序 insertion sort是一种简单的排序算法，它的工作原理与手动整理一副牌的过程非常相似。

####  实现逻辑

> ① 从第一个元素开始，该元素可以认为已经被排序
> ② 取出下一个元素，在已经排序的元素序列中从后向前扫描
> ③如果该元素（已排序）大于新元素，将该元素移到下一位置
> ④ 重复步骤③，直到找到已排序的元素小于或者等于新元素的位置
> ⑤将新元素插入到该位置后
> ⑥ 重复步骤②~⑤

![动图](.\img\v2-91b76e8e4dab9b0cad9a017d7dd431e2_b.webp)

#### 代码实现

```python
def insertion_sort(nums: list[int]):
    """插入排序"""
    # 外循环：已排序区间为 [0, i-1]
    for i in range(1, len(nums)):
        base = nums[i]
        j = i - 1
        # 内循环：将 base 插入到已排序区间 [0, i-1] 中的正确位置
        while j >= 0 and nums[j] > base:
            nums[j + 1] = nums[j]  # 将 nums[j] 向右移动一位
            j -= 1
        nums[j + 1] = base  # 将 base 赋值到正确位置

```



## 4. 归并排序

#### 定义：

采用经典的分治策略，先递归地将当前数组平均分成两半，然后将有序数组两两合并，最终合并成一个有序数组。

归并排序是用分治思想，分治模式在每一层递归上有三个步骤：

- **分解（Divide）**：将n个元素分成个含n/2个元素的子序列。
- **解决（Conquer）**：用合并排序法对两个子序列递归的排序。
- **合并（Combine）**：合并两个已排序的子序列已得到排序结果。

#### 实现逻辑

**迭代法**

> ① 申请空间，使其大小为两个已经排序序列之和，该空间用来存放合并后的序列
> ② 设定两个指针，最初位置分别为两个已经排序序列的起始位置
> ③ 比较两个指针所指向的元素，选择相对小的元素放入到合并空间，并移动指针到下一位置
> ④ 重复步骤③直到某一指针到达序列尾
> ⑤ 将另一序列剩下的所有元素直接复制到合并序列尾

**递归法**

> ① 将序列每相邻两个数字进行归并操作，形成floor(n/2)个序列，排序后每个序列包含两个元素
> ② 将上述序列再次归并，形成floor(n/4)个序列，每个序列包含四个元素
> ③ 重复步骤②，直到所有元素排序完毕

![动图](.\img\v2-a29c0dd0186d1f8cef3c5ebdedf3e5a3_b.webp)

#### 代码实现

```python
def merge(nums: list[int], left: int, mid: int, right: int):
    """合并左子数组和右子数组"""
    # 左子数组区间 [left, mid]
    # 右子数组区间 [mid + 1, right]
    # 初始化辅助数组
    tmp = list(nums[left : right + 1])
    # 左子数组的起始索引和结束索引
    left_start = 0
    left_end = mid - left
    # 右子数组的起始索引和结束索引
    right_start = mid + 1 - left
    right_end = right - left
    # i, j 分别指向左子数组、右子数组的首元素
    i = left_start
    j = right_start
    # 通过覆盖原数组 nums 来合并左子数组和右子数组
    for k in range(left, right + 1):
        # 若“左子数组已全部合并完”，则选取右子数组元素，并且 j++
        if i > left_end:
            nums[k] = tmp[j]
            j += 1
        # 否则，若“右子数组已全部合并完”或“左子数组元素 <= 右子数组元素”，则选取左子数组元素，并且 i++
        elif j > right_end or tmp[i] <= tmp[j]:
            nums[k] = tmp[i]
            i += 1
        # 否则，若“左右子数组都未全部合并完”且“左子数组元素 > 右子数组元素”，则选取右子数组元素，并且 j++
        else:
            nums[k] = tmp[j]
            j += 1

def merge_sort(nums: list[int], left: int, right: int):
    """归并排序"""
    # 终止条件
    if left >= right:
        return  # 当子数组长度为 1 时终止递归
    # 划分阶段
    mid = (left + right) // 2  # 计算中点
    merge_sort(nums, left, mid)  # 递归左子数组
    merge_sort(nums, mid + 1, right)  # 递归右子数组
    # 合并阶段
    merge(nums, left, mid, right)

```



## 5. 希尔排序



## 6. 快速排序



## 7. 堆排序



## 8. 桶排序‘



## 9. 基数排序 



## 10.练习题

### [1.](https://datawhalechina.github.io/leetcode-notes/#/ch01/01.03/01.03.04-Exercises?id=_1-剑指-offer-45-把数组排成最小的数)[剑指 Offer 45. 把数组排成最小的数](https://leetcode.cn/problems/ba-shu-zu-pai-cheng-zui-xiao-de-shu-lcof/)

### [2.](https://datawhalechina.github.io/leetcode-notes/#/ch01/01.03/01.03.04-Exercises?id=_2-0283-移动零)[0283. 移动零](https://leetcode.cn/problems/move-zeroes/)

### [3.](https://datawhalechina.github.io/leetcode-notes/#/ch01/01.03/01.03.04-Exercises?id=_3-0912-排序数组)[0912. 排序数组](https://leetcode.cn/problems/sort-an-array/)

### [4.](https://datawhalechina.github.io/leetcode-notes/#/ch01/01.03/01.03.07-Exercises?id=_1-0506-相对名次)[0506. 相对名次](https://leetcode.cn/problems/relative-ranks/)

### [5.](https://datawhalechina.github.io/leetcode-notes/#/ch01/01.03/01.03.07-Exercises?id=_2-0088-合并两个有序数组)[0088. 合并两个有序数组](https://leetcode.cn/problems/merge-sorted-array/)

### [6.](https://datawhalechina.github.io/leetcode-notes/#/ch01/01.03/01.03.07-Exercises?id=_3-剑指-offer-51-数组中的逆序对)[剑指 Offer 51. 数组中的逆序对](https://leetcode.cn/problems/shu-zu-zhong-de-ni-xu-dui-lcof/)

### [7.](https://datawhalechina.github.io/leetcode-notes/#/ch01/01.03/01.03.10-Exercises?id=_1-0075-颜色分类)[0075. 颜色分类](https://leetcode.cn/problems/sort-colors/)

### [8.](https://datawhalechina.github.io/leetcode-notes/#/ch01/01.03/01.03.10-Exercises?id=_2-0215-数组中的第k个最大元素)[0215. 数组中的第K个最大元素](https://leetcode.cn/problems/kth-largest-element-in-an-array/)

### [9.](https://datawhalechina.github.io/leetcode-notes/#/ch01/01.03/01.03.10-Exercises?id=_3-剑指-offer-40-最小的k个数)[剑指 Offer 40. 最小的k个数](https://leetcode.cn/problems/zui-xiao-de-kge-shu-lcof/)

### [10.](https://datawhalechina.github.io/leetcode-notes/#/ch01/01.03/01.03.14-Exercises?id=_1-1122-数组的相对排序)[1122. 数组的相对排序](https://leetcode.cn/problems/relative-sort-array/)

### [11.](https://datawhalechina.github.io/leetcode-notes/#/ch01/01.03/01.03.14-Exercises?id=_2-0220-存在重复元素-iii)[0220. 存在重复元素 III](https://leetcode.cn/problems/contains-duplicate-iii/)

### [12.](https://datawhalechina.github.io/leetcode-notes/#/ch01/01.03/01.03.14-Exercises?id=_3-0164-最大间距)[0164. 最大间距](https://leetcode.cn/problems/maximum-gap/)

# [11. 排序算法题目](https://datawhalechina.github.io/leetcode-notes/#/ch01/01.03/01.03.15-Array-Sort-List?id=_010315-排序算法题目)

### [冒泡排序题目](https://datawhalechina.github.io/leetcode-notes/#/ch01/01.03/01.03.15-Array-Sort-List?id=冒泡排序题目)

| 题号          | 标题                                                         | 题解                                                         | 标签               | 难度 |
| ------------- | ------------------------------------------------------------ | ------------------------------------------------------------ | ------------------ | ---- |
| 剑指 Offer 45 | [把数组排成最小的数](https://leetcode.cn/problems/ba-shu-zu-pai-cheng-zui-xiao-de-shu-lcof/) | [网页链接](https://datawhalechina.github.io/leetcode-notes/#/solutions/Offer-45)、[Github 链接](https://github.com/datawhalechina/leetcode-notes/blob/main/docs/solutions/Offer-45.md) | 贪心、字符串、排序 | 中等 |
| 0283          | [移动零](https://leetcode.cn/problems/move-zeroes/)          | [网页链接](https://datawhalechina.github.io/leetcode-notes/#/solutions/0283)、[Github 链接](https://github.com/datawhalechina/leetcode-notes/blob/main/docs/solutions/0283.md) | 数组、双指针       | 简单 |

### [选择排序题目](https://datawhalechina.github.io/leetcode-notes/#/ch01/01.03/01.03.15-Array-Sort-List?id=选择排序题目)

| 题号 | 标题                                                         | 题解                                                         | 标签                                       | 难度 |
| ---- | ------------------------------------------------------------ | ------------------------------------------------------------ | ------------------------------------------ | ---- |
| 0215 | [数组中的第K个最大元素](https://leetcode.cn/problems/kth-largest-element-in-an-array/) | [网页链接](https://datawhalechina.github.io/leetcode-notes/#/solutions/0215)、[Github 链接](https://github.com/datawhalechina/leetcode-notes/blob/main/docs/solutions/0215.md) | 数组、分治、快速选择、排序、堆（优先队列） | 中等 |

### [插入排序题目](https://datawhalechina.github.io/leetcode-notes/#/ch01/01.03/01.03.15-Array-Sort-List?id=插入排序题目)

| 题号 | 标题                                                  | 题解                                                         | 标签               | 难度 |
| ---- | ----------------------------------------------------- | ------------------------------------------------------------ | ------------------ | ---- |
| 0075 | [颜色分类](https://leetcode.cn/problems/sort-colors/) | [网页链接](https://datawhalechina.github.io/leetcode-notes/#/solutions/0075)、[Github 链接](https://github.com/datawhalechina/leetcode-notes/blob/main/docs/solutions/0075.md) | 数组、双指针、排序 | 中等 |

### [希尔排序题目](https://datawhalechina.github.io/leetcode-notes/#/ch01/01.03/01.03.15-Array-Sort-List?id=希尔排序题目)

| 题号 | 标题                                                     | 题解                                                         | 标签                                                         | 难度 |
| ---- | -------------------------------------------------------- | ------------------------------------------------------------ | ------------------------------------------------------------ | ---- |
| 0912 | [排序数组](https://leetcode.cn/problems/sort-an-array/)  | [网页链接](https://datawhalechina.github.io/leetcode-notes/#/solutions/0912)、[Github 链接](https://github.com/datawhalechina/leetcode-notes/blob/main/docs/solutions/0912.md) | 数组、分治、桶排序、计数排序、基数排序、排序、堆（优先队列）、归并排序 | 中等 |
| 0506 | [相对名次](https://leetcode.cn/problems/relative-ranks/) | [网页链接](https://datawhalechina.github.io/leetcode-notes/#/solutions/0506)、[Github 链接](https://github.com/datawhalechina/leetcode-notes/blob/main/docs/solutions/0506.md) | 数组、排序、堆（优先队列）                                   | 简单 |

### [归并排序题目](https://datawhalechina.github.io/leetcode-notes/#/ch01/01.03/01.03.15-Array-Sort-List?id=归并排序题目)

| 题号          | 标题                                                         | 题解                                                         | 标签                                                         | 难度 |
| ------------- | ------------------------------------------------------------ | ------------------------------------------------------------ | ------------------------------------------------------------ | ---- |
| 0912          | [排序数组](https://leetcode.cn/problems/sort-an-array/)      | [网页链接](https://datawhalechina.github.io/leetcode-notes/#/solutions/0912)、[Github 链接](https://github.com/datawhalechina/leetcode-notes/blob/main/docs/solutions/0912.md) | 数组、分治、桶排序、计数排序、基数排序、排序、堆（优先队列）、归并排序 | 中等 |
| 0088          | [合并两个有序数组](https://leetcode.cn/problems/merge-sorted-array/) | [网页链接](https://datawhalechina.github.io/leetcode-notes/#/solutions/0088)、[Github 链接](https://github.com/datawhalechina/leetcode-notes/blob/main/docs/solutions/0088.md) | 数组、双指针、排序                                           | 简单 |
| 剑指 Offer 51 | [数组中的逆序对](https://leetcode.cn/problems/shu-zu-zhong-de-ni-xu-dui-lcof/) | [网页链接](https://datawhalechina.github.io/leetcode-notes/#/solutions/Offer-51)、[Github 链接](https://github.com/datawhalechina/leetcode-notes/blob/main/docs/solutions/Offer-51.md) | 树状数组、线段树、数组、二分查找、分治、有序集合、归并排序   | 困难 |
| 0315          | [计算右侧小于当前元素的个数](https://leetcode.cn/problems/count-of-smaller-numbers-after-self/) | [网页链接](https://datawhalechina.github.io/leetcode-notes/#/solutions/0315)、[Github 链接](https://github.com/datawhalechina/leetcode-notes/blob/main/docs/solutions/0315.md) | 树状数组、线段树、数组、二分查找、分治、有序集合、归并排序   | 困难 |

### [快速排序题目](https://datawhalechina.github.io/leetcode-notes/#/ch01/01.03/01.03.15-Array-Sort-List?id=快速排序题目)

| 题号 | 标题                                                       | 题解                                                         | 标签                                                         | 难度 |
| ---- | ---------------------------------------------------------- | ------------------------------------------------------------ | ------------------------------------------------------------ | ---- |
| 0912 | [排序数组](https://leetcode.cn/problems/sort-an-array/)    | [网页链接](https://datawhalechina.github.io/leetcode-notes/#/solutions/0912)、[Github 链接](https://github.com/datawhalechina/leetcode-notes/blob/main/docs/solutions/0912.md) | 数组、分治、桶排序、计数排序、基数排序、排序、堆（优先队列）、归并排序 | 中等 |
| 0169 | [多数元素](https://leetcode.cn/problems/majority-element/) | [网页链接](https://datawhalechina.github.io/leetcode-notes/#/solutions/0169)、[Github 链接](https://github.com/datawhalechina/leetcode-notes/blob/main/docs/solutions/0169.md) | 数组、哈希表、分治、计数、排序                               | 简单 |

### [堆排序题目](https://datawhalechina.github.io/leetcode-notes/#/ch01/01.03/01.03.15-Array-Sort-List?id=堆排序题目)

| 题号          | 标题                                                         | 题解                                                         | 标签                                                         | 难度 |
| ------------- | ------------------------------------------------------------ | ------------------------------------------------------------ | ------------------------------------------------------------ | ---- |
| 0912          | [排序数组](https://leetcode.cn/problems/sort-an-array/)      | [网页链接](https://datawhalechina.github.io/leetcode-notes/#/solutions/0912)、[Github 链接](https://github.com/datawhalechina/leetcode-notes/blob/main/docs/solutions/0912.md) | 数组、分治、桶排序、计数排序、基数排序、排序、堆（优先队列）、归并排序 | 中等 |
| 0215          | [数组中的第K个最大元素](https://leetcode.cn/problems/kth-largest-element-in-an-array/) | [网页链接](https://datawhalechina.github.io/leetcode-notes/#/solutions/0215)、[Github 链接](https://github.com/datawhalechina/leetcode-notes/blob/main/docs/solutions/0215.md) | 数组、分治、快速选择、排序、堆（优先队列）                   | 中等 |
| 剑指 Offer 40 | [最小的k个数](https://leetcode.cn/problems/zui-xiao-de-kge-shu-lcof/) | [网页链接](https://datawhalechina.github.io/leetcode-notes/#/solutions/Offer-40)、[Github 链接](https://github.com/datawhalechina/leetcode-notes/blob/main/docs/solutions/Offer-40.md) | 数组、分治、快速选择、排序、堆（优先队列）                   | 简单 |

### [计数排序题目](https://datawhalechina.github.io/leetcode-notes/#/ch01/01.03/01.03.15-Array-Sort-List?id=计数排序题目)

| 题号 | 标题                                                         | 题解                                                         | 标签                                                         | 难度 |
| ---- | ------------------------------------------------------------ | ------------------------------------------------------------ | ------------------------------------------------------------ | ---- |
| 0912 | [排序数组](https://leetcode.cn/problems/sort-an-array/)      | [网页链接](https://datawhalechina.github.io/leetcode-notes/#/solutions/0912)、[Github 链接](https://github.com/datawhalechina/leetcode-notes/blob/main/docs/solutions/0912.md) | 数组、分治、桶排序、计数排序、基数排序、排序、堆（优先队列）、归并排序 | 中等 |
| 1122 | [数组的相对排序](https://leetcode.cn/problems/relative-sort-array/) | [网页链接](https://datawhalechina.github.io/leetcode-notes/#/solutions/1122)、[Github 链接](https://github.com/datawhalechina/leetcode-notes/blob/main/docs/solutions/1122.md) | 数组、哈希表、计数排序、排序                                 | 简单 |
| 0561 | [数组拆分](https://leetcode.cn/problems/array-partition/)    | [网页链接](https://datawhalechina.github.io/leetcode-notes/#/solutions/0561)、[Github 链接](https://github.com/datawhalechina/leetcode-notes/blob/main/docs/solutions/0561.md) | 贪心、数组、计数排序、排序                                   | 简单 |

### [桶排序题目](https://datawhalechina.github.io/leetcode-notes/#/ch01/01.03/01.03.15-Array-Sort-List?id=桶排序题目)

| 题号 | 标题                                                         | 题解                                                         | 标签                                                         | 难度 |
| ---- | ------------------------------------------------------------ | ------------------------------------------------------------ | ------------------------------------------------------------ | ---- |
| 0912 | [排序数组](https://leetcode.cn/problems/sort-an-array/)      | [网页链接](https://datawhalechina.github.io/leetcode-notes/#/solutions/0912)、[Github 链接](https://github.com/datawhalechina/leetcode-notes/blob/main/docs/solutions/0912.md) | 数组、分治、桶排序、计数排序、基数排序、排序、堆（优先队列）、归并排序 | 中等 |
| 0220 | [存在重复元素 III](https://leetcode.cn/problems/contains-duplicate-iii/) | [网页链接](https://datawhalechina.github.io/leetcode-notes/#/solutions/0220)、[Github 链接](https://github.com/datawhalechina/leetcode-notes/blob/main/docs/solutions/0220.md) | 数组、桶排序、有序集合、排序、滑动窗口                       | 困难 |
| 0164 | [最大间距](https://leetcode.cn/problems/maximum-gap/)        | [网页链接](https://datawhalechina.github.io/leetcode-notes/#/solutions/0164)、[Github 链接](https://github.com/datawhalechina/leetcode-notes/blob/main/docs/solutions/0164.md) | 数组、桶排序、基数排序、排序                                 | 困难 |

### [基数排序题目](https://datawhalechina.github.io/leetcode-notes/#/ch01/01.03/01.03.15-Array-Sort-List?id=基数排序题目)

| 题号 | 标题                                                  | 题解                                                         | 标签                         | 难度 |
| ---- | ----------------------------------------------------- | ------------------------------------------------------------ | ---------------------------- | ---- |
| 0164 | [最大间距](https://leetcode.cn/problems/maximum-gap/) | [网页链接](https://datawhalechina.github.io/leetcode-notes/#/solutions/0164)、[Github 链接](https://github.com/datawhalechina/leetcode-notes/blob/main/docs/solutions/0164.md) | 数组、桶排序、基数排序、排序 | 困难 |

### [其他排序题目](https://datawhalechina.github.io/leetcode-notes/#/ch01/01.03/01.03.15-Array-Sort-List?id=其他排序题目)

| 题号          | 标题                                                         | 题解                                                         | 标签                     | 难度 |
| ------------- | ------------------------------------------------------------ | ------------------------------------------------------------ | ------------------------ | ---- |
| 0217          | [存在重复元素](https://leetcode.cn/problems/contains-duplicate/) | [网页链接](https://datawhalechina.github.io/leetcode-notes/#/solutions/0217)、[Github 链接](https://github.com/datawhalechina/leetcode-notes/blob/main/docs/solutions/0217.md) | 数组、哈希表、排序       | 简单 |
| 0136          | [只出现一次的数字](https://leetcode.cn/problems/single-number/) | [网页链接](https://datawhalechina.github.io/leetcode-notes/#/solutions/0136)、[Github 链接](https://github.com/datawhalechina/leetcode-notes/blob/main/docs/solutions/0136.md) | 位运算、数组             | 简单 |
| 0056          | [合并区间](https://leetcode.cn/problems/merge-intervals/)    | [网页链接](https://datawhalechina.github.io/leetcode-notes/#/solutions/0056)、[Github 链接](https://github.com/datawhalechina/leetcode-notes/blob/main/docs/solutions/0056.md) | 数组、排序               | 中等 |
| 0179          | [最大数](https://leetcode.cn/problems/largest-number/)       | [网页链接](https://datawhalechina.github.io/leetcode-notes/#/solutions/0179)、[Github 链接](https://github.com/datawhalechina/leetcode-notes/blob/main/docs/solutions/0179.md) | 贪心、数组、字符串、排序 | 中等 |
| 0384          | [打乱数组](https://leetcode.cn/problems/shuffle-an-array/)   | [网页链接](https://datawhalechina.github.io/leetcode-notes/#/solutions/0384)、[Github 链接](https://github.com/datawhalechina/leetcode-notes/blob/main/docs/solutions/0384.md) | 数组、数学、随机化       | 中等 |
| 剑指 Offer 45 | [把数组排成最小的数](https://leetcode.cn/problems/ba-shu-zu-pai-cheng-zui-xiao-de-shu-lcof/) | [网页链接](https://datawhalechina.github.io/leetcode-notes/#/solutions/Offer-45)、[Github 链接](https://github.com/datawhalechina/leetcode-notes/blob/main/docs/solutions/Offer-45.md) | 贪心、字符串、排序       | 中等 |