# DDIM 反转
---
### 本章知识点

- DDIM采样的工作原理
- 确定性采样和随机性采样的比较
- DDIM反转的理论支持
- 使用反转来编辑图像

## 实战：反转

### 配置

首先安装所需的库并且配置环境，代码如下：


```python
!pip install -q transformers diffusers accelerate
```


```python
!pip install -q chardet
```


```python
import torch
import requests
import torch.nn as nn
import torch.nn.functional as F
from PIL import Image
from io import BytesIO
from tqdm.auto import tqdm
from matplotlib import pyplot as plt
from torchvision import transforms as tfms
from diffusers import StableDiffusionPipeline, DDIMScheduler

```


```python
def load_image(url, size=None):
    response = requests.get(url,timeout=1)
    img = Image.open(BytesIO(response.content)).convert('RGB')
    if size is not None:
        img = img.resize(size)
    return img

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
```

## 载入一个预训练过的管线

首先：使用stable diffusion pipeline加载预训练模型并配置DIMM调度器。而后对预训练模型进行一次采样：


```python
# 载入一个管线
mypipe = "runwayml/stable-diffusion-v1-5"
pipe = StableDiffusionPipeline.from_pretrained(mypipe).to(device)
# 配置DDIM调度器
pipe.scheduler = DDIMScheduler.from_config(pipe.scheduler.config)
# 从中采样一次，以保证代码运行正常
prompt = 'Beautiful DSLR Photograph of a penguin on the beach, golden hour'

negative_prompt = 'blurry, ugly, stock photo'
im = pipe(prompt, negative_prompt=negative_prompt).images[0]
im.resize((256, 256))

```


    Loading pipeline components...:   0%|          | 0/7 [00:00<?, ?it/s]


    `text_config_dict` is provided which will be used to initialize `CLIPTextConfig`. The value `text_config["id2label"]` will be overriden.
    `text_config_dict` is provided which will be used to initialize `CLIPTextConfig`. The value `text_config["bos_token_id"]` will be overriden.
    `text_config_dict` is provided which will be used to initialize `CLIPTextConfig`. The value `text_config["eos_token_id"]` will be overriden.
    


      0%|          | 0/50 [00:00<?, ?it/s]





    
![png](img/output_6_3.png)
    




```python
prompt = 'Beautiful DSLR Photograph of a girl on the beach, golden hour'

negative_prompt = 'blurry, lightness, stock photo'
im = pipe(prompt, negative_prompt=negative_prompt).images[0]
im.resize((256, 256))
```


      0%|          | 0/50 [00:00<?, ?it/s]





    
![png](img/output_7_1.png)
    



## DIMM 采样

在给定时刻$t$,带有噪声的图像$x_t$通过对原始图像$x_0$ 加上高斯噪声ϵ得到：
$$x_t=\sqrt{a_t x_o} + \sqrt{1-a_t ϵ}$$

ϵ是方差归一化后的高斯噪声，$a_t$在DDPM论文中被称为$a$,并被用于定义噪声调度器。



```python
# 使用alphas_cumprod函数得到alphas
timesteps = pipe.scheduler.timesteps.cpu()
alphas = pipe.scheduler.alphas_cumprod[timesteps]
plt.plot(timesteps, alphas, label='alpha_t');
plt.legend();

```


    
![png](img/output_9_0.png)
    


当时间步为0时，从一幅无噪声的干净图像开始，此时$\alpha_t=1$，当达到更高的时间步，得到一幅几乎全是噪声的图像，$\alpha_t$也几乎下降到0。

> 前向过程在给定$x_{t-1}$和$x_0$的情况下变得更加确定。在生成过程中，随机噪声$\epsilon_t$前面的系数变为0，可得到隐式概率模型，其中模型样本是更加固定的过程从隐变量生成的(从$x_T$到$x_0$)，该模型命名为去噪扩散隐式模型（DDIM）。


