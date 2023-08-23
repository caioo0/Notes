# 阿里的OneData理论进行数据仓库建设


## OneData 介绍

OneData是阿里巴巴多年大数据开发和治理实践中沉淀总结的方法论，包含OneModel,OneService,OneID 三个概念。

用于解决 数据治理 中的以下问题：

- **数据孤岛：** 各产品、业务的数据相互隔离，难以通过共性ID打通；
- **重复建设：** 重复的开发、计算、存储，带来高昂的数据成本；
- **数据歧义：**指标定义口径不一致，造成计算偏差，应用困难；

![在这里插入图片描述](https://img-blog.csdnimg.cn/8b7ea812312a437585c0376d8e046850.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBA5p625p6E5biI5b-g5ZOl,size_20,color_FFFFFF,t_70,g_se,x_16)
