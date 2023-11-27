# task05:策略梯度和Actor-critic算法

---

> （本学习笔记来源于DataWhale-第39期组队学习：[强化学习](https://linklearner.com/datawhale-homepage/#/learn/detail/91)） ,[B站视频讲解](https://www.bilibili.com/video/BV1HZ4y1v7eX) 观看地址

## 策略梯度相关概念

- 什么是策略梯度方法？

策略梯度方法是相对于动作价值函数的另一类强化学习思路。
在基于动作价值函数的方法中，我们需要先学习价值函数Q(s,a)，再根据估计的价值函数选择动作，价值函数相当于在不同状态下对不同动作的评分，是不可缺少的。
而在策略梯度方法中，我们会直接学习动作策略，也就是说输出应当是当前状态下应该执行的动作，即π(a|s)=P(a|s)，实际上这里的动作是一个概率分布，更有利的动作会分配到更大的选择概率。
因此策略梯度方法可以用包括神经网络在内的任意模型进行参数化，代表策略的参数向量我们用θ∈Rd′来表示，则t时刻下当状态为s、策略参数为θ时选择执行动作a的概率可写作：

$$
π(a|s,θ)=Pr{At=a|St=s,θt=θ}。
$$

在所有的策略梯度类方法中，我们都会预先确定一个用于评价策略的某种性能指标，这里用J(θ)来表示。我们的目的是最大化这个性能指标，因此利用梯度上升对策略参数θ进行更新：

$$
θt+1=θt+α∇J(θt)ˆ
$$

这里的∇J(θt)ˆ∈Rd′实际上是一个随机估计，它的期望是选定的性能指标J对策略的参数θt的梯度∇J(θt)的近似。对参数更新也就是策略更新的方法，更新后的策略则直接指导动作的执行。
在有些算法中，我们会同时学习策略和近似的价值函数，这类方法被称为actor-critic。

- 策略梯度方法与价值函数方法的比较

基于价值函数的方法很多，以经典的DQN为例，它以神经网络代替Q表来逼近最优Q函数，更新后的网络同时作为价值函数引导动作的选择，一定程度上解决了高维离散输入的问题，使得图像等信息的处理在强化学习中变得可能。但其仍存在一些问题，如：

- 无法表示随机策略，对于某些特殊环境而言，最优的动作策略可能是一个带有随机性的策略，因此需要按特定概率输出动作。
- 无法输出连续的动作值，比如连续范围内的温度数值。
- 价值函数在更新过程中的微小变动可能使得被选中的最优动作完全改变，在收敛过程中缺少鲁棒性。

相对而言，策略梯度算法可以较好地解决上述问题，而且策略的参数化允许我们通过参数模型的引入来添加先验知识。
当然在有些情况下动作价值函数方法会更简单，更容易近似，有些情况下则相反，还是要根据实际情况选择采用的方法。

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



## 总结

### 策略梯度算法：

优点：

1. 简单易懂：策略梯度算法相对直观，易于理解和实现。
2. 适合处理连续动作空间：策略梯度算法可以扩展到连续动作空间，而不仅仅是离散动作空间。
3. 样本效率高：策略梯度算法使用样本平均来估计梯度，使得它能够从有限的样本中学习有效的策略。

缺点：

1. 容易陷入局部最优：策略梯度算法通常容易陷入局部最优解，可能无法找到全局最优解。
2. 动作噪声：策略梯度算法在学习过程中可能会引入动作噪声，这可能会干扰学习过程。
3. 对参数敏感：策略梯度算法对参数的选择非常敏感，不同的参数设置可能会对学习结果产生显著影响。

### Actor-Critic算法：

优点：

1. 结合了策略梯度和值函数估计的优势：Actor-Critic算法结合了策略梯度算法和值函数估计算法的优点，能够同时更新策略和值函数，使得学习过程更加高效。
2. 适合处理连续动作空间：与策略梯度算法类似，Actor-Critic算法也可以扩展到连续动作空间。
3. 样本效率高：Actor-Critic算法使用样本平均来估计梯度和值函数，使得它能够从有限的样本中学习有效的策略。

缺点：

1. 计算量大：由于Actor-Critic算法同时更新策略和值函数，因此计算量相对较大，需要更多的计算资源。
2. 对参数敏感：Actor-Critic算法对参数的选择也非常敏感，不同的参数设置可能会对学习结果产生显著影响。
3. 可能产生过估计：在某些情况下，Actor-Critic算法可能会产生过估计，这可能会干扰学习过程。

## 参考资料：

1. DataWhale组队学习资料——《强化学习》 王琦 杨毅远 江季 著
2. [https://www.cnblogs.com/yijuncheng/p/10138604.html](https://www.cnblogs.com/yijuncheng/p/10138604.html) 值函数近似——Deep Q-learning
3. [https://www.jianshu.com/p/1835317e5886](https://www.jianshu.com/p/1835317e5886) Reinforcement Learning笔记(2)--动态规划与蒙特卡洛方法
4. [https://zhuanlan.zhihu.com/p/114482584](https://zhuanlan.zhihu.com/p/114482584) 强化学习基础 Ⅱ: 动态规划，蒙特卡洛，时序差分