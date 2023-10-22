# task04:DQN算法及Actor-Critic算法

---

> （本学习笔记来源于DataWhale-第39期组队学习：[强化学习](https://linklearner.com/datawhale-homepage/#/learn/detail/91)） ,[B站视频讲解](https://www.bilibili.com/video/BV1HZ4y1v7eX) 观看地址

## DQN算法基本原理

### 什么是DQN？

DQN是早期最经典的深度强化学习算法，作为Q-Learning算法的拓展（Q-Learning的坑还没填。。），其核心思想是利用神经网络代替表格式方法来完成 值函数近似 ，此外DQN算法还引入 目标网络（Target Network） 和 经验回放（Experience Replay） 的概念，提升了训练的稳定性和数据利用效率。

### 什么是值函数近似？

在Q-Learning算法中用于评估动作价值的函数被称为Q函数（状态-动作价值函数），它代表了在当前状态s下选择动作a后依据某个确定的策略π得到的预期累计奖励。我们优化的目标就是寻找合适的策略π，使得执行该策略得到的任意状态下的Q值最大化。对于Q-Learning中离散状态空间的值函数，我们可以用Q表来记录，但如果状态空间维度过高或在连续空间中，想要准确求解每个状态每个动作下的Q值就比较困难，通常需要对Q函数进行参数化的近似，在DRL中我们通常选择利用神经网络来拟合这个Q函数，这个过程就被称为值函数近似。

### 什么是目标网络？

在时间差分方法更新Q网络的过程中，根据优化

$$
Qπ(st,at)=rt+Qπ(st+1,π(st+1))Qπ(st,at)=rt+Qπ(st+1,π(st+1))

$$

，若左右两部分均发生变化则会使得训练过程不稳定，收敛困难。因此DQN中引入一个目标网络来与正在被更新的网络分开，目标网络基本保持稳定，用于计算目标Q值（即公式中右半部分的预测Q值），然后每隔一段时间才将当前Q网络的参数更新过来。

### 什么是经验回放？

因为强化学习的采样是一个连续的过程，前后数据关联性很大，而神经网络的训练通常要求数据样本是静态的独立同分布。因此我们在这里引入一个经验池（Replay Buffer）的概念，即将强化学习直接利用当前Q网络的策略采样得到的数据以元组的形式

$$
<st,at,rt,st+1><st,at,rt,st+1>

$$

存储下来，在训练时，从经验池中随机采样一些样本作为一个batch，然后用这个打乱后的batch对Q网络进行更新，而当Buffer装满后最早的数据样本就会被删除。

### 动态规划、蒙特卡洛与时序差分方法的异同

广义的动态规划（Dynamic Programming）是指将复杂问题分解为许多较小的问题来求解，而这些小问题的解可以集合起来反推最初复杂问题的解。在这个过程中需要我们对整个环境（模型）有完整的认识，而且需要对过程中已求解部分问题的结果进行一个储存。在MDP中我们利用值函数储存子问题的解，而用贝尔曼方程进行当前状态解与下一状态解之间的递归。注意，由于模型已知，我们只需要状态值函数V就可以确定策略，而在蒙特卡洛中则需要状态-动作值函数Q来估计每个动作的价值。

广义的蒙特卡洛方法（Monte Carlo Methods）是一种通过大量随机采样来近似构建系统模型的数值模拟方法。在处理MDP时，我们可以通过对序列的完整采样获得一个episode，如果有足够多的episode，我们甚至可以遍历MDP中可能出现的所有序列，即使做不到这一点，大量的采样也可以近似地体现MDP的特性。与动态规划方法不同的是，蒙特卡洛方法无需对模型有充分了解（如了解状态转移概率或即时奖励函数），而是相当于通过大量实验来进行经验总结，同时它对于值函数的估计也不是计算累积回报的期望，而是在充分采样的基础上，直接计算经验平均回报。通俗的说，就是在每个采样序列中记录任意状态s下的某动作a第一次出现后（因为一个状态-动作对可能在序列中出现多次）得到的后续累积回报，记作first-visit，通过多次采样，对(s,a)的first-visit累积回报求平均。由大数定理可知，当采样足够多，这个平均值就会接近价值函数在(s,a)处的取值Qπ(s,a)Qπ(s,a)

## Actor Critic

### Actor Critic算法简介

#### 为什么要有Actor Critic

Actor-Critic的Actor的前身是Policy Gradient，这能让它毫不费力地在连续动作中选取合适的动作，而Q-Learning做这件事会瘫痪，那为什么不直接用Policy Gradient呢，原来Actor-Critic中的Critic的前身是Q-Learning或者其他的以值为基础的学习法，能进行单步更新，而更传统的Policy Gradient则是回合更新，这降低了学习效率。
现在我们有两套不同的体系，Actor和Critic，他们都能用不同的神经网络来代替。现实中的奖惩会左右Actor的更新情况。Policy Gradient也是靠着这个来获取适宜的更新。那么何时会有奖惩这种信息能不能被学习呢？这看起来不就是以值为基础的强化学习方法做过的事吗。那我们就拿一个Critic去学习这些奖惩机制，学习完了以后，由Actor来指手画脚，由Critic来告诉Actor你的哪些指手画脚哪些指得好，哪些指得差，Critic通过学习环境和奖励之间的关系，能看到现在所处状态的潜在奖励，所以用它来指点Actor便能使Actor每一步都在更新，如果使用单纯的Policy Gradient，Actor只能等到回合结束才能开始更新。
但是事务始终有它坏的一面，Actor-Critic设计到了两个神经网络，而且每次都是在连续状态中更新参数，每次参数更新前后都存在相关性，导致神经网络只能片面的看待问题，甚至导致神经网络学不到东西。Google DeepMind为了解决这个问题，修改了Actor-Critic的算法。

#### 改进版Deep Deterministic Policy Gradient(DDPG)

将之前在电动游戏Atari上获得成功的DQN网络加入进Actor-Critic系统中，这种新算法叫做Deep Deterministic Policy Gradient，成功的解决在连续动作预测上的学不到东西的问题。
文章【强化学习】Deep Deterministic Policy Gradient(DDPG)算法详解一文对该算法有详细的介绍，文章链接：https://blog.csdn.net/shoppingend/article/details/124344083?spm=1001.2014.3001.5502

### Actor-Critic算法详解

一句话概括Actor-Critic算法：结合了Policy Gradient(Actor)和Function Approximation(Critic)的方法。Actor基于概率选行为，Critic基于Actor的行为评判行为的得分，Actor根据Critic的评分修改选行为的概率。
Actor-Critic方法的优势：可以进行单步更新，比传统的Policy Gradient要快。
Actor-Critic方法的劣势：取决于Critic的价值判断，但是Critic难收敛，再加上Actor的更新，就更难收敛，为了解决这个问题，Google Deepmind提出了Actor-Critic升级版Deep Deterministic Policy Gradient。后者融合了DQN的优势，解决了收敛难得问题。

这套算法是在普通的Policy Gradient算法上面修改的，如果对Policy Gradient算法不是很了解，可以点这里https://blog.csdn.net/shoppingend/article/details/124297444?spm=1001.2014.3001.5502了解一下。
这套算法打个比方：Actor修改行为时就像蒙着眼睛一直向前开车，Critic就是那个扶方向盘改变Actor开车方向的。

或者说详细点，就是Actor在运用Policy Gradient的方法进行Gradient ascent的时候，由Critic来告诉他，这次的Gradient ascent是不是一次正确的ascent，如果这次的得分不好，那么就不要ascent这么多。

代码主结构

上面是Actor的神经网络结构，代码结构如下：

```for i_episode in range(MAX_EPISODE):
    s = env.reset()
    t = 0
    track_r = []    # 每回合的所有奖励
    while True:
        if RENDER: env.render()

        a = actor.choose_action(s)

        s_, r, done, info = env.step(a)

        if done: r = -20    # 回合结束的惩罚

        track_r.append(r)

        td_error = critic.learn(s, r, s_)  # Critic 学习
        actor.learn(s, a, td_error)     # Actor 学习

        s = s_
        t += 1

        if done or t >= MAX_EP_STEPS:
            # 回合结束, 打印回合累积奖励
            ep_rs_sum = sum(track_r)
            if 'running_reward' not in globals():
                running_reward = ep_rs_sum
            else:
                running_reward = running_reward * 0.95 + ep_rs_sum * 0.05
            if running_reward > DISPLAY_REWARD_THRESHOLD: RENDER = True  # rendering
            print("episode:", i_episode, "  reward:", int(running_reward))
            break

class Actor(object):
    def __init__(self, sess, n_features, n_actions, lr=0.001):
        # 用 tensorflow 建立 Actor 神经网络,
        # 搭建好训练的 Graph.

    def learn(self, s, a, td):
        # s, a 用于产生 Gradient ascent 的方向,
        # td 来自 Critic, 用于告诉 Actor 这方向对不对.

    def choose_action(self, s):
        # 根据 s 选 行为 a

```

上面是Critic的神经网络结构，代码结构如下：

```
class Actor(object):
    def __init__(self, sess, n_features, n_actions, lr=0.001):
        # 用 tensorflow 建立 Actor 神经网络,
        # 搭建好训练的 Graph.

    def learn(self, s, a, td):
        # s, a 用于产生 Gradient ascent 的方向,
        # td 来自 Critic, 用于告诉 Actor 这方向对不对.

    def choose_action(self, s):
        # 根据 s 选 行为 a

```

两者学习方式

Actor 想要最大化期望的reward，在Actor-Critic算法中，我们用“比平时好多少”（TDerror）来当作reward，所以就是：

```
with tf.variable_scope('exp_v'):
    log_prob = tf.log(self.acts_prob[0, self.a])    # log 动作概率
    self.exp_v = tf.reduce_mean(log_prob * self.td_error)   # log 概率 * TD 方向
with tf.variable_scope('train'):
    # 因为我们想不断增加这个 exp_v (动作带来的额外价值),
    # 所以我们用过 minimize(-exp_v) 的方式达到
    # maximize(exp_v) 的目的
    self.train_op = tf.train.AdamOptimizer(lr).minimize(-self.exp_v)

```

Critic的更新更简单，就是像Q-Learning那样更新现实和估计的误差（TDerror）就好。

```
with tf.variable_scope('squared_TD_error'):
    self.td_error = self.r + GAMMA * self.v_ - self.v
    self.loss = tf.square(self.td_error)    # TD_error = (r+gamma*V_next) - V_eval
with tf.variable_scope('train'):
    self.train_op = tf.train.AdamOptimizer(lr).minimize(self.loss)

```

每回合算法

```
for i_episode in range(MAX_EPISODE):
    s = env.reset()
    t = 0
    track_r = []    # 每回合的所有奖励
    while True:
        if RENDER: env.render()

        a = actor.choose_action(s)

        s_, r, done, info = env.step(a)

        if done: r = -20    # 回合结束的惩罚

        track_r.append(r)

        td_error = critic.learn(s, r, s_)  # Critic 学习
        actor.learn(s, a, td_error)     # Actor 学习

        s = s_
        t += 1

        if done or t >= MAX_EP_STEPS:
            # 回合结束, 打印回合累积奖励
            ep_rs_sum = sum(track_r)
            if 'running_reward' not in globals():
                running_reward = ep_rs_sum
            else:
                running_reward = running_reward * 0.95 + ep_rs_sum * 0.05
            if running_reward > DISPLAY_REWARD_THRESHOLD: RENDER = True  # rendering
            print("episode:", i_episode, "  reward:", int(running_reward))
            break

```

## 参考资料：

1. DataWhale组队学习资料——《强化学习》 王琦 杨毅远 江季 著
2. [https://www.cnblogs.com/yijuncheng/p/10138604.html](https://www.cnblogs.com/yijuncheng/p/10138604.html) 值函数近似——Deep Q-learning
3. [https://www.jianshu.com/p/1835317e5886](https://www.jianshu.com/p/1835317e5886) Reinforcement Learning笔记(2)--动态规划与蒙特卡洛方法
4. [https://zhuanlan.zhihu.com/p/114482584](https://zhuanlan.zhihu.com/p/114482584) 强化学习基础 Ⅱ: 动态规划，蒙特卡洛，时序差分
