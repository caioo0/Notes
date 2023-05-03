# Task02 学习Attention和Transformer

## seq2seq模型

> seq2seq 被提出于2014年，最早由两篇文章独立地阐述了它主要思想，分别是
Google Brain团队:[《Sequence to Sequence Learning with Neural Networks》](https://papers.nips.cc/paper/5346-sequence-to-sequence-learning-with-neural-networks.pdf) 和 
Yoshua Bengio团队:[《Learning Phrase Representation using RNN Encoder-Decoder for Statistical Machine Translation》](http://emnlp2014.org/papers/pdf/EMNLP2014179.pdf)



####  模型定义：

seq2seq 是一种常见的NLP模型结构，全称是 Sequence-to-sequence 模型，翻译为"序列到序列"，顾名思义Seq2seq模型的输入是序列化数据（比如单词、信件内容、图片特征等），输出也是序列化数据。

它由两个循环神经网络（可以是 RNN、LSTM、GRU 等）组成：

- Encoder 编码器，Encoder 用于编码序列的信息，将任意长度的序列信息编码到一个固定“上下文向量”c 里。

- Decoder 解码器，得到固定“上下文向量” c 之后可以将信息解码，并输出为序列，输出为目标序列。

  

####  原理解析：



#### 优点和缺点：

**优点**

1. 输入序列和输出序列的长度可以不固定.
2. Encoder 处理完整个输入句子后，Decoder 再进行预测.

**缺点** 

1. 如果输入数据很长时，就会有很多信息无法被压缩进固定长度的“上下文向量”中(通常为 128 或者 256)。

2. “上下文向量”在 Decoder 中只是在最开始的时候传递一次，之后都要靠 Decoder 自己的 循环神经网络 单元的记忆能力去传递信息，这样当遇到长句子时，记忆能力也是有限的。

3. 运算量太大了，训练起来比较困难。

#### 用 Keras 实现 seq2seq

```python
from random import seed
from random import randint
from numpy import array
from math import ceil
from math import log10
from math import sqrt
from numpy import argmax
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from keras.layers import TimeDistributed
from keras.layers import RepeatVector


n_samples = 1000
n_numbers = 2
largest = 10

# random_sum_pairs 就是用来随机生成 1000 组数据，每一组的 X 是 2 个在 1~10 之间的数字，每一组的 y 是 X 中所有数字的求和。
## 例如 X[0]=[7, 7]，y[0]=14。

def random_sum_pairs(n_examples, n_numbers, largest):
    X, y = list(), list()
    for i in range(n_examples):
        in_pattern = [randint(1,largest) for _ in range(n_numbers)]
        out_pattern = sum(in_pattern)
        X.append(in_pattern)
        y.append(out_pattern)
    return X, y

def to_string(X, y, n_numbers, largest):
    max_length = n_numbers * ceil(log10(largest+1)) + n_numbers - 1
    Xstr = list()
    for pattern in X:
        strp = '+'.join([str(n) for n in pattern])
        strp = ''.join([' ' for _ in range(max_length-len(strp))]) + strp
        Xstr.append(strp)
    max_length = ceil(log10(n_numbers * (largest+1)))
    ystr = list()
    for pattern in y:
        strp = str(pattern)
        strp = ''.join([' ' for _ in range(max_length-len(strp))]) + strp
        ystr.append(strp)
    return Xstr, ystr


alphabet = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '+', ' ']


    
```


```python
def integer_encode(X, y, alphabet):
    char_to_int = dict((c, i) for i, c in enumerate(alphabet))
    Xenc = list()
    for pattern in X:
        integer_encoded = [char_to_int[char] for char in pattern]
        Xenc.append(integer_encoded)
    yenc = list()
    for pattern in y:
        integer_encoded = [char_to_int[char] for char in pattern]
        yenc.append(integer_encoded)
    return Xenc, yenc
```


```python
def one_hot_encode(X, y, max_int):
    Xenc = list()
    for seq in X:
        pattern = list()
        for index in seq:
            vector = [0 for _ in range(max_int)]
            vector[index] = 1
            pattern.append(vector)
        Xenc.append(pattern)
    yenc = list()
    for seq in y:
        pattern = list()
        for index in seq:
            vector = [0 for _ in range(max_int)]
            vector[index] = 1
            pattern.append(vector)
        yenc.append(pattern)
    return Xenc, yenc
```


```python
def generate_data(n_samples, n_numbers, largest, alphabet):
    X, y = random_sum_pairs(n_samples, n_numbers, largest)
    X, y = to_string(X, y, n_numbers, largest)
    X, y = integer_encode(X, y, alphabet)
    X, y = one_hot_encode(X, y, len(alphabet))
    X, y = array(X), array(y)
    return X, y
```


```python
def invert(seq, alphabet):
    int_to_char = dict((i, c) for i, c in enumerate(alphabet))
    strings = list()
    for pattern in seq:
        string = int_to_char[argmax(pattern)]
        strings.append(string)
    return ''.join(strings)
```


```python
seed(1)
n_samples = 1000        # 生成几组数据
n_numbers = 2            # 每组是几个数字相加
largest = 10            # 每个数字随机生成的上界
alphabet = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '+', ' ']            # 用于将数字映射成数字时
n_chars = len(alphabet)                                                            # 每个字符的向量表示的长度
n_in_seq_length = n_numbers * ceil(log10(largest+1)) + n_numbers - 1            # X 的最大长度
n_out_seq_length = ceil(log10(n_numbers * (largest+1)))                            # y 的最大长度
n_batch = 10
n_epoch = 30
```


```python
model = Sequential()
model.add(LSTM(100, input_shape=(n_in_seq_length, n_chars)))
model.add(RepeatVector(n_out_seq_length))
model.add(LSTM(50, return_sequences=True))
model.add(TimeDistributed(Dense(n_chars, activation='softmax')))
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
print(model.summary())

    
```

    Model: "sequential"
    _________________________________________________________________
    Layer (type)                 Output Shape              Param #   
    =================================================================
    lstm (LSTM)                  (None, 100)               45200     
    _________________________________________________________________
    repeat_vector (RepeatVector) (None, 2, 100)            0         
    _________________________________________________________________
    lstm_1 (LSTM)                (None, 2, 50)             30200     
    _________________________________________________________________
    time_distributed (TimeDistri (None, 2, 12)             612       
    =================================================================
    Total params: 76,012
    Trainable params: 76,012
    Non-trainable params: 0
    _________________________________________________________________
    None



```python
for i in range(n_epoch):
    X, y = generate_data(n_samples, n_numbers, largest, alphabet)
    print(i)
    model.fit(X, y, epochs=1, batch_size=n_batch)
```

    0
    100/100 [==============================] - 3s 5ms/step - loss: 1.9888 - accuracy: 0.3605
    1
    100/100 [==============================] - 0s 4ms/step - loss: 1.5387 - accuracy: 0.3585
    2
    100/100 [==============================] - 0s 5ms/step - loss: 1.4579 - accuracy: 0.4140
    3
    100/100 [==============================] - 0s 4ms/step - loss: 1.3328 - accuracy: 0.5015
    4
    100/100 [==============================] - 0s 4ms/step - loss: 1.2434 - accuracy: 0.5315
    5
    100/100 [==============================] - 0s 5ms/step - loss: 1.1305 - accuracy: 0.5885
    6
    100/100 [==============================] - 0s 5ms/step - loss: 1.0045 - accuracy: 0.6600
    7
    100/100 [==============================] - 0s 4ms/step - loss: 0.8755 - accuracy: 0.7145
    8
    100/100 [==============================] - 0s 5ms/step - loss: 0.7514 - accuracy: 0.7620
    9
    100/100 [==============================] - 0s 5ms/step - loss: 0.6657 - accuracy: 0.8090
    10
    100/100 [==============================] - 0s 5ms/step - loss: 0.5714 - accuracy: 0.8490
    11
    100/100 [==============================] - 0s 5ms/step - loss: 0.4743 - accuracy: 0.9125
    12
    100/100 [==============================] - 0s 5ms/step - loss: 0.4063 - accuracy: 0.9295
    13
    100/100 [==============================] - 0s 5ms/step - loss: 0.3558 - accuracy: 0.9515: 0s - loss: 0.3767 - 
    14
    100/100 [==============================] - 0s 5ms/step - loss: 0.3274 - accuracy: 0.9580
    15
    100/100 [==============================] - 0s 4ms/step - loss: 0.2855 - accuracy: 0.9580
    16
    100/100 [==============================] - 1s 5ms/step - loss: 0.2645 - accuracy: 0.9620
    17
    100/100 [==============================] - 0s 5ms/step - loss: 0.2507 - accuracy: 0.9565
    18
    100/100 [==============================] - ETA: 0s - loss: 0.2021 - accuracy: 0.97 - 1s 5ms/step - loss: 0.2039 - accuracy: 0.9725
    19
    100/100 [==============================] - 1s 5ms/step - loss: 0.1815 - accuracy: 0.9805
    20
    100/100 [==============================] - 0s 5ms/step - loss: 0.1667 - accuracy: 0.9830: 0s - loss: 0.1825 - 
    21
    100/100 [==============================] - 0s 5ms/step - loss: 0.1501 - accuracy: 0.9835
    22
    100/100 [==============================] - 0s 5ms/step - loss: 0.1325 - accuracy: 0.9835: 0s - loss: 0.1326 - accuracy: 0.98
    23
    100/100 [==============================] - 0s 5ms/step - loss: 0.1477 - accuracy: 0.9660
    24
    100/100 [==============================] - 0s 5ms/step - loss: 0.3715 - accuracy: 0.8645
    25
    100/100 [==============================] - 1s 5ms/step - loss: 0.1166 - accuracy: 0.9855
    26
    100/100 [==============================] - 0s 5ms/step - loss: 0.0918 - accuracy: 0.9870
    27
    100/100 [==============================] - 0s 5ms/step - loss: 0.0881 - accuracy: 0.9875
    28
    100/100 [==============================] - 0s 5ms/step - loss: 0.0795 - accuracy: 0.9880
    29
    100/100 [==============================] - 1s 5ms/step - loss: 0.0768 - accuracy: 0.9850



```python
X, y = generate_data(n_samples, n_numbers, largest, alphabet)
result = model.predict(X, batch_size=n_batch, verbose=0)
```


```python
expected = [invert(z, alphabet) for z in y]
predicted = [invert(z, alphabet) for z in result]
for i in range(20):
    print('Expected=%s, Predicted=%s' % (expected[i], predicted[i]))
```

    Expected=13, Predicted=13
    Expected=13, Predicted=13
    Expected=13, Predicted=13
    Expected= 9, Predicted= 9
    Expected=11, Predicted=11
    Expected=18, Predicted=18
    Expected=15, Predicted=15
    Expected=14, Predicted=14
    Expected= 6, Predicted= 6
    Expected=15, Predicted=15
    Expected= 9, Predicted= 9
    Expected=10, Predicted=10
    Expected= 8, Predicted= 8
    Expected=14, Predicted=14
    Expected=14, Predicted=14
    Expected=19, Predicted=19
    Expected= 4, Predicted= 4
    Expected=13, Predicted=13
    Expected= 9, Predicted= 9
    Expected=12, Predicted=12


通过上面的这个很简单的例子，我们知道了 seq2seq 是如何处理序列的，下面我们将自注意力部分。

## Attention


为了改善seq2seq上述的两个瓶颈问题，Bahdanau 在 2015 年首次提出注意力模型(Attention)


在这个注意力模型中，Decoder 的每一个时间步都可以访问到 Encoder 的所有状态信息，这样记忆问题得以改善，而且在 Decoder 的不同时间步可以对 Encoder 中不同的时间步予以不同程度的关注，这样重要信息不会被淹没。


在没有注意力的 seq2seq 中，上下文向量是 Encoder 最后的**隐向量**，在 Attention 中，上下文向量是这些隐向量的**加权平均**。

在没有注意力的 seq2seq 中，上下文向量只是在 Decoder 开始时输入进去，在 Attention 中，上下文向量会传递给 Decoder 的每一个时间步。



**几种经典的注意力模型**


根据对齐函数的不同，又有 Global attention 和 Local attention 两种。

根据生成向量函数的不同，有 Hard attention 和 Soft attention 之分。

同样附上代码：


```python
import tensorflow as tf
from keras import backend as K
from keras import regularizers, constraints, initializers, activations
from keras.layers.recurrent import Recurrent          
from keras.engine import InputSpec

def time_distributed_dense(x, w, b=None, dropout=None,
                           input_dim=None, output_dim=None, timesteps=None):
    if not input_dim:
        input_dim = K.shape(x)[2]
    if not timesteps:
        timesteps = K.shape(x)[1]
    if not output_dim:
        output_dim = K.shape(w)[1]

    if dropout:
        # 在每个时间步采用同样的 dropout
        ones = K.ones_like(K.reshape(x[:, 0, :], (-1, input_dim)))
        dropout_matrix = K.dropout(ones, dropout)
        expanded_dropout_matrix = K.repeat(dropout_matrix, timesteps)
        x *= expanded_dropout_matrix

    x = K.reshape(x, (-1, input_dim))

    x = K.dot(x, w)
    if b:
        x = x + b

    x = K.reshape(x, (-1, timesteps, output_dim))
    return x

tfPrint = lambda d, T: tf.Print(input_=T, data=[T, tf.shape(T)], message=d)

class AttentionDecoder(Recurrent):

    # 在 __init__ 初始化权重，激活函数，正则化算法等
    def __init__(self, units, output_dim,
                 activation='tanh',
                 return_probabilities=False,
                 name='AttentionDecoder',
                 kernel_initializer='glorot_uniform',
                 recurrent_initializer='orthogonal',
                 bias_initializer='zeros',
                 kernel_regularizer=None,
                 bias_regularizer=None,
                 activity_regularizer=None,
                 kernel_constraint=None,
                 bias_constraint=None,
                 **kwargs):

        self.units = units                        # 隐状态的维度
        self.output_dim = output_dim            # 输出序列的标签个数
        self.return_probabilities = return_probabilities
        self.activation = activations.get(activation)
        self.kernel_initializer = initializers.get(kernel_initializer)
        self.recurrent_initializer = initializers.get(recurrent_initializer)
        self.bias_initializer = initializers.get(bias_initializer)

        self.kernel_regularizer = regularizers.get(kernel_regularizer)
        self.recurrent_regularizer = regularizers.get(kernel_regularizer)
        self.bias_regularizer = regularizers.get(bias_regularizer)
        self.activity_regularizer = regularizers.get(activity_regularizer)

        self.kernel_constraint = constraints.get(kernel_constraint)
        self.recurrent_constraint = constraints.get(kernel_constraint)
        self.bias_constraint = constraints.get(bias_constraint)

        super(AttentionDecoder, self).__init__(**kwargs)
        self.name = name
        self.return_sequences = True  # must return sequences

    # build(input_shape): 在这里定义模型中用到的权重
    def build(self, input_shape):

        self.batch_size, self.timesteps, self.input_dim = input_shape

        if self.stateful:
            super(AttentionDecoder, self).reset_states()

        self.states = [None, None]  # y, s

        """
            用来建立上下文向量
        """

        self.V_a = self.add_weight(shape=(self.units,),
                                   name='V_a',
                                   initializer=self.kernel_initializer,
                                   regularizer=self.kernel_regularizer,
                                   constraint=self.kernel_constraint)
        self.W_a = self.add_weight(shape=(self.units, self.units),
                                   name='W_a',
                                   initializer=self.kernel_initializer,
                                   regularizer=self.kernel_regularizer,
                                   constraint=self.kernel_constraint)
        self.U_a = self.add_weight(shape=(self.input_dim, self.units),
                                   name='U_a',
                                   initializer=self.kernel_initializer,
                                   regularizer=self.kernel_regularizer,
                                   constraint=self.kernel_constraint)
        self.b_a = self.add_weight(shape=(self.units,),
                                   name='b_a',
                                   initializer=self.bias_initializer,
                                   regularizer=self.bias_regularizer,
                                   constraint=self.bias_constraint)
        """
            用来建立 reset 门
        """
        self.C_r = self.add_weight(shape=(self.input_dim, self.units),
                                   name='C_r',
                                   initializer=self.recurrent_initializer,
                                   regularizer=self.recurrent_regularizer,
                                   constraint=self.recurrent_constraint)
        self.U_r = self.add_weight(shape=(self.units, self.units),
                                   name='U_r',
                                   initializer=self.recurrent_initializer,
                                   regularizer=self.recurrent_regularizer,
                                   constraint=self.recurrent_constraint)
        self.W_r = self.add_weight(shape=(self.output_dim, self.units),
                                   name='W_r',
                                   initializer=self.recurrent_initializer,
                                   regularizer=self.recurrent_regularizer,
                                   constraint=self.recurrent_constraint)
        self.b_r = self.add_weight(shape=(self.units, ),
                                   name='b_r',
                                   initializer=self.bias_initializer,
                                   regularizer=self.bias_regularizer,
                                   constraint=self.bias_constraint)

        """
            用来建立 update 门
        """
        self.C_z = self.add_weight(shape=(self.input_dim, self.units),
                                   name='C_z',
                                   initializer=self.recurrent_initializer,
                                   regularizer=self.recurrent_regularizer,
                                   constraint=self.recurrent_constraint)
        self.U_z = self.add_weight(shape=(self.units, self.units),
                                   name='U_z',
                                   initializer=self.recurrent_initializer,
                                   regularizer=self.recurrent_regularizer,
                                   constraint=self.recurrent_constraint)
        self.W_z = self.add_weight(shape=(self.output_dim, self.units),
                                   name='W_z',
                                   initializer=self.recurrent_initializer,
                                   regularizer=self.recurrent_regularizer,
                                   constraint=self.recurrent_constraint)
        self.b_z = self.add_weight(shape=(self.units, ),
                                   name='b_z',
                                   initializer=self.bias_initializer,
                                   regularizer=self.bias_regularizer,
                                   constraint=self.bias_constraint)
        """
            用来建立 proposal
        """
        self.C_p = self.add_weight(shape=(self.input_dim, self.units),
                                   name='C_p',
                                   initializer=self.recurrent_initializer,
                                   regularizer=self.recurrent_regularizer,
                                   constraint=self.recurrent_constraint)
        self.U_p = self.add_weight(shape=(self.units, self.units),
                                   name='U_p',
                                   initializer=self.recurrent_initializer,
                                   regularizer=self.recurrent_regularizer,
                                   constraint=self.recurrent_constraint)
        self.W_p = self.add_weight(shape=(self.output_dim, self.units),
                                   name='W_p',
                                   initializer=self.recurrent_initializer,
                                   regularizer=self.recurrent_regularizer,
                                   constraint=self.recurrent_constraint)
        self.b_p = self.add_weight(shape=(self.units, ),
                                   name='b_p',
                                   initializer=self.bias_initializer,
                                   regularizer=self.bias_regularizer,
                                   constraint=self.bias_constraint)
        """
            用来生成预测结果
        """
        self.C_o = self.add_weight(shape=(self.input_dim, self.output_dim),
                                   name='C_o',
                                   initializer=self.recurrent_initializer,
                                   regularizer=self.recurrent_regularizer,
                                   constraint=self.recurrent_constraint)
        self.U_o = self.add_weight(shape=(self.units, self.output_dim),
                                   name='U_o',
                                   initializer=self.recurrent_initializer,
                                   regularizer=self.recurrent_regularizer,
                                   constraint=self.recurrent_constraint)
        self.W_o = self.add_weight(shape=(self.output_dim, self.output_dim),
                                   name='W_o',
                                   initializer=self.recurrent_initializer,
                                   regularizer=self.recurrent_regularizer,
                                   constraint=self.recurrent_constraint)
        self.b_o = self.add_weight(shape=(self.output_dim, ),
                                   name='b_o',
                                   initializer=self.bias_initializer,
                                   regularizer=self.bias_regularizer,
                                   constraint=self.bias_constraint)

        # 建立初始状态
        self.W_s = self.add_weight(shape=(self.input_dim, self.units),
                                   name='W_s',
                                   initializer=self.recurrent_initializer,
                                   regularizer=self.recurrent_regularizer,
                                   constraint=self.recurrent_constraint)

        self.input_spec = [
            InputSpec(shape=(self.batch_size, self.timesteps, self.input_dim))]
        self.built = True

    # call(x): 在这里编写层的功能逻辑，它的第一个参数是输入张量
    def call(self, x):
        # 这一句是用来存储整个序列，以便后面在每一个时间步时使用
        self.x_seq = x

        # 这一步是在计算 e j t 中的 U a h j，
        # 用 time_distributed_dense 对编码序列的所有元素执行这个计算，
        # 放在这里因为它不依赖前面的步骤，可以节省计算时间。
        self._uxpb = time_distributed_dense(self.x_seq, self.U_a, b=self.b_a,
                                             input_dim=self.input_dim,
                                             timesteps=self.timesteps,
                                             output_dim=self.units)

        return super(AttentionDecoder, self).call(x)

    def get_initial_state(self, inputs):
        print('inputs shape:', inputs.get_shape())

        # 在第一个时间步得到初始状态 s0.
        s0 = activations.tanh(K.dot(inputs[:, 0], self.W_s))

        # 用 keras.layers.recurrent 初始化向量 (batchsize, output_dim)
        y0 = K.zeros_like(inputs)          # (samples, timesteps, input_dims)
        y0 = K.sum(y0, axis=(1, 2))      # (samples, )
        y0 = K.expand_dims(y0)          # (samples, 1)
        y0 = K.tile(y0, [1, self.output_dim])

        return [y0, s0]

    # step 是模型建立的核心部分
    def step(self, x, states):

        # 首先取 t-1 时刻的输出和状态
        ytm, stm = states

        # equation 1

        # 因为计算是向量化的，需要将隐状态重复多次，使它的长度等于输入序列的长度
        _stm = K.repeat(stm, self.timesteps)

        # 权重矩阵与隐状态相乘
        _Wxstm = K.dot(_stm, self.W_a)

        # 计算注意力概率
        et = K.dot(activations.tanh(_Wxstm + self._uxpb),
                   K.expand_dims(self.V_a))

        # equation 2 

        at = K.exp(et)
        at_sum = K.sum(at, axis=1)
        at_sum_repeated = K.repeat(at_sum, self.timesteps)        # 用 repeat 使每个时间步除以相应的和
        at /= at_sum_repeated                                      # 此时向量大小 (batchsize, timesteps, 1)

        # equation 3

        # 计算上下文向量
        # self.x_seq 和 at 的维度中有 batch dimension，需要用 batch_dot 避开在这个维度上的乘法
        context = K.squeeze(K.batch_dot(at, self.x_seq, axes=1), axis=1)

        # equation 4  (reset gate)

        # 计算新的隐状态
        # 首先计算 reset 门
        rt = activations.sigmoid(
            K.dot(ytm, self.W_r)
            + K.dot(stm, self.U_r)
            + K.dot(context, self.C_r)
            + self.b_r)

        # equation 5 (update gate)

        # 计算 z 门
        zt = activations.sigmoid(
            K.dot(ytm, self.W_z)
            + K.dot(stm, self.U_z)
            + K.dot(context, self.C_z)
            + self.b_z)

        # equation 6 (proposal state)

        # 计算 proposal 隐状态
        s_tp = activations.tanh(
            K.dot(ytm, self.W_p)
            + K.dot((rt * stm), self.U_p)
            + K.dot(context, self.C_p)
            + self.b_p)

        # equation 7 (new hidden states)

        # 得到新的隐状态
        st = (1-zt)*stm + zt * s_tp

        # equation 8 

        yt = activations.softmax(
            K.dot(ytm, self.W_o)
            + K.dot(stm, self.U_o)
            + K.dot(context, self.C_o)
            + self.b_o)

        if self.return_probabilities:
            return at, [yt, st]
        else:
            return yt, [yt, st]

    # compute_output_shape(input_shape): 在这里定义张量的形状变化逻辑，对于任意给定的输入，Keras 可以自动推断各层输出的形状。
    def compute_output_shape(self, input_shape):
        if self.return_probabilities:
            return (None, self.timesteps, self.timesteps)
        else:
            return (None, self.timesteps, self.output_dim)

    def get_config(self):
        config = {
            'output_dim': self.output_dim,
            'units': self.units,
            'return_probabilities': self.return_probabilities
        }
        base_config = super(AttentionDecoder, self).get_config()
        return dict(list(base_config.items()) + list(config.items()))

# 应用注意力机制，建立模型：
if __name__ == '__main__':
    from keras.layers import Input, LSTM
    from keras.models import Model
    from keras.layers.wrappers import Bidirectional

    i = Input(shape=(100,104), dtype='float32')
    enc = Bidirectional(LSTM(64, return_sequences=True), merge_mode='concat')(i)
    dec = AttentionDecoder(32, 4)(enc)
    model = Model(inputs=i, outputs=dec)
    model.summary()

    
```


    ---------------------------------------------------------------------------
    
    ImportError                               Traceback (most recent call last)
    
    <ipython-input-18-8b4f34e37cb9> in <module>
          2 from keras import backend as K
          3 from keras import regularizers, constraints, initializers, activations
    ----> 4 from keras.layers.recurrent import Recurrent
          5 from keras.engine import InputSpec
          6 


    ImportError: cannot import name 'Recurrent' from 'keras.layers.recurrent' (d:\ProgramData\Anaconda3\lib\site-packages\keras\layers\recurrent.py)


## Transformer

**Transformer** 是由 Google 团队的 Ashish Vaswani 等人在 2017 年 6 月发表的论文 Attention Is All You Need 中提出的 NLP 经典之作，这个模型可以算是近几年来 NLP 领域的一个重大的里程碑，在它之前 seq2seq + Attention 就表现很强了，结果这篇论文一出来就引起了不小的轰动，它竟然不需要任何 RNN 等结构，只通过注意力机制就可以在机器翻译任务上超过 RNN，CNN 等模型的表现。

#### Transformer 和 RNN 比较

在机器翻译任务中，虽然说在 Transformer 之前 Encoder-Decoder + Attention 结构已经有很好的表现了，但是其中的 RNN 结构却存在着一些不足。

- 首先，RNN 模型不擅长并行计算。因为 RNN 具有序列的性质，就是当模型处理一个状态时需要依赖于之前的状态，这个性质不利于使用 GPU 进行计算，即使用了 CuDNN，RNN 在 GPU 上也还是很低效的。

- 而 Transformer 最大的优点就是可以高效地并行化﻿，因为它的模型内部的核心其实就是大量的矩阵乘法运算，能够很好地用于并行计算，这也是 Transformer 很快的原因之一。

- 另一个不足就是 RNN 在学习长期依赖上存在困难，可能存在梯度消失等问题。尽管 LSTM 和 Attention 在理论上都可以处理长期记忆，但是记忆这些长期信息也是一个很大的挑战。
-  而 Transformer 可以用注意力机制来对这些长期依赖进行建模，尤其是论文还提出了 Multi-Head Attention，让模型的性能更强大。

#### Transformer模型

Transformer 的基本框架本质上就是一种 Encoder-Decoder 结构，如下图所示是它的基本单元，左侧是 Encoder 部分，右侧是 Decoder：


![image.png](attachment:image.png)

## 参考：

-  NLP之Seq2Seq:https://blog.csdn.net/qq_32241189/article/details/81591456
-  Seq2seq+Attention模型最通俗易懂的讲解:https://zhuanlan.zhihu.com/p/150294471


