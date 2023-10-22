# 第5章 微调和引导
> **实现代码来自diffusion-models-class（中文）**：https://github.com/darcula1993/diffusion-models-class-CN  

基于现有模型实现改造的主要方法：

- 微调： 可以在新的数据集上重新训练已有的模型，以改变原有的输出类型
- 引导： 在推理阶段引导现有模型的生成过程，以获取额外的控制
- 条件生成：在训练过程中产生的额外信息，把这些信息输入到模型中进行预测，通过输入相关信息作为条件来控制模型的生成。

## 环境准备

1. 安装python库


```python
!pip install -qq diffusers datasets accelerate wandb open-clip-torch
```

2. 登录hugging Face Hub


```python
# token: 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
from huggingface_hub import notebook_login
notebook_login()
```

引入需要的库和计算设备



```python
import numpy as np 
import torch
import torch.nn.functional as F
import torchvision
from datasets import load_dataset
from diffusers import DDIMScheduler,DDPMPipeline
from matplotlib import pyplot as plt 
from PIL import Image
from torchvision import transforms
```


```python
from tqdm.auto import tqdm
device = (
    "mps"
    if torch.backends.mps.is_available()
    else "cuda"
    if torch.cuda.is_available()
    else "cpu"
)
```

## 载入训练过的管线

首先载入一个现有的管线，看看能用它做些什么。


```python
_pipe = "google/ddpm-cecebahq-256"
image_pipe = DDPMPipeline.from_pretrained(_pipe)
image_pipe.to(device);
```


```python
images = image_pipe().images # 调用函数生成图片
images[0]  # 过程可能有点慢，请耐心等待
```

## DDIM - 更快的采样过程

生成图片过程中，每一步模型都会接收一个带噪声的输入，并且预测这个噪声，以此估算没有噪声的完整图像。

Diffusers库通过调度器进行控制采样方法，每次更新由`step()`函数完成，最后，将返回的输出命名为`pre_sample`,其中，prev表示previous,在时间上是倒退的，整个过程是从高噪声到低噪声（与前向扩散过程相反）。


载入调度器 DDIMScheduler （论文“[Denoising Diffusion Implicit
Models](https://arxiv.org/abs/2010.02502)”）,实现代码：



```python
# 创建一个新的调度器并设置推理迭代次数
scheduler = DDIMScheduler.from_pretrained(_pipe)
scheduler.set_timesteps(num_inference_steps=40)   

scheduler.timesteps 
```


```python
# 随机噪声
x = torch.randn(4, 3, 256, 256).to(device)
# batch_size=4，三通道，长宽均为256像素的一组图像
# 循环时间步
for i, t in tqdm(enumerate(scheduler.timesteps)):
    # 模型输入：给“带噪”图像加上时间步信息
    model_input = scheduler.scale_model_input(x, t)
    
    # 预测噪声
    with torch.no_grad():
        noise_pred = image_pipe.unet(model_input, t)["sample"]
    
    # 使用调度器计算更新后的样本
    scheduler_output = scheduler.step(noise_pred, t, x)

    # 更新输入图像
    x = scheduler_output.prev_sample
    
    # 时不时看一下输入图像和预测的“去噪”图像
    if i % 10 == 0 or i == len(scheduler.timesteps) - 1:
        fig, axs = plt.subplots(1, 2, figsize=(12, 5))

        grid = torchvision.utils.make_grid(x, nrow=4).permute(1, 2, 0)
        axs[0].imshow(grid.cpu().clip(-1, 1) * 0.5 + 0.5)
        axs[0].set_title(f"Current x (step {i})")

        pred_x0 = scheduler_output.pred_original_sample  
        grid = torchvision.utils.make_grid(pred_x0, nrow=4).permute(1, 2, 0)
        axs[1].imshow(grid.cpu().clip(-1, 1) * 0.5 + 0.5)
        axs[1].set_title(f"Predicted denoised images (step {i})")
        plt.show()

```

随着过程的推进，预测的输出逐步得到改善。通过新的调度器替换原有管线中的调度器，然后进行采用：


```python
image_pipe.sheduler = scheduler
images = image_pipe(num_inference_steps = 40).images
images[0]
```

**这里简单说一下DDIM:** :
DDIM和DDPM有相同的训练目标，但是它不再限制扩散过程必须是一个马尔卡夫链，这使得DDIM可以采用更小的采样步数来加速生成过程，DDIM的另外是一个特点是从一个随机噪音生成样本的过程是一个确定的过程（中间没有加入随机噪音）。

## 扩散模型之微调

### 实战：微调


```python
dataset_name = "huggan/smithsonian_butterflies_subset"
dataset = load_dataset(dataset_name,split="train")
image_size = 256
batch_size = 4
preprocess = transforms.Compose(
    [
        transforms.Resize((iamge_size,image_size)),
        transforms.RandomHorizontalFlip(),
        transforms.ToTensor(),
        transforms.Normalize([0,5],[0.5]),
    ]
)

def transform(examples):
    images = [preprocess(image.convert("RGB")) for image in 
             examples[image]]
    return {"images":images}

dataset.set_transform(transform)

train_dataloader =torch.utils.data.DataLoader(
    dataset,batch_size = batch_size,shuffle = True
)

print("Previewing batch:")
batch = next(iter(train_dataloader))
grid = torchvision.utils.make_grid(batch["image"],nrow=4)
plt.imshow(grid.permute(1, 2, 0).cpu().clip(-1, 1) * 0.5 + 0.5);

```


```python
需要考虑的4个额外因素：

额外因素1：适应GPU显存，需要权衡好batch size和图像尺寸
```


```python
num_epochs = 2
lr = 1e-5
grad_accumulation_steps = 2  

optimizer = torch.optim.AdamW(image_pipe.unet.parameters(), lr=lr)

losses = []

for epoch in range(num_epochs):
    for step, batch in tqdm(enumerate(train_dataloader), total=len(train_dataloader)):
        clean_images = batch["images"].to(device)
        # 随机生成一个噪声,稍后加到图像上
        noise = torch.randn(clean_images.shape).to(clean_images.device)
        bs = clean_images.shape[0]
        # 随机选取一个时间步
        timesteps = torch.randint(
            0,
            image_pipe.scheduler.conf.num_train_timesteps,
            (bs,),
            device=clean_images.device,
        ).long()
        
        # 根据选中的时间步和确定的幅值，添加噪声，并进行前向扩散过程
        
        noisy_images = image_pipe.scheduler.add_noise(clean_images, noise, timesteps)
        # 使用“带噪”图像进行网络预测
        noise_pred = image_pipe.unet(noisy_images, timesteps, return_dict=False)[0]

        # 对真正的噪声和预测的结果进行比较，注意这里是预测噪声
        loss = F.mse_loss(noise_pred, noise)

        # 保存损失值
        losses.append(loss.item())
        # 更新梯度
        loss.backward(loss)

        # 进行梯度累积，在累积到一定步数后更新模型参数 
        if (step + 1) % grad_accumulation_steps == 0:
            optimizer.step()
            optimizer.zero_grad()

    print(f"Epoch {epoch} average loss: {sum(losses[-len(train_dataloader):])/len(train_dataloader)}")

# 绘制损失曲线
plt.plot(losses)

```

额外因素2： 通过观测图，损失曲线跟噪声一样混乱，可以通过进行梯度累积（gradient accumulation），来得到与使用更大batch size一样的收益，又不会造成内存溢出。

具体做法：

多运行几次loss.backward()再调用optimizer.step() 和 optimizer.zero_grad() .

> 练习5-1：思考是否可以把梯度累积加到训练循环中呢？如果可以，具体该怎么做呢？如何基于梯度累积的步数调整学习率？学习率与之前一样吗？

额外因素3： 频率不足以及时反映我们的训练进展。因此为了更好地了解训练情况，我们应该采取以下两个步骤。
(1)在训练过程中，时不时生成一些图像样本，供我们检查模型性能。  
(2)在训练过程中，将损失值、生成的图像样本等信息记录到日志中，可使用Weights and Biases、TensorBoard等功能或工具。 

为了方便你了解训练效果，本书提供了一个快速的脚本程序，该脚本程序使用上述训练代码并加入了少量日志记录功能。

通过观察这些信息，你可以发现，尽管从损失值的角度看，训练似乎没有得到改进，但你可以看到一个从原有图像分布到新的数据集逐渐演变的过程。

> 练习5-2：尝试修改第4章的示例训练脚本程序。你可以使用预训练好的模型，而不是从头开始训练。对比一下这里提供的脚本程序，看看有哪些额外功能是这里的脚本程序所没有的。

接下来，我们可以使用模型生成一些图像样本：


```python
x = torch.randn(8, 3, 256, 256).to(device)
for i, t in tqdm(enumerate(scheduler.timesteps)):
    model_input = scheduler.scale_model_input(x, t)
    with torch.no_grad():
        noise_pred = image_pipe.unet(model_input, t)["sample"]
    x = scheduler.step(noise_pred, t, x).prev_sample
grid = torchvision.utils.make_grid(x, nrow=4)
plt.imshow(grid.permute(1, 2, 0).cpu().clip(-1, 1) * 0.5 + 0.5);

```

额外因素4：微调过程可能是难以预测的。如果训练时间很长，则我们有可能看到一些完美的蝴蝶图像，但模型的中间过程也非常有趣，特别是对于那些对不同艺术风格感兴趣的人来说！你还可以试着
短时间或长时间观察一下训练过程，并试着改变学习率，看看这会如何影响模型最终的输出

### 使用最小化实例程序来微调模型：

一个最小化示例程序，用于微调相关模型：


```python
## 下载微调用的脚本
!wget https://github.com/huggingface/diffusion-models￾class/raw/main/unit2/finetune_model.py
## 在终端运行脚本：在Vintage Face数据集上训练脚本
python finetune_model.py
 --image_size 128 --batch_size 8 --num_epochs 16 \
 --grad_accumulation_steps 2 --start_model "google/ddpm-celebahq-256" \
 --dataset_name "Norod78/Vintage-Faces-FFHQAligned" \
 --wandb_project 'dm-finetune' \
 --log_samples_every 100 --save_model_every 1000 \
 --model_save_name 'vintageface'
```

### 保存和载入微调过的管线


```python
image_pipe.save_pretrained("my-finetuned-model")
```

## 引导

使用LSUM bedrooms 数据集上训练并在wikiart数据集上进行一轮微调的新模型进行引导。


```python
# 加载一个预训练的管线
pipeline_name = "johnowhitaker/sd-class-wikiart-from-bedrooms"
image_pipe = DDPMPipeline.from_pretrained(pipeline_name).to(device)

# 使用DDIM调度器，用40步生成图片
scheduler = DDIMScheduler.from_pretrained(pipeline_name)
scheduler.set_timesteps(num_inference_steps=40)

# 从随机噪声开始
x = torch.randn(8, 3, 256, 256).to(device)

# 使用一个最简单的采样循环
for i, t in tqdm(enumerate(scheduler.timesteps)):
    model_input = scheduler.scale_model_input(x, t)
    with torch.no_grad():
        noise_pred = image_pipe.unet(model_input, t)["sample"]
    x = scheduler.step(noise_pred, t, x).prev_sample

# 生成图片
grid = torchvision.utils.make_grid(x, nrow=4)
plt.imshow(grid.permute(1, 2, 0).cpu().clip(-1, 1) * 0.5 + 0.5);

```

需要引导的几种情况：

1. 在一个很小的数据集上微调文本条件模型，希望模型尽可能保留其原始训练所学习的内容，以便能够理解数据集中未涵盖的各种文本提示语。同时，希望它能适应我们的数据集，以便生成的内容与原有的数据风格一致，需要使用很小的学习率并对模型执行指数平均操作。

2. 可能需要重新训练一个模型以适应新的数据集，需要使用较大的学习率并进行长时间的训练。


### 实战：引导

如果想要对生成的样本施加控制，该怎么做呢？如果想让生成的图片偏向于靠近某种颜色，又该怎么做呢？这时我们可以利用引导(guidance)，在采样过程中施加额外的控制。

首先，创建一个函数，用于定义希望优化的指标（损失值）。


```python
def color_loss(images, target_color=(0.1, 0.9, 0.5)):
    """给定一个RGB值，返回一个损失值，用于衡量图片的像素值与目标颜色之差"""
    # 归一化
    target = torch.tensor(target_color).to(images.device) * 2 - 1  
    # 将目标张量的形状改未(b, c, h, w)
    target = target[None, :, None, None]  
    # 计算图片的像素值以及目标颜色的均方误差
    error = torch.abs(images - target).mean()  
    return error
```

接下来，需要修改采样循环并执行以下操作：

(1)创建新的输入图像$x$，将它的requires_grad属性设置为True。  
(2)计算“去噪”后的图像$x_0$。  
(3)将“去噪”后的图像$x_0$传递给损失函数。  
(4)计算损失函数对输入图像$x$的梯度。  
(5)在使用调度器之前，先用计算出来的梯度修改输入图像$x$，使输入图像$x$朝着减少损失值的方向改进。  

实现方法有两种：

**方法1：** 从UNet中获取噪声预测，将其设置为输入图像x的requires_grad属性，可以更高效地使用内存。缺点是导致梯度的精度降低。


```python

# 用于决定引导的强度有多大，可设置5~100之间的数
guidance_loss_scale = 40  

x = torch.randn(8, 3, 256, 256).to(device)

for i, t in tqdm(enumerate(scheduler.timesteps)):

    model_input = scheduler.scale_model_input(x, t)

    with torch.no_grad():
        noise_pred = image_pipe.unet(model_input, t)["sample"]

    x = x.detach().requires_grad_()
    
    # 得到去噪后的图像
    x0 = scheduler.step(noise_pred, t, x).pred_original_sample

    loss = color_loss(x0) * guidance_loss_scale
    if i % 10 == 0:
        print(i, "loss:", loss.item())
    
    # 获取梯度
    cond_grad = -torch.autograd.grad(loss, x)[0]
    # 梯度更新x
    x = x.detach() + cond_grad
    # 使用调度器更新x
    x = scheduler.step(noise_pred, t, x).prev_sample

grid = torchvision.utils.make_grid(x, nrow=4)
im = grid.permute(1, 2, 0).cpu().clip(-1, 1) * 0.5 + 0.5
Image.fromarray(np.array(im * 255).astype(np.uint8))

```

方法2：先将输入图像x
x的requires_grad属性设置为True，然后传递给UNet并计算“去噪”后的图像$x_0$


```python
guidance_loss_scale = 40
x = torch.randn(4, 3, 256, 256).to(device)

for i, t in tqdm(enumerate(scheduler.timesteps)):
    # 设置requires_grad
    x = x.detach().requires_grad_()
    model_input = scheduler.scale_model_input(x, t)
    # 预测
    noise_pred = image_pipe.unet(model_input, t)["sample"]
    # 得到“去噪”后的图像
    x0 = scheduler.step(noise_pred, t, x).pred_original_sample

    loss = color_loss(x0) * guidance_loss_scale
    if i % 10 == 0:
        print(i, "loss:", loss.item())
    # 获取梯度
    cond_grad = -torch.autograd.grad(loss, x)[0]
    # 更新x
    x = x.detach() + cond_grad
    # 使用调度器更新x
    x = scheduler.step(noise_pred, t, x).prev_sample

grid = torchvision.utils.make_grid(x, nrow=4)
im = grid.permute(1, 2, 0).cpu().clip(-1, 1) * 0.5 + 0.5
Image.fromarray(np.array(im * 255).astype(np.uint8))

```

第二种方法对GPU显存的要求更高了，但更接近于训练模型所使用的数据。也可以通过增大guidance_loss_scale来增强颜色迁移的效果。

> 练习5-3：选出你最喜欢的颜色并找出相应的RGB值，然后修改上述代码中的color_loss()函数，将目标颜色改成你最喜欢的颜色并检查输出。观察输出和你预期的结果匹配吗？

###  CLIP引导

CLIP是一个由OpenAI开发的模型，它使得我们能够对图片和文字说明进行比较

基本流程：

对文本提示语进行embedding，为 CLIP 获取一个512维的embedding。
在扩散模型的生成过程中的每一步进行如下操作：
- 制作多个不同版本的预测出来的“去噪”图片。
- 对预测出来的每一张“去噪”图片，用CLIP给图片做embedding，并对图片和文字的embedding做对比。
- 计算损失对于当前“带噪”的输入x的梯度，在使用调度器更新x之前先用这个梯度修改它。


```python
import open_clip

clip_model, _, preprocess = open_clip.create_model_and_transforms("ViT-B-32", pretrained="openai")
clip_model.to(device)

tfms = torchvision.transforms.Compose(
    [
        torchvision.transforms.RandomResizedCrop(224), 
        torchvision.transforms.RandomAffine(5),  
        torchvision.transforms.RandomHorizontalFlip(),  
        torchvision.transforms.Normalize(
            mean=(0.48145466, 0.4578275, 0.40821073),
            std=(0.26862954, 0.26130258, 0.27577711),
        ),
    ]
)

# 定义一个损失函数，用于获取图片的特征，然后与提示文字的特征进行对比
def clip_loss(image, text_features):
    image_features = clip_model.encode_image(
        tfms(image)
    )  # Note: applies the above transforms
    input_normed = torch.nn.functional.normalize(image_features.unsqueeze(1), dim=2)
    embed_normed = torch.nn.functional.normalize(text_features.unsqueeze(0), dim=2)
    dists = (
        input_normed.sub(embed_normed).norm(dim=2).div(2).arcsin().pow(2).mul(2)
    )  # Squared Great Circle Distance
    return dists.mean()

prompt = "Red Rose (still life), red flower painting"

guidance_scale = 8  
n_cuts = 4  

scheduler.set_timesteps(50)

# 使用CLIP从提示文字中提取特征
text = open_clip.tokenize([prompt]).to(device)
with torch.no_grad(), torch.cuda.amp.autocast():
    text_features = clip_model.encode_text(text)


x = torch.randn(4, 3, 256, 256).to(device)

for i, t in tqdm(enumerate(scheduler.timesteps)):

    model_input = scheduler.scale_model_input(x, t)

    with torch.no_grad():
        noise_pred = image_pipe.unet(model_input, t)["sample"]

    cond_grad = 0

    for cut in range(n_cuts):

        x = x.detach().requires_grad_()
        # 获取“去噪”后的图像
        x0 = scheduler.step(noise_pred, t, x).pred_original_sample

        loss = clip_loss(x0, text_features) * guidance_scale
        # 获取梯度并使用n_cuts平均
        cond_grad -= torch.autograd.grad(loss, x)[0] / n_cuts

    if i % 25 == 0:
        print("Step:", i, ", Guidance loss:", loss.item())

    alpha_bar = scheduler.alphas_cumprod[i]
    x = x.detach() + cond_grad * alpha_bar.sqrt()

    x = scheduler.step(noise_pred, t, x).prev_sample


grid = torchvision.utils.make_grid(x.detach(), nrow=4)
im = grid.permute(1, 2, 0).cpu().clip(-1, 1) * 0.5 + 0.5
Image.fromarray(np.array(im * 255).astype(np.uint8))


```


```python
plt.plot([1 for a in scheduler.alphas_cumprod], label="no
scaling")
plt.plot([a for a in scheduler.alphas_cumprod],
label="alpha_bar")
plt.plot([a.sqrt() for a in scheduler.alphas_cumprod],
 label="alpha_bar.sqrt()")
plt.plot(
 [(1 - a).sqrt() for a in scheduler.alphas_cumprod], label="
(1-
 alpha_bar).sqrt()"
)
plt.legend()
```

> 如需分享你的自定义采样训练，可以关注扩展工具gradio的使用 

## 实战：创建一个类别条件扩散模型

### 1. 配置和数据准备


```python
import torch
import torchvision
from torch import nn
from torch.nn import functional as F
from torch.utils.data import DataLoader
from diffusers import DDPMScheduler, UNet2DModel
from matplotlib import pyplot as plt
from tqdm.auto import tqdm

device = 'cuda' if torch.cuda.is_available() else 'cpu'
print(f'Using device: {device}')

```


```python
# 加载MNIST数据集
dataset = torchvision.datasets.MNIST(root="./data/mnist/", train=True, 
                                     download=True, 
                                     transform=torchvision.transforms.ToTensor())

train_dataloader = DataLoader(dataset, batch_size=8, shuffle=True)

x, y = next(iter(train_dataloader))
print('Input shape:', x.shape)
print('Labels:', y)
plt.imshow(torchvision.utils.make_grid(x)[0], cmap='Greys');

```

### 2. 创建一个以类别为条件的UNet模型


输入类别的流程：

1. 创建一个标准的UNet2DModel，加入一些额外的输入通道。
2. 通过一个嵌入层，把类别标签映射到一个长度为class_emb_size的特征向量上。
3. 把这个信息作为额外通道和原有的输入向量拼接起来。
4. 将net_input（其中包含class_emb_size + 1个通道）输入UNet模型，得到最终的预测结果。


```python
class ClassConditionedUnet(nn.Module):
    def __init__(self, num_classes=10, class_emb_size=4):
        super().__init__()
        
        self.class_emb = nn.Embedding(num_classes, class_emb_size)

        self.model = UNet2DModel(
            sample_size=28,           
            in_channels=1 + class_emb_size, # 加入额外的输入通道
            out_channels=1,           # 输出结果的通道数
            layers_per_block=2,       # 残差层个数
            block_out_channels=(32, 64, 64), 
            down_block_types=( 
                "DownBlock2D",        # 下采样模块
                "AttnDownBlock2D",    # 含有spatil self-attention的ResNet下采样模块
                "AttnDownBlock2D",
            ), 
            up_block_types=(
                "AttnUpBlock2D", 
                "AttnUpBlock2D",      # 含有spatil self-attention的ResNet上采样模块
                "UpBlock2D",          # 上采样模块
              ),
        )

    def forward(self, x, t, class_labels):
        bs, ch, w, h = x.shape
        # 类别条件将会以额外通道的形式输入
        class_cond = self.class_emb(class_labels) 
        class_cond = class_cond.view(bs, class_cond.shape[1], 1, 1).expand(bs, class_cond.shape[1], w, h)

        net_input = torch.cat((x, class_cond), 1) # (bs, 5, 28, 28)

        return self.model(net_input, t).sample # (bs, 1, 28, 28)

```

###  3.训练和采样


```python
noise_scheduler = DDPMScheduler(num_train_timesteps=1000, beta_schedule='squaredcos_cap_v2')

train_dataloader = DataLoader(dataset, batch_size=128, shuffle=True)

n_epochs = 10

net = ClassConditionedUnet().to(device)

loss_fn = nn.MSELoss()

opt = torch.optim.Adam(net.parameters(), lr=1e-3) 

losses = []

for epoch in range(n_epochs):
    for x, y in tqdm(train_dataloader):
        
        x = x.to(device) * 2 - 1 
        y = y.to(device)
        noise = torch.randn_like(x)
        timesteps = torch.randint(0, 999, (x.shape[0],)).long().to(device)
        noisy_x = noise_scheduler.add_noise(x, noise, timesteps)

        pred = net(noisy_x, timesteps, y) 

        loss = loss_fn(pred, noise) 

        opt.zero_grad()
        loss.backward()
        opt.step()

        losses.append(loss.item())

    avg_loss = sum(losses[-100:])/100
    print(f'Finished epoch {epoch}. Average of the last 100 loss values: {avg_loss:05f}')

plt.plot(losses)

```


```python
# 准备一个随机噪声作为起点，并准备想要的图片标签
x = torch.randn(80, 1, 28, 28).to(device)
y = torch.tensor([[i]*8 for i in range(10)]).flatten().to(device)

# 循环采样
for i, t in tqdm(enumerate(noise_scheduler.timesteps)):

    with torch.no_grad():
        residual = net(x, t, y)

    x = noise_scheduler.step(residual, t, x).prev_sample

fig, ax = plt.subplots(1, 1, figsize=(12, 12))
ax.imshow(torchvision.utils.make_grid(x.detach().cpu().clip(-1, 1), nrow=8)[0], cmap='Greys')

```

> 练习5-4（选做）：采用同样的方法在FashionMNIST数据集上进行尝试，调节学习率、batch size和训练周期数。看你能否使用比上面的示例更少的训练时间，最终得到一些看起来不错的与时尚相关的图片吗？


```python

```

## 参考资料

[1].[扩散模型之DDIM](https://zhuanlan.zhihu.com/p/565698027)


```python

```
