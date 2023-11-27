#   DQN算法、DQN算法进阶]

> （本学习笔记来源于DataWhale-第52期组队学习：[强化学习](https://linklearner.com/datawhale-homepage/#/learn/detail/91)） , [B站视频讲解](https://www.bilibili.com/video/BV1HZ4y1v7eX) 观看地址

## 1.DQN算法

### 1.1 介绍

DQN 算法 ，英文全称（Deep Q-Network）, DeepMind于2015年首次提出。它结合了深度学习和Q学习两种技术，可以解决具有大量状态和动作的复杂问题。

论文：Deep Reinforcement Learning with Double Q-Learning| Proceedings of the AAAI Conference on Artificial Intelligence

代码：https://github.com/indigoLovee/DDQN

Q-learning中，用表（Q-table）来存储每个状态-动作对的Q值。然而，当状态和动作的数量非常大时，用表格存储的方式就会变得不现实，因为需要的存储空间和计算资源会非常巨大。

在DQN中，使用一个神经网络（通常是一个深度神经网络）来近似Q值函数。网络的输入是一个状态，输出是对应于各个可能动作的Q值。通过这种方式，我们就可以在连续的状态空间和大规模的动作空间中工作。

DQN中有几个关键的技术：

1. **经验回放（Experience Replay）**：为了打破数据之间的相关性并提高学习的效率，DQN会将智能体的经验（状态、动作、奖励、新状态）存储在一个数据集中，然后从中随机抽取样本进行学习。
2. **目标网络（Target Network）**：DQN使用了两个神经网络，一个是在线网络，用于选择动作；一个是目标网络，用于计算TD目标（Temporal-Difference Target）。这两个网络有相同的结构，但参数不同。在每一步学习过程中，我们使用在线网络的参数来更新目标网络的参数，但是更新的幅度较小。这样可以提高学习的稳定性。

在DQN中，Q值的更新公式为：

```python
Q(s, a) = r + γ * max_a' Q_target(s', a')
```

其中，Q_target(s', a') 是通过目标网络计算出的Q值，而Q(s, a)则是通过在线网络计算出的Q值。

DQN算法的应用领域非常广泛，从玩电子游戏到控制机器人，都有其身影。其中最著名的应用就是在Atari 2600游戏上的表现，DQN能够在大量的游戏上达到超越人类的性能。

### 1.2 关于两个网络以及如何训练的两个网络

在DQN中，使用了两个不同的神经网络，这两个网络被称为在线网络（Online Network）和目标网络（Target Network）。这两个网络都是用来估计Q值的，但在学习过程中起到了不同的角色。

1. **在线网络**：在线网络用于根据当前的状态s选择智能体的动作a。这个网络会不断地进行学习和更新，以尽可能地提高对Q值的估计。在每个时间步，智能体都会根据在线网络提供的Q值来选择动作，然后根据这个动作和环境的反馈来更新网络的参数。
2. **目标网络**：目标网络用于计算Q值更新公式中的TD目标（Temporal-Difference Target），即下一个状态s'的最大Q值。这个网络的参数不会在每个时间步中都进行更新，而是在一定的间隔后，才将在线网络的参数复制过来。这样可以使学习过程更加稳定，避免因为在线网络的快速更新导致的震荡问题。

在线网络和目标网络的结构是相同的，都是用来估计Q值的深度神经网络。它们的输入是智能体的状态，输出是对应于各个可能动作的Q值。这种网络结构也被称为Q网络。

这两个网络在DQN的学习过程中都起到了重要的作用。在线网络负责智能体的决策，目标网络则保证了学习过程的稳定性。通过这两个网络的配合，DQN能够有效地学习在复杂环境中的最优策略。

**如何训练?**

在线网络和目标网络在DQN中的训练过程是稍有不同的，下面详细解释一下：

1. **在线网络训练**：在线网络的训练主要依靠智能体与环境的交互。每次当智能体在环境中执行一个动作并观察到结果（新状态和奖励）时，我们就可以获得一个样本（状态，动作，奖励，新状态），然后使用这个样本来更新网络的参数。我们希望网络预测的Q值（即 Q(s, a)）接近于从这个样本中计算出的目标值，即 r + γ * max_a' Q_target(s', a')。这个目标值由实际得到的奖励和目标网络预测的未来奖励（discounted）之和构成。我们可以使用梯度下降算法来最小化网络预测的Q值和这个目标值之间的差距（通常使用平方损失函数）。
2. **目标网络训练**：目标网络的训练实际上不涉及到任何从数据中学习的过程，它的参数是直接从在线网络复制过来的。我们定期（每隔一定的步数）将在线网络的参数复制到目标网络。这样做的目的是为了增加学习的稳定性。由于在线网络在训练过程中参数会不断变化，如果我们直接使用在线网络来计算目标值，可能会导致目标值震荡，从而影响学习的稳定性。通过使用一个参数更新较慢的目标网络来计算目标值，可以有效地防止这种情况的发生。

在线网络和目标网络的配合使得DQN能够在复杂的环境中有效地学习。在线网络的参数通过与环境的交互不断更新，以逐渐逼近真实的Q值函数。而目标网络则提供了一个稳定的目标，帮助在线网络更稳定地学习。



### 1.3 算法过程&代码实现



![image-20231122145516492](.\img\image-20231122145516492.png)

DQN算法的大致流程如下：

1. **初始化**：首先，初始化在线网络和目标网络（它们具有相同的结构但是参数不同）。然后，创建一个经验回放缓冲区。
2. **探索与利用**：智能体在每个时间步会选择一个动作。动作的选择可以是随机的（探索），也可以是根据在线网络预测的Q值选择的（利用）。通常，我们会使用一个策略（如ε-greedy策略），使得智能体在初期更倾向于探索，在后期更倾向于利用。
3. **交互与存储**：智能体根据选择的动作与环境交互，然后观察到新的状态和奖励。这个过程产生了一个转移（状态，动作，奖励，新状态），这个转移被存储在经验回放缓冲区中。
4. **学习**：从经验回放缓冲区中随机抽取一批样本，然后使用这些样本来训练在线网络。具体来说，我们计算每个样本的目标值（r + γ * max_a' Q_target(s', a')），然后通过最小化网络预测的Q值和这个目标值之间的差距来更新网络的参数。
5. **更新目标网络**：每隔一定的步数，我们将在线网络的参数复制到目标网络。这样，目标网络的参数保持相对稳定，使得学习过程更加稳定。
6. **迭代**：重复上述步骤（步骤2-5），直到满足停止条件（如达到最大步数或达到预定的性能标准）。



下面是一个使用PyTorch实现的简单的DQN算法的例子。在这个例子中，我们假设环境是OpenAI Gym的CartPole环境。

```python
import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
import gym
from collections import deque
import random

# 定义Q网络
class QNetwork(nn.Module):
    def __init__(self, state_dim, action_dim):
        super(QNetwork, self).__init__()
        self.fc = nn.Sequential(
            nn.Linear(state_dim, 64),
            nn.ReLU(),
            nn.Linear(64, 64),
            nn.ReLU(),
            nn.Linear(64, action_dim)
        )

    def forward(self, state):
        return self.fc(state)

# 创建环境
env = gym.make('CartPole-v0')
state_dim = env.observation_space.shape[0]
action_dim = env.action_space.n

# 创建网络
online_net = QNetwork(state_dim, action_dim)
target_net = QNetwork(state_dim, action_dim)
target_net.load_state_dict(online_net.state_dict())

# 创建优化器
optimizer = optim.Adam(online_net.parameters())

# 创建经验回放缓冲区
replay_buffer = deque(maxlen=10000)

# 设置超参数
epsilon = 1.0  # 探索率
epsilon_decay = 0.995  # 探索率衰减
min_epsilon = 0.01  # 最小探索率
gamma = 0.99  # 折扣因子
batch_size = 64  # 批大小
update_target_every = 100  # 更新目标网络的频率
max_steps = 10000  # 最大步数

# 训练过程
for step in range(max_steps):
    # 选择动作
    state = env.reset()
    state = torch.tensor(state, dtype=torch.float32).unsqueeze(0)
    if np.random.rand() < epsilon:
        action = env.action_space.sample()  # 探索
    else:
        with torch.no_grad():
            action = torch.argmax(online_net(state)).item()  # 利用

    # 执行动作并存储转移
    next_state, reward, done, _ = env.step(action)
    next_state = torch.tensor(next_state, dtype=torch.float32).unsqueeze(0)
    reward = torch.tensor([reward], dtype=torch.float32)
    replay_buffer.append((state, action, reward, next_state, done))
    state = next_state

    # 学习
    if len(replay_buffer) >= batch_size:
        minibatch = random.sample(replay_buffer, batch_size)
        states, actions, rewards, next_states, dones = zip(*minibatch)
        states = torch.cat(states)
        actions = torch.tensor(actions, dtype=torch.long).unsqueeze(1)
        rewards = torch.cat(rewards)
        next_states = torch.cat(next_states)
        dones = torch.tensor(dones, dtype=torch.float32)

        q_values = online_net(states).gather(1, actions)
        with torch.no_grad():
            max_next_q_values = target_net(next_states).max(1)[0]
            target_q_values = rewards + gamma * (1 - dones) * max_next_q_values

        loss = nn.functional.mse_loss(q_values, target_q_values.unsqueeze(1))
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        # 更新目标网络
        if step % update_target_every == 0:
            target_net.load_state_dict(online_net.state_dict())

    # 更新探索率
    epsilon = max(min_epsilon, epsilon * epsilon_decay)

    # 检查是否完成
    if done:
        break

```

## 2.DQN算法进阶

### 2.1 Double DQN 算法

### 2.2 Dueling DQN 算法



## 练习题

* 相比于$\text{Q-learning}$ 算法，$\text{DQN}$ 算法做了哪些改进？
* 为什么要在 $\text{DQN}$ 算法中引入 $\varepsilon-\text{greedy}$ 策略？
* $\text{DQN}$ 算法为什么要多加一个目标网络？
* 经验回放的作用是什么？