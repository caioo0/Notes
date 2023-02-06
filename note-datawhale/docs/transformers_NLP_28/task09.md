# 微调transformer模型解决翻译任务

本文为datawhale.[learn-nlp-with-transformers](https://github.com/datawhalechina/learn-nlp-with-transformers/blob/main/docs/%E7%AF%87%E7%AB%A04-%E4%BD%BF%E7%94%A8Transformers%E8%A7%A3%E5%86%B3NLP%E4%BB%BB%E5%8A%A1/4.6-%E7%94%9F%E6%88%90%E4%BB%BB%E5%8A%A1-%E6%9C%BA%E5%99%A8%E7%BF%BB%E8%AF%91.md) 学习笔记

在这个notebook中，我们将展示如何使用Transformers代码库中的模型来解决自然语言处理中的翻译任务。我们将会使用WMT dataset数据集。这是翻译任务最常用的数据集之一。

## 安装环境


```python
! pip install datasets transformers sacrebleu==1.5.1 sentencepiece
```

    Requirement already satisfied: datasets in /usr/local/lib/python3.7/dist-packages (1.11.0)
    Requirement already satisfied: transformers in /usr/local/lib/python3.7/dist-packages (4.10.0)
    Requirement already satisfied: sacrebleu==1.5.1 in /usr/local/lib/python3.7/dist-packages (1.5.1)
    Requirement already satisfied: sentencepiece in /usr/local/lib/python3.7/dist-packages (0.1.96)
    Requirement already satisfied: portalocker==2.0.0 in /usr/local/lib/python3.7/dist-packages (from sacrebleu==1.5.1) (2.0.0)
    Requirement already satisfied: tqdm>=4.42 in /usr/local/lib/python3.7/dist-packages (from datasets) (4.62.0)
    Requirement already satisfied: importlib-metadata in /usr/local/lib/python3.7/dist-packages (from datasets) (4.6.4)
    Requirement already satisfied: fsspec>=2021.05.0 in /usr/local/lib/python3.7/dist-packages (from datasets) (2021.8.1)
    Requirement already satisfied: dill in /usr/local/lib/python3.7/dist-packages (from datasets) (0.3.4)
    Requirement already satisfied: pandas in /usr/local/lib/python3.7/dist-packages (from datasets) (1.1.5)
    Requirement already satisfied: xxhash in /usr/local/lib/python3.7/dist-packages (from datasets) (2.0.2)
    Requirement already satisfied: numpy>=1.17 in /usr/local/lib/python3.7/dist-packages (from datasets) (1.19.5)
    Requirement already satisfied: multiprocess in /usr/local/lib/python3.7/dist-packages (from datasets) (0.70.12.2)
    Requirement already satisfied: huggingface-hub<0.1.0 in /usr/local/lib/python3.7/dist-packages (from datasets) (0.0.16)
    Requirement already satisfied: packaging in /usr/local/lib/python3.7/dist-packages (from datasets) (21.0)
    Requirement already satisfied: requests>=2.19.0 in /usr/local/lib/python3.7/dist-packages (from datasets) (2.23.0)
    Requirement already satisfied: pyarrow!=4.0.0,>=1.0.0 in /usr/local/lib/python3.7/dist-packages (from datasets) (3.0.0)
    Requirement already satisfied: typing-extensions in /usr/local/lib/python3.7/dist-packages (from huggingface-hub<0.1.0->datasets) (3.7.4.3)
    Requirement already satisfied: filelock in /usr/local/lib/python3.7/dist-packages (from huggingface-hub<0.1.0->datasets) (3.0.12)
    Requirement already satisfied: pyparsing>=2.0.2 in /usr/local/lib/python3.7/dist-packages (from packaging->datasets) (2.4.7)
    Requirement already satisfied: urllib3!=1.25.0,!=1.25.1,<1.26,>=1.21.1 in /usr/local/lib/python3.7/dist-packages (from requests>=2.19.0->datasets) (1.24.3)
    Requirement already satisfied: idna<3,>=2.5 in /usr/local/lib/python3.7/dist-packages (from requests>=2.19.0->datasets) (2.10)
    Requirement already satisfied: chardet<4,>=3.0.2 in /usr/local/lib/python3.7/dist-packages (from requests>=2.19.0->datasets) (3.0.4)
    Requirement already satisfied: certifi>=2017.4.17 in /usr/local/lib/python3.7/dist-packages (from requests>=2.19.0->datasets) (2021.5.30)
    Requirement already satisfied: pyyaml>=5.1 in /usr/local/lib/python3.7/dist-packages (from transformers) (5.4.1)
    Requirement already satisfied: regex!=2019.12.17 in /usr/local/lib/python3.7/dist-packages (from transformers) (2019.12.20)
    Requirement already satisfied: tokenizers<0.11,>=0.10.1 in /usr/local/lib/python3.7/dist-packages (from transformers) (0.10.3)
    Requirement already satisfied: sacremoses in /usr/local/lib/python3.7/dist-packages (from transformers) (0.0.45)
    Requirement already satisfied: zipp>=0.5 in /usr/local/lib/python3.7/dist-packages (from importlib-metadata->datasets) (3.5.0)
    Requirement already satisfied: pytz>=2017.2 in /usr/local/lib/python3.7/dist-packages (from pandas->datasets) (2018.9)
    Requirement already satisfied: python-dateutil>=2.7.3 in /usr/local/lib/python3.7/dist-packages (from pandas->datasets) (2.8.2)
    Requirement already satisfied: six>=1.5 in /usr/local/lib/python3.7/dist-packages (from python-dateutil>=2.7.3->pandas->datasets) (1.15.0)
    Requirement already satisfied: click in /usr/local/lib/python3.7/dist-packages (from sacremoses->transformers) (7.1.2)
    Requirement already satisfied: joblib in /usr/local/lib/python3.7/dist-packages (from sacremoses->transformers) (1.0.1)
    


```python
model_checkpoint = "Helsinki-NLP/opus-mt-en-ro" 
# 选择一个模型checkpoint

```

## 加载数据


```python
from datasets import load_dataset, load_metric

raw_datasets = load_dataset("wmt16", "ro-en")

metric = load_metric("sacrebleu")

```

    Reusing dataset wmt16 (/root/.cache/huggingface/datasets/wmt16/ro-en/1.0.0/0d9fb3e814712c785176ad8cdb9f465fbe6479000ee6546725db30ad8a8b5f8a)
    

-----
**问题：**AttributeError: module 'sacrebleu' has no attribute 'DEFAULT_TOKENIZER'

**解决：** pip install sacrebleu==1.5.1


```python
raw_datasets

```




    DatasetDict({
        train: Dataset({
            features: ['translation'],
            num_rows: 610320
        })
        validation: Dataset({
            features: ['translation'],
            num_rows: 1999
        })
        test: Dataset({
            features: ['translation'],
            num_rows: 1999
        })
    })




```python
raw_datasets["train"][0]
# 我们可以看到一句英语en对应一句罗马尼亚语言ro

```




    {'translation': {'en': 'Membership of Parliament: see Minutes',
      'ro': 'Componenţa Parlamentului: a se vedea procesul-verbal'}}



随机样例：


```python
import datasets
import random
import pandas as pd
from IPython.display import display, HTML

def show_random_elements(dataset, num_examples=5):
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
show_random_elements(raw_datasets["train"])
```


<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>translation</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>{'en': 'However, this can only be brought to pass if South Africa manages to take real action on its own behalf by setting out a proper disarmament policy, which is thought to be the real foundation on which to base the development project in the country.', 'ro': 'Însă acest lucru nu se poate realiza decât dacă Africa de Sud va adopta, la rândul său, măsuri concrete prin elaborarea unei politici adecvate de dezarmare, considerată a fi fundamentul real pe care se poate construi proiectul de dezvoltare a ţării.'}</td>
    </tr>
    <tr>
      <th>1</th>
      <td>{'en': 'I would like to know how the European Commission intends to approach these negotiations and this draft convention, and on the basis of what mandate it will act on behalf of all of us, so that tomorrow, in the area of domestic work, the European Union can set an example and that we, too, can give expression to the values of the European Union.', 'ro': 'Aș vrea să știu cum intenționează Comisia Europeană să abordeze aceste negocieri și proiectul de convenție aferent și pe baza cărui mandat va acționa în numele nostru, al tuturor, astfel încât, în domeniul muncii casnice, Uniunea Europeană să devină mâine un exemplu demn de a fi urmat și astfel încât noi, la rândul nostru, să putem da viață valorilor Uniunii Europene.'}</td>
    </tr>
    <tr>
      <th>2</th>
      <td>{'en': 'The application relates to 2 840 job losses in the company Dell in the counties of Limerick, Clare and North Tipperary and in the city of Limerick, of which 2 400 were targeted for assistance.', 'ro': 'Cererea se referă la 2 840 de disponibilizări în compania Dell în districtele Limerick, Clare şi North Tipperary şi în oraşul Limerick, dintre care 2 400 au fost vizaţi pentru asistenţă.'}</td>
    </tr>
    <tr>
      <th>3</th>
      <td>{'en': 'Ms Rivasi', 'ro': 'Dna Rivasi'}</td>
    </tr>
    <tr>
      <th>4</th>
      <td>{'en': 'The Poles and the Germans also have a bit of tidying up to do.', 'ro': 'Polonezii şi germanii au şi ei de făcut puţină curăţenie.'}</td>
    </tr>
  </tbody>
</table>



```python
metric
```




    Metric(name: "sacrebleu", features: {'predictions': Value(dtype='string', id='sequence'), 'references': Sequence(feature=Value(dtype='string', id='sequence'), length=-1, id='references')}, usage: """
    Produces BLEU scores along with its sufficient statistics
    from a source against one or more references.
    
    Args:
        predictions: The system stream (a sequence of segments).
        references: A list of one or more reference streams (each a sequence of segments).
        smooth_method: The smoothing method to use. (Default: 'exp').
        smooth_value: The smoothing value. Only valid for 'floor' and 'add-k'. (Defaults: floor: 0.1, add-k: 1).
        tokenize: Tokenization method to use for BLEU. If not provided, defaults to 'zh' for Chinese, 'ja-mecab' for
            Japanese and '13a' (mteval) otherwise.
        lowercase: Lowercase the data. If True, enables case-insensitivity. (Default: False).
        force: Insist that your tokenized input is actually detokenized.
    
    Returns:
        'score': BLEU score,
        'counts': Counts,
        'totals': Totals,
        'precisions': Precisions,
        'bp': Brevity penalty,
        'sys_len': predictions length,
        'ref_len': reference length,
    
    Examples:
    
        >>> predictions = ["hello there general kenobi", "foo bar foobar"]
        >>> references = [["hello there general kenobi", "hello there !"], ["foo bar foobar", "foo bar foobar"]]
        >>> sacrebleu = datasets.load_metric("sacrebleu")
        >>> results = sacrebleu.compute(predictions=predictions, references=references)
        >>> print(list(results.keys()))
        ['score', 'counts', 'totals', 'precisions', 'bp', 'sys_len', 'ref_len']
        >>> print(round(results["score"], 1))
        100.0
    """, stored examples: 0)




```python
fake_preds = ["hello there", "general kenobi"]
fake_labels = [["hello there"], ["general kenobi"]]
metric.compute(predictions=fake_preds, references=fake_labels)
```




    {'bp': 1.0,
     'counts': [4, 2, 0, 0],
     'precisions': [100.0, 100.0, 0.0, 0.0],
     'ref_len': 4,
     'score': 0.0,
     'sys_len': 4,
     'totals': [4, 2, 0, 0]}



## 数据预处理


```python
from transformers import AutoTokenizer
# 需要安装`sentencepiece`： pip install sentencepiece
    
tokenizer = AutoTokenizer.from_pretrained(model_checkpoint)

```


    Downloading:   0%|          | 0.00/42.0 [00:00<?, ?B/s]



    Downloading:   0%|          | 0.00/1.13k [00:00<?, ?B/s]



    Downloading:   0%|          | 0.00/789k [00:00<?, ?B/s]



    Downloading:   0%|          | 0.00/817k [00:00<?, ?B/s]



    Downloading:   0%|          | 0.00/1.39M [00:00<?, ?B/s]



```python
if "mbart" in model_checkpoint:
    tokenizer.src_lang = "en-XX"
    tokenizer.tgt_lang = "ro-RO"

```


```python
tokenizer("Hello, this one sentence!")

```




    {'input_ids': [125, 778, 3, 63, 141, 9191, 23, 0], 'attention_mask': [1, 1, 1, 1, 1, 1, 1, 1]}




```python
tokenizer(["Hello, this one sentence!", "This is another sentence."])

```




    {'input_ids': [[125, 778, 3, 63, 141, 9191, 23, 0], [187, 32, 716, 9191, 2, 0]], 'attention_mask': [[1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1]]}




```python
with tokenizer.as_target_tokenizer():
    print(tokenizer("Hello, this one sentence!"))
    model_input = tokenizer("Hello, this one sentence!")
    tokens = tokenizer.convert_ids_to_tokens(model_input['input_ids'])
    # 打印看一下special toke
    print('tokens: {}'.format(tokens))

```

    {'input_ids': [10334, 1204, 3, 15, 8915, 27, 452, 59, 29579, 581, 23, 0], 'attention_mask': [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]}
    tokens: ['▁Hel', 'lo', ',', '▁', 'this', '▁o', 'ne', '▁se', 'nten', 'ce', '!', '</s>']
    


```python
if model_checkpoint in ["t5-small", "t5-base", "t5-larg", "t5-3b", "t5-11b"]:
    prefix = "translate English to Romanian: "
else:
    prefix = ""
```


```python
max_input_length = 128
max_target_length = 128
source_lang = "en"
target_lang = "ro"

def preprocess_function(examples):
    inputs = [prefix + ex[source_lang] for ex in examples["translation"]]
    targets = [ex[target_lang] for ex in examples["translation"]]
    model_inputs = tokenizer(inputs, max_length=max_input_length, truncation=True)

    # Setup the tokenizer for targets
    with tokenizer.as_target_tokenizer():
        labels = tokenizer(targets, max_length=max_target_length, truncation=True)

    model_inputs["labels"] = labels["input_ids"]
    return model_inputs
```


```python
preprocess_function(raw_datasets['train'][:2])
```




    {'input_ids': [[393, 4462, 14, 1137, 53, 216, 28636, 0], [24385, 14, 28636, 14, 4646, 4622, 53, 216, 28636, 0]], 'attention_mask': [[1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]], 'labels': [[42140, 494, 1750, 53, 8, 59, 903, 3543, 9, 15202, 0], [36199, 6612, 9, 15202, 122, 568, 35788, 21549, 53, 8, 59, 903, 3543, 9, 15202, 0]]}




```python
tokenized_datasets = raw_datasets.map(preprocess_function, batched=True)
```


      0%|          | 0/611 [00:00<?, ?ba/s]



      0%|          | 0/2 [00:00<?, ?ba/s]



      0%|          | 0/2 [00:00<?, ?ba/s]


## 微调transformer模型


```python
from transformers import AutoModelForSeq2SeqLM, DataCollatorForSeq2Seq, Seq2SeqTrainingArguments, Seq2SeqTrainer

model = AutoModelForSeq2SeqLM.from_pretrained(model_checkpoint)

```


    Downloading:   0%|          | 0.00/301M [00:00<?, ?B/s]



```python
batch_size = 3
args = Seq2SeqTrainingArguments(
    "test-translation",
    evaluation_strategy = "epoch",
    learning_rate=2e-5,
    per_device_train_batch_size=batch_size,
    per_device_eval_batch_size=batch_size,
    weight_decay=0.01,
    save_total_limit=3,
    num_train_epochs=1,
    predict_with_generate=True,
    fp16=False,
)

```


```python
data_collator = DataCollatorForSeq2Seq(tokenizer, model=model)

```


```python
import numpy as np

def postprocess_text(preds, labels):
    preds = [pred.strip() for pred in preds]
    labels = [[label.strip()] for label in labels]

    return preds, labels

def compute_metrics(eval_preds):
    preds, labels = eval_preds
    if isinstance(preds, tuple):
        preds = preds[0]
    decoded_preds = tokenizer.batch_decode(preds, skip_special_tokens=True)

    # Replace -100 in the labels as we can't decode them.
    labels = np.where(labels != -100, labels, tokenizer.pad_token_id)
    decoded_labels = tokenizer.batch_decode(labels, skip_special_tokens=True)

    # Some simple post-processing
    decoded_preds, decoded_labels = postprocess_text(decoded_preds, decoded_labels)

    result = metric.compute(predictions=decoded_preds, references=decoded_labels)
    result = {"bleu": result["score"]}

    prediction_lens = [np.count_nonzero(pred != tokenizer.pad_token_id) for pred in preds]
    result["gen_len"] = np.mean(prediction_lens)
    result = {k: round(v, 4) for k, v in result.items()}
    return result

```


```python
trainer = Seq2SeqTrainer(
    model,
    args,
    train_dataset=tokenized_datasets["train"],
    eval_dataset=tokenized_datasets["validation"],
    data_collator=data_collator,
    tokenizer=tokenizer,
    compute_metrics=compute_metrics
)

```


```python
trainer.train()

```

    The following columns in the training set  don't have a corresponding argument in `MarianMTModel.forward` and have been ignored: translation.
    ***** Running training *****
      Num examples = 610320
      Num Epochs = 1
      Instantaneous batch size per device = 3
      Total train batch size (w. parallel, distributed & accumulation) = 3
      Gradient Accumulation steps = 1
      Total optimization steps = 203440
    



    <div>

      <progress value='5786' max='203440' style='width:300px; height:20px; vertical-align: middle;'></progress>
      [  5786/203440 16:32 < 9:25:16, 5.83 it/s, Epoch 0.03/1]
    </div>
    <table border="1" class="dataframe">
  <thead>
    <tr style="text-align: left;">
      <th>Epoch</th>
      <th>Training Loss</th>
      <th>Validation Loss</th>
    </tr>
  </thead>
  <tbody>
  </tbody>
</table><p>


    Saving model checkpoint to test-translation/checkpoint-500
    Configuration saved in test-translation/checkpoint-500/config.json
    Model weights saved in test-translation/checkpoint-500/pytorch_model.bin
    tokenizer config file saved in test-translation/checkpoint-500/tokenizer_config.json
    Special tokens file saved in test-translation/checkpoint-500/special_tokens_map.json
    Saving model checkpoint to test-translation/checkpoint-1000
    Configuration saved in test-translation/checkpoint-1000/config.json
    Model weights saved in test-translation/checkpoint-1000/pytorch_model.bin
    tokenizer config file saved in test-translation/checkpoint-1000/tokenizer_config.json
    Special tokens file saved in test-translation/checkpoint-1000/special_tokens_map.json
    Saving model checkpoint to test-translation/checkpoint-1500
    Configuration saved in test-translation/checkpoint-1500/config.json
    Model weights saved in test-translation/checkpoint-1500/pytorch_model.bin
    tokenizer config file saved in test-translation/checkpoint-1500/tokenizer_config.json
    Special tokens file saved in test-translation/checkpoint-1500/special_tokens_map.json
    Saving model checkpoint to test-translation/checkpoint-2000
    Configuration saved in test-translation/checkpoint-2000/config.json
    Model weights saved in test-translation/checkpoint-2000/pytorch_model.bin
    tokenizer config file saved in test-translation/checkpoint-2000/tokenizer_config.json
    Special tokens file saved in test-translation/checkpoint-2000/special_tokens_map.json
    Deleting older checkpoint [test-translation/checkpoint-500] due to args.save_total_limit
    Saving model checkpoint to test-translation/checkpoint-2500
    Configuration saved in test-translation/checkpoint-2500/config.json
    Model weights saved in test-translation/checkpoint-2500/pytorch_model.bin
    tokenizer config file saved in test-translation/checkpoint-2500/tokenizer_config.json
    Special tokens file saved in test-translation/checkpoint-2500/special_tokens_map.json
    Deleting older checkpoint [test-translation/checkpoint-1000] due to args.save_total_limit
    Saving model checkpoint to test-translation/checkpoint-3000
    Configuration saved in test-translation/checkpoint-3000/config.json
    Model weights saved in test-translation/checkpoint-3000/pytorch_model.bin
    tokenizer config file saved in test-translation/checkpoint-3000/tokenizer_config.json
    Special tokens file saved in test-translation/checkpoint-3000/special_tokens_map.json
    Deleting older checkpoint [test-translation/checkpoint-1500] due to args.save_total_limit
    Saving model checkpoint to test-translation/checkpoint-3500
    Configuration saved in test-translation/checkpoint-3500/config.json
    Model weights saved in test-translation/checkpoint-3500/pytorch_model.bin
    tokenizer config file saved in test-translation/checkpoint-3500/tokenizer_config.json
    Special tokens file saved in test-translation/checkpoint-3500/special_tokens_map.json
    Deleting older checkpoint [test-translation/checkpoint-2000] due to args.save_total_limit
    Saving model checkpoint to test-translation/checkpoint-4000
    Configuration saved in test-translation/checkpoint-4000/config.json
    Model weights saved in test-translation/checkpoint-4000/pytorch_model.bin
    tokenizer config file saved in test-translation/checkpoint-4000/tokenizer_config.json
    Special tokens file saved in test-translation/checkpoint-4000/special_tokens_map.json
    Deleting older checkpoint [test-translation/checkpoint-2500] due to args.save_total_limit
    Saving model checkpoint to test-translation/checkpoint-4500
    Configuration saved in test-translation/checkpoint-4500/config.json
    Model weights saved in test-translation/checkpoint-4500/pytorch_model.bin
    tokenizer config file saved in test-translation/checkpoint-4500/tokenizer_config.json
    Special tokens file saved in test-translation/checkpoint-4500/special_tokens_map.json
    Deleting older checkpoint [test-translation/checkpoint-3000] due to args.save_total_limit
    Saving model checkpoint to test-translation/checkpoint-5000
    Configuration saved in test-translation/checkpoint-5000/config.json
    Model weights saved in test-translation/checkpoint-5000/pytorch_model.bin
    tokenizer config file saved in test-translation/checkpoint-5000/tokenizer_config.json
    Special tokens file saved in test-translation/checkpoint-5000/special_tokens_map.json
    Deleting older checkpoint [test-translation/checkpoint-3500] due to args.save_total_limit
    Saving model checkpoint to test-translation/checkpoint-5500
    Configuration saved in test-translation/checkpoint-5500/config.json
    Model weights saved in test-translation/checkpoint-5500/pytorch_model.bin
    tokenizer config file saved in test-translation/checkpoint-5500/tokenizer_config.json
    Special tokens file saved in test-translation/checkpoint-5500/special_tokens_map.json
    Deleting older checkpoint [test-translation/checkpoint-4000] due to args.save_total_limit
    


```python

```