```python
@torch.no_grad()
def sample(prompt, start_step=0, start_latents=None,
           guidance_scale=3.5, num_inference_steps=30,
           num_images_per_prompt=1, do_classifier_free_guidance=True,
           negative_prompt='', device=device):
    # 对文本提示语进行编码
    text_embeddings = pipe._encode_prompt(
            prompt, device, num_images_per_prompt, do_classifier_free_guidance, negative_prompt
    )
    # 设置推理步数
    pipe.scheduler.set_timesteps(num_inference_steps, device=device)
    # 创建随机起点
    if start_latents is None:
        start_latents = torch.randn(1, 4, 64, 64, device=device)
        start_latents *= pipe.scheduler.init_noise_sigma

    latents = start_latents.clone()

    for i in tqdm(range(start_step, num_inference_steps)):

        t = pipe.scheduler.timesteps[i]

        # 如果正在进行CFG，则对隐层进行扩展
        latent_model_input = torch.cat([latents] * 2) if do_classifier_free_guidance else latents
        latent_model_input = pipe.scheduler.scale_model_input(latent_model_input, t)

        # 预测噪声
        noise_pred = pipe.unet(latent_model_input, t, encoder_hidden_states=text_embeddings).sample

        # 进行引导
        if do_classifier_free_guidance:
            noise_pred_uncond, noise_pred_text = noise_pred.chunk(2)
            noise_pred = noise_pred_uncond + guidance_scale * (noise_pred_text - noise_pred_uncond)


        # Normally we'd rely on the scheduler to handle the update step:
        # latents = pipe.scheduler.step(noise_pred, t, latents).prev_sample

        # 自行实现调度器
        prev_t = max(1, t.item() - (1000//num_inference_steps)) # t-1
        alpha_t = pipe.scheduler.alphas_cumprod[t.item()]
        alpha_t_prev = pipe.scheduler.alphas_cumprod[prev_t]
        predicted_x0 = (latents - (1-alpha_t).sqrt()*noise_pred) / alpha_t.sqrt()
        direction_pointing_to_xt = (1-alpha_t_prev).sqrt()*noise_pred
        latents = alpha_t_prev.sqrt()*predicted_x0 + direction_pointing_to_xt

    # 进行后处理
    images = pipe.decode_latents(latents)
    images = pipe.numpy_to_pil(images)

    return images
```


```python
prompt = 'Watercolor painting of a beach sunset'
sample(prompt, negative_prompt=negative_prompt, num_inference_steps=50)[0].resize((256, 256))
```

    /usr/local/lib/python3.10/dist-packages/diffusers/pipelines/stable_diffusion/pipeline_stable_diffusion.py:237: FutureWarning: `_encode_prompt()` is deprecated and it will be removed in a future version. Use `encode_prompt()` instead. Also, be aware that the output format changed from a concatenated tensor to a tuple.
      deprecate("_encode_prompt()", "1.0.0", deprecation_message, standard_warn=False)
    


      0%|          | 0/50 [00:00<?, ?it/s]


    /usr/local/lib/python3.10/dist-packages/diffusers/pipelines/stable_diffusion/pipeline_stable_diffusion.py:430: FutureWarning: The decode_latents method is deprecated and will be removed in 1.0.0. Please use VaeImageProcessor.postprocess(...) instead
      deprecate("decode_latents", "1.0.0", deprecation_message, standard_warn=False)
    




    
![png](img/output_12_3.png)
    




```python
prompt = 'Van Gogh watercolor starry night'
sample(prompt, negative_prompt=negative_prompt, num_inference_steps=50)[0].resize((256, 256))
```


      0%|          | 0/50 [00:00<?, ?it/s]





    
![png](img/output_13_1.png)
    



## 反转

反转的目标是得到“带噪”的隐式表示。


```python
input_image = load_image('https://images.pexels.com/photos/8306128/pexels-photo-8306128.jpeg', size=(512, 512))
input_image
```




    
![png](img/output_15_0.png)
    




```python
input_image_prompt = "Photograph of a puppy on the grass"
```


```python
# 使用VAE进行编码
with torch.no_grad():
    latent = pipe.vae.encode(tfms.functional.to_tensor(input_image).unsqueeze(0).to(device)*2-1)
l = 0.18215 * latent.latent_dist.sample()
```


