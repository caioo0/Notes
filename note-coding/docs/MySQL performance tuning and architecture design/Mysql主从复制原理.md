## 数据库运维---主从复制、读写分离

# 1. 理解MySQL主从复制原理

主服务器开启binlog日志，从库生成log dump线程，将binlog日志传给从库I/O线程，从库生成俩个线程，一个是I/O线程，一个是SQL线程，I/O线程去请主库的binlog日志，并将binlog日志中的文件写入relay log中，sql线程会读取relay log 中的内容，并解析成具体的操作，来实现主从一致，达到最终数据一致的目的。

# 2. 完成MySQL主从复制（一主两从）

**环境准备：**



| 主机名 | IP地址         | 端口号 |
| ------ | -------------- | ------ |
| node01 | 192.168.11.110 | 3306   |
| node02 | 192.168.11.111 | 3306   |
| node03 | 192.168.11.112 | 3306   |

> 三台主机安装centos 7.*，数据库版本等要求一样。
>
> 关于服务器名称参使用：hostname master  /ectc

**数据库准备：**

```
create database company;
use company
CREATE TABLE `emp`  (
  `empno` int(4) NOT NULL,
  `ename` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `job` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `mgr` int(4) NULL DEFAULT NULL,
  `hiredate` date NOT NULL,
  `sai` int(255) NOT NULL,
  `comm` int(255) NULL DEFAULT NULL,
  `deptno` int(2) NOT NULL,
  PRIMARY KEY (`empno`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

INSERT INTO `emp` VALUES (1001, '甘宁', '文员', 1013, '2000-12-17', 8000, NULL, 20);
INSERT INTO `emp` VALUES (1002, '黛绮丝', '销售员', 1006, '2001-02-20', 16000, 3000, 30);
INSERT INTO `emp` VALUES (1003, '殷天正', '销售员', 1006, '2001-02-22', 12500, 5000, 30);
INSERT INTO `emp` VALUES (1004, '刘备', '经理', 1009, '2001-04-02', 29750, NULL, 20);
INSERT INTO `emp` VALUES (1005, '谢逊', '销售员', 1006, '2001-09-28', 12500, 14000, 30);
INSERT INTO `emp` VALUES (1006, '关羽', '经理', 1009, '2001-05-01', 28500, NULL, 30);
INSERT INTO `emp` VALUES (1007, '张飞', '经理', 1009, '2001-09-01', 24500, NULL, 10);
INSERT INTO `emp` VALUES (1008, '诸葛亮', '分析师', 1004, '2007-04-19', 30000, NULL, 20);
INSERT INTO `emp` VALUES (1009, '曾阿牛', '董事长', NULL, '2001-11-17', 50000, NULL, 10);
INSERT INTO `emp` VALUES (1010, '韦一笑', '销售员', 1006, '2001-09-08', 15000, 0, 30);
INSERT INTO `emp` VALUES (1011, '周泰', '文员', 1006, '2007-05-23', 11000, NULL, 20);
INSERT INTO `emp` VALUES (1012, '程普', '文员', 1006, '2001-12-03', 9500, NULL, 30);
INSERT INTO `emp` VALUES (1013, '庞统', '分析师', 1004, '2001-12-03', 30000, NULL, 20);
INSERT INTO `emp` VALUES (1014, '黄盖', '文员', 1007, '2002-01-23', 13000, NULL, 10);
INSERT INTO `emp` VALUES (1015, '张三', '保洁员', 1001, '2013-05-01', 80000, 50000, 50);
```

## 方式一：基于三台服务器实现主从复制

**主库配置：**

1、在mysqld标签下添加server_id并开启bin_log日志

```
[root@node01 ~]# cat /etc/my.cnf
[mysqld]
#开启二进制日志
log_bin=mysql_bin # //[必须]
#主数据库端ID号
server_id=10 # //[必须]服务器唯一ID，默认是1，一般取IP最后一段
#需要复制的数据库名，如果复制多个数据库，重复设置这个选项即可,全部数据库同步以下不需设置（重点）
binlog-do-db = <db> # company
```

2、重启数据库服务

```
[root@node01 ~]# systemctl restart mysqld.service  //如 centos 6 下命令自查
```

3、授权同步账号和密码

