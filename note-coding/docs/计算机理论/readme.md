# 计算器理论
---


### 1. 深入理解计算机系统

### 课后实验部署

```
docker实现lab:
# 查看
docker images
# 启动容器（里面有配置好的环境 和 PDF 资料）
docker run --name csapp -itd linxi177229/csapp 
# 进入容器 
docker attach csapp

# 接下来就和使用 平常的 Ubuntu：20.04 一样了
# 进入 lab1 进行一个简单的测试
cd ~
ls
cd csapplab
cd datalab/datalab-handout
make clean && make && ./btest

# 阅读pdf文档
sudo snap install evince
evince datalab.pdf  &  //打开pdf 
```

### 2. 汇编语言

### 3. 编译原理

### 4. 参考资料

- [深入理解计算机系统配套的9个lab](https://www.zhihu.com/column/c_1480603406519238656)
- [Computer Systems: A Programmer's Perspective](https://dreamanddead.github.io/CSAPP-3e-Solutions/chapter2/2.55/)
- [homework](https://dreamanddead.github.io/CSAPP-3e-Solutions/chapter2/2.55/)
- [CSAPP一键环境配置、完成8个lab总结](https://zhuanlan.zhihu.com/p/505497911)
- [ASCII码一览表，ASCII码对照表](http://c.biancheng.net/c/ascii/)
- [深入理解计算机系统》中文电子版（原书第 3 版）](https://hansimov.gitbook.io/csapp/)
- https://www.zhihu.com/people/222-75-24/columns
- https://blog.csdn.net/qq_39654127/article/details/88698911
- https://zhuanlan.zhihu.com/p/139785404
- https://zhuanlan.zhihu.com/p/380175489
- https://blog.csdn.net/tqdada/article/details/53132201
- https://blog.csdn.net/tenlee/article/details/48712177
- https://blog.csdn.net/qq_39654127/article/details/88698911