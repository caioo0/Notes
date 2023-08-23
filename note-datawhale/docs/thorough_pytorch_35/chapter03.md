# 第三章 PyTorch的主要组成模块
（本学习笔记来源于[DataWhale-深入浅出PyTorch](https://datawhalechina.github.io/thorough-pytorch/)）

## 3.1 机器学习 vs 深度学习

**机器学习步骤**

1. 数据预处理，包括数据格式的统一和必要的数据变换，同时划分训练集和测试集。
2. 模型选择，设定损失函数和优化函数，以及对应的超参数（也可使用`sklearn`自带的损失函数和优化器）。
3. 模型实现 拟合训练集数据，并在验证集/测试集上计算模型表现。


**深度学习步骤**

跟机器学习在流程上类似，但在代码实现上有较大的差异。

首先，由于深度学习所需的**样本量很大**，一次加载全部数据运行可能会超出内存容量而无法实现；同时还有**批（batch）训练**等提高模型表现的策略，需要每次训练读取固定数量的样本送入模型中训练，因此深度学习在数据加载上需要有专门的设计。

其次，在模型实现上，深度学习和机器学习也有很大差异。由于**深度神经网络层数往往较多，同时会有一些用于实现特定功能的层（如卷积层、池化层、批正则化层、LSTM层等），因此深度神经网络往往需要“逐层”搭建**，或者预先定义好可以实现特定功能的模块，再把这些模块组装起来。这种“定制化”的模型构建方式能够充分保证模型的灵活性，也对代码实现提出了新的要求。

最后，损失函数和优化器的设定，这部分和经典机器学习的实现是类似的。但由于模型设定的灵活性，因此损失函数和优化器要能够保证反向传播能够在用户自行定义的模型结构上实现。


深度学习中训练和验证过程最大的特点在于读入数据是按批的，每次读入一个批次的数据，放入GPU中训练，然后将损失函数反向传播回网络最前面的层，同时使用优化器调整网络参数。这里会涉及到各个模块配合的问题。训练/验证后还需要根据设定好的指标计算模型表现。


## 3.2 基本配置

首先导入必须的包， 注意这里**只是建议导入的包导入的方式**



```python
import os
import numpy as np
import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
import torch.optim as optimizer
```

超参数设置：

- batch size
- 初始学习率（初始）
- 训练次数（max_epochs）
- GPU配置



```python
batch_size = 16
lr = 1e-4
max_epochs = 100
```

GPU设置: 

两种常见的方式


```python
# 方案一：使用os.environ，这种情况如果使用GPU不需要设置

os.environ['CUDA_VISIBLE_DEVICES']  = '0,1'

# 方案二：使用"device",后续对要使用GPU的变量.to(device)即可

device = torch.device("cuda:1" if torch.cuda.is_available() else "cpu")
```

**根据实际需要一些其他模块或用户自定义模块会用到的参数，也可以一开始进行设置。**

## 3.3 读取数据

PyTorch数据读入是通过`Dataset`+`DataLoader`的方式完成的，`Dataset`定义好数据的格式和数据变换形式，`DataLoader`用`iterative`的方式不断读入批次数据。

### 3.3.1 Datasets 

`Dataset` 类是 PyTorch 图像数据集中最为重要的一个类，也是 PyTorch 中所有数据集加载类中应该继承的父类。其中，父类的两个私有成员函数必须被重载。

`Dataset`类的三个主要函数：

-  `__init__`: 向类中传入外部参数，同时定义样本集
-  `__getitem__`:支持数据集索引的函数 于逐个读取样本集合中的元素，可以进行一定的变换，并将返回训练/验证所需要的数据。
- `__len__`: 返回数据集的大小

DataSets的框架：

```python
class CustomDataset(data.Dataset): # 需要继承 data.Dataset
    def __init__(self):
        # TODO
        # 初始化文件路径或者文件列表
        pass
        
    def __getitem__(self, index):
        # TODO
        # 1. 从文件中读取指定 index 的数据（例：使用 numpy.fromfile, PIL.Image.open）
        # 2. 预处理读取的数据（例：torchvision.Transform）
        # 3. 返回数据对（例：图像和对应标签）
        pass
    
    def __len__(self):
        # TODO
        # You should change 0 to the total size of your dataset.
        return 0
```


例子，这里以[cifar10](http://www.cs.toronto.edu/~kriz/cifar.html)数据集构建`dataset`类的方式：

```python
train_data = datasets.ImageFolder(train_path,transform = data_transform)
val_data   = datasets.ImageFolder(val_path,transform = data_transform)
```

### 3.3.2 DataLoader

`DataLoader` 是 PyTorch 中读取数据的一个重要接口，该接口定义在 `dataloader.py` 文件中，该接口的目的： 将自定义的 `Dataset` 根据 `batch size` 的大小、是否 `shuffle` 等封装成一个 `batch size` 大小的 `Tensor`，用于后面的训练。

通过 `DataLoader`，使得我们在准备 `mini-batch` 时可以多线程并行处理，这样可以加快准备数据的速度。

> DataLoader 是一个高效、简洁、直观地网络输入数据结构，便于使用和扩展
> - DataLoader 本质是一个可迭代对象，使用 iter() 访问，不能使用 next() 访问
> - 使用 iter(dataloader) 返回的是一个迭代器，然后使用 next() 访问
> - 也可以使用 for features, targets in dataloaders 进行可迭代对象的访问
> - 一般我们实现一个 datasets 对象，传入到 DataLoader 中，然后内部使用 yield 返回每一次    batch 的数据

DataLoader(object) 的部分参数：

```python
# 传入的数据集
dataset(Dataset)

# 每个 batch 有多少个样本
batch_size(int, optional)

# 在每个 epoch 开始的时候，对数据进行重新排序
shuffle(bool, optional)

# 自定义从数据集中抽取样本的策略，如果指定这个参数，那么 shuffle 必须为 False
sampler(Sampler, optional)

# 与 sampler 类似，但是一次只返回一个 batch 的 indices（索引），如果指定这个参数，那么 batch_size, shuffle, sampler, drop_last 就不能再指定了
batch_sampler(Sampler, optional)

# 这个参数决定有多少进程处理数据加载，0 意味着所有数据都会被加载到主进程，默认为0
num_workers(int, optional)

# 如果设置为 True，则最后不足batch_size大小的数据会被丢弃，比如batch_size=64, 而一个epoch只有100个样本，则最后36个会被丢弃；如果设置为False，则最后的batch_size会小一点
drop_last(bool, optional)

```

## 3.4 模型构建

### 3.4.1  神经网络的构造

使用`torch.nn`构建神经网络。

上一讲已经讲过了`autograd`，`nn`包依赖 `Autograd`包来定义模型并求导， 一个`nn.Module`包含各个层和一个`forward(input)`方法，该方法返回`output`。

**约定：torch.nn 我们为了方便使用，会为他设置别名为nn，本章除nn以外还有其他的命名约定**


```python
# 首先要引入相关的包
import torch
# 引入torch.nn并指定别名
import torch.nn as nn
#打印一下版本
torch.__version__
```




    '1.9.0+cpu'



除了`nn`别名以外，我们还引用了`nn.functional`，这个包中包含了神经网络中使用的一些常用函数。

一般情况下我们会**将nn.functional 设置为大写的F**，这样缩写方便调用


```python
import torch.nn.functional as F
```

###  3.4.2 简单实现MLP网络

PyTorch中已经为我们准备好了现成的网络模型，只要继承`nn.Module`，并实现它的`forward`方法，PyTorch会根据`autograd`，自动实现`backward`函数，在`forward`函数中可使用任何`tensor`支持的函数，还可以使用if、for循环、print、log等Python语法，写法和标准的Python写法一致。


```python
import torch
from torch import nn

class MLP(nn.Module):
    # 声明带有模型参数的层，这里声明了三个全连接层
    def __init__(self, **kwargs):
        super(MLP,self).__init__(**kwargs)
        self.fc1 = nn.Linear(784,512)
        self.act1 = nn.ReLU()
        self.fc2 = nn.Linear(512,128)
        self.act2 = nn.ReLU()
        self.fc3 = nn.Linear(128,10)
        self.act3 = nn.Softmax(dim=1)
        
    def forward(self,x):
        o = self.act1(self.fc1(x))
        o = self.act2(self.fc2(o))
        return self.act3(self.fc3(o))

```


```python
X = torch.rand(2,784)
net = MLP()
print(net)
net(X)
```

    MLP(
      (fc1): Linear(in_features=784, out_features=512, bias=True)
      (act1): ReLU()
      (fc2): Linear(in_features=512, out_features=128, bias=True)
      (act2): ReLU()
      (fc3): Linear(in_features=128, out_features=10, bias=True)
      (act3): Softmax(dim=1)
    )





    tensor([[0.1047, 0.1060, 0.0996, 0.0889, 0.1035, 0.0912, 0.1113, 0.0893, 0.1108,
             0.0947],
            [0.1044, 0.1047, 0.0981, 0.0891, 0.1016, 0.0926, 0.1066, 0.0938, 0.1168,
             0.0922]], grad_fn=<SoftmaxBackward>)



### 3.4.3  神经网络中常见的层


深度学习的一个魅力在于神经网络中各式各样的层，例如全连接层、卷积层、池化层与循环层等，下面我们学习使用`Module`定义层：

- 不含模型参数的层
- 含模型参数的层


两种类型核心都一样,自定义一个继承自`nn.Module`的类,在类的`forward`函数里实现该`layer`的计算,不同的是,带参数的`layer`需要用到`nn.Parameter`

**不含模型参数的层**

直接继承`nn.Module`

自定义了一个**将输入减掉均值后输出**的层，并将层的计算定义在了 `forward` 函数里。


```python
import torch
from torch import nn

class MyLayer(nn.Module):
    def __init__(self,**kwargs):
        super(MyLayer,self).__init__(**kwargs)
        
    def forward(self,x):
        return x - x.mean()
    
```

实例化该层，然后做前向计算`forward`:



```python
layer = MyLayer()
layer(torch.tensor([1, 2, 3, 4, 5], dtype=torch.float))
```




    tensor([-2., -1.,  0.,  1.,  2.])



**含模型参数的层**

- Parameter
- ParameterList
- ParameterDict

`Parameter`类其实是`Tensor`的子类，如果一个`Tenso`r是`Parameter`，那么它会自动被添加到模型的参数列表里。所以在自定义含模型参数的层时，我们应该将参数定义成`Parameter`，除了直接定义成`Parameter`类外，还可以使用`ParameterList`和`ParameterDict`分别定义参数的列表和字典。


```python
class MyListDense(nn.Module):
    def __init__(self):
        super(MyListDense,self).__init__()
        self.params = nn.ParameterList([nn.Parameter(torch.randn(4,4)) for i in range(3)])
        self.params.append(nn.Parameter(torch.randn(4,1)))
        
    def forward(self,x):
        for i in range(len(self.params)):
            x = torch.mm(x,self.params[i])
        return x 
    
net = MyListDense()
print(net)
```

    MyListDense(
      (params): ParameterList(
          (0): Parameter containing: [torch.FloatTensor of size 4x4]
          (1): Parameter containing: [torch.FloatTensor of size 4x4]
          (2): Parameter containing: [torch.FloatTensor of size 4x4]
          (3): Parameter containing: [torch.FloatTensor of size 4x1]
      )
    )



```python
class MyDictDense(nn.Module):
    def __init__(self):
        super(MyDictDense,self).__init__()
        self.params = nn.ParameterDict({
            'linear1':nn.Parameter(torch.randn(4,4)),
            'linear2':nn.Parameter(torch.randn(4,1))
        })
        self.params.update({'linear3':nn.Parameter(torch.randn(4,2))}) # 新增
        
    def forward(self,x,choice='linear1'):
        return torch.mm(x,self.params[choice])
    
net = MyDictDense()
print(net)
        
```

    MyDictDense(
      (params): ParameterDict(
          (linear1): Parameter containing: [torch.FloatTensor of size 4x4]
          (linear2): Parameter containing: [torch.FloatTensor of size 4x1]
          (linear3): Parameter containing: [torch.FloatTensor of size 4x2]
      )
    )


下面给出常见的神经网络的一些层，比如卷积层、池化层，以及较为基础的AlexNet，LeNet等。

**二维卷积层**

二维卷积层将输入和卷积核做互相关运算，并加上一个标量偏差来得到输出。卷积层的模型参数包括了卷积核和标量偏差。在训练模型的时候，通常我们先对卷积核随机初始化，然后不断迭代卷积核和偏差。


```python
import torch
from torch import nn

# 卷积运算（二维互相关）
def corr2d(X,K):
    h,w = K.shape
    X,K = X.float(),K.float()
    Y = torch.zeros((X.shape[0] - h + 1,X.shape[1] - w + 1))
    for i in range(Y.shape[0]):
        for j in range(Y.shape[1]):
            Y[i,j] = (x[i:1+h,j:j+w] * K).sum()
    return Y

# 二维卷积层
class Conv2D(nn.Module):
    def __init__(self,kernel_size):
        super(Conv2D,self).__init__()
        self.weight 

```


## 参考资料

1. [从头学PyTorch](https://www.cnblogs.com/sdu20112013/category/1610864.html)
2. [PyTorch 中文手册（pytorch handbook）](https://handbook.pytorch.wiki/index.html)
3. [深度学习入门之 PyTorch](https://wizardforcel.gitbooks.io/learn-dl-with-pytorch-liaoxingyu/content/)
