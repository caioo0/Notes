#  哈希表

> 关于笔记，主要来自[datawhale-Leetcode算法笔记](https://datawhalechina.github.io/leetcode-notes/#/ch01/01.01/01.01.02-Algorithm-Complexity)

## 1、概述

哈希表（Hash Table):  也叫做散列表。通过 键 key 和 映射函数 Hash(key) 计算出对应的值 value，实现高效的元素查询。时间复杂度`O(1)`。

表 常见的哈希算法

|          | MD5                            | SHA-1            | SHA-2                        | SHA-3                |
| :------- | :----------------------------- | :--------------- | :--------------------------- | :------------------- |
| 推出时间 | 1992                           | 1995             | 2002                         | 2008                 |
| 输出长度 | 128 bits                       | 160 bits         | 256 / 512 bits               | 224/256/384/512 bits |
| 哈希冲突 | 较多                           | 较多             | 很少                         | 很少                 |
| 安全等级 | 低，已被成功攻击               | 低，已被成功攻击 | 高                           | 高                   |
| 应用     | 已被弃用，仍用于数据完整性检查 | 已被弃用         | 加密货币交易验证、数字签名等 | 可用于替代 SHA-2     |

哈希表、数组、链表效率比较：

|          | 数组     | 链表     | 哈希表   |
| :------- | :------- | :------- | :------- |
| 查找元素 | \(O(n)\) | \(O(n)\) | \(O(1)\) |
| 添加元素 | \(O(1)\) | \(O(1)\) | \(O(1)\) |
| 删除元素 | \(O(n)\) | \(O(n)\) | \(O(1)\) |

## 2、常用操作

哈希表的常见操作包括：初始化、查询操作、添加键值对和删除键值对等。

```python
# 初始化哈希表
hmap: dict = {}

# 添加操作
# 在哈希表中添加键值对（key, value）
hmap[12308] = "小鱼"
hmap[13332] = "小丁"
hmap[14363] = "小沙"
hmap[10911] = "小海"

# 查询操作
# 在哈希表中删除键值对（key,value）
name :str = hmap[13332]

# 删除操作
# 在哈希表中删除键值对（Key,value）
hmap.pop(12308)
```

哈希表三种常用遍历方式：遍历键值对、遍历键和遍历值。

```python
# 遍历哈希表
# 遍历键值对 key->value
for key, value in hmap.items():
    print(key, "->", value)
# 单独遍历键 key
for key in hmap.keys():
    print(key)
# 单独遍历值 value
for value in hmap.values():
    print(value)

```

## 3、哈希表的实现

哈希表的关键思想是使用**哈希函数**。

> **哈希函数（散列函数）能够将任意长度的输入值转变成固定长度的值输出，该值称为散列值，输出值通常为字母与数字组合**。

Hash值J计算公式：
$$
h = H(M)
$$
哈希函数会满足以下几个条件:

- Hash可用于任意大小的数据块
- hash可以接受任意长度的信息，并将其输出成固定长度的消息摘要
- 单向性。给定一个输入M，一定有一个h与其对应，满足H(M)=h，反之，则不行，算法操作是不可逆的。
- 碰撞性。给定一个M,要找到一个M’满足是不可H(M)=H(M’)是不可能的。即不能同时找到两个不同的输入使其输出结果完全一致
- 低复杂性：算法具有运算的低复杂性

### **哈希表实际应用**

**1、**关键字的类型：除了数字类型，还有可能是**字符串类型、浮点数类型、大整数类型，甚至还有可能是几种类型的组**

```python
num = 3
hash_num = hash(num)
# 整数 3 的哈希值为 3

bol = True
hash_bol = hash(bol)
# 布尔量 True 的哈希值为 1

dec = 3.14159
hash_dec = hash(dec)
# 小数 3.14159 的哈希值为 326484311674566659

str = "Hello  hash"
hash_str = hash(str)
# 字符串 Hello 算法 的哈希值为 1311076784711723454

tup = (12836, "小哈")
hash_tup = hash(tup)
# 元组 (12836, '小哈') 的哈希值为 1029005403108185979

obj = ListNode(0)
hash_obj = hash(obj)
# 节点对象 <ListNode object at 0x1058fd810> 的哈希值为 274267521

```

2、各种类型的关键字先转换为整数类型，再通过哈希函数，将其映射到哈希表中。

