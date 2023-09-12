# 机器学习思考题目——13卷积神经网络（CNN）

本文直译自《hands on ML》课后题。（有改动的以【】表示）。



## 1.图片分类中，CNN相对于全连接的DNN有什么优势？

（a）由于只是局部连接，同时高度复用weight，CNN比全连接DNN少很多参数，这使得它训练更快，减少了过拟合的风险，需要的训练集小得多。
（b）当CNN学习到检测某个特征的核（kernel）的时候，它可以在图片的任何位置检测到这个特征。而DNN在某个位置学习到某个特征，它只能在这个位置识别它。由于图片一般有很多重复的特征，CNN在分类等领域可以用更少的训练集比DNN泛化地好得多。
（c）最后，DNN对于像素怎么组织的没有先验的知识；它不知道邻近的像素是相近的（nearby pixels are close）。CNN的架构嵌入了这一先验知识。较低层一般发现图片中小区域里的特征，较高层把这些低级别（lower-level）的特征组合成更大的特征。这适用于大多数自然图像，与DNN相比，CNN具有决定性优势。

## 2.考察一个由三个卷积层组成的CNN：kernel=3 × 3，stride=2，padding=SAME。 最低层输出100个特征映射（feature map），中间层200个特征映射，最高层400个特征映射。输入是200×300的RGB图片。那么：

**（a）CNN中参数的总数目是多少？
（b）如果用32-bit浮点数，在预测一个样本的时候，至少需要多大的RAM？
（c）如果用32-bit浮点数，用50张图片组成的mini-batch训练，至少需要多大RAM？**
***ANSWER：***
（a）
【第一层】由于第一个卷积层kernel=3×3，输入有3个通道（channel），因此每个特征映射有3×3×3个weight，加上bias，每个特征映射对应28个参数。由于第一层有100个特征映射，因此有2800个参数。
【第二层】第二层kernel=3×3，输入是前一层的100个特征映射，因此每个特征映射有3×3×100=900个weight，加上一个bias。由于共有200个特征映射，因此需要901×200=180200个参数。
【第三层】kernel=3×3，输入是前一层的200个特征映射，因此（第三层的）每个特征映射有3×3×200=1800个weight，加上bias。由于第三层有400个特征映射，因此这一层共有1801×400=720400个参数。
【总共】以上求和共有2800+180200+720400=903400个参数。
（b）当用一个样本进行预测的时候，首先计算每一层特征映射的大小。由于stride=2，同时padding=SAME，图片的长宽尺寸每层都要除以2（除不尽则取整），因此输入是200×300，第一层的特征映射是100×150，第二层的特征映射是50×75，第三层的特征映射是25×38（向上取整）。
由于32 bits=4 bytes，
第一层需要4×100×150×100=6million字节（大约5.7MB，1MB=1024KB）。
第二层需要4×50×75×200=3million字节（大约2.9MB）。
第三层需要4×25×38×400=1520000字节（大约1.4MB）。
每当一层算完之后，前一层占用的存储可以被释放。
因此如果经过细致的优化，只需要6+9=15million字节（大约14.3MB，当第二层算完之后，第一层占用的空间还没有释放）RAM。【这里貌似有问题，应该是6+3=9million字节吧？下面的答案应该减去2.9MB？】
除此之外，还要加上CNN的参数所占用的空间，由前述，需要903400个参数，每个4字节，因此共有3613600 字节（大约3.4MB）。
总计需要RAM（至少）18613600字节（大约17.8MB）。
（c）最后，当用50张图片的mini-batch进行训练的时候。训练过程中Tensorflow用反向传播，这需要反向通过计算图开始的时候，要保存所有计算过的数值。因此我们需要计算一个样本训练所需的总的RAM然后乘以50！前面计算了三层分别需要5.7、2.9、1.4MB。一个样本总计10MB，因此50个样本需要500MB。加上输入图片本身占用的空间，50×4×200×300×3=36million bytes（大约34.3MB），再加上模型参数3.4MB，加上梯度所占用的空间（忽略，因为随着反向传播的过程，逐渐释放了）。总共需要500+34.3+3.4=537.7MB。这是优化后的最小值了。

## 3.训练CNN的时候，你的GPU存储溢出，该怎么解决这个问题（不考虑购买更大RAM的GPU）？

（a）减小mini-batch的大小。
（b）在某一层或者多层中用一个更大的stride来减小维度。
（c）移除一层或者多层。
（d）用16-bit浮点数代替32-bit 浮点数。
（e）在多台设备上分布式计算。

## 4.为什么需要加入一个max pooling层，而不是相同stride的卷积层？

Max pooling层没有任何参数，而卷积层有参数（虽然很少）。

## 5. When would you want to add a local response normalization layer?

1. A local response normalization layer makes the neurons that most strongly acti‐
   vate inhibit neurons at the same location but in neighboring feature maps, which
   encourages different feature maps to specialize and pushes them apart, forcing
   them to explore a wider range of features. It is typically used in the lower layers to
   have a larger pool of low-level features that the upper layers can build upon.

## 6.AlexNet相对于LeNet-5有哪些主要创新？GoogLeNet相对于ResNet有哪些主要创新？

（1） AlexNet相对于LeNet-5主要创新：
　　（a）网络更深更大；
　　（b）它把卷积层直接堆叠到一起，而不是把pooling层放到每个卷积层的上面。
（2） GoogLeNet相对于ResNet主要创新：
　　（a）引入了inception模块，这使网络可以比以前的CNN结构更深，同时参数更少。
（3）补充：ResNet的主要创新是引入了skip connections，使得网络可以超过100层。可以说，它的简洁性和一致性也相当具有创新性。