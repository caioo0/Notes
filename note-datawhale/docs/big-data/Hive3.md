# task06之三：Apache Hive高级实战

---

（本学习笔记整理自[datawhale-大数据处理技术导论](https://github.com/datawhalechina/juicy-bigdata)，部分内容来自其他相关参考教程）


由于hive涉及内容有点多，所以我用了3个篇幅来说明：

1. [task06之一：数据仓库Hive基础](hive.md)
2. [task06之二:Hive-数据仓库进阶](Hive2.md)
3. [task06之三：Apache Hive高级实战](Hive3.md)

**本课目标 (Objective)**

- 理解Hive的事务处理
- 了解Hive的UDF，自定义函数
- 掌握Hive的性能调优

## 6.1 事务处理

Apache Hive 0.13 版本引入了事务特性，能够在 Hive 表上实现 ACID 语义，包括 INSERT/UPDATE/DELETE/MERGE 语句、增量数据抽取等。

Hive 3.0 又对该特性进行了优化，包括改进了底层的文件组织方式，减少了对表结构的限制，以及支持条件下推和向量化查询。

对于在Hive中使用ACID和Transactions，主要有以下限制：

- 不支持BEGIN,COMMIT和ROLLBACK
- 只支持ORC文件格式
- 表必须分桶
- 不允许从一个非ACID连接写入/读取ACID表
- 为了使 Hive 支持事务操作，需将以下参数加入到 hive-site.xml 文件中。

```
<property>
<name>hive.support.concurrency</name>
<value>true</value>
</property>
<property>
<name>hive.enforce.bucketing</name>
<value>true</value>
</property>
<property>
<name>hive.exec.dynamic.partition.mode</name>
<value>nonstrict</value>
</property>
<property>
<name>hive.txn.manager</name>
<value>org.apache.hadoop.hive.ql.lockmgr.DbTxnManager</value>
</property>
<property>
<name>hive.compactor.initiator.on</name>
<value>true</value>
</property>
<property>
<name>hive.compactor.worker.threads </name>
<value>1</value>
</property>
```

### 6.1.1 ACID 与实现原理

何为事务？就是一组单元化操作，这些操作要么都执行，要么都不执行，是一个不可分割的工作单位。

事务（transaction）所应该具有的四个要素：原子性（Atomicity）、一致性（Consistency）、隔离性（Isolation）、持久性（Durability）。这四个基本要素通常称为 ACID 特性。

- 原子性（Atomicity）
- 一个事务是一个不可再分割的工作单位，事务中的所有操作要么都发生，要么都不发生。
- 一致性（Consistency）
- 事务开始之前和事务结束以后，数据库的完整性约束没有被破坏。这是说数据库事务不能破坏关系数据的完整性以及业务逻辑上的一致性。
- 隔离性（Isolation）
- 多个事务并发访问，事务之间是隔离的，一个事务不影响其它事务运行效果。这指的是在并发环境中，当不同的事务同时操作相同的数据时，每个事务都有各自完整的数据空间。事务查看数据更新时，数据所处的状态要么是另一事务修改它之前的状态，要么是另一事务修改后的状态，事务不会查看到中间状态的数据。
- 事务之间的相应影响，分别为：脏读、不可重复读、幻读、丢失更新。
- 持久性（Durability）
- 意味着在事务完成以后，该事务锁对数据库所作的更改便持久的保存在数据库之中，并不会被回滚。

### 6.1.2 ACID 的实现原理

事务可以保证 ACID 原则的操作，那么事务是如何保证这些原则的？解决 ACID 问题的两大技术点是：

* 预写日志（Write-ahead logging）保证原子性和持久性
* 锁（locking）保证隔离性

这里并没有提到一致性，是因为一致性是应用相关的话题，它的定义一个由业务系统来定义，什么样的状态才是一致？而实现一致性的代码通常在业务逻辑的代码中得以体现。

注：锁是指在并发环境中通过读写锁来保证操作的互斥性。根据隔离程度不同，锁的运用也不同。

### 6.1.3 Hive 的 ACID 测试

- Hive不开启事务情况下，开启Concurrency

1.Concurrency配置

```
<property>
<name>hive.support.concurrency</name>
<value>true</value>
</property>
```

2.配置完成后重启hiveserver2

3.创建一个普通的Hive表

```
create table test_notransaction(user_id Int,name String);
create table test(name string, id int);
```

4.准备测试数据，向表中插入数据

```
insert into test_notransaction values(1,'peach1'),(2,'peach2'),(3, 'peach3'),(4, 'peach4');
```

5.开启Concurrency测用例

1)对catalog_sales表进行并发select操作

