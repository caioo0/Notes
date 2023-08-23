



### 查询data路径：

show variables like '%datadir%';

use mysql；
select  User,authentication_string,Host from user；

### 权限设置

GRANT ALL PRIVILEGES ON *.* TO 'root'@'%' IDENTIFIED BY '123456'  
flush privileges;  

提升权限：

chown -R mysql:mysql /usr/local/mysql/data

删除mysql:

sudo apt-get autoremove mysql* --purge
sudo apt-get remove apparmor


安装失败可先更新环境：

sudo dpkg --configure -a
sudo apt-get update
sudo apt-get upgrade
sudo apt-get --reinstall install `dpkg --get-selections | grep '[[:space:]]install' | cut -f1`


conda创建环境：

查看环境

conda info --e
创建环境：conda create -n 环境名称 python=版本

conda create -n env_name python=3.6
激活环境：conda activate 环境名称

conda activate env_name



Ubuntu中使用python3中的venv创建虚拟环境

以前不知道Python3中内置了venv模块，一直用的就是virtualenv模块，venv相比virtualenv好用不少，可以替代virtualenv

一、安装venv包：

$ sudo apt install python3-venv
二、创建虚拟环境

首先创建一个项目文件夹，虚拟环境将会安装在项目文件夹下，我这里使用的项目文件夹是myproject，进入mypeoject文件夹，执行命令：

$ python3 -m venv venv
这时虚拟环境就创建好了，默认是Python3的环境

三、激活虚拟环境

在项目文件夹下，执行activate文件激活虚拟环境

source venv/bin/activate
四、创建项目

可以看到项目文件夹下除了venv的虚拟环境文件，没有项目文件，可以使用pip工具安装任何你需要的框架，比如flask、django



当前在 WSL 发行版上运行的服务，请输入：`service --status-all`
