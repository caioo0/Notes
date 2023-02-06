# Task03 学习BERT和GPT基础
------


## BERT

2018 年 10 月 11 日，谷歌 AI 团队在 arXiv 提交了论文，发布了 BERT 模型。BERT（Bidirectional Encoder Representations from Transformers）的中文意思是：语言理解中深度双向转换模型的预训练模式。BERT 在机器阅读理解顶级水平测试 SQuAD 1.1 中表现出惊人的成绩：

> 在全部的两个衡量指标上全面超越人类，并且还在 11 种不同 NLP 测试中创出最佳成绩，包括将 GLUE 基准推至 80.4％（绝对改进 7.6％），MultiNLI 准确度达到 86.7% （绝对改进率 5.6％）。


``` HTML
GLUE ：General Language Understanding Evaluation
MNLI ：Multi-Genre Natural Language Inference
SQuAD v1.1 ：The Standford Question Answering Dataset
QQP ： Quora Question Pairs 
QNLI ： Question Natural Language Inference
SST-2 ：The Stanford Sentiment Treebank
CoLA ：The Corpus of Linguistic Acceptability 
STS-B ：The Semantic Textual Similarity Benchmark
MRPC ：Microsoft Research Paraphrase Corpus
RTE ：Recognizing Textual Entailment 
WNLI ：Winograd NLI
SWAG ：The Situations With Adversarial Generations

```

毋庸置疑，BERT 模型开启了 NLP 的新时代！


Google AI Language 的论文：[BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding](https://arxiv.org/pdf/1810.04805.pdf)


#### BERT 原理

概括地说 BERT 是一个多层双向 Transformer Encoder 的堆栈。

我们在前面的文章中知道 Transformer 是一种注意力机制，可以学习文本中单词之间的上下文关系。

在 Transformer 中包括两个机制:

- 一个是 Encoder 负责接收文本作为输入，
- 一个是 Decoder 负责预测结果。

而 BERT 的目标是生成语言模型，所以只需要 Transformer 的 Encoder 机制。

在 BERT 这篇论文中提出了两种大小的模型：

- BERT BASE：这个是为了与 OpenAI Transformer 的表现进行比较而构建的，模型的大小也与它相当。包括 12 个 Transformer 编码器层，12 个注意力头，768 个隐藏单元，1.1 亿参数。

- BERT LARGE：一个非常巨大的模型，达到了当时最佳的表现。包括 24 个 Transformer 编码器层，16 个注意力头，1024 个隐藏单元，3.4 亿参数。

#### BERT 最关键两点；

- 第一是特征抽取器采用 Transformer 的 Encoder（GPT 就开始使用了）；
- 第二是预训练的时候采用双向语言模型（ELMO 就是这么做的）。


#### BERT 的训练过程

BERT训练是两阶段过程组成的：

**第一阶段：语言模型预训练**

BERT 采用和 GPT 完全相同的两阶段模型，和 GPT 的最主要不同在于在预训练阶段采用了类似 ELMO 的双向语言模型，当然另外一点是语言模型的数据规模要比 GPT 大。

**第二阶段：NLP 任务训练**

使用 Fine-Tuning 模式解决特定的 NLP 任务。

#### BERT 的创新

我们提过 BERT 本身在开创性创新上，确实没有特别突出的特点，在模型和方法角度上有如下两个创新点：

- Masked 语言模型（本质其实是 CBOW）
- 句子预测 Next Sentence Prediction

(1) Masked 双向语言模型

> Masked 双向语言模型：随机选择语料中 15% 的单词，把它抠掉，也就是用 [Mask] 掩码代替原始单词，然后要求模型去正确预测被抠掉的单词。


(2) 句子预测 Next Sentence Prediction

语言模型预训练的时候，分两种情况选择两个句子：

- 一种是选择语料中真正顺序相连的两个句子；
- 另一种是第二个橘子从语料库随机选择一个，拼接到第一个句子后面。

我们要求模型除了做上述的 Masked 语言模型任务外，附带再做个句子关系预测，判断第二个句子是不是真的是第一个句子的后续句子。

注：个人认为，其实就是一个 GAN。

单词预测粒度的训练到不了句子关系这个层级，增加这个任务有助于下游句子关系判断任务。所以可以看到，它的预训练是个多任务过程。这也是 BERT 的一个创新。


#### 小结

BERT 是 NLP 里里程碑式的工作，对于后面 NLP 的研究和工业应用会产生长久的影响。从模型或者方法角度看，BERT 不是凭空出现的，它借鉴了 ELMO、GPT 及 CBOW，主要提出了 Masked 语言模型及 Next Sentence Prediction。



## GPT模型

> GPT 是“Generative Pre-Training”的简称，由 OpenAI 在 2018 年在论文 improving language understanding by Generative Pre-Training 中发表。

GPT 顾名思义是预训练模型。

GPT 采用两阶段过程：

- 第一个阶段是利用语言模型进行预训练；
- 第二阶段通过 Fine-Tuning 的模式解决下游任务。


**GPT 的缺点**

GPT 相比较 BERT，就是一个缺点——单向语言模型，即通过上文预测下文，而不是通过上文和下文一起来预测和理解。




```python

```