**3、**常用的哈希函数方法：**直接定址法、除留余数法、平方取中法、基数转换法、数字分析法、折叠法、随机数法、乘积法、点积法等**。



几个常用的哈希函数方法：

- **直接定址法**：取关键字或者关键字的某个线性函数值为哈希地址。即：Hash(key) = key  或者 $Hash(key) = a * key + b$，其中 a 和 b 为常数。
- **除留余数法**：假设哈希表的表长为 m，取一个不大于 m 但接近或等于 m 的质数 p，利用取模运算，将关键字转换为哈希地址。即：$Hash(key) = key % p$，其中 p 为不大于 m 的质数。
- **平方取中法**：先通过求关键字平方值的方式扩大相近数之间的差别，然后根据表长度取关键字平方值的中间几位数为哈希地址。
- **基数转换法**：将关键字看成另一种进制的数再转换成原来进制的数，然后选其中几位作为哈希地址。

```python
class Pair:
    """键值对"""

    def __init__(self, key: int, val: str):
        self.key = key
        self.val = val

class ArrayHashMap:
    """基于数组简易实现的哈希表"""

    def __init__(self):
        """构造方法"""
        # 初始化数组，包含 100 个桶
        self.buckets: list[Pair | None] = [None] * 100

    def hash_func(self, key: int) -> int:
        """哈希函数"""
        index = key % 100
        return index

    def get(self, key: int) -> str:
        """查询操作"""
        index: int = self.hash_func(key)
        pair: Pair = self.buckets[index]
        if pair is None:
            return None
        return pair.val

    def put(self, key: int, val: str):
        """添加操作"""
        pair = Pair(key, val)
        index: int = self.hash_func(key)
        self.buckets[index] = pair

    def remove(self, key: int):
        """删除操作"""
        index: int = self.hash_func(key)
        # 置为 None ，代表删除
        self.buckets[index] = None

    def entry_set(self) -> list[Pair]:
        """获取所有键值对"""
        result: list[Pair] = []
        for pair in self.buckets:
            if pair is not None:
                result.append(pair)
        return result

    def key_set(self) -> list[int]:
        """获取所有键"""
        result = []
        for pair in self.buckets:
            if pair is not None:
                result.append(pair.key)
        return result

    def value_set(self) -> list[str]:
        """获取所有值"""
        result = []
        for pair in self.buckets:
            if pair is not None:
                result.append(pair.val)
        return result

    def print(self):
        """打印哈希表"""
        for pair in self.buckets:
            if pair is not None:
                print(pair.key, "->", pair.val)

```

## 4、哈希冲突

哈希冲突：不同的关键字通过同一个哈希函数可能得到同一个哈希地址 , 即 **`key1 ≠ key2`** ,而 **`Hash(key1) = Hash(key2)`，这种现象称为哈希冲突。**

常用解决方法主要是两类：「开放寻址法」和「链地址法」

### 开放寻址法

开放寻址法：指的是将哈希表中的「空地址」向处理冲突开放。当哈希表未满时，处理冲突时需要尝试另外的单元，直到找到空的单元为止。「开放寻址 open addressing」不引入额外的数据结构，而是通过“多次探测”来处理哈希冲突，探测方式主要包括线性探测、平方探测、多次哈希等。

#### 1.  线性探测