```
select count(*) from catalog_sales;
select count(*) from catalog_sales;
```

2)对test表进行并发insert操作

```
insert into test values('test11aaa1',1252);
insert into test values('test1',52);
```

3)对test表执行select的同时执行insert操作
alter user 'root'@'localhost' identified by 'root';

GRANT ALL PRIVILEGES ON *.* TO 'root'@'%' IDENTIFIED BY '1234567890' WITH GRANT OPTION;

GRANT ALL PRIVILEGES ON *.* TO 'root'@'0.0.0.0'IDENTIFIED BY 'root' WITH GRANT OPTION;
```
select count(*) from test;
insert into test values("test123",123);
```

4)对test表执行insert的同时执行select操作

```
insert into test values("test123",123);
select count(*) from test;
```

5)对test表进行update和delete操作

```
update test set name='aaaa' where id=1252;
delete test set name='bbbb' where id=123;
```

二、Hive不开启事务情况下关闭Concurrency
1.Concurrency配置

```
<property>
<name>hive.support.concurrency</name>
<value>false</value>
</property>
```

2.配置完成后重启hiveserver2

4.关闭Concurrency测试用例

1)执行insert操作的同时执行select操作

```
insert into test_notransaction values(1,'peach1'),(2,'peach2'),(3, 'peach3'),(4, 'peach4');
select count(*) from test_notransaction;
```

2)执行select操作的同时执行insert操作

```
select count(*) from test_notransaction;
insert into test_notransaction values(1,'peach1'),(2,'peach2'),(3, 'peach3'),(4, 'peach4');
```

3)同时执行多条insert操作

```
insert into test_notransaction values(1,'peach1'),(2,'peach2'),(3, 'peach3'),(4, 'peach4');
insert into test_notransaction values(1,'peach1'),(2,'peach2'),(3, 'peach3'),(4, 'peach4');
```

4)执行update操作，将表中user_id为2的用户名修改为peach22

```
update test_notransaction set name='peach22' where user_id=2;
```

5)执行delete操作，将表中user_id为1信息删除

```
delete from test_notransaction where user_id=1;
```

6)查看表获取锁类型

```
show locks;
```

### 6.1.4 Hive的事务

1.事务配置

```
<property>
<name>hive.support.concurrency</name>
<value>true</value>
</property>
<property>
<name>hive.enforce.bucketing</name>
<value>true</value>
</property>
<property>
<name>hive.exec.dynamic.partition.mode</name>
<value>nonstrict</value>
</property>
<property>
<name>hive.txn.manager</name>
<value>org.apache.hadoop.hive.ql.lockmgr.DbTxnManager</value>
</property>
<property>
<name>hive.compactor.initiator.on</name>
<value>true</value>
</property>
<property>
<name>hive.compactor.worker.threads </name>
<value>1</value>
</property>
```

2.配置完成后重启hiveserver2

3.hive事务建表语句

```
create table test_trancaction (user_id Int,name String)
clustered by (user_id) into 3 buckets stored as orc TBLPROPERTIES ('transactional'='true');
```

修改表名：`alter table test_trancaction rename to test_transaction;`

4.准备测试数据，向表中插入数据

