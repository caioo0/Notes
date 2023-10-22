# Task02:数据库的基本使用
---

> （本学习笔记来源于DataWhale-12月组队学习：[推荐系统实战](https://github.com/datawhalechina/fun-rec)，[直播视频地址](https://datawhale.feishu.cn/minutes/obcnzns778b725r5l535j32o)） 

## MySQL基本管理

### 1.安装 和卸载


安装MySQL需要安装两个程序：

`mysql-server`和`mysql-client`
             
1. 首先查看是否已经有`mysql`，输入命令`sudo netstat -tap | grep mysql` 
     
2. 安装

```bash
   sudo apt-get install mysql-server -y
   sudo apt install mysql-client  -y
   sudo apt install libmysqlclient-dev -y
   
```
3. 再次输入如下命令进行检验是否安装mysql成功

```bash 
  sudo netstat -tap | grep mysql 
```
4. 获取版本号：`mysql --version`

5. 如何卸载

```bash
  sudo apt-get autoremove mysql* --purge
  sudo apt-get remove apparmor
  sudo apt purge mysql-*
  sudo rm -rf /etc/mysql/ /var/lib/mysql
  sudo apt autoremove
  sudo apt autoclean
```







### 2. 管理MySQL命令

- 启动安全脚本提示符：`sudo mysql_secure_installation`,根据指示输入`Y`即可。

> 注：第一个提示符会询问是否要设置验证密码插件，该插件可用于测试 MySQL 密码的强度。   
> 然后将为 MySQL 根用户设置密码，  
> 决定是否删除匿名用户，  
> 决定是否允许根用户本地和远程登录，  
> 决定是否删除测试数据库，  
> 最后决定是否立即重新加载特权表。  
- 查询字符集：`show variables like 'character%';`（注意不同版本会有区别）
- 列出所有数据库:`show databases`
- 操作指定数据库;`use userinfo` (`userinfo`指定的数据库名，改为你要指定的数据库即可)
- 显示指定数据库所有表：1).`use userinfo`指定数据库，2). `show tabels`
- 显示数据表的属性，类型主键信息，是否为NULL,默认值等信息： `SHOW COLUMNS FROM 数据表`
- 显示数据表的索引信息，包括PRIMARY KEY(主键)：`SHOW INDEX FROM runoob_tbl;`
- 输出基本表信息：`SHOW TABLE STATUS [FROM db_name] [LIKE 'pattern'] \G:`
- 查询mysql所有用户：
```bash
use mysql；
select  User,authentication_string,Host from user；
```

-  root权限设置 

```bash
GRANT ALL PRIVILEGES ON *.* TO 'root'@'localhost' IDENTIFIED BY 'PASSWORK'  
flush privileges;  
```

-  创建账号`admin`和密码`admin123`,开放远程访问`%`:`CREATE USER 'admin'@'%' identified by 'admin123';`


-  赋予admin用户全部的权限，你也可以只授予部分权限:`GRANT ALL PRIVILEGES ON *.* TO '用户名'@'localhost';`


