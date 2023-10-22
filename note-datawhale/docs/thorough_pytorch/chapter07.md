# 第七章 PyTorch可视化

（本学习笔记来源于[DataWhale-深入浅出PyTorch](https://github.com/datawhalechina/thorough-pytorch)）

关键知识点： `torchinfo`,`CNN可视化`,`grad-cam`,`flashtorch`, `TensorBoard`

## 7.1 可视化网络结构

### 7.1.1 使用print函数打印模型基础信息

```python
import torchvision.models as models
model = models.resnet18()
```

```python
ResNet(
  (conv1): Conv2d(3, 64, kernel_size=(7, 7), stride=(2, 2), padding=(3, 3), bias=False)
  (bn1): BatchNorm2d(64, eps=1e-05, momentum=0.1, affine=True, track_running_stats=True)
  (relu): ReLU(inplace=True)
  (maxpool): MaxPool2d(kernel_size=3, stride=2, padding=1, dilation=1, ceil_mode=False)
  (layer1): Sequential(
    (0): Bottleneck(
      (conv1): Conv2d(64, 64, kernel_size=(1, 1), stride=(1, 1), bias=False)
      (bn1): BatchNorm2d(64, eps=1e-05, momentum=0.1, affine=True, track_running_stats=True)
      (conv2): Conv2d(64, 64, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1), bias=False)
      (bn2): BatchNorm2d(64, eps=1e-05, momentum=0.1, affine=True, track_running_stats=True)
      (conv3): Conv2d(64, 256, kernel_size=(1, 1), stride=(1, 1), bias=False)
      (bn3): BatchNorm2d(256, eps=1e-05, momentum=0.1, affine=True, track_running_stats=True)
      (relu): ReLU(inplace=True)
      (downsample): Sequential(
        (0): Conv2d(64, 256, kernel_size=(1, 1), stride=(1, 1), bias=False)
        (1): BatchNorm2d(256, eps=1e-05, momentum=0.1, affine=True, track_running_stats=True)
      )
    )
  )
  (avgpool): AdaptiveAvgPool2d(output_size=(1, 1))
  (fc): Linear(in_features=2048, out_features=1000, bias=True)
)
```

`print(model)`，只能得出基础构件的信息，既不能显示出每一层的shape，也不能显示对应参数量的大小，为了解决这些问题，我们就需要介绍`torchinfo`

### 7.1.2 使用torchinfo可视化网络结构

**torchinfo的安装**

```python
# 安装方法一
#pip install torchinfo 
# 安装方法二
!conda install -c conda-forge torchinfo
```

**torchinfo的使用**

有时候我们希望观察网络的每个层是什么操作、输出维度、模型的总参数量、训练的参数量、网络的占用内存情况。为了解决这个问题，人们开发了torchinfo工具包

torchinfo是由torchsummary和torchsummaryX重构出的库, torchsummary和torchsummaryX已经许久没更新了。

```python
import torchvision.models as models
from torchinfo import summary
resnet18 = models.resnet18() # 实例化模型
summary(model, (1, 3, 224, 224)) # 1：batch_size 3:图片的通道数 224: 图片的高宽
```

我们可以看到torchinfo提供了更加详细的信息，包括模块信息（每一层的类型、输出shape和参数量）、模型整体的参数量、模型大小、一次前向或者反向传播需要的内存大小等

## 7.2 CNN可视化

- 可视化CNN卷积核的方法
- 可视化CNN特征图的方法
- 可视化CNN显著图（class activation map）的方法

### 7.2.1 CNN卷积核可视化

PyTorch中可视化卷积核的实现方案，以torchvision自带的VGG11模型为例。

```python
import torch
from torchvision.models import vgg11

model = vgg11(pretrained=True)
print(dict(model.features.named_children()))
```

卷积核对应的应为卷积层（Conv2d），这里以第“3”层为例，可视化对应的参数：

```python
conv1 = dict(model.features.named_children())['3']
kernel_set = conv1.weight.detach()
num = len(conv1.weight.detach())
print(kernel_set.shape)
for i in range(0,num):
    i_kernel = kernel_set[i]
    plt.figure(figsize=(20, 17))
    if (len(i_kernel)) > 1:
        for idx, filer in enumerate(i_kernel):
            plt.subplot(9, 9, idx+1) 
            plt.axis('off')
            plt.imshow(filer[ :, :].detach(),cmap='bwr')
```

### 7.2.2 CNN特征图可视化方法

```python
class Hook(object):
    def __init__(self):
        self.module_name = []
        self.features_in_hook = []
        self.features_out_hook = []

    def __call__(self,module, fea_in, fea_out):
        print("hooker working", self)
        self.module_name.append(module.__class__)
        self.features_in_hook.append(fea_in)
        self.features_out_hook.append(fea_out)
        return None
  

def plot_feature(model, idx):
    hh = Hook()
    model.features[idx].register_forward_hook(hh)
  
    forward_model(model,False)
    print(hh.module_name)
    print((hh.features_in_hook[0][0].shape))
    print((hh.features_out_hook[0].shape))
  
    out1 = hh.features_out_hook[0]

    total_ft  = out1.shape[1]
    first_item = out1[0].cpu().clone()  

    plt.figure(figsize=(20, 17))
  

    for ftidx in range(total_ft):
        if ftidx > 99:
            break
        ft = first_item[ftidx]
        plt.subplot(10, 10, ftidx+1) 
    
        plt.axis('off')
        #plt.imshow(ft[ :, :].detach(),cmap='gray')
        plt.imshow(ft[ :, :].detach())
```

这里我们首先实现了一个hook类，之后在plot_feature函数中，将该hook类的对象注册到要进行可视化的网络的某层中。model在进行前向传播的时候会调用hook的__call__函数，我们也就是在那里存储了当前层的输入和输出。这里的features_out_hook 是一个list，每次前向传播一次，都是调用一次，也就是features_out_hook  长度会增加1。

### 7.2.3 CNN class activation map可视化方法

CAM系列操作的实现可以通过开源工具包pytorch-grad-cam来实现。

- 安装

```python
pip install grad-cam
```

一个简单的例子

```python
import torch
from torchvision.models import vgg11,resnet18,resnet101,resnext101_32x8d
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np

model = vgg11(pretrained=True)
img_path = './dog.jpg'
# resize操作是为了和传入神经网络训练图片大小一致
img = Image.open(img_path).resize((224,224))
# 需要将原始图片转为np.float32格式并且在0-1之间 
rgb_img = np.float32(img)/255
plt.imshow(img)
```

```python
from pytorch_grad_cam import GradCAM,ScoreCAM,GradCAMPlusPlus,AblationCAM,XGradCAM,EigenCAM,FullGrad
from pytorch_grad_cam.utils.model_targets import ClassifierOutputTarget
from pytorch_grad_cam.utils.image import show_cam_on_image

target_layers = [model.features[-1]]
# 选取合适的类激活图，但是ScoreCAM和AblationCAM需要batch_size
cam = GradCAM(model=model,target_layers=target_layers)
targets = [ClassifierOutputTarget(preds)]
grayscale_cam = cam(input_tensor=img_tensor, targets=targets)
grayscale_cam = grayscale_cam[0, :]
cam_img = show_cam_on_image(rgb_img, grayscale_cam, use_rgb=True)
print(type(cam_img))
Image.fromarray(cam_img)
```

### 7.2.4 使用FlashTorch快速实现CNN可视化

目前已经有不少开源工具能够帮助我们快速实现CNN可视化。这里我们介绍其中的一个——[FlashTorch](https://github.com/MisaOgura/flashtorch)。

- 安装

```python
pip install flashtorch
```

- 可视化梯度

```python
# Download example images
# !mkdir -p images
# !wget -nv \
#    https://github.com/MisaOgura/flashtorch/raw/master/examples/images/great_grey_owl.jpg \
#    https://github.com/MisaOgura/flashtorch/raw/master/examples/images/peacock.jpg   \
#    https://github.com/MisaOgura/flashtorch/raw/master/examples/images/toucan.jpg    \
#    -P /content/images

import matplotlib.pyplot as plt
import torchvision.models as models
from flashtorch.utils import apply_transforms, load_image
from flashtorch.saliency import Backprop

model = models.alexnet(pretrained=True)
backprop = Backprop(model)

image = load_image('/content/images/great_grey_owl.jpg')
owl = apply_transforms(image)

target_class = 24
backprop.visualize(owl, target_class, guided=True, use_gpu=True)
```

可视化卷积核

```python
import torchvision.models as models
from flashtorch.activmax import GradientAscent

model = models.vgg16(pretrained=True)
g_ascent = GradientAscent(model.features)

# specify layer and filter info
conv5_1 = model.features[24]
conv5_1_filters = [45, 271, 363, 489]

g_ascent.visualize(conv5_1, conv5_1_filters, title="VGG16: conv5_1")
```

## 7.3 使用TensorBoard可视化训练过程

- 安装TensorBoard工具
- 了解TensorBoard可视化的基本逻辑
- 掌握利用TensorBoard实现训练过程可视化
- 掌握利用TensorBoard完成其他内容的可视化

### 7.3.1 TensorBoard安装

```python
pip install tensorboard
```

也可以使用PyTorch自带的tensorboard工具，此时不需要额外安装tensorboard。

### 7.3.2 TensorBoard可视化的基本逻辑

Tensorboard的工作流程简单来说是

- 将代码运行过程中的，某些你关心的数据保存在一个文件夹中：

```md
这一步由代码中的writer完成
```

- 再读取这个文件夹中的数据，用浏览器显示出来：

```md
这一步通过在命令行运行tensorboard完成。
```

相关代码：
首先导入tensorboard

```python
from torch.utils.tensorboard import SummaryWriter   
```

这里的SummaryWriter的作用就是，将数据以特定的格式存储到刚刚提到的那个文件夹中。

首先我们将其实例化

```python
writer = SummaryWriter('./path/to/log')
```

这里传入的参数就是指向文件夹的路径，之后我们使用这个writer对象“拿出来”的任何数据都保存在这个路径之下。

这个对象包含多个方法，比如针对数值，我们可以调用

```python
writer.add_scalar(tag, scalar_value, global_step=None, walltime=None)
```

这里的tag指定可视化时这个变量的名字，scalar_value是你要存的值，global_step可以理解为x轴坐标。

举一个简单的例子：

```python
for epoch in range(100)
    mAP = eval(model)
    writer.add_scalar('mAP', mAP, epoch)
```

这样就会生成一个x轴跨度为100的折线图，y轴坐标代表着每一个epoch的mAP。这个折线图会保存在指定的路径下（但是现在还看不到）

同理，除了数值，我们可能还会想看到模型训练过程中的图像

```python
 writer.add_image(tag, img_tensor, global_step=None, walltime=None, dataformats='CHW')
 writer.add_images(tag, img_tensor, global_step=None, walltime=None, dataformats='NCHW')
```

### 可视化

我们已经将关心的数据拿出来了，接下来我们只需要在命令行运行：

```python
tensorboard --logdir=./path/to/the/folder --port 8123
```

然后打开浏览器，访问地址http://localhost:8123/ 即可。 这里的8123只是随便一个例子，用其他的未被占用端口也没有任何问题，注意命令行的端口与浏览器访问的地址同步。

如果发现不显示数据，注意检查一下路径是否正确，命令行这里注意是

```python
--logdir=./path/to/the/folder 
```

而不是

```python
--logdir= './path/to/the/folder '
```

另一点要注意的是tensorboard并不是实时显示（visdom是完全实时的），而是默认30秒刷新一次。

#### 其他注意项

**1.变量归类**

命名变量的时候可以使用形如

```python
writer.add_scalar('loss/loss1', loss1, epoch)
writer.add_scalar('loss/loss2', loss2, epoch)
writer.add_scalar('loss/loss3', loss3, epoch)
```

的格式，这样3个loss就会被显示在同一个section。

**2.同时显示多个折线图**

假如使用了两种学习率去训练同一个网络，想要比较它们训练过程中的loss曲线，只需要将两个日志文件夹放到同一目录下，并在命令行运行

```python
tensorboard --logdir=./path/to/the/root --port 8123
```

## 7.4 参考资料

1. https://github.com/datawhalechina/thorough-pytorch
2. https://andrewhuman.github.io/cnn-hidden-layout_search
3. https://github.com/jacobgil/pytorch-grad-cam
4. https://github.com/MisaOgura/flashtorch
5. https://zhuanlan.zhihu.com/p/103630393
6. https://github.com/lanpa/tensorboardX