```
[root@node01 ~]# mysql -uroot -p
Enter password:
mysql> grant replication slave on *.* to 'rep'@'192.168.11.%' identified by '123456';
//ip填写从服务器ip，rep是创建的mysql用户名
Query OK, 0 rows affected, 1 warning (0.00 sec)
```

关于授权的一些其他操作：

4、查看授权信息

```
mysql> show grants for 'rep'@'192.168.11.%';
+--------------------------------------------------------+
| Grants for rep@192.168.11.%                            |
+--------------------------------------------------------+
| GRANT REPLICATION SLAVE ON *.* TO 'rep'@'192.168.11.%' |
+--------------------------------------------------------+
1 row in set (0.00 sec)

```

5、对表操作

```
# 锁表设置为只读
# 为后边备份准备，注意生产环境要提前申请停机时间，停服
mysql> flush tables with read lock;

# 超过时间不操作会自动解锁，查看超时时间
mysql> show variables like '%timeout%';
+-----------------------------+----------+
| Variable_name               | Value    |
+-----------------------------+----------+
| connect_timeout             | 10       |
| delayed_insert_timeout      | 300      |
| have_statement_timeout      | YES      |
| innodb_flush_log_at_timeout | 1        |
| innodb_lock_wait_timeout    | 50       |
| innodb_rollback_on_timeout  | OFF      |
| interactive_timeout         | 28800    |
| lock_wait_timeout           | 31536000 |
| net_read_timeout            | 30       |
| net_write_timeout           | 60       |
| rpl_stop_slave_timeout      | 31536000 |
| slave_net_timeout           | 60       |
| wait_timeout                | 28800    |
+-----------------------------+----------+
13 rows in set (0.01 sec)

# 查看主库状态
mysql> show master status ;
+------------------+----------+--------------+------------------+-------------------+
| File             | Position | Binlog_Do_DB | Binlog_Ignore_DB | Executed_Gtid_Set |
+------------------+----------+--------------+------------------+-------------------+
| mysql_bin.000001 |    11824 |              |                  |                   |
+------------------+----------+--------------+------------------+-------------------+
1 row in set (0.00 sec)
```

6、备份数据库数据

```
# 创建备份目录
[root@node01 ~]# mkdir /server/backup -p

[root@node01 ~]# mysqldump -uroot -p -A -B | gzip > /server/backup/mysql_bak.$(date +%F).sql.gz
Enter password:
```

7、解锁

```bash
mysql> unlock tables;
Query OK, 0 rows affected (0.00 sec)
```

8、主库备份数据传送到从库

```
# 在从库上常见备份目录
[root@node02 ~]# mkdir /server/backup -p

# scp传送
[root@node01 ~]# scp /server/backup/mysql_bak.2023-03-25.sql.gz  192.168.11.111:/server/backup/
[root@node01 ~]# scp /server/backup/mysql_bak.2023-03-25.sql.gz  192.168.11.112:/server/backup/
```



**从库配置：**

1、关闭bin_log参数，设置server-id

```bash
[root@node02 ~]# cat /etc/my.cnf
[mysqld]
datadir=/usr/local/mysql/data
socket=/tmp/mysql.sock
server_id=11
```

2、重启数据库服务

```bash
[root@node02 ~]# systemctl restart mysqld.service
```

3、还原从主库传输过来的数据文件

```bash
[root@node02 ~]# cd /server/backup/
[root@node02 backup]# gzip -d mysql_bak.2023-03-25.sql.gz
[root@node02 backup]# mysql -uroot -p < mysql_bak.2023-03-25.sql
Enter password:
```

4、检查数据完整性

```bash
mysql> show databases;
+--------------------+
| Database           |
+--------------------+
| information_schema |
| company            |
| mysql              |
| performance_schema |
| sys                |
+--------------------+
5 rows in set (0.00 sec)

mysql> use company;
mysql> select * from company;
# 数据完整，恢复完成
```

5、配置主从同步

