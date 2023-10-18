# 第1章：基本原理简介
> 第一周实验题地址：[unit01实验](./docs/diffusion_models_51/colab_Doffisers/colab_Doffisers.md) 
> DDPM论文相关：
>
> [DDPM: Denoising Diffusion Probabilistic Models](https%3A//arxiv.org/abs/2006.11239)
>
> [DDPM相关数学知识](https://link.zhihu.com/?target=https%3A//t.bilibili.com/700526762586538024%3Fspm_id_from%3D333.999.0.0)

扩散模型（Diffusion Model）是一类当前比较先进的基于物理力学中的扩散思想的深度学习生成模型。扩散模型包括：前向扩散 和 后向扩散

生成模型除扩散模型外，还有出现较早的 VAE（Variational Auto-Encoder，变分⾃编码器）和GAN（Generative Adversarial Net，⽣成对抗⽹络）等。

DDPM较之前的扩散模型（[Deep Unsupervised Learning using Nonequilibrium Thermodynamics](https://link.zhihu.com/?target=https%3A//arxiv.org/abs/1503.03585)）进行了简化，并通过**变分推断**（variational inference）来进行建模。

因为扩散模型也是一个**隐变量模型**（latent variable model），相比VAE这样的隐变量模型，扩散模型的隐变量是和原始数据是同维度的，而且推理过程（即扩散过程）往往是固定的。

## 1. 扩散模型原理

### 生成模型

通俗定义：生成模型可以描述成一个生成数据的模型，一种概率模型。通过这个模型我们可以生成不包含在训练数据集中的新的数据。比如我们有很多马的图片通过生成模型学习这些马的图像，从中学习到马的样子，生成模型就可以生成看起来很真实的马的图像并却这个图像是不属于训练图像的。

严肃定义：根据给定的样本（训练数据）生成新样本。

> 首先给定一批训练数据$X$,假设其服从某种复杂的真实分布$p(x)$,则给定的训练数据可视为从该分布中采样的观测样本$x$.其作用式估计该训练数据的真实分布，并将其假定为$q(x)$,这个过程又称为拟合网络。

**划重点：**求得估计的分布$q(x)$和真实分布$p(x)$的差距最小，解决方法之一就通过最⼤似然估计思想对训练数据的分布进⾏建模，并求得所有的训练数据样本采样⾃q(x)的概率最⼤，最⼤似然估计思想也是⽣成模型的基本思想之⼀。

### **扩散过程**

扩散模型可看作⼀个更深层次的VAE。扩散模型的表达能⼒更加丰富，⽽且其核⼼在于扩散过程。

扩散的思想来⾃物理学中的⾮平衡热⼒学分⽀。其中最为典型的研究案例是⼀滴墨⽔在⽔中扩散的过程。在扩散开始之前，这滴墨⽔会在⽔中的某个地⽅形成⼀个⼤的斑点，我们可以认为这是这滴墨⽔的初始状态，但要描述该初始状态的概率分布则很困难，因为这个概率分布⾮常复杂。随着扩散过程的进⾏，这滴墨⽔随着时间的推移逐步扩散到⽔中，⽔的颜⾊也逐渐变成这滴墨⽔的颜⾊。

在这种情况下，⾮平衡热⼒学就派上⽤场了，它可以描述这滴墨⽔随时间推移的扩散过程中每⼀个“时间步”（旨在将连续的时间过程离散化）状态的概率分布。若能够想到办法把这个过程反过来，就可以从简单的分布中逐步推断出复杂的分布。

公认最早的**扩散模型DDPM（Denoising Diffusion Probabilistic Model）**的扩散原理就由此⽽来，不过仅有上述条件依然很难从简单的分布倒推出复杂的分布。DDPM还做了⼀些假设，例如假设扩散过程是**⻢尔可夫过程 （即每⼀个时间步状态的概率分布仅由上⼀个时间步状态的概率分布加上当前时间步的⾼斯噪声得到）**，以及假设扩散过程的逆过程是**⾼斯分布**等。

![image-20231015155238906](.\img\image-20231015155238906.png)

DDPM的扩散过程具体分为**前向过程和反向过程**两部分。

其中前向过程又称为**扩散过程（diffusion process）**。无论是前向过程还是反向过程都是一个**参数化的马尔可夫链（Markov chain）**，

其中反向过程可用于生成数据样本（它的作用类似GAN中的生成器，只不过GAN生成器会有维度变化，而DDPM的反向过程没有维度变化）

![image-20231015155649314](.\img\image-20231015155649314.png)

- $x_0 到 x_T$ 为逐步加噪过的**前向程**，噪声是已知的，该过程从原始图片逐步加噪至一组纯噪声。
- $x_T 到 x_0$ 为将一组随机噪声还原为输入的过程。该过程需要学习一个去噪过程，直到还原一张图片。

**前向过程**

前向过程是**加噪**的过程，前向过程中图像 $x_t$ 只和上一时刻的 $x_{t-1}$ 有关, 该过程可以视为马尔科夫过程, 满足:

$q(x_{1:T}|x_0) = \prod_{t = 1}^{T}q(x_t|x_{t-1})$

$q(x_t|x_{t-1}) = N(x_t, \sqrt{1-\beta_t}x_{t-1},\beta_t I)$

其中不同$t$的 $\beta_t$ 是预先定义好的逐渐衰减的，可以是Linear，Cosine等，满足 $\beta_1<\beta_2<...<\beta_T$ 。

根据以上公式，可以通过重参数化采样得到x_t。 $\epsilon \sim N(0,I) ，\alpha_t = 1 - \beta_t$

$\overline\alpha_t=\Pi_{i=1}^{T}\alpha_i$

经过推导，可以得出 x_t 与x_0 的关系：

$q(x_t|x_0)=N(x_t;\sqrt{\overline\alpha_t}x_0,(1-\overline\alpha_t)I)$

**反向过程**

反向过程是去噪的过程，如果得到反向过程 $q(x_{t-1}|x_{t})$，就可以通过随机噪声$ x_T $逐步还原出一张图像。DDPM使用神经网络 $p_{\theta}(x_{t-1}|x_{t})$ 拟合反向过程 $q(x_{t-1}|x_{t})$ 。

$q(x_{t-1}|x_{t},x_0)=N(x_{t-1}|\tilde{\mu_t}(x_t,x_0),\tilde{\beta_t}I)$ ，可以推导出:

$p_\theta(x_{t-1}|x_{t}) = N(x_{t-1}|\mu_{\theta}(x_t,t),\Sigma_{\theta}(x_t,t))$

DDPM论文中不计方差，通过神经网络拟合均值$\mu_{\theta}$ ，从而得到 $x_{t-1}$ ,

$\mu_{\theta} = \frac{1}{\sqrt{\alpha_t}}(x_t-\frac{1-{\alpha_t}}{\sqrt{1-\overline{\alpha_t}}}\epsilon_{\theta(x_t,t)})$

因为 $t$ 和 $x_t$ 已知，只需使用神经网络拟合 $\epsilon_{\theta(x_t,t)}$

**优化目标**

扩散模型预测得是噪声残差，即要求反向过程中预测的噪声分布与前向过程中施加的噪声分布之间的“距离”最小。

如果我们把中间产生的变量看成隐变量的话，那么扩散模型其实是包含T个隐变量的**隐变量模型（latent variable model）**，它可以看成是一个特殊的**Hierarchical VAEs**（见[Understanding Diffusion Models: A Unified Perspective](https://link.zhihu.com/?target=https%3A//arxiv.org/abs/2208.11970)）：

![img](.\img\v2-5d7343c24d2b9346e9666a0d386dcec3_1440w.webp)

相比VAE来说，扩散模型的隐变量是和原始数据同维度的，而且encoder（即扩散过程）是固定的。既然扩散模型是隐变量模型，那么我们可以就可以基于**变分推断**来得到变分下界[variational lower bound](https://link.zhihu.com/?target=https%3A//en.wikipedia.org/wiki/Evidence_lower_bound)（**VLB**，又称**ELBO**）作为最大化优化目标，最后得到最终优化目标得数学表达式 如下：

$L_{t-1}^{\text{simple}}=\mathbb{E}_{\mathbf{x}_{0},\mathbf{\epsilon}\sim \mathcal{N}(\mathbf{0}, \mathbf{I})}\Big[ \| \mathbf{\epsilon}- \mathbf{\epsilon}_\theta\big(\sqrt{\bar{\alpha}_t}\mathbf{x}_0 + \sqrt{1 - \bar{\alpha}_t}\mathbf{\epsilon}, t\big)\|^2\Big]$

在训练DDPM时，只要用一个简单的MSE（Mean Squared Error ,均方误差）损失来最小化前向过程施加的噪声分布和后向过程预测的噪声分布，就能实现最终的优化目标。

## 2. 扩散模型的发展

- 开始扩散：基础扩散模型的提出与改进；
- 加速生成：采样器；
- 刷新纪录：基于显式分类器引导的扩散模型；
- 引爆网络：基于 CLIP ( Contrastive Language - Image Pretraining ，对比语言﹣图像预处理）的多模态图像生成；
- 再次"出图"：大模型的"再学习"方法﹣ DreamBooth 、 LoRA 和 ControlNet ；
- 开启 AI 作画时代：众多商业公司提出成熟的图像生成解决方案。

**1）开始扩散：基础扩散模型的提出与改进**

图像生成领域，最早出现的扩散模型是 DDPM （于2020年提出）。DDPM 首次将"去噪"扩散概率模型应用到图像生成任务中，奠定了扩散模型在图像生成领域应用的基础，包括扩散过程定义、噪声分布假设、马尔可夫链计算、随机微分方程求解和损失函数表征等.

**2）加速生成：采样器**

采样过程是一个随机微分方程，通过离散化地求解该随机微分方程，就可以降低采样的步数。相关论文《Score-Based Generative Modeling through Stochastic Differential Equations》

目前市面的一些求解器: 如 **Euler、SDE、DPM-Solver++和Karras**。

![image-20231015175236135](.\img\image-20231015175236135.png)

**3）刷新纪录：基于显式分类器引导的扩散模型**

论文" Diffusion Models Beat GANs on Image Synthesis "的发表真正让扩散模型开始在研究领域"爆火"。

**4）引爆网络：基于 CLIP 的多模态图像生成**

CLIP 是连接文本和图像的模型，由于这项技术和扩散模型的结合，才引起基于文字引导的文字生成图像扩散型在图像生成领域的彻底爆发

**5）再次"出图"：大模型的"再学习"方法﹣DreamBooth 、 LoRA 和 ControlNet**

- DreamBooth 可以实现使用现有模型再学习到指定主体图像的功能，只要通过少量训练将主体绑定到唯一的文本标识符后，就可以通过输入文本提示语来控制自己的主体以生成不同的图像
- LoRA 可以实现使用现有模型再学习到自己指定数据集风格或人物的功能，并且还能够将其融入现有的图像生成中
- ontrolNet 可以再学习到更多模态的信息，并利用分割图、边缘图等功能更精细地控制图像的生成

**6）AI作画**：

Midjoryney、DreamStudio、Adobe Firefly，以及百度的文心一格AI创作平台，阿里的通义文生图大模型等。

## 3. 扩散模型的应用

扩散只是一种思想，扩散模型也并非固定的深度网络结构。除此之外，如果将扩散的思想融入其他领域，扩散模型同样可以发挥重要作用。

在实际应用中，扩散模型最常见、最成熟的应用就是完成图像生成任务，本书同样聚焦于此。不过即使如此，扩散模型在其他领域的应用仍不容忽视，可能在不远的将来，它们就会像在图像生成领域一样蓬勃发展，一鸣惊人。

本文将介绍扩散模型在如下领域的应用：

- - 计算机视觉：图像分割与目标检测、图像超分辨率（串联多个扩散模型）、图像修复、图像翻译和图像编辑。
  - 时序数据预测：TimeGrad模型，使用RNN处理历史数据并保存到隐空间，对数据添加噪声实现扩散过程，处理数千维度德多元数据完成预测。
  - 自然语言：使用Diffusion-LM可以应用在语句生成、语言翻译、问答对话、搜索补全、情感分析、文章续写等任务中。
  - 基于文本的多模态：文本生成图像（DALLE-2、Imagen、Stable Diffusion）、文本生成视频（Make-A-Video、ControlNet Video）、文本生成3D（DiffRF）
  - AI基础科学：SMCDiff（支架蛋白质生成）、CDVAE（扩散晶体变分自编码器模型）

## 参考资料

1. [扩散模型之DDPM](https://zhuanlan.zhihu.com/p/563661713)
2. [[贝叶斯统计] 2 隐变量模型，随机变分推断和VAEs](https://zhuanlan.zhihu.com/p/356516670)
3. [超详细的扩散模型（Diffusion Models）原理+代码](https://zhuanlan.zhihu.com/p/624221952)
4. [去噪扩散概率模型（Denoising Diffusion Probabilistic Model，DDPM阅读笔记）](https://zhuanlan.zhihu.com/p/619210083)
5. [扩散模型的工作原理：从零开始的数学](https://zhuanlan.zhihu.com/p/599538060)
6. [Diffusion Models导读](https://zhuanlan.zhihu.com/p/591720296)
7. [扩散模型：DDPM](https://zhuanlan.zhihu.com/p/614498231)
