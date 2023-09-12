# 机器学习思考题目——09 Tensorflow常识

本文直译自《hands on ML》课后题。（有改动的以【】表示）。

## 1.用计算图的方法而不是直接执行计算的好处是什么？有哪些缺点？

主要优点：
（a）Tensorflow可以自动计算梯度（用reverse-mode autodiff）；
（b）Tensorflow可以用不同的进程并行运行这些操作；
（c）在不同的设备上运行同样的模型更方便；
（d）简化了自我检查（introspection）——例如，在tensorboard中查看模型。
主要缺点：
（a） It makes the learning curve steeper【貌似有点问题？没理解】
（b）提高了debugg的难度。

## 2.a_val = a.eval(session=sess)和a_val =sess.run(a)两个命令（的作用）是相等的么？

是的。

## 3.命令a_val, b_val = a.eval(session=sess), b.eval(session=sess)和 a_val, b_val = sess.run([a, b])的作用是否是一样的？

不一样。实际上，前者对计算图运行了两次（一次计算a，一次计算b），后者运行了计算图一次。如果图中的任何一个操作（或者它们依赖的操作）有副作用（side effects，例如变量被修改、一个元素被插入队列、reader读取了文件等等），那么影响也会不同。如果计算图中不会有副作用，两个命令返回相同的结果，但是后者会比前者更快。

## 4.可以在同一个session里面运行两个图么？

不能，此时只能把先把两个图merge成一个图才行。

## 5.一个图g中包含变量w，两个进程各自打开一个session，但二者用同一个图g。两个session是共享同一个w还是有各自的w？

（a）在本地的Tensorflow（local Tensorflow）中，session来管理变量值，因此题目中的情况是每个session有自己的w值。
（b）不过，在分布式Tensorflow（distributed Tensorflow）中，变量值是存储在集群管理的容器里（containers managed by the cluster），因此两个session是共享w值的。

## 6.（在tensorflow中）变量是什么时候被初始化的？是什么时候被销毁的（destroyed）？

当调用变量的initializer的时候变量被初始化，当session结束的时候被销毁。在分布式Tensorflow中，关闭一个session不会销毁变量，销毁变量需要清空（包含它的）容器（container）。

## 7.placeholder和variable的区别是什么？

二者是极其不同的，初学者常常混淆它们：
（a）variable是包含一个值的操作。如果运行variable，它返回这个值。在运行它之前，需要对它进行初始化。可以改变variable的值（例如，通过一个assignment操作）。variable的值在连续运行图的时候是不变的。它常用来保存模型参数（还有其他的用处，例如保存全局训练步数）。
（b）placeholder：它们只包含它们代表的tensor的type和shape等信息，但是不包含任何数值。事实上，如果需要evaluate一个依赖于某个placeholder的操作，必须告诉tensorflow这个placeholder的值（用feed_dict）,否则就会报错。placeholder常常用来给tensorflow输入训练数据和测试数据。它们也用来给一个分配节点（assignment node）传数据来改变变量的值（例如模型权重）。

## 8.运行计算图，去evaluate依赖一个placeholder的操作，如果不给placeholder赋值，结果会怎样？如果这个操作不依赖于placeholder呢？

前者会报错，后者不会报错。

## 9. When you run a graph, can you feed the output value of any operation, or just the value of placeholders?

When you run a graph, you can feed the output value of any operation, not just
the value of placeholders. In practice, however, this is rather rare (it can be useful,
for example, when you are caching the output of frozen layers of an auto-encoder).

## 10.在执行阶段（execution phase），如何按需改变一个variable的值？

在创建图的时候可以给一个variable设置一个初始值，执行阶段，当运行initializer的时候它会被初始化。执行阶段，想要改变variable的值的时候，最简单的办法是用tf.assign()函数设置一个assignment节点（在构建图的时候），给这个函数传输一个varibale和一个placeholder作为参数。在执行阶段，可以通过placeholder给变量赋一个新值。示例代码如下

```python
import tensorflow as tf
x = tf.Variable(tf.random_uniform(shape=(), minval=0.0, maxval=1.0))
x_new_val = tf.placeholder(shape=(), dtype=tf.float32)
x_assign = tf.assign(x, x_new_val)
with tf.Session():
	x.initializer.run() # random number is sampled *now*
	print(x.eval()) # 0.646157 (some random number)
	x_assign.eval(feed_dict={x_new_val: 5.0})
	print(x.eval()) # 5.0
123456789
```

## 11.对于有10个variable的损失函数，为了计算它的梯度的，如果用reverse-mode自动微分（autodiff）需要通过（tranverse）计算图几次？forward-mode自动微分呢？符号微分呢？

（a）对于包含任意数目变量的损失函数，reverse-mode自动微分(TensorFlow中的)只需要通过计算图2次。
（b）forward-mode自动微分对每一个变量（损失函数中的）都要通过一次（10个变量需要通过10次）。
（c）对于符号微分，计算梯度是另外一个计算图，因此它根本不需要穿过原图。一个高度优化的符号计算有可能只需要一次就计算出梯度（对所有的变量），但是这个图可能极度复杂。