```bash
# 查看主库的binlog和pos位置点
mysql> show master status;
+------------------+----------+--------------+------------------+-------------------+
| File             | Position | Binlog_Do_DB | Binlog_Ignore_DB | Executed_Gtid_Set |
+------------------+----------+--------------+------------------+-------------------+
| mysql_bin.000001 |    11824 |              |                  |                   |
+------------------+----------+--------------+------------------+-------------------+
1 row in set (0.00 sec)

# 从库上配置
mysql> change master to
    -> master_host='192.168.11.110',
    -> master_user='rep',
    -> master_password='123456',
    -> master_log_file='mysql_bin.000001',
    -> master_log_pos=11824;
Query OK, 0 rows affected, 2 warnings (0.01 sec)
```

6、启动从库同步并检查状态

```bash
mysql> start slave;
Query OK, 0 rows affected (0.00 sec)

mysql> show slave status \G
*************************** 1. row ***************************
               Slave_IO_State: Waiting for master to send event
                  Master_Host: 192.168.11.110
                  Master_User: rep
                  Master_Port: 3306
                Connect_Retry: 60
              Master_Log_File: mysql_bin.000001
          Read_Master_Log_Pos: 11824
               Relay_Log_File: node02-relay-bin.000002
                Relay_Log_Pos: 320
        Relay_Master_Log_File: mysql_bin.000001
             Slave_IO_Running: Yes
            Slave_SQL_Running: Yes
# 看目前最后俩行是否为YES，俩个线程都为YES才OK
```

测试：

1、主库创建一个数据库

```bash
mysql> create database test_master;
Query OK, 1 row affected (0.00 sec)

mysql> show databases;
+--------------------+
| Database           |
+--------------------+
| information_schema |
| company            |
| mysql              |
| performance_schema |
| sys                |
| test_master        |
+--------------------+
6 rows in set (0.00 sec)
```

2、从库检查

```bash
[root@node02 backup]# mysql -uroot  -p -e 'show databases;'
Enter password:
+--------------------+
| Database           |
+--------------------+
| information_schema |
| company            |
| mysql              |
| performance_schema |
| sys                |
| test_master        |
+--------------------+
```

## 方式二：基于docker实现主从复制

环境准备：

| 主机名  | IP地址        | 端口 |
| ------- | ------------- | ---- |
| mysql01 | 192.168.11.10 | 3306 |
| mysql02 | 192.168.11.10 | 3307 |
| msyql03 | 192.168.11.10 | 3308 |

安装docker环境：

```bash
# step 1: 安装必要的一些系统工具
sudo yum install -y yum-utils device-mapper-persistent-data lvm2
# Step 2: 添加软件源信息
sudo yum-config-manager --add-repo https://mirrors.aliyun.com/docker-ce/linux/centos/docker-ce.repo
# Step 3
sudo sed -i 's+download.docker.com+mirrors.aliyun.com/docker-ce+' /etc/yum.repos.d/docker-ce.repo
# Step 4: 更新并安装Docker-CE
sudo yum makecache fast
sudo yum -y install docker-ce
# Step 4: 开启Docker服务
sudo service docker start

# 注意：
# 官方软件源默认启用了最新的软件，您可以通过编辑软件源的方式获取各个版本的软件包。例如官方并没有将测试版本的软件源置为可用，您可以通过以下方式开启。同理可以开启各种测试版本等。
# vim /etc/yum.repos.d/docker-ce.repo
#   将[docker-ce-test]下方的enabled=0修改为enabled=1
#
# 安装指定版本的Docker-CE:
# Step 1: 查找Docker-CE的版本:
# yum list docker-ce.x86_64 --showduplicates | sort -r
#   Loading mirror speeds from cached hostfile
#   Loaded plugins: branch, fastestmirror, langpacks
#   docker-ce.x86_64            17.03.1.ce-1.el7.centos            docker-ce-stable
#   docker-ce.x86_64            17.03.1.ce-1.el7.centos            @docker-ce-stable
#   docker-ce.x86_64            17.03.0.ce-1.el7.centos            docker-ce-stable
#   Available Packages
# Step2: 安装指定版本的Docker-CE: (VERSION例如上面的17.03.0.ce.1-1.el7.centos)
# sudo yum -y install docker-ce-[VERSION]
```

1、运行三个容器，mysql01 mysql02 mysql03