```python
class HashMapOpenAddressing:
    """开放寻址哈希表"""

    def __init__(self):
        """构造方法"""
        self.size = 0  # 键值对数量
        self.capacity = 4  # 哈希表容量
        self.load_thres = 2.0 / 3.0  # 触发扩容的负载因子阈值
        self.extend_ratio = 2  # 扩容倍数
        self.buckets: list[Pair | None] = [None] * self.capacity  # 桶数组
        self.TOMBSTONE = Pair(-1, "-1")  # 删除标记

    def hash_func(self, key: int) -> int:
        """哈希函数"""
        return key % self.capacity

    def load_factor(self) -> float:
        """负载因子"""
        return self.size / self.capacity

    def find_bucket(self, key: int) -> int:
        """搜索 key 对应的桶索引"""
        index = self.hash_func(key)
        first_tombstone = -1
        # 线性探测，当遇到空桶时跳出
        while self.buckets[index] is not None:
            # 若遇到 key ，返回对应桶索引
            if self.buckets[index].key == key:
                # 若之前遇到了删除标记，则将键值对移动至该索引
                if first_tombstone != -1:
                    self.buckets[first_tombstone] = self.buckets[index]
                    self.buckets[index] = self.TOMBSTONE
                    return first_tombstone  # 返回移动后的桶索引
                return index  # 返回桶索引
            # 记录遇到的首个删除标记
            if first_tombstone == -1 and self.buckets[index] is self.TOMBSTONE:
                first_tombstone = index
            # 计算桶索引，越过尾部返回头部
            index = (index + 1) % self.capacity
        # 若 key 不存在，则返回添加点的索引
        return index if first_tombstone == -1 else first_tombstone

    def get(self, key: int) -> str:
        """查询操作"""
        # 搜索 key 对应的桶索引
        index = self.find_bucket(key)
        # 若找到键值对，则返回对应 val
        if self.buckets[index] not in [None, self.TOMBSTONE]:
            return self.buckets[index].val
        # 若键值对不存在，则返回 None
        return None

    def put(self, key: int, val: str):
        """添加操作"""
        # 当负载因子超过阈值时，执行扩容
        if self.load_factor() > self.load_thres:
            self.extend()
        # 搜索 key 对应的桶索引
        index = self.find_bucket(key)
        # 若找到键值对，则覆盖 val 并返回
        if self.buckets[index] not in [None, self.TOMBSTONE]:
            self.buckets[index].val = val
            return
        # 若键值对不存在，则添加该键值对
        self.buckets[index] = Pair(key, val)
        self.size += 1

    def remove(self, key: int):
        """删除操作"""
        # 搜索 key 对应的桶索引
        index = self.find_bucket(key)
        # 若找到键值对，则用删除标记覆盖它
        if self.buckets[index] not in [None, self.TOMBSTONE]:
            self.buckets[index] = self.TOMBSTONE
            self.size -= 1

    def extend(self):
        """扩容哈希表"""
        # 暂存原哈希表
        buckets_tmp = self.buckets
        # 初始化扩容后的新哈希表
        self.capacity *= self.extend_ratio
        self.buckets = [None] * self.capacity
        self.size = 0
        # 将键值对从原哈希表搬运至新哈希表
        for pair in buckets_tmp:
            if pair not in [None, self.TOMBSTONE]:
                self.put(pair.key, pair.val)

    def print(self):
        """打印哈希表"""
        for pair in self.buckets:
            if pair is None:
                print("None")
            elif pair is self.TOMBSTONE:
                print("TOMBSTONE")
            else:
                print(pair.key, "->", pair.val)

```

#### 2.  平方探测

平方探测不是简单地跳过一个固定的步数，而是跳过“探测次数的平方”的步数，即 $(1, 4, 9, \dots)$ 步。

#### 3.  多次哈希

与线性探测相比，多次哈希方法不易产生聚集，但多个哈希函数会增加额外的计算量

> 请注意，开放寻址（线性探测、平方探测和多次哈希）哈希表都存在“不能直接删除元素”的问题。

### **链地址法**

链地址法：将具有相同哈希地址的元素（或记录）存储在同一个线性链表中。 链地址法是一种更加常用的哈希冲突解决方法。

```python
class HashMapChaining:
    """链式地址哈希表"""

    def __init__(self):
        """构造方法"""
        self.size = 0  # 键值对数量
        self.capacity = 4  # 哈希表容量
        self.load_thres = 2.0 / 3.0  # 触发扩容的负载因子阈值
        self.extend_ratio = 2  # 扩容倍数
        self.buckets = [[] for _ in range(self.capacity)]  # 桶数组

    def hash_func(self, key: int) -> int:
        """哈希函数"""
        return key % self.capacity

    def load_factor(self) -> float:
        """负载因子"""
        return self.size / self.capacity

    def get(self, key: int) -> str | None:
        """查询操作"""
        index = self.hash_func(key)
        bucket = self.buckets[index]
        # 遍历桶，若找到 key 则返回对应 val
        for pair in bucket:
            if pair.key == key:
                return pair.val
        # 若未找到 key 则返回 None
        return None

    def put(self, key: int, val: str):
        """添加操作"""
        # 当负载因子超过阈值时，执行扩容
        if self.load_factor() > self.load_thres:
            self.extend()
        index = self.hash_func(key)
        bucket = self.buckets[index]
        # 遍历桶，若遇到指定 key ，则更新对应 val 并返回
        for pair in bucket:
            if pair.key == key:
                pair.val = val
                return
        # 若无该 key ，则将键值对添加至尾部
        pair = Pair(key, val)
        bucket.append(pair)
        self.size += 1

    def remove(self, key: int):
        """删除操作"""
        index = self.hash_func(key)
        bucket = self.buckets[index]
        # 遍历桶，从中删除键值对
        for pair in bucket:
            if pair.key == key:
                bucket.remove(pair)
                self.size -= 1
                break

    def extend(self):
        """扩容哈希表"""
        # 暂存原哈希表
        buckets = self.buckets
        # 初始化扩容后的新哈希表
        self.capacity *= self.extend_ratio
        self.buckets = [[] for _ in range(self.capacity)]
        self.size = 0
        # 将键值对从原哈希表搬运至新哈希表
        for bucket in buckets:
            for pair in bucket:
                self.put(pair.key, pair.val)

    def print(self):
        """打印哈希表"""
        for bucket in self.buckets:
            res = []
            for pair in bucket:
                res.append(str(pair.key) + " -> " + pair.val)
            print(res)

```

## 5、哈希算法

![image-20231115135959409](.\img\image-20231115135959409.png)

**键值对的分布情况由哈希函数决定**。回忆哈希函数的计算步骤，先计算哈希值，再对数组长度取模：

```
index = hash(key) % capacity
```

观察以上公式，当哈希表容量 `capacity` 固定时，**哈希算法 `hash()` 决定了输出值**，进而决定了键值对在哈希表中的分布情况。

这意味着，为了减小哈希冲突的发生概率，我们应当将注意力集中在哈希算法 `hash()` 的设计上。

### 哈希算法的目标

为了实现“既快又稳”的哈希表数据结构，哈希算法应包含以下特点。

- **确定性**：对于相同的输入，哈希算法应始终产生相同的输出。这样才能确保哈希表是可靠的。
- **效率高**：计算哈希值的过程应该足够快。计算开销越小，哈希表的实用性越高。
- **均匀分布**：哈希算法应使得键值对平均分布在哈希表中。分布越平均，哈希冲突的概率就越低。

实际上，哈希算法除了可以用于实现哈希表，还广泛应用于其他领域中。

- **密码存储**：为了保护用户密码的安全，系统通常不会直接存储用户的明文密码，而是存储密码的哈希值。当用户输入密码时，系统会对输入的密码计算哈希值，然后与存储的哈希值进行比较。如果两者匹配，那么密码就被视为正确。
- **数据完整性检查**：数据发送方可以计算数据的哈希值并将其一同发送；接收方可以重新计算接收到的数据的哈希值，并与接收到的哈希值进行比较。如果两者匹配，那么数据就被视为完整的。

对于密码学的相关应用，为了防止从哈希值推导出原始密码等逆向工程，哈希算法需要具备更高等级的安全特性。

- **单向性**：无法通过哈希值反推出关于输入数据的任何信息。
- **抗碰撞性**：应当极其困难找到两个不同的输入，使得它们的哈希值相同。
- **雪崩效应**：输入的微小变化应当导致输出的显著且不可预测的变化。

### 哈希算法的设计

哈希算法的设计是一个需要考虑许多因素的复杂问题。然而对于某些要求不高的场景，我们也能设计一些简单的哈希算法。

- **加法哈希**：对输入的每个字符的 ASCII 码进行相加，将得到的总和作为哈希值。
- **乘法哈希**：利用了乘法的不相关性，每轮乘以一个常数，将各个字符的 ASCII 码累积到哈希值中。
- **异或哈希**：将输入数据的每个元素通过异或操作累积到一个哈希值中。
- **旋转哈希**：将每个字符的 ASCII 码累积到一个哈希值中，每次累积之前都会对哈希值进行旋转操作。

```python
def add_hash(key: str) -> int:
    """加法哈希"""
    hash = 0
    modulus = 1000000007
    for c in key:
        hash += ord(c)
    return hash % modulus

def mul_hash(key: str) -> int:
    """乘法哈希"""
    hash = 0
    modulus = 1000000007
    for c in key:
        hash = 31 * hash + ord(c)
    return hash % modulus

def xor_hash(key: str) -> int:
    """异或哈希"""
    hash = 0
    modulus = 1000000007
    for c in key:
        hash ^= ord(c)
    return hash % modulus

def rot_hash(key: str) -> int:
    """旋转哈希"""
    hash = 0
    modulus = 1000000007
    for c in key:
        hash = (hash << 4) ^ (hash >> 28) ^ ord(c)
    return hash % modulus

```



