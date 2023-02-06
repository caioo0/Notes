# 使用Transformer模型解决各类NLP任务进行学习
-----

首先，安装Transformers和Datasets库


```python
!pip install transformers datasets
```

    Collecting transformers
      Downloading transformers-4.9.2-py3-none-any.whl (2.6 MB)
    [K     |████████████████████████████████| 2.6 MB 4.3 MB/s 
    [?25hCollecting datasets
      Downloading datasets-1.11.0-py3-none-any.whl (264 kB)
    [K     |████████████████████████████████| 264 kB 51.6 MB/s 
    [?25hRequirement already satisfied: numpy>=1.17 in /usr/local/lib/python3.7/dist-packages (from transformers) (1.19.5)
    Requirement already satisfied: packaging in /usr/local/lib/python3.7/dist-packages (from transformers) (21.0)
    Collecting tokenizers<0.11,>=0.10.1
      Downloading tokenizers-0.10.3-cp37-cp37m-manylinux_2_5_x86_64.manylinux1_x86_64.manylinux_2_12_x86_64.manylinux2010_x86_64.whl (3.3 MB)
    [K     |████████████████████████████████| 3.3 MB 33.8 MB/s 
    [?25hRequirement already satisfied: requests in /usr/local/lib/python3.7/dist-packages (from transformers) (2.23.0)
    Requirement already satisfied: tqdm>=4.27 in /usr/local/lib/python3.7/dist-packages (from transformers) (4.62.0)
    Collecting huggingface-hub==0.0.12
      Downloading huggingface_hub-0.0.12-py3-none-any.whl (37 kB)
    Collecting sacremoses
      Downloading sacremoses-0.0.45-py3-none-any.whl (895 kB)
    [K     |████████████████████████████████| 895 kB 31.5 MB/s 
    [?25hRequirement already satisfied: importlib-metadata in /usr/local/lib/python3.7/dist-packages (from transformers) (4.6.4)
    Collecting pyyaml>=5.1
      Downloading PyYAML-5.4.1-cp37-cp37m-manylinux1_x86_64.whl (636 kB)
    [K     |████████████████████████████████| 636 kB 35.5 MB/s 
    [?25hRequirement already satisfied: regex!=2019.12.17 in /usr/local/lib/python3.7/dist-packages (from transformers) (2019.12.20)
    Requirement already satisfied: filelock in /usr/local/lib/python3.7/dist-packages (from transformers) (3.0.12)
    Requirement already satisfied: typing-extensions in /usr/local/lib/python3.7/dist-packages (from huggingface-hub==0.0.12->transformers) (3.7.4.3)
    Requirement already satisfied: pyparsing>=2.0.2 in /usr/local/lib/python3.7/dist-packages (from packaging->transformers) (2.4.7)
    Requirement already satisfied: pyarrow!=4.0.0,>=1.0.0 in /usr/local/lib/python3.7/dist-packages (from datasets) (3.0.0)
    Requirement already satisfied: multiprocess in /usr/local/lib/python3.7/dist-packages (from datasets) (0.70.12.2)
    Requirement already satisfied: pandas in /usr/local/lib/python3.7/dist-packages (from datasets) (1.1.5)
    Collecting xxhash
      Downloading xxhash-2.0.2-cp37-cp37m-manylinux2010_x86_64.whl (243 kB)
    [K     |████████████████████████████████| 243 kB 51.7 MB/s 
    [?25hRequirement already satisfied: dill in /usr/local/lib/python3.7/dist-packages (from datasets) (0.3.4)
    Collecting fsspec>=2021.05.0
      Downloading fsspec-2021.7.0-py3-none-any.whl (118 kB)
    [K     |████████████████████████████████| 118 kB 56.9 MB/s 
    [?25hRequirement already satisfied: chardet<4,>=3.0.2 in /usr/local/lib/python3.7/dist-packages (from requests->transformers) (3.0.4)
    Requirement already satisfied: idna<3,>=2.5 in /usr/local/lib/python3.7/dist-packages (from requests->transformers) (2.10)
    Requirement already satisfied: certifi>=2017.4.17 in /usr/local/lib/python3.7/dist-packages (from requests->transformers) (2021.5.30)
    Requirement already satisfied: urllib3!=1.25.0,!=1.25.1,<1.26,>=1.21.1 in /usr/local/lib/python3.7/dist-packages (from requests->transformers) (1.24.3)
    Requirement already satisfied: zipp>=0.5 in /usr/local/lib/python3.7/dist-packages (from importlib-metadata->transformers) (3.5.0)
    Requirement already satisfied: python-dateutil>=2.7.3 in /usr/local/lib/python3.7/dist-packages (from pandas->datasets) (2.8.2)
    Requirement already satisfied: pytz>=2017.2 in /usr/local/lib/python3.7/dist-packages (from pandas->datasets) (2018.9)
    Requirement already satisfied: six>=1.5 in /usr/local/lib/python3.7/dist-packages (from python-dateutil>=2.7.3->pandas->datasets) (1.15.0)
    Requirement already satisfied: click in /usr/local/lib/python3.7/dist-packages (from sacremoses->transformers) (7.1.2)
    Requirement already satisfied: joblib in /usr/local/lib/python3.7/dist-packages (from sacremoses->transformers) (1.0.1)
    Installing collected packages: xxhash, tokenizers, sacremoses, pyyaml, huggingface-hub, fsspec, transformers, datasets
      Attempting uninstall: pyyaml
        Found existing installation: PyYAML 3.13
        Uninstalling PyYAML-3.13:
          Successfully uninstalled PyYAML-3.13
    Successfully installed datasets-1.11.0 fsspec-2021.7.0 huggingface-hub-0.0.12 pyyaml-5.4.1 sacremoses-0.0.45 tokenizers-0.10.3 transformers-4.9.2 xxhash-2.0.2
    


```python
GLUE_TASKS = ["cola", "mnli", "mnli-mm", "mrpc", "qnli", "qqp", "rte", "sst2", "stsb", "wnli"]
```


```python
task = "cola"
model_checkpoint = "distilbert-base-uncased"
batch_size = 16
```

## 加载数据


```python
from datasets import load_dataset, load_metric
```


```python
actual_task = "mnli" if task == "mnli-mm" else task
dataset = load_dataset("glue", actual_task)
metric = load_metric('glue', actual_task)
```


    Downloading:   0%|          | 0.00/7.78k [00:00<?, ?B/s]



    Downloading:   0%|          | 0.00/4.47k [00:00<?, ?B/s]


    Downloading and preparing dataset glue/cola (download: 368.14 KiB, generated: 596.73 KiB, post-processed: Unknown size, total: 964.86 KiB) to /root/.cache/huggingface/datasets/glue/cola/1.0.0/dacbe3125aa31d7f70367a07a8a9e72a5a0bfeb5fc42e75c9db75b96da6053ad...
    


    Downloading:   0%|          | 0.00/377k [00:00<?, ?B/s]



    0 examples [00:00, ? examples/s]



    0 examples [00:00, ? examples/s]



    0 examples [00:00, ? examples/s]


    Dataset glue downloaded and prepared to /root/.cache/huggingface/datasets/glue/cola/1.0.0/dacbe3125aa31d7f70367a07a8a9e72a5a0bfeb5fc42e75c9db75b96da6053ad. Subsequent calls will reuse this data.
    


    Downloading:   0%|          | 0.00/1.86k [00:00<?, ?B/s]


这个datasets对象本身是一种DatasetDict数据结构. 对于训练集、验证集和测试集，只需要使用对应的key（train，validation，test）即可得到相应的数据。


```python
dataset
```




    DatasetDict({
        train: Dataset({
            features: ['sentence', 'label', 'idx'],
            num_rows: 8551
        })
        validation: Dataset({
            features: ['sentence', 'label', 'idx'],
            num_rows: 1043
        })
        test: Dataset({
            features: ['sentence', 'label', 'idx'],
            num_rows: 1063
        })
    })



给定一个数据切分的key（train、validation或者test）和下标即可查看数据。


```python
dataset["train"][1]
```




    {'idx': 1,
     'label': 1,
     'sentence': "One more pseudo generalization and I'm giving up."}




```python
dataset["train"]
```




    Dataset({
        features: ['sentence', 'label', 'idx'],
        num_rows: 8551
    })



为了能够进一步理解数据长什么样子，下面的函数将从数据集里随机选择几个例子进行展示。


```python
import datasets
import random
import pandas as pd
from IPython.display import display, HTML

def show_random_elements(dataset, num_examples=10):
    assert num_examples <= len(dataset), "Can't pick more elements than there are in the dataset."
    picks = []
    for _ in range(num_examples):
        pick = random.randint(0, len(dataset)-1)
        while pick in picks:
            pick = random.randint(0, len(dataset)-1)
        picks.append(pick)
    
    df = pd.DataFrame(dataset[picks])
    for column, typ in dataset.features.items():
        if isinstance(typ, datasets.ClassLabel):
            df[column] = df[column].transform(lambda i: typ.names[i])
    display(HTML(df.to_html()))
```


```python
show_random_elements(dataset["train"])
```


<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>sentence</th>
      <th>label</th>
      <th>idx</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>The video which I thought John told us you recommended was really terrific.</td>
      <td>acceptable</td>
      <td>4871</td>
    </tr>
    <tr>
      <th>1</th>
      <td>The terrier attacked the burglar and savaged the burglar's ankles.</td>
      <td>acceptable</td>
      <td>6668</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Dogs chase cats.</td>
      <td>acceptable</td>
      <td>6627</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Gilgamesh doesn't be in the dungeon</td>
      <td>unacceptable</td>
      <td>7701</td>
    </tr>
    <tr>
      <th>4</th>
      <td>How is someone to chat to a girl if she does not go out?</td>
      <td>acceptable</td>
      <td>6828</td>
    </tr>
    <tr>
      <th>5</th>
      <td>John will see you.</td>
      <td>acceptable</td>
      <td>7414</td>
    </tr>
    <tr>
      <th>6</th>
      <td>The harder it rains, the faster who runs?</td>
      <td>unacceptable</td>
      <td>297</td>
    </tr>
    <tr>
      <th>7</th>
      <td>My eyes are itching my brother.</td>
      <td>unacceptable</td>
      <td>3160</td>
    </tr>
    <tr>
      <th>8</th>
      <td>They investigated.</td>
      <td>unacceptable</td>
      <td>4867</td>
    </tr>
    <tr>
      <th>9</th>
      <td>I went out with a girl who that John showed up pleased.</td>
      <td>unacceptable</td>
      <td>1132</td>
    </tr>
  </tbody>
</table>


评估metic是datasets.Metric的一个实例:


```python
metric
```




    Metric(name: "glue", features: {'predictions': Value(dtype='int64', id=None), 'references': Value(dtype='int64', id=None)}, usage: """
    Compute GLUE evaluation metric associated to each GLUE dataset.
    Args:
        predictions: list of predictions to score.
            Each translation should be tokenized into a list of tokens.
        references: list of lists of references for each translation.
            Each reference should be tokenized into a list of tokens.
    Returns: depending on the GLUE subset, one or several of:
        "accuracy": Accuracy
        "f1": F1 score
        "pearson": Pearson Correlation
        "spearmanr": Spearman Correlation
        "matthews_correlation": Matthew Correlation
    Examples:
    
        >>> glue_metric = datasets.load_metric('glue', 'sst2')  # 'sst2' or any of ["mnli", "mnli_mismatched", "mnli_matched", "qnli", "rte", "wnli", "hans"]
        >>> references = [0, 1]
        >>> predictions = [0, 1]
        >>> results = glue_metric.compute(predictions=predictions, references=references)
        >>> print(results)
        {'accuracy': 1.0}
    
        >>> glue_metric = datasets.load_metric('glue', 'mrpc')  # 'mrpc' or 'qqp'
        >>> references = [0, 1]
        >>> predictions = [0, 1]
        >>> results = glue_metric.compute(predictions=predictions, references=references)
        >>> print(results)
        {'accuracy': 1.0, 'f1': 1.0}
    
        >>> glue_metric = datasets.load_metric('glue', 'stsb')
        >>> references = [0., 1., 2., 3., 4., 5.]
        >>> predictions = [0., 1., 2., 3., 4., 5.]
        >>> results = glue_metric.compute(predictions=predictions, references=references)
        >>> print({"pearson": round(results["pearson"], 2), "spearmanr": round(results["spearmanr"], 2)})
        {'pearson': 1.0, 'spearmanr': 1.0}
    
        >>> glue_metric = datasets.load_metric('glue', 'cola')
        >>> references = [0, 1]
        >>> predictions = [0, 1]
        >>> results = glue_metric.compute(predictions=predictions, references=references)
        >>> print(results)
        {'matthews_correlation': 1.0}
    """, stored examples: 0)



直接调用metric的compute方法，传入labels和predictions即可得到metric的值：


```python
import numpy as np

fake_preds = np.random.randint(0, 2, size=(64,))
fake_labels = np.random.randint(0, 2, size=(64,))
metric.compute(predictions=fake_preds, references=fake_labels)
```




    {'matthews_correlation': -0.08952126702661474}



## 数据预处理

在将数据喂入模型之前，我们需要对数据进行预处理。预处理的工具叫Tokenizer。Tokenizer首先对输入进行tokenize，然后将tokens转化为预模型中需要对应的token ID，再转化为模型需要的输入格式。

为了达到数据预处理的目的，我们使用AutoTokenizer.from_pretrained方法实例化我们的tokenizer，这样可以确保：

我们得到一个与预训练模型一一对应的tokenizer。
使用指定的模型checkpoint对应的tokenizer的时候，我们也下载了模型需要的词表库vocabulary，准确来说是tokens vocabulary。
这个被下载的tokens vocabulary会被缓存起来，从而再次使用的时候不会重新下载。


```python
from transformers import AutoTokenizer
    
tokenizer = AutoTokenizer.from_pretrained(model_checkpoint, use_fast=True)
```


    Downloading:   0%|          | 0.00/28.0 [00:00<?, ?B/s]



    Downloading:   0%|          | 0.00/442 [00:00<?, ?B/s]



    Downloading:   0%|          | 0.00/232k [00:00<?, ?B/s]



    Downloading:   0%|          | 0.00/466k [00:00<?, ?B/s]


注意：use_fast=True要求tokenizer必须是transformers.PreTrainedTokenizerFast类型，因为我们在预处理的时候需要用到fast tokenizer的一些特殊特性（比如多线程快速tokenizer）。如果对应的模型没有fast tokenizer，去掉这个选项即可。

tokenizer既可以对单个文本进行预处理，也可以对一对文本进行预处理，tokenizer预处理后得到的数据满足预训练模型输入格式


```python
tokenizer("Hello, this one sentence!", "And this sentence goes with it.")
```




    {'input_ids': [101, 7592, 1010, 2023, 2028, 6251, 999, 102, 1998, 2023, 6251, 3632, 2007, 2009, 1012, 102], 'attention_mask': [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]}



为了预处理我们的数据，我们需要知道不同数据和对应的数据格式，因此我们定义下面这个dict。


```python
task_to_keys = {
    "cola": ("sentence", None),
    "mnli": ("premise", "hypothesis"),
    "mnli-mm": ("premise", "hypothesis"),
    "mrpc": ("sentence1", "sentence2"),
    "qnli": ("question", "sentence"),
    "qqp": ("question1", "question2"),
    "rte": ("sentence1", "sentence2"),
    "sst2": ("sentence", None),
    "stsb": ("sentence1", "sentence2"),
    "wnli": ("sentence1", "sentence2"),
}
```

对数据格式进行检查:


```python
sentence1_key, sentence2_key = task_to_keys[task]
if sentence2_key is None:
    print(f"Sentence: {dataset['train'][0][sentence1_key]}")
else:
    print(f"Sentence 1: {dataset['train'][0][sentence1_key]}")
    print(f"Sentence 2: {dataset['train'][0][sentence2_key]}")
```

    Sentence: Our friends won't buy this analysis, let alone the next one we propose.
    

随后将预处理的代码放到一个函数中：


```python
def preprocess_function(examples):
    if sentence2_key is None:
        return tokenizer(examples[sentence1_key], truncation=True)
    return tokenizer(examples[sentence1_key], examples[sentence2_key], truncation=True)
```

预处理函数可以处理单个样本，也可以对多个样本进行处理。如果输入是多个样本，那么返回的是一个list：


```python
preprocess_function(dataset['train'][:5])
```




    {'input_ids': [[101, 2256, 2814, 2180, 1005, 1056, 4965, 2023, 4106, 1010, 2292, 2894, 1996, 2279, 2028, 2057, 16599, 1012, 102], [101, 2028, 2062, 18404, 2236, 3989, 1998, 1045, 1005, 1049, 3228, 2039, 1012, 102], [101, 2028, 2062, 18404, 2236, 3989, 2030, 1045, 1005, 1049, 3228, 2039, 1012, 102], [101, 1996, 2062, 2057, 2817, 16025, 1010, 1996, 13675, 16103, 2121, 2027, 2131, 1012, 102], [101, 2154, 2011, 2154, 1996, 8866, 2024, 2893, 14163, 8024, 3771, 1012, 102]], 'attention_mask': [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]}



接下来对数据集datasets里面的所有样本进行预处理，处理的方式是使用map函数，将预处理函数prepare_train_features应用到（map)所有样本上。


```python
encoded_dataset = dataset.map(preprocess_function, batched=True)
```


      0%|          | 0/9 [00:00<?, ?ba/s]



      0%|          | 0/2 [00:00<?, ?ba/s]



      0%|          | 0/2 [00:00<?, ?ba/s]


上面使用到的batched=True这个参数是tokenizer的特点，以为这会使用多线程同时并行对输入进行处理。4

## 微调预训练模型

既然数据已经准备好了，现在我们需要下载并加载我们的预训练模型，然后微调预训练模型。既然我们是做seq2seq任务，那么我们需要一个能解决这个任务的模型类。我们使用AutoModelForSequenceClassification 这个类。和tokenizer相似，from_pretrained方法同样可以帮助我们下载并加载模型，同时也会对模型进行缓存，就不会重复下载模型啦。

需要注意的是：STS-B是一个回归问题，MNLI是一个3分类问题：


```python
from transformers import AutoModelForSequenceClassification, TrainingArguments, Trainer

num_labels = 3 if task.startswith("mnli") else 1 if task=="stsb" else 2
model = AutoModelForSequenceClassification.from_pretrained(model_checkpoint, num_labels=num_labels)
```


    Downloading:   0%|          | 0.00/268M [00:00<?, ?B/s]


    Some weights of the model checkpoint at distilbert-base-uncased were not used when initializing DistilBertForSequenceClassification: ['vocab_projector.bias', 'vocab_layer_norm.bias', 'vocab_transform.weight', 'vocab_transform.bias', 'vocab_layer_norm.weight', 'vocab_projector.weight']
    - This IS expected if you are initializing DistilBertForSequenceClassification from the checkpoint of a model trained on another task or with another architecture (e.g. initializing a BertForSequenceClassification model from a BertForPreTraining model).
    - This IS NOT expected if you are initializing DistilBertForSequenceClassification from the checkpoint of a model that you expect to be exactly identical (initializing a BertForSequenceClassification model from a BertForSequenceClassification model).
    Some weights of DistilBertForSequenceClassification were not initialized from the model checkpoint at distilbert-base-uncased and are newly initialized: ['pre_classifier.weight', 'pre_classifier.bias', 'classifier.weight', 'classifier.bias']
    You should probably TRAIN this model on a down-stream task to be able to use it for predictions and inference.
    

由于我们微调的任务是文本分类任务，而我们加载的是预训练的语言模型，所以会提示我们加载模型的时候扔掉了一些不匹配的神经网络参数（比如：预训练语言模型的神经网络head被扔掉了，同时随机初始化了文本分类的神经网络head）。

为了能够得到一个Trainer训练工具，我们还需要3个要素，其中最重要的是训练的设定/参数 TrainingArguments。这个训练设定包含了能够定义训练过程的所有属性。


```python
metric_name = "pearson" if task == "stsb" else "matthews_correlation" if task == "cola" else "accuracy"

args = TrainingArguments(
    "test-glue",
    evaluation_strategy = "epoch",
    save_strategy = "epoch",
    learning_rate=2e-5,
    per_device_train_batch_size=batch_size,
    per_device_eval_batch_size=batch_size,
    num_train_epochs=5,
    weight_decay=0.01,
    load_best_model_at_end=True,
    metric_for_best_model=metric_name,
)
```

上面evaluation_strategy = "epoch"参数告诉训练代码：我们每个epcoh会做一次验证评估。

上面batch_size在这个notebook之前定义好了。

最后，由于不同的任务需要不同的评测指标，我们定一个函数来根据任务名字得到评价方法:


```python
def compute_metrics(eval_pred):
    predictions, labels = eval_pred
    if task != "stsb":
        predictions = np.argmax(predictions, axis=1)
    else:
        predictions = predictions[:, 0]
    return metric.compute(predictions=predictions, references=labels)
```

全部传给 Trainer:


```python
validation_key = "validation_mismatched" if task == "mnli-mm" else "validation_matched" if task == "mnli" else "validation"
trainer = Trainer(
    model,
    args,
    train_dataset=encoded_dataset["train"],
    eval_dataset=encoded_dataset[validation_key],
    tokenizer=tokenizer,
    compute_metrics=compute_metrics
)
```

开始训练:


```python
trainer.train()
```

    The following columns in the training set  don't have a corresponding argument in `DistilBertForSequenceClassification.forward` and have been ignored: sentence, idx.
    ***** Running training *****
      Num examples = 8551
      Num Epochs = 5
      Instantaneous batch size per device = 16
      Total train batch size (w. parallel, distributed & accumulation) = 16
      Gradient Accumulation steps = 1
      Total optimization steps = 2675
    



    <div>

      <progress value='2675' max='2675' style='width:300px; height:20px; vertical-align: middle;'></progress>
      [2675/2675 05:50, Epoch 5/5]
    </div>
    <table border="1" class="dataframe">
  <thead>
    <tr style="text-align: left;">
      <th>Epoch</th>
      <th>Training Loss</th>
      <th>Validation Loss</th>
      <th>Matthews Correlation</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>1</td>
      <td>0.530500</td>
      <td>0.514990</td>
      <td>0.432712</td>
    </tr>
    <tr>
      <td>2</td>
      <td>0.351000</td>
      <td>0.505386</td>
      <td>0.491490</td>
    </tr>
    <tr>
      <td>3</td>
      <td>0.237000</td>
      <td>0.662538</td>
      <td>0.495476</td>
    </tr>
    <tr>
      <td>4</td>
      <td>0.180800</td>
      <td>0.788094</td>
      <td>0.515403</td>
    </tr>
    <tr>
      <td>5</td>
      <td>0.129100</td>
      <td>0.909952</td>
      <td>0.527495</td>
    </tr>
  </tbody>
</table><p>


    The following columns in the evaluation set  don't have a corresponding argument in `DistilBertForSequenceClassification.forward` and have been ignored: sentence, idx.
    ***** Running Evaluation *****
      Num examples = 1043
      Batch size = 16
    Saving model checkpoint to test-glue/checkpoint-535
    Configuration saved in test-glue/checkpoint-535/config.json
    Model weights saved in test-glue/checkpoint-535/pytorch_model.bin
    tokenizer config file saved in test-glue/checkpoint-535/tokenizer_config.json
    Special tokens file saved in test-glue/checkpoint-535/special_tokens_map.json
    The following columns in the evaluation set  don't have a corresponding argument in `DistilBertForSequenceClassification.forward` and have been ignored: sentence, idx.
    ***** Running Evaluation *****
      Num examples = 1043
      Batch size = 16
    Saving model checkpoint to test-glue/checkpoint-1070
    Configuration saved in test-glue/checkpoint-1070/config.json
    Model weights saved in test-glue/checkpoint-1070/pytorch_model.bin
    tokenizer config file saved in test-glue/checkpoint-1070/tokenizer_config.json
    Special tokens file saved in test-glue/checkpoint-1070/special_tokens_map.json
    The following columns in the evaluation set  don't have a corresponding argument in `DistilBertForSequenceClassification.forward` and have been ignored: sentence, idx.
    ***** Running Evaluation *****
      Num examples = 1043
      Batch size = 16
    Saving model checkpoint to test-glue/checkpoint-1605
    Configuration saved in test-glue/checkpoint-1605/config.json
    Model weights saved in test-glue/checkpoint-1605/pytorch_model.bin
    tokenizer config file saved in test-glue/checkpoint-1605/tokenizer_config.json
    Special tokens file saved in test-glue/checkpoint-1605/special_tokens_map.json
    The following columns in the evaluation set  don't have a corresponding argument in `DistilBertForSequenceClassification.forward` and have been ignored: sentence, idx.
    ***** Running Evaluation *****
      Num examples = 1043
      Batch size = 16
    Saving model checkpoint to test-glue/checkpoint-2140
    Configuration saved in test-glue/checkpoint-2140/config.json
    Model weights saved in test-glue/checkpoint-2140/pytorch_model.bin
    tokenizer config file saved in test-glue/checkpoint-2140/tokenizer_config.json
    Special tokens file saved in test-glue/checkpoint-2140/special_tokens_map.json
    The following columns in the evaluation set  don't have a corresponding argument in `DistilBertForSequenceClassification.forward` and have been ignored: sentence, idx.
    ***** Running Evaluation *****
      Num examples = 1043
      Batch size = 16
    Saving model checkpoint to test-glue/checkpoint-2675
    Configuration saved in test-glue/checkpoint-2675/config.json
    Model weights saved in test-glue/checkpoint-2675/pytorch_model.bin
    tokenizer config file saved in test-glue/checkpoint-2675/tokenizer_config.json
    Special tokens file saved in test-glue/checkpoint-2675/special_tokens_map.json
    
    
    Training completed. Do not forget to share your model on huggingface.co/models =)
    
    
    Loading best model from test-glue/checkpoint-2675 (score: 0.5274949902750498).
    




    TrainOutput(global_step=2675, training_loss=0.2759985401474427, metrics={'train_runtime': 350.8716, 'train_samples_per_second': 121.854, 'train_steps_per_second': 7.624, 'total_flos': 229537542078168.0, 'train_loss': 0.2759985401474427, 'epoch': 5.0})



训练完成后进行评估:


```python
trainer.evaluate()
```

    The following columns in the evaluation set  don't have a corresponding argument in `DistilBertForSequenceClassification.forward` and have been ignored: sentence, idx.
    ***** Running Evaluation *****
      Num examples = 1043
      Batch size = 16
    



<div>

  <progress value='66' max='66' style='width:300px; height:20px; vertical-align: middle;'></progress>
  [66/66 00:01]
</div>






    {'epoch': 5.0,
     'eval_loss': 0.9099518060684204,
     'eval_matthews_correlation': 0.5274949902750498,
     'eval_runtime': 2.0289,
     'eval_samples_per_second': 514.064,
     'eval_steps_per_second': 32.529}



## 超参数搜索

Trainer同样支持超参搜索，使用optuna or Ray Tune代码库。

反注释下面两行安装依赖：


```python
! pip install optuna
! pip install ray[tune]
```

    Collecting optuna
      Downloading optuna-2.9.1-py3-none-any.whl (302 kB)
    [K     |████████████████████████████████| 302 kB 4.1 MB/s 
    [?25hRequirement already satisfied: numpy in /usr/local/lib/python3.7/dist-packages (from optuna) (1.19.5)
    Requirement already satisfied: tqdm in /usr/local/lib/python3.7/dist-packages (from optuna) (4.62.0)
    Collecting cmaes>=0.8.2
      Downloading cmaes-0.8.2-py3-none-any.whl (15 kB)
    Requirement already satisfied: packaging>=20.0 in /usr/local/lib/python3.7/dist-packages (from optuna) (21.0)
    Requirement already satisfied: sqlalchemy>=1.1.0 in /usr/local/lib/python3.7/dist-packages (from optuna) (1.4.22)
    Collecting cliff
      Downloading cliff-3.9.0-py3-none-any.whl (80 kB)
    [K     |████████████████████████████████| 80 kB 8.9 MB/s 
    [?25hCollecting alembic
      Downloading alembic-1.6.5-py2.py3-none-any.whl (164 kB)
    [K     |████████████████████████████████| 164 kB 46.2 MB/s 
    [?25hRequirement already satisfied: PyYAML in /usr/local/lib/python3.7/dist-packages (from optuna) (5.4.1)
    Collecting colorlog
      Downloading colorlog-6.4.1-py2.py3-none-any.whl (11 kB)
    Requirement already satisfied: scipy!=1.4.0 in /usr/local/lib/python3.7/dist-packages (from optuna) (1.4.1)
    Requirement already satisfied: pyparsing>=2.0.2 in /usr/local/lib/python3.7/dist-packages (from packaging>=20.0->optuna) (2.4.7)
    Requirement already satisfied: greenlet!=0.4.17 in /usr/local/lib/python3.7/dist-packages (from sqlalchemy>=1.1.0->optuna) (1.1.1)
    Requirement already satisfied: importlib-metadata in /usr/local/lib/python3.7/dist-packages (from sqlalchemy>=1.1.0->optuna) (4.6.4)
    Requirement already satisfied: python-dateutil in /usr/local/lib/python3.7/dist-packages (from alembic->optuna) (2.8.2)
    Collecting Mako
      Downloading Mako-1.1.5-py2.py3-none-any.whl (75 kB)
    [K     |████████████████████████████████| 75 kB 4.3 MB/s 
    [?25hCollecting python-editor>=0.3
      Downloading python_editor-1.0.4-py3-none-any.whl (4.9 kB)
    Collecting pbr!=2.1.0,>=2.0.0
      Downloading pbr-5.6.0-py2.py3-none-any.whl (111 kB)
    [K     |████████████████████████████████| 111 kB 52.6 MB/s 
    [?25hCollecting cmd2>=1.0.0
      Downloading cmd2-2.1.2-py3-none-any.whl (141 kB)
    [K     |████████████████████████████████| 141 kB 49.8 MB/s 
    [?25hCollecting autopage>=0.4.0
      Downloading autopage-0.4.0-py3-none-any.whl (20 kB)
    Collecting stevedore>=2.0.1
      Downloading stevedore-3.4.0-py3-none-any.whl (49 kB)
    [K     |████████████████████████████████| 49 kB 5.9 MB/s 
    [?25hRequirement already satisfied: PrettyTable>=0.7.2 in /usr/local/lib/python3.7/dist-packages (from cliff->optuna) (2.1.0)
    Requirement already satisfied: wcwidth>=0.1.7 in /usr/local/lib/python3.7/dist-packages (from cmd2>=1.0.0->cliff->optuna) (0.2.5)
    Collecting pyperclip>=1.6
      Downloading pyperclip-1.8.2.tar.gz (20 kB)
    Collecting colorama>=0.3.7
      Downloading colorama-0.4.4-py2.py3-none-any.whl (16 kB)
    Requirement already satisfied: attrs>=16.3.0 in /usr/local/lib/python3.7/dist-packages (from cmd2>=1.0.0->cliff->optuna) (21.2.0)
    Requirement already satisfied: typing-extensions in /usr/local/lib/python3.7/dist-packages (from cmd2>=1.0.0->cliff->optuna) (3.7.4.3)
    Requirement already satisfied: zipp>=0.5 in /usr/local/lib/python3.7/dist-packages (from importlib-metadata->sqlalchemy>=1.1.0->optuna) (3.5.0)
    Requirement already satisfied: MarkupSafe>=0.9.2 in /usr/local/lib/python3.7/dist-packages (from Mako->alembic->optuna) (2.0.1)
    Requirement already satisfied: six>=1.5 in /usr/local/lib/python3.7/dist-packages (from python-dateutil->alembic->optuna) (1.15.0)
    Building wheels for collected packages: pyperclip
      Building wheel for pyperclip (setup.py) ... [?25l[?25hdone
      Created wheel for pyperclip: filename=pyperclip-1.8.2-py3-none-any.whl size=11136 sha256=cba59f219b3848b9a55ccd230be7687ae271686befb114888ca67aca90beb62a
      Stored in directory: /root/.cache/pip/wheels/9f/18/84/8f69f8b08169c7bae2dde6bd7daf0c19fca8c8e500ee620a28
    Successfully built pyperclip
    Installing collected packages: pyperclip, pbr, colorama, stevedore, python-editor, Mako, cmd2, autopage, colorlog, cmaes, cliff, alembic, optuna
    Successfully installed Mako-1.1.5 alembic-1.6.5 autopage-0.4.0 cliff-3.9.0 cmaes-0.8.2 cmd2-2.1.2 colorama-0.4.4 colorlog-6.4.1 optuna-2.9.1 pbr-5.6.0 pyperclip-1.8.2 python-editor-1.0.4 stevedore-3.4.0
    Collecting ray[tune]
      Downloading ray-1.6.0-cp37-cp37m-manylinux2014_x86_64.whl (49.6 MB)
    [K     |████████████████████████████████| 49.6 MB 5.9 kB/s 
    [?25hRequirement already satisfied: msgpack<2.0.0,>=1.0.0 in /usr/local/lib/python3.7/dist-packages (from ray[tune]) (1.0.2)
    Requirement already satisfied: filelock in /usr/local/lib/python3.7/dist-packages (from ray[tune]) (3.0.12)
    Collecting redis>=3.5.0
      Downloading redis-3.5.3-py2.py3-none-any.whl (72 kB)
    [K     |████████████████████████████████| 72 kB 553 kB/s 
    [?25hRequirement already satisfied: click>=7.0 in /usr/local/lib/python3.7/dist-packages (from ray[tune]) (7.1.2)
    Requirement already satisfied: numpy>=1.16 in /usr/local/lib/python3.7/dist-packages (from ray[tune]) (1.19.5)
    Requirement already satisfied: attrs in /usr/local/lib/python3.7/dist-packages (from ray[tune]) (21.2.0)
    Requirement already satisfied: pyyaml in /usr/local/lib/python3.7/dist-packages (from ray[tune]) (5.4.1)
    Requirement already satisfied: grpcio>=1.28.1 in /usr/local/lib/python3.7/dist-packages (from ray[tune]) (1.39.0)
    Requirement already satisfied: protobuf>=3.15.3 in /usr/local/lib/python3.7/dist-packages (from ray[tune]) (3.17.3)
    Requirement already satisfied: pandas in /usr/local/lib/python3.7/dist-packages (from ray[tune]) (1.1.5)
    Requirement already satisfied: tabulate in /usr/local/lib/python3.7/dist-packages (from ray[tune]) (0.8.9)
    Requirement already satisfied: requests in /usr/local/lib/python3.7/dist-packages (from ray[tune]) (2.23.0)
    Collecting tensorboardX>=1.9
      Downloading tensorboardX-2.4-py2.py3-none-any.whl (124 kB)
    [K     |████████████████████████████████| 124 kB 52.7 MB/s 
    [?25hRequirement already satisfied: six>=1.5.2 in /usr/local/lib/python3.7/dist-packages (from grpcio>=1.28.1->ray[tune]) (1.15.0)
    Requirement already satisfied: python-dateutil>=2.7.3 in /usr/local/lib/python3.7/dist-packages (from pandas->ray[tune]) (2.8.2)
    Requirement already satisfied: pytz>=2017.2 in /usr/local/lib/python3.7/dist-packages (from pandas->ray[tune]) (2018.9)
    Requirement already satisfied: chardet<4,>=3.0.2 in /usr/local/lib/python3.7/dist-packages (from requests->ray[tune]) (3.0.4)
    Requirement already satisfied: idna<3,>=2.5 in /usr/local/lib/python3.7/dist-packages (from requests->ray[tune]) (2.10)
    Requirement already satisfied: certifi>=2017.4.17 in /usr/local/lib/python3.7/dist-packages (from requests->ray[tune]) (2021.5.30)
    Requirement already satisfied: urllib3!=1.25.0,!=1.25.1,<1.26,>=1.21.1 in /usr/local/lib/python3.7/dist-packages (from requests->ray[tune]) (1.24.3)
    Installing collected packages: redis, tensorboardX, ray
    Successfully installed ray-1.6.0 redis-3.5.3 tensorboardX-2.4
    

超参搜索时，Trainer将会返回多个训练好的模型，所以需要传入一个定义好的模型从而让Trainer可以不断重新初始化该传入的模型：


```python
def model_init():
    return AutoModelForSequenceClassification.from_pretrained(model_checkpoint, num_labels=num_labels)
```

和之前调用 Trainer类似:


```python
trainer = Trainer(
    model_init=model_init,
    args=args,
    train_dataset=encoded_dataset["train"],
    eval_dataset=encoded_dataset[validation_key],
    tokenizer=tokenizer,
    compute_metrics=compute_metrics
)
```

    loading configuration file https://huggingface.co/distilbert-base-uncased/resolve/main/config.json from cache at /root/.cache/huggingface/transformers/23454919702d26495337f3da04d1655c7ee010d5ec9d77bdb9e399e00302c0a1.d423bdf2f58dc8b77d5f5d18028d7ae4a72dcfd8f468e81fe979ada957a8c361
    Model config DistilBertConfig {
      "activation": "gelu",
      "architectures": [
        "DistilBertForMaskedLM"
      ],
      "attention_dropout": 0.1,
      "dim": 768,
      "dropout": 0.1,
      "hidden_dim": 3072,
      "initializer_range": 0.02,
      "max_position_embeddings": 512,
      "model_type": "distilbert",
      "n_heads": 12,
      "n_layers": 6,
      "pad_token_id": 0,
      "qa_dropout": 0.1,
      "seq_classif_dropout": 0.2,
      "sinusoidal_pos_embds": false,
      "tie_weights_": true,
      "transformers_version": "4.9.2",
      "vocab_size": 30522
    }
    
    loading weights file https://huggingface.co/distilbert-base-uncased/resolve/main/pytorch_model.bin from cache at /root/.cache/huggingface/transformers/9c169103d7e5a73936dd2b627e42851bec0831212b677c637033ee4bce9ab5ee.126183e36667471617ae2f0835fab707baa54b731f991507ebbb55ea85adb12a
    Some weights of the model checkpoint at distilbert-base-uncased were not used when initializing DistilBertForSequenceClassification: ['vocab_projector.bias', 'vocab_layer_norm.bias', 'vocab_transform.weight', 'vocab_transform.bias', 'vocab_layer_norm.weight', 'vocab_projector.weight']
    - This IS expected if you are initializing DistilBertForSequenceClassification from the checkpoint of a model trained on another task or with another architecture (e.g. initializing a BertForSequenceClassification model from a BertForPreTraining model).
    - This IS NOT expected if you are initializing DistilBertForSequenceClassification from the checkpoint of a model that you expect to be exactly identical (initializing a BertForSequenceClassification model from a BertForSequenceClassification model).
    Some weights of DistilBertForSequenceClassification were not initialized from the model checkpoint at distilbert-base-uncased and are newly initialized: ['pre_classifier.weight', 'pre_classifier.bias', 'classifier.weight', 'classifier.bias']
    You should probably TRAIN this model on a down-stream task to be able to use it for predictions and inference.
    

我们可以先用部分数据集进行超参搜索，再进行全量训练。 比如使用1/10的数据进行搜索：


```python
best_run = trainer.hyperparameter_search(n_trials=10, direction="maximize")
```

    [32m[I 2021-08-26 16:38:36,575][0m A new study created in memory with name: no-name-aa863487-b4b4-4025-b86c-705cc1efe422[0m
    Trial:
    loading configuration file https://huggingface.co/distilbert-base-uncased/resolve/main/config.json from cache at /root/.cache/huggingface/transformers/23454919702d26495337f3da04d1655c7ee010d5ec9d77bdb9e399e00302c0a1.d423bdf2f58dc8b77d5f5d18028d7ae4a72dcfd8f468e81fe979ada957a8c361
    Model config DistilBertConfig {
      "activation": "gelu",
      "architectures": [
        "DistilBertForMaskedLM"
      ],
      "attention_dropout": 0.1,
      "dim": 768,
      "dropout": 0.1,
      "hidden_dim": 3072,
      "initializer_range": 0.02,
      "max_position_embeddings": 512,
      "model_type": "distilbert",
      "n_heads": 12,
      "n_layers": 6,
      "pad_token_id": 0,
      "qa_dropout": 0.1,
      "seq_classif_dropout": 0.2,
      "sinusoidal_pos_embds": false,
      "tie_weights_": true,
      "transformers_version": "4.9.2",
      "vocab_size": 30522
    }
    
    loading weights file https://huggingface.co/distilbert-base-uncased/resolve/main/pytorch_model.bin from cache at /root/.cache/huggingface/transformers/9c169103d7e5a73936dd2b627e42851bec0831212b677c637033ee4bce9ab5ee.126183e36667471617ae2f0835fab707baa54b731f991507ebbb55ea85adb12a
    Some weights of the model checkpoint at distilbert-base-uncased were not used when initializing DistilBertForSequenceClassification: ['vocab_projector.bias', 'vocab_layer_norm.bias', 'vocab_transform.weight', 'vocab_transform.bias', 'vocab_layer_norm.weight', 'vocab_projector.weight']
    - This IS expected if you are initializing DistilBertForSequenceClassification from the checkpoint of a model trained on another task or with another architecture (e.g. initializing a BertForSequenceClassification model from a BertForPreTraining model).
    - This IS NOT expected if you are initializing DistilBertForSequenceClassification from the checkpoint of a model that you expect to be exactly identical (initializing a BertForSequenceClassification model from a BertForSequenceClassification model).
    Some weights of DistilBertForSequenceClassification were not initialized from the model checkpoint at distilbert-base-uncased and are newly initialized: ['pre_classifier.weight', 'pre_classifier.bias', 'classifier.weight', 'classifier.bias']
    You should probably TRAIN this model on a down-stream task to be able to use it for predictions and inference.
    The following columns in the training set  don't have a corresponding argument in `DistilBertForSequenceClassification.forward` and have been ignored: sentence, idx.
    ***** Running training *****
      Num examples = 8551
      Num Epochs = 4
      Instantaneous batch size per device = 4
      Total train batch size (w. parallel, distributed & accumulation) = 4
      Gradient Accumulation steps = 1
      Total optimization steps = 8552
    



    <div>

      <progress value='8552' max='8552' style='width:300px; height:20px; vertical-align: middle;'></progress>
      [8552/8552 11:40, Epoch 4/4]
    </div>
    <table border="1" class="dataframe">
  <thead>
    <tr style="text-align: left;">
      <th>Epoch</th>
      <th>Training Loss</th>
      <th>Validation Loss</th>
      <th>Matthews Correlation</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>1</td>
      <td>0.578800</td>
      <td>0.579945</td>
      <td>0.080368</td>
    </tr>
    <tr>
      <td>2</td>
      <td>0.524400</td>
      <td>0.554124</td>
      <td>0.394445</td>
    </tr>
    <tr>
      <td>3</td>
      <td>0.481200</td>
      <td>0.574259</td>
      <td>0.411984</td>
    </tr>
    <tr>
      <td>4</td>
      <td>0.474000</td>
      <td>0.599907</td>
      <td>0.412597</td>
    </tr>
  </tbody>
</table><p>


    The following columns in the evaluation set  don't have a corresponding argument in `DistilBertForSequenceClassification.forward` and have been ignored: sentence, idx.
    ***** Running Evaluation *****
      Num examples = 1043
      Batch size = 16
    Saving model checkpoint to test-glue/run-0/checkpoint-2138
    Configuration saved in test-glue/run-0/checkpoint-2138/config.json
    Model weights saved in test-glue/run-0/checkpoint-2138/pytorch_model.bin
    tokenizer config file saved in test-glue/run-0/checkpoint-2138/tokenizer_config.json
    Special tokens file saved in test-glue/run-0/checkpoint-2138/special_tokens_map.json
    The following columns in the evaluation set  don't have a corresponding argument in `DistilBertForSequenceClassification.forward` and have been ignored: sentence, idx.
    ***** Running Evaluation *****
      Num examples = 1043
      Batch size = 16
    Saving model checkpoint to test-glue/run-0/checkpoint-4276
    Configuration saved in test-glue/run-0/checkpoint-4276/config.json
    Model weights saved in test-glue/run-0/checkpoint-4276/pytorch_model.bin
    tokenizer config file saved in test-glue/run-0/checkpoint-4276/tokenizer_config.json
    Special tokens file saved in test-glue/run-0/checkpoint-4276/special_tokens_map.json
    The following columns in the evaluation set  don't have a corresponding argument in `DistilBertForSequenceClassification.forward` and have been ignored: sentence, idx.
    ***** Running Evaluation *****
      Num examples = 1043
      Batch size = 16
    Saving model checkpoint to test-glue/run-0/checkpoint-6414
    Configuration saved in test-glue/run-0/checkpoint-6414/config.json
    Model weights saved in test-glue/run-0/checkpoint-6414/pytorch_model.bin
    tokenizer config file saved in test-glue/run-0/checkpoint-6414/tokenizer_config.json
    Special tokens file saved in test-glue/run-0/checkpoint-6414/special_tokens_map.json
    The following columns in the evaluation set  don't have a corresponding argument in `DistilBertForSequenceClassification.forward` and have been ignored: sentence, idx.
    ***** Running Evaluation *****
      Num examples = 1043
      Batch size = 16
    Saving model checkpoint to test-glue/run-0/checkpoint-8552
    Configuration saved in test-glue/run-0/checkpoint-8552/config.json
    Model weights saved in test-glue/run-0/checkpoint-8552/pytorch_model.bin
    tokenizer config file saved in test-glue/run-0/checkpoint-8552/tokenizer_config.json
    Special tokens file saved in test-glue/run-0/checkpoint-8552/special_tokens_map.json
    
    
    Training completed. Do not forget to share your model on huggingface.co/models =)
    
    
    Loading best model from test-glue/run-0/checkpoint-8552 (score: 0.4125966670772873).
    [32m[I 2021-08-26 16:50:19,288][0m Trial 0 finished with value: 0.4125966670772873 and parameters: {'learning_rate': 1.281584120271522e-06, 'num_train_epochs': 4, 'seed': 8, 'per_device_train_batch_size': 4}. Best is trial 0 with value: 0.4125966670772873.[0m
    Trial:
    loading configuration file https://huggingface.co/distilbert-base-uncased/resolve/main/config.json from cache at /root/.cache/huggingface/transformers/23454919702d26495337f3da04d1655c7ee010d5ec9d77bdb9e399e00302c0a1.d423bdf2f58dc8b77d5f5d18028d7ae4a72dcfd8f468e81fe979ada957a8c361
    Model config DistilBertConfig {
      "activation": "gelu",
      "architectures": [
        "DistilBertForMaskedLM"
      ],
      "attention_dropout": 0.1,
      "dim": 768,
      "dropout": 0.1,
      "hidden_dim": 3072,
      "initializer_range": 0.02,
      "max_position_embeddings": 512,
      "model_type": "distilbert",
      "n_heads": 12,
      "n_layers": 6,
      "pad_token_id": 0,
      "qa_dropout": 0.1,
      "seq_classif_dropout": 0.2,
      "sinusoidal_pos_embds": false,
      "tie_weights_": true,
      "transformers_version": "4.9.2",
      "vocab_size": 30522
    }
    
    loading weights file https://huggingface.co/distilbert-base-uncased/resolve/main/pytorch_model.bin from cache at /root/.cache/huggingface/transformers/9c169103d7e5a73936dd2b627e42851bec0831212b677c637033ee4bce9ab5ee.126183e36667471617ae2f0835fab707baa54b731f991507ebbb55ea85adb12a
    Some weights of the model checkpoint at distilbert-base-uncased were not used when initializing DistilBertForSequenceClassification: ['vocab_projector.bias', 'vocab_layer_norm.bias', 'vocab_transform.weight', 'vocab_transform.bias', 'vocab_layer_norm.weight', 'vocab_projector.weight']
    - This IS expected if you are initializing DistilBertForSequenceClassification from the checkpoint of a model trained on another task or with another architecture (e.g. initializing a BertForSequenceClassification model from a BertForPreTraining model).
    - This IS NOT expected if you are initializing DistilBertForSequenceClassification from the checkpoint of a model that you expect to be exactly identical (initializing a BertForSequenceClassification model from a BertForSequenceClassification model).
    Some weights of DistilBertForSequenceClassification were not initialized from the model checkpoint at distilbert-base-uncased and are newly initialized: ['pre_classifier.weight', 'pre_classifier.bias', 'classifier.weight', 'classifier.bias']
    You should probably TRAIN this model on a down-stream task to be able to use it for predictions and inference.
    The following columns in the training set  don't have a corresponding argument in `DistilBertForSequenceClassification.forward` and have been ignored: sentence, idx.
    ***** Running training *****
      Num examples = 8551
      Num Epochs = 3
      Instantaneous batch size per device = 64
      Total train batch size (w. parallel, distributed & accumulation) = 64
      Gradient Accumulation steps = 1
      Total optimization steps = 402
    



    <div>

      <progress value='402' max='402' style='width:300px; height:20px; vertical-align: middle;'></progress>
      [402/402 02:14, Epoch 3/3]
    </div>
    <table border="1" class="dataframe">
  <thead>
    <tr style="text-align: left;">
      <th>Epoch</th>
      <th>Training Loss</th>
      <th>Validation Loss</th>
      <th>Matthews Correlation</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>1</td>
      <td>No log</td>
      <td>0.537729</td>
      <td>0.333395</td>
    </tr>
    <tr>
      <td>2</td>
      <td>No log</td>
      <td>0.498041</td>
      <td>0.453913</td>
    </tr>
    <tr>
      <td>3</td>
      <td>No log</td>
      <td>0.504697</td>
      <td>0.459738</td>
    </tr>
  </tbody>
</table><p>


    The following columns in the evaluation set  don't have a corresponding argument in `DistilBertForSequenceClassification.forward` and have been ignored: sentence, idx.
    ***** Running Evaluation *****
      Num examples = 1043
      Batch size = 16
    Saving model checkpoint to test-glue/run-1/checkpoint-134
    Configuration saved in test-glue/run-1/checkpoint-134/config.json
    Model weights saved in test-glue/run-1/checkpoint-134/pytorch_model.bin
    tokenizer config file saved in test-glue/run-1/checkpoint-134/tokenizer_config.json
    Special tokens file saved in test-glue/run-1/checkpoint-134/special_tokens_map.json
    The following columns in the evaluation set  don't have a corresponding argument in `DistilBertForSequenceClassification.forward` and have been ignored: sentence, idx.
    ***** Running Evaluation *****
      Num examples = 1043
      Batch size = 16
    Saving model checkpoint to test-glue/run-1/checkpoint-268
    Configuration saved in test-glue/run-1/checkpoint-268/config.json
    Model weights saved in test-glue/run-1/checkpoint-268/pytorch_model.bin
    tokenizer config file saved in test-glue/run-1/checkpoint-268/tokenizer_config.json
    Special tokens file saved in test-glue/run-1/checkpoint-268/special_tokens_map.json
    The following columns in the evaluation set  don't have a corresponding argument in `DistilBertForSequenceClassification.forward` and have been ignored: sentence, idx.
    ***** Running Evaluation *****
      Num examples = 1043
      Batch size = 16
    Saving model checkpoint to test-glue/run-1/checkpoint-402
    Configuration saved in test-glue/run-1/checkpoint-402/config.json
    Model weights saved in test-glue/run-1/checkpoint-402/pytorch_model.bin
    tokenizer config file saved in test-glue/run-1/checkpoint-402/tokenizer_config.json
    Special tokens file saved in test-glue/run-1/checkpoint-402/special_tokens_map.json
    
    
    Training completed. Do not forget to share your model on huggingface.co/models =)
    
    
    Loading best model from test-glue/run-1/checkpoint-402 (score: 0.4597376022777596).
    [32m[I 2021-08-26 16:52:36,754][0m Trial 1 finished with value: 0.4597376022777596 and parameters: {'learning_rate': 1.1747425604731912e-05, 'num_train_epochs': 3, 'seed': 30, 'per_device_train_batch_size': 64}. Best is trial 1 with value: 0.4597376022777596.[0m
    Trial:
    loading configuration file https://huggingface.co/distilbert-base-uncased/resolve/main/config.json from cache at /root/.cache/huggingface/transformers/23454919702d26495337f3da04d1655c7ee010d5ec9d77bdb9e399e00302c0a1.d423bdf2f58dc8b77d5f5d18028d7ae4a72dcfd8f468e81fe979ada957a8c361
    Model config DistilBertConfig {
      "activation": "gelu",
      "architectures": [
        "DistilBertForMaskedLM"
      ],
      "attention_dropout": 0.1,
      "dim": 768,
      "dropout": 0.1,
      "hidden_dim": 3072,
      "initializer_range": 0.02,
      "max_position_embeddings": 512,
      "model_type": "distilbert",
      "n_heads": 12,
      "n_layers": 6,
      "pad_token_id": 0,
      "qa_dropout": 0.1,
      "seq_classif_dropout": 0.2,
      "sinusoidal_pos_embds": false,
      "tie_weights_": true,
      "transformers_version": "4.9.2",
      "vocab_size": 30522
    }
    
    loading weights file https://huggingface.co/distilbert-base-uncased/resolve/main/pytorch_model.bin from cache at /root/.cache/huggingface/transformers/9c169103d7e5a73936dd2b627e42851bec0831212b677c637033ee4bce9ab5ee.126183e36667471617ae2f0835fab707baa54b731f991507ebbb55ea85adb12a
    Some weights of the model checkpoint at distilbert-base-uncased were not used when initializing DistilBertForSequenceClassification: ['vocab_projector.bias', 'vocab_layer_norm.bias', 'vocab_transform.weight', 'vocab_transform.bias', 'vocab_layer_norm.weight', 'vocab_projector.weight']
    - This IS expected if you are initializing DistilBertForSequenceClassification from the checkpoint of a model trained on another task or with another architecture (e.g. initializing a BertForSequenceClassification model from a BertForPreTraining model).
    - This IS NOT expected if you are initializing DistilBertForSequenceClassification from the checkpoint of a model that you expect to be exactly identical (initializing a BertForSequenceClassification model from a BertForSequenceClassification model).
    Some weights of DistilBertForSequenceClassification were not initialized from the model checkpoint at distilbert-base-uncased and are newly initialized: ['pre_classifier.weight', 'pre_classifier.bias', 'classifier.weight', 'classifier.bias']
    You should probably TRAIN this model on a down-stream task to be able to use it for predictions and inference.
    The following columns in the training set  don't have a corresponding argument in `DistilBertForSequenceClassification.forward` and have been ignored: sentence, idx.
    ***** Running training *****
      Num examples = 8551
      Num Epochs = 5
      Instantaneous batch size per device = 4
      Total train batch size (w. parallel, distributed & accumulation) = 4
      Gradient Accumulation steps = 1
      Total optimization steps = 10690
    



    <div>

      <progress value='10690' max='10690' style='width:300px; height:20px; vertical-align: middle;'></progress>
      [10690/10690 14:11, Epoch 5/5]
    </div>
    <table border="1" class="dataframe">
  <thead>
    <tr style="text-align: left;">
      <th>Epoch</th>
      <th>Training Loss</th>
      <th>Validation Loss</th>
      <th>Matthews Correlation</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>1</td>
      <td>0.529600</td>
      <td>0.521288</td>
      <td>0.436994</td>
    </tr>
    <tr>
      <td>2</td>
      <td>0.482700</td>
      <td>0.937550</td>
      <td>0.421327</td>
    </tr>
    <tr>
      <td>3</td>
      <td>0.351500</td>
      <td>1.042375</td>
      <td>0.481940</td>
    </tr>
    <tr>
      <td>4</td>
      <td>0.301500</td>
      <td>1.020909</td>
      <td>0.504605</td>
    </tr>
    <tr>
      <td>5</td>
      <td>0.195300</td>
      <td>1.104221</td>
      <td>0.515008</td>
    </tr>
  </tbody>
</table><p>


    The following columns in the evaluation set  don't have a corresponding argument in `DistilBertForSequenceClassification.forward` and have been ignored: sentence, idx.
    ***** Running Evaluation *****
      Num examples = 1043
      Batch size = 16
    Saving model checkpoint to test-glue/run-2/checkpoint-2138
    Configuration saved in test-glue/run-2/checkpoint-2138/config.json
    Model weights saved in test-glue/run-2/checkpoint-2138/pytorch_model.bin
    tokenizer config file saved in test-glue/run-2/checkpoint-2138/tokenizer_config.json
    Special tokens file saved in test-glue/run-2/checkpoint-2138/special_tokens_map.json
    The following columns in the evaluation set  don't have a corresponding argument in `DistilBertForSequenceClassification.forward` and have been ignored: sentence, idx.
    ***** Running Evaluation *****
      Num examples = 1043
      Batch size = 16
    Saving model checkpoint to test-glue/run-2/checkpoint-4276
    Configuration saved in test-glue/run-2/checkpoint-4276/config.json
    Model weights saved in test-glue/run-2/checkpoint-4276/pytorch_model.bin
    tokenizer config file saved in test-glue/run-2/checkpoint-4276/tokenizer_config.json
    Special tokens file saved in test-glue/run-2/checkpoint-4276/special_tokens_map.json
    The following columns in the evaluation set  don't have a corresponding argument in `DistilBertForSequenceClassification.forward` and have been ignored: sentence, idx.
    ***** Running Evaluation *****
      Num examples = 1043
      Batch size = 16
    Saving model checkpoint to test-glue/run-2/checkpoint-6414
    Configuration saved in test-glue/run-2/checkpoint-6414/config.json
    Model weights saved in test-glue/run-2/checkpoint-6414/pytorch_model.bin
    tokenizer config file saved in test-glue/run-2/checkpoint-6414/tokenizer_config.json
    Special tokens file saved in test-glue/run-2/checkpoint-6414/special_tokens_map.json
    The following columns in the evaluation set  don't have a corresponding argument in `DistilBertForSequenceClassification.forward` and have been ignored: sentence, idx.
    ***** Running Evaluation *****
      Num examples = 1043
      Batch size = 16
    Saving model checkpoint to test-glue/run-2/checkpoint-8552
    Configuration saved in test-glue/run-2/checkpoint-8552/config.json
    Model weights saved in test-glue/run-2/checkpoint-8552/pytorch_model.bin
    tokenizer config file saved in test-glue/run-2/checkpoint-8552/tokenizer_config.json
    Special tokens file saved in test-glue/run-2/checkpoint-8552/special_tokens_map.json
    The following columns in the evaluation set  don't have a corresponding argument in `DistilBertForSequenceClassification.forward` and have been ignored: sentence, idx.
    ***** Running Evaluation *****
      Num examples = 1043
      Batch size = 16
    Saving model checkpoint to test-glue/run-2/checkpoint-10690
    Configuration saved in test-glue/run-2/checkpoint-10690/config.json
    Model weights saved in test-glue/run-2/checkpoint-10690/pytorch_model.bin
    tokenizer config file saved in test-glue/run-2/checkpoint-10690/tokenizer_config.json
    Special tokens file saved in test-glue/run-2/checkpoint-10690/special_tokens_map.json
    
    
    Training completed. Do not forget to share your model on huggingface.co/models =)
    
    
    Loading best model from test-glue/run-2/checkpoint-10690 (score: 0.5150075229081177).
    [32m[I 2021-08-26 17:06:50,836][0m Trial 2 finished with value: 0.5150075229081177 and parameters: {'learning_rate': 1.1020818235845332e-05, 'num_train_epochs': 5, 'seed': 31, 'per_device_train_batch_size': 4}. Best is trial 2 with value: 0.5150075229081177.[0m
    Trial:
    loading configuration file https://huggingface.co/distilbert-base-uncased/resolve/main/config.json from cache at /root/.cache/huggingface/transformers/23454919702d26495337f3da04d1655c7ee010d5ec9d77bdb9e399e00302c0a1.d423bdf2f58dc8b77d5f5d18028d7ae4a72dcfd8f468e81fe979ada957a8c361
    Model config DistilBertConfig {
      "activation": "gelu",
      "architectures": [
        "DistilBertForMaskedLM"
      ],
      "attention_dropout": 0.1,
      "dim": 768,
      "dropout": 0.1,
      "hidden_dim": 3072,
      "initializer_range": 0.02,
      "max_position_embeddings": 512,
      "model_type": "distilbert",
      "n_heads": 12,
      "n_layers": 6,
      "pad_token_id": 0,
      "qa_dropout": 0.1,
      "seq_classif_dropout": 0.2,
      "sinusoidal_pos_embds": false,
      "tie_weights_": true,
      "transformers_version": "4.9.2",
      "vocab_size": 30522
    }
    
    loading weights file https://huggingface.co/distilbert-base-uncased/resolve/main/pytorch_model.bin from cache at /root/.cache/huggingface/transformers/9c169103d7e5a73936dd2b627e42851bec0831212b677c637033ee4bce9ab5ee.126183e36667471617ae2f0835fab707baa54b731f991507ebbb55ea85adb12a
    Some weights of the model checkpoint at distilbert-base-uncased were not used when initializing DistilBertForSequenceClassification: ['vocab_projector.bias', 'vocab_layer_norm.bias', 'vocab_transform.weight', 'vocab_transform.bias', 'vocab_layer_norm.weight', 'vocab_projector.weight']
    - This IS expected if you are initializing DistilBertForSequenceClassification from the checkpoint of a model trained on another task or with another architecture (e.g. initializing a BertForSequenceClassification model from a BertForPreTraining model).
    - This IS NOT expected if you are initializing DistilBertForSequenceClassification from the checkpoint of a model that you expect to be exactly identical (initializing a BertForSequenceClassification model from a BertForSequenceClassification model).
    Some weights of DistilBertForSequenceClassification were not initialized from the model checkpoint at distilbert-base-uncased and are newly initialized: ['pre_classifier.weight', 'pre_classifier.bias', 'classifier.weight', 'classifier.bias']
    You should probably TRAIN this model on a down-stream task to be able to use it for predictions and inference.
    The following columns in the training set  don't have a corresponding argument in `DistilBertForSequenceClassification.forward` and have been ignored: sentence, idx.
    ***** Running training *****
      Num examples = 8551
      Num Epochs = 3
      Instantaneous batch size per device = 4
      Total train batch size (w. parallel, distributed & accumulation) = 4
      Gradient Accumulation steps = 1
      Total optimization steps = 6414
    



    <div>

      <progress value='6414' max='6414' style='width:300px; height:20px; vertical-align: middle;'></progress>
      [6414/6414 08:33, Epoch 3/3]
    </div>
    <table border="1" class="dataframe">
  <thead>
    <tr style="text-align: left;">
      <th>Epoch</th>
      <th>Training Loss</th>
      <th>Validation Loss</th>
      <th>Matthews Correlation</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>1</td>
      <td>0.595100</td>
      <td>0.555811</td>
      <td>0.427992</td>
    </tr>
    <tr>
      <td>2</td>
      <td>0.488200</td>
      <td>0.796043</td>
      <td>0.499255</td>
    </tr>
    <tr>
      <td>3</td>
      <td>0.253800</td>
      <td>1.007716</td>
      <td>0.522859</td>
    </tr>
  </tbody>
</table><p>


    The following columns in the evaluation set  don't have a corresponding argument in `DistilBertForSequenceClassification.forward` and have been ignored: sentence, idx.
    ***** Running Evaluation *****
      Num examples = 1043
      Batch size = 16
    Saving model checkpoint to test-glue/run-3/checkpoint-2138
    Configuration saved in test-glue/run-3/checkpoint-2138/config.json
    Model weights saved in test-glue/run-3/checkpoint-2138/pytorch_model.bin
    tokenizer config file saved in test-glue/run-3/checkpoint-2138/tokenizer_config.json
    Special tokens file saved in test-glue/run-3/checkpoint-2138/special_tokens_map.json
    The following columns in the evaluation set  don't have a corresponding argument in `DistilBertForSequenceClassification.forward` and have been ignored: sentence, idx.
    ***** Running Evaluation *****
      Num examples = 1043
      Batch size = 16
    Saving model checkpoint to test-glue/run-3/checkpoint-4276
    Configuration saved in test-glue/run-3/checkpoint-4276/config.json
    Model weights saved in test-glue/run-3/checkpoint-4276/pytorch_model.bin
    tokenizer config file saved in test-glue/run-3/checkpoint-4276/tokenizer_config.json
    Special tokens file saved in test-glue/run-3/checkpoint-4276/special_tokens_map.json
    The following columns in the evaluation set  don't have a corresponding argument in `DistilBertForSequenceClassification.forward` and have been ignored: sentence, idx.
    ***** Running Evaluation *****
      Num examples = 1043
      Batch size = 16
    Saving model checkpoint to test-glue/run-3/checkpoint-6414
    Configuration saved in test-glue/run-3/checkpoint-6414/config.json
    Model weights saved in test-glue/run-3/checkpoint-6414/pytorch_model.bin
    tokenizer config file saved in test-glue/run-3/checkpoint-6414/tokenizer_config.json
    Special tokens file saved in test-glue/run-3/checkpoint-6414/special_tokens_map.json
    
    
    Training completed. Do not forget to share your model on huggingface.co/models =)
    
    
    Loading best model from test-glue/run-3/checkpoint-6414 (score: 0.5228587817244016).
    [32m[I 2021-08-26 17:15:26,436][0m Trial 3 finished with value: 0.5228587817244016 and parameters: {'learning_rate': 2.4750516321557143e-05, 'num_train_epochs': 3, 'seed': 32, 'per_device_train_batch_size': 4}. Best is trial 3 with value: 0.5228587817244016.[0m
    Trial:
    loading configuration file https://huggingface.co/distilbert-base-uncased/resolve/main/config.json from cache at /root/.cache/huggingface/transformers/23454919702d26495337f3da04d1655c7ee010d5ec9d77bdb9e399e00302c0a1.d423bdf2f58dc8b77d5f5d18028d7ae4a72dcfd8f468e81fe979ada957a8c361
    Model config DistilBertConfig {
      "activation": "gelu",
      "architectures": [
        "DistilBertForMaskedLM"
      ],
      "attention_dropout": 0.1,
      "dim": 768,
      "dropout": 0.1,
      "hidden_dim": 3072,
      "initializer_range": 0.02,
      "max_position_embeddings": 512,
      "model_type": "distilbert",
      "n_heads": 12,
      "n_layers": 6,
      "pad_token_id": 0,
      "qa_dropout": 0.1,
      "seq_classif_dropout": 0.2,
      "sinusoidal_pos_embds": false,
      "tie_weights_": true,
      "transformers_version": "4.9.2",
      "vocab_size": 30522
    }
    
    loading weights file https://huggingface.co/distilbert-base-uncased/resolve/main/pytorch_model.bin from cache at /root/.cache/huggingface/transformers/9c169103d7e5a73936dd2b627e42851bec0831212b677c637033ee4bce9ab5ee.126183e36667471617ae2f0835fab707baa54b731f991507ebbb55ea85adb12a
    Some weights of the model checkpoint at distilbert-base-uncased were not used when initializing DistilBertForSequenceClassification: ['vocab_projector.bias', 'vocab_layer_norm.bias', 'vocab_transform.weight', 'vocab_transform.bias', 'vocab_layer_norm.weight', 'vocab_projector.weight']
    - This IS expected if you are initializing DistilBertForSequenceClassification from the checkpoint of a model trained on another task or with another architecture (e.g. initializing a BertForSequenceClassification model from a BertForPreTraining model).
    - This IS NOT expected if you are initializing DistilBertForSequenceClassification from the checkpoint of a model that you expect to be exactly identical (initializing a BertForSequenceClassification model from a BertForSequenceClassification model).
    Some weights of DistilBertForSequenceClassification were not initialized from the model checkpoint at distilbert-base-uncased and are newly initialized: ['pre_classifier.weight', 'pre_classifier.bias', 'classifier.weight', 'classifier.bias']
    You should probably TRAIN this model on a down-stream task to be able to use it for predictions and inference.
    The following columns in the training set  don't have a corresponding argument in `DistilBertForSequenceClassification.forward` and have been ignored: sentence, idx.
    ***** Running training *****
      Num examples = 8551
      Num Epochs = 3
      Instantaneous batch size per device = 16
      Total train batch size (w. parallel, distributed & accumulation) = 16
      Gradient Accumulation steps = 1
      Total optimization steps = 1605
    



    <div>

      <progress value='1605' max='1605' style='width:300px; height:20px; vertical-align: middle;'></progress>
      [1605/1605 03:29, Epoch 3/3]
    </div>
    <table border="1" class="dataframe">
  <thead>
    <tr style="text-align: left;">
      <th>Epoch</th>
      <th>Training Loss</th>
      <th>Validation Loss</th>
      <th>Matthews Correlation</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>1</td>
      <td>0.532900</td>
      <td>0.504142</td>
      <td>0.427517</td>
    </tr>
    <tr>
      <td>2</td>
      <td>0.320400</td>
      <td>0.483228</td>
      <td>0.506019</td>
    </tr>
    <tr>
      <td>3</td>
      <td>0.198700</td>
      <td>0.647676</td>
      <td>0.537328</td>
    </tr>
  </tbody>
</table><p>


    The following columns in the evaluation set  don't have a corresponding argument in `DistilBertForSequenceClassification.forward` and have been ignored: sentence, idx.
    ***** Running Evaluation *****
      Num examples = 1043
      Batch size = 16
    Saving model checkpoint to test-glue/run-4/checkpoint-535
    Configuration saved in test-glue/run-4/checkpoint-535/config.json
    Model weights saved in test-glue/run-4/checkpoint-535/pytorch_model.bin
    tokenizer config file saved in test-glue/run-4/checkpoint-535/tokenizer_config.json
    Special tokens file saved in test-glue/run-4/checkpoint-535/special_tokens_map.json
    The following columns in the evaluation set  don't have a corresponding argument in `DistilBertForSequenceClassification.forward` and have been ignored: sentence, idx.
    ***** Running Evaluation *****
      Num examples = 1043
      Batch size = 16
    Saving model checkpoint to test-glue/run-4/checkpoint-1070
    Configuration saved in test-glue/run-4/checkpoint-1070/config.json
    Model weights saved in test-glue/run-4/checkpoint-1070/pytorch_model.bin
    tokenizer config file saved in test-glue/run-4/checkpoint-1070/tokenizer_config.json
    Special tokens file saved in test-glue/run-4/checkpoint-1070/special_tokens_map.json
    The following columns in the evaluation set  don't have a corresponding argument in `DistilBertForSequenceClassification.forward` and have been ignored: sentence, idx.
    ***** Running Evaluation *****
      Num examples = 1043
      Batch size = 16
    Saving model checkpoint to test-glue/run-4/checkpoint-1605
    Configuration saved in test-glue/run-4/checkpoint-1605/config.json
    Model weights saved in test-glue/run-4/checkpoint-1605/pytorch_model.bin
    tokenizer config file saved in test-glue/run-4/checkpoint-1605/tokenizer_config.json
    Special tokens file saved in test-glue/run-4/checkpoint-1605/special_tokens_map.json
    
    
    Training completed. Do not forget to share your model on huggingface.co/models =)
    
    
    Loading best model from test-glue/run-4/checkpoint-1605 (score: 0.5373281885173845).
    [32m[I 2021-08-26 17:18:58,713][0m Trial 4 finished with value: 0.5373281885173845 and parameters: {'learning_rate': 4.183914192191685e-05, 'num_train_epochs': 3, 'seed': 32, 'per_device_train_batch_size': 16}. Best is trial 4 with value: 0.5373281885173845.[0m
    Trial:
    loading configuration file https://huggingface.co/distilbert-base-uncased/resolve/main/config.json from cache at /root/.cache/huggingface/transformers/23454919702d26495337f3da04d1655c7ee010d5ec9d77bdb9e399e00302c0a1.d423bdf2f58dc8b77d5f5d18028d7ae4a72dcfd8f468e81fe979ada957a8c361
    Model config DistilBertConfig {
      "activation": "gelu",
      "architectures": [
        "DistilBertForMaskedLM"
      ],
      "attention_dropout": 0.1,
      "dim": 768,
      "dropout": 0.1,
      "hidden_dim": 3072,
      "initializer_range": 0.02,
      "max_position_embeddings": 512,
      "model_type": "distilbert",
      "n_heads": 12,
      "n_layers": 6,
      "pad_token_id": 0,
      "qa_dropout": 0.1,
      "seq_classif_dropout": 0.2,
      "sinusoidal_pos_embds": false,
      "tie_weights_": true,
      "transformers_version": "4.9.2",
      "vocab_size": 30522
    }
    
    loading weights file https://huggingface.co/distilbert-base-uncased/resolve/main/pytorch_model.bin from cache at /root/.cache/huggingface/transformers/9c169103d7e5a73936dd2b627e42851bec0831212b677c637033ee4bce9ab5ee.126183e36667471617ae2f0835fab707baa54b731f991507ebbb55ea85adb12a
    Some weights of the model checkpoint at distilbert-base-uncased were not used when initializing DistilBertForSequenceClassification: ['vocab_projector.bias', 'vocab_layer_norm.bias', 'vocab_transform.weight', 'vocab_transform.bias', 'vocab_layer_norm.weight', 'vocab_projector.weight']
    - This IS expected if you are initializing DistilBertForSequenceClassification from the checkpoint of a model trained on another task or with another architecture (e.g. initializing a BertForSequenceClassification model from a BertForPreTraining model).
    - This IS NOT expected if you are initializing DistilBertForSequenceClassification from the checkpoint of a model that you expect to be exactly identical (initializing a BertForSequenceClassification model from a BertForSequenceClassification model).
    Some weights of DistilBertForSequenceClassification were not initialized from the model checkpoint at distilbert-base-uncased and are newly initialized: ['pre_classifier.weight', 'pre_classifier.bias', 'classifier.weight', 'classifier.bias']
    You should probably TRAIN this model on a down-stream task to be able to use it for predictions and inference.
    The following columns in the training set  don't have a corresponding argument in `DistilBertForSequenceClassification.forward` and have been ignored: sentence, idx.
    ***** Running training *****
      Num examples = 8551
      Num Epochs = 4
      Instantaneous batch size per device = 64
      Total train batch size (w. parallel, distributed & accumulation) = 64
      Gradient Accumulation steps = 1
      Total optimization steps = 536
    



    <div>

      <progress value='135' max='536' style='width:300px; height:20px; vertical-align: middle;'></progress>
      [135/536 00:39 < 02:00, 3.33 it/s, Epoch 1/4]
    </div>
    <table border="1" class="dataframe">
  <thead>
    <tr style="text-align: left;">
      <th>Epoch</th>
      <th>Training Loss</th>
      <th>Validation Loss</th>
      <th>Matthews Correlation</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>1</td>
      <td>No log</td>
      <td>0.515904</td>
      <td>0.391445</td>
    </tr>
  </tbody>
</table><p>


    The following columns in the evaluation set  don't have a corresponding argument in `DistilBertForSequenceClassification.forward` and have been ignored: sentence, idx.
    ***** Running Evaluation *****
      Num examples = 1043
      Batch size = 16
    [32m[I 2021-08-26 17:19:43,270][0m Trial 5 pruned. [0m
    Trial:
    loading configuration file https://huggingface.co/distilbert-base-uncased/resolve/main/config.json from cache at /root/.cache/huggingface/transformers/23454919702d26495337f3da04d1655c7ee010d5ec9d77bdb9e399e00302c0a1.d423bdf2f58dc8b77d5f5d18028d7ae4a72dcfd8f468e81fe979ada957a8c361
    Model config DistilBertConfig {
      "activation": "gelu",
      "architectures": [
        "DistilBertForMaskedLM"
      ],
      "attention_dropout": 0.1,
      "dim": 768,
      "dropout": 0.1,
      "hidden_dim": 3072,
      "initializer_range": 0.02,
      "max_position_embeddings": 512,
      "model_type": "distilbert",
      "n_heads": 12,
      "n_layers": 6,
      "pad_token_id": 0,
      "qa_dropout": 0.1,
      "seq_classif_dropout": 0.2,
      "sinusoidal_pos_embds": false,
      "tie_weights_": true,
      "transformers_version": "4.9.2",
      "vocab_size": 30522
    }
    
    loading weights file https://huggingface.co/distilbert-base-uncased/resolve/main/pytorch_model.bin from cache at /root/.cache/huggingface/transformers/9c169103d7e5a73936dd2b627e42851bec0831212b677c637033ee4bce9ab5ee.126183e36667471617ae2f0835fab707baa54b731f991507ebbb55ea85adb12a
    Some weights of the model checkpoint at distilbert-base-uncased were not used when initializing DistilBertForSequenceClassification: ['vocab_projector.bias', 'vocab_layer_norm.bias', 'vocab_transform.weight', 'vocab_transform.bias', 'vocab_layer_norm.weight', 'vocab_projector.weight']
    - This IS expected if you are initializing DistilBertForSequenceClassification from the checkpoint of a model trained on another task or with another architecture (e.g. initializing a BertForSequenceClassification model from a BertForPreTraining model).
    - This IS NOT expected if you are initializing DistilBertForSequenceClassification from the checkpoint of a model that you expect to be exactly identical (initializing a BertForSequenceClassification model from a BertForSequenceClassification model).
    Some weights of DistilBertForSequenceClassification were not initialized from the model checkpoint at distilbert-base-uncased and are newly initialized: ['pre_classifier.weight', 'pre_classifier.bias', 'classifier.weight', 'classifier.bias']
    You should probably TRAIN this model on a down-stream task to be able to use it for predictions and inference.
    The following columns in the training set  don't have a corresponding argument in `DistilBertForSequenceClassification.forward` and have been ignored: sentence, idx.
    ***** Running training *****
      Num examples = 8551
      Num Epochs = 3
      Instantaneous batch size per device = 4
      Total train batch size (w. parallel, distributed & accumulation) = 4
      Gradient Accumulation steps = 1
      Total optimization steps = 6414
    



    <div>

      <progress value='6414' max='6414' style='width:300px; height:20px; vertical-align: middle;'></progress>
      [6414/6414 08:33, Epoch 3/3]
    </div>
    <table border="1" class="dataframe">
  <thead>
    <tr style="text-align: left;">
      <th>Epoch</th>
      <th>Training Loss</th>
      <th>Validation Loss</th>
      <th>Matthews Correlation</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>1</td>
      <td>0.562300</td>
      <td>0.546838</td>
      <td>0.464728</td>
    </tr>
    <tr>
      <td>2</td>
      <td>0.450700</td>
      <td>0.767376</td>
      <td>0.505577</td>
    </tr>
    <tr>
      <td>3</td>
      <td>0.333000</td>
      <td>0.904653</td>
      <td>0.531748</td>
    </tr>
  </tbody>
</table><p>


    The following columns in the evaluation set  don't have a corresponding argument in `DistilBertForSequenceClassification.forward` and have been ignored: sentence, idx.
    ***** Running Evaluation *****
      Num examples = 1043
      Batch size = 16
    Saving model checkpoint to test-glue/run-6/checkpoint-2138
    Configuration saved in test-glue/run-6/checkpoint-2138/config.json
    Model weights saved in test-glue/run-6/checkpoint-2138/pytorch_model.bin
    tokenizer config file saved in test-glue/run-6/checkpoint-2138/tokenizer_config.json
    Special tokens file saved in test-glue/run-6/checkpoint-2138/special_tokens_map.json
    The following columns in the evaluation set  don't have a corresponding argument in `DistilBertForSequenceClassification.forward` and have been ignored: sentence, idx.
    ***** Running Evaluation *****
      Num examples = 1043
      Batch size = 16
    Saving model checkpoint to test-glue/run-6/checkpoint-4276
    Configuration saved in test-glue/run-6/checkpoint-4276/config.json
    Model weights saved in test-glue/run-6/checkpoint-4276/pytorch_model.bin
    tokenizer config file saved in test-glue/run-6/checkpoint-4276/tokenizer_config.json
    Special tokens file saved in test-glue/run-6/checkpoint-4276/special_tokens_map.json
    The following columns in the evaluation set  don't have a corresponding argument in `DistilBertForSequenceClassification.forward` and have been ignored: sentence, idx.
    ***** Running Evaluation *****
      Num examples = 1043
      Batch size = 16
    Saving model checkpoint to test-glue/run-6/checkpoint-6414
    Configuration saved in test-glue/run-6/checkpoint-6414/config.json
    Model weights saved in test-glue/run-6/checkpoint-6414/pytorch_model.bin
    tokenizer config file saved in test-glue/run-6/checkpoint-6414/tokenizer_config.json
    Special tokens file saved in test-glue/run-6/checkpoint-6414/special_tokens_map.json
    
    
    Training completed. Do not forget to share your model on huggingface.co/models =)
    
    
    Loading best model from test-glue/run-6/checkpoint-6414 (score: 0.5317477654019562).
    [32m[I 2021-08-26 17:28:19,617][0m Trial 6 finished with value: 0.5317477654019562 and parameters: {'learning_rate': 1.1524647652876275e-05, 'num_train_epochs': 3, 'seed': 20, 'per_device_train_batch_size': 4}. Best is trial 4 with value: 0.5373281885173845.[0m
    Trial:
    loading configuration file https://huggingface.co/distilbert-base-uncased/resolve/main/config.json from cache at /root/.cache/huggingface/transformers/23454919702d26495337f3da04d1655c7ee010d5ec9d77bdb9e399e00302c0a1.d423bdf2f58dc8b77d5f5d18028d7ae4a72dcfd8f468e81fe979ada957a8c361
    Model config DistilBertConfig {
      "activation": "gelu",
      "architectures": [
        "DistilBertForMaskedLM"
      ],
      "attention_dropout": 0.1,
      "dim": 768,
      "dropout": 0.1,
      "hidden_dim": 3072,
      "initializer_range": 0.02,
      "max_position_embeddings": 512,
      "model_type": "distilbert",
      "n_heads": 12,
      "n_layers": 6,
      "pad_token_id": 0,
      "qa_dropout": 0.1,
      "seq_classif_dropout": 0.2,
      "sinusoidal_pos_embds": false,
      "tie_weights_": true,
      "transformers_version": "4.9.2",
      "vocab_size": 30522
    }
    
    loading weights file https://huggingface.co/distilbert-base-uncased/resolve/main/pytorch_model.bin from cache at /root/.cache/huggingface/transformers/9c169103d7e5a73936dd2b627e42851bec0831212b677c637033ee4bce9ab5ee.126183e36667471617ae2f0835fab707baa54b731f991507ebbb55ea85adb12a
    Some weights of the model checkpoint at distilbert-base-uncased were not used when initializing DistilBertForSequenceClassification: ['vocab_projector.bias', 'vocab_layer_norm.bias', 'vocab_transform.weight', 'vocab_transform.bias', 'vocab_layer_norm.weight', 'vocab_projector.weight']
    - This IS expected if you are initializing DistilBertForSequenceClassification from the checkpoint of a model trained on another task or with another architecture (e.g. initializing a BertForSequenceClassification model from a BertForPreTraining model).
    - This IS NOT expected if you are initializing DistilBertForSequenceClassification from the checkpoint of a model that you expect to be exactly identical (initializing a BertForSequenceClassification model from a BertForSequenceClassification model).
    Some weights of DistilBertForSequenceClassification were not initialized from the model checkpoint at distilbert-base-uncased and are newly initialized: ['pre_classifier.weight', 'pre_classifier.bias', 'classifier.weight', 'classifier.bias']
    You should probably TRAIN this model on a down-stream task to be able to use it for predictions and inference.
    The following columns in the training set  don't have a corresponding argument in `DistilBertForSequenceClassification.forward` and have been ignored: sentence, idx.
    ***** Running training *****
      Num examples = 8551
      Num Epochs = 3
      Instantaneous batch size per device = 64
      Total train batch size (w. parallel, distributed & accumulation) = 64
      Gradient Accumulation steps = 1
      Total optimization steps = 402
    



    <div>

      <progress value='135' max='402' style='width:300px; height:20px; vertical-align: middle;'></progress>
      [135/402 00:39 < 01:19, 3.34 it/s, Epoch 1/3]
    </div>
    <table border="1" class="dataframe">
  <thead>
    <tr style="text-align: left;">
      <th>Epoch</th>
      <th>Training Loss</th>
      <th>Validation Loss</th>
      <th>Matthews Correlation</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>1</td>
      <td>No log</td>
      <td>0.556286</td>
      <td>0.000000</td>
    </tr>
  </tbody>
</table><p>


    The following columns in the evaluation set  don't have a corresponding argument in `DistilBertForSequenceClassification.forward` and have been ignored: sentence, idx.
    ***** Running Evaluation *****
      Num examples = 1043
      Batch size = 16
    /usr/local/lib/python3.7/dist-packages/sklearn/metrics/_classification.py:900: RuntimeWarning:
    
    invalid value encountered in double_scalars
    
    [32m[I 2021-08-26 17:29:04,185][0m Trial 7 pruned. [0m
    Trial:
    loading configuration file https://huggingface.co/distilbert-base-uncased/resolve/main/config.json from cache at /root/.cache/huggingface/transformers/23454919702d26495337f3da04d1655c7ee010d5ec9d77bdb9e399e00302c0a1.d423bdf2f58dc8b77d5f5d18028d7ae4a72dcfd8f468e81fe979ada957a8c361
    Model config DistilBertConfig {
      "activation": "gelu",
      "architectures": [
        "DistilBertForMaskedLM"
      ],
      "attention_dropout": 0.1,
      "dim": 768,
      "dropout": 0.1,
      "hidden_dim": 3072,
      "initializer_range": 0.02,
      "max_position_embeddings": 512,
      "model_type": "distilbert",
      "n_heads": 12,
      "n_layers": 6,
      "pad_token_id": 0,
      "qa_dropout": 0.1,
      "seq_classif_dropout": 0.2,
      "sinusoidal_pos_embds": false,
      "tie_weights_": true,
      "transformers_version": "4.9.2",
      "vocab_size": 30522
    }
    
    loading weights file https://huggingface.co/distilbert-base-uncased/resolve/main/pytorch_model.bin from cache at /root/.cache/huggingface/transformers/9c169103d7e5a73936dd2b627e42851bec0831212b677c637033ee4bce9ab5ee.126183e36667471617ae2f0835fab707baa54b731f991507ebbb55ea85adb12a
    Some weights of the model checkpoint at distilbert-base-uncased were not used when initializing DistilBertForSequenceClassification: ['vocab_projector.bias', 'vocab_layer_norm.bias', 'vocab_transform.weight', 'vocab_transform.bias', 'vocab_layer_norm.weight', 'vocab_projector.weight']
    - This IS expected if you are initializing DistilBertForSequenceClassification from the checkpoint of a model trained on another task or with another architecture (e.g. initializing a BertForSequenceClassification model from a BertForPreTraining model).
    - This IS NOT expected if you are initializing DistilBertForSequenceClassification from the checkpoint of a model that you expect to be exactly identical (initializing a BertForSequenceClassification model from a BertForSequenceClassification model).
    Some weights of DistilBertForSequenceClassification were not initialized from the model checkpoint at distilbert-base-uncased and are newly initialized: ['pre_classifier.weight', 'pre_classifier.bias', 'classifier.weight', 'classifier.bias']
    You should probably TRAIN this model on a down-stream task to be able to use it for predictions and inference.
    The following columns in the training set  don't have a corresponding argument in `DistilBertForSequenceClassification.forward` and have been ignored: sentence, idx.
    ***** Running training *****
      Num examples = 8551
      Num Epochs = 5
      Instantaneous batch size per device = 4
      Total train batch size (w. parallel, distributed & accumulation) = 4
      Gradient Accumulation steps = 1
      Total optimization steps = 10690
    



    <div>

      <progress value='2139' max='10690' style='width:300px; height:20px; vertical-align: middle;'></progress>
      [ 2139/10690 02:48 < 11:15, 12.66 it/s, Epoch 1/5]
    </div>
    <table border="1" class="dataframe">
  <thead>
    <tr style="text-align: left;">
      <th>Epoch</th>
      <th>Training Loss</th>
      <th>Validation Loss</th>
      <th>Matthews Correlation</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>1</td>
      <td>0.551400</td>
      <td>0.602044</td>
      <td>0.000000</td>
    </tr>
  </tbody>
</table><p>


    The following columns in the evaluation set  don't have a corresponding argument in `DistilBertForSequenceClassification.forward` and have been ignored: sentence, idx.
    ***** Running Evaluation *****
      Num examples = 1043
      Batch size = 16
    /usr/local/lib/python3.7/dist-packages/sklearn/metrics/_classification.py:900: RuntimeWarning:
    
    invalid value encountered in double_scalars
    
    [32m[I 2021-08-26 17:31:57,366][0m Trial 8 pruned. [0m
    Trial:
    loading configuration file https://huggingface.co/distilbert-base-uncased/resolve/main/config.json from cache at /root/.cache/huggingface/transformers/23454919702d26495337f3da04d1655c7ee010d5ec9d77bdb9e399e00302c0a1.d423bdf2f58dc8b77d5f5d18028d7ae4a72dcfd8f468e81fe979ada957a8c361
    Model config DistilBertConfig {
      "activation": "gelu",
      "architectures": [
        "DistilBertForMaskedLM"
      ],
      "attention_dropout": 0.1,
      "dim": 768,
      "dropout": 0.1,
      "hidden_dim": 3072,
      "initializer_range": 0.02,
      "max_position_embeddings": 512,
      "model_type": "distilbert",
      "n_heads": 12,
      "n_layers": 6,
      "pad_token_id": 0,
      "qa_dropout": 0.1,
      "seq_classif_dropout": 0.2,
      "sinusoidal_pos_embds": false,
      "tie_weights_": true,
      "transformers_version": "4.9.2",
      "vocab_size": 30522
    }
    
    loading weights file https://huggingface.co/distilbert-base-uncased/resolve/main/pytorch_model.bin from cache at /root/.cache/huggingface/transformers/9c169103d7e5a73936dd2b627e42851bec0831212b677c637033ee4bce9ab5ee.126183e36667471617ae2f0835fab707baa54b731f991507ebbb55ea85adb12a
    Some weights of the model checkpoint at distilbert-base-uncased were not used when initializing DistilBertForSequenceClassification: ['vocab_projector.bias', 'vocab_layer_norm.bias', 'vocab_transform.weight', 'vocab_transform.bias', 'vocab_layer_norm.weight', 'vocab_projector.weight']
    - This IS expected if you are initializing DistilBertForSequenceClassification from the checkpoint of a model trained on another task or with another architecture (e.g. initializing a BertForSequenceClassification model from a BertForPreTraining model).
    - This IS NOT expected if you are initializing DistilBertForSequenceClassification from the checkpoint of a model that you expect to be exactly identical (initializing a BertForSequenceClassification model from a BertForSequenceClassification model).
    Some weights of DistilBertForSequenceClassification were not initialized from the model checkpoint at distilbert-base-uncased and are newly initialized: ['pre_classifier.weight', 'pre_classifier.bias', 'classifier.weight', 'classifier.bias']
    You should probably TRAIN this model on a down-stream task to be able to use it for predictions and inference.
    The following columns in the training set  don't have a corresponding argument in `DistilBertForSequenceClassification.forward` and have been ignored: sentence, idx.
    ***** Running training *****
      Num examples = 8551
      Num Epochs = 4
      Instantaneous batch size per device = 8
      Total train batch size (w. parallel, distributed & accumulation) = 8
      Gradient Accumulation steps = 1
      Total optimization steps = 4276
    



    <div>

      <progress value='1070' max='4276' style='width:300px; height:20px; vertical-align: middle;'></progress>
      [1069/4276 01:38 < 04:55, 10.84 it/s, Epoch 1.00/4]
    </div>
    <table border="1" class="dataframe">
  <thead>
    <tr style="text-align: left;">
      <th>Epoch</th>
      <th>Training Loss</th>
      <th>Validation Loss</th>
      <th>Matthews Correlation</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>1</td>
      <td>0.523900</td>
      <td>0.536631</td>
      <td>0.358391</td>
    </tr>
  </tbody>
</table><p>


    The following columns in the evaluation set  don't have a corresponding argument in `DistilBertForSequenceClassification.forward` and have been ignored: sentence, idx.
    ***** Running Evaluation *****
      Num examples = 1043
      Batch size = 16
    [32m[I 2021-08-26 17:33:40,302][0m Trial 9 pruned. [0m
    

hyperparameter_search会返回效果最好的模型相关的参数：


```python
best_run
```




    BestRun(run_id='4', objective=0.5373281885173845, hyperparameters={'learning_rate': 4.183914192191685e-05, 'num_train_epochs': 3, 'seed': 32, 'per_device_train_batch_size': 16})



将Trainner设置为搜索到的最好参数，进行训练：


```python
for n, v in best_run.hyperparameters.items():
    setattr(trainer.args, n, v)

trainer.train()
```

    loading configuration file https://huggingface.co/distilbert-base-uncased/resolve/main/config.json from cache at /root/.cache/huggingface/transformers/23454919702d26495337f3da04d1655c7ee010d5ec9d77bdb9e399e00302c0a1.d423bdf2f58dc8b77d5f5d18028d7ae4a72dcfd8f468e81fe979ada957a8c361
    Model config DistilBertConfig {
      "activation": "gelu",
      "architectures": [
        "DistilBertForMaskedLM"
      ],
      "attention_dropout": 0.1,
      "dim": 768,
      "dropout": 0.1,
      "hidden_dim": 3072,
      "initializer_range": 0.02,
      "max_position_embeddings": 512,
      "model_type": "distilbert",
      "n_heads": 12,
      "n_layers": 6,
      "pad_token_id": 0,
      "qa_dropout": 0.1,
      "seq_classif_dropout": 0.2,
      "sinusoidal_pos_embds": false,
      "tie_weights_": true,
      "transformers_version": "4.9.2",
      "vocab_size": 30522
    }
    
    loading weights file https://huggingface.co/distilbert-base-uncased/resolve/main/pytorch_model.bin from cache at /root/.cache/huggingface/transformers/9c169103d7e5a73936dd2b627e42851bec0831212b677c637033ee4bce9ab5ee.126183e36667471617ae2f0835fab707baa54b731f991507ebbb55ea85adb12a
    Some weights of the model checkpoint at distilbert-base-uncased were not used when initializing DistilBertForSequenceClassification: ['vocab_projector.bias', 'vocab_layer_norm.bias', 'vocab_transform.weight', 'vocab_transform.bias', 'vocab_layer_norm.weight', 'vocab_projector.weight']
    - This IS expected if you are initializing DistilBertForSequenceClassification from the checkpoint of a model trained on another task or with another architecture (e.g. initializing a BertForSequenceClassification model from a BertForPreTraining model).
    - This IS NOT expected if you are initializing DistilBertForSequenceClassification from the checkpoint of a model that you expect to be exactly identical (initializing a BertForSequenceClassification model from a BertForSequenceClassification model).
    Some weights of DistilBertForSequenceClassification were not initialized from the model checkpoint at distilbert-base-uncased and are newly initialized: ['pre_classifier.weight', 'pre_classifier.bias', 'classifier.weight', 'classifier.bias']
    You should probably TRAIN this model on a down-stream task to be able to use it for predictions and inference.
    The following columns in the training set  don't have a corresponding argument in `DistilBertForSequenceClassification.forward` and have been ignored: sentence, idx.
    ***** Running training *****
      Num examples = 8551
      Num Epochs = 3
      Instantaneous batch size per device = 16
      Total train batch size (w. parallel, distributed & accumulation) = 16
      Gradient Accumulation steps = 1
      Total optimization steps = 1605
    



    <div>

      <progress value='1605' max='1605' style='width:300px; height:20px; vertical-align: middle;'></progress>
      [1605/1605 03:29, Epoch 3/3]
    </div>
    <table border="1" class="dataframe">
  <thead>
    <tr style="text-align: left;">
      <th>Epoch</th>
      <th>Training Loss</th>
      <th>Validation Loss</th>
      <th>Matthews Correlation</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>1</td>
      <td>0.532900</td>
      <td>0.504142</td>
      <td>0.427517</td>
    </tr>
    <tr>
      <td>2</td>
      <td>0.320400</td>
      <td>0.483228</td>
      <td>0.506019</td>
    </tr>
    <tr>
      <td>3</td>
      <td>0.198700</td>
      <td>0.647676</td>
      <td>0.537328</td>
    </tr>
  </tbody>
</table><p>


    The following columns in the evaluation set  don't have a corresponding argument in `DistilBertForSequenceClassification.forward` and have been ignored: sentence, idx.
    ***** Running Evaluation *****
      Num examples = 1043
      Batch size = 16
    Saving model checkpoint to test-glue/checkpoint-535
    Configuration saved in test-glue/checkpoint-535/config.json
    Model weights saved in test-glue/checkpoint-535/pytorch_model.bin
    tokenizer config file saved in test-glue/checkpoint-535/tokenizer_config.json
    Special tokens file saved in test-glue/checkpoint-535/special_tokens_map.json
    The following columns in the evaluation set  don't have a corresponding argument in `DistilBertForSequenceClassification.forward` and have been ignored: sentence, idx.
    ***** Running Evaluation *****
      Num examples = 1043
      Batch size = 16
    Saving model checkpoint to test-glue/checkpoint-1070
    Configuration saved in test-glue/checkpoint-1070/config.json
    Model weights saved in test-glue/checkpoint-1070/pytorch_model.bin
    tokenizer config file saved in test-glue/checkpoint-1070/tokenizer_config.json
    Special tokens file saved in test-glue/checkpoint-1070/special_tokens_map.json
    The following columns in the evaluation set  don't have a corresponding argument in `DistilBertForSequenceClassification.forward` and have been ignored: sentence, idx.
    ***** Running Evaluation *****
      Num examples = 1043
      Batch size = 16
    Saving model checkpoint to test-glue/checkpoint-1605
    Configuration saved in test-glue/checkpoint-1605/config.json
    Model weights saved in test-glue/checkpoint-1605/pytorch_model.bin
    tokenizer config file saved in test-glue/checkpoint-1605/tokenizer_config.json
    Special tokens file saved in test-glue/checkpoint-1605/special_tokens_map.json
    
    
    Training completed. Do not forget to share your model on huggingface.co/models =)
    
    
    Loading best model from test-glue/checkpoint-1605 (score: 0.5373281885173845).
    




    TrainOutput(global_step=1605, training_loss=0.33954220590561723, metrics={'train_runtime': 209.5547, 'train_samples_per_second': 122.417, 'train_steps_per_second': 7.659, 'total_flos': 140092812016524.0, 'train_loss': 0.33954220590561723, 'epoch': 3.0})



**后记：** 本文为datawhale学习代码，非本人编写


```python

```



本次打卡跟着章节学习了使用transformer模型解决文本分类任务，主要是4.1的代码学习；

学习内容分为：
 
- 1.加载数据 ： from datasets import load_dataset, load_metric
- 2.数据预处理： 预处理的工具叫Tokenizer的代码实现
- 3.微调预训练模型：使用AutoModelForSequenceClassification，并且对训练完成效果进行评估：trainer.evaluate() 
- 4.超参数搜索：


本次打卡跟着章节学习了使用transformer模型解决文本分类任务，主要是4.1的代码学习；

学习内容分为：
 
- 1.加载数据 ： from datasets import load_dataset, load_metric
- 2.数据预处理： 预处理的工具叫Tokenizer的代码实现
- 3.微调预训练模型：使用AutoModelForSequenceClassification，并且对训练完成效果进行评估：trainer.evaluate() 
- 4.超参数搜索：