```bash
# 重启docker服务
[root@template ~]# systemctl restart docker.service

# 拉取镜像
[root@template ~]# docker run --name mysql01 -p 3306:3306 -e MYSQL_ROOT_PASSWORD=123456 -d mysql:5.7 --lower_case_table_names=1
[root@template ~]# docker run --name mysql02 -p 3307:3306 -e MYSQL_ROOT_PASSWORD=123456 -d mysql:5.7 --lower_case_table_names=1
[root@template ~]# docker run --name mysql03 -p 3308:3306 -e MYSQL_ROOT_PASSWORD=123456 -d mysql:5.7 --lower_case_table_names=1
```

2、修改配置文件

将容器里面的配置文件复制出来，主要修改服务器的配置；在root目录下创建一个/server/backup的目录存放从Docker容器里面复制过来的配置文件。进入目录：cd /server/backup

> 因为在docker中vi命令都没有

```bash
# 创建备份目录
[root@template ~]# mkdir /server/backup -p

# 使用docker cp将文件传到宿主机
[root@template ~]# cd /server/backup/

# 进入容器查看mysql文件
[root@template backup]# docker exec -it  mysql01 bash
bash-4.2# mysql -uroot -p
Enter password:

# 从Docker容器里面复制过来的配置文件,配置文件路径不一样
[root@template ~]# docker cp mysql01:/etc/my.cnf  mysql01.cnf
[root@template ~]# docker cp mysql02:/etc/my.cnf  mysql02.cnf
Successfully copied 3.072kB to /root/mysql02.cnf
[root@template ~]# docker cp mysql03:/etc/my.cnf  mysql03.cnf
Successfully copied 3.072kB to /root/mysql03.cnf
[root@template ~]# ll
total 16
-rw-------. 1 root root 1425 Mar  3 18:52 anaconda-ks.cfg
-rw-r--r--. 1 root root 1159 Mar 22 04:51 mysql01.cnf
-rw-r--r--. 1 root root 1159 Mar 22 04:51 mysql02.cnf
-rw-r--r--. 1 root root 1159 Mar 22 04:51 mysql03.cnf
```

3、主库的mysql01.cnf

```bash
[root@template ~]# vim mysql01.cnf
[mysqld]
server_id=1
log_bin=mysql01.bin
# 添加server_id 和 开启日志
```

4、从库修改server_id即可

```bash
[root@template ~]# vim mysql02.cnf
server_id=2
[root@template ~]# vim mysql03.cnf
server_id=3
```

5、修改完成后，将 mysql01.cnf mysql02.cnf mysql03.cnf 三个文件传入容器中

```bash
[root@template ~]# docker cp mysql01.cnf mysql01:/etc/my.cnf
Successfully copied 3.072kB to mysql01:/etc/my.cnf
[root@template ~]# docker cp mysql02.cnf mysql02:/etc/my.cnf
Successfully copied 3.072kB to mysql02:/etc/my.cnf
[root@template ~]# docker cp mysql03.cnf mysql03:/etc/my.cnf
Successfully copied 3.072kB to mysql03:/etc/my.cnf
```

6、重启数据库

```bash
[root@template ~]# docker restart mysql01  mysql02 mysql03
```

7、测试连接

```bash
[root@node03 ~]# mysql -uroot -p123456 -h 192.168.11.10 -P 3306
mysql: [Warning] Using a password on the command line interface can be insecure.
Welcome to the MySQL monitor.  Commands end with ; or \g.
Your MySQL connection id is 2
Server version: 5.7.41-log MySQL Community Server (GPL)

Copyright (c) 2000, 2021, Oracle and/or its affiliates.

Oracle is a registered trademark of Oracle Corporation and/or its
affiliates. Other names may be trademarks of their respective
owners.

Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

mysql> \q
Bye
[root@node03 ~]# mysql -uroot -p123456 -h 192.168.11.10 -P 3307
mysql: [Warning] Using a password on the command line interface can be insecure.
Welcome to the MySQL monitor.  Commands end with ; or \g.
Your MySQL connection id is 2
Server version: 5.7.41 MySQL Community Server (GPL)

Copyright (c) 2000, 2021, Oracle and/or its affiliates.

Oracle is a registered trademark of Oracle Corporation and/or its
affiliates. Other names may be trademarks of their respective
owners.

Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

mysql> \q
Bye
[root@node03 ~]# mysql -uroot -p123456 -h 192.168.11.10 -P 3308
mysql: [Warning] Using a password on the command line interface can be insecure.
Welcome to the MySQL monitor.  Commands end with ; or \g.
Your MySQL connection id is 2
Server version: 5.7.41 MySQL Community Server (GPL)

Copyright (c) 2000, 2021, Oracle and/or its affiliates.

Oracle is a registered trademark of Oracle Corporation and/or its
affiliates. Other names may be trademarks of their respective
owners.

Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

mysql>
```