```
insert into test_transaction values(1,'peach'),(2,'peach2'),(3,'peach3'),(4,'peach4'),(5,'peach5');
```

5.hive事务测试用例

1)执行update操作，将user_id的name修改为peach_update

```
update test_transaction set name='peach_update' where user_id=1;
```

2)同时修改同一条数据，将user_id为1的用户名字修改为peach，另一条sql将名字修改为peach_

```
update test_transaction set name='peach' where user_id=1;
update test_transaction set name='peach_' where user_id=1;
```

3)同时修改不同数据，修改id为2的name为peachtest，修改id为3的name为peach_test

```
update test_transaction set name='peachtest' where user_id=2;
update test_transaction set name='peach_test' where user_id=3;
```

4)执行select操作的同时执行insert操作

```
select count(*) from test_transaction;
insert into test_transaction values(3,'peach3');
```

5)update同一条数据的同时select该条数据

```
update test_transaction set name='peach_update' where user_id=1;
select * from test_transaction where user_id=1;
```

6)执行delete操作，将user_id为3的数据删除

```
delete from test_transaction where user_id=3;
```

7)同时delete同一条数据

```
delete from test_transaction where user_id=3;
delete from test_transaction where user_id=3;
```

8)同时delete两条不同的数据

```
delete from test_transaction where user_id=1;
delete from test_transaction where user_id=5;
```

9)执行delete的同时对删除的数据进行update操作

```
delete from test_transaction where user_id=3;
update test_transaction set name='test' where user_id=3;
```

10)执行delete的同时对不同的数据进行update操作

```
delete from test_transaction where user_id=2;
update test_transaction set name='test' where user_id=4;
```

11)执行delete的同时执行select操作

```
delete from test_transaction where user_id=4;
select count(*) from test_transaction;
```

**Hive 事务使用建议**

- 传统数据库中有三种模型隐式事务、显示事务和自动事务。在目前 Hive 对事务仅支持自动事务，因此 Hive 无法通过显示事务的方式对一个操作序列进行事务控制。
- 传统数据库事务在遇到异常情况可自动进行回滚，目前 Hive 无法支持 ROLLBACK。
- 传统数据库中支持事务并发，而 Hive 对事务无法做到完全并发控制, 多个操作均需要获取 WRITE 的时候则这些操作为串行模式执行（在测试用例中"delete 同一条数据的同时 update 该数据"，操作是串行的且操作完成后数据未被删除且数据被修改）未保证数据一致性。
- Hive 的事务功能尚属于实验室功能，并不建议用户直接上生产系统，因为目前它还有诸多的限制，如只支持 ORC 文件格式，建表必须分桶等，使用起来没有那么方便，另外该功能的稳定性还有待进一步验证。
- 如果对于数据一致性不在乎，可以完全关闭 Hive 的 Concurrency 功能关闭，即设置 hive.support.concurrency 为 false，这样 Hive 的并发读写将没有任何限制。

## 6.2 Hive 高级查询

### 6.2.1 排序

#### 1. 全局排序（order by）

Oder By : 全局排序，一个Reduce 默认 ASC (升序)

```sql
select * from emp order by sal;
select * from emp order by sal desc;
select ename, sal*2 twosal from emp order by twosal;
select ename, deptno, sal from emp order by deptno, sal ;
```

#### 2. 每个MapReduce内部排序（Sort By）

Sort By：每个Reducer内部进行排序，对全局结果集来说不是排序。

**设置和查看reduce个数**

```text
hive (default)> set mapreduce.job.reduces=3;
hive (default)> set mapreduce.job.reduces;
mapreduce.job.reduces=3
```

**根据部门编号降序查看员工信息**

```sql
select * from emp sort by empno desc;
```

**将查询结果导入到文件中（按照部门编号降序排序）**

```sql

```

## 6.3 学习参考

1. https://www.infoq.cn/article/guide-of-hive-transaction-management