# PyTorch进阶训练技巧
----

（本学习笔记来源于[DataWhale-深入浅出PyTorch](https://github.com/datawhalechina/thorough-pytorch)）



## 6.1 自定义损失函数

`torch.nn`模块提供的损失函数有：`MSELoss`,`L1Loss`,`BCELoss`等，也有非官方提供的Loss:`DiceLoss`,`HuberLoss`,`SobolevLoss`,这些非通用损失函数的实现需要我们通过自定义损失函数来实现。


### 6.1.1  以函数方式定义



```python
def my_loss(output,target):
    loss = torch.mean((output-target)**2)
    return loss
```

### 6.1.2 以类方式定义

比起函数丁依依的方式，以类方式定义更加常用。在以类方式定义损失函数时，我们如果看每一个损失函数的继承关系我们就可以发现`Loss`函数部分继承自`_loss`, 部分继承自`_WeightedLoss`, 而`_WeightedLoss`继承自`_loss`，` _loss`继承自 **nn.Module**。


DiceLoss是一种在分割领域常见的损失函数，定义如下：

$$
DSC = \frac{2|X∩Y|}{|X|+|Y|}
$$

实现代码如下：


```python
import torch.nn as nn

class DiceLoss(nn.Module):
    def __init__(self,weight=None,size_average=True):
        super(DiceLoss,self).__init__()
        
    def forward(self,inputs,targets,smooth=1):
        inputs = F.sigmoid(inputs)
        inputs = inputs.view(-1)
        targets = targets.view(-1)
        intersection = (inputs * targes).sum()
        dice = (2.* intersection + smooth)/(inputs.sum() + targets.sum() + smooth)
        
        return 1 - dice
    
# 使用方法
criterion = DiceLoss()
loss = criterion(input,targets)

        
```

除此之外，常见的损失函数还有BCE-Dice Loss，Jaccard/Intersection over Union (IoU) Loss，Focal Loss......


```python
import torch.nn as nn

class DiceBCELoss(nn.Module):
    def __init__(self, weight=None, size_average=True):
        super(DiceBCELoss, self).__init__()

    def forward(self, inputs, targets, smooth=1):
        inputs = F.sigmoid(inputs)       
        inputs = inputs.view(-1)
        targets = targets.view(-1)
        intersection = (inputs * targets).sum()                     
        dice_loss = 1 - (2.*intersection + smooth)/(inputs.sum() + targets.sum() + smooth)  
        BCE = F.binary_cross_entropy(inputs, targets, reduction='mean')
        Dice_BCE = BCE + dice_loss
        
        return Dice_BCE

    
class IoULoss(nn.Module):
    def __init__(self, weight=None, size_average=True):
        super(IoULoss, self).__init__()

    def forward(self, inputs, targets, smooth=1):
        inputs = F.sigmoid(inputs)       
        inputs = inputs.view(-1)
        targets = targets.view(-1)
        intersection = (inputs * targets).sum()
        total = (inputs + targets).sum()
        union = total - intersection 
        
        IoU = (intersection + smooth)/(union + smooth)
                
        return 1 - IoU

    
ALPHA = 0.8
GAMMA = 2

class FocalLoss(nn.Module):
    def __init__(self, weight=None, size_average=True):
        super(FocalLoss, self).__init__()

    def forward(self, inputs, targets, alpha=ALPHA, gamma=GAMMA, smooth=1):
        inputs = F.sigmoid(inputs)       
        inputs = inputs.view(-1)
        targets = targets.view(-1)
        BCE = F.binary_cross_entropy(inputs, targets, reduction='mean')
        BCE_EXP = torch.exp(-BCE)
        focal_loss = alpha * (1-BCE_EXP)**gamma * BCE
                       
        return focal_loss
# 更多的可以参考链接1
```

## 6.2 动态调整学习率


通过一个适当的学习率衰减策略来改善这种现象，提高学习率的精度。这种设置方式在PyTorch中被称为**scheduler**

### 6.2.1 scheduler

官方提供的API,详细见[官方文档](https://pytorch.org/docs/stable/optim.html)

+ [`lr_scheduler.LambdaLR`](https://pytorch.org/docs/stable/generated/torch.optim.lr_scheduler.LambdaLR.html#torch.optim.lr_scheduler.LambdaLR)
+ [`lr_scheduler.MultiplicativeLR`](https://pytorch.org/docs/stable/generated/torch.optim.lr_scheduler.MultiplicativeLR.html#torch.optim.lr_scheduler.MultiplicativeLR)
+ [`lr_scheduler.StepLR`](https://pytorch.org/docs/stable/generated/torch.optim.lr_scheduler.StepLR.html#torch.optim.lr_scheduler.StepLR)
+ [`lr_scheduler.MultiStepLR`](https://pytorch.org/docs/stable/generated/torch.optim.lr_scheduler.MultiStepLR.html#torch.optim.lr_scheduler.MultiStepLR)
+ [`lr_scheduler.ExponentialLR`](https://pytorch.org/docs/stable/generated/torch.optim.lr_scheduler.ExponentialLR.html#torch.optim.lr_scheduler.ExponentialLR)
+ [`lr_scheduler.CosineAnnealingLR`](https://pytorch.org/docs/stable/generated/torch.optim.lr_scheduler.CosineAnnealingLR.html#torch.optim.lr_scheduler.CosineAnnealingLR)
+ [`lr_scheduler.ReduceLROnPlateau`](https://pytorch.org/docs/stable/generated/torch.optim.lr_scheduler.ReduceLROnPlateau.html#torch.optim.lr_scheduler.ReduceLROnPlateau)
+ [`lr_scheduler.CyclicLR`](https://pytorch.org/docs/stable/generated/torch.optim.lr_scheduler.CyclicLR.html#torch.optim.lr_scheduler.CyclicLR)
+ [`lr_scheduler.OneCycleLR`](https://pytorch.org/docs/stable/generated/torch.optim.lr_scheduler.OneCycleLR.html#torch.optim.lr_scheduler.OneCycleLR)
+ [`lr_scheduler.CosineAnnealingWarmRestarts`](https://pytorch.org/docs/stable/generated/torch.optim.lr_scheduler.CosineAnnealingWarmRestarts.html#torch.optim.lr_scheduler.CosineAnnealingWarmRestarts)


**使用官方API**

```
# 选择一种优化器
optimizer = torch.optim.Adam(...) 
# 选择上面提到的一种或多种动态调整学习率的方法
scheduler1 = torch.optim.lr_scheduler.... 
scheduler2 = torch.optim.lr_scheduler....
...
schedulern = torch.optim.lr_scheduler....
# 进行训练
for epoch in range(100):
    train(...)
    validate(...)
    optimizer.step()
    # 需要在优化器参数更新之后再动态调整学习率
	scheduler1.step() 
	##...
    schedulern.step()
    
    
    **注**：
```
我们在使用官方给出的`torch.optim.lr_scheduler`时，需要将`scheduler.step()`放在`optimizer.step()`后面进行使用。

### 6.2.2 自定义scheduler

通过`adjust_learning_rate`改变`param_group`中`lr`的值，来调整学习率的简单实现


```python
def adjust_learning_rate(optimizer,epoch):
    lr = args.lr * (0.1 ** (epoch //30))
    for param_group in optimizer.param_groups:
        param_group['lr'] = lr
        
```

训练过程中的调用方法：

```python
def adjust_learning_rate(optimizer,...):
    ...
optimizer = torch.optim.SGD(model.parameters(),lr = args.lr,momentum = 0.9)
for epoch in range(10):
    train(...)
    validate(...)
    adjust_learning_rate(optimizer,epoch)
```

## 6.3 模型微调


迁移学习(transfer learning)，将从源数据集学到的知识迁移到目标数据集上,这里我们了解一下迁移学习的一种应用场景**模型微调(fineturn)**。

简单来理解：我们先找到一个同类的别人训练好的模型，把别人现成的训练好了的模型拿过来，换成自己的数据，通过训练调整一下参数。

### 6.3.1 模型微调的流程

1. 在源数据集（例如ImageNet数据集）上预训练要给神经网络模型，即源模型。
2. 创建一个新的神经网络模型，即目标模型。它复制了源模型上除了输出层外的所有模型涉及及其参数。
我们假设这些模型参数包含了源数据集上学习到的知识，且这些知识同样适用于目标数据集。我们还假设源模型的输出层跟源数据集的标签紧密相关，因此在目标模型中不与采用。
3. 为目标模型参加要给输出大小为目标数据集类别个数的输出层，并随机初始化该层的模型参数。
4. 在目标数据集上训练目标模型。我们将从头训练输出层，而其他层的参数都是基于源模型的参数微调得到的。

![finetune](images\finetune.png)


### 6.3.2 使用已有模型结构

以**torchvision**中的常见模型为例，列出了如何在图像分类任务中使用PyTorch提供的常见模型结构和参数。对于其他任务和网络结构，使用方式是类似的：

**实例化网络**


```python
import torchvision.models as models
resnet18 = models.resnet18() # resnet18 = models.resnet18(pretrained=False)  等价
alexnet = models.alexnet()
vgg16 = models.vgg16()
squeezenet = models.squeezenet1_0()
densenet = models.densenet161()
inception = models.inception_v3()
googlenet = models.googlenet()
shufflenet = models.shufflenet_v2_x1_0()
mobilenet_v2 = models.mobilenet_v2()
mobilenet_v3_large = models.mobilenet_v3_large()
mobilenet_v3_small = models.mobilenet_v3_small()
resnext50_32x4d = models.resnext50_32x4d()
wide_resnet50_2 = models.wide_resnet50_2()
mnasnet = models.mnasnet1_0()

```

**传递`pretrained`参数**

通过`True`或者`False`来决定是否使用预训练好的权重，在默认状态下`pretrained = False`，意味着我们不使用预训练得到的权重，当`pretrained = True`，意味着我们将使用在一些数据集上预训练得到的权重。


```python
import torchvision.models as models
resnet18 = models.resnet18(pretrained=True)
alexnet = models.alexnet(pretrained=True)
squeezenet = models.squeezenet1_0(pretrained=True)
vgg16 = models.vgg16(pretrained=True)
densenet = models.densenet161(pretrained=True)
inception = models.inception_v3(pretrained=True)
googlenet = models.googlenet(pretrained=True)
shufflenet = models.shufflenet_v2_x1_0(pretrained=True)
mobilenet_v2 = models.mobilenet_v2(pretrained=True)
mobilenet_v3_large = models.mobilenet_v3_large(pretrained=True)
mobilenet_v3_small = models.mobilenet_v3_small(pretrained=True)
resnext50_32x4d = models.resnext50_32x4d(pretrained=True)
wide_resnet50_2 = models.wide_resnet50_2(pretrained=True)
mnasnet = models.mnasnet1_0(pretrained=True)
```

注意事项：

1. 通常PyTorch模型的扩展为`.pt`或`.pth`，程序运行时会首先检查默认路径中是否有已经下载的模型权重，一旦权重被下载，下次加载就不需要下载了。

2. 预训练模型的下载比较慢，我们可以直接通过迅雷或者其他方式去 [这里](https://github.com/pytorch/vision/tree/master/torchvision/models) 查看自己的模型里面`model_urls`，然后手动下载，预训练模型的权重在`Linux`和`Mac`的默认下载路径是用户根目录下的`.cache`文件夹。在`Windows`下就是`C:\Users\<username>\.cache\torch\hub\checkpoint`。我们可以通过使用 [`torch.utils.model_zoo.load_url()`](https://pytorch.org/docs/stable/model_zoo.html#torch.utils.model_zoo.load_url)设置权重的下载地址。

3. 如果觉得麻烦，还可以将自己的权重下载下来放到同文件夹下，然后再将参数加载网络。

   ```python
   self.model = models.resnet50(pretrained=False)
   self.model.load_state_dict(torch.load('./model/resnet50-19c8e357.pth'))
   ```

4. 如果中途强行停止下载的话，一定要去对应路径下将权重文件删除干净，要不然可能会报错。

### 6.3.3 训练特定层

在默认情况下，参数的属性`.requires_grad = True`，如果我们从头开始训练或微调不需要注意这里。但如果我们正在提取特征并且只想为新初始化的层计算梯度，其他参数不进行改变。那我们就需要通过设置`requires_grad = False`来冻结部分层。在PyTorch官方中提供了这样一个例程。


```python
def set_parameter_requires_grad(model, feature_extracting):
    if feature_extracting:
        for param in model.parameters():
            param.requires_grad = False
```

以`resnet18`为例的将1000类改为4类，但是仅改变最后一层的模型参数，不改变特征提取的模型参数；


```python
import torchvision.models as models
# 冻结参数的梯度
feature_extract = True
model = models.resnet18(pretrained=True)
set_parameter_requires_grad(model, feature_extract)
# 修改模型
num_ftrs = model.fc.in_features
model.fc = nn.Linear(in_features=512, out_features=4, bias=True)
```

注意我们先冻结模型参数的梯度，再对模型输出部分的全连接层进行修改，这样修改后的全连接层的参数就是可计算梯度的。

之后在训练过程中，`model`仍会进行梯度回传，但是参数更新则只会发生在`fc`层。通过设定参数的`requires_grad`属性，我们完成了指定训练模型的特定层的目标，这对实现模型微调非常重要。

## 6.4 半精度训练


GPU的性能主要分为两部分：算力和显存。
- 算力决定了显卡计算的速度，
- 显存决定了显卡可以同时放入多少数据用于计算。

在可以使用的显存数量一定的情况下，每次训练能够加载的数据更多（也就是batch size更大），则也可以提高训练效率。

另外，有时候数据本身也比较大（比如3D图像、视频等），显存较小的情况下可能甚至batch size为1的情况都无法实现。因此，合理使用显存也就显得十分重要。

PyTorch默认的浮点数存储方式用的是`torch.float32`,小数点后位数更多固然能保证数据的精确性，但绝大多数场景其实并不需要这么精确，只保留一半的信息也不会影响结果，也就是使用torch.float16格式。由于数位减了一半，因此被称为“半精度”，具体如下图：

![amp](images\float16.jpg)


显然半精度能够减少显存占用，使得显卡可以同时加载更多数据进行计算。本节会介绍如何在PyTorch中设置使用半精度计算。

### 6.4.1 半精度训练的设置

**import autocast**


```python
from torch.cuda.amp import autocast
```

**模型设置**

在模型定义中，使用python的装饰器方法，用`autocast`装饰模型中的`forward`函数。关于装饰器的使用，可以参考[这里](https://www.cnblogs.com/jfdwd/p/11253925.html)：

```python
@autocast()   
def forward(self, x):
    ...
    return x
```

**训练过程**

在训练过程中，只需在将数据输入模型及其之后的部分放入`with autocast():`即可：

```python
 for x in train_loader:
	x = x.cuda()
	with autocast():
        output = model(x)
        ...

```

**注意：**

半精度训练主要适用于数据本身的size比较大（比如说3D图像、视频等）。当数据本身的size并不大时（比如手写数字MNIST数据集的图片尺寸只有28*28），使用半精度训练则可能不会带来显著的提升。


## 6.5  本节参考

1. [PyTorch官方文档](https://pytorch.org/docs/stable/optim.html)
2. [参数更新](https://www.pytorchtutorial.com/docs/package_references/torch-optim/)
3. [给不同层分配不同的学习率](https://blog.csdn.net/jdzwanghao/article/details/90402577)
4. https://www.kaggle.com/bigironsphere/loss-function-library-keras-pytorch/notebook
5. https://www.zhihu.com/question/66988664/answer/247952270
6. https://blog.csdn.net/dss_dssssd/article/details/84103834
7. https://zj-image-processing.readthedocs.io/zh_CN/latest/pytorch/%E8%87%AA%E5%AE%9A%E4%B9%89%E6%8D%9F%E5%A4%B1%E5%87%BD%E6%95%B0/
8. https://blog.csdn.net/qq_27825451/article/details/95165265
9. https://discuss.pytorch.org/t/should-i-define-my-custom-loss-function-as-a-class/89468