8、在3306作为主库

```bash
[root@template backup]# docker exec -it mysql01 bash
bash-4.2# mysql -uroot -p123456
```

9、创建一个rep用户

```bash
mysql> create user 'rep'@'%' identified by '123456';
Query OK, 0 rows affected (0.02 sec)
```

10、添加权限

```bash
mysql> grant replication slave on *.* to 'rep'@'%';
Query OK, 0 rows affected (0.00 sec)
```

11、刷新权限表

```bash
mysql> flush privileges;
Query OK, 0 rows affected (0.00 sec)
```

12、测试用rep登录

```bash
bash-4.2# mysql -urep -p123456
```

13、进入从库做配置

```bash
# 查看主库上的信息，注意用户，要用root用户，开始用的rep错误信息如下：
mysql> show master status;
ERROR 1227 (42000): Access denied; you need (at least one of) the SUPER, REPLICATION CLIENT privilege(s) for this operation
# 查看主库上的信息
mysql> show master status;
+----------------+----------+--------------+------------------+-------------------+
| File           | Position | Binlog_Do_DB | Binlog_Ignore_DB | Executed_Gtid_Set |
+----------------+----------+--------------+------------------+-------------------+
| mysql01.000001 |      745 |              |                  |                   |
+----------------+----------+--------------+------------------+-------------------+
1 row in set (0.00 sec)


[root@template ~]# docker exec -it mysql02 bash
[root@template ~]# docker exec -it mysql03 bash

bash-4.2# mysql -uroot -p123456
mysql> change master to
    -> master_host="192.168.11.10",
    -> master_user="rep",
    -> master_password="123456",
    -> master_log_file="mysql01.000001",
    -> master_log_pos=745;
Query OK, 0 rows affected, 2 warnings (0.01 sec)
```

14、开启slave并且查看俩个线程状态

```bash
mysql> start slave;
Query OK, 0 rows affected (0.01 sec)

mysql> show slave status \G
*************************** 1. row ***************************
               Slave_IO_State: Waiting for master to send event
                  Master_Host: 192.168.11.10
                  Master_User: rep
                  Master_Port: 3306
                Connect_Retry: 60
              Master_Log_File: mysql01.000001
          Read_Master_Log_Pos: 745
               Relay_Log_File: cb6044d1b02b-relay-bin.000002
                Relay_Log_Pos: 318
        Relay_Master_Log_File: mysql01.000001
             Slave_IO_Running: Yes
            Slave_SQL_Running: Yes
```

15、可以用客户端连接测试，实验完成！！！

# 3.基于MySQL一主两从配置，完成MySQL读写分离配置

在docker环境上完成！！！

1、使用MYCAT2安装JDK，因为MYCAT是基于JDK1.8开发的

```bash
[root@template ~]# yum install -y jdk-8u261-linux-x64.rpm
[root@template ~]# java -version
java version "1.8.0_261"
```

2、下载压缩包和jar包

```bash
#创建/data/tools目录
[root@template ~]# mkdir -p /data/tools
[root@template ~]# cd /data/tools/
[root@template ~]# wget -c http://dl.mycat.org.cn/2.0/install-template/mycat2-install-template-1.21.zip
[root@template ~]# wget -c http://dl.mycat.org.cn/2.0/1.21-release/mycat2-1.21-release-jar-with-dependencies.jar
```

3、安装MyCAT2

```bash
[root@template tools]# ll
total 149484
-rw-r--r--. 1 root root 151819628 May  9  2022 mycat2-1.21-release-jar-with-dependencies.jar
-rw-r--r--. 1 root root   1246974 May  9  2022 mycat2-install-template-1.21.zip
```

4、安装unzip

```bash
[root@template tools]# yum install -y unzip
```

5、解压到指定目录

```bash
[root@template tools]# unzip mycat2-install-template-1.21.zip -d /data/
```

6、修改权限