有关使用 MySQL 数据库的更多信息，请参阅 [MySQL 文档](https://dev.mysql.com/doc/mysql-getting-started/en/)。

### 3. 数据库基本操作

```bash
//首先选定操作的数据库
use userinfo;
//创建表student
create table register_user(
  userid  int(11),
  username  varchar(20),
  age int(11)
);
//查看数据表
show tables;
//查看数据表信息，后面加上参数/G可使结果更加美观
show create table register_user;
//查看表的的字段信息
desc register_user;
//修改表名
alter table register_user rename [to] register_user_1;
//修改字段名
alter table register_user_1 change username user_name varchar(50);
//修改字段的数据类型
alter table register_user_1 modify id int(20);
//添加字段
alter table register_user_1 add gender varchar(30);
//删除字段
alter table register_user_1 drop gender;
//修改字段的位置
alter table register_user_1 modify user_name varchar(50) first;
alter table register_user_1 modify id userid(11) after age;
//删除数据表
drop table register_user_1;


//查询数据表
SELECT <字段名>[as <新字段名>], …… FROM <表名>; 
SELECT * FROM <表名>; # 星号(*)代表全部字段
//去重查询
SELECT   DISTINCT <字段名>  FROM <表名>;
//指定条件查询
SELECT <字段名>, …… FROM <表名> WHERE <条件表达式>;
//表的复制
CREATE TABLE <表名1> SELECT * FROM <表名>;

//往表中插入一行数据
INSERT INTO <表名> (字段1, 字段2, 字段3, ……) VALUES (值1, 值2, 值3, ……);

//往表中插入多行数据
INSERT INTO <表名> (字段1, 字段2, 字段3, ……) VALUES 
	(值1, 值2, 值3, ……),
	(值1, 值2, 值3, ……),
	...
	;
    
// 数据的更新 
UPDATE <表名> SET <字段名> = <表达式>;

```

### 分组查询

**聚合函数**：

- `COUNT` 计算表中的记录数（行数）:`SELECT COUNT(*) FROM <表名>;`

- `SUM` 计算表中数值列中数据的合计值:`SELECT MAX(<字段名>) FROM <表名>;`

- `AVG`计算表中数值列中数据的平均值

- `MAX` 求出表中任意列中数据的最大值

- `MIN`求出表中任意列中数据的最小值

**分组查询**：`SELECT <列名1>, <列名2>, <列名3>, ……FROM <表名>GROUP BY <列名1>, <列名2>, ……;`



### MySQL的缺陷与不足
- 不支持 hash join，大表之间不适合做 joi n操作，没办法满足复杂的OLAP要求。
- MySQL 不支持函数索引，也不支持并行更新
- MySQL 连接的 8 小时问题，相对于使用 Oracle 数据库，使用MySQL需要注意更多的细节问题。
- 对于 SQL 批处理和预编译，支持程度不如 Oracle 数据库。
- MySQL 优化器还是比较欠缺，不及 Oracle 数据库。

### MySQL的优点
- 互联网领域使用较多，文档资料丰富，使用案例非常多，对潜在的问题比较容提前做出应对方案。
- 由于 MySQL 是开源的数据库，因此很多互联网公司都根据自己的业务需求，开发出了自己的 MySQL 版本，例如阿里云上的 RDS、腾讯云、美团云等。
- MySQL 相关的开源解决方案众多，无需重复造轮子既可以获得包括读写分离、分库分表等高级特性，例如 Mycat、Sharding-JDBC 等。同时，MySQL 官方的解决方案也越来越丰富，例如 MySQL-Router 等。


## Pymysql的使用
---

### 1.安装


```python
pip install PyMySQL
```

### 2. 数据库操作


```python
import pymysql

# 建立连接
db = pymysql.connect(
    host = 'localhost',
    user = 'root',
    password = '123456',
    database = 'userinfo',
    charset = 'utf8mb4',
    cursorclass = pymysql.cursors.DictCursor
)

# 创建游标
cursor = db.cursor(cursor=pymysql.cursors.DictCursor)

```

`cursors`共支持四类游标：
- `Cursor`: 默认，元组类型
- `DictCursor`: 字典类型
- `SSCursor`: 无缓冲元组类型
- `SSDictCursor`: 无缓冲字典类型


更详细的资料，可参考官方的API或者Github:

[pymysql github]: https://github.com/PyMySQL/PyMySQL

[pymysql document]: https://pymysql.readthedocs.io/en/latest/modules/index.html#

创建了一个表


```python
sql = """
CREATE TABLE Employee(
    id INT PRIMARY KEY,
    name CHAR(15) NOT NULL
    )
    """

# 提交执行
cursor.execute(sql)


```


```python
# 2. 往表中插入数据
sql = "INSERT INTO Employee (id, name) VALUES (%s, %s)"
values = [(1, 'XiaoBai'),
          (2, 'XiaoHei'),
          (3, 'XiaoHong'),
          (4, 'XiaoMei'),
          (5, 'XiaoLi')]

try:
		# 通过executemany可以插入多条数据
    cursor.executemany(sql, values)
    # 提交事务
    db.commit()
except:
    db.rollback()


# 3. 关闭光标及连接
cursor.close()
db.close()
```

查询数据表


```python
import pymysql

# 以admin身份连接到数据库shop
connection = pymysql.connect(
    host='localhost',
    user='admin',
    password='admin123',
    database='userinfo',
    charset='utf8mb4',
)

cursor = connection.cursor(cursor=pymysql.cursors.DictCursor)

# 1. 通过fetchone只查询一条
cursor.execute("SHOW CREATE TABLE Employee")
result = cursor.fetchone()
print(f'查询结果1： \n{result}')

# 2. 通过fetchmany查询size条
cursor.execute("DESC Employee")
result = cursor.fetchmany(size=2)
print(f'查询结果2： \n{result}')

# 3. 通过fetchall查询所有
cursor.execute("SELECT * FROM Employee")
result = cursor.fetchall()
print(f'查询结果3： \n{result}')


```

实例1,新增表并且插入数据


```python
import pymysql

# 以admin身份连接到数据库shop
connection = pymysql.connect(
    host='localhost',
    user='admin',
    password='admin123',
    database='userinfo',
    charset='utf8mb4',
)

# 创建游标
cursor = connection.cursor(cursor=pymysql.cursors.DictCursor)

sql = """
        CREATE TABLE UserInfo(
          id INT PRIMARY KEY,
          name VARCHAR(15),
          password CHAR(15) NOT NULL
          )
    """

cursor.execute(sql)

sql = "INSERT INTO UserInfo (id, name, password) VALUES (%s, %s, %s)"
values = [(1, 'XiaoBai', '123'),
          (2, 'XiaoHei', '234'),
          (3, 'XiaoHong', '567'),
          (4, 'XiaoMei', '321'),
          (5, 'XiaoLi', '789')]

cursor.executemany(sql, values)
connection.commit()
```

根据上面的实例1，模拟登录操作


```python
import pymysql

# 以admin身份连接到数据库shop
connection = pymysql.connect(
    host='localhost',
    user='admin',
    password='admin123',
    database='userinfo',
    charset='utf8mb4',
)

# 创建游标
cursor = connection.cursor(cursor=pymysql.cursors.DictCursor)


```


```python
sql = "select name, password from UserInfo where name=%s and password=%s"
cursor.execute(sql, (user, password))
```

## SQLAlchemy基本操作
---

首先安装MySQL驱动和sqlalchemy

```bash
pip install mysql-connector
pip install sqlalchemy    #如果python环境装的的Anaconda就不用再执
```



```python
pip install mysql-connector

```

    Looking in indexes: https://pypi.tuna.tsinghua.edu.cn/simple
    Requirement already satisfied: mysql-connector in d:\programdata\anaconda3\lib\site-packages (2.2.9)
    Note: you may need to restart the kernel to use updated packages.
    


```python
#DataBaseConfig.py主要是用来配置数据库相关信息，并创建session
# 数据库配置
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# 初始化数据库连接:
# 如果链接的是mysql8.x 请加上?auth_plugin=mysql_native_password
engine = create_engine(
'mysql+mysqlconnector://admin:admin123@192.168.148.156:3306/test?auth_plugin=mysql_native_password' ,
    max_overflow=0,  # 超过连接池大小外最多创建的连接
    pool_size=5,  # 连接池大小
    pool_timeout=30,  # 池中没有线程最多等待的时间，否则报错
    pool_recycle=-1)  # 多久之后对线程池中的线程进行一次连接的回收（重置）)
# 创建 DBsession类型:
DBSession = sessionmaker(bind=engine)
session = DBSession()
```


```python
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column,String,Integer
 
engine = create_engine("mysql+pymysql://root:root@127.0.0.1/test",encoding="utf-8",echo=True,max_overflow=5)
#连接mysql数据库，echo为是否打印结果
 
Base = declarative_base() #生成orm基类
 
class User(Base): #继承生成的orm基类
    __tablename__ = "sql_test" #表名
    id = Column(Integer,primary_key=True) #设置主键
    user_name = Column(String(32))
    user_password = Column(String(64))
 
class Admin(Base):
    __tablename__ = "admin"
    id = Column(Integer, primary_key=True)
    username = Column(String(32))
    password = Column(String(64))
 
Base.metadata.create_all(engine) #创建表结构
```

    2021-12-18 20:27:28,603 INFO sqlalchemy.engine.Engine SHOW VARIABLES LIKE 'sql_mode'
    2021-12-18 20:27:28,604 INFO sqlalchemy.engine.Engine [raw sql] {}
    2021-12-18 20:27:28,606 INFO sqlalchemy.engine.Engine SHOW VARIABLES LIKE 'lower_case_table_names'
    2021-12-18 20:27:28,607 INFO sqlalchemy.engine.Engine [generated in 0.00095s] {}
    2021-12-18 20:27:28,612 INFO sqlalchemy.engine.Engine SELECT DATABASE()
    2021-12-18 20:27:28,612 INFO sqlalchemy.engine.Engine [raw sql] {}
    2021-12-18 20:27:28,615 INFO sqlalchemy.engine.Engine BEGIN (implicit)
    2021-12-18 20:27:28,617 INFO sqlalchemy.engine.Engine SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = %(table_schema)s AND table_name = %(table_name)s
    2021-12-18 20:27:28,618 INFO sqlalchemy.engine.Engine [generated in 0.00124s] {'table_schema': 'test', 'table_name': 'sql_test'}
    2021-12-18 20:27:28,620 INFO sqlalchemy.engine.Engine SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = %(table_schema)s AND table_name = %(table_name)s
    2021-12-18 20:27:28,621 INFO sqlalchemy.engine.Engine [cached since 0.004377s ago] {'table_schema': 'test', 'table_name': 'admin'}
    2021-12-18 20:27:28,623 INFO sqlalchemy.engine.Engine COMMIT
    


```python
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column,String,Integer
from sqlalchemy.orm import sessionmaker
 
engine = create_engine(
'mysql+mysqlconnector://admin:admin123@192.168.148.156:3306/test?auth_plugin=mysql_native_password')
 
Base = declarative_base()
 
class Admin(Base):
    __tablename__ = "admin"
    id = Column(Integer, primary_key=True)
    username = Column(String(32))
    password = Column(String(64))
 
Base.metadata.create_all(engine)
 
Session_Class = sessionmaker(bind=engine) #创建与数据库的会话，Session_Class为一个类
 
Session = Session_Class() #实例化与数据库的会话
 
t1 = Admin(username='test',password='123456') #生成admin表要插入的一条数据
t2 = Admin(username='test1',password='abcdef') #生成admin表要插入的一条数据
 
print(t1.username,t1.password)
print(t2.username,t2.password)
 
Session.add(t1) #把admin表要插入的数据添加到Session里
Session.add(t2)
 
Session.commit() #提交，不然不能创建数据
```

    test 123456
    test1 abcdef
    

##  MongoDB 基本操作



```python

```

### 安装

这是在系统中安装 [MongoDB](https://docs.mongoing.com/the-mongodb-manual-cn) 的简便方法，你只需输入一个命令即可。

1. 安装 MongoDB
首先，确保你的包是最新的。打开终端并输入：

```
sudo apt update && sudo apt upgrade -y]
```
2. 继续安装 MongoDB：
```
sudo apt install mongodb
```
这就完成了！MongoDB 现在安装到你的计算机上了。

3. MongoDB 服务应该在安装时自动启动，但要检查服务状态：
```
sudo service  mongodb status
```

安装时报错解决：error while loading shared libraries: libcrypto.so.1.1

```bash
ln -s /usr/local/lib/libssl.so.1.1 /usr/lib/libssl.so.1.1
ln -s /usr/local/lib/libcrypto.so.1.1 /usr/lib/libcrypto.so.1.1
```

### 卸载

1.停止 mongodb服务
```
sudo service mongod stop
```
2.卸载mongodb
```
sudo apt-get remove mongodb
```
3.移除相关包
```
sudo apt-get purge mongodb-org*
sudo apt-get purge mongodb
sudo apt-get autoremove
sudo apt-get autorclean
```
4.移除相关目录
```
sudo rm -r /var/log/mongodb
sudo rm -r /var/lib/mongodb
```
5.查看系统还有哪些残留的文件或目录
```
whereis mongo
whereis mongodb
whereis mongod
which mongo
which mongodb
which mongod
```

## 参考资料
[^1]. [Flask-SQLAlchemy常用操作](https://www.cnblogs.com/huchong/p/8274510.html)  
[^2]. [MongoDB用户手册说明](https://docs.mongoing.com/the-mongodb-manual-cn)   
[^3]. https://zhuanlan.zhihu.com/p/76349679



```python

```
