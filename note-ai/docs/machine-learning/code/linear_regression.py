import numpy as np
import pandas as pd

### 初始化模型参数
def initialze_params(dims):
    '''
    输入：
    dims: 训练数据变量维度
    输出：
    w: 初始化权重参数值
    b: 初始化偏差参数值
    '''
    # 初始化权重参数为零矩阵
    w = np.zeros((dims,1))
    # 初始化偏差参数为零
    b = 0
    return w,b

### 定义模型主体部分
### 包含线性回归公式、均方损失和参数偏导三部分
def linear_loss(X,y,w,b):
    """
    输入
    :param X: 输入变量矩阵
    :param y: 输出标签向量
    :param w: 变量参数权重矩阵
    :param b: 偏差项
    输出
    :param y_hat:线性模型预测输出
    :param loss:均方损失值
    :param dw:权重参数一阶偏导
    :param db: 偏差项一阶偏导
    """
    # 训练样本数量
    num_train = X.shape[0]
    # 训练特征数量
    num_feature = X.shape[1]
    # 线性回归预测输出
    y_hat = np.dot(X,w) +b
    # 计算预测输出与实际标签之间的均方损失
    loss = np.sum((y_hat - y)**2)/num_train
    # 基于均方损失对权重参数的一阶偏导数
    dw = np.dot(X.T,(y_hat -y))/num_train
    # 基于均方损失对偏差项的一阶偏导数
    db = np.sum((y_hat-y))/num_train
    return y_hat,loss,dw,db

### 定义线性回归模型训练过程
def linear_train(X,y,learning_rate = 0.01, epochs = 10000):
    '''
     输入：
     X：输入变量矩阵
     y：输出标签向量
     learning_rate：学习率
     epochs：训练迭代次数
     输出：
     loss_his：每次迭代的均方损失
     params：优化后的参数字典
     grads：优化后的参数梯度字典
     '''
    # 记录训练损失的空列表
    loss_his = []
    # 初始化模型参数
    w,b = initialze_params(X.shape[1])
    # 迭代训练
    for i in range(1,epochs):
        # 计算当前迭代的预测值，损失和梯度
        y_hat,loss,dw,db = linear_loss(X,y,w,b)
        # 基于梯度下降的参数更新
        w += -learning_rate * dw
        b += -learning_rate * db
        # 记录当前迭代的损失
        loss_his.append(loss)
        # 每迭代1000次打印当前损失信息
        if i % 1000 ==0:
            print("epoch %d loss %f" % (i,loss))
        # 将当前迭代步优化后的参数保存到字典
        params = {
            'w':w,
            'b':b
        }
        # 将当前迭代步的梯度保存到字典
        grads = {
            'dw':dw,
            'db':db
        }
        return loss_his,params,grads

from sklearn.datasets import load_diabetes
diabetes = load_diabetes()
data = diabetes.data
target = diabetes.target
print(data.shape)
print(target.shape)
print(data[:5])
print(target[:5])

# 导入skearn diabetes 数据接口
from sklearn.datasets import load_disabetes
# 导入skearn打乱数据函数 