```bash
[root@template ~] cd /data/mycat/lib/
[root@template bin]# chmod +x *
[root@template bin]# cp /data/tools/mycat2-1.21-release-jar-with-dependencies.jar ./
```

7、查看mycat目录结构

```bash
[root@template bin]# ll /data/mycat/
total 8
drwxr-xr-x. 2 root root 4096 Mar 25 22:56 bin
drwxr-xr-x. 9 root root  275 Mar  5  2021 conf
drwxr-xr-x. 2 root root 4096 Mar  5  2021 lib
drwxr-xr-x. 2 root root    6 Mar  5  2021 logs
```

8、启动mycat

```bash
./mycat start 启动
./mycat console 前台运行
./mycat install 添加到系统自动启动
./mycat remove 取消随系统自动启动
./mycat restart 重启
./mycat pause 暂停
./mycat status 查看启动状态
```

9、出现以下信息表示启动成功

```bash
[root@template bin]# ./mycat start
Starting mycat2...
[root@template bin]# cat /data/mycat/logs/wrapper.log
STATUS | wrapper  | 2023/03/25 22:59:23 | --> Wrapper Started as Daemon
STATUS | wrapper  | 2023/03/25 22:59:23 | Launching a JVM...
INFO   | jvm 1    | 2023/03/25 22:59:23 | Wrapper (Version 3.2.3) http://wrapper.tanukisoftware.org
INFO   | jvm 1    | 2023/03/25 22:59:23 |   Copyright 1999-2006 Tanuki Software, Inc.  All Rights Reserved.
INFO   | jvm 1    | 2023/03/25 22:59:23 |
INFO   | jvm 1    | 2023/03/25 22:59:23 | WrapperSimpleApp: Unable to locate the class io.mycat.MycatCore: java.lang.ClassNotFoundException: io.mycat.MycatCore
INFO   | jvm 1    | 2023/03/25 22:59:23 |
INFO   | jvm 1    | 2023/03/25 22:59:23 | WrapperSimpleApp Usage:
INFO   | jvm 1    | 2023/03/25 22:59:23 |   java org.tanukisoftware.wrapper.WrapperSimpleApp {app_class} [app_arguments]
INFO   | jvm 1    | 2023/03/25 22:59:23 |
INFO   | jvm 1    | 2023/03/25 22:59:23 | Where:
INFO   | jvm 1    | 2023/03/25 22:59:23 |   app_class:      The fully qualified class name of the application to run.
INFO   | jvm 1    | 2023/03/25 22:59:23 |   app_arguments
```

10、修改容器中的mysql配置文件

```bash
[root@template backup]# docker cp mysql01:/etc/my.cnf mysql01.cnf
[root@template backup]# docker cp mysql02:/etc/my.cnf mysql02.cnf
[root@template backup]# docker cp mysql03:/etc/my.cnf mysql03.cnf
```

11、分别修改配置文件

```bash
[root@template backup]# cat mysql01.cnf mysql02.cnf mysql03.cnf
[mysqld]
server_id=1
log_bin=mysql01.bin
skip-host-cache
skip-name-resolve

[mysqld]
server_id=2
skip-host-cache
skip-name-resolve

[mysqld]
server_id=3
skip-host-cache
skip-name-resolve
```

12、修改完成后复制到容器中

```bash
[root@template backup]# docker cp mysql01.cnf  mysql01:/etc/mysql01.cnf
[root@template backup]# docker cp mysql02.cnf  mysql02:/etc/mysql02.cnf
[root@template backup]# docker cp mysql03.cnf  mysql03:/etc/mysql03.cnf
```

13、重启数据库

```bash
[root@template backup]# docker restart mysql01 mysql02  mysql03
mysql01
mysql02
mysql03
下面出现容器名称，重启成功！
```

14、关联主机

