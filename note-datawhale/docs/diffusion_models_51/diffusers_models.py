import torch
import torchvision
from torch import nn
from torch.nn import functional as F
from torch.utils.data import DataLoader
from diffusers import DDPMScheduler,UNet2DModel
from matplotlib import pyplot as plt

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# 数据集测试
dataset = torchvision.datasets.MNIST(root="mnist/",train=True,download=True,
                                     transform = torchvision.transforms.ToTensor())
train_dataloader = DataLoader(dataset,batch_size=8,shuffle=True)
X,y = next(iter(train_dataloader))

print('Input shape:',X.shape)
print('Labels:',y)

plt.imshow(torchvision.utils.make_grid(X)[0],cmap='Greys')

# noise = torch.rand_like(X)
# print(noise)
# noise_x = (1-amount)*x + amount *noise
# print(noise_x)

def corrupt(x,amount):
    """根据amount为输入x加入噪声，这就是退化过程"""
    noise = torch.rand_like(x)
    amount = amount.view(-1,1,1,1) # 整理形状以保证广播机制不出错
    return x*(1-amount) + noise*amount

# 绘制输入数据
fig ,axs = plt.subplots(2,1,figsize=(12,5))
axs[0].set_title('input data')
axs[0].imshow(torchvision.utils.make_grid(X)[0],cmap='Greys')

# 加入噪声
amount = torch.linspace(0,1,X.shape[0]) # 从0到1 -> 退化更强烈
noise_x = corrupt(X,amount)

# 绘制加噪版本的图像
axs[1].set_title('Corrupted data (-- amount invreases -->)')
axs[1].imshow(torchvision.utils.make_grid(noise_x)[0],cmap='Greys')


