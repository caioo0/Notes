# 强化学习--贝尔曼方程

贝尔曼方程： 强化学习的基础和核心

贝尔曼三个主要概念： **策略函数、状态价值函数 和 状态 - 动作价值函数**（简称动作价值函数）

**策略函数（Policy Function）：**

策略函数是一个输入为s输出为a的函数表示为 ${\pi(s)}$，其中s表示状态，a表示动作，策略函数的含义就是在状态s下应该选择的动作a。

强化学习的核心问题就是最优化策略函数从而最大化后面介绍的价值函数。

**状态价值函数（State Value Function）：**

一个策略$ \pi $的状态价值函数的定义是: 从状态s出发，遵循策略$ \pi $能够获得的期望回报：
$$
V^{\pi}(s)= E_{\pi}[G_{t}|S_{t}=s]
$$
$V(s)$是个数学期望，也就是在状态s之后的动作序列上的累积奖励$G_t$的数学期望。那么$G_t$又是什么呢？在最简单的一个具有马尔科夫性质的序列上面，这个Gt其实就是一个按照时间降权的累积回报：
$$
G_{t}=R_{t}+\gamma R_{t+1}+\gamma^{2}R_{t+2}+...=\sum_{0}^{N}{\gamma^{k}R_{t+k}}
$$
其中$ {R_{t+1}}$ 表示从 ${S_{t}}$ 转移到$ {S_{t+1}} $时获得的回报， $\gamma$ 是折损因子，取值为$ 0\sim1 $。可以将上面的状态价值函数的形式表示为递归的形式：



**动作价值函数**

所谓动作价值，顾名思义就是在当前状态s，执行动作a之后，遵循策略 \pi 能够获得的期望回报：
$$
Q^{\pi}(s,a)= E_{\pi}[G_{t}|S_{t}=s,A_{t}=a]
$$
OK，公式有了，那么这个定义是啥意思呢？可以通俗的解释一下，状态价值是指到达当前这个状态以后，接下来的潜在收益。比如成功拿到了阿里巴巴的offer，那么“在阿里巴巴工作” 这个状态的潜在价值就是未来各种可能工作的收益期望。那动作价值呢，是指现在在阿里巴巴工作了，假设发生跳槽动作，比如跳槽去一家创业公司，这个跳槽动作带来的潜在价值。那这个动作价值呢，又包含了即时奖励（比如创业公司给开年薪50万），和入职创业公司以后的状态价值(比如创业公司会上市，股票会升值）。

用个公式来表达也就是：
$$
Q^{\pi}(s,a)= r(s,a)+\gamma\sum_{s^{'}\in S}^{}{P(s^{'}|s,a)V^{\pi}(s^{'})}
$$




### 贝尔曼方程 (Bellman Equation)



## 资料

1. https://blog.csdn.net/Mocode/article/details/130383093
2. https://zhuanlan.zhihu.com/p/28084942