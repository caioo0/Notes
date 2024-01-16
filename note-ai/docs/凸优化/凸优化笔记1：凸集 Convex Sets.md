# 凸集 Convex Sets

## 1. 凸集

区分两种集合的定义（下面的描述并不是严格的数学语言，领会意思就行了）：

**仿射集（Affine set）: ** $x =  \theta  x_1 + (1 - \theta ) x_2 , \theta \in R$

**凸集（Convex set）：**$x =  \theta  x_1 + (1 - \theta ) x_2 , \theta \in [0,1]$

主要的区别就在于后面$\theta$ 的取值范围，简单理解就是说仿射集类似**直线**，凸集类似**线段**。

更一般的，仿射集都可以表示为线性方程的解集 ，也即${x|Ax = b}$



## 2. 常见凸集

### 2.1 凸包（convec hull）

假如集合 $ S = {x_1,...,x_k}$,则其凸包可以表示为：

$ { \sum^k_{i=1}\theta_ix_i|\sum \theta_i = 1,\theta_i >= 0 }$

![image-20231228202252894](.\img\image-20231228202252894.png)

### 2.2 超平面（Hyperplanes）

类比三维空间中的平面，可以有超平面的定义 