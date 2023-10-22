# PyTorch简介和安装
（本学习笔记来源于[DataWhale-深入浅出PyTorch](https://github.com/datawhalechina/thorough_pytorch)）
## PyTorch简介

### 1.1.1 PyTorch的介绍

PyTorch是由Facebook人工智能研究小组开发的一种基于Lua编写的Torch库的Python实现的深度学习库，目前被广泛应用于学术界和工业界，而随着Caffe2项目并入Pytorch， Pytorch开始影响到TensorFlow在深度学习应用框架领域的地位。总的来说，PyTorch是当前难得的简洁优雅且高效快速的框架。因此本课程我们选择了PyTorch来进行开源学习。

### 1.1.2 PyTorch的优势

##### PyTorch有着下面的优势：

+ **更加简洁**，相比于其他的框架，PyTorch的框架更加简洁，易于理解。PyTorch的设计追求最少的封装，避免重复造轮子。
+ **上手快**，掌握numpy和基本的深度学习知识就可以上手。
+ PyTorch有着**良好的文档和社区支持**，作者亲自维护的论坛供用户交流和求教问题。Facebook 人工智能研究院对PyTorch提供了强力支持，作为当今排名前三的深度学习研究机构，FAIR的支持足以确保PyTorch获得持续的开发更新。
+ **项目开源**，在Github上有越来越多的开源代码是使用PyTorch进行开发。
+ 可以**更好的调试代码**，PyTorch可以让我们逐行执行我们的脚本。这就像调试NumPy一样 – 我们可以轻松访问代码中的所有对象，并且可以使用打印语句（或其他标准的Python调试）来查看方法失败的位置。
+ 越来越完善的扩展库，活力旺盛，正处在**当打之年**。

## PyTorch安装

PyTorch的安装，一般常见的是**Anaconda/miniconda+Pytorch**+ (Pycharm) 的工具，我们的安装分为以下几步

1. Anaconda的安装
2. 检查有无NVIDIA GPU
3. PyTorch的安装
4. Pycharm的安装 ( Windows系统上更为常用）

### 1.2.1 Anaconda的安装

**Step 1**：登陆[Anaconda | Individual Edition](https://www.anaconda.com/products/individual)，选择相应系统DownLoad，具体安装详见官方文档。

**Step 2**：安装好Anaconda后，我们项目创建虚拟环境`Pytorch38`，Linux在终端(`Ctrl`+`Alt`+`T`)进行，Windows在`Anaconda Prompt`或者`cmd`进行,相关命令：

```md
conda env list # 检查本地已创建的虚拟环境
conda create -n Pytorch38 python==3.8 #创建新的虚拟环境
conda remove -n Pytorch38 --all  # 删除虚拟环境
conda activate Pytorch38  #为本激活虚拟环境
```

**Step 3**：Anaconda换源(可选)

1、文件管理器文件路径地址栏敲：`%APPDATA%` 回车，快速进入 `C:\Users\电脑用户\AppData\Roaming` 文件夹中
2、新建 pip 文件夹并在文件夹中新建 `pip.ini` 配置文件
3、我们需要在pip.ini 配置文件内容，你可以选择使用记事本打开，输入以下内容，输入完后记得按下ctrl+s保存哦，在这里我们使用的是豆瓣源

```md
[global]
index-url = http://pypi.douban.com/simple
[install]
use-mirrors =true
mirrors =http://pypi.douban.com/simple/
trusted-host =pypi.douban.com
```
**conda换源**（换成清华源）[官方换源帮助](https://mirrors.tuna.tsinghua.edu.cn/help/anaconda/)

### 1.2.2 查看自己的显卡（CPU或者集显的小伙伴们可以跳过该部分）

在`cmd/terminal中`输入`nvidia-smi`（Linux和Win命令一样）、使用NVIDIA控制面板或者使用任务管理器查看自己是否有NVIDIA的独立显卡及其型号.

### 1.2.3 安装 PyTorch

1. 先查看cuda安装有没有问题：`nvcc -V`
2. 登录官网[Pytorch官网](https://pytorch.org/) 或者根据版本执行下面的命令
```md
# CUDA 10.2
conda install pytorch==1.9.0 torchvision==0.10.0 torchaudio==0.9.0 cudatoolkit=10.2 -c pytorch

# CUDA 11.3
conda install pytorch==1.9.0 torchvision==0.10.0 torchaudio==0.9.0 cudatoolkit=11.3 -c pytorch -c conda-forge

# CPU Only
conda install pytorch==1.9.0 torchvision==0.10.0 torchaudio==0.9.0 cpuonly -c pytorch
```
注意下一定要保持Pytorch和cudatoolkit的版本适配。[查看](https://pytorch.org/get-started/previous-versions/),本机版本为：


### 1.2.4 检验本地环境是否安装成功

进入所在的**虚拟环境**`conda activate Pytorch38 `，紧接着输入`python`，在输入下面的代码。

```shell
>>> import torch                                                      
>>> torch.cuda.is_available()
True
```
到此环境安装成功！

### 1.2.5 jupyter notebook添加指定环境

```shell
pip install ipykernel
python -m ipykernel install --name Pytorch38
```
(Pytorch38换成你自己的虚拟环境名字)


