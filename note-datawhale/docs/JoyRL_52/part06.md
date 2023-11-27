# task06 DDPG算法，PPO算法、SAC算法

## 1. 近端策略优化（PPO）算法

### 1.1 PPO整体思路--PG算法

强化学习中，我们有一个Agent作为我们的智能体，它根据策略 ![[公式]](https://www.zhihu.com/equation?tex=%5Cpi) ，在不同的环境状态s下选择相应的动作来执行，环境根据Agent的动作，反馈新的状态以及奖励，Agent又根据新的状态选择新的动作，这样不停的循环，知道游戏结束，便完成了eposide。在深度强化学习中，策略 ![[公式]](https://www.zhihu.com/equation?tex=%5Cpi)是由神经网络构成，神经网络的参数为 ![[公式]](https://www.zhihu.com/equation?tex=%5Ctheta) ，表示成 ![[公式]](https://www.zhihu.com/equation?tex=%5Cpi_%7B%5Ctheta%7D) 。

![](https://pic2.zhimg.com/80/v2-49b826fcc9066dc547ed1866cd98d425_720w.jpg)

一个完整的eposide序列，用 ![[公式]](https://www.zhihu.com/equation?tex=%5Ctau) 来表示。而一个特定的 ![[公式]](https://www.zhihu.com/equation?tex=%5Ctau) 序列发生的概率为：

![](https://pic2.zhimg.com/80/v2-ed4bf312340970ef1d6316d106300499_720w.jpg)

如果是固定的开局方式，这里p(s1)可以省略掉。

对于一个完整的 ![[公式]](https://www.zhihu.com/equation?tex=%5Ctau) 序列，他在整个游戏期间获得的总的奖励用 ![[公式]](https://www.zhihu.com/equation?tex=R%28%5Ctau%29) 来表示。对于给定参数 ![[公式]](https://www.zhihu.com/equation?tex=%5Ctheta) 的策略，我们评估其应该获得的每局中的总奖励是：对每个采样得到的的 ![[公式]](https://www.zhihu.com/equation?tex=%5Ctau) 序列（即每一局）的加权和， 即：

![](https://pic2.zhimg.com/80/v2-5be280df84aa97f9513f5620eb6fcc61_720w.jpg)

这里的\bar{R}_{\theta}是在当前策略参数\theta下，从一局游戏中得到的奖励的期望的无偏估计。

因此，对于一个游戏，我们自然希望通过调整策略参数 ![[公式]](https://www.zhihu.com/equation?tex=%5Ctheta) ,得到的 ![[公式]](https://www.zhihu.com/equation?tex=%5Cbar%7BR%7D_%7B%5Ctheta%7D) 越大越好，因为这意味着，我们选用的策略参数能平均获得更多奖励。这个形式自然就很熟悉了。调整![[公式]](https://www.zhihu.com/equation?tex=%5Ctheta)， 获取更大的![[公式]](https://www.zhihu.com/equation?tex=%5Cbar%7BR%7D_%7B%5Ctheta%7D)， 这个很自然的就想到梯度下降的方式来求解。于是用期望的每局奖励对 ![[公式]](https://www.zhihu.com/equation?tex=%5Ctheta) 求导：

![](https://pic2.zhimg.com/80/v2-f2c9c24359ccb508ca8052ab8b1e8501_720w.jpg)

在这个过程中，第一个等号是梯度的变换；第二三个等号是利用了log函数的特性；第四个等号将求和转化成期望的形式；期望又可以由我们采集到的数据序列进行近似；最后一个等号是将每一个数据序列展开成每个数据点上的形式：

![[公式]](https://www.zhihu.com/equation?tex=%5Cnabla+%5Cbar%7BR%7D_%7B%5Ctheta%7D+%3D+%5Cfrac%7B1%7D%7BN%7D%5Csum_%7Bn%3D1%7D%5E%7BN%7D%5Csum_%7Bt%3D1%7D%5E%7BT_n%7D+R%28%5Ctau%5En%29%5Cnabla%5Clog+p_%7B%5Ctheta%7D%28a_t%5En%7Cs_t%5En%29+%5C%5C+%3D%5Cfrac%7B1%7D%7BN%7D%5Csum_%7Bn%3D1%7D%5E%7BN%7DR%28%5Ctau%5En%29+%5B+%5Csum_%7Bt%3D1%7D%5E%7BT_n%7D+%5Cnabla%5Clog+p_%7B%5Ctheta%7D%28a_t%5En%7Cs_t%5En%29+%5D+%5Ctag%7B1%7D)

之所以把R提出来，因为这样理解起来会更直观一点。形象的解释这个式子就是：每一条采样到的数据序列都会希望 ![[公式]](https://www.zhihu.com/equation?tex=%5Ctheta) 的向着自己的方向进行更新，总体上，我们希望更加靠近奖励比较大的那条序列（效果好的话语权自然要大一点嘛），因此用每条序列的奖励来加权平均他们的更新方向。比如我们假设第三条数据的奖励很大，通过上述公式更新后的策略，使得 ![[公式]](https://www.zhihu.com/equation?tex=p_%7B%5Ctheta%7D%28a%5E3_t%7Cs%5E3_t%29) 发生的概率更大，以后再遇到 ![[公式]](https://www.zhihu.com/equation?tex=s_t%5E3) 这个状态时，我们就更倾向于采取 ![[公式]](https://www.zhihu.com/equation?tex=a_t%5E3) 这个动作，或者说以后遇到的状态和第三条序列中的状态相同时，我们更倾向于采取第三条序列曾经所采用过的策略。具体的算法伪代码是：

![](https://pic4.zhimg.com/80/v2-74078031e977541b2d7b77e147c62003_720w.jpg)

以上，就构成了梯度和采集到的数据序列的近似关系。有了梯度方向和采集的数据序列的关系，一个完整的PG方法就可以表示成：

![](https://pic1.zhimg.com/80/v2-753fccb144e53030b63b319b5966eb80_720w.jpg)

我们首先采集数据，然后基于前面得到的梯度提升的式子更新参数，随后再根据更新后的策略再采集数据，再更新参数，如此循环进行。注意到图中的大红字only used once，因为在更新参数后，我们的策略已经变了，而先前的数据是基于更新参数前的策略得到的

### 1.2 关于PG方法的Tips:

**增加一个基线。** 在上面的介绍方法中PG在更新的时候的基本思想就是增大奖励大的策略动作出现的概率，减小奖励小的策略动作出现的概率。但是当奖励的设计不够好的时候，这个思路就会有问题。极端一点的是：无论采取任何动作，都能获得正的奖励。但是这样，对于那些没有采样到的动作，在公式中这些动作策略就体现为0奖励。则可能没被采样到的更好的动作产生的概率就越来越小，使得最后，好的动作反而都被舍弃了。这当然是不对的。于是我们引入一个基线，让奖励有正有负，一般增加基线的方式是所有采样序列的奖励的平均值：

![](https://pic1.zhimg.com/80/v2-b5c4d2efd156811a61d546a5186efc50_720w.jpg)

**折扣因子。** 这个很容易理解，就像买股票一样，同样一块钱，当前的一块钱比未来期望的一块钱更具有价值。因此在强化学习中，对未来的奖励需要进行一定的折扣：

![](https://pic3.zhimg.com/80/v2-ec8e25c0de99d0e9690117a355474b9a_720w.jpg)

**使用优势函数。** 之前用的方法，对于同一个采样序列中的数据点，我们使用相同的奖励 ![[公式]](https://www.zhihu.com/equation?tex=R%28%5Ctau%29) （见公式1）。这样的做法实在有点粗糙，更细致的做法是：将这里的奖励替换成关于 ![[公式]](https://www.zhihu.com/equation?tex=s_t%2Ca_t) 的函数，我们吧这个函数叫优势函数， 用 ![[公式]](https://www.zhihu.com/equation?tex=A%5E%7B%5Ctheta%7D%28s_t%2C+a_t%29) 来表示

![[公式]](https://www.zhihu.com/equation?tex=A%5E%7B%5Ctheta%7D%28s_t%2Ca_t%29+%3D%5Csum_%7Bt%27%3Et%7D%5Cgamma%5E%7Bt%27-t%7Dr_%7Bt%27%7D-V_%7B%5Cphi%7D%28s_t%29+%5Ctag%7B2%7D)

其中 ![[公式]](https://www.zhihu.com/equation?tex=V_%7B%5Cphi%7D%28s_t%29) 是通过critic来计算得到的，它由一个结构与策略网络相同但参数不同的神经网络构成，主要是来拟合从 ![[公式]](https://www.zhihu.com/equation?tex=s_t) 到终局的折扣奖励。 ![[公式]](https://www.zhihu.com/equation?tex=A%5E%7B%5Ctheta%7D) 前半部分是实际的采样折扣奖励，后半部分是拟合的折扣奖励。 ![[公式]](https://www.zhihu.com/equation?tex=A%5E%7B%5Ctheta%7D) 表示了![[公式]](https://www.zhihu.com/equation?tex=s_t+) 下采取动作 ![[公式]](https://www.zhihu.com/equation?tex=a_t) ，实际得到的折扣奖励相对于模拟的折扣奖励下的优势，因为模拟的折扣奖励是在 ![[公式]](https://www.zhihu.com/equation?tex=s_t) 所有采集过的动作的折扣奖励的拟合（平均），因此这个优势函数也就代表了采用动作 ![[公式]](https://www.zhihu.com/equation?tex=a_t) 相对于这些动作的平均优势。这个优势函数由一个critic(评价者)来给出。

具体来说，譬如在 ![[公式]](https://www.zhihu.com/equation?tex=s_t) , n个不同采样样本中分别选用了动作 ![[公式]](https://www.zhihu.com/equation?tex=%5Calpha_1%2C+%5Calpha_2%2C%5Ccdots%2C+%5Calpha_n) ，分别得到折扣奖励（从 ![[公式]](https://www.zhihu.com/equation?tex=s_t) 到终局）是 ![[公式]](https://www.zhihu.com/equation?tex=%5Cgamma_1%2C%5Cgamma_2%2C%5Ccdots%2C%5Cgamma_n) , 因为![[公式]](https://www.zhihu.com/equation?tex=V_%7B%5Cphi%7D%28s_t%29)是拟合折扣奖励，所以它表示了在 ![[公式]](https://www.zhihu.com/equation?tex=s_t) 下得到的折扣奖励的期望，我们用 ![[公式]](https://www.zhihu.com/equation?tex=%5Cgamma_i) , ![[公式]](https://www.zhihu.com/equation?tex=i%3D1%2C2%2C%5Ccdots%2Cn) , 作为特征去拟合，拟合好后，![[公式]](https://www.zhihu.com/equation?tex=V_%7B%5Cphi%7D%28s_t%29)就代表了![[公式]](https://www.zhihu.com/equation?tex=s_t)的价值（或者说代表了其获得折扣奖励的期望）。那么(2)式就表示了 ![[公式]](https://www.zhihu.com/equation?tex=a_t) 相对于![[公式]](https://www.zhihu.com/equation?tex=%5Calpha_1%2C+%5Calpha_2%2C%5Ccdots%2C+%5Calpha_n)这些动作的平均优势。

![](https://pic2.zhimg.com/80/v2-0dc55c887b1223787804d57404f65e59_720w.jpg)

### 1.3 PPO算法思想

PG方法一个很大的缺点就是参数更新慢，因为我们每更新一次参数都需要进行重新的采样，这其实是中on-policy的策略，即我们想要训练的agent和与环境进行交互的agent是同一个agent；与之对应的就是off-policy的策略，即想要训练的agent和与环境进行交互的agent不是同一个agent，简单来说，就是拿别人的经验来训练自己。举个下棋的例子，如果你是通过自己下棋来不断提升自己的棋艺，那么就是on-policy的，如果是通过看别人下棋来提升自己，那么就是off-policy的：

![](https://pic4.zhimg.com/80/v2-c1ebc1f92badb22d014761feab8f34af_720w.jpg)

那么为了提升我们的训练速度，让采样到的数据可以重复使用，我们可以将on-policy的方式转换为off-policy的方式。即我们的训练数据通过另一个相同结构的网络（对应的网络参数为θ'）得到

岔开一下话题，这里介绍一下重要性采样：

![](https://pic2.zhimg.com/80/v2-c240f6e7587d76ddd07dfe1315137f11_720w.jpg)

这里的重要采样其实是一个很常用的思路。在其他很多算法（诸如粒子滤波等）中也经常用到。先引入问题：对于一个服从概率p分布的变量x， 我们要估计f(x) 的期望。直接想到的是，我们采用一个服从p的随机产生器，直接产生若干个变量x的采样，然后计算他们的函数值f(x)，最后求均值就得到结果。但这里有一个问题是，对于每一个给定点x，我们知道其发生的概率，但是我们并不知道p的分布，也就无法构建这个随机数发生器。因此需要转换思路：从一个已知的分布q中进行采样。通过对采样点的概率进行比较，确定这个采样点的重要性。也就是上图所描述的方法。

当然通过这种采样方式的分布p和q不能差距过大，否则，会由于采样的偏离带来谬误。即如下图：

![](https://pic4.zhimg.com/80/v2-f61568d93399972c524363e4364098fb_720w.jpg)

回到PPO中，我们之前的PG方法每次更新参数后，都需要重新和环境进行互动来收集数据，然后用的数据进行更新，这样，每次收集的数据使用一次就丢掉，很浪费，使得网络的更新很慢。于是我们考虑把收集到数据进行重复利用。假设我们收集数据时使用的策略参数是 ![[公式]](https://www.zhihu.com/equation?tex=%5Ctheta%27) ,此时收集到的数据 ![[公式]](https://www.zhihu.com/equation?tex=%5Ctau) 保存到记忆库中，但收集到足够的数据后，我们对参数按照前述的PG方式进行更新，更新后，策略的参数从 ![[公式]](https://www.zhihu.com/equation?tex=%5Ctheta%27+%5Crightarrow+%5Ctheta) ，此时如果采用PG的方式，我们就应该用参数 ![[公式]](https://www.zhihu.com/equation?tex=%5Ctheta) 的策略重新收集数据，但是我们打算重新利用旧有的数据再更新更新 ![[公式]](https://www.zhihu.com/equation?tex=%5Ctheta) 。注意到我我们本来应该是基于 ![[公式]](https://www.zhihu.com/equation?tex=%5Ctheta) 的策略来收集数据，但实际上我们的数据是由 ![[公式]](https://www.zhihu.com/equation?tex=%5Ctheta%27) 收集的，所以就需要引入重要性采样来修正这二者之间的偏差，这也就是前面要引入重要性采样的原因。

利用记忆库中的旧数据更新参数的方式变为：

![](https://pic1.zhimg.com/80/v2-98ce6175627cbf2dc22c0f98d6987fac_720w.jpg)

当然，这种方式还是比较原始的，我们通过引入Tips中的优势函数，更精细的控制更细，则更新的梯度变为：

![[公式]](https://www.zhihu.com/equation?tex=%5Cnabla%5Cbar%7BR%7D+%3D+E_%7B%5Ctau%5Csim+p_%7B%5Ctheta%27%7D%28%5Ctau%29%7D%5B%5Cfrac%7Bp_%7B%5Ctheta%7D%7D%7Bp_%7B%5Ctheta%27%7D%7DA%5D+%3D+%5Csum_%7Bt%3D1%7D%5ET%5Cfrac%7Bp_%7B%5Ctheta%7D%28a_t%7Cs_t%29%7D%7Bp_%7B%5Ctheta%27%7D%28a_t%7Cs_t%29%7DA_t%28s_t%2Ca_t%29+%5Ctag%7B3%7D)

同时，根据重要性采样来说， ![[公式]](https://www.zhihu.com/equation?tex=p_%7B%5Ctheta%7D%E5%92%8Cp_%7B%5Ctheta%27%7D) 不能差太远了，因为差太远了会引入谬误，所以我们要用KL散度来惩罚二者之间的分布偏差。所以就得到了：

![[公式]](https://www.zhihu.com/equation?tex=+%5Cnabla%5Cbar%7BR%7D+%3D+%5Csum_%7Bt%3D1%7D%5ET%5Cfrac%7Bp_%7B%5Ctheta%7D%28a_t%7Cs_t%29%7D%7Bp_%7B%5Ctheta%27%7D%28a_t%7Cs_t%29%7DA_t%28s_t%2Ca_t%29-%5Clambda+KL%5B%5Ctheta%2C+%5Ctheta%27%5D+%5Ctag%7B4%7D)

这里再解释一下优势函数（2）的构成：

![[公式]](https://www.zhihu.com/equation?tex=A%5E%7B%5Ctheta%7D%28s_t%2Ca_t%29+%3D%5Csum_%7Bt%27%3Et%7D%5Cgamma%5E%7Bt%27-t%7Dr_%7Bt%27%7D-V_%7B%5Cphi%7D%28s_t%29+%5Ctag%7B2%7D+)

其中前半部分就是我们收集到的数据中的一个序列 ![[公式]](https://www.zhihu.com/equation?tex=%5Ctau) 中的某一个动作点之后总的折扣奖励。后半部分是critic网络对 ![[公式]](https://www.zhihu.com/equation?tex=s_t) 这个状态的评价。critic网络我们可以看成是一个监督学习网络，他的目的是估计从一个状态 ![[公式]](https://www.zhihu.com/equation?tex=s_t) 到游戏结束能获得的总的折扣奖励，相当于对 ![[公式]](https://www.zhihu.com/equation?tex=s_t) 这个状态的一个评估。从另一个角度看，这里的 ![[公式]](https://www.zhihu.com/equation?tex=V_%7B%5Cphi%7D%28s_t%29) 也可以看成是对 ![[公式]](https://www.zhihu.com/equation?tex=s_t) 这个状态的后续所以折扣奖励的期望，这就成为了前面Tips中的奖励的基准。

既然是监督学习，我们对 ![[公式]](https://www.zhihu.com/equation?tex=V_%7B%5Cphi%7D%28%5Ccdot%29) 的训练就是对每一个数据序列中的每一个动作点的后续折扣奖励作为待学习的特征，来通过最小化预测和特征之间的误差来更新参数。

通过以上，我们可以看到PPO的更新策略其实有三套网络参数：

一套策略参数 ![[公式]](https://www.zhihu.com/equation?tex=%5Ctheta) ，他与环境交互收集批量数据，然后批量数据关联到 ![[公式]](https://www.zhihu.com/equation?tex=%5Ctheta) 的副本中。他每次都会被更新。

一套策略参数的副本 ![[公式]](https://www.zhihu.com/equation?tex=%5Ctheta%27) ，他是策略参数与环境互动后收集的数据的关联参数，相当于重要性采样中的q分布。

一套评价网络的参数 ![[公式]](https://www.zhihu.com/equation?tex=%5Cphi) ，他是基于收集到的数据，用监督学习的方式来更新对状态的评估。他也是每次都更新。

打个比喻来说，PPO的思路是：

0点时：我与环境进行互动，收集了很多数据。然后利用数据更新我的策略，此时我成为1点的我。当我被更新后，理论上，1点的我再次与环境互动，收集数据，然后把我更新到2点，然后这样往复迭代。

但是如果我仍然想继续0点的我收集的数据来进行更新。因为这些数据是0点的我（而不是1点的我）所收集的。所以，我要对这些数据做一些重要性重采样，让这些数据看起来像是1点的我所收集的。当然这里仅仅是看起来像而已，所以我们要对这个“不像”的程度加以更新时的惩罚（KL）。

其中，更新的方式是：我收集到的每个数据序列，对序列中每个（s, a）的优势程度做评估，评估越好的动作，将来就又在s状态时，让a出现的概率加大。这里评估优势程度的方法，可以用数据后面的总折扣奖励来表示。另外，考虑引入基线的Tip，我们就又引入一个评价者小明，让他跟我们一起学习，他只学习每个状态的期望折扣奖励的平均期望。这样，我们评估（s, a）时，我们就可以吧小明对 s 的评估结果就是 s 状态后续能获得的折扣期望，也就是我们的基线。注意哈：优势函数中，前一半是实际数据中的折扣期望，后一半是估计的折扣期望（小明心中认为s应该得到的分数，即小明对s的期望奖励），如果你选取的动作得到的实际奖励比这个小明心中的奖励高，那小明为你打正分，认为可以提高这个动作的出现概率；如果选取的动作的实际得到的奖励比小明心中的期望还低，那小明为这个动作打负分，你应该减小这个动作的出现概率。这样，小明就成为了一个评判官。

当然，作为评判官，小明自身也要提高自己的知识文化水平，也要在数据中不断的学习打分技巧，这就是对 ![[公式]](https://www.zhihu.com/equation?tex=%5Cphi) 的更新了。

最后，贴出整个PPO的伪代码：

![](https://pic4.zhimg.com/80/v2-9208ac7c5d514191a14c16ceee2bde5f_720w.jpg)

### 关键字

- **policy（策略）：** 每一个actor中会有对应的策略，这个策略决定了actor的行为。具体来说，Policy 就是给一个外界的输入，然后它会输出 actor 现在应该要执行的行为。**一般地，我们将policy写成 $\pi$ 。**
- **Return（回报）：** 一个回合（Episode）或者试验（Trial）所得到的所有的reward的总和，也被人们称为Total reward。**一般地，我们用 $R$ 来表示它。**
- **Trajectory：** 一个试验中我们将environment 输出的 $s$ 跟 actor 输出的行为 $a$，把这个 $s$ 跟 $a$ 全部串起来形成的集合，我们称为Trajectory，即 $\text { Trajectory } \tau=\left\{s_{1}, a_{1}, s_{2}, a_{2}, \cdots, s_{t}, a_{t}\right\}$。
- **Reward function：** 根据在某一个 state 采取的某一个 action 决定说现在这个行为可以得到多少的分数，它是一个 function。也就是给一个 $s_1$，$a_1$，它告诉你得到 $r_1$。给它 $s_2$ ，$a_2$，它告诉你得到 $r_2$。 把所有的 $r$ 都加起来，我们就得到了 $R(\tau)$ ，代表某一个 trajectory $\tau$ 的 reward。
- **Expected reward：** $\bar{R}_{\theta}=\sum_{\tau} R(\tau) p_{\theta}(\tau)=E_{\tau \sim p_{\theta}(\tau)}[R(\tau)]$。
- **REINFORCE：** 基于策略梯度的强化学习的经典算法，其采用回合更新的模式。
- **on-policy(同策略)：** 要learn的agent和环境互动的agent是同一个时，对应的policy。
- **off-policy(异策略)：** 要learn的agent和环境互动的agent不是同一个时，对应的policy。
- **important sampling（重要性采样）：** 使用另外一种数据分布，来逼近所求分布的一种方法，在强化学习中通常和蒙特卡罗方法结合使用，公式如下：$\int f(x) p(x) d x=\int f(x) \frac{p(x)}{q(x)} q(x) d x=E_{x \sim q}[f(x){\frac{p(x)}{q(x)}}]=E_{x \sim p}[f(x)]$  我们在已知 $q$ 的分布后，可以使用上述公式计算出从 $p$ 这个distribution sample x 代入 $f$ 以后所算出来的期望值。
- **Proximal Policy Optimization (PPO)：** 避免在使用important sampling时由于在 $\theta$ 下的 $p_{\theta}\left(a_{t} | s_{t}\right)$ 跟 在  $\theta '$  下的 $p_{\theta'}\left(a_{t} | s_{t}\right)$ 差太多，导致important sampling结果偏差较大而采取的算法。具体来说就是在training的过程中增加一个constrain，这个constrain对应着 $\theta$  跟 $\theta'$  output 的 action 的 KL divergence，来衡量 $\theta$  与 $\theta'$ 的相似程度。

## 2. DDPG

### 2.1 概念

DDPG，全称是deep deterministic policy gradient，深度确定性策略梯度算法。

DDPG和PPO一样，也是AC的架构。加上名字上有PG字眼，所以在学习的时候，很多人会以为DDPG就是只输出一个动作的PPO，所以直接省去了impotance sampling等一堆麻烦的事情。

但两者的思路是完全不一样的，DDPG更接近DQN，是用一个actor去弥补DQN不能处理连续控制性问题的缺点。

在这里我们可以将DDPG分为两部分，

- 一是作为“演员”（Actor）的策略网络，
- 二是作为“评论家”的价值网络。策略网络利用策略梯度方法进行更新，但它不是直接与环境交互来计算目标函数，而是通过价值网络估计的Q值来调整自己的网络参数**θ**θ。也就是说“演员”并不直接与提供奖励的观众（环境）接触，而是利用价值网络间接地获得对动作的评价。

与此同时，价值网络部分可以看作经典的DQN模型

- 一方面与环境交互，利用reward来更新自己Q网络的参数**w**；
- 另一方面它作为评委需要估算当前状态和动作的Q值来引导策略网络的更新。

由于借鉴了DQN中的一些思想，DDPG中的策略网络和价值网络也都各分为两部分，**即一个用于每步更新的当前网络和一个用于计算预测的Q值及动作的目标（target）网络**，后者每隔一段时间从当前网络中复制参数，加起来总共四个网络。这样可以尽量保证预测时可以得到比较稳定的Q值，有助于模型的收敛。

![image-20231123114625522](.\img\image-20231123114625522.png)

### Critic

- Critic网络的作用是预估Q，虽然它还叫Critic，但和AC中的Critic不一样，这里预估的是Q不是V；
- 注意Critic的输入有两个：动作和状态，需要一起输入到Critic中；
- Critic网络的loss其还是和AC一样，用的是TD-error。这里就不详细说明了，我详细大家学习了那么久，也知道为什么了。

### Actor

- 和AC不同，Actor输出的是一个动作；
- Actor的功能是，输出一个动作A，这个动作A输入到Crititc后，能够获得最大的Q值。
- 所以Actor的更新方式和AC不同，不是用带权重梯度更新，而是用梯度上升。

弄清楚怎么来的，就不会和PPO混淆在一起了。也就明白为什么说DDPG是源于DQN而不是AC了。

所以，和DQN一样，更新的时候如果更新目标在不断变动，会造成更新困难。所以DDPG和DQN一样，用了固定网络(fix network)技术，就是先冻结住用来求target的网络。在更新之后，再把参数赋值到target网络。

所以在实做的时候，我们需要4个网络。actor, critic, Actor_target, cirtic_target。

![image-20231123114723218](.\img\image-20231123114723218.png)

> 示例代码:[tutorial_DDPG](https://link.zhihu.com/?target=https%3A//github.com/louisnino/RLcode/blob/master/tutorial_DDPG.py)

# 3. SAC算法

### 3.1 SAC算法简介

柔性动作-评价（Soft Actor-Critic，SAC）算法的网络结构有5个。SAC算法解决的问题是 **离散动作空间和连续动作空间** 的强化学习问题，是 **off-policy** 的强化学习算法（关于on-policy和off-policy的讨论可见：[强化学习之图解PPO算法和TD3算法](https://zhuanlan.zhihu.com/p/384497349)）。

论文：

1. [Soft Actor-Critic Algorithms and Applications](https://link.zhihu.com/?target=https%3A//arxiv.org/pdf/1812.05905.pdf)
2. [Soft Actor-Critic Algorithms and Applications](https://link.zhihu.com/?target=https%3A//arxiv.org/pdf/1812.05905.pdf)

本文介绍的算法思路是1个actor网络，2个V Critic网络（1个V Critic网络，1个Target V Critic网络），2个Q Critic网络.

### 3.2. 网络结构

## 4. 参考

1. https://zhuanlan.zhihu.com/p/385658411
