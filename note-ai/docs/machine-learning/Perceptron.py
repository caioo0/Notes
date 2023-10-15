"""
该模块用于实现针对前馈神经网络的随机梯度下降算法。
通过反向传播算法计算梯度。注意，这里着重于让代码简单易读且易于修改，
并没有进行优化，略去了不少可取的特性。
"""

# 标准库
import random

# 第三方库
import numpy as np

class Network(object):
    def __init__(self):
    """
    列表sizes包含对应层的神经元的数目。
    """
    self.num_layaers = len(sizes)
    self.sizes = sizes
    self.biases = [np.random.randn(y,1)] for y in sizes[1:]]
    self.weights = [np.random.randn(y,x)
                  for x,y in zip(sizes[:-1],sizes[1:])]

    def feedforward(self,a):
    """
    若 a 为输入，则返回输出。
    """
    for b,w in zip(self.biases,self.weights):
        a = sigmoid(np.dot(w,a) + b )
    return a

    def SGD(self,traing_data,epochs,mini_batch_size,eta,test_data=None):
        """
        使用小批量随机梯度下降算法训练神经网络。
        train_data是由
        """





