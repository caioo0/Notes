# task03:策略梯度与PPO算法

> （本学习笔记来源于DataWhale-第39期组队学习：[强化学习](https://linklearner.com/datawhale-homepage/#/learn/detail/91)） ,
> [B站视频讲解](https://www.bilibili.com/video/BV1HZ4y1v7eX) 观看地址

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

## 

## 近端策略优化（PPO）算法


## PPO整体思路--PG算法

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

## 接下来是关于PG方法的Tips:

**增加一个基线。** 在上面的介绍方法中PG在更新的时候的基本思想就是增大奖励大的策略动作出现的概率，减小奖励小的策略动作出现的概率。但是当奖励的设计不够好的时候，这个思路就会有问题。极端一点的是：无论采取任何动作，都能获得正的奖励。但是这样，对于那些没有采样到的动作，在公式中这些动作策略就体现为0奖励。则可能没被采样到的更好的动作产生的概率就越来越小，使得最后，好的动作反而都被舍弃了。这当然是不对的。于是我们引入一个基线，让奖励有正有负，一般增加基线的方式是所有采样序列的奖励的平均值：

![](https://pic1.zhimg.com/80/v2-b5c4d2efd156811a61d546a5186efc50_720w.jpg)

**折扣因子。** 这个很容易理解，就像买股票一样，同样一块钱，当前的一块钱比未来期望的一块钱更具有价值。因此在强化学习中，对未来的奖励需要进行一定的折扣：

![](https://pic3.zhimg.com/80/v2-ec8e25c0de99d0e9690117a355474b9a_720w.jpg)

**使用优势函数。** 之前用的方法，对于同一个采样序列中的数据点，我们使用相同的奖励 ![[公式]](https://www.zhihu.com/equation?tex=R%28%5Ctau%29) （见公式1）。这样的做法实在有点粗糙，更细致的做法是：将这里的奖励替换成关于 ![[公式]](https://www.zhihu.com/equation?tex=s_t%2Ca_t) 的函数，我们吧这个函数叫优势函数， 用 ![[公式]](https://www.zhihu.com/equation?tex=A%5E%7B%5Ctheta%7D%28s_t%2C+a_t%29) 来表示

![[公式]](https://www.zhihu.com/equation?tex=A%5E%7B%5Ctheta%7D%28s_t%2Ca_t%29+%3D%5Csum_%7Bt%27%3Et%7D%5Cgamma%5E%7Bt%27-t%7Dr_%7Bt%27%7D-V_%7B%5Cphi%7D%28s_t%29+%5Ctag%7B2%7D)

其中 ![[公式]](https://www.zhihu.com/equation?tex=V_%7B%5Cphi%7D%28s_t%29) 是通过critic来计算得到的，它由一个结构与策略网络相同但参数不同的神经网络构成，主要是来拟合从 ![[公式]](https://www.zhihu.com/equation?tex=s_t) 到终局的折扣奖励。 ![[公式]](https://www.zhihu.com/equation?tex=A%5E%7B%5Ctheta%7D) 前半部分是实际的采样折扣奖励，后半部分是拟合的折扣奖励。 ![[公式]](https://www.zhihu.com/equation?tex=A%5E%7B%5Ctheta%7D) 表示了![[公式]](https://www.zhihu.com/equation?tex=s_t+) 下采取动作 ![[公式]](https://www.zhihu.com/equation?tex=a_t) ，实际得到的折扣奖励相对于模拟的折扣奖励下的优势，因为模拟的折扣奖励是在 ![[公式]](https://www.zhihu.com/equation?tex=s_t) 所有采集过的动作的折扣奖励的拟合（平均），因此这个优势函数也就代表了采用动作 ![[公式]](https://www.zhihu.com/equation?tex=a_t) 相对于这些动作的平均优势。这个优势函数由一个critic(评价者)来给出。

具体来说，譬如在 ![[公式]](https://www.zhihu.com/equation?tex=s_t) , n个不同采样样本中分别选用了动作 ![[公式]](https://www.zhihu.com/equation?tex=%5Calpha_1%2C+%5Calpha_2%2C%5Ccdots%2C+%5Calpha_n) ，分别得到折扣奖励（从 ![[公式]](https://www.zhihu.com/equation?tex=s_t) 到终局）是 ![[公式]](https://www.zhihu.com/equation?tex=%5Cgamma_1%2C%5Cgamma_2%2C%5Ccdots%2C%5Cgamma_n) , 因为![[公式]](https://www.zhihu.com/equation?tex=V_%7B%5Cphi%7D%28s_t%29)是拟合折扣奖励，所以它表示了在 ![[公式]](https://www.zhihu.com/equation?tex=s_t) 下得到的折扣奖励的期望，我们用 ![[公式]](https://www.zhihu.com/equation?tex=%5Cgamma_i) , ![[公式]](https://www.zhihu.com/equation?tex=i%3D1%2C2%2C%5Ccdots%2Cn) , 作为特征去拟合，拟合好后，![[公式]](https://www.zhihu.com/equation?tex=V_%7B%5Cphi%7D%28s_t%29)就代表了![[公式]](https://www.zhihu.com/equation?tex=s_t)的价值（或者说代表了其获得折扣奖励的期望）。那么(2)式就表示了 ![[公式]](https://www.zhihu.com/equation?tex=a_t) 相对于![[公式]](https://www.zhihu.com/equation?tex=%5Calpha_1%2C+%5Calpha_2%2C%5Ccdots%2C+%5Calpha_n)这些动作的平均优势。

![](https://pic2.zhimg.com/80/v2-0dc55c887b1223787804d57404f65e59_720w.jpg)

## PPO算法

接着上面的讲，PG方法一个很大的缺点就是参数更新慢，因为我们每更新一次参数都需要进行重新的采样，这其实是中on-policy的策略，即我们想要训练的agent和与环境进行交互的agent是同一个agent；与之对应的就是off-policy的策略，即想要训练的agent和与环境进行交互的agent不是同一个agent，简单来说，就是拿别人的经验来训练自己。举个下棋的例子，如果你是通过自己下棋来不断提升自己的棋艺，那么就是on-policy的，如果是通过看别人下棋来提升自己，那么就是off-policy的：

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

## 关键字

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

## 问题集

- 如果我们想让机器人自己玩video game, 那么强化学习中三个组成（actor、environment、reward function）部分具体分别是什么？

  答：actor 做的事情就是去操控游戏的摇杆， 比如说向左、向右、开火等操作；environment 就是游戏的主机， 负责控制游戏的画面负责控制说，怪物要怎么移动， 你现在要看到什么画面等等；reward function 就是当你做什么事情，发生什么状况的时候，你可以得到多少分数， 比如说杀一只怪兽得到 20 分等等。
- 在一个process中，一个具体的trajectory $s_1$,$a_1$, $s_2$ , $a_2$ 出现的概率取决于什么？

  答：

  1. 一部分是 **environment 的行为**， environment 的 function 它内部的参数或内部的规则长什么样子。 $p(s_{t+1}|s_t,a_t)$这一项代表的是 environment， environment 这一项通常你是无法控制它的，因为那个是人家写好的，或者已经客观存在的。
  2. 另一部分是 **agent 的行为**，你能控制的是 $p_\theta(a_t|s_t)$。给定一个 $s_t$， actor 要采取什么样的 $a_t$ 会取决于你 actor 的参数 $\theta$， 所以这部分是 actor 可以自己控制的。随着 actor 的行为不同，每个同样的 trajectory， 它就会有不同的出现的概率。
- 当我们在计算 maximize expected reward时，应该使用什么方法？

  答： **gradient ascent（梯度上升）**，因为要让它越大越好，所以是 gradient ascent。Gradient ascent 在 update 参数的时候要加。要进行 gradient ascent，我们先要计算 expected reward $\bar{R}$ 的 gradient 。我们对 $\bar{R}$ 取一个 gradient，这里面只有 $p_{\theta}(\tau)$ 是跟 $\theta$ 有关，所以 gradient 就放在 $p_{\theta}(\tau)$ 这个地方。
- 我们应该如何理解梯度策略的公式呢？

  答：

  $$
  \begin{aligned}
  E_{\tau \sim p_{\theta}(\tau)}\left[R(\tau) \nabla \log p_{\theta}(\tau)\right] &\approx \frac{1}{N} \sum_{n=1}^{N} R\left(\tau^{n}\right) \nabla \log p_{\theta}\left(\tau^{n}\right) \\
  &=\frac{1}{N} \sum_{n=1}^{N} \sum_{t=1}^{T_{n}} R\left(\tau^{n}\right) \nabla \log p_{\theta}\left(a_{t}^{n} \mid s_{t}^{n}\right)
  \end{aligned}

  $$

  $p_{\theta}(\tau)$ 里面有两项，$p(s_{t+1}|s_t,a_t)$ 来自于 environment，$p_\theta(a_t|s_t)$ 是来自于 agent。 $p(s_{t+1}|s_t,a_t)$ 由环境决定从而与 $\theta$ 无关，因此 $\nabla \log p(s_{t+1}|s_t,a_t) =0 $。因此 $\nabla p_{\theta}(\tau)=
  \nabla \log p_{\theta}\left(a_{t}^{n} | s_{t}^{n}\right)$。 公式的具体推导可见我们的教程。

  具体来说：

  * 假设你在 $s_t$ 执行 $a_t$，最后发现 $\tau$ 的 reward 是正的， 那你就要增加这一项的概率，即增加在 $s_t$ 执行 $a_t$ 的概率。
  * 反之，在 $s_t$ 执行 $a_t$ 会导致$\tau$  的 reward 变成负的， 你就要减少这一项的概率。
- 我们可以使用哪些方法来进行gradient ascent的计算？

  答：用 gradient ascent 来 update 参数，对于原来的参数 $\theta$ ，可以将原始的 $\theta$  加上更新的 gradient 这一项，再乘以一个 learning rate，learning rate 其实也是要调的，和神经网络一样，我们可以使用 Adam、RMSProp 等优化器对其进行调整。
- 我们进行基于梯度策略的优化时的小技巧有哪些？

  答：

  1. **Add a baseline：**为了防止所有的reward都大于0，从而导致每一个stage和action的变换，会使得每一项的概率都会上升。所以通常为了解决这个问题，我们把reward 减掉一项叫做 b，这项 b 叫做 baseline。你减掉这项 b 以后，就可以让 $R(\tau^n)-b$ 这一项， 有正有负。 所以如果得到的 total reward $R(\tau^n)$ 大于 b 的话，就让它的概率上升。如果这个 total reward 小于 b，就算它是正的，正的很小也是不好的，你就要让这一项的概率下降。 如果$R(\tau^n)<b$  ， 你就要让这个 state 采取这个 action 的分数下降 。这样也符合常理。但是使用baseline会让本来reward很大的“行为”的reward变小，降低更新速率。
  2. **Assign suitable credit：** 首先第一层，本来的 weight 是整场游戏的 reward 的总和。那现在改成从某个时间 $t$ 开始，假设这个 action 是在 t 这个时间点所执行的，从 $t$ 这个时间点，一直到游戏结束所有 reward 的总和，才真的代表这个 action 是好的还是不好的；接下来我们再进一步，我们把未来的reward做一个discount，这里我们称由此得到的reward的和为**Discounted Return(折扣回报)** 。
  3. 综合以上两种tip，我们将其统称为**Advantage function**， 用 `A` 来代表 advantage function。Advantage function 是 dependent on s and a，我们就是要计算的是在某一个 state s 采取某一个 action a 的时候，advantage function 有多大。
  4. Advantage function 的意义就是，假设我们在某一个 state $s_t$ 执行某一个 action $a_t$，相较于其他可能的 action，它有多好。它在意的不是一个绝对的好，而是相对的好，即相对优势(relative advantage)。因为会减掉一个 b，减掉一个 baseline， 所以这个东西是相对的好，不是绝对的好。 $A^{\theta}\left(s_{t}, a_{t}\right)$ 通常可以是由一个 network estimate 出来的，这个 network 叫做 critic。
- 对于梯度策略的两种方法，蒙特卡洛（MC）强化学习和时序差分（TD）强化学习两个方法有什么联系和区别？

  答：

  1. **两者的更新频率不同**，蒙特卡洛强化学习方法是**每一个episode更新一次**，即需要经历完整的状态序列后再更新（比如我们的贪吃蛇游戏，贪吃蛇“死了”游戏结束后再更新），而对于时序差分强化学习方法是**每一个step就更新一次** ，（比如我们的贪吃蛇游戏，贪吃蛇每移动一次（或几次）就进行更新）。相对来说，时序差分强化学习方法比蒙特卡洛强化学习方法更新的频率更快。
  2. 时序差分强化学习能够在知道一个小step后就进行学习，相比于蒙特卡洛强化学习，其更加**快速、灵活**。
  3. 具体举例来说：假如我们要优化开车去公司的通勤时间。对于此问题，每一次通勤，我们将会到达不同的路口。对于时序差分（TD）强化学习，其会对于每一个经过的路口都会计算时间，例如在路口 A 就开始更新预计到达路口 B、路口 C $\cdots \cdots$, 以及到达公司的时间；而对于蒙特卡洛（MC）强化学习，其不会每经过一个路口就更新时间，而是到达最终的目的地后，再修改每一个路口和公司对应的时间。
- 请详细描述REINFORCE的计算过程。

  答：首先我们需要根据一个确定好的policy model来输出每一个可能的action的概率，对于所有的action的概率，我们使用sample方法（或者是随机的方法）去选择一个action与环境进行交互，同时环境就会给我们反馈一整个episode数据。对于此episode数据输入到learn函数中，并根据episode数据进行loss function的构造，通过adam等优化器的优化，再来更新我们的policy model。
- 给我手工推导一下策略梯度公式的计算过程。

  答：首先我们目的是最大化reward函数，即调整 $\theta$ ，使得期望回报最大，可以用公式表示如下

  $$
  J(\theta)=E_{\tau \sim p_{\theta(\mathcal{T})}}[\sum_tr(s_t,a_t)]

  $$

  对于上面的式子， $\tau$ 表示从从开始到结束的一条完整路径。通常，对于最大化问题，我们可以使用梯度上升算法来找到最大值，即

  $$
  \theta^* = \theta + \alpha\nabla J({\theta})

  $$

  所以我们仅仅需要计算（更新）$\nabla J({\theta})$  ，也就是计算回报函数 $J({\theta})$ 关于 $\theta$ 的梯度，也就是策略梯度，计算方法如下：

  $$
  \begin{aligned}
  \nabla_{\theta}J(\theta) &= \int {\nabla}_{\theta}p_{\theta}(\tau)r(\tau)d_{\tau} \\
  &= \int p_{\theta}{\nabla}_{\theta}logp_{\theta}(\tau)r(\tau)d_{\tau} \\
  &= E_{\tau \sim p_{\theta}(\tau)}[{\nabla}_{\theta}logp_{\theta}(\tau)r(\tau)]
  \end{aligned}

  $$

  接着我们继续讲上式展开，对于 $p_{\theta}(\tau)$ ，即 $p_{\theta}(\tau|{\theta})$ :

  $$
  p_{\theta}(\tau|{\theta}) = p(s_1)\prod_{t=1}^T \pi_{\theta}(a_t|s_t)p(s_{t+1}|s_t,a_t)

  $$

  取对数后为：

  $$
  logp_{\theta}(\tau|{\theta}) = logp(s_1)+\sum_{t=1}^T log\pi_{\theta}(a_t|s_t)p(s_{t+1}|s_t,a_t)

  $$

  继续求导：

  $$
  \nabla logp_{\theta}(\tau|{\theta}) = \sum_{t=1}^T \nabla_{\theta}log \pi_{\theta}(a_t|s_t)

  $$

  带入第三个式子，可以将其化简为：

  $$
  \begin{aligned}
  \nabla_{\theta}J(\theta) &= E_{\tau \sim p_{\theta}(\tau)}[{\nabla}_{\theta}logp_{\theta}(\tau)r(\tau)] \\
  &= E_{\tau \sim p_{\theta}}[(\nabla_{\theta}log\pi_{\theta}(a_t|s_t))(\sum_{t=1}^Tr(s_t,a_t))] \\
  &= \frac{1}{N}\sum_{i=1}^N[(\sum_{t=1}^T\nabla_{\theta}log \pi_{\theta}(a_{i,t}|s_{i,t}))(\sum_{t=1}^Nr(s_{i,t},a_{i,t}))]
  \end{aligned}

  $$
- 可以说一下你了解到的基于梯度策略的优化时的小技巧吗？

  答：

  1. **Add a baseline：**为了防止所有的reward都大于0，从而导致每一个stage和action的变换，会使得每一项的概率都会上升。所以通常为了解决这个问题，我们把reward 减掉一项叫做 b，这项 b 叫做 baseline。你减掉这项 b 以后，就可以让 $R(\tau^n)-b$ 这一项， 有正有负。 所以如果得到的 total reward $R(\tau^n)$ 大于 b 的话，就让它的概率上升。如果这个 total reward 小于 b，就算它是正的，正的很小也是不好的，你就要让这一项的概率下降。 如果$R(\tau^n)<b$  ， 你就要让这个 state 采取这个 action 的分数下降 。这样也符合常理。但是使用baseline会让本来reward很大的“行为”的reward变小，降低更新速率。
  2. **Assign suitable credit：** 首先第一层，本来的 weight 是整场游戏的 reward 的总和。那现在改成从某个时间 $t$ 开始，假设这个 action 是在 t 这个时间点所执行的，从 $t$ 这个时间点，一直到游戏结束所有 reward 的总和，才真的代表这个 action 是好的还是不好的；接下来我们再进一步，我们把未来的reward做一个discount，这里我们称由此得到的reward的和为**Discounted Return(折扣回报)** 。
  3. 综合以上两种tip，我们将其统称为**Advantage function**， 用 `A` 来代表 advantage function。Advantage function 是 dependent on s and a，我们就是要计算的是在某一个 state s 采取某一个 action a 的时候，advantage function 有多大。
- 基于on-policy的policy gradient有什么可改进之处？或者说其效率较低的原因在于？

  答：

  - 经典policy gradient的大部分时间花在sample data处，即当我们的agent与环境做了交互后，我们就要进行policy model的更新。但是对于一个回合我们仅能更新policy model一次，更新完后我们就要花时间去重新collect data，然后才能再次进行如上的更新。
  - 所以我们的可以自然而然地想到，使用off-policy方法使用另一个不同的policy和actor，与环境进行互动并用collect data进行原先的policy的更新。这样等价于使用同一组data，在同一个回合，我们对于整个的policy model更新了多次，这样会更加有效率。
- 使用important sampling时需要注意的问题有哪些。

  答：我们可以在important sampling中将 $p$ 替换为任意的 $q$，但是本质上需要要求两者的分布不能差的太多，即使我们补偿了不同数据分布的权重 $\frac{p(x)}{q(x)}$ 。 $E_{x \sim p}[f(x)]=E_{x \sim q}\left[f(x) \frac{p(x)}{q(x)}\right]$ 当我们对于两者的采样次数都比较多时，最终的结果时一样的，没有影响的。但是通常我们不会取理想的数量的sample data，所以如果两者的分布相差较大，最后结果的variance差距（平方级）将会很大。
- 基于off-policy的importance sampling中的 data 是从 $\theta'$ sample 出来的，从 $\theta$ 换成 $\theta'$ 有什么优势？

  答：使用off-policy的importance sampling后，我们不用 $\theta$ 去跟环境做互动，假设有另外一个 policy  $\theta'$，它就是另外一个actor。它的工作是他要去做demonstration，$\theta'$ 的工作是要去示范给 $\theta$ 看。它去跟环境做互动，告诉 $\theta$ 说，它跟环境做互动会发生什么事。然后，借此来训练$\theta$。我们要训练的是 $\theta$ ，$\theta'$  只是负责做 demo，负责跟环境做互动，所以 sample 出来的东西跟 $\theta$ 本身是没有关系的。所以你就可以让 $\theta'$ 做互动 sample 一大堆的data，$\theta$ 可以update 参数很多次。然后一直到 $\theta$  train 到一定的程度，update 很多次以后，$\theta'$ 再重新去做 sample，这就是 on-policy 换成 off-policy 的妙用。
- 在本节中PPO中的KL divergence指的是什么？

  答：本质来说，KL divergence是一个function，其度量的是两个action （对应的参数分别为$\theta$ 和 $\theta'$ ）间的行为上的差距，而不是参数上的差距。这里行为上的差距（behavior distance）可以理解为在相同的state的情况下，输出的action的差距（他们的概率分布上的差距），这里的概率分布即为KL divergence。
- 请问什么是重要性采样呀？

  答：使用另外一种数据分布，来逼近所求分布的一种方法，算是一种期望修正的方法，公式是：

  $$
  \begin{aligned}
  \int f(x) p(x) d x &= \int f(x) \frac{p(x)}{q(x)} q(x) d x \\
  &= E_{x \sim q}[f(x){\frac{p(x)}{q(x)}}] \\
  &= E_{x \sim p}[f(x)]
  \end{aligned}

  $$

  我们在已知 $q$ 的分布后，可以使用上述公式计算出从 $p$ 分布的期望值。也就可以使用 $q$ 来对于 $p$ 进行采样了，即为重要性采样。
- 高冷的面试官：请问on-policy跟off-policy的区别是什么？

  答：用一句话概括两者的区别，生成样本的policy（value-funciton）和网络参数更新时的policy（value-funciton）是否相同。具体来说，on-policy：生成样本的policy（value function）跟网络更新参数时使用的policy（value function）相同。SARAS算法就是on-policy的，基于当前的policy直接执行一次action，然后用这个样本更新当前的policy，因此生成样本的policy和学习时的policy相同，算法为on-policy算法。该方法会遭遇探索-利用的矛盾，仅利用目前已知的最优选择，可能学不到最优解，收敛到局部最优，而加入探索又降低了学习效率。epsilon-greedy 算法是这种矛盾下的折衷。优点是直接了当，速度快，劣势是不一定找到最优策略。off-policy：生成样本的policy（value function）跟网络更新参数时使用的policy（value function）不同。例如，Q-learning在计算下一状态的预期收益时使用了max操作，直接选择最优动作，而当前policy并不一定能选择到最优动作，因此这里生成样本的policy和学习时的policy不同，即为off-policy算法。
- 高冷的面试官：请简述下PPO算法。其与TRPO算法有何关系呢?

  答：PPO算法的提出：旨在借鉴TRPO算法，使用一阶优化，在采样效率、算法表现，以及实现和调试的复杂度之间取得了新的平衡。这是因为PPO会在每一次迭代中尝试计算新的策略，让损失函数最小化，并且保证每一次新计算出的策略能够和原策略相差不大。具体来说，在避免使用important sampling时由于在 $\theta$ 下的 $p_{\theta}\left(a_{t} | s_{t}\right)$ 跟 在 $\theta'$ 下的 $ p_{\theta'}\left(a_{t} | s_{t}\right) $ 差太多，导致important sampling结果偏差较大而采取的算法。

## 参考资料：

- [理解策略梯度算法](https://zhuanlan.zhihu.com/p/93629846)
- [强化学习进阶 第六讲 策略梯度方法](https://zhuanlan.zhihu.com/p/26174099)
- [Proximal Policy Optimization(PPO)算法原理及实现！](https://www.jianshu.com/p/9f113adc0c50)
- [强化学习之PPO算法](https://zhuanlan.zhihu.com/p/468828804)
