```python
!pip install transformers
```

    Collecting transformers
      Downloading transformers-4.9.2-py3-none-any.whl (2.6 MB)
    [K     |████████████████████████████████| 2.6 MB 4.0 MB/s 
    [?25hRequirement already satisfied: requests in /usr/local/lib/python3.7/dist-packages (from transformers) (2.23.0)
    Requirement already satisfied: numpy>=1.17 in /usr/local/lib/python3.7/dist-packages (from transformers) (1.19.5)
    Requirement already satisfied: importlib-metadata in /usr/local/lib/python3.7/dist-packages (from transformers) (4.6.4)
    Requirement already satisfied: filelock in /usr/local/lib/python3.7/dist-packages (from transformers) (3.0.12)
    Collecting huggingface-hub==0.0.12
      Downloading huggingface_hub-0.0.12-py3-none-any.whl (37 kB)
    Collecting tokenizers<0.11,>=0.10.1
      Downloading tokenizers-0.10.3-cp37-cp37m-manylinux_2_5_x86_64.manylinux1_x86_64.manylinux_2_12_x86_64.manylinux2010_x86_64.whl (3.3 MB)
    [K     |████████████████████████████████| 3.3 MB 40.2 MB/s 
    [?25hRequirement already satisfied: tqdm>=4.27 in /usr/local/lib/python3.7/dist-packages (from transformers) (4.62.0)
    Requirement already satisfied: packaging in /usr/local/lib/python3.7/dist-packages (from transformers) (21.0)
    Collecting pyyaml>=5.1
      Downloading PyYAML-5.4.1-cp37-cp37m-manylinux1_x86_64.whl (636 kB)
    [K     |████████████████████████████████| 636 kB 41.1 MB/s 
    [?25hRequirement already satisfied: regex!=2019.12.17 in /usr/local/lib/python3.7/dist-packages (from transformers) (2019.12.20)
    Collecting sacremoses
      Downloading sacremoses-0.0.45-py3-none-any.whl (895 kB)
    [K     |████████████████████████████████| 895 kB 41.3 MB/s 
    [?25hRequirement already satisfied: typing-extensions in /usr/local/lib/python3.7/dist-packages (from huggingface-hub==0.0.12->transformers) (3.7.4.3)
    Requirement already satisfied: pyparsing>=2.0.2 in /usr/local/lib/python3.7/dist-packages (from packaging->transformers) (2.4.7)
    Requirement already satisfied: zipp>=0.5 in /usr/local/lib/python3.7/dist-packages (from importlib-metadata->transformers) (3.5.0)
    Requirement already satisfied: urllib3!=1.25.0,!=1.25.1,<1.26,>=1.21.1 in /usr/local/lib/python3.7/dist-packages (from requests->transformers) (1.24.3)
    Requirement already satisfied: chardet<4,>=3.0.2 in /usr/local/lib/python3.7/dist-packages (from requests->transformers) (3.0.4)
    Requirement already satisfied: certifi>=2017.4.17 in /usr/local/lib/python3.7/dist-packages (from requests->transformers) (2021.5.30)
    Requirement already satisfied: idna<3,>=2.5 in /usr/local/lib/python3.7/dist-packages (from requests->transformers) (2.10)
    Requirement already satisfied: click in /usr/local/lib/python3.7/dist-packages (from sacremoses->transformers) (7.1.2)
    Requirement already satisfied: six in /usr/local/lib/python3.7/dist-packages (from sacremoses->transformers) (1.15.0)
    Requirement already satisfied: joblib in /usr/local/lib/python3.7/dist-packages (from sacremoses->transformers) (1.0.1)
    Installing collected packages: tokenizers, sacremoses, pyyaml, huggingface-hub, transformers
      Attempting uninstall: pyyaml
        Found existing installation: PyYAML 3.13
        Uninstalling PyYAML-3.13:
          Successfully uninstalled PyYAML-3.13
    Successfully installed huggingface-hub-0.0.12 pyyaml-5.4.1 sacremoses-0.0.45 tokenizers-0.10.3 transformers-4.9.2
    


```python

from transformers import BertForTokenClassification, BertTokenizer
import torch

model = BertForTokenClassification.from_pretrained("dbmdz/bert-large-cased-finetuned-conll03-english")
tokenizer = BertTokenizer.from_pretrained("bert-base-cased")

label_list = [
"O",       # Outside of a named entity
"B-MISC",  # Beginning of a miscellaneous entity right after another miscellaneous entity
"I-MISC",  # Miscellaneous entity
"B-PER",   # Beginning of a person's name right after another person's name
"I-PER",   # Person's name
"B-ORG",   # Beginning of an organisation right after another organisation
"I-ORG",   # Organisation
"B-LOC",   # Beginning of a location right after another location
"I-LOC"    # Location
]

sequence = "Hugging Face Inc. is a company based in New York City. Its headquarters are in DUMBO, therefore very close to the Manhattan Bridge."

# Bit of a hack to get the tokens with the special tokens
tokens = tokenizer.tokenize(tokenizer.decode(tokenizer.encode(sequence)))
inputs = tokenizer.encode(sequence, return_tensors="pt")

outputs = model(inputs).logits
predictions = torch.argmax(outputs, dim=2)
```


    Downloading:   0%|          | 0.00/998 [00:00<?, ?B/s]



    Downloading:   0%|          | 0.00/1.33G [00:00<?, ?B/s]



    Downloading:   0%|          | 0.00/213k [00:00<?, ?B/s]



    Downloading:   0%|          | 0.00/29.0 [00:00<?, ?B/s]



    Downloading:   0%|          | 0.00/436k [00:00<?, ?B/s]



    Downloading:   0%|          | 0.00/570 [00:00<?, ?B/s]



```python
for token, prediction in zip(tokens, predictions[0].numpy()):
    print((token, model.config.id2label[prediction]))
```

    ('[CLS]', 'O')
    ('Hu', 'I-ORG')
    ('##gging', 'I-ORG')
    ('Face', 'I-ORG')
    ('Inc', 'I-ORG')
    ('.', 'O')
    ('is', 'O')
    ('a', 'O')
    ('company', 'O')
    ('based', 'O')
    ('in', 'O')
    ('New', 'I-LOC')
    ('York', 'I-LOC')
    ('City', 'I-LOC')
    ('.', 'O')
    ('Its', 'O')
    ('headquarters', 'O')
    ('are', 'O')
    ('in', 'O')
    ('D', 'I-LOC')
    ('##UM', 'I-LOC')
    ('##BO', 'I-LOC')
    (',', 'O')
    ('therefore', 'O')
    ('very', 'O')
    ('close', 'O')
    ('to', 'O')
    ('the', 'O')
    ('Manhattan', 'I-LOC')
    ('Bridge', 'I-LOC')
    ('.', 'O')
    ('[SEP]', 'O')
    


```python
from transformers import AutoTokenizer, AutoModelForQuestionAnswering
import torch

tokenizer = AutoTokenizer.from_pretrained("bert-large-uncased-whole-word-masking-finetuned-squad")
model = AutoModelForQuestionAnswering.from_pretrained("bert-large-uncased-whole-word-masking-finetuned-squad")

text = "🤗 Transformers (formerly known as pytorch-transformers and pytorch-pretrained-bert) provides general-purpose architectures (BERT, GPT-2, RoBERTa, XLM, DistilBert, XLNet…) for Natural Language Understanding (NLU) and Natural Language Generation (NLG) with over 32+ pretrained models in 100+ languages and deep interoperability between TensorFlow 2.0 and PyTorch."

questions = [
"How many pretrained models are available in 🤗 Transformers?",
"What does 🤗 Transformers provide?",
"🤗 Transformers provides interoperability between which frameworks?",
]

for question in questions:
    inputs = tokenizer(question, text, add_special_tokens=True, return_tensors="pt")
    input_ids = inputs["input_ids"].tolist()[0]
    outputs = model(**inputs)
    answer_start_scores = outputs.start_logits
    answer_end_scores = outputs.end_logits
    answer_start = torch.argmax(
        answer_start_scores
    )  # Get the most likely beginning of answer with the argmax of the score
    answer_end = torch.argmax(answer_end_scores) + 1  # Get the most likely end of answer with the argmax of the score
    answer = tokenizer.convert_tokens_to_string(tokenizer.convert_ids_to_tokens(input_ids[answer_start:answer_end]))
    print(f"Question: {question}")
    print(f"Answer: {answer}")
```


    Downloading:   0%|          | 0.00/1.34G [00:00<?, ?B/s]


    Question: How many pretrained models are available in 🤗 Transformers?
    Answer: over 32 +
    Question: What does 🤗 Transformers provide?
    Answer: general - purpose architectures
    Question: 🤗 Transformers provides interoperability between which frameworks?
    Answer: tensorflow 2. 0 and pytorch
    
