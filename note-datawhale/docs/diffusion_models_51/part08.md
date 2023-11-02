# 第8章 音频扩散模型
---
## 8.1 实战：音频扩散模型

### 8.1.1 设置与导入

首先安装需要用到的库并配置环境，代码如下：



```python
!pip install -q datasets diffusers torchaudio accelerate
```


```python
import torch,random
import numpy as np
import torch.nn.functional as F
from tqdm.auto import tqdm
from IPython.display import Audio
from matplotlib import pyplot as plt
from diffusers import DiffusionPipeline
from torchaudio import transforms as AT
from torchvision import transforms as IT
```

### 8.1.2 从预训练的音频扩散模型管线中进行采样

加载一个预训练的音频扩散模型管线


```python
# 加载一个预训练的音频扩散模型管线
device = "cuda" if torch.cuda.is_available() else "cpu"
mypipe = "teticio/audiodiffusion-instrumental-hiphop- 256"
pipe   = DiffusionPipeline.from_pretrained(mypipe).to(device)
```


```python
# 在管线中采样一次并将采样结果显示出来
output = pipe()
display(output.images[0])
display(Audio(output.audio[0],
rate = pipe.mel.get_sample_rate()))
```

在上述代码中，rate参数定义了音频的采样率。此外你可能还会注意到管线返回了其他一些内容。

首先是数据数组，代表生成的音频：


```python
# 音频序列
output.audios[0].shape
```


```python
# 输出的图像（频谱）
output.images[0].size
```

注意：音频并非由扩散模型直接生成

扩展：[梅 尔 频 谱 (Mel spectrogram)](https://www.rtcdeveloper.cn/cn/community/blog/21571)


```python
### 8.1.3 从音频到频谱的转换
spec_transform = AT.Spectrogram(power=2)
spectrogram = spec_transform(torch.tensor(output.audios[0]))
print(spectrogram.min(),spectrogram.max())
log_spectrogram = spectrogram.log()
lt.imshow(log_spectrogram[0],cmap = 'gray');
tensor(0.) tensor(6.0842)
```


```python
# 增加mel频谱
a = pipe.mel.image_to_audio(output.images[0])
a.shape
```


```python

pip.mel.load_audio(raw_audio=a)
im = pipe.mel.audio_slice_to_image(0)
im 
```


```python
sample_rate_pipeline = pipe.mel.get_sample_rate()
sample_rate_pipeline
```


```python
display(Audio(output.audios[0],rate=44100)) # 播放速度被加倍
```

### 8.1.4 微调管线

尝试一个新得示例：


```python
from datasets import load_dataset
dataset = load_dataset('lewtun/music_genres', split='train')
dataset
```


```python
for g in list(set(dataset['genre'])):
 print(g, sum(x==g for x in dataset['genre']))
```

该数据集已将音频存储为数组


```python
audio_array = dataset[0]['audio']['array']
sample_rate_dataset = dataset[0]['audio']['sampling_rate']
print('Audio array shape:', audio_array.shape)
print('Sample rate:', sample_rate_dataset)
```

使用pipe.mel 将其自动切片为更短的片段


```python
audio_array = dataset[0]['audio']['array']
sample_rate_dataset = dataset[0]['audio']['sampling_rate']
print('Audio array shape:', audio_array.shape)
print('Sample rate:', sample_rate_dataset)
```

调整采样率，因为该数据集中的数据在每一秒都拥有两倍的数据点


```python
sample_rate_dataset = dataset[0]['audio']['sampling_rate']
sample_rate_dataset
```

使用torchaudio transforms（导入为AT）进行音频的重采样，并使用管线的mel功能将音频转换为频谱图像，然后使用
torchvision transforms（导入为IT）将频谱图像转换为频谱张量。以下代码中的to_image()函数可以将音频片段转换为频谱张量，供训
练使用：


```python
resampler = AT.Resample(sample_rate_dataset,
sample_rate_pipeline,
 dtype=torch.float32)
to_t = IT.ToTensor()
```


```python
def to_image(audio_array):
     audio_tensor = torch.tensor(audio_array).to(torch.float32)
     audio_tensor = resampler(audio_tensor)
     pipe.mel.load_audio(raw_audio=np.array(audio_tensor))
     num_slices = pipe.mel.get_number_of_slices()
     slice_idx = random.randint(0, num_slices-1) # 每次随机取一张（除了最后那张）
     im = pipe.mel.audio_slice_to_image(slice_idx)
     return im
```

将每个音频转换为频谱图像，然后将它们的张量堆叠起来


```python
def collate_fn(examples):
    # 将图像转变为张量，再缩放到(-1, 1)区间，再变成数组
    audio_ims = [to_t(to_image(x['audio']['array']))*2-1 for x in examples]
    return torch.stack(audio_ims)

# 创建一个只包含Chiptune/Glitch风格的音乐
batch_size=4
# 设置训练风格
chosen_genre = 'Electronic'
indexes = [i for i, g in enumerate(dataset['genre']) if g == chosen_genre]
filtered_dataset = dataset.select(indexes)
filtered_dataset = filtered_dataset.select(range(100))
dl = torch.utils.data.DataLoader(filtered_dataset.shuffle(), batch_size=batch_size, collate_fn=collate_fn, shuffle=True)
batch = next(iter(dl))
print(batch.shape)

```

### 8.1.5 训练循环

下面的训练循环通过使用几个周期微调管线的UNet网络


```python
epochs = 3
lr = 1e-4

pipe.unet.train()
pipe.scheduler.set_timesteps(1000)
optimizer = torch.optim.AdamW(pipe.unet.parameters(), lr=lr)

for epoch in range(epochs):
    for step, batch in tqdm(enumerate(dl), total=len(dl)):
        # 输入图片
        clean_images = batch.to(device)
        bs = clean_images.shape[0]
        # 为每一张图片设置一个随机的时间步
        timesteps = torch.randint(
            0, pipe.scheduler.config.num_train_timesteps, (bs,), device=clean_images.device
        ).long()
        
        # 添加噪声
        noise = torch.randn(clean_images.shape).to(clean_images.device)
        noisy_images = pipe.scheduler.add_noise(clean_images, noise, timesteps)
        
        # 得到噪声预测
        noise_pred = pipe.unet(noisy_images, timesteps, return_dict=False)[0]
        
        # 计算损失
        loss = F.mse_loss(noise_pred, noise)
        loss.backward(loss)
        
        # 更新模型参数
        optimizer.step()
        optimizer.zero_grad()

```


```python
# 装载之前训练好的频谱样本，如图8-6所示
output = pipe()
display(output.images[0])
display(Audio(output.audios[0], rate=22050))

```


```python
# 输入一个不同形状的起点噪声张量，可以得到一个更长的频谱样本
noise = torch.randn(1, 1, pipe.unet.sample_size, pipe.unet.sample_size*4).to(device)
output = pipe(noise=noise)
display(output.images[0])
display(Audio(output.audios[0], rate=22050))

```

这个输出可能不是最佳结果，可以尝试调整学习率和迭代周期。


```python

```
