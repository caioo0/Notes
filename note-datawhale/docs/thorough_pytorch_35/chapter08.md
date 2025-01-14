# 第八章 PyTorch生态介绍

（本学习笔记来源于[DataWhale-深入浅出PyTorch](https://github.com/datawhalechina/thorough-pytorch)）

关键知识点： `TorchVision`,`torchtext`,`PyTorchVideo`

**本章简介**

介绍PyTorch生态在图像、视频、文本等领域中的发展，针对某个领域我们选择其中有代表性的一个工具包进行详细介绍，
主要包括工具包的作者或其所在机构、数据预处理工具（这块可能再引入第三方工具包）、数据扩增、常用模型结构的预定义、预训练模型权重、常用损失函数、常用评测指标、封装好的训练&测试模块，以及可视化工具。


## 8.1 PyTorch生态

- 计算机视觉：`TorchVision`、`TorchVideo`等用于图片和视频处理
- 自然语言处理：`torchtext`
- 图卷积网络：`PyTorch Geometric`


## 8.2 torchvision

`torchvision`包含了在计算机视觉中常常用到的数据集，模型和图像处理的方式.

`torchvision`库列表 （带 * 的部分是我们经常会使用到的一些库）

+ torchvision.datasets *                           
+ torchvision.models *
+ torchvision.transforms *
+ torchvision.io 
+ torchvision.ops
+ torchvision.utils


### 8.2.2 torchvision.datasets

`torchvision.datasets`主要包含了一些我们在计算机视觉中常见的数据集，下面表格展示了部分==0.10.0版本数据集合：

| Caltech       | CelebA           | CIFAR             | Cityscapes |
| ------------- | ---------------- | ----------------- | ---------- |
| **EMNIST**    | **FakeData**     | **Fashion-MNIST** | **Flickr** |
| **ImageNet**  | **Kinetics-400** | **KITTI**         | **KMNIST** |
| **PhotoTour** | **Places365**    | **QMNIST**        | **SBD**    |
| **SEMEION**   | **STL10**        | **SVHN**          | **UCF101** |
| **VOC**       | **WIDERFace**    |                   |            |


### 8.2.3 torchvision.transforms

数据预处理操作，详细[官方文档](https://pytorch.org/vision/stable/transforms.html)


```python
from torchvision import transforms
data_transform = transforms.Compose([
    transforms.ToPILImage(),
    transforms.Resize(image_size),
    transforms.ToTensor()
])
```

### 8.2.4 torchvision.models

为了提高训练效率，减少不必要的重复劳动，PyTorch官方也提供了一些预训练好的模型供我们使用，可以点击[这里](https://github.com/pytorch/vision/tree/master/torchvision/models)进行查看现在有哪些预训练模型，下面我们将对如何使用这些模型进行详细介绍。 此处我们以torchvision0.10.0 为例，如果希望获取更多的预训练模型，可以使用使用pretrained-models.pytorch仓库。现有预训练好的模型可以分为以下几类：

- **Classification**

在图像分类里面，PyTorch官方提供了以下模型，并正在不断增多。

| AlexNet         | VGG              | ResNet        | SqueezeNet        |
| --------------- | ---------------- | ------------- | ----------------- |
| **DenseNet**    | **Inception v3** | **GoogLeNet** | **ShuffleNet v2** |
| **MobileNetV2** | **MobileNetV3**  | **ResNext**   | **Wide ResNet**   |
| **MNASNet**     | **EfficientNet** | **RegNet**    | **持续更新**      |

这些模型是在ImageNet-1k进行预训练好的，具体的使用我们会在后面进行介绍。除此之外，我们也可以点击[这里](https://pytorch.org/vision/stable/models.html#)去查看这些模型在ImageNet-1k的准确率。

- **Semantic Segmentation**

语义分割的预训练模型是在COCO train2017的子集上进行训练的，提供了20个类别，包括`background`, `aeroplane`, `bicycle`, `bird`, `boat`, `bottle, bus`, `car`, `cat`, `chair`, `cow`, `diningtable`, `dog`, `horse`, `motorbike`, `person`, `pottedplant`, `sheep`, `sofa`,`train`, `tvmonitor`。

| **FCN ResNet50**              | **FCN ResNet101**               | **DeepLabV3 ResNet50** | **DeepLabV3 ResNet101** |
| ----------------------------- | ------------------------------- | ---------------------- | ----------------------- |
| **LR-ASPP<br> MobileNetV3-Large** | **DeepLabV3 <br>MobileNetV3-Large** | **未完待续**           |                         |

- **Object Detection，instance Segmentation and Keypoint Detection**

物体检测，实例分割和人体关键点检测的模型我们同样是在COCO train2017进行训练的，在下方我们提供了实例分割的类别和人体关键点检测类别：

```python
COCO_INSTANCE_CATEGORY_NAMES = [
    '__background__', 'person', 'bicycle', 'car', 'motorcycle', 'airplane', 'bus','train', 'truck', 'boat', 'traffic light', 'fire hydrant', 'N/A', 'stop sign', 'parking meter', 'bench', 'bird', 'cat', 'dog', 'horse', 'sheep', 'cow', 'elephant', 'bear', 'zebra', 'giraffe', 'N/A', 'backpack', 'umbrella', 'N/A', 'N/A','handbag', 'tie', 'suitcase', 'frisbee', 'skis', 'snowboard', 'sports ball','kite', 'baseball bat', 'baseball glove', 'skateboard', 'surfboard', 'tennis racket','bottle', 'N/A', 'wine glass', 'cup', 'fork', 'knife', 'spoon', 'bowl','banana', 'apple', 'sandwich', 'orange', 'broccoli', 'carrot', 'hot dog', 'pizza','donut', 'cake', 'chair', 'couch', 'potted plant', 'bed', 'N/A', 'dining table','N/A', 'N/A', 'toilet', 'N/A', 'tv', 'laptop', 'mouse', 'remote', 'keyboard', 'cell phone','microwave', 'oven', 'toaster', 'sink', 'refrigerator', 'N/A', 'book','clock', 'vase', 'scissors', 'teddy bear', 'hair drier', 'toothbrush']
COCO_PERSON_KEYPOINT_NAMES =['nose','left_eye','right_eye','left_ear','right_ear','left_shoulder','right_shoulder','left_elbow','right_elbow','left_wrist','right_wrist','left_hip','right_hip','left_knee','right_knee','left_ankle','right_ankle']
```
| **Faster R-CNN** | **Mask R-CNN** | **RetinaNet** | **SSDlite** |
| ---------------- | -------------- | ------------- | ----------- |
| **SSD**          | **未完待续**   |               |             |

同样的，我们可以点击[这里](https://pytorch.org/vision/stable/models.html#object-detection-instance-segmentation-and-person-keypoint-detection)查看这些模型在COCO train 2017上的`box AP`,`keypoint AP`,`mask AP`

- **Video classification**

视频分类模型是在 Kinetics-400上进行预训练的

| **ResNet 3D 18** | **ResNet MC 18** | **ResNet (2+1) D** |
| ---------------- | ---------------- | ------------------ |
| **未完待续**     |                  |                    |

同样我们也可以点击[这里](https://pytorch.org/vision/stable/models.html#video-classification)查看这些模型的`Clip acc@1`,`Clip acc@5`

#### 8.2.5 torchvision.io

在`torchvision.io`提供了视频、图片和文件的 IO 操作的功能，它们包括读取、写入、编解码处理操作。随着torchvision的发展，io也增加了更多底层的高效率的API。在使用torchvision.io的过程中，我们需要注意以下几点：

- 不同版本之间，`torchvision.io`有着较大变化，因此在使用时，需要查看下我们的`torchvision`版本是否存在你想使用的方法。
- 除了read_video()等方法，torchvision.io为我们提供了一个细粒度的视频API torchvision.io.VideoReader()  ，它具有更高的效率并且更加接近底层处理。在使用时，我们需要先安装ffmpeg然后从源码重新编译torchvision我们才能我们能使用这些方法。
- 在使用Video相关API时，我们最好提前安装好PyAV这个库。



#### 8.2.6 torchvision.ops

torchvision.ops 为我们提供了许多计算机视觉的特定操作，包括但不仅限于NMS，RoIAlign（MASK R-CNN中应用的一种方法），RoIPool（Fast R-CNN中用到的一种方法）。在合适的时间使用可以大大降低我们的工作量，避免重复的造轮子，想看更多的函数介绍可以点击[这里](https://pytorch.org/vision/stable/ops.html)进行细致查看。



#### 8.2.7 torchvision.utils

torchvision.utils 为我们提供了一些可视化的方法，可以帮助我们将若干张图片拼接在一起、可视化检测和分割的效果。具体方法可以点击[这里](https://pytorch.org/vision/stable/utils.html)进行查看。



## 8.3 PyTorchVideo

传统视频深度学习模型仍然有着许多缺点：

- 计算资源耗费更多，并且没有高质量的`model zoo`，不能像图片一样进行迁移学习和论文复现。
- 数据集处理较麻烦，但没有一个很好的视频处理工具。
- 随着多模态越来越流行，亟需一个工具来处理其他模态。

除此之外，还有部署优化等问题，为了解决这些问题，Meta推出了`PyTorchVideo`深度学习库（包含组件如Figure 1所示）。PyTorchVideo 是一个专注于视频理解工作的深度学习库。PytorchVideo 提供了加速视频理解研究所需的可重用、模块化和高效的组件。PyTorchVideo 是使用[PyTorch](https://pytorch.org/)开发的，支持不同的深度学习视频组件，如视频模型、视频数据集和视频特定转换。

![](images/list.png)


### 8.3.1 PyTorchVideo的主要部件和亮点

PyTorchVideo主要亮点如下：

- **基于 PyTorch：**使用 PyTorch 构建。使所有 PyTorch 生态系统组件的使用变得容易。
- **Model Zoo：**PyTorchVideo提供了包含I3D、R(2+1)D、SlowFast、X3D、MViT等SOTA模型的高质量model zoo（目前还在快速扩充中，未来会有更多SOTA model），并且PyTorchVideo的model zoo调用与[PyTorch Hub](https://link.zhihu.com/?target=https%3A//pytorch.org/hub/)做了整合，大大简化模型调用，具体的一些调用方法可以参考下面的【使用 PyTorchVideo model zoo】部分。

- **数据预处理和常见数据**，PyTorchVideo支持Kinetics-400, Something-Something V2, Charades, Ava (v2.2), Epic Kitchen, HMDB51, UCF101, Domsev等主流数据集和相应的数据预处理，同时还支持randaug, augmix等数据增强trick。
- **模块化设计**：PyTorchVideo的设计类似于torchvision，也是提供许多模块方便用户调用修改，在PyTorchVideo中具体来说包括data, transforms, layer, model, accelerator等模块，方便用户进行调用和读取。
- **支持多模态**：PyTorchVideo现在对多模态的支持包括了visual和audio，未来会支持更多模态，为多模态模型的发展提供支持。
- **移动端部署优化**：PyTorchVideo支持针对移动端模型的部署优化（使用前述的PyTorchVideo/accelerator模块），模型经过PyTorchVideo优化了最高达**7倍**的提速，并实现了第一个能实时跑在手机端的X3D模型（实验中可以实时跑在2018年的三星Galaxy S8上，具体请见[Android Demo APP](https://github.com/pytorch/android-demo-app/tree/master/TorchVideo)）。

### 8.3.2 PyTorchVideo的安装

我们可以直接使用pip来安装PyTorchVideo：



```python
pip install pytorchvideo
```

注：

- 安装的虚拟环境的python版本 >= 3.7
- PyTorch >= 1.8.0，安装的torchvision也需要匹配
- CUDA >= 10.2
- ioPath：[具体情况](https://github.com/facebookresearch/iopath)
- fvcore版本 >= 0.1.4：[具体情况](https://github.com/facebookresearch/fvcore)

### 8.3.3 Model zoo 和 benchmark

在下面这部分，我将简单介绍些PyTorchVideo所提供的Model zoo和benchmark

- Kinetics-400

- 

| arch     | depth | pretrain | frame length x sample rate | top 1 | top 5 | Flops (G) x views | Params (M) | Model                                                        |
| -------- | ----- | -------- | -------------------------- | ----- | ----- | ----------------- | ---------- | ------------------------------------------------------------ |
| C2D      | R50   | \-       | 8x8                        | 71.46 | 89.68 | 25.89 x 3 x 10    | 24.33      | [link](https://dl.fbaipublicfiles.com/pytorchvideo/model_zoo/kinetics/C2D\_8x8\_R50.pyth) |
| I3D      | R50   | \-       | 8x8                        | 73.27 | 90.70 | 37.53 x 3 x 10    | 28.04      | [link](https://dl.fbaipublicfiles.com/pytorchvideo/model_zoo/kinetics/I3D\_8x8\_R50.pyth) |
| Slow     | R50   | \-       | 4x16                       | 72.40 | 90.18 | 27.55 x 3 x 10    | 32.45      | [link](https://dl.fbaipublicfiles.com/pytorchvideo/model_zoo/kinetics/SLOW\_4x16\_R50.pyth) |
| Slow     | R50   | \-       | 8x8                        | 74.58 | 91.63 | 54.52 x 3 x 10    | 32.45      | [link](https://dl.fbaipublicfiles.com/pytorchvideo/model_zoo/kinetics/SLOW\_8x8\_R50.pyth) |
| SlowFast | R50   | \-       | 4x16                       | 75.34 | 91.89 | 36.69 x 3 x 10    | 34.48      | [link](https://dl.fbaipublicfiles.com/pytorchvideo/model_zoo/kinetics/SLOWFAST\_4x16\_R50.pyth) |
| SlowFast | R50   | \-       | 8x8                        | 76.94 | 92.69 | 65.71 x 3 x 10    | 34.57      | [link](https://dl.fbaipublicfiles.com/pytorchvideo/model_zoo/kinetics/SLOWFAST\_8x8\_R50.pyth) |
| SlowFast | R101  | \-       | 8x8                        | 77.90 | 93.27 | 127.20 x 3 x 10   | 62.83      | [link](https://dl.fbaipublicfiles.com/pytorchvideo/model_zoo/kinetics/SLOWFAST\_8x8\_R101.pyth) |
| SlowFast | R101  | \-       | 16x8                       | 78.70 | 93.61 | 215.61 x 3 x 10   | 53.77      | [link](https://dl.fbaipublicfiles.com/pytorchvideo/model_zoo/kinetics/SLOWFAST\_16x8\_R101_50_50.pyth) |
| CSN      | R101  | \-       | 32x2                       | 77.00 | 92.90 | 75.62 x 3 x 10    | 22.21      | [link](https://dl.fbaipublicfiles.com/pytorchvideo/model_zoo/kinetics/CSN\_32x2\_R101.pyth) |
| R(2+1)D  | R50   | \-       | 16x4                       | 76.01 | 92.23 | 76.45 x 3 x 10    | 28.11      | [link](https://dl.fbaipublicfiles.com/pytorchvideo/model_zoo/kinetics/R2PLUS1D\_16x4\_R50.pyth) |
| X3D      | XS    | \-       | 4x12                       | 69.12 | 88.63 | 0.91 x 3 x 10     | 3.79       | [link](https://dl.fbaipublicfiles.com/pytorchvideo/model_zoo/kinetics/X3D\_XS.pyth) |
| X3D      | S     | \-       | 13x6                       | 73.33 | 91.27 | 2.96 x 3 x 10     | 3.79       | [link](https://dl.fbaipublicfiles.com/pytorchvideo/model_zoo/kinetics/X3D\_S.pyth) |
| X3D      | M     | \-       | 16x5                       | 75.94 | 92.72 | 6.72 x 3 x 10     | 3.79       | [link](https://dl.fbaipublicfiles.com/pytorchvideo/model_zoo/kinetics/X3D\_M.pyth) |
| X3D      | L     | \-       | 16x5                       | 77.44 | 93.31 | 26.64 x 3 x 10    | 6.15       | [link](https://dl.fbaipublicfiles.com/pytorchvideo/model_zoo/kinetics/X3D\_L.pyth) |
| MViT     | B     | \-       | 16x4                       | 78.85 | 93.85 | 70.80 x 1 x 5     | 36.61      | [link](https://dl.fbaipublicfiles.com/pytorchvideo/model_zoo/kinetics/MVIT\_B\_16x4.pyth) |
| MViT     | B     | \-       | 32x3                       | 80.30 | 94.69 | 170.37 x 1 x 5    | 36.61      | [link](https://dl.fbaipublicfiles.com/pytorchvideo/model_zoo/kinetics/MVIT\_B\_32x3\_f294077834.pyth) |

- Something-Something V2

| arch     | depth | pretrain     | frame length x sample rate | top 1 | top 5 | Flops (G) x views | Params (M) | Model                                                        |
| -------- | ----- | ------------ | -------------------------- | ----- | ----- | ----------------- | ---------- | ------------------------------------------------------------ |
| Slow     | R50   | Kinetics 400 | 8x8                        | 60.04 | 85.19 | 55.10 x 3 x 1     | 31.96      | [link](https://dl.fbaipublicfiles.com/pytorchvideo/model_zoo/ssv2/SLOW\_8x8\_R50.pyth) |
| SlowFast | R50   | Kinetics 400 | 8x8                        | 61.68 | 86.92 | 66.60 x 3 x 1     | 34.04      | [link](https://dl.fbaipublicfiles.com/pytorchvideo/model_zoo/ssv2/SLOWFAST\_8x8\_R50.pyth) |

- Charades

| arch     | depth | pretrain     | frame length x sample rate | MAP   | Flops (G) x views | Params (M) | Model                                                        |
| -------- | ----- | ------------ | -------------------------- | ----- | ----------------- | ---------- | ------------------------------------------------------------ |
| Slow     | R50   | Kinetics 400 | 8x8                        | 34.72 | 55.10 x 3 x 10    | 31.96      | [link](https://dl.fbaipublicfiles.com/pytorchvideo/model_zoo/charades/SLOW\_8x8\_R50.pyth) |
| SlowFast | R50   | Kinetics 400 | 8x8                        | 37.24 | 66.60 x 3 x 10    | 34.00      | [link](https://dl.fbaipublicfiles.com/pytorchvideo/model_zoo/charades/SLOWFAST\_8x8\_R50.pyth) |

- AVA (V2.2)

| arch     | depth | pretrain     | frame length x sample rate | MAP   | Params (M) | Model                                                        |
| -------- | ----- | ------------ | -------------------------- | ----- | ---------- | ------------------------------------------------------------ |
| Slow     | R50   | Kinetics 400 | 4x16                       | 19.5  | 31.78      | [link](https://dl.fbaipublicfiles.com/pytorchvideo/model_zoo/ava/SLOW\_4x16\_R50\_DETECTION.pyth) |
| SlowFast | R50   | Kinetics 400 | 8x8                        | 24.67 | 33.82      | [link](https://dl.fbaipublicfiles.com/pytorchvideo/model_zoo/ava/SLOWFAST\_8x8\_R50\_DETECTION.pyth) |



#### 8.3.4 使用 PyTorchVideo model zoo

PyTorchVideo提供了三种使用方法，并且给每一种都配备了`tutorial`

* TorchHub，这些模型都已经在TorchHub存在。我们可以根据实际情况来选择需不需要使用预训练模型。除此之外，官方也给出了TorchHub使用的 [tutorial](https://pytorchvideo.org/docs/tutorial_torchhub_inference) 。
* PySlowFast，使用 [PySlowFast workflow](https://github.com/facebookresearch/SlowFast/) 去训练或测试PyTorchVideo models/datasets.
* [PyTorch Lightning](https://github.com/PyTorchLightning/pytorch-lightning)建立一个工作流进行处理，点击查看官方 [tutorial](https://pytorchvideo.org/docs/tutorial_classification)。

- 如果想查看更多的使用教程，可以点击 [这里](https://github.com/facebookresearch/pytorchvideo/tree/main/tutorials) 进行尝试

总的来说，PyTorchVideo的使用与torchvision的使用方法类似，在有了前面的学习基础上，我们可以很快上手PyTorchVideo，具体的我们可以通过查看官方提供的文档和一些例程来了解使用方法：[官方网址](https://pytorchvideo.readthedocs.io/en/latest/index.html)




## 8.4 torchtext

本节我们来介绍PyTorch官方用于自然语言处理（NLP）的工具包torchtext。自然语言处理也是深度学习的一大应用场景，近年来随着大规模预训练模型的应用，深度学习在人机对话、机器翻译等领域的取得了非常好的效果，也使得NLP相关的深度学习模型获得了越来越多的关注。

由于NLP和CV在数据预处理中的不同，因此NLP的工具包torchtext和torchvision等CV相关工具包也有一些功能上的差异，如：

- 数据集（dataset）定义方式不同
- 数据预处理工具
- 没有琳琅满目的model zoo

本节介绍参考了[atnlp的Github](https://github.com/atnlp/torchtext-summary)，在此致谢！



### 8.4.1 torchtext的主要组成部分

torchtext可以方便的对文本进行预处理，例如截断补长、构建词表等。torchtext主要包含了以下的主要组成部分：

- 数据处理工具 torchtext.data.functional、torchtext.data.utils
- 数据集 torchtext.data.datasets
- 词表工具 torchtext.vocab
- 评测指标 torchtext.metrics



### 8.4.2 torchtext的安装

torchtext可以直接使用pip进行安装：

```bash
pip install torchtext
```



### 8.4.3 构建数据集

- **Field及其使用**

Field是torchtext中定义数据类型以及转换为张量的指令。`torchtext` 认为一个样本是由多个字段（文本字段，标签字段）组成，不同的字段可能会有不同的处理方式，所以才会有 `Field` 抽象。定义Field对象是为了明确如何处理不同类型的数据，但具体的处理则是在Dataset中完成的。下面我们通过一个例子来简要说明一下Field的使用：

```python
tokenize = lambda x: x.split()
TEXT = data.Field(sequential=True, tokenize=tokenize, lower=True, fix_length=200)
LABEL = data.Field(sequential=False, use_vocab=False)
```

其中：

​	sequential设置数据是否是顺序表示的；

​	tokenize用于设置将字符串标记为顺序实例的函数

​	lower设置是否将字符串全部转为小写；

​	fix_length设置此字段所有实例都将填充到一个固定的长度，方便后续处理；

​	use_vocab设置是否引入Vocab object，如果为False，则需要保证之后输入field中的data都是numerical的

构建Field完成后就可以进一步构建dataset了：

```python
from torchtext import data
def get_dataset(csv_data, text_field, label_field, test=False):
    fields = [("id", None), # we won't be needing the id, so we pass in None as the field
                 ("comment_text", text_field), ("toxic", label_field)]       
    examples = []

    if test:
        # 如果为测试集，则不加载label
        for text in tqdm(csv_data['comment_text']):
            examples.append(data.Example.fromlist([None, text, None], fields))
    else:
        for text, label in tqdm(zip(csv_data['comment_text'], csv_data['toxic'])):
            examples.append(data.Example.fromlist([None, text, label], fields))
    return examples, fields
```

这里使用数据csv_data中有"comment_text"和"toxic"两列，分别对应text和label。

```python
train_data = pd.read_csv('train_toxic_comments.csv')
valid_data = pd.read_csv('valid_toxic_comments.csv')
test_data = pd.read_csv("test_toxic_comments.csv")
TEXT = data.Field(sequential=True, tokenize=tokenize, lower=True)
LABEL = data.Field(sequential=False, use_vocab=False)

# 得到构建Dataset所需的examples和fields
train_examples, train_fields = get_dataset(train_data, TEXT, LABEL)
valid_examples, valid_fields = get_dataset(valid_data, TEXT, LABEL)
test_examples, test_fields = get_dataset(test_data, TEXT, None, test=True)
# 构建Dataset数据集
train = data.Dataset(train_examples, train_fields)
valid = data.Dataset(valid_examples, valid_fields)
test = data.Dataset(test_examples, test_fields)
```

可以看到，定义Field对象完成后，通过get_dataset函数可以读入数据的文本和标签，将二者（examples）连同field一起送到torchtext.data.Dataset类中，即可完成数据集的构建。使用以下命令可以看下读入的数据情况：

```python
# 检查keys是否正确
print(train[0].__dict__.keys())
print(test[0].__dict__.keys())
# 抽查内容是否正确
print(train[0].comment_text)
```

- **词汇表（vocab）**

在NLP中，将字符串形式的词语（word）转变为数字形式的向量表示（embedding）是非常重要的一步，被称为Word Embedding。这一步的基本思想是收集一个比较大的语料库（尽量与所做的任务相关），在语料库中使用word2vec之类的方法构建词语到向量（或数字）的映射关系，之后将这一映射关系应用于当前的任务，将句子中的词语转为向量表示。

在torchtext中可以使用Field自带的build_vocab函数完成词汇表构建。

```python
TEXT.build_vocab(train)
```

- **数据迭代器**

其实就是torchtext中的DataLoader，看下代码就明白了：

```python
from torchtext.data import Iterator, BucketIterator
# 若只针对训练集构造迭代器
# train_iter = data.BucketIterator(dataset=train, batch_size=8, shuffle=True, sort_within_batch=False, repeat=False)

# 同时对训练集和验证集进行迭代器的构建
train_iter, val_iter = BucketIterator.splits(
        (train, valid), # 构建数据集所需的数据集
        batch_sizes=(8, 8),
        device=-1, # 如果使用gpu，此处将-1更换为GPU的编号
        sort_key=lambda x: len(x.comment_text), # the BucketIterator needs to be told what function it should use to group the data.
        sort_within_batch=False
)

test_iter = Iterator(test, batch_size=8, device=-1, sort=False, sort_within_batch=False)
```

torchtext支持只对一个dataset和同时对多个dataset构建数据迭代器。

- **使用自带数据集**

与torchvision类似，torchtext也提供若干常用的数据集方便快速进行算法测试。可以查看[官方文档](https://pytorch.org/text/stable/datasets.html)寻找想要使用的数据集。



### 8.4.4 评测指标（metric）

NLP中部分任务的评测不是通过准确率等指标完成的，比如机器翻译任务常用BLEU (bilingual evaluation understudy) score来评价预测文本和标签文本之间的相似程度。torchtext中可以直接调用torchtext.data.metrics.bleu_score来快速实现BLEU，下面是一个官方文档中的一个例子：

```python
from torchtext.data.metrics import bleu_score
candidate_corpus = [['My', 'full', 'pytorch', 'test'], ['Another', 'Sentence']]
references_corpus = [[['My', 'full', 'pytorch', 'test'], ['Completely', 'Different']], [['No', 'Match']]]
bleu_score(candidate_corpus, references_corpus)
```

```
0.8408964276313782
```



### 8.4.5 其他

值得注意的是，由于NLP常用的网络结构比较固定，torchtext并不像torchvision那样提供一系列常用的网络结构。模型主要通过torch.nn中的模块来实现，比如torch.nn.LSTM、torch.nn.RNN等。



**备注：**

对于文本研究而言，当下Transformer已经成为了绝对的主流，因此PyTorch生态中的[HuggingFace](https://huggingface.co/)等工具包也受到了越来越广泛的关注。这里强烈建议读者自行探索相关内容，可以写下自己对于HuggingFace的笔记，如果总结全面的话欢迎pull request，充实我们的课程内容。





## 8.5 参考资料

- [torchtext官方文档](https://pytorch.org/text/stable/index.html)
- [Datawhale-深入浅出PyTorch](https://github.com/datawhalechina/thorough-pytorch)
