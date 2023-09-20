# task05: 数组双指针、滑动窗口

> 关于笔记，主要来自[datawhale-Leetcode算法笔记](https://datawhalechina.github.io/leetcode-notes/#/ch01/01.01/01.01.02-Algorithm-Complexity)

## 双指针

### 算法解释

双指针(Two Pointers): 指在遍历元素的过程中，不是使用单个指针进行访问，而是使用两个指针进行访问，从而达到相应的目的。

如果两个指针方向相反，则称为「对撞指针」。

如果两个指针方向相同，则称为「快慢指针」。如果两个指针分别属于不同的数组 / 链表，则称为「分离双指针」。

双指针比较灵活，可以大大降低[时间复杂度](https://so.csdn.net/so/search?q=时间复杂度&spm=1001.2101.3001.7020)，可用在数组，单链表等数据结构中。

### 基本思想

使用两个指针在数据结构中同时移动，以便有效地查找或比较元素。

- 数组中，通常使用两个指针从两端向中间移动，以便查找满足特定条件的元素。
- 链表中，通常使用两个指针以不同的速度移动，以便在链表中查找环或回文字符串等问题。双指针法也可以用于优化时间复杂度，例如 : 快速排序和归并排序等算法中常常使用双指针法。

#### **双指针法两种扫描方向：**

（1）同向扫描，i 和 j 方向相同，都从头到尾，但速度不同，所以i和j被称为“快慢指针”。

（2）反向扫描，i 和 j 方向相反，i 从头到尾，j 从尾到头，在中间相会，”对撞指针“。



**快慢指针：**一快一慢，步长一大一小。例如，是否有环问题（看慢指针是否能追上快指针），单链表找中间节点问题（快指针到单链表结尾，慢指针到一半）。

**对撞指针：**一左一右向中间逼近。



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

