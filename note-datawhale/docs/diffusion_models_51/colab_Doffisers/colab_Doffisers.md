# 第一周练习：Diffusers 介绍

> **实现代码来自diffusion-models-class（中文）**：https://github.com/darcula1993/diffusion-models-class-CN

## **推荐阅读列表**

- [第1章 扩散模型简介](docs/diffusion_models_51/part01.md)
- [第2章 Hugging Face简介](docs/diffusion_models_51/part02.md)
- [第3章 从零开始搭建扩散模型](docs/diffusion_models_51/part03.md)

## 练习代码

在这个 Notebook 里，你将训练你的第一个扩散模型来 **生成美丽的蝴蝶的图片 🦋**。在此过程中，你将了解 🤗 Diffuers 库，它将为我们稍后将在课程中介绍的更高级的应用程序提供良好的基础

让我们直接上代码吧！

运行环境：  google colab T4 GPU

![img.png](img.png)

```python
%pip install -qq -U diffusers datasets transformers accelerate ftfy pyarrow==9.0

```

[2K     [90m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[0m [32m1.5/1.5 MB[0m [31m17.1 MB/s[0m eta [36m0:00:00[0m
[2K     [90m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[0m [32m519.6/519.6 kB[0m [31m49.7 MB/s[0m eta [36m0:00:00[0m
[2K     [90m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[0m [32m7.7/7.7 MB[0m [31m103.7 MB/s[0m eta [36m0:00:00[0m
[2K     [90m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[0m [32m258.1/258.1 kB[0m [31m33.4 MB/s[0m eta [36m0:00:00[0m
[2K     [90m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[0m [32m53.1/53.1 kB[0m [31m7.9 MB/s[0m eta [36m0:00:00[0m
[2K     [90m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[0m [32m302.0/302.0 kB[0m [31m36.8 MB/s[0m eta [36m0:00:00[0m
[2K     [90m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[0m [32m1.3/1.3 MB[0m [31m86.7 MB/s[0m eta [36m0:00:00[0m
[2K     [90m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[0m [32m115.3/115.3 kB[0m [31m17.2 MB/s[0m eta [36m0:00:00[0m
[2K     [90m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[0m [32m194.1/194.1 kB[0m [31m21.1 MB/s[0m eta [36m0:00:00[0m
[2K     [90m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[0m [32m134.8/134.8 kB[0m [31m7.6 MB/s[0m eta [36m0:00:00[0m
[2K     [90m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[0m [32m3.8/3.8 MB[0m [31m76.7 MB/s[0m eta [36m0:00:00[0m
[2K     [90m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[0m [32m295.0/295.0 kB[0m [31m33.6 MB/s[0m eta [36m0:00:00[0m
[?25h
```python
from huggingface_hub import notebook_login

notebook_login()

# token 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

```
VBox(children=(HTML(value='<center> <img\nsrc=https://huggingface.co/front/assets/huggingface_logo-noborder.sv…
```python
%%capture
!sudo apt -qq install git-lfs
!git config --global credential.helper store
```
```python
!pip install torch torchvision

```
Requirement already satisfied: torch in /usr/local/lib/python3.10/dist-packages (2.0.1+cu118)
Requirement already satisfied: torchvision in /usr/local/lib/python3.10/dist-packages (0.15.2+cu118)
Requirement already satisfied: filelock in /usr/local/lib/python3.10/dist-packages (from torch) (3.12.4)
Requirement already satisfied: typing-extensions in /usr/local/lib/python3.10/dist-packages (from torch) (4.5.0)
Requirement already satisfied: sympy in /usr/local/lib/python3.10/dist-packages (from torch) (1.12)
Requirement already satisfied: networkx in /usr/local/lib/python3.10/dist-packages (from torch) (3.1)
Requirement already satisfied: jinja2 in /usr/local/lib/python3.10/dist-packages (from torch) (3.1.2)
Requirement already satisfied: triton==2.0.0 in /usr/local/lib/python3.10/dist-packages (from torch) (2.0.0)
Requirement already satisfied: cmake in /usr/local/lib/python3.10/dist-packages (from triton==2.0.0->torch) (3.27.6)
Requirement already satisfied: lit in /usr/local/lib/python3.10/dist-packages (from triton==2.0.0->torch) (17.0.2)
Requirement already satisfied: numpy in /usr/local/lib/python3.10/dist-packages (from torchvision) (1.23.5)
Requirement already satisfied: requests in /usr/local/lib/python3.10/dist-packages (from torchvision) (2.31.0)
Requirement already satisfied: pillow!=8.3.*,>=5.3.0 in /usr/local/lib/python3.10/dist-packages (from torchvision) (9.4.0)
Requirement already satisfied: MarkupSafe>=2.0 in /usr/local/lib/python3.10/dist-packages (from jinja2->torch) (2.1.3)
Requirement already satisfied: charset-normalizer<4,>=2 in /usr/local/lib/python3.10/dist-packages (from requests->torchvision) (3.3.0)
Requirement already satisfied: idna<4,>=2.5 in /usr/local/lib/python3.10/dist-packages (from requests->torchvision) (3.4)
Requirement already satisfied: urllib3<3,>=1.21.1 in /usr/local/lib/python3.10/dist-packages (from requests->torchvision) (2.0.6)
Requirement already satisfied: certifi>=2017.4.17 in /usr/local/lib/python3.10/dist-packages (from requests->torchvision) (2023.7.22)
Requirement already satisfied: mpmath>=0.19 in /usr/local/lib/python3.10/dist-packages (from sympy->torch) (1.3.0)
```python
import numpy as np
import torch
import torch.nn.functional as F
from matplotlib import pyplot as plt
from PIL import Image
```
```python
def show_images(x):
    """Given a batch of images x, make a grid and convert to PIL"""
    x = x * 0.5 + 0.5  # Map from (-1, 1) back to (0, 1)
    grid = torchvision.utils.make_grid(x)
    grid_im = grid.detach().cpu().permute(1, 2, 0).clip(0, 1) * 255
    grid_im = Image.fromarray(np.array(grid_im).astype(np.uint8))
    return grid_im


def make_grid(images, size=64):
    """Given a list of PIL images, stack them together into a line for easy viewing"""
    output_im = Image.new("RGB", (size * len(images), size))
    for i, im in enumerate(images):
        output_im.paste(im.resize((size, size)), (i * size, 0))
    return output_im


# Mac users may need device = 'mps' (untested)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
```
```python
device
```
device(type='cuda')
```python
from IPython.display import YouTubeVideo

YouTubeVideo("W4Mcuh38wyM")
```
<iframe
    width="400"
    height="300"
    src="https://www.youtube.com/embed/W4Mcuh38wyM"
    frameborder="0"
    allowfullscreen

> </iframe>

```python
from diffusers import StableDiffusionPipeline

# Check out https://huggingface.co/sd-dreambooth-library for loads of models from the community
model_id = "sd-dreambooth-library/mr-potato-head"

# Load the pipeline
pipe = StableDiffusionPipeline.from_pretrained(model_id, torch_dtype=torch.float32).to(
    device
)
```
The cache for model files in Transformers v4.22.0 has been updated. Migrating your old cache. This is a one-time only operation. You can interrupt this and resume the migration later on by calling `transformers.utils.move_cache()`.



0it [00:00, ?it/s]



Downloading (…)ain/model_index.json:   0%|          | 0.00/546 [00:00<?, ?B/s]


safety_checker/model.safetensors not found



Fetching 15 files:   0%|          | 0/15 [00:00<?, ?it/s]



Downloading (…)_encoder/config.json:   0%|          | 0.00/589 [00:00<?, ?B/s]



Downloading (…)rocessor_config.json:   0%|          | 0.00/342 [00:00<?, ?B/s]



Downloading (…)tokenizer/merges.txt:   0%|          | 0.00/525k [00:00<?, ?B/s]



Downloading (…)cial_tokens_map.json:   0%|          | 0.00/472 [00:00<?, ?B/s]



Downloading (…)cheduler_config.json:   0%|          | 0.00/289 [00:00<?, ?B/s]



Downloading (…)_checker/config.json:   0%|          | 0.00/4.67k [00:00<?, ?B/s]



Downloading (…)okenizer_config.json:   0%|          | 0.00/805 [00:00<?, ?B/s]



Downloading (…)tokenizer/vocab.json:   0%|          | 0.00/1.06M [00:00<?, ?B/s]



Downloading (…)d4e/unet/config.json:   0%|          | 0.00/794 [00:00<?, ?B/s]



Downloading (…)2d4e/vae/config.json:   0%|          | 0.00/597 [00:00<?, ?B/s]



Downloading pytorch_model.bin:   0%|          | 0.00/608M [00:00<?, ?B/s]



Downloading pytorch_model.bin:   0%|          | 0.00/246M [00:00<?, ?B/s]



Downloading (…)on_pytorch_model.bin:   0%|          | 0.00/167M [00:00<?, ?B/s]



Downloading (…)on_pytorch_model.bin:   0%|          | 0.00/1.72G [00:00<?, ?B/s]



Loading pipeline components...:   0%|          | 0/7 [00:00<?, ?it/s]


`text_config_dict` is provided which will be used to initialize `CLIPTextConfig`. The value `text_config["id2label"]` will be overriden.
`text_config_dict` is provided which will be used to initialize `CLIPTextConfig`. The value `text_config["bos_token_id"]` will be overriden.
`text_config_dict` is provided which will be used to initialize `CLIPTextConfig`. The value `text_config["eos_token_id"]` will be overriden.
```python
prompt = "an  Bosai Kitty oil painting of sks mr cat head by picasso"
image = pipe(prompt, num_inference_steps=50, guidance_scale=7.5).images[0]
image
```
  0%|          | 0/50 [00:00<?, ?it/s]
![png](output_10_1.png)

*斜体文本*

```python
from diffusers import DDPMPipeline

# Load the butterfly pipeline
butterfly_pipeline = DDPMPipeline.from_pretrained(
    "johnowhitaker/ddpm-butterflies-32px"
).to(device)

# Create 8 images
images = butterfly_pipeline(batch_size=8).images

# View the result
make_grid(images)
```
Downloading (…)ain/model_index.json:   0%|          | 0.00/180 [00:00<?, ?B/s]


diffusion_pytorch_model.safetensors not found



Fetching 4 files:   0%|          | 0/4 [00:00<?, ?it/s]



Downloading (…)b9c177f3/config.json:   0%|          | 0.00/702 [00:00<?, ?B/s]



Downloading (…)cheduler_config.json:   0%|          | 0.00/267 [00:00<?, ?B/s]



Downloading (…)on_pytorch_model.bin:   0%|          | 0.00/74.3M [00:00<?, ?B/s]



Loading pipeline components...:   0%|          | 0/2 [00:00<?, ?it/s]



  0%|          | 0/1000 [00:00<?, ?it/s]
![png](output_12_8.png)

```python
import torchvision
from datasets import load_dataset
from torchvision import transforms

dataset = load_dataset("huggan/smithsonian_butterflies_subset", split="train")

# Or load images from a local folder
# dataset = load_dataset("imagefolder", data_dir="path/to/folder")

# We'll train on 32-pixel square images, but you can try larger sizes too
image_size = 32
# You can lower your batch size if you're running out of GPU memory
batch_size = 64

# Define data augmentations
preprocess = transforms.Compose(
    [
        transforms.Resize((image_size, image_size)),  # Resize
        transforms.RandomHorizontalFlip(),  # Randomly flip (data augmentation)
        transforms.ToTensor(),  # Convert to tensor (0, 1)
        transforms.Normalize([0.5], [0.5]),  # Map to (-1, 1)
    ]
)


def transform(examples):
    images = [preprocess(image.convert("RGB")) for image in examples["image"]]
    return {"images": images}


dataset.set_transform(transform)

# Create a dataloader from the dataset to serve up the transformed images in batches
train_dataloader = torch.utils.data.DataLoader(
    dataset, batch_size=batch_size, shuffle=True
)
```
Downloading readme:   0%|          | 0.00/609 [00:00<?, ?B/s]


Repo card metadata block was not found. Setting CardData to empty.
WARNING:huggingface_hub.repocard:Repo card metadata block was not found. Setting CardData to empty.



Downloading metadata:   0%|          | 0.00/1.65k [00:00<?, ?B/s]



Downloading data files:   0%|          | 0/1 [00:00<?, ?it/s]



Downloading data:   0%|          | 0.00/237M [00:00<?, ?B/s]



Extracting data files:   0%|          | 0/1 [00:00<?, ?it/s]



Generating train split:   0%|          | 0/1000 [00:00<?, ? examples/s]
```python
xb = next(iter(train_dataloader))["images"].to(device)[:8]
print("X shape:", xb.shape)
show_images(xb).resize((8 * 64, 64), resample=Image.NEAREST)
```
X shape: torch.Size([8, 3, 32, 32])
![png](output_14_1.png)

```python
from diffusers import DDPMScheduler

noise_scheduler = DDPMScheduler(num_train_timesteps=1000)
```
```python
plt.plot(noise_scheduler.alphas_cumprod.cpu() ** 0.5, label=r"${\sqrt{\bar{\alpha}_t}}$")
plt.plot((1 - noise_scheduler.alphas_cumprod.cpu()) ** 0.5, label=r"$\sqrt{(1 - \bar{\alpha}_t)}$")
plt.legend(fontsize="x-large");
```

![png](output_16_0.png)

```python
noise_scheduler = DDPMScheduler(num_train_timesteps=1000, beta_start=0.001, beta_end=0.004)
```
```python
plt.plot(noise_scheduler.alphas_cumprod.cpu() ** 0.5, label=r"${\sqrt{\bar{\alpha}_t}}$")
plt.plot((1 - noise_scheduler.alphas_cumprod.cpu()) ** 0.5, label=r"$\sqrt{(1 - \bar{\alpha}_t)}$")
plt.legend(fontsize="x-large");
```

![png](output_19_0.png)

```python
noise_scheduler = DDPMScheduler(num_train_timesteps=1000, beta_schedule='squaredcos_cap_v2')
```
```python
plt.plot(noise_scheduler.alphas_cumprod.cpu() ** 0.5, label=r"${\sqrt{\bar{\alpha}_t}}$")
plt.plot((1 - noise_scheduler.alphas_cumprod.cpu()) ** 0.5, label=r"$\sqrt{(1 - \bar{\alpha}_t)}$")
plt.legend(fontsize="x-large");
```

![png](output_21_0.png)

```python
timesteps = torch.linspace(0, 999, 8).long().to(device)
noise = torch.randn_like(xb)
noisy_xb = noise_scheduler.add_noise(xb, noise, timesteps)
print("Noisy X shape", noisy_xb.shape)
show_images(noisy_xb).resize((8 * 64, 64), resample=Image.NEAREST)
```
Noisy X shape torch.Size([8, 3, 32, 32])
![png](output_22_1.png)

```python
from diffusers import UNet2DModel

# Create a model
model = UNet2DModel(
    sample_size=image_size,  # the target image resolution
    in_channels=3,  # the number of input channels, 3 for RGB images
    out_channels=3,  # the number of output channels
    layers_per_block=2,  # how many ResNet layers to use per UNet block
    block_out_channels=(64, 128, 128, 256),  # More channels -> more parameters
    down_block_types=(
        "DownBlock2D",  # a regular ResNet downsampling block
        "DownBlock2D",
        "AttnDownBlock2D",  # a ResNet downsampling block with spatial self-attention
        "AttnDownBlock2D",
    ),
    up_block_types=(
        "AttnUpBlock2D",
        "AttnUpBlock2D",  # a ResNet upsampling block with spatial self-attention
        "UpBlock2D",
        "UpBlock2D",  # a regular ResNet upsampling block
    ),
)
model.to(device);
```
```python
with torch.no_grad():
    model_prediction = model(noisy_xb, timesteps).sample
model_prediction.shape
```
torch.Size([8, 3, 32, 32])
```python
# Set the noise scheduler
noise_scheduler = DDPMScheduler(
    num_train_timesteps=1000, beta_schedule="squaredcos_cap_v2"
)

# Training loop
optimizer = torch.optim.AdamW(model.parameters(), lr=4e-4)

losses = []

for epoch in range(30):
    for step, batch in enumerate(train_dataloader):
        clean_images = batch["images"].to(device)
        # Sample noise to add to the images
        noise = torch.randn(clean_images.shape).to(clean_images.device)
        bs = clean_images.shape[0]

        # Sample a random timestep for each image
        timesteps = torch.randint(
            0, noise_scheduler.num_train_timesteps, (bs,), device=clean_images.device
        ).long()

        # Add noise to the clean images according to the noise magnitude at each timestep
        noisy_images = noise_scheduler.add_noise(clean_images, noise, timesteps)

        # Get the model prediction
        noise_pred = model(noisy_images, timesteps, return_dict=False)[0]

        # Calculate the loss
        loss = F.mse_loss(noise_pred, noise)
        loss.backward(loss)
        losses.append(loss.item())

        # Update the model parameters with the optimizer
        optimizer.step()
        optimizer.zero_grad()

    if (epoch + 1) % 5 == 0:
        loss_last_epoch = sum(losses[-len(train_dataloader) :]) / len(train_dataloader)
        print(f"Epoch:{epoch+1}, loss: {loss_last_epoch}")
```
/usr/local/lib/python3.10/dist-packages/diffusers/configuration_utils.py:134: FutureWarning: Accessing config attribute `num_train_timesteps` directly via 'DDPMScheduler' object attribute is deprecated. Please access 'num_train_timesteps' over 'DDPMScheduler's config object instead, e.g. 'scheduler.config.num_train_timesteps'.
  deprecate("direct config name access", "1.0.0", deprecation_message, standard_warn=False)


Epoch:5, loss: 0.14980323100462556
Epoch:10, loss: 0.1132772983983159
Epoch:15, loss: 0.09343559155240655
Epoch:20, loss: 0.08541441080160439
Epoch:25, loss: 0.07371148932725191
Epoch:30, loss: 0.07440270017832518
```python
fig, axs = plt.subplots(1, 2, figsize=(12, 4))
axs[0].plot(losses)
axs[1].plot(np.log(losses))
plt.show()
```

![png](output_26_0.png)

```python
model = butterfly_pipeline.unet # 或者通过管道来调用模型
```
```python
from diffusers import DDPMPipeline

image_pipe = DDPMPipeline(unet=model, scheduler=noise_scheduler)
```
```python
pipeline_output = image_pipe()
pipeline_output.images[0]
```
  0%|          | 0/1000 [00:00<?, ?it/s]
![png](output_29_1.png)

```python
image_pipe.save_pretrained("my_pipeline")
```
```python
!ls my_pipeline/
```
model_index.json  scheduler  unet
```python
!ls my_pipeline/unet/
```
config.json  diffusion_pytorch_model.safetensors
```python
??image_pipe.forward
```
Object `image_pipe.forward` not found.
```python
# Random starting point (8 random images):
sample = torch.randn(8, 3, 32, 32).to(device)

for i, t in enumerate(noise_scheduler.timesteps):

    # Get model pred
    with torch.no_grad():
        residual = model(sample, t).sample

    # Update sample with step
    sample = noise_scheduler.step(residual, t, sample).prev_sample

show_images(sample)
```

![png](output_34_0.png)

```python
from huggingface_hub import get_full_repo_name

model_name = "sd-class-butterflies-Jochoi-32"
hub_model_id = get_full_repo_name(model_name)
hub_model_id
```
'Jochoi/sd-class-butterflies-Jochoi-32'
```python
from huggingface_hub import HfApi, create_repo

create_repo(hub_model_id)
api = HfApi()
api.upload_folder(
    folder_path="my_pipeline/scheduler", path_in_repo="", repo_id=hub_model_id
)
api.upload_folder(folder_path="my_pipeline/unet", path_in_repo="", repo_id=hub_model_id)
api.upload_file(
    path_or_fileobj="my_pipeline/model_index.json",
    path_in_repo="model_index.json",
    repo_id=hub_model_id,
)
```
diffusion_pytorch_model.safetensors:   0%|          | 0.00/74.2M [00:00<?, ?B/s]





'https://huggingface.co/Jochoi/sd-class-butterflies-Jochoi-32/blob/main/model_index.json'
```python
from huggingface_hub import ModelCard

content = f"""
---
license: mit
tags:
- pytorch
- diffusers
- unconditional-image-generation
- diffusion-models-class
---

# Model Card for Unit 1 of the [Diffusion Models Class 🧨](https://github.com/huggingface/diffusion-models-class)

This model is a diffusion model for unconditional image generation of cute 🦋.

## Usage

​```python
from diffusers import DDPMPipeline

pipeline = DDPMPipeline.from_pretrained('{hub_model_id}')
image = pipeline().images[0]
image
```
"""

card = ModelCard(content)
card.push_to_hub(hub_model_id)

```




    'https://huggingface.co/Jochoi/sd-class-butterflies-Jochoi-32/blob/main/README.md'




​```python
from diffusers import DDPMPipeline

image_pipe = DDPMPipeline.from_pretrained(hub_model_id)
pipeline_output = image_pipe()
pipeline_output.images[0]
```
Downloading (…)ain/model_index.json:   0%|          | 0.00/181 [00:00<?, ?B/s]



Fetching 4 files:   0%|          | 0/4 [00:00<?, ?it/s]



Downloading (…)c8fdf3a6/config.json:   0%|          | 0.00/1.04k [00:00<?, ?B/s]



Downloading (…)cheduler_config.json:   0%|          | 0.00/473 [00:00<?, ?B/s]



Downloading (…)ch_model.safetensors:   0%|          | 0.00/74.2M [00:00<?, ?B/s]



Loading pipeline components...:   0%|          | 0/2 [00:00<?, ?it/s]



  0%|          | 0/1000 [00:00<?, ?it/s]
![png](output_38_7.png)

# 使用 🤗 Accelerate 来扩大规模

```python
!wget https://github.com/huggingface/diffusers/raw/main/examples/unconditional_image_generation/train_unconditional.py
```
--2023-10-18 05:48:36--  https://github.com/huggingface/diffusers/raw/main/examples/unconditional_image_generation/train_unconditional.py
Resolving github.com (github.com)... 140.82.113.3
Connecting to github.com (github.com)|140.82.113.3|:443... connected.
HTTP request sent, awaiting response... 302 Found
Location: https://raw.githubusercontent.com/huggingface/diffusers/main/examples/unconditional_image_generation/train_unconditional.py [following]
--2023-10-18 05:48:36--  https://raw.githubusercontent.com/huggingface/diffusers/main/examples/unconditional_image_generation/train_unconditional.py
Resolving raw.githubusercontent.com (raw.githubusercontent.com)... 185.199.108.133, 185.199.109.133, 185.199.110.133, ...
Connecting to raw.githubusercontent.com (raw.githubusercontent.com)|185.199.108.133|:443... connected.
HTTP request sent, awaiting response... 200 OK
Length: 29768 (29K) [text/plain]
Saving to: ‘train_unconditional.py’

train_unconditional 100%[===================>]  29.07K  --.-KB/s    in 0.002s  

2023-10-18 05:48:36 (17.3 MB/s) - ‘train_unconditional.py’ saved [29768/29768]

```python
# Let's give our new model a name for the Hub
model_name = "sd-class-butterflies-Jochoi-64"
hub_model_id = get_full_repo_name(model_name)
hub_model_id


```
'Jochoi/sd-class-butterflies-Jochoi-64'
```python
!accelerate launch train_unconditional.py \
  --dataset_name="huggan/smithsonian_butterflies_subset" \
  --resolution=64 \
  --output_dir={model_name} \
  --train_batch_size=32 \
  --num_epochs=50 \
  --gradient_accumulation_steps=1 \
  --learning_rate=1e-4 \
  --lr_warmup_steps=500 \
  --mixed_precision="no"
```
```python
create_repo(hub_model_id)
api = HfApi()
api.upload_folder(
    folder_path=f"{model_name}/scheduler", path_in_repo="", repo_id=hub_model_id
)
api.upload_folder(
    folder_path=f"{model_name}/unet", path_in_repo="", repo_id=hub_model_id
)
api.upload_file(
    path_or_fileobj=f"{model_name}/model_index.json",
    path_in_repo="model_index.json",
    repo_id=hub_model_id,
)

content = f"""
---
license: mit
tags:
- pytorch
- diffusers
- unconditional-image-generation
- diffusion-models-class
---

# Model Card for Unit 1 of the [Diffusion Models Class 🧨](https://github.com/huggingface/diffusion-models-class)

This model is a diffusion model for unconditional image generation of cute 🦋.

## Usage

​```python
from diffusers import DDPMPipeline

pipeline = DDPMPipeline.from_pretrained('{hub_model_id}')
image = pipeline().images[0]
image
```
"""

card = ModelCard(content)
card.push_to_hub(hub_model_id)

```


​```python
pipeline = DDPMPipeline.from_pretrained(hub_model_id).to(device)
images = pipeline(batch_size=8).images
make_grid(images)
```
