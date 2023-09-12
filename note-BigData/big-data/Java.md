# **Java核心基础**

## 0.1 Java简介

### 0.1.1 为什么要学习Java语言

- 使用最广泛, 且简单易学
- Java是一门强类型的语言
- Java有非常完善的异常处理机制
- Java提供了对于大数据的基础性支持

### 0.1.2 概述

- Sun公司(Stanford University NetWork): 美国的斯坦福大学)在1995年推出的高级编程语言.
- Java之父: 詹姆斯·高斯林(James Gosling)
- Sun公司在2009年被甲骨文(Oracle)公司给收购了.

![image-20230824095707192](.\images\image-20230824095707192.png)

### 0.1.3 平台版本

- **J2SE: 标准版,** 也是其他两个版本的基础. 在JDK1.5的时候正式更名为: JavaSE.
- J2ME: 小型版, 一般用来研发嵌入式程序. 已经被Android替代了. 在JDK1.5的时候正式更名为: JavaME.
- J2EE: 企业版, 一般开发企业级互联网程序. 在JDK1.5的时候正式更名为: JavaEE.

### 0.1.4 特点

- 开源

- - 指的是Java源代码是开放的. 

- 跨平台

- - 指的是: 用Java代码编写的程序, 可以在不同的操作系统上运行. 
  - **原理:** 由JVM保证Java程序的跨平台性, 但是JVM本身并不能跨平台. 
  - 图解: 

![image-20230824100013870](.\images\image-20230824100013870.png)

- 多态
- 多线程
- 面向对象

## 0.2 Java环境搭建

### 0.2.1 JDK和JRE的概述

- JDK: Java开发工具包(Java Development Kit), 包含开发工具 和 JRE.

- - 常用的开发工具: javac, java

- JRE: Java运行时环境(Java Runtime Environment), 包含运行Java程序时所需的核心类库和 JVM.

- - 核心类库: java.lang, java.util, java.io

- JVM: Java虚拟机(Java Virtual Machine)

- - 作用: 用来保证Java程序跨平台性的, 但是JVM本身并不能跨平台.

### 0.2.2 JDK和JRE的图解

![image-20230824100150322](.\images\image-20230824100150322.png)

### 0.2.3 JDK的下载和安装 

- JDK的下载 