```bash
主库：
mysql> show master status;
+----------------+----------+--------------+------------------+-------------------+
| File           | Position | Binlog_Do_DB | Binlog_Ignore_DB | Executed_Gtid_Set |
+----------------+----------+--------------+------------------+-------------------+
| mysql01.000002 |      154 |              |                  |                   |
+----------------+----------+--------------+------------------+-------------------+
1 row in set (0.00 sec)

从库：
mysql> stop slave;
Query OK, 0 rows affected (0.01 sec)

mysql> change master to
    ->  master_host="192.168.11.10",
    ->  master_user="rep",
    ->  master_password="123456",
    ->  master_log_file="mysql01.000002",
    ->  master_log_pos=154;
Query OK, 0 rows affected, 2 warnings (0.01 sec)

mysql>
mysql> start slave;
Query OK, 0 rows affected (0.00 sec)

# 查看状态
mysql> show slave status \G
*************************** 1. row ***************************
               Slave_IO_State: Waiting for master to send event
                  Master_Host: 192.168.11.10
                  Master_User: rep
                  Master_Port: 3306
                Connect_Retry: 60
              Master_Log_File: mysql01.000002
          Read_Master_Log_Pos: 154
               Relay_Log_File: cb6044d1b02b-relay-bin.000002
                Relay_Log_Pos: 318
        Relay_Master_Log_File: mysql01.000002
             Slave_IO_Running: Yes
            Slave_SQL_Running: Yes
....
```

15、从库上新建用户并授权

```bash
mysql> create user 'rep'@'%' identified by '123456';
Query OK, 0 rows affected (0.00 sec)

mysql> grant replication slave on *.* to 'rep'@'%';
Query OK, 0 rows affected (0.00 sec)
```

16、刷新权限并尝试新用户登录

```bash
mysql> flush privileges;
Query OK, 0 rows affected (0.00 sec)
```

17、主库创建数据库测试

```bash
mysql> show databases;
+--------------------+
| Database           |
+--------------------+
| information_schema |
| mysql              |
| performance_schema |
| sys                |
+--------------------+
4 rows in set (0.00 sec)

mysql> create database stu;
Query OK, 1 row affected (0.00 sec)

# 从库上检查是否也创建了stu数据库
mysql> mysql> show databases;
```

至此，主从同步完成！！！

在notpad++装一个插件可以连接mycat

18、添加数据源

```bash
# 添加mysql02读的数据源
/*+ mycat:createDataSource{
"dbType":"mysql",
"idleTimeout":60000,
"initSqls":[],
"initSqlsGetConnection":true,
"instanceType":"READ",
"maxCon":1000,
"maxConnectTimeout":3000,
"maxRetryCount":5,
"minCon":1,
"name":"mysql02",
"password":"123456",
"type":"JDBC",
"url":"jdbc:mysql://127.0.0.1:3307?
useUnicode=true&serverTimezone=UTC&characterEncoding=UTF-8",
"user":"root",
"weight":0
} */;

# 添加mysql03读的数据源
/*+ mycat:createDataSource{
"dbType":"mysql",
"idleTimeout":60000,
"initSqls":[],
"initSqlsGetConnection":true,
"instanceType":"READ",
"maxCon":1000,
"maxConnectTimeout":3000,
"maxRetryCount":5,
"minCon":1,
"name":"mysql03",
"password":"123456",
"type":"JDBC",
"url":"jdbc:mysql://127.0.0.1:3308?
useUnicode=true&serverTimezone=UTC&characterEncoding=UTF-8",
"user":"root",
"weight":0
} */;
```

19、修改集群配置

```bash
{
"clusterType":"MASTER_SLAVE",
"heartbeat":{
"heartbeatTimeout":1000,
"maxRetryCount":0,
"minSwitchTimeInterval":300,
"showLog":true,
"slaveThreshold":0.0
},
"masters":[
"mysql01"
],
"maxCon":2000,
"name":"prototype",
"readBalanceType":"BALANCE_ALL",
"replicas":[
"mysql02","mysql03"
],
"switchType":"SWITCH"
}
```

20、重启mycat测试

```bash
[root@template backup]# cd /data/mycat/bin
[root@template bin]# ./mycat restart

# 在mysqt中测试，可以用第三方数据库连接软件
CREATE DATABASE db1 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
# 建表
use db1
create table sys_user(
id bigint primary key,
username varchar(200) not null,
address varchar(500)
)；
# 刷新逻辑表到物理表

/*+ mycat:repairPhysicalTable{} */;

# mycat中插入输入数据
insert INTO sys_user(id,username,address) values(1,"z3","bj");

# 刷新数据库
```



## 其他资料

1. https://zhuanlan.zhihu.com/p/366925038
2. https://blog.csdn.net/andyguan01_2/article/details/107005913