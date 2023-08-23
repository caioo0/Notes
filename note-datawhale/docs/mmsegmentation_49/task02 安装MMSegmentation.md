# task02:安装MMSegmentation



## 1. Pytorch环境

**步骤 1.** 创建一个 conda 环境，并激活

```
conda create --name openmmlab python=3.8 -y
conda activate openmmlab
```

**Step 2.** 参考 [official instructions](https://pytorch.org/get-started/locally/) 安装 PyTorch

```
pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

## 2. 用MIM安装MMCV

```
pip install -U openmim
mim install mmengine
mim install mmcv
```

## 3. 安装mmsegmentation

```
git clone https://github.com/open-mmlab/mmsegmentation.git -b v1.1.0
cd mmsegmentation
!pip install -v -e .
```

## 4. 检测环境成功

```
# 检查 Pytorch
import torch, torchvision
print('Pytorch 版本', torch.__version__)
print('CUDA 是否可用',torch.cuda.is_available())

# 检查 mmcv
import mmcv
from mmcv.ops import get_compiling_cuda_version, get_compiler_version
print('MMCV版本', mmcv.__version__)
print('CUDA版本', mmcv.ops.get_compiling_cuda_version())
print('编译器版本', get_compiler_version())

# 检查 mmsegmentation
import mmseg
from mmseg.utils import register_all_modules
from mmseg.apis import inference_model, init_model
print('mmsegmentation版本', mmseg.__version__)
```

结果显示：

```
Pytorch 版本 2.0.1+cu118
CUDA 是否可用 True
MMCV版本 2.0.1
CUDA版本 11.8
编译器版本 MSVC 192930148
mmsegmentation版本 1.1.1
```

### 官方文档测试案例

为了验证 MMSegmentation 是否正确安装，我们提供了一些示例代码来运行一个推理 demo 。

**步骤 1.** 下载配置文件和模型文件

```
mim download mmsegmentation --config pspnet_r50-d8_4xb2-40k_cityscapes-512x1024 --dest .
```



该下载过程可能需要花费几分钟，这取决于您的网络环境。当下载结束，您将看到以下两个文件在您当前工作目录：`pspnet_r50-d8_4xb2-40k_cityscapes-512x1024.py` 和 `pspnet_r50-d8_512x1024_40k_cityscapes_20200605_003338-2966598c.pth`

**步骤 2.** 验证推理 demo

选项 (a). 如果您通过源码安装了 mmsegmentation，运行以下命令即可：

```
python demo/image_demo.py demo/demo.png configs/pspnet/pspnet_r50-d8_4xb2-40k_cityscapes-512x1024.py pspnet_r50-d8_512x1024_40k_cityscapes_20200605_003338-2966598c.pth --device cuda:0 --out-file result.jpg
```



您将在当前文件夹中看到一个新图像 `result.jpg`，其中所有目标都覆盖了分割 mask

选项 (b). 如果您通过 pip 安装 mmsegmentation, 打开您的 python 解释器，复制粘贴以下代码：

```
from mmseg.apis import inference_model, init_model, show_result_pyplot
import mmcv

config_file = 'pspnet_r50-d8_4xb2-40k_cityscapes-512x1024.py'
checkpoint_file = 'pspnet_r50-d8_512x1024_40k_cityscapes_20200605_003338-2966598c.pth'

# 根据配置文件和模型文件建立模型
model = init_model(config_file, checkpoint_file, device='cuda:0')

# 在单张图像上测试并可视化
img = 'demo/demo.png'  # or img = mmcv.imread(img), 这样仅需下载一次
result = inference_model(model, img)
# 在新的窗口可视化结果
show_result_pyplot(model, img, result, show=True)
# 或者将可视化结果保存到图像文件夹中
# 您可以修改分割 map 的透明度 (0, 1].
show_result_pyplot(model, img, result, show=True, out_file='result.jpg', opacity=0.5)
# 在一段视频上测试并可视化分割结果
video = mmcv.VideoReader('video.mp4')
for frame in video:
   result = inference_segmentor(model, frame)
   show_result_pyplot(model, result, wait_time=1)
```

结果如下：

![image-20230815163729894](.\img\image-20230815163729894.png)

## 参考

[mmesgmentation 官方文档 ](https://mmsegmentation.readthedocs.io/zh_CN/latest/get_started.html)