```python
# 反转
@torch.no_grad()
def invert(start_latents, prompt, guidance_scale=3.5, num_inference_steps=80,
           num_images_per_prompt=1, do_classifier_free_guidance=True,
           negative_prompt='', device=device):

    # 对提示文本进行编码
    text_embeddings = pipe._encode_prompt(
            prompt, device, num_images_per_prompt, do_classifier_free_guidance, negative_prompt
    )

    # 指定起点
    latents = start_latents.clone()

    # 保存反转的隐层
    intermediate_latents = []

    # 设置推理步数
    pipe.scheduler.set_timesteps(num_inference_steps, device=device)

    # 反转时间步
    timesteps = reversed(pipe.scheduler.timesteps)


    for i in tqdm(range(1, num_inference_steps), total=num_inference_steps-1):
        # 跳过最后一次迭代
        if i >= num_inference_steps - 1: continue

        t = timesteps[i]

        # 如果正在进行CFG，则对隐层进行扩展
        latent_model_input = torch.cat([latents] * 2) if do_classifier_free_guidance else latents
        latent_model_input = pipe.scheduler.scale_model_input(latent_model_input, t)

        # 预测残留的噪声
        noise_pred = pipe.unet(latent_model_input, t, encoder_hidden_states=text_embeddings).sample

        # 引导
        if do_classifier_free_guidance:
            noise_pred_uncond, noise_pred_text = noise_pred.chunk(2)
            noise_pred = noise_pred_uncond + guidance_scale * (noise_pred_text - noise_pred_uncond)

        current_t = max(0, t.item() - (1000//num_inference_steps)) # t
        next_t = t # min(999, t.item() + (1000//num_inference_steps)) # t+1
        alpha_t = pipe.scheduler.alphas_cumprod[current_t]
        alpha_t_next = pipe.scheduler.alphas_cumprod[next_t]

        # 反转的更新步（重新排列更新步，利用当前隐层得到新的隐层）
        latents = (latents - (1-alpha_t).sqrt() * noise_pred) * (alpha_t_next.sqrt() / alpha_t.sqrt()) + (1-alpha_t_next).sqrt() * noise_pred

        # 保存隐层
        intermediate_latents.append(latents)

    return torch.cat(intermediate_latents)
```


```python
inverted_latents = invert(l, input_image_prompt,num_inference_steps=50)
inverted_latents.shape
```


      0%|          | 0/49 [00:00<?, ?it/s]





    torch.Size([48, 4, 64, 64])




```python
torch.Size([48, 4, 64, 64])
```




    torch.Size([48, 4, 64, 64])




```python
# 解码反转的最后一个隐层
with torch.no_grad():
    im = pipe.decode_latents(inverted_latents[-1].unsqueeze(0))
pipe.numpy_to_pil(im)[0]
```




    
![png](img/output_21_1_0.png)
    




```python
# 可以通过常规调用方法，将反转隐层传递给管线
pipe(input_image_prompt, latents=inverted_latents[-1][None], num_inference_steps=50, guidance_scale=3.5).images[0]
```


      0%|          | 0/50 [00:00<?, ?it/s]





    
![png](img/output_22_1.png)
    




```python
# 从第20步的隐式表示开始，得到的结果距离最初的图片很近了！
start_step=20
sample(input_image_prompt, start_latents=inverted_latents[-(start_step+1)][None],
       start_step=start_step, num_inference_steps=50)[0]
```


      0%|          | 0/30 [00:00<?, ?it/s]





    
![png](img/output_23_1.png)
    




```python
# 把小狗换成小猫，从第10步的隐式表示开始
start_step=10
new_prompt = input_image_prompt.replace('puppy', 'cat')
sample(new_prompt, start_latents=inverted_latents[-(start_step+1)][None],
       start_step=start_step, num_inference_steps=50)[0]
```


      0%|          | 0/40 [00:00<?, ?it/s]





    
![png](img/output_24_1.png)
    




```python
start_step=10
new_prompt = input_image_prompt.replace('puppy', 'horse')
sample(new_prompt, start_latents=inverted_latents[-(start_step+1)][None],
       start_step=start_step, num_inference_steps=50)[0]
```


      0%|          | 0/40 [00:00<?, ?it/s]





    
![png](img/output_25_1.png)
    



##  组合封装


```python
def edit(input_image, input_image_prompt, edit_prompt, num_steps=100, start_step=30, guidance_scale=3.5):
    with torch.no_grad(): latent = pipe.vae.encode(tfms.functional.to_tensor(input_image).unsqueeze(0).to(device)*2-1)
    l = 0.18215 * latent.latent_dist.sample()
    inverted_latents = invert(l, input_image_prompt,num_inference_steps=num_steps)
    final_im = sample(edit_prompt, start_latents=inverted_latents[-(start_step+1)][None],
                      start_step=start_step, num_inference_steps=num_steps, guidance_scale=guidance_scale)[0]
    return final_im
```


```python
input_image
```




    
![png](img/output_28_0.png)
    




