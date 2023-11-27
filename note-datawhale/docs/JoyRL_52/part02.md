# 免模型预测、免模型控制

> （本学习笔记来源于DataWhale-第52期组队学习：[强化学习](https://linklearner.com/datawhale-homepage/#/learn/detail/91)） , [B站视频讲解](https://www.bilibili.com/video/BV1HZ4y1v7eX) 观看地址

## 1. 免模型预测

免模型预测方法： 蒙特卡洛方法（Monte Carlo,MC）和 时序差分方法(temporal-difference,TD)。

### 基本概念

**有模型（Model based）:** 有模型强化学习是一类依赖于环境模型（状态转移概率和奖励函数）的强化学习算法。有模型算法通过学习环境的模型来进行规划（Planning）和决策。常见的有模型强化学习算法包括动态规划（Dynamic Programming）、蒙特卡洛树搜索（Monte Carlo Tree Search, MCTS）等。

**免模型（Model free）：** 一类不依赖于环境模型（状态转移概率和奖励函数）的[强化学习算法](https://so.csdn.net/so/search?q=强化学习算法&spm=1001.2101.3001.7020)。免模型算法直接通过与环境的交互获取经验数据，并根据这些数据进行学习和优化。常见的免模型强化学习算法包括Q-learning、SARSA、Deep Q-Network（DQN）等。

**预测（prediction）：** 估计或计算环境中的某种期望值，比如：比如状态价值函数 $V(s)$ 或动作价值函数 $Q(s,a)$

**控制（control）：** 找到一种最优策略，常涉及两个相互交替的步骤：策略评估（使用当前策略估计值函数）和策略改进（基于当前的值函数更新策略）。

**免模型与有模型强化学习的区别与比较:**

免模型强化学习不依赖于环境模型，直接通过与环境的交互获取经验数据进行学习。有模型强化学习依赖于环境模型，通过学习环境的模型进行规划和决策。

免模型强化学习适用于环境模型未知或难以获得的情况，例如实际机器人控制、游戏AI等。有

模型强化学习适用于环境模型已知或可以通过学习获得的情况，例如规划问题、棋类游戏等。

免模型强化学习的优点是不需要事先知道环境的状态转移概率和奖励函数，因此适用于许多实际问题。缺点是学习过程可能需要大量的交互数据。有模型强化学习的优点是可以利用环境模型进行规划和决策，从而更加高效地找到最优策略。缺点是需要准确的环境模型，否则可能导致错误的决策。

### 有模型与免模型预测和控制的方法

**有模型（MDP）：**

预测：动态规划DP

控制：policy iteration；value iteration

**免模型：**

预测：MC；TD

控制：Sarsa；Q-learning；

### 1.1 蒙特卡洛方法（Monte Carlo,MC）

蒙特卡洛树搜索是一种基于随机模拟的有模型强化学习算法，常用于解决大状态空间和大动作空间的问题。MCTS包括四个步骤：选择（Selection）、扩展（Expansion）、模拟（Simulation）和回传（Backpropagation）。

### 1.2 时序差分方法(temporal-difference,TD)

## 2.免模型控制

## 2.1 Q-learning

### 2.1.1 算法思想

Q-learning是强化学习算法中`value-based`的算法，Q即Q(s,a)就是在某一个时刻s状态下($s \in S$) 采取动作 $a (a \in A)$动作能够获得收益的期望， 环境根据agent的动作反馈相应的回报reward , 所以算法的主要思想就是将state 与 action构建成一张Q-table来存储Q值 ，然后根据Q值来选取能够获得最大的收益的动作。


| Q-Table | a1       | a2       |
| --------- | ---------- | ---------- |
| s1      | q(s1,a1) | q(s1,a2) |
| s2      | q(s2,a1) | q(s2,a2) |
| s3      | q(s3,a1) | q(s3,a2) |

Q-Learning的目的是学习特定State下、特定Action的价值。是建立一个Q-Table，以State为行、Action为列，通过每个动作带来的奖赏更新Q-Table。

Q-Learning是off-policy的。异策略是指行动策略和评估策略不是一个策略。Q-Learning中行动策略是ε-greedy策略，要更新Q表的策略是贪婪策略。

### 2.1.2  公式推导

Q-learning算法的工作流程如下：

1. **初始化**：Q-values通常开始时被随机初始化，然后在训练过程中进行更新。
2. **探索与利用**：在每个时间步，智能体都需要选择一个行动。这可以通过一种叫做ε-greedy策略的方法来完成，该方法会在探索（随机选择行动）和利用（选择当前Q-value最高的行动）之间进行权衡。
3. **学习**：一旦智能体选择了一个行动并观察到了结果，就可以更新Q-value。更新是基于一个叫做贝尔曼等式的公式，它使用了从采取行动后观察到的奖励，以及预期的未来奖励（基于新状态下的最大Q-value）。

Q-learning算法的更新公式如下：
$$
\tag{3.2}
Q(s_t,a_t) \leftarrow Q(s_t,a_t)+\alpha[r_t+\gamma\max _{a}Q(s_{t+1},a)-Q(s_t,a_t)]
$$

其中，(s)表示当前状态，(a)表示当前行动，(r)表示获得的即时奖励，(s’)表示下一个状态，(a’)表示下一个行动，$(\alpha)$表示学习率，$(\gamma)$表示折扣因子。

![image-20231121103141062](.\img\image-20231121103141062.png)

### 2.1.3 Q-learning实战

我们假设智能体在一个有四个状态（s0, s1, s2, s3）的环境中，并且在每个状态下都可以采取两个动作（a0, a1）。奖励函数和状态转移函数是已知的

```python
import numpy as np

# 建立状态转移和奖励矩阵
# 其中，R[s,a,s'] 是智能体从状态 s 采取动作 a 转移到状态 s' 的奖励
# P[s,a,s'] 是智能体从状态 s 采取动作 a 转移到状态 s' 的概率
R = np.zeros((4, 2, 4))
P = np.zeros((4, 2, 4))

# 初始化 Q 矩阵
Q = np.zeros((4, 2))

# 设定学习参数
alpha = 0.5
gamma = 0.95
epsilon = 0.1
n_episodes = 10000

# 对每个情节进行循环
for _ in range(n_episodes):
    # 初始化状态
    s = np.random.choice([0, 1, 2, 3])
    
    # 对每个时间步进行循环，限制最大步数为 100，防止陷入无限循环
    for _ in range(100):
        # 选择动作，部分时间用于探索，部分时间用于利用
        if np.random.rand() < epsilon:
            a = np.random.choice([0, 1])
        else:
            a = np.argmax(Q[s])
        
        # 根据状态转移概率选择新的状态
        s_ = np.random.choice([0, 1, 2, 3], p=P[s, a])
        
        # 更新 Q 值
        Q[s, a] = Q[s, a] + alpha * (R[s, a, s_] + gamma * np.max(Q[s_]) - Q[s, a])
        
        # 更新当前状态
        s = s_

# 输出最终的 Q 值
print(Q)

```



## 2.2. Sarsa

### 2.2.1 算法思想

Sarsa全称是state-action-reward-state'-action'。 也是采用Q-table的方式存储动作值函数；而且决策部分和Q-Learning是一样的, 也是采用ε-greedy策略。不同的地方在于 Sarsa 的更新方式是不一样的。

1.Sarsa是on-policy的更新方式，它的行动策略和评估策略都是ε-greedy策略。

2.Sarsa是先做出动作后更新。

Q-Learning算法，先假设下一步选取最大奖赏的动作，更新值函数。然后再通过ε-greedy策略选择动作。

Sarsa算法，先通过ε-greedy策略执行动作，然后根据所执行的动作，更新值函数。

### 2.2.2 公式推导

SARSA是另一种免模型强化学习算法，与Q-learning类似，但SARSA是一种同轨算法（On-Policy），即在更新Q值时使用的是实际执行的行动。SARSA算法的更新公式为：

$$
\tag{4.2}
Q(s_t,a_t) \leftarrow Q(s_t,a_t)+\alpha[r_t+\gamma Q(s_{t+1},a_{t+1})-Q(s_t,a_t)]
$$

$\text{Sarsa}$ 算法是直接用下一个状态和动作对应的 $Q$ 值来作为估计值的，而 $\text{Q-learning}$ 算法则是用下一个状态对应的最大 $Q$ 值。

![image-20231121103427880](.\img\image-20231121103427880.png)

### 2.2.3 Sarsa实战

## 总结：

Sarsa是在线学习(On Policy)的算法，因为他是在行动中学习的，而且至始至终**只有一个Policy.** 使用了两次greedy-epsilon 方法来选择出了 Q(S,A) 和 Q(S′,A′)。

而Q-Learning离线学习(Off Policy)的算法，Q-Learning选择 Q(S,A)用了greedy方法，而计算A(S',A')时用的是**max**方法，而真正选择的时候又**不一定会选择max**的行动, 所以 Q learning 学习和行动分别采用了**两套不同的Policy。换句话说，**Q-Learning在更新当前位置**max**方法的Q值的时候会参考表中收益最大的那个值，但下一步不一定会走到那个位置。而Sarsa是先选取下一步要走的位置的Q值来更新当前位置的Q值，当然，选完它下一步一定会去走那一步。

Q-Learning 通过Max的函数，总是在寻找能最快获得宝藏的道路，所以他比较勇敢。而Sarsa 却相对谨慎，因为它选取下一步的位置是严格按照已有学习到的经验来选择，所以它探索未知位置的能力就会很差。

```python
next_action = q_learning_agent.choose_action(next_state)
next_sarsa_action = sarsa_agent.choose_action(next_sarsa_state)
q_learning_agent.update(state, action, reward_value, next_state)
sarsa_agent.update(state, sarsa_action, sarsa_reward_value, next_sarsa_state, next_sarsa_action)
if next_state == 2:
    break
state = next_state
action = next_action
sarsa_action = next_sarsa_action

# 输出训练后的Q值函数
print("Q-learning Q-value Function:")
print(q_learning_agent.Q)
print("SARSA Q-value Function:")
print(sarsa_agent.Q)
```

## 参考资料

1. https://blog.csdn.net/qq_43655453/article/details/107296374
2. https://zhuanlan.zhihu.com/p/316581374
3. https://www.cnblogs.com/xoslh/p/17609512.html
