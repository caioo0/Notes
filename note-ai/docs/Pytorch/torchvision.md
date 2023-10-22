# tochvision

## **一、简介**

tochvision主要处理图像数据，包含一些常用的数据集、模型、转换函数等。torchvision独立于PyTorch，需要专门安装。
torchvision主要包含以下四部分：

- torchvision.models: 提供深度学习中各种经典的网络结构、预训练好的模型，如：Alex-Net、VGG、ResNet、Inception等。
- torchvision.datasets：提供常用的数据集，设计上继承 torch.utils.data.Dataset，主要包括：MNIST、CIFAR10/100、ImageNet、COCO等。
- torchvision.transforms：提供常用的数据预处理操作，主要包括对Tensor及PIL Image对象的操作。
- torchvision.utils：工具类，如保存张量作为图像到磁盘，给一个小批量创建一个图像网格。

## 二、安装

```
pip install torchvision
```

torchvision要注意与pytorch版本和Cuda相匹配。
要查询pytorch和torchvision的版本，可以使用下面语句 ：

```
import torch
import torchvision
print(torch.__version__)
print(torchvision.__version__)
```