- - Oracle官网: [www.oracle.com](http://www.oracle.com)
  - 直接下载JDK的地址: 	https://www.oracle.com/java/technologies/javase/javase-jdk8-downloads.html

- JDK的安装

1. 1. 傻瓜式安装(下一步下一步就可以了)
   2. 安装路径(以后但凡是安装开发软件, 都要满足以下两点: )

- - - 不要直接安装到盘符目录下. 
    - 安装路径最好不要出现中文, 空格等特殊符号. 

1. 1. 目录解释:

- - - bin: 存放的是编译器和工具
    - db: 存数数据
    - include: 编译本地方法.
    - jre: Java运行时文件
    - lib: 存放类库文件
    - src.zip: 存放源代码的.

- JDK的卸载
- 去控制面板直接卸载就可以了. 
- windows环境下: windows徽标键 + 字母R -> control -> 然后敲回车, 这样可以直接打开控制面板.

### 0.2.4 Path环境变量配置

#### 0.2.4.1 目的

让我们可以在任意目录下都能使用**JDK提供的常用开发工具, 例如: javac, java**

#### 0.2.4.2 步骤

1. 新建一个系统变量: JAVA_HOME, 它的值就是你安装的JDK的路径(注意: 不要带bin这一级)

![image-20230824100518477](.\images\image-20230824100518477.png)

- 注意: 变量值不要带bin目录.

1. 在path中配置你刚才设置好的JAVA_HOME环境变量.

- 格式:  %JAVA_HOME%\bin  
- 解释: %JAVA*HOME%表示引入该系统变量的值, 即: C:\Software\OfficeSoftware\jdk1.8.0*112

1. 测试

- - 方式一: 在DOS窗口中输入"javac 或者 java", 能看到对应的一坨指令即可.
  - 方式二: 在DOS窗口中输入"java -version", 可以看到当前配置的JDK的版本. 

![image-20230824100634978](.\images\image-20230824100634978.png)

### 0.2.5 HelloWorld案例

#### 0.2.5.1 程序的开发步骤

Java程序的开发步骤一共3步, 分别是: 

- 编写
- 编译
- 执行

<img src=".\images\image-20230824101025087.png" alt="image-20230824101025087" style="zoom:50%;" />

1. 编写源代码： 相当于编写一些指令，在后缀名.java的源文件中编写。
2. 编译：通过**javac指令**:`javac HelloWorld.java`实现编译：HelloWord.java(源代码文件) ---> HelloWorld.class (字节码文件，计算机)
3. 运行：让计算机运行指定的字节码文件，使用命令：` java HelloWorld`。

#### 0.2.5.2 编写源代码

1. 中创建HelloWorld.java文件.
2. 用记事本打开HelloWorld.java文件.
3. 在HelloWorld.java文件中编写如下内容:

```java
public class HelloWorld {
	public static void main(String[] args) {
		    	System.out.println("Hello World!");
		    System.out.println("你好, 欢迎来到我的直播间, 记得刷礼物喲!");
 	}
}
```

- 注意: HelloWorld.java叫源代码文件, 是我们能看懂, 但是计算机看不懂的文件.

#### 0.2.5.3 编译

通过javac指令将HelloWorld.java文件编译成HelloWorld.class字节码文件.

**格式**

//在DOS窗口中输入如下内容: 

javac HelloWorld.java

#### 0.2.5.4 执行

通过java指令, 让计算机执行HelloWorld.class字节码文件.

**格式**

//在DOS窗口中输入如下内容: 

java HelloWorld

注意: 直接写文件名即可, 不需要写文件后缀名, 即: .class

#### 0.2.5.5 可能会遇到的问题

**Bug**

- 概述
- 在电脑系统或程序中，隐藏着的一些未被发现的缺陷或问题统称为bug（漏洞）
- 解决方案
- 多看, 多思考, 多尝试, 多总结

**遇到的问题**

   非法字符.

- 注意: 我们使用的符号全部都是**英文状态下的符号**

   注意字母的大小写.

- 注意: Java是严格区分大小写的. 也就是说: A和a不是一回事儿.

   文件后缀名的问题.

- 千万不要出现 `HelloWorld.java.txt` 这种情况 

   在编译或者运行时, 指令及文件名不要写错了.

- //编译的格式
  `javac HelloWorld.java`
  //运行的格式
  `java HelloWorld`

## 0.3 IDEA的使用

### 0.3.1 概述

IDEA 全称 IntelliJ IDEA，是Java编程语言开发的集成环境。IntelliJ在业界被公认为最好的java开发工具，尤其在智能代码助手、代码自动提示、重构、J2EE支持、各类版本工具(git、svn等)、JUnit、CVS整合、代码分析、 创新的GUI设计等方面的功能可以说是超常的。IDEA是JetBrains公司的产品，这家公司总部位于捷克共和国的首都布拉格，开发人员以严谨著称的东欧程序员为主。它的旗舰版本还支持HTML，CSS，PHP，MySQL，Python等。免费版只支持Python等少数语言。

总结: **IDEA这个软件是用ava语言开发的, 所以想使用IDEA, 你电脑上必须安装JRE.** 

### 0.3.2 下载地址 

JetBrains公司官网: www.jetbrains.com

直接下载地址: www.jetbrains.com/idea/download/other.html  

### 0.3.3 安装

安装步骤这里省略，永久使用版本方法省略



### 0.3.4 创建项目和模块

1. IDEA版项目组成简介.

- 简单理解: 一个Java程序 = 一个IDEA中创建的项目.
- ![img](https://cdn.nlark.com/yuque/0/2023/png/28122275/1678518071036-e73d3f63-26b2-4042-92d8-30010ab7f139.png?x-oss-process=image%2Fwatermark%2Ctype_d3F5LW1pY3JvaGVp%2Csize_35%2Ctext_55-l6K-G5pif55CDQOWkp-aVsOaNruaKgOacr-WtpumZog%3D%3D%2Ccolor_FFFFFF%2Cshadow_50%2Ct_80%2Cg_se%2Cx_10%2Cy_10)



1. 选择Create New Project, 新建项目.

- ![img](https://cdn.nlark.com/yuque/0/2023/png/28122275/1678518071327-3ac9a9da-2fe0-460e-9b4d-5784a693cc8b.png?x-oss-process=image%2Fwatermark%2Ctype_d3F5LW1pY3JvaGVp%2Csize_19%2Ctext_55-l6K-G5pif55CDQOWkp-aVsOaNruaKgOacr-WtpumZog%3D%3D%2Ccolor_FFFFFF%2Cshadow_50%2Ct_80%2Cg_se%2Cx_10%2Cy_10)



1. 新建一个空项目.

- ![img](https://cdn.nlark.com/yuque/0/2023/png/28122275/1678518071780-a9b7726f-69cb-456b-bdca-824f301f5118.png?x-oss-process=image%2Fwatermark%2Ctype_d3F5LW1pY3JvaGVp%2Csize_20%2Ctext_55-l6K-G5pif55CDQOWkp-aVsOaNruaKgOacr-WtpumZog%3D%3D%2Ccolor_FFFFFF%2Cshadow_50%2Ct_80%2Cg_se%2Cx_10%2Cy_10)



1. 指定项目名和项目的保存位置.

- ![img](https://cdn.nlark.com/yuque/0/2023/png/28122275/1678518072141-b3949c15-8702-4493-979a-dbcc326a216e.png?x-oss-process=image%2Fwatermark%2Ctype_d3F5LW1pY3JvaGVp%2Csize_20%2Ctext_55-l6K-G5pif55CDQOWkp-aVsOaNruaKgOacr-WtpumZog%3D%3D%2Ccolor_FFFFFF%2Cshadow_50%2Ct_80%2Cg_se%2Cx_10%2Cy_10)



1. 新建模块.

- ![img](https://cdn.nlark.com/yuque/0/2023/png/28122275/1678518072493-0fc89290-dbe2-4b82-9811-dd596b8db41c.png?x-oss-process=image%2Fwatermark%2Ctype_d3F5LW1pY3JvaGVp%2Csize_29%2Ctext_55-l6K-G5pif55CDQOWkp-aVsOaNruaKgOacr-WtpumZog%3D%3D%2Ccolor_FFFFFF%2Cshadow_50%2Ct_80%2Cg_se%2Cx_10%2Cy_10)



1. 第一次使用IDEA, 需要关联JDK.

- ![img](https://cdn.nlark.com/yuque/0/2023/png/28122275/1678518072837-47bb42c9-c216-41e5-9edc-3cbe67af267a.png?x-oss-process=image%2Fwatermark%2Ctype_d3F5LW1pY3JvaGVp%2Csize_20%2Ctext_55-l6K-G5pif55CDQOWkp-aVsOaNruaKgOacr-WtpumZog%3D%3D%2Ccolor_FFFFFF%2Cshadow_50%2Ct_80%2Cg_se%2Cx_10%2Cy_10)



1. 创建Java模块.

- ![img](https://cdn.nlark.com/yuque/0/2023/png/28122275/1678518073198-bafb007c-c6ff-462f-83f8-29d62c83cb3e.png?x-oss-process=image%2Fwatermark%2Ctype_d3F5LW1pY3JvaGVp%2Csize_20%2Ctext_55-l6K-G5pif55CDQOWkp-aVsOaNruaKgOacr-WtpumZog%3D%3D%2Ccolor_FFFFFF%2Cshadow_50%2Ct_80%2Cg_se%2Cx_10%2Cy_10)



1. 指定模块名和路径, 然后选择Finish.

- ![img](https://cdn.nlark.com/yuque/0/2023/png/28122275/1678518073788-6dc460bb-9837-42e0-ad42-dd4a07a29018.png?x-oss-process=image%2Fwatermark%2Ctype_d3F5LW1pY3JvaGVp%2Csize_20%2Ctext_55-l6K-G5pif55CDQOWkp-aVsOaNruaKgOacr-WtpumZog%3D%3D%2Ccolor_FFFFFF%2Cshadow_50%2Ct_80%2Cg_se%2Cx_10%2Cy_10)



1. 第一次创建模块时, 如果模块没有自动关联JDK, 则需要我们手动设置下关联.

- ![img](https://cdn.nlark.com/yuque/0/2023/png/28122275/1678518074267-b1cf4215-5a52-4d13-9d79-deb7e50f030d.png?x-oss-process=image%2Fwatermark%2Ctype_d3F5LW1pY3JvaGVp%2Csize_29%2Ctext_55-l6K-G5pif55CDQOWkp-aVsOaNruaKgOacr-WtpumZog%3D%3D%2Ccolor_FFFFFF%2Cshadow_50%2Ct_80%2Cg_se%2Cx_10%2Cy_10)



1. 设好以后, 格式如下, 至此, 模块创建完毕.

![img](https://cdn.nlark.com/yuque/0/2023/png/28122275/1678518074557-b9d6e18a-d3ea-48c7-b147-21d512ce179e.png?x-oss-process=image%2Fwatermark%2Ctype_d3F5LW1pY3JvaGVp%2Csize_29%2Ctext_55-l6K-G5pif55CDQOWkp-aVsOaNruaKgOacr-WtpumZog%3D%3D%2Ccolor_FFFFFF%2Cshadow_50%2Ct_80%2Cg_se%2Cx_10%2Cy_10)

1. 第一次进入到项目界面, 会弹出如下对话框. 

![img](https://cdn.nlark.com/yuque/0/2023/png/28122275/1678518074881-eb627c40-1d91-4aa7-84ab-15ded020b4f7.png?x-oss-process=image%2Fwatermark%2Ctype_d3F5LW1pY3JvaGVp%2Csize_17%2Ctext_55-l6K-G5pif55CDQOWkp-aVsOaNruaKgOacr-WtpumZog%3D%3D%2Ccolor_FFFFFF%2Cshadow_50%2Ct_80%2Cg_se%2Cx_10%2Cy_10)



### 0.3.5 HelloWorld案例(IDEA版)

1. 在src源代码包下创建自定义包 com.itheima.demo01

- ![img](https://cdn.nlark.com/yuque/0/2023/png/28122275/1678518075283-e93ee4f9-23d4-427b-94ec-bf8c48e7f5d4.png?x-oss-process=image%2Fwatermark%2Ctype_d3F5LW1pY3JvaGVp%2Csize_22%2Ctext_55-l6K-G5pif55CDQOWkp-aVsOaNruaKgOacr-WtpumZog%3D%3D%2Ccolor_FFFFFF%2Cshadow_50%2Ct_80%2Cg_se%2Cx_10%2Cy_10)





![img](https://cdn.nlark.com/yuque/0/2023/png/28122275/1678518075538-c28980f8-1d70-4b72-a3e8-8de752e12533.png?x-oss-process=image%2Fwatermark%2Ctype_d3F5LW1pY3JvaGVp%2Csize_11%2Ctext_55-l6K-G5pif55CDQOWkp-aVsOaNruaKgOacr-WtpumZog%3D%3D%2Ccolor_FFFFFF%2Cshadow_50%2Ct_80%2Cg_se%2Cx_10%2Cy_10)

1. 在com.itheima.demo01包下创建HelloWorld类. 

![img](https://cdn.nlark.com/yuque/0/2023/png/28122275/1678518076001-68540486-3268-4649-820d-677c7fbbaf4f.png?x-oss-process=image%2Fwatermark%2Ctype_d3F5LW1pY3JvaGVp%2Csize_24%2Ctext_55-l6K-G5pif55CDQOWkp-aVsOaNruaKgOacr-WtpumZog%3D%3D%2Ccolor_FFFFFF%2Cshadow_50%2Ct_80%2Cg_se%2Cx_10%2Cy_10)





![img](https://cdn.nlark.com/yuque/0/2023/png/28122275/1678518076525-14f5c81c-ce76-4fcd-a392-3c87eb7b7b58.png?x-oss-process=image%2Fwatermark%2Ctype_d3F5LW1pY3JvaGVp%2Csize_15%2Ctext_55-l6K-G5pif55CDQOWkp-aVsOaNruaKgOacr-WtpumZog%3D%3D%2Ccolor_FFFFFF%2Cshadow_50%2Ct_80%2Cg_se%2Cx_10%2Cy_10)

1. 编写源代码, 然后在代码编辑区右键, 选择Run HelloWorld.main(), 执行程序即可.

![img](https://cdn.nlark.com/yuque/0/2023/png/28122275/1678518077061-002230b5-d511-4794-8124-9e7b6f4afd13.png?x-oss-process=image%2Fwatermark%2Ctype_d3F5LW1pY3JvaGVp%2Csize_23%2Ctext_55-l6K-G5pif55CDQOWkp-aVsOaNruaKgOacr-WtpumZog%3D%3D%2Ccolor_FFFFFF%2Cshadow_50%2Ct_80%2Cg_se%2Cx_10%2Cy_10)



1. 如果提示错误: 找不到或无法加载主类 com.itheima.demo01.HelloWorld, 则修改下项目语言级别即可, 然后重启下IDEA.

具体步骤: 

左上角的File -> Project Structure -> Project -> 修改Project SDK和Project language level两个选项的值 -> 然后关闭IDEA软件, 重新打开即可.

图解:

![img](https://cdn.nlark.com/yuque/0/2023/png/28122275/1678518077551-5410f9e7-1ef1-4276-9eb0-c240fc6171b5.png?x-oss-process=image%2Fwatermark%2Ctype_d3F5LW1pY3JvaGVp%2Csize_12%2Ctext_55-l6K-G5pif55CDQOWkp-aVsOaNruaKgOacr-WtpumZog%3D%3D%2Ccolor_FFFFFF%2Cshadow_50%2Ct_80%2Cg_se%2Cx_10%2Cy_10)





![img](https://cdn.nlark.com/yuque/0/2023/png/28122275/1678518078062-02b5ba3e-961b-40a6-9fae-acc70e1610d7.png?x-oss-process=image%2Fwatermark%2Ctype_d3F5LW1pY3JvaGVp%2Csize_25%2Ctext_55-l6K-G5pif55CDQOWkp-aVsOaNruaKgOacr-WtpumZog%3D%3D%2Ccolor_FFFFFF%2Cshadow_50%2Ct_80%2Cg_se%2Cx_10%2Cy_10)



1. 目录解释. 

![img](https://cdn.nlark.com/yuque/0/2023/png/28122275/1678518078582-bdb15eec-bc93-4fa2-9cb8-0090510ad39b.png?x-oss-process=image%2Fwatermark%2Ctype_d3F5LW1pY3JvaGVp%2Csize_23%2Ctext_55-l6K-G5pif55CDQOWkp-aVsOaNruaKgOacr-WtpumZog%3D%3D%2Ccolor_FFFFFF%2Cshadow_50%2Ct_80%2Cg_se%2Cx_10%2Cy_10)



### 0.3.6 .基本配置和常用快捷键

#### 0.3.6.1 基本配置, 详见下图: 

![img](https://cdn.nlark.com/yuque/0/2023/png/28122275/1678518079084-e3e2dfcf-fbc1-49bf-aaab-9d5e7a6ce476.png?x-oss-process=image%2Fwatermark%2Ctype_d3F5LW1pY3JvaGVp%2Csize_14%2Ctext_55-l6K-G5pif55CDQOWkp-aVsOaNruaKgOacr-WtpumZog%3D%3D%2Ccolor_FFFFFF%2Cshadow_50%2Ct_80%2Cg_se%2Cx_10%2Cy_10)



#### 0.3.6.2 注意

隐藏不需要的文件, 需要在界面的lgnore files and folders选项值后加*.idea;*.iml;out;即可.

#### 0.3.63 IDEA常用快捷键

常用的快捷键如下图:

![img](https://cdn.nlark.com/yuque/0/2023/png/28122275/1678518079579-03911a64-9c33-483a-84ea-54ed3a0cb784.png?x-oss-process=image%2Fwatermark%2Ctype_d3F5LW1pY3JvaGVp%2Csize_26%2Ctext_55-l6K-G5pif55CDQOWkp-aVsOaNruaKgOacr-WtpumZog%3D%3D%2Ccolor_FFFFFF%2Cshadow_50%2Ct_80%2Cg_se%2Cx_10%2Cy_10)



### 0.3.7 导入和删除模块

#### 0.3.7.1 删除项目

选择要移除的项目, 然后右键点击, 选择Remove Module, 即可移除该模块.

![img](https://cdn.nlark.com/yuque/0/2023/png/28122275/1678518080152-0876081d-ee8d-4867-a83b-5280f0b19305.png?x-oss-process=image%2Fwatermark%2Ctype_d3F5LW1pY3JvaGVp%2Csize_17%2Ctext_55-l6K-G5pif55CDQOWkp-aVsOaNruaKgOacr-WtpumZog%3D%3D%2Ccolor_FFFFFF%2Cshadow_50%2Ct_80%2Cg_se%2Cx_10%2Cy_10)



#### 3.7.2 导入模块

选择IDEA软件左上角的File选项, 然后选择Project Structured, 选择Modules, 选择+(加号), 然后选择Import Module, 然后导入指定模块即可.

![img](https://cdn.nlark.com/yuque/0/2023/png/28122275/1678518080643-cbc1d92e-bfa8-4472-9b12-e67f10e6b54a.png?x-oss-process=image%2Fwatermark%2Ctype_d3F5LW1pY3JvaGVp%2Csize_26%2Ctext_55-l6K-G5pif55CDQOWkp-aVsOaNruaKgOacr-WtpumZog%3D%3D%2Ccolor_FFFFFF%2Cshadow_50%2Ct_80%2Cg_se%2Cx_10%2Cy_10)



![img](https://cdn.nlark.com/yuque/0/2023/png/28122275/1678518081413-e9d5891c-cf8b-45b3-b0d9-910d8ab37640.png?x-oss-process=image%2Fwatermark%2Ctype_d3F5LW1pY3JvaGVp%2Csize_20%2Ctext_55-l6K-G5pif55CDQOWkp-aVsOaNruaKgOacr-WtpumZog%3D%3D%2Ccolor_FFFFFF%2Cshadow_50%2Ct_80%2Cg_se%2Cx_10%2Cy_10)





![img](https://cdn.nlark.com/yuque/0/2023/png/28122275/1678518081708-baeab0b3-f8b6-43ee-a8d5-e94b6eaa5e82.png?x-oss-process=image%2Fwatermark%2Ctype_d3F5LW1pY3JvaGVp%2Csize_20%2Ctext_55-l6K-G5pif55CDQOWkp-aVsOaNruaKgOacr-WtpumZog%3D%3D%2Ccolor_FFFFFF%2Cshadow_50%2Ct_80%2Cg_se%2Cx_10%2Cy_10)





![img](https://cdn.nlark.com/yuque/0/2023/png/28122275/1678518082181-b3b65d78-45a0-43a1-8f3b-fb812b63ce1c.png?x-oss-process=image%2Fwatermark%2Ctype_d3F5LW1pY3JvaGVp%2Csize_20%2Ctext_55-l6K-G5pif55CDQOWkp-aVsOaNruaKgOacr-WtpumZog%3D%3D%2Ccolor_FFFFFF%2Cshadow_50%2Ct_80%2Cg_se%2Cx_10%2Cy_10)





![img](https://cdn.nlark.com/yuque/0/2023/png/28122275/1678518082452-4da4a863-c423-4450-a957-084a7e3e95d5.png?x-oss-process=image%2Fwatermark%2Ctype_d3F5LW1pY3JvaGVp%2Csize_20%2Ctext_55-l6K-G5pif55CDQOWkp-aVsOaNruaKgOacr-WtpumZog%3D%3D%2Ccolor_FFFFFF%2Cshadow_50%2Ct_80%2Cg_se%2Cx_10%2Cy_10)





![img](https://cdn.nlark.com/yuque/0/2023/png/28122275/1678518082750-97474742-4cb9-480e-bf4c-558ff678efc2.png?x-oss-process=image%2Fwatermark%2Ctype_d3F5LW1pY3JvaGVp%2Csize_20%2Ctext_55-l6K-G5pif55CDQOWkp-aVsOaNruaKgOacr-WtpumZog%3D%3D%2Ccolor_FFFFFF%2Cshadow_50%2Ct_80%2Cg_se%2Cx_10%2Cy_10)





![img](https://cdn.nlark.com/yuque/0/2023/png/28122275/1678518083290-b33b7d2a-269a-4b53-94ec-0c911aef3252.png?x-oss-process=image%2Fwatermark%2Ctype_d3F5LW1pY3JvaGVp%2Csize_26%2Ctext_55-l6K-G5pif55CDQOWkp-aVsOaNruaKgOacr-WtpumZog%3D%3D%2Ccolor_FFFFFF%2Cshadow_50%2Ct_80%2Cg_se%2Cx_10%2Cy_10)



## 0.4 Java核心基础

### 0.4.1 注释

#### 0.4.1.1 概述

就是用来对程序进行解释和说明的文字.

大白话翻译: 注释是给我们程序员看的, 并不是给计算机看的. 

#### 0.4.1.2 分类

```shell
//单行注释
----------------
/*
	多行注释
	多行注释
*/
----------------
/**
	文档注释
	文档注释
*/
----------------
```

### 0.4.2 关键字

#### 0.4.2.1 概述

就是被Java语言赋予了特殊含义的单词. 

#### 0.4.2.2 特点

- 关键字是由纯英文字母组成的, 而且全部都是小写的.
- 常用的开发工具(Notepad++, IDEA)针对于关键字都会高亮显示.

#### 0.4.2.3 常用的关键字

- public: 公共的权限, 目前先了解即可.
- class: 表示在创建一个类.
- static: 表示静态的意思.
- void: 表示方法的返回值类型.

### 0.4.3 常量

#### 0.4.3.1 概述

指的是在程序的执行过程中, 其值不能发生改变的量.



#### 0.4.3.2 分类

- 自定义常量(目前先了解, 在面向对象的时候, 才会详细解释)
- 字面值常量

- 解释: 根据字面意思就可以划分的常量.

1. 1. 整数常量.

- - 例如: 1, 2, 3, 11, 22, 521

1. 1. 小数常量.

- - 例如: 5.21, 13.14

1. 1. 字符常量.

- - 解释: 字符的意思是说只能有一个值, 而且要用单引号括起来
  - 例如: 'A', 'B', 'c', '10'(这样写会报错, 因为10是由1和0两个值组成的)

1. 1. 字符串常量.

- - 解释: 字符串常量值都要用双引号括起来
  - 例如: "abc", "五分钟学大数据", "大数据"

1. 1. 布尔常量

- - 解释: 比较特殊, 值只有两个

- - - true, 相当于正确
    - false, 相当于不正确

1. 1. 空常量

- - 解释: 比较特殊, 值只有一个: null, 表示什么都没有.
  - 注意: 空常量不能通过输出语句直接打印. 

- 

### 0.4.4 变量

#### 0.4.4.1 概述

- 在程序的执行过程中, 其值可以在某个范围内发生改变的量就叫变量. 
  
- Java中要求一个变量每次只能保存一个数据，而且必须要明确保存数据的数据类型。
  
- #### 0.4.4.2 格式

- 方式一: 声明变量并赋值. 
  
  - 数据类型 变量名 = 初始化值;

```java
  //示例: 声明(定义)一个int类型的变量, 变量名叫a, 初始化值为: 10
  int a = 10;
```

- - 方式二: 先声明, 后赋值.
  - 数据类型 变量名;
  - 变量名 = 初始化值;

- ```java
  //示例
  //1. 声明(定义)一个int类型的变量, 变量名叫a
  int a;						
  //2. 把数字10赋值给变量a	  
  a = 10;
  ```

- - **解释:**

- - - **数据类型：**变量变化的范围就是数据类型
    - **变量名：**每个变量都有一个名字，方便存取。
    - **初始化值：**使用变量前，需要给变量赋值。

#### 0.4.4.3 示例一: 变量入门

- **需求**

- 定义变量, 记录班级的学生人数, 并将结果打印到控制台上.

- **参考代码**

- ```
  //1. 定义一个Java类, 类名叫: VariableDemo01
  public class VariableDemo01 {
      //2. 定义main方法, 作为程序的主入口, 所有代码都是从这里开始执行的.
      public static void main(String[] args) {
          //3. 定义一个int类型的变量, 变量名叫a, 初始化值为: 121
          int a = 121;
          //4. 通过输出语句, 将变量a的值打印到控制台上. 
          System.out.println(a);
      }
  }
  ```

#### 0.4.4.4 数据类型详解

##### 0.4.4.4.1 概述

- Java是一种强类型语言, 针对于每一个数据都给出了明确的数据类型.

- 解释:

- 区分一门语言到底是强类型语言还是弱类型语言的依据是: 看这门语言对数据的数据类型划分是否精细.

- 如果精细, 则是强类型语言, 如果不精细, 则是弱类型语言. 

- ##### 0.4.4.4.2 数据类型的分类

- - 基本数据类型(简称: 基本类型) 

- - - byte, short, char, int, long, float, double, boolean

- - 引用数据类型(简称: 引用类型)

- - - String, 数组, 类, 接口, 目前先了解, 后续会详细讲解. 

- ##### 0.4.4.4.3 数据类型的分类图解

- ![image-20230824135421412](.\images\image-20230824135421412.png)

##### 0.4.4.4.4 数据类型的取值范围图解

![image-20230824135452759](.\images\image-20230824135452759.png)

**记忆**

1. byte类型的取值范围是: **-128 ~ 127**,char类型的取值范围是: **0 ~ 65535**
2. 默认的整形是: int类型, 默认的浮点型(即: 小数类型)是: double类型.
3. 定义long类型的数据时, 数据后边要加字母L(大小写均可), 建议加L
4. 定义float类型的数据时, 数据后边要加字母F(大小写均可), 建议加F

#### 0.4.4.5 示例二: 定义变量并打印

**需求** 定义变量, 分别记录上述的8种基本类型数据, 并将变量值打印到控制台上.

**思路分析**

1. 通过**声明变量并赋值**的方式实现.
2. 通过**先声明, 后赋值**的方式实现.

**参考代码**

方式一: 声明变量并赋值

```java
//1. 定义一个类, 类名叫: VariableDemo02
public class VariableDemo02 {
    //2. 定义main方法, 作为程序的主入口.
    public static void main(String[] args) {
        //3. 测试byte类型.
        //3.1 定义一个byte类型的变量, 变量名叫b, 初始化值为10.
        byte b = 10;
        //3.2 将变量b的值打印到控制台上.
        System.out.println(b);

        //4. 测试short类型.
        //4.1 定义一个short类型的变量, 变量名叫s, 初始化值为20.
        short s = 20;
        //4.2 将变量s的值打印到控制台上.
        System.out.println(s);

        //5. 测试char类型.
        //5.1 定义一个char类型的变量, 变量名叫c, 初始化值为'A'.
        char c = 'A';
        //5.2 将变量c的值打印到控制台上.
        System.out.println(c);

        //6. 测试int类型
        int a = 10;
        System.out.println(a);

        //7. 测试long类型, 数据后记得加字母L.
        long lon = 100L;
        System.out.println(lon);

        //8. 测试float类型, 数据后边加字母F.
        float f = 10.3F;
        System.out.println(f);

        //9. 测试double类型.
        double d = 5.21;
        System.out.println(d);

        //10. 测试boolean类型.
        boolean bb = true;
        System.out.println(bb);
    }
}
```

方式二: 先声明, 后赋值

```java
//1. 定义一个类, 类名叫: VariableDemo03
public class VariableDemo03 {
    //2. 定义main方法, 作为程序的主入口.
    public static void main(String[] args) {
        //3. 测试byte类型.
        //3.1 定义一个byte类型的变量, 变量名叫b.
        byte b;
        //3.2 把数字10赋值给变量b.
        b = 10;
        //3.3 将变量b的值打印到控制台上.
        System.out.println(b);


        //4. 测试char类型.
        //4.1 定义一个char类型的变量, 变量名叫c.
        char c;
        //4.2 把字符'A'赋值给变量c.
        c = 'A';
        //4.3 将变量c的值打印到控制台上.
        System.out.println(c);

        //5. 测试int类型
        int a;
        a = 10;
        System.out.println(a);


        //6. 测试double类型.
        double d;
        d = 5.21;
        System.out.println(d);

        //7. 测试boolean类型.
        boolean bb;
        bb = true;
        System.out.println(bb);
    }
}
```

#### 0.4.4.6 注意事项

##### 0.4.4.6.1 概述

1. 变量未赋值，不能使用.
2. 变量只在它所属的范围内有效.
3. 一行上可以定义多个变量，但是不建议.

##### 0.4.4.6.2 示例三: 变量进阶

**需求**

演示上述使用变量时的三个注意事项.

**参考代码**

```java
//1. 定义一个类, 类名叫: VariableDemo04
public class VariableDemo04 {
    //2. 定义main方法, 作为程序的主入口.
    public static void main(String[] args) {
        //3. 变量未赋值，不能使用.
        int a;
        //a = 10;
        System.out.println(a);      //这样写, 代码会报错, 因为变量a没有赋值.

        //4. 变量只在它所属的范围内有效.
        {
            //大括号包裹起来的代码叫: 代码块.
            //作用: 让变量尽可能早的从内存消失, 从而节约资源, 提高效率.
            double d = 5.21;
            System.out.println(d);
        }
        //下边这行代码会报错, 出了上述的大括号, 变量d就已经从内存中消失了, 无法访问.
        System.out.println(d);
        //5. 一行上可以定义多个变量，但是不建议.
        int e = 10, f = 20, g = 30;
        System.out.println(e);
        System.out.println(f);
        System.out.println(g);
    }
}
```



## 参考资料

1. [JVM（一）一文读懂Java编译全过程](https://blog.csdn.net/gonghaiyu/article/details/110727963)