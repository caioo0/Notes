# task03数据排序

>  关于笔记，主要来自[datawhale-Leetcode算法笔记](https://datawhalechina.github.io/leetcode-notes/#/ch01/01.01/01.01.02-Algorithm-Complexity)

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

#### 定义：

将整个数组切按照一定的间隔取值划分为若干个子数组，每个子数组分别进行插入排序。然后逐渐缩小间隔进行下一轮划分子数组和对子数组进行插入排序。直至最后一轮排序间隔为 1，对整个数组进行插入排序。



希尔排序的实质就是分组插入排序，该方法又称递减增量排序算法，因DL．Shell于1959年提出而得名。希尔排序是非稳定的排序算法。

希尔排序是基于插入排序的以下两点性质而提出改进方法的：

> 插入排序在对几乎已经排好序的数据操作时，效率高，即可以达到线性排序的效率但插入排序一般来说是低效的，因为插入排序每次只能将数据移动一位  

#### 实现逻辑

> ① 先取一个小于n的整数d1作为第一个增量，把文件的全部记录分成d1个组。  
> ② 所有距离为d1的倍数的记录放在同一个组中，在各组内进行直接插入排序。  
> ③ 取第二个增量d2小于d1重复上述的分组和排序，直至所取的增量dt=1(dt小于dt-l小于…小于d2小于d1)，即所有记录放在同一组中进行直接插入排序为止。

![动图](.\img\v2-f9616f6892819e579a2d4ab10256a732_b.webp)

#### 代码实现

```python
class Solution:
    def shellSort(self, nums: [int]) -> [int]:
        size = len(nums)
        gap = size // 2
        # 按照 gap 分组
        while gap > 0:
            # 对每组元素进行插入排序
            for i in range(gap, size):
                # temp 为每组中无序数组第 1 个元素
                temp = nums[i]
                j = i
                # 从右至左遍历每组中的有序数组元素
                while j >= gap and nums[j - gap] > temp:
                    # 将每组有序数组中插入位置右侧的元素依次在组中右移一位
                    nums[j] = nums[j - gap]
                    j -= gap
                # 将该元素插入到适当位置
                nums[j] = temp
            # 缩小 gap 间隔
            gap = gap // 2
        return nums

    def sortArray(self, nums: [int]) -> [int]:
        return self.shellSort(nums)
    
print(Solution().sortArray([7, 2, 6, 8, 0, 4, 1, 5, 9, 3]))

```



## 6. 快速排序

快速排序，又称划分交换排序（partition-exchange sort）

#### 定义

通过一趟排序将待排记录分隔成独立的两部分，其中一部分记录的关键字均比另一部分的关键字小，则可分别对这两部分记录继续进行排序，以达到整个序列有序。

#### 实现逻辑

快速排序使用分治法（Divide and conquer）策略来把一个序列（list）分为两个子序列（sub-lists）。

> ① 从数列中挑出一个元素，称为 “基准”（pivot），  
> ② 重新排序数列，所有元素比基准值小的摆放在基准前面，所有元素比基准值大的摆在基准的后面（相同的数可以到任一边）。在这个分区退出之后，该基准就处于数列的中间位置。这个称为分区（partition）操作。  
> ③ 递归地（recursive）把小于基准值元素的子数列和大于基准值元素的子数列排序。  

递归到最底部时，数列的大小是零或一，也就是已经排序好了。这个算法一定会结束，因为在每次的迭代（iteration）中，它至少会把一个元素摆到它最后的位置去。

![动图](.\img\v2-d4e5d0a778dba725091d8317e6bac939_b.webp)

#### 代码实现

```python
def partition(self, nums: list[int], left: int, right: int) -> int:
    """哨兵划分"""
    # 以 nums[left] 作为基准数
    i, j = left, right
    while i < j:
        while i < j and nums[j] >= nums[left]:
            j -= 1  # 从右向左找首个小于基准数的元素
        while i < j and nums[i] <= nums[left]:
            i += 1  # 从左向右找首个大于基准数的元素
        # 元素交换
        nums[i], nums[j] = nums[j], nums[i]
    # 将基准数交换至两子数组的分界线
    nums[i], nums[left] = nums[left], nums[i]
    return i  # 返回基准数的索引

```



## 7. 堆排序

#### 堆的概念

堆一般指的是二叉堆，顾名思义，二叉堆是完全二叉树或者近似完全二叉树

##### 堆的性质

> ① 是一棵完全二叉树  
> ② 每个节点的值都大于或等于其子节点的值，为最大堆；反之为最小堆。  

##### 堆的存储

一般用数组来表示堆，下标为 i 的结点的父结点下标为(i-1)/2；其左右子结点分别为 (2i + 1)、(2i + 2)

##### 堆的操作

在堆的数据结构中，堆中的最大值总是位于根节点(在优先队列中使用堆的话堆中的最小值位于根节点)。堆中定义以下几种操作：

> ① **最大堆调整（Max_Heapify）**：将堆的末端子节点作调整，使得子节点永远小于父节点  
> ② **创建最大堆（Build_Max_Heap）**：将堆所有数据重新排序  
> ③ **堆排序（HeapSort）**：移除位在第一个数据的根节点，并做最大堆调整的递归运算   

#### 定义



「堆排序 heap sort」是一种基于堆数据结构实现的高效排序算法。我们可以利用已经学过的“建堆操作”和“元素出堆操作”实现堆排序。

1. 输入数组并建立小顶堆，此时最小元素位于堆顶。
2. 不断执行出堆操作，依次记录出堆元素，即可得到从小到大排序的序列。

以上方法虽然可行，但需要借助一个额外数组来保存弹出的元素，比较浪费空间。在实际中，我们通常使用一种更加优雅的实现方式。



#### 实现逻辑

> ① 先将初始的R[0…n-1]建立成最大堆，此时是无序堆，而堆顶是最大元素。  
> ② 再将堆顶R[0]和无序区的最后一个记录R[n-1]交换，由此得到新的无序区R[0…n-2]和有序区R[n-1]，且满足R[0…n-2].keys ≤ R[n-1].key  
> ③ 由于交换后新的根R[1]可能违反堆性质，故应将当前无序区R[1..n-1]调整为堆。然后再次将R[1..n-1]中关键字最大的记录R[1]和该区间的最后一个记录R[n-1]交换，由此得到新的无序区R[1..n-2]和有序区R[n-1..n]，且仍满足关系R[1..n-2].keys≤R[n-1..n].keys，同样要将R[1..n-2]调整为堆。   
> ④ 直到无序区只有一个元素为止。  

![动图](.\img\v2-b7907d351809293c60658b0b87053c66_b.webp)

#### 代码实现

```python
def sift_down(nums: list[int], n: int, i: int):
    """堆的长度为 n ，从节点 i 开始，从顶至底堆化"""
    while True:
        # 判断节点 i, l, r 中值最大的节点，记为 ma
        l = 2 * i + 1
        r = 2 * i + 2
        ma = i
        if l < n and nums[l] > nums[ma]:
            ma = l
        if r < n and nums[r] > nums[ma]:
            ma = r
        # 若节点 i 最大或索引 l, r 越界，则无须继续堆化，跳出
        if ma == i:
            break
        # 交换两节点
        nums[i], nums[ma] = nums[ma], nums[i]
        # 循环向下堆化
        i = ma

def heap_sort(nums: list[int]):
    """堆排序"""
    # 建堆操作：堆化除叶节点以外的其他所有节点
    for i in range(len(nums) // 2 - 1, -1, -1):
        sift_down(nums, len(nums), i)
    # 从堆中提取最大元素，循环 n-1 轮
    for i in range(len(nums) - 1, 0, -1):
        # 交换根节点与最右叶节点（即交换首元素与尾元素）
        nums[0], nums[i] = nums[i], nums[0]
        # 以根节点为起点，从顶至底进行堆化
        sift_down(nums, i, 0)

```



## 8. 桶排序

#### 定义

将待排序数组中的元素分散到若干个「桶」中，然后对每个桶中的元素再进行单独排序。



桶排序（Bucket sort）或所谓的箱排序，是一个排序算法，工作的原理是将数组分到有限数量的桶里。每个桶再个别排序（有可能再使用别的排序算法或是以递归方式继续使用桶排序进行排序），最后依次把各个桶中的记录列出来记得到有序序列。桶排序是鸽巢排序的一种归纳结果。当要被排序的数组内的数值是均匀分配的时候，桶排序使用线性时间（Θ(n)）。但桶排序并不是比较排序，他不受到O(n log n)下限的影响。

桶排序的思想近乎彻底的**分治思想**。

桶排序假设待排序的一组数均匀独立的分布在一个范围中，并将这一范围划分成几个子范围（桶）。

然后基于某种映射函数f ，将待排序列的关键字 k 映射到第i个桶中 (即桶数组B 的下标i) ，那么该关键字k 就作为 B[i]中的元素 (每个桶B[i]都是一组大小为N/M 的序列 )。

接着将各个桶中的数据有序的合并起来 : 对每个桶B[i] 中的所有元素进行比较排序 (可以使用快排)。然后依次枚举输出 B[0]….B[M] 中的全部内容即是一个有序序列。

> 补充： 映射函数一般是 f = array[i] / k; k^2 = n; n是所有元素个数  

为了使桶排序更加高效，我们需要做到这两点：

> 1、在额外空间充足的情况下，尽量增大桶的数量；  
> 2、使用的映射函数能够将输入的 N 个数据均匀的分配到 K 个桶中；  

同时，对于桶中元素的排序，选择何种比较排序算法对于性能的影响至关重要。



#### 实现逻辑

- 设置一个定量的数组当作空桶子。
- 寻访序列，并且把项目一个一个放到对应的桶子去。
- 对每个不是空的桶子进行排序。
- 从不是空的桶子里把项目再放回原来的序列中。

![动图](.\img\v2-b29c1a8ee42595e7992b6d2eb1030f76_b.webp)

分步骤图示说明：设有数组 array = [63, 157, 189, 51, 101, 47, 141, 121, 157, 156, 194, 117, 98, 139, 67, 133, 181, 13, 28, 109]，对其进行桶排序：

![img](.\img\v2-ff4cdccdb1ff6b90ecdb3fc4d361f725_1440w.webp)

#### 代码实现

```python
def bucket_sort(nums: list[float]):
    """桶排序"""
    # 初始化 k = n/2 个桶，预期向每个桶分配 2 个元素
    k = len(nums) // 2
    buckets = [[] for _ in range(k)]
    # 1. 将数组元素分配到各个桶中
    for num in nums:
        # 输入数据范围 [0, 1)，使用 num * k 映射到索引范围 [0, k-1]
        i = int(num * k)
        # 将 num 添加进桶 i
        buckets[i].append(num)
    # 2. 对各个桶执行排序
    for bucket in buckets:
        # 使用内置排序函数，也可以替换成其他排序算法
        bucket.sort()
    # 3. 遍历桶合并结果
    i = 0
    for bucket in buckets:
        for num in bucket:
            nums[i] = num
            i += 1

```



## 9. 基数排序 

基数排序（Radix sort）是一种非比较型整数排序算法。

#### 定义

将整数按位数切割成不同的数字，然后从低位开始，依次到高位，逐位进行排序，从而达到排序的目的。

基数排序的方式可以采用LSD（Least significant digital）或MSD（Most significant digital），LSD的排序方式由键值的最右边开始，而MSD则相反，由键值的最左边开始。

- **MSD**：先从高位开始进行排序，在每个关键字上，可采用计数排序
- **LSD**：先从低位开始进行排序，在每个关键字上，可采用桶排序

#### 实现逻辑

> ① 将所有待比较数值（正整数）统一为同样的数位长度，数位较短的数前面补零。  
> ② 从最低位开始，依次进行一次排序。  
> ③ 这样从最低位排序一直到最高位排序完成以后, 数列就变成一个有序序列。  



![基数排序算法流程](.\img\radix_sort_overview.png)

#### 代码实现

```python
def digit(num: int, exp: int) -> int:
    """获取元素 num 的第 k 位，其中 exp = 10^(k-1)"""
    # 传入 exp 而非 k 可以避免在此重复执行昂贵的次方计算
    return (num // exp) % 10

def counting_sort_digit(nums: list[int], exp: int):
    """计数排序（根据 nums 第 k 位排序）"""
    # 十进制的位范围为 0~9 ，因此需要长度为 10 的桶
    counter = [0] * 10
    n = len(nums)
    # 统计 0~9 各数字的出现次数
    for i in range(n):
        d = digit(nums[i], exp)  # 获取 nums[i] 第 k 位，记为 d
        counter[d] += 1  # 统计数字 d 的出现次数
    # 求前缀和，将“出现个数”转换为“数组索引”
    for i in range(1, 10):
        counter[i] += counter[i - 1]
    # 倒序遍历，根据桶内统计结果，将各元素填入 res
    res = [0] * n
    for i in range(n - 1, -1, -1):
        d = digit(nums[i], exp)
        j = counter[d] - 1  # 获取 d 在数组中的索引 j
        res[j] = nums[i]  # 将当前元素填入索引 j
        counter[d] -= 1  # 将 d 的数量减 1
    # 使用结果覆盖原数组 nums
    for i in range(n):
        nums[i] = res[i]

def radix_sort(nums: list[int]):
    """基数排序"""
    # 获取数组的最大元素，用于判断最大位数
    m = max(nums)
    # 按照从低位到高位的顺序遍历
    exp = 1
    while exp <= m:
        # 对数组元素的第 k 位执行计数排序
        # k = 1 -> exp = 1
        # k = 2 -> exp = 10
        # 即 exp = 10^(k-1)
        counting_sort_digit(nums, exp)
        exp *= 10

```



## 10.练习题

### [1.](https://datawhalechina.github.io/leetcode-notes/#/ch01/01.03/01.03.04-Exercises?id=_1-剑指-offer-45-把数组排成最小的数)[剑指 Offer 45. 把数组排成最小的数](https://leetcode.cn/problems/ba-shu-zu-pai-cheng-zui-xiao-de-shu-lcof/)

```python
class Solution:
    def minNumber(self, nums):

        arr = [str(i) for i in nums]
        def quick_sort(left, right):
            if left >= right: return 
            low, high = left, right
            target = arr[left]

            while left < right:
                while left < right and arr[right] + target >= target + arr[right] : right -= 1
                arr[left] = arr[right]
                while left < right and arr[left] + target <= target + arr[left]: left += 1
                arr[right] = arr[left]
            
            arr[left] = target
            quick_sort(low, left-1)
            quick_sort(right+1, high)

        quick_sort(0, len(arr)-1)
        return ''.join(arr)
```

### [2.](https://datawhalechina.github.io/leetcode-notes/#/ch01/01.03/01.03.04-Exercises?id=_2-0283-移动零)[0283. 移动零](https://leetcode.cn/problems/move-zeroes/)

```python
class Solution(object):
    def moveZeroes(self, nums):
        slow = 0
        for fast in range(len(nums)):
            if nums[fast] != 0:
                nums[slow] = nums[fast]
                slow += 1
        for i in range(slow, len(nums)):
            nums[i] = 0
```



### [3.](https://datawhalechina.github.io/leetcode-notes/#/ch01/01.03/01.03.04-Exercises?id=_3-0912-排序数组)[0912. 排序数组](https://leetcode.cn/problems/sort-an-array/)

```python
class Solution:
    def sortArray(self, nums: List[int]) -> List[int]:
        self.quickSort(nums, 0, len(nums)-1)
        return nums

        
    def quickSort(self, nums, left: int, right: int):
        flag = nums[randint(left, right)]
        i,j = left,right

        while i<=j:
            while nums[i]<flag:
                i+=1
            while nums[j]>flag:
                j-=1
            if i<=j:
                nums[i], nums[j]=nums[j], nums[i]
                i+=1
                j-=1

        if i<right:
            self.quickSort(nums, i, right)
        if left<j:
            self.quickSort(nums, left, j)
```



### [4.](https://datawhalechina.github.io/leetcode-notes/#/ch01/01.03/01.03.07-Exercises?id=_1-0506-相对名次)[0506. 相对名次](https://leetcode.cn/problems/relative-ranks/)

```python
class Solution:
    def findRelativeRanks(self, score: List[int]) -> List[str]:
        res = [None for _ in range(len(score))]
        for prize, oridata in enumerate(sorted(enumerate(score), key=lambda x: -x[1])):
            idx, _ = oridata
            if prize == 0:
                res[idx] = "Gold Medal"
            elif prize == 1:
                res[idx] = "Silver Medal"
            elif prize == 2:
                res[idx] = "Bronze Medal"
            else:
                res[idx] = str(prize+1)
        return res

```



### [5.](https://datawhalechina.github.io/leetcode-notes/#/ch01/01.03/01.03.07-Exercises?id=_2-0088-合并两个有序数组)[0088. 合并两个有序数组](https://leetcode.cn/problems/merge-sorted-array/)

```python
class Solution:
    def merge(self, nums1: List[int], m: int, nums2: List[int], n: int) -> None:
        """
        Do not return anything, modify nums1 in-place instead.
        """
        p1, p2 = m - 1, n - 1
        tail = m + n - 1
        while p1 >= 0 or p2 >= 0:
            if p1 == -1:
                nums1[tail] = nums2[p2]
                p2 -= 1
            elif p2 == -1:
                nums1[tail] = nums1[p1]
                p1 -= 1
            elif nums1[p1] > nums2[p2]:
                nums1[tail] = nums1[p1]
                p1 -= 1
            else:
                nums1[tail] = nums2[p2]
                p2 -= 1
            tail -= 1

```



### [6.](https://datawhalechina.github.io/leetcode-notes/#/ch01/01.03/01.03.07-Exercises?id=_3-剑指-offer-51-数组中的逆序对)[剑指 Offer 51. 数组中的逆序对](https://leetcode.cn/problems/shu-zu-zhong-de-ni-xu-dui-lcof/)

```python
class Solution:
    def reversePairs(self, nums: List[int]) -> int:
        self.cnt = 0
        def merge(nums, start, mid, end, temp):
            i, j = start, mid + 1
            while i <= mid and j <= end:
                if nums[i] <= nums[j]:
                    temp.append(nums[i])
                    i += 1
                else:
                    self.cnt += mid - i + 1
                    temp.append(nums[j])
                    j += 1
            while i <= mid:
                temp.append(nums[i])
                i += 1
            while j <= end:
                temp.append(nums[j])
                j += 1
            
            for i in range(len(temp)):
                nums[start + i] = temp[i]
            temp.clear()
                    

        def mergeSort(nums, start, end, temp):
            if start >= end: return
            mid = (start + end) >> 1
            mergeSort(nums, start, mid, temp)
            mergeSort(nums, mid + 1, end, temp)
            merge(nums, start, mid,  end, temp)
        mergeSort(nums, 0, len(nums) - 1, [])
        return self.cnt
```



### [7.](https://datawhalechina.github.io/leetcode-notes/#/ch01/01.03/01.03.10-Exercises?id=_1-0075-颜色分类)[0075. 颜色分类](https://leetcode.cn/problems/sort-colors/)

```python
class Solution:
    def sortColors(self, nums: List[int]) -> None:
        i, zero, two = 0, -1, len(nums)
        while i < two:
            if nums[i] == 1:
                i += 1
            elif nums[i] == 2:  
                two -= 1
                nums[i], nums[two] = nums[two], nums[i]
            else: 
                zero += 1
                nums[i], nums[zero] = nums[zero], nums[i]
                i += 1

```



### [8.](https://datawhalechina.github.io/leetcode-notes/#/ch01/01.03/01.03.10-Exercises?id=_2-0215-数组中的第k个最大元素)[0215. 数组中的第K个最大元素](https://leetcode.cn/problems/kth-largest-element-in-an-array/)

```python
class Solution:
    def findKthLargest(self, nums: List[int], k: int) -> int:
        # nums.sort(reverse=True)
        # return nums[k-1]
        def quicksort(nums:list)->list:
            if len(nums) < 2:
                return nums
            else:
                pivot = nums[0]
                small_list = [i for i in nums[1::] if i<= pivot]
                big_list = [i for i in nums[1::] if i > pivot]
                return quicksort(big_list) +[pivot] + quicksort(small_list)
                # 这里按照降序排列
        nums = quicksort(nums)
        return nums[k-1]

```



### [9.](https://datawhalechina.github.io/leetcode-notes/#/ch01/01.03/01.03.10-Exercises?id=_3-剑指-offer-40-最小的k个数)[剑指 Offer 40. 最小的k个数](https://leetcode.cn/problems/zui-xiao-de-kge-shu-lcof/)

```python
class Solution:
    def getLeastNumbers(self, arr: List[int], k: int) -> List[int]:
        if k == 0:
            return list()
        
        hp = [-x for x in arr[:k]]
        heapq.heapify(hp)
        for i in range(k, len(arr)):
            if -hp[0] > arr[i]:
                heapq.heappop(hp)
                heapq.heappush(hp, -arr[i])

        res = [-x for x in hp]
        return res

```



### [10.](https://datawhalechina.github.io/leetcode-notes/#/ch01/01.03/01.03.14-Exercises?id=_1-1122-数组的相对排序)[1122. 数组的相对排序](https://leetcode.cn/problems/relative-sort-array/)

```python
class Solution(object):
    def relativeSortArray(self, arr1, arr2):
        """
        :type arr1: List[int]
        :type arr2: List[int]
        :rtype: List[int]
        """
        #将arr1 counter计数，按照arr2来取
        li = []
        counter = collections.Counter
        count = counter(arr1)
        #按照arr2将arr1的元素存入li
        for val in arr2:
            if val in count:
                l = count[val]
                print(l)
                for i in range(l):
                    li.append(val)
            #被存的元素删除掉
            del count[val]
        #剩下的元素排序放到末尾
        li += sorted(list(count.elements()))
        return li
```



### [11.](https://datawhalechina.github.io/leetcode-notes/#/ch01/01.03/01.03.14-Exercises?id=_2-0220-存在重复元素-iii)[0220. 存在重复元素 III](https://leetcode.cn/problems/contains-duplicate-iii/)

```python
class Solution:
    def containsNearbyAlmostDuplicate(self, nums: List[int], k: int, t: int) -> bool:
        bucket = dict()
        if t < 0: return False
        for i in range(len(nums)):
            nth = nums[i] // (t + 1)
            if nth in bucket:
                return True
            if nth - 1 in bucket and abs(nums[i] - bucket[nth - 1]) <= t:
                return True
            if nth + 1 in bucket and abs(nums[i] - bucket[nth + 1]) <= t:
                return True
            bucket[nth] = nums[i]
            if i >= k: bucket.pop(nums[i - k] // (t + 1))
        return False
```



### [12.](https://datawhalechina.github.io/leetcode-notes/#/ch01/01.03/01.03.14-Exercises?id=_3-0164-最大间距)[0164. 最大间距](https://leetcode.cn/problems/maximum-gap/)

```python
class Solution:
    def maximumGap(self, nums: List[int]) -> int:
        if not nums or len(nums)<=1:
            return 0
        nums.sort(reverse = True)
        return max(nums[i] - nums[i+1]   for i in range(len(nums)-1))
```



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