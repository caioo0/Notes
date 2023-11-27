# 数据结构：字符串(String)

> 关于笔记，主要来自[datawhale-Leetcode算法笔记](https://datawhalechina.github.io/leetcode-notes/#/ch03/03.02/03.02.10-Trie)

## 知识点

**基本概念：** 主串 、子串、串长、模式串

**存储结构：** 定长顺序存储、堆分配存储、块链存储

**模式匹配算法：** 暴力匹配法、 RK算法、KMP算法（部分匹配值表、next数组、next函数的推理过程）、Kmp算法改进（nextval数组）、字典树

## 1、串的定义

> 串(String)是由零个或多个字符组成的有序序列，又名叫字符串。

记为： $ S = 'a_1,a_2...a_n' (n>=0)$

S是串名，单引号括起来是字符串序列是串的值；$a_n$ 可以是字母、数字和其他字符；串的长度为$n$

### 串的基本概念

- 空串： n=0
- 空格串： 只包含空格的串。注意它与空串的区别，空格串是有内容有长度的，而且可以不止一个空格。
- 子串：串中任意连续字符组成的子序列称为该串的子串
- 主串：包含子串的串称为主串。字符在串中的序号表示该字符在串中的位置，子串的第一个字符在主串中的序号称号子串的位置
- 串相等：当且仅当两个串的长度相等且对应位置上字符都相同，称两个串是相等的

串的逻辑结构和线性表相似：但串的数据对象限定为字符集。

串和线性表在基本操作上区别：

- 线性表基本操作：以单个元素作为操作对象，如查找、插入或删除某个元素等;
- 串基本操作：以子串作为操作对象，如查找、插入或删除一个子串等。

## 2、串的存储结构

#### 定长顺序存储表示

用一组地址连续的存储单元存储串值的字符序列。在串的定长顺序存储结构中，为每个串变量分配一个固定长度的存储区，即定长数组

串的实际长度只能小于等于MAXLEN，超过预定义长度的串值会被舍去，称为截断。

串长有两种表示方法:

1、是如上述定义描述的那样，用一个额外的变量len来存放串的长度;

2、是在串值后面加一一个不计入串长的结束标记字符“\0”，此时的串长为隐含值。

#### 堆分配存储表示

堆分配存储表示仍然以一组地址连续的存储单元存放串值的字符序列，但它们的存储空间是在程序执行过程中动态分配得到的。

在C语言中，存在一一个称之为“堆”的自由存储区，并用malloc()和free()函数来完成动则返回一个指向起始地址的指针，作为串的基地址，这个串由ch指针来指示;若分配失败，则返回NULL。已分配的空间可用free()释放掉。

#### 块链存储表示

由于串的特殊性(每个元素只有一个字符)，在具体实现时，每个结点既可以存放一个字符， 也可以存放多个字符。每个结点称为块，整个链表称为块链结构。

## 3、模式匹配算法

### BF算法

从主串 S = "goodjob"中，找到子串 T = "job"的位置。我们通常需要下面的步骤。

```shell
1. 将子串"job"与主串S从第一位对应匹配。即判断 whether 'g' == 'j';
2. 判断结果为否，继续匹配 whether 'o' == 'j';
3. 直到找到第一位匹配 'j' = 'j';
4. 继续匹配完整 S[4:7] == 'job' == T。
```

```python
def bf_match(pattern, text):  
    m = len(pattern)  
    n = len(text)  
    for i in range(n - m + 1):  
        j = 0  
        while j < m:  
            if text[i + j] != pattern[j]:  
                break  
            j += 1  
        if j == m:  
            return i  
    return -1
```

是一种最简单的匹配算法，暴力易实现，但有许多冗余的步骤。

- BF算法的思想比较简单，但当在最坏情况下，算法的时间复杂度为O(n*m),其中n和m分别是主串和模式串的长度。这个算法的主要事件耗费在失配后的比较位置有回溯，因而比较次数过多。为降低时间复杂度可采用无回溯的算法。

### KMP模式匹配算法

KMP (Knuth-Morris-Pratt) 算法是一个用来进行字符串匹配的算法，它能在文本串 S 中寻找到模式串 P 的出现位置。相较于朴素的字符串匹配算法，KMP 算法更加高效，因为它通过一个名为 "next" 的预处理数组来跳过一些明显不会产生匹配的比较。

"next" 数组的作用是保存模式串的自我匹配信息。next[i] 保存的是当第 i 个字符匹配失败时，下一次应该从模式串的哪个位置开始比较。

KMP 算法的一个关键性质是：如果字符 x 和 y 在模式串中相邻出现（即模式串的第 x 个字符和第 y 个字符相邻），那么在 next 数组中，x 和 y 的 next 值一定相等。

```python
def get_next(pattern):  
    """  
    计算 next 数组  
    """  
    next = [0] * len(pattern)  
    j = 0  
    for i in range(1, len(pattern)):  
        while j > 0 and pattern[i] != pattern[j]:  
            j = next[j - 1]  
        if pattern[i] == pattern[j]:  
            j += 1  
        next[i] = j  
    return next  
  
def kmp_match(pattern, text):  
    """  
    KMP模式匹配算法实现  
    """  
    m = len(pattern)  
    n = len(text)  
    next = get_next(pattern)  
    j = 0  
    result = []  
    for i in range(n):  
        while j > 0 and text[i] != pattern[j]:  
            j = next[j - 1]  
        if text[i] == pattern[j]:  
            j += 1  
        if j == m:  
            result.append(i - m + 1)  
            j = next[j - 1]  
    return result
```

这是基本的 KMP 算法，它的时间复杂度为 O(n+m)，其中 n 和 m 分别是文本串和模式串的长度。然而，KMP 算法还可以进一步优化。当在文本串中找到一个匹配的位置后（即 j == m），我们可以利用 next 数组中的信息，跳过一些已经确定不会有匹配的位置，从而提高效率。这种优化称为 "Partial Match Table"，也被广泛应用在其他字符串匹配问题中。

## 4、练习题目

### [1.](https://datawhalechina.github.io/leetcode-notes/#/ch03/03.02/03.02.02-Exercises?id=_1-0125-验证回文串)[0125. 验证回文串](https://leetcode.cn/problems/valid-palindrome/)

解：

```python
# 方法一
class Solution:
    def isPalindrome(self, s: str) -> bool:
        # 只保留字符和数字 
        sgood = "".join([ch.lower() for ch in s if ch.isalnum()])
        # 利用切片跟逆序比较
        return sgood == sgood[::-1]
  
# 方法二
class Solution:
    def isPalindrome(self, s: str) -> bool:
        # 只保留字符和数字 
        sgood = "".join([ch.lower() for ch in s if ch.isalnum()])
        # 获取长度
        n = len(sgood)
        # 初始化指针
        left , right = 0, n-1
        while left < right:
            if sgood[left] != sgood[right]:
                return False
            left ,right = left +1 , right -1 
        return True
```

### [2.](https://datawhalechina.github.io/leetcode-notes/#/ch03/03.02/03.02.02-Exercises?id=_2-0344-反转字符串)[0344. 反转字符串](https://leetcode.cn/problems/reverse-string/)

解：

```python
class Solution:
    def reverseString(self, s: List[str]) -> None:
        """
        Do not return anything, modify s in-place instead.
        """
    
        l,r = 0,len(s)-1
        # 跟上一题相似
        while l < r:
            s[l],s[r] = s[r],s[l]
            l,r = l+1,r-1
```

### [3.](https://datawhalechina.github.io/leetcode-notes/#/ch03/03.02/03.02.02-Exercises?id=_3-0557-反转字符串中的单词-iii)[0557. 反转字符串中的单词 III](https://leetcode.cn/problems/reverse-words-in-a-string-iii/)

解：

```python
利用栈的原理实现：
class Solution:
    def reverseWords(self, s: str) -> str:
        stack ,res ,s = [],'',s+' '
        for i in s:
            stack.append(i) #进栈
            if i == ' ':
                while stack:
                    res +=stack.pop() #出栈 
        return res[1:]
```

### [4.](https://datawhalechina.github.io/leetcode-notes/#/ch03/03.02/03.02.07-Exercises?id=_1-0028-找出字符串中第一个匹配项的下标)[0028. 找出字符串中第一个匹配项的下标](https://leetcode.cn/problems/find-the-index-of-the-first-occurrence-in-a-string/)

解：

KMP模式：

```python
class Solution:
    def strStr(self, haystack: str, needle: str) -> int:
        a=len(needle)
        b=len(haystack)
        if a==0:
            return 0
        next=self.getnext(a,needle)
        p=-1
        for j in range(b):
            while p>=0 and needle[p+1]!=haystack[j]:
                p=next[p]
            if needle[p+1]==haystack[j]:
                p+=1
            if p==a-1:
                return j-a+1
        return -1

    def getnext(self,a,needle):
        next=['' for i in range(a)]
        k=-1
        next[0]=k
        for i in range(1,len(needle)):
            while (k>-1 and needle[k+1]!=needle[i]):
                k=next[k]
            if needle[k+1]==needle[i]:
                k+=1
            next[i]=k
        return next
```

### [5.](https://datawhalechina.github.io/leetcode-notes/#/ch03/03.02/03.02.07-Exercises?id=_2-0459-重复的子字符串)[0459. 重复的子字符串](https://leetcode.cn/problems/repeated-substring-pattern/)

### [6.](https://datawhalechina.github.io/leetcode-notes/#/ch03/03.02/03.02.07-Exercises?id=_3-0686-重复叠加字符串匹配)[0686. 重复叠加字符串匹配](https://leetcode.cn/problems/repeated-string-match/)

### [7.](https://datawhalechina.github.io/leetcode-notes/#/ch03/03.02/03.02.11-Exercises?id=_1-0208-实现-trie-前缀树)[0208. 实现 Trie (前缀树)](https://leetcode.cn/problems/implement-trie-prefix-tree/)

### [8.](https://datawhalechina.github.io/leetcode-notes/#/ch03/03.02/03.02.11-Exercises?id=_2-0677-键值映射)[0677. 键值映射](https://leetcode.cn/problems/map-sum-pairs/)

### [9.](https://datawhalechina.github.io/leetcode-notes/#/ch03/03.02/03.02.11-Exercises?id=_3-1023-驼峰式匹配)[1023. 驼峰式匹配](https://leetcode.cn/problems/camelcase-matching/)

### [10.](https://datawhalechina.github.io/leetcode-notes/#/ch03/03.02/03.02.12-Exercises?id=_1-0211-添加与搜索单词-数据结构设计)[0211. 添加与搜索单词 - 数据结构设计](https://leetcode.cn/problems/design-add-and-search-words-data-structure/)

### [11.](https://datawhalechina.github.io/leetcode-notes/#/ch03/03.02/03.02.12-Exercises?id=_2-0648-单词替换)[0648. 单词替换](https://leetcode.cn/problems/replace-words/)

### [12.](https://datawhalechina.github.io/leetcode-notes/#/ch03/03.02/03.02.12-Exercises?id=_3-0676-实现一个魔法字典)[0676. 实现一个魔法字典](https://leetcode.cn/problems/implement-magic-dictionary/)

## 参考资料

- 【博文】[字符串和编码 - 廖雪峰的官方网站](https://www.liaoxuefeng.com/wiki/1016959663602400/1017075323632896)
- 【文章】[数组和字符串 - LeetBook - 力扣](https://leetcode.cn/leetbook/read/array-and-string/c9lnm/)
- 【文章】[字符串部分简介 - OI Wiki](https://oi-wiki.org/string/)
- 【文章】[解密 Python 中字符串的底层实现，以及相关操作 - 古明地盆 - 博客园](https://www.cnblogs.com/traditional/p/13455962.html)
- 【文章】[Python 算法基础篇之字符串操作：索引、切片、常用方法](https://cloud.tencent.com/developer/article/2304373)
- 【文章】[动画：什么是 BF 算法 ？- 吴师兄学编程](https://www.cxyxiaowu.com/560.html)
- 【文章】[BF 算法（普通模式匹配算法）及 C 语言实现 - 数据结构与算法教程](http://data.biancheng.net/view/12.html)
- 【文章】[字符串匹配基础（上）- 数据结构与算法之美 - 极客时间](https://time.geekbang.org/column/article/71187)
- 【文章】[字符串匹配基础（上）- 数据结构与算法之美 - 极客时间](https://time.geekbang.org/column/article/71187)
- 【文章】[字符串匹配算法 - Rabin Karp 算法 - coolcao 的小站](https://coolcao.com/2020/08/20/rabin-karp/)
- 【问答】[string - Python: Rabin-Karp algorithm hashing - Stack Overflow](https://stackoverflow.com/questions/22216948/python-rabin-karp-algorithm-hashing)
