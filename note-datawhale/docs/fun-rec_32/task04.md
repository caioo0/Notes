# Task04:前后端基础及交互
---

> （本学习笔记来源于DataWhale-12月组队学习：[推荐系统实战](https://github.com/datawhalechina/fun-rec)，[直播视频地址](https://datawhale.feishu.cn/minutes/obcnzns778b725r5l535j32o)） 

    太阳总有办法照到我们，不管我们在哪里 ---《克拉拉与太阳》


## 前后端交互

**前端技术：vue+mint-UI**

**前端页面：注册页，登录页，我的页（包含退出功能）、热门列表页、推荐列表页、新闻详情页**

**后端技术：Flask+Mysql+MongoDB+Redis+crontab**

**后端接口：提供用户注册、用户登录、用户推荐页列表、用户热门页列表、新闻详情、用户行为等服务请求，完成用户从注册到新闻浏览、点赞和收藏的接口**



## 后端部分重要的结构

- **conf/dao_config.py: 候选整体配置文件**
- **controller/ : 项目中用于操作数据库的接口**
- **dao/ : 项目的实体类，对应数据库表**
- **materials/: 项目的物料部分，主要用户爬取物料以及处理用户画像和新闻画像**
- **recpocess/: 项目的推荐模块，主要包含召回和排序，以及一些线上服务和线下处理部分**
- **scheduler: 项目的定时任务的脚本部分**
- **server.py: 项目后端的入口部分，主要包含项目整体的后端接口部分。**

## 1. Vue 项目的搭建

### 1.1 安装Node环境

Node.js下载地址：http://nodejs.cn/download/

根据自身电脑版本，安装相应的安装包。也可以通过 `NVM` 安装，`nvm`可以是先多node版本管理

安装成功后，可通过下面指定检测node环境是否搭建成功。

```bash
# -v 是 -version 的缩写，目的是为了查看当前 node 与 npm 的版本号。
$ node -v
v16.6.2
$ npm -v
7.22.0
```
npm 的默认源是国外地址，所以下载文件的时候会很慢。建议更换为国内源。

npm 换源操作如下（建议使用第二种方式）：

```bash
# 第一种方式：使用阿里定制的 cnpm 命令行工具代替默认的 npm。
$ npm install -g cnpm --registry=https://registry.npm.taobao.org
# 第二种方式：习惯了使用 npm，直接配置 npm 源即可。
$ npm config set registry https://registry.npm.taobao.org

```

### 1.2 安装 webpack

```bash
# -g 是 global 的缩写，意思是全局安装 webpack。
$ npm install -g webpack 
```

### 1.3 安装 vue-cli 脚手架工具

```bash
npm install -g @vue/cli
```
安装结束后，检测 vue-cli 是否安装成功，运行一下命令，若显示当前版本号，则安装成功。

```bash
# 注意：这里是大写的 V 而不是小写的 v
$ vue -V
@vue/cli 4.5.15
```

### 1.4 创建vue项目

```bash
vue create hello-world
# 进入项目具体路径
cd hello-world
# 下载依赖
npm install
# 启动运行项目
npm run serve 
# 项目打包
npm run build
```

## 2 Flask配置

### 2.1 安装

```bash
pip install virtualenv
# 创建项目具体路径
mkdir newproj
# 进入项目具体路径
cd newproj
# 创建虚拟环境
virtualenv venv
# 激活虚拟环境
venv/bin/activate
# 安装flask 
pip install Flask
```
### 2.2 FLASK测试运行

```python

from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
   return 'Hello World'

if __name__ == '__main__':
   app.run()
   
```

运行代码，在浏览器中打开**localhost：5000**，将显示**“Hello World”**消息。

```python
python Hello.py
```


### 参考链接：

1. https://juejin.cn/post/6844904013322944525
2. https://segmentfault.com/a/1190000010030848
3. https://github.com/axios/axios 