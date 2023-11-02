# 机器学习中的基本数学知识

> 笔记来源：https://www.cnblogs.com/steven-yang/p/6348112.html

## 线性代数(linear algebra )

### 第一公式

$$
f(x) = xw^T = b
$$

线性分类函数(linear class ifier)，机器学习中最常见的公式。

训练分类器的目标就是求出(w,b)。

其中：

x 是一个单行矩阵 $[[x_1,x_2,...,x_n]]$

w是一个单行矩阵$[[w_1,w_2,...,w_n]]$

x 和 w 的维度相同

b是一个数

$xw^T = \sum_{i=1}^n x_i w_i$ ,称为点积（dot product）.

有时，我们也会见到这个公式表示为类似下面的样子，它们的基本含义都是一样的。
$$
f(x) = wx +b \\
f(x) = w^Tx+b \\
f(x) = \vec{w}\vec{w} +b
$$

> 注： 
>
> 1. w 表示一维数组（或者向量、矢量(vector)）$ [x_i,x_x,...,x_n] $
> 2. $ab \neq ba $ ,所以对于表达式$w^Tx$,严格来说，看作列矩阵（不是行矩阵），才符合数学上的定义。
> 3. 表示式$\vec{w}\vec{x}$ 和$wx$是正确的，因为$w$$和$x$是矢量，这个符合矢量计算的含义。

### 矩阵的操作

#### 置换(transpose)

矩阵的置换操作：将矩阵的数按照对角线交换。

数学公式：$w^T$

代码示例：

```python
# matrix transpose
m = numpy.mat([[1,2],[3,4]])
print(m.T)
```

#### 矩阵乘法

- 矩阵相乘的含义

  如果一斤苹果10元，5斤苹果多少元？  答案$ 10 * 5 = 50 $

  如果一斤苹果10元，一斤梨20元，5斤苹果2斤梨一共多少元？

  答案：
  $$
  \begin{bmatrix}
  10 & 20 
  \end{bmatrix}
  \begin{bmatrix}
  5 \\
  2 
  \end{bmatrix} = 10 \times 5 + 20 \times 2 = 90
  $$
  

$\star$ 矩阵相乘约束：**乘数1的列数要和乘数2的行数相等**。

> 矩阵乘法不满足交换律：$ m1 \cdot m2 = m2 \cdot m1$

