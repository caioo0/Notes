# task05: 数组双指针、滑动窗口

> 关于笔记，主要来自[datawhale-Leetcode算法笔记](https://datawhalechina.github.io/leetcode-notes/#/ch01/01.01/01.01.02-Algorithm-Complexity)

## 双指针

### 定义

双指针(Two Pointers): 指在遍历元素的过程中，不是使用单个指针进行访问，而是使用两个指针进行访问，从而达到相应的目的。如果两个指针方向相反，则称为「对撞指针」。如果两个指针方向相同，则称为「快慢指针」。如果两个指针分别属于不同的数组 / 链表，则称为「分离双指针」。



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

**滑动窗口：**类似计算机网络中的滑动窗口，一般是右端向右扩充，达到停止条件后右端不动，左端向右端逼近，逼近达到停止条件后，左端不动，右端继续扩充。

### 练习题

#### 1. [0344. 反转字符串](https://leetcode.cn/problems/reverse-string/)

#### 2. [0345. 反转字符串中的元音字母](https://leetcode.cn/problems/reverse-vowels-of-a-string/)

#### 3. [0015. 三数之和](https://leetcode.cn/problems/3sum/)

#### 4. [0027. 移除元素](https://leetcode.cn/problems/remove-element/)

#### 5. [0080. 删除有序数组中的重复项 II](https://leetcode.cn/problems/remove-duplicates-from-sorted-array-ii/)

#### 6. [0925. 长按键入](https://leetcode.cn/problems/long-pressed-name/)



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

[1343. 大小为 K 且平均值大于等于阈值的子数组数目 - 力扣（LeetCode）](https://leetcode.cn/problems/number-of-sub-arrays-of-size-k-and-average-greater-than-or-equal-to-threshold/)

#### 不定长度滑动窗口

> **不定长度滑动窗口算法（Sliding Window）**：在给定数组 / 字符串上维护一个不定长度的窗口。可以对窗口进行滑动操作、缩放操作，以及维护最优解操作。

![image-20230920153437357](.\img\image-20230920153437357.png)

[3. 无重复字符的最长子串 - 力扣（LeetCode）](https://leetcode.cn/problems/longest-substring-without-repeating-characters/)



#### 练习题

1. [0643. 子数组最大平均数 I](https://leetcode.cn/problems/maximum-average-subarray-i/)

2. [0674. 最长连续递增序列](https://leetcode.cn/problems/longest-continuous-increasing-subsequence/)

3. [1004. 最大连续1的个数 III](https://leetcode.cn/problems/max-consecutive-ones-iii/)