## 6、练习题

### 1. [0217. 存在重复元素](https://leetcode.cn/problems/contains-duplicate/)

解答：

```python
class Solution:
    def containsDuplicate(self, nums: List[int]) -> bool:
        num_dict = {}  
        for num in nums:  
            if num in num_dict:  
                return True  
            else:  
                num_dict[num] = 1  
        return False  
```

![image-20231115152007386](.\img\image-20231115152007386.png)

### 2. [0219. 存在重复元素 II](https://leetcode.cn/problems/contains-duplicate-ii/)

解答:

```python
class Solution:
    def containsNearbyDuplicate(self, nums: List[int], k: int) -> bool:
        seen = {}  
        for i, num in enumerate(nums):  
            if num in seen and i - seen[num] <= k:  
                return True  
            seen[num] = i  
        return False
```

![image-20231115152942118](.\img\image-20231115152942118.png)

### 3. [0036. 有效的数独](https://leetcode.cn/problems/valid-sudoku/)

解答：

```python
class Solution:
    def isValidSudoku(self, board: List[List[str]]) -> bool:
        cnt = defaultdict(list)
        for i in range(9):
            for j in range(9):
                cur = board[i][j]
                x, y = i // 3, j //3
                if cur.isdigit():
                    if cur in cnt[(i, -1)] or cur in cnt[(-1, j)]\
                    or cur in cnt[(x, y)]: return False
                    cnt[(i, -1)].append(cur)
                    cnt[(-1, j)].append(cur)
                    cnt[(x, y)].append(cur)
        return True
```

![image-20231115153622231](.\img\image-20231115153622231.png)

### 4. [0349. 两个数组的交集](https://leetcode.cn/problems/intersection-of-two-arrays/)

解答：

```python
class Solution:
    def intersection(self, nums1: List[int], nums2: List[int]) -> List[int]:

        if not nums1 or not nums2:   # 有一个数组为空，则交集为空
            return []
        hash = {}                   # 初始化哈希表
        res = []                    # 初始化结果列表，存放最后结果

        # 哈希表 key 为 nums1 数组中的数，value 为值
        for i in nums1:
            if not hash.get(i):
                hash[i] = 1
        # 遍历 nums，如果 nums2 数组中的数出现在哈希表中，对应数放入结果列表，对应 value 值置-为0
        for j in nums2:
            if hash.get(j):
                res.append(j)
                hash[j] = 0
        return res
```

![image-20231115154218722](D:\www\learning\caioo0.github.io\note-datawhale\docs\leetcode_notes\img\image-20231115154218722.png)

### 5. [0350. 两个数组的交集 II](https://leetcode.cn/problems/intersection-of-two-arrays-ii/)

解答：

```python
class Solution:
    def intersect(self, nums1: List[int], nums2: List[int]) -> List[int]:
        count = Counter(nums1)
        has = []
        for num in nums2:
            if num in count and count[num]:
                has.append(num)
                count[num] -= 1
        return has
```

![image-20231115155037934](.\img\image-20231115155037934.png)

### 6. [0706. 设计哈希映射](https://leetcode.cn/problems/design-hashmap/)

解答：

```python
class MyHashMap:

    def __init__(self):
     
        # 初始化数据结构
        self.hash = collections.defaultdict(lambda: -1)

    def put(self, key: int, value: int) -> None:
        # 将给定的键和值存储到哈希表中。如果键已经存在，则更新对应的值
        self.hash[key] = value

    def get(self, key: int) -> int:
        # 根据给定的键获取对应的值。如果键不存在，则返回-1。
        return self.hash[key]

    def remove(self, key: int) -> None:
        # 从哈希表中删除给定的键及其对应的值。如果键不存在，则不进行任何操作。
        self.hash[key] = -1


# 实例化调用
# obj = MyHashMap()
# obj.put(key,value)
# param_2 = obj.get(key)
# obj.remove(key)
```

![image-20231115155850178](.\img\image-20231115155850178.png)

## 7、参考资料

1、https://zhuanlan.zhihu.com/p/496515259

2、https://tianchi.aliyun.com/course/932/14648

3、https://www.hello-algo.com/chapter_hashing/hash_collision/