```python
edit(input_image, 'A puppy on the grass', 'an old grey dog on the grass', num_steps=50, start_step=10)
```


      0%|          | 0/49 [00:00<?, ?it/s]



      0%|          | 0/40 [00:00<?, ?it/s]





    
![png](img/output_29_2.png)
    




```python
face = load_image('https://cdn.pixabay.com/photo/2017/03/05/23/14/girl-2120196_640.jpg', size=(512, 512))
face
```




    
![png](img/output_30_0.png)
    




```python
edit(face, 'A photograph of a face', 'A photograph of a face with sunglasses', num_steps=250, start_step=30, guidance_scale=3.5)
```


      0%|          | 0/249 [00:00<?, ?it/s]



      0%|          | 0/220 [00:00<?, ?it/s]





    
![png](img/output_31_2.png)
    



##  ControlNet的结构与训练过程

**目标：** 主要解决图像细节的提示，包括人物四肢的角度、背景中物体的位置、每一缕光线照射的角度等。

**方案：** ControlNet能够嵌入任意已经训练好的扩散模型，可以提供更多控制条件。

> ControlNet的基本结构由一个对应的预训练网络的神经网络模块和两个“零卷积”层组成。在训练过程中，固定预训练网络的权重，只更新ControlNet基本结构中的网络“副本”和零卷积层的权重。网络“副本”将学会如何让模型按照新的控制条件来生成结果，被固定的网络会保留原先网络已经学会的所有知识。

**ControlNet模型的训练过程：**
1. 收集数据集，并包含对应的prompt。   
2. 将prompt输入被固定的稳定扩散模型，并将标注好的图像控制条件输入ControlNet，然后按照稳定扩散模型的训练过程迭代ControlNet block的权重。
3. 在训练过程中，随机将50%的文本提示语替换为空白字符串。
4. 训练结束后，使用ControlNet对应的图像控制条件，来控制扩散模型生成符合条件的图像。

## ControlNet实战

###  生成人物的肖像


```python
!pip install -q diffusers==0.14.0 transformers xformers git+https://github.com/huggingface/accelerate.git
```

      Installing build dependencies ... [?25l[?25hdone
      Getting requirements to build wheel ... [?25l[?25hdone
      Preparing metadata (pyproject.toml) ... [?25l[?25hdone
    [2K     [90m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[0m [32m737.4/737.4 kB[0m [31m6.6 MB/s[0m eta [36m0:00:00[0m
    [2K     [90m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[0m [32m211.8/211.8 MB[0m [31m2.2 MB/s[0m eta [36m0:00:00[0m
    [?25h  Building wheel for accelerate (pyproject.toml) ... [?25l[?25hdone
    


```python
!pip install -q opencv-contrib-python
```


```python
!pip install -q controlnet_aux
```


```python
from diffusers import StableDiffusionControlNetPipeline
from diffusers.utils import load_image

image = load_image("https://s.yimg.com/ny/api/res/1.2/uf5CdO4GWdFvAlccVVFd9g--/YXBwaWQ9aGlnaGxhbmRlcjt3PTk2MDtoPTk1NjtjZj13ZWJw/https://media.zenfs.com/zh-tw/entertainment.nownews.hk/c441463e5276b19ae4588c1690199852")
image
```




    
![png](img/output_36_0.png)
    




```python
import cv2
from PIL import Image
import numpy as np

image = np.array(image)

low_threshold = 100
high_threshold = 200

# 提取图片边缘线条
image = cv2.Canny(image, low_threshold, high_threshold)
image = image[:, :, None]
image = np.concatenate([image, image, image], axis=2)
canny_image = Image.fromarray(image)
canny_image
```




    
![png](img/output_37_0.png)
    




```python
# 使用半精度节约计算资源，加快推理速度
from diffusers import StableDiffusionControlNetPipeline, ControlNetModel
import torch

controlnet = ControlNetModel.from_pretrained("lllyasviel/sd-controlnet-canny", torch_dtype=torch.float16).to(device)
pipe = StableDiffusionControlNetPipeline.from_pretrained("runwayml/stable-diffusion-v1-5", controlnet=controlnet,
                                                        torch_dtype=torch.float16).to(device)
```


    Loading pipeline components...:   0%|          | 0/7 [00:00<?, ?it/s]


    `text_config_dict` is provided which will be used to initialize `CLIPTextConfig`. The value `text_config["id2label"]` will be overriden.
    `text_config_dict` is provided which will be used to initialize `CLIPTextConfig`. The value `text_config["bos_token_id"]` will be overriden.
    `text_config_dict` is provided which will be used to initialize `CLIPTextConfig`. The value `text_config["eos_token_id"]` will be overriden.
    


```python
# 使用速度最快的扩散模型调度器UniPCMultistepScheduler
from diffusers import UniPCMultistepScheduler

pipe.scheduler = UniPCMultistepScheduler.from_config(pipe.scheduler.config)
```


```python
def image_grid(imgs, rows, cols):
    assert len(imgs) == rows * cols

    w, h = imgs[0].size
    grid = Image.new("RGB", size=(cols * w, rows * h))
    grid_w, grid_h = grid.size

    for i, img in enumerate(imgs):
        grid.paste(img, box=(i % cols * w, i // cols * h))

    return grid
```


```python
prompt = ", best quality, extremely detailed"
prompt = [t + prompt for t in ["Sandra Oh", "Kim Kardashian", "rihanna", "taylor swift"]]
generator = [torch.Generator(device=device).manual_seed(2) for i in range(len(prompt))]

output = pipe(
    prompt,
    canny_image,
    negative_prompt=["monochrome, lowres, bad anatomy, worst quality, low quality"] * len(prompt),
    generator=generator,
    num_inference_steps=30
)

image_grid(output.images, 2, 2)
```


      0%|          | 0/30 [00:00<?, ?it/s]


### 提取身体姿态


```python
urls = ["yoga1.jpeg", "yoga2.jpeg", "yoga3.jpeg", "yoga4.jpeg"]
imgs = [
    load_image("https://huggingface.co/datasets/YiYiXu/controlnet-testing/resolve/main/" + url) for url in urls
]
image_grid(imgs, 2, 2)
```




    
![png](img/output_43_0.png)
    




```python
from controlnet_aux import OpenposeDetector

model = OpenposeDetector.from_pretrained("lllyasviel/ControlNet")

poses = [model(img) for img in imgs]
image_grid(poses, 2, 2)
```




    
![png](img/output_44_0.png)
    




```python
from diffusers import ControlNetModel, UniPCMultistepScheduler, StableDiffusionControlNetPipeline

controlnet = ControlNetModel.from_pretrained("fusing/stable-diffusion-v1-5-controlnet-openpose",
                                             torch_dtype=torch.float16).to(device)
```


```python
model_id = "runwayml/stable-diffusion-v1-5"
pipe = StableDiffusionControlNetPipeline.from_pretrained(
    model_id,
    controlnet = controlnet,
    torch_dtype=torch.float16
).to(device)
```


    Loading pipeline components...:   0%|          | 0/7 [00:00<?, ?it/s]


    `text_config_dict` is provided which will be used to initialize `CLIPTextConfig`. The value `text_config["id2label"]` will be overriden.
    `text_config_dict` is provided which will be used to initialize `CLIPTextConfig`. The value `text_config["bos_token_id"]` will be overriden.
    `text_config_dict` is provided which will be used to initialize `CLIPTextConfig`. The value `text_config["eos_token_id"]` will be overriden.
    


```python
pipe.scheduler = UniPCMultistepScheduler.from_config(pipe.scheduler.config)
pipe.enable_model_cpu_offload()
pipe.enable_xformers_memory_efficient_attention()
```


```python
device
```




    device(type='cuda')




```python
generator = [torch.Generator(device=device).manual_seed(10) for i in range(4)]
prompt = "super-hero character, best quality, extremely detailed"

output = pipe(
    [prompt] * 4,
    poses,
    negative_prompt=["monochrome, lowres, bad anatomy, worst quality, low quality"] * 4,
    generator=generator,
    num_inference_steps=20
)

```


      0%|          | 0/20 [00:00<?, ?it/s]



```python
image_grid(output.images, 2, 2)
```




    
![png](img/output_50_0.png)
    




```python


generator = [torch.Generator(device=device).manual_seed(10) for i in range(4)]
prompt = "Super villain, best quality, very rough. Change it"

output = pipe(
    [prompt] * 4,
    poses,
    negative_prompt=["monochrome, lowres, bad anatomy, worst quality, low quality"] * 4,
    generator=generator,
    num_inference_steps=20
)

```


      0%|          | 0/20 [00:00<?, ?it/s]


    Potential NSFW content was detected in one or more images. A black image will be returned instead. Try again with a different prompt and/or seed.
    


```python
image_grid(output.images, 2, 2)
```




    
![png](img/output_52_0.png)
    


