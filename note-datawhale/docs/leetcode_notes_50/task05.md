# task05: 数组双指针、滑动窗口

> 关于笔记，主要来自[datawhale-Leetcode算法笔记](https://datawhalechina.github.io/leetcode-notes/#/ch01/01.01/01.01.02-Algorithm-Complexity)

## 双指针

### 算法解释

**双指针算法**是一种通过设置**两个指针**不断进行**单向移动**来解决问题的算法。

它包含两种形式：

1. 两个指针分别指向**不同**的序列，称为**对撞指针**“。比如：归并排序的合并过程。
2. 两个指针指向**同一个**序列，但速度不同，称为“**快慢指针**”。比如：快速排序的划分过程。

一般更多使用、也更难想到是**第2种**情况。

双指针算法最核心的用途就是**优化时间复杂度**。

【**核心思想**】：

> 原本两个指针是有$ n^2$ 种组合，因此时间复杂度是$ 0(n^2) $。
> 而双指针算法就是运用单调性使得指针只能单向移动，因此总的时间复杂度只有$ O(2n)$，也就是$0(2n)$。

- 双指针可以实现$ O(n) $的时间复杂度是因为指针只能单向移动，没有指针的回溯，而且每一步都会有指针移动。

- 朴素的 $O(n^2)$ 算法的问题就在于指针经常**回溯到之前的位置**。

双指针比较灵活，可用在数组，单链表等数据结构中：

- 数组中，通常使用两个指针从两端向中间移动，以便查找满足特定条件的元素。
- 链表中，通常使用两个指针以不同的速度移动，以便在链表中查找环或回文字符串等问题。双指针法也可以用于优化时间复杂度，例如 : 快速排序和归并排序等算法中常常使用双指针法。

### 快慢指针

> 一快一慢，步长一大一小。例如，是否有环问题（看慢指针是否能追上快指针），单链表找中间节点问题（快指针到单链表结尾，慢指针到一半）。

#### 解题思路：

我们可以使用两个指针`slow `与 `fast` 一起来遍历链表。其中`slow` 一次走一步，`fast` 一次走两步。那么当 `fast` 到达链表的末尾时，`slow`必然位于中间位置。

代码如下：

```python
def middleNode(self, head: ListNode) -> ListNode:
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
    return slow
```

上述代码中，使用了往同一个方向移动的两个指针，同样涉及三个通用步骤。如下：

- **初始化**：两个指针将从同一位置开始，即链表的开头。
- **移动**：它们将朝着相同的方向移动，但第二个比第一个快。
- **终止条件**：当移动更快的指针到达链表的末尾时，遍历将停止。由于更快的指针的移动速度是慢指针的两倍，当它到达末端时，慢指针将位于中间。

具体过程，图示如下：

![image-20230922104130581](.\img\image-20230922104130581.png)

**复杂度分析**

- 时间复杂度：O(N)，其中 N 是给定链表的结点数目。
- 空间复杂度：O(1)，只需要常数空间存放 `slow `和 `fast` 两个指针。

### 对撞指针

> 一左一右向中间逼近。

#### 解题思路：

因为是有序数组，从小到大排列。

收尾之和对应的为中间值，而头部向后则和增加；

反之，尾部向前移动则变小；

最小的和为 索引0 和 1；

最大的和为 索引n-2 n-1, n为List长度；

结束条件是头和尾相撞。

代码如下：

```python
class Solution:
    def twoSum(self, numbers: List[int], target: int) -> List[int]:
        if not numbers: return []  #输入列表不存在，返回空值
        start, end = 0, len(numbers)-1  #头尾指针
 
        while start < end:  #保证尾指针在头指针后边
            _sum = numbers[start] + numbers[end]
            if  _sum < target:  #小于目标值，首指针后移
                start += 1
            elif _sum > target: #大于目标值，尾指针前移
                end -= 1
            else:               #等于目标值，返回结果
                return [start + 1, end + 1]
        return []
```



### 练习题

#### 1. [0344. 反转字符串](https://leetcode.cn/problems/reverse-string/)

```python
class Solution:
    def reverseString(self, s: List[str]) -> None:
        i, j = 0, len(s)-1
        while i<j:
            s[i], s[j] = s[j], s[i]
            i += 1
            j -= 1

```



#### 2. [0345. 反转字符串中的元音字母](https://leetcode.cn/problems/reverse-vowels-of-a-string/)

```python
class Solution:
    def reverseVowels(self, s: str) -> str:
        length = len(s)
        low, high = 0, length-1
        s = list(s)
        res =['a','e','i','o','u','A','E','I','O','U']
        while low <= high: 
            while low< high and s[high] not in res:
                high-=1
            while low < high and s[low] not in res:
                low += 1
            s[low],s[high]  = s[high],s[low]
            low+=1
            high-=1
        return  "".join(s)
            
```



#### 3. [0015. 三数之和](https://leetcode.cn/problems/3sum/)

```python
class Solution:
    def threeSum(self, nums: List[int]) -> List[List[int]]:
        if len(nums) < 3: return []
        nums, res = sorted(nums), []
        for i in range(len(nums) - 2):
            cur, l, r = nums[i], i + 1, len(nums) - 1
            if res != [] and res[-1][0] == cur: continue 

            while l < r:
                if cur + nums[l] + nums[r] == 0:
                    res.append([cur, nums[l], nums[r]])
                   
                    while l < r - 1 and nums[l] == nums[l + 1]:
                        l += 1
                    while r > l + 1 and nums[r] == nums[r - 1]:
                        r -= 1
                if cur + nums[l] + nums[r] > 0:
                    r -= 1
                else:
                    l += 1
        return res

```



#### 4. [0027. 移除元素](https://leetcode.cn/problems/remove-element/)

```python

class Solution:
    def removeElement(self, nums: List[int], val: int) -> int:
        s = f = 0
        while f < len(nums):
            nums[s] = nums[f]
            if nums[f] == val:  
                f += 1
            else:
                s += 1
                f += 1 
            
        return s 

```



#### 5. [0080. 删除有序数组中的重复项 II](https://leetcode.cn/problems/remove-duplicates-from-sorted-array-ii/)

```python
class Solution:
    def removeDuplicates(self, nums: List[int]) -> int:
        index, l = 0, len(nums)

        if l < 3:

            return len(nums)

        while index <= l - 3:

            if nums[index] != nums[index + 2]:

                index += 1

            else:
                nums.pop(index + 2)

                l = len(nums)
        return len(nums)

```



#### 6. [0925. 长按键入](https://leetcode.cn/problems/long-pressed-name/)

```python
class Solution:
    def isLongPressedName(self, name: str, typed: str) -> bool:
        # 定义指针，分别指向 name 和 typed 的首字符
        p = 0
        q = 0

        m = len(name)
        n = len(typed)
        # 遍历 typed 与 name 中的字符比较
        while q < n:
            # 比较，相同移动指针
            if p < m and name[p] == typed[q]:
                p += 1
                q += 1
            # 不相同时，要注意 p 指针指向的元素
            # 如果是首元素，那么表示 name 和 typed 首字符都不同，可以直接返回 False
            # 如果不在首元素，看是否键入重复，键入重复，继续移动 q 指针，继续判断；如果不重复，也就是不相等的情况，直接返回 False，表示输入错误
            elif p > 0 and name[p-1] == typed[q]:
                q += 1
            else:
                return False
        
        # typed 遍历完成后要检查 name 是否遍历完成
        return p == m

```



## 滑动窗口

滑动窗口协议（Sliding Window Protocol）：传输层进行流控的一种措施，接收方通过通告发送方自己的窗口大小，从而控制发送方的发送速度，从而达到防止发送方发送速度过快而导致自己被淹没的目的。

**滑动窗口算法（Sliding Window）**：在给定数组 / 字符串上维护一个固定长度或不定长度的窗口。可以对窗口进行滑动操作、缩放操作，以及维护最优解操作。

- **滑动操作**：窗口可按照一定方向进行移动。最常见的是向右侧移动。
- **缩放操作**：对于不定长度的窗口，可以从左侧缩小窗口长度，也可以从右侧增大窗口长度。

滑动窗口利用了双指针中的快慢指针技巧，我们可以将滑动窗口看做是快慢指针两个指针中间的区间，也可以将滑动窗口看做是快慢指针的一种特殊形式。

![image-20230920152847863](.\img\image-20230920152847863.png)

滑动窗口算法: 解决一些查找满足一定条件的连续区间的性质（长度等）的问题。

该算法可以将一部分问题中的嵌套循环转变为一个单循环，因此它可以减少时间复杂度。

按照窗口长度的固定情况，我们可以将滑动窗口题目分为以下两种：

- **固定长度窗口**：窗口大小是固定的。
- **不定长度窗口**：窗口大小是不固定的。
  - 求解最大的满足条件的窗口。
  - 求解最小的满足条件的窗口。

#### **固定长度滑动窗口**

> **固定长度滑动窗口算法（Fixed Length Sliding Window）**：在给定数组 / 字符串上维护一个固定长度的窗口。可以对窗口进行滑动操作、缩放操作，以及维护最优解操作。

![image-20230920153034504](.\img\image-20230920153034504.png)

**测验题：**

#### [1343. 大小为 K 且平均值大于等于阈值的子数组数目 - 力扣（LeetCode）](https://leetcode.cn/problems/number-of-sub-arrays-of-size-k-and-average-greater-than-or-equal-to-threshold/)

```python
class Solution:
    def numOfSubarrays(self, arr: List[int], k: int, threshold: int) -> int:
        res = [0]
        ans = 0
        for i in range(len(arr)):
            res.append(res[-1] + arr[i])
        
        for i in range(len(res)-k):
            b = res[i+k]
            a = res[i]
            if (b-a)/k >= threshold:
                ans+=1
            
        
        return ans
```



#### 不定长度滑动窗口

> **不定长度滑动窗口算法（Sliding Window）**：在给定数组 / 字符串上维护一个不定长度的窗口。可以对窗口进行滑动操作、缩放操作，以及维护最优解操作。

![image-20230920153437357](.\img\image-20230920153437357.png)

#### [无重复字符的最长子串 - 力扣（LeetCode）](https://leetcode.cn/problems/longest-substring-without-repeating-characters/)

```python
class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        cur, res = [], 0
        for r in range(len(s)):
            while s[r] in cur: 
                cur.pop(0) # 左边出
            cur.append(s[r]) # 右侧无论如何都会进入新的
            res = max(len(cur),res)
        return res
```



### 练习题

#### [0643. 子数组最大平均数 I](https://leetcode.cn/problems/maximum-average-subarray-i/)

```python
class Solution:
    def findMaxAverage(self, nums: List[int], k: int) -> float:
        maxsum = sums = sum(nums[:k])
        left,right = 1,k
        while right<len(nums):
            sums = sums-nums[left-1]+nums[right]
            maxsum = max(maxsum,sums)
            left+=1
            right+=1
        return maxsum/k

```



#### [0674. 最长连续递增序列](https://leetcode.cn/problems/longest-continuous-increasing-subsequence/)

```python
class Solution:
    def findLengthOfLCIS(self, nums: List[int]) -> int:
        dp = [1 for _ in range(len(nums))]
        for i in range(1, len(nums)):
            if nums[i] > nums[i-1]:
                dp[i] = dp[i-1] + 1
        return max(dp)

```



#### [1004. 最大连续1的个数 III](https://leetcode.cn/problems/max-consecutive-ones-iii/)

```python
class Solution:
    def longestOnes(self, A: List[int], K: int) -> int:
        #标准滑动窗口
        start = 0
        max_len = float('-inf')
        count = 0
        for end in range(len(A)):
            if A[end] == 1:
                count += 1
            while end-start+1 > count + K:
                if A[start] == 1:
                    count -= 1
                start += 1
            max_len = max(max_len,end-start+1)
        return max_len
```

## 参考资料

1.[Hello-算法](https://www.hello-algo.com/chapter_computational_complexity/time_complexity/#234)

2.[datawhale-Leetcode算法笔记](https://datawhalechina.github.io/leetcode-notes/#/ch01/01.01/01.01.02-Algorithm-Complexity)

3.[Python技巧之双指针](https://zhuanlan.zhihu.com/p/529362145)

