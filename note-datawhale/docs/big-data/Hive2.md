# task06之二:Hive-数据仓库进阶

---

（本学习笔记整理自[datawhale-大数据处理技术导论](https://github.com/datawhalechina/juicy-bigdata)，部分内容来自其他相关参考教程）


由于hive涉及内容有点多，所以我用了3个篇幅来说明：

1. [task06之一：数据仓库Hive基础](hive.md)
2. [task06之二:Hive-数据仓库进阶](Hive2.md)
3. [task06之三：Apache Hive高级实战](Hive3.md)

**本节目标**

- Hive视图和索引
- Hive数据查询
- Hive常用DDL操作
- Hive常用DML操作

## 6.1 DDL 数据定义

### 6.1.1 创建数据库

1) 创建一个数据库，数据库在HDFS上的默认存储路径是`/user/hive/warehouse/*.db`。 格式：

   ```
   CREATE (DATABASE|SCHEMA) [IF NOT EXISTS] database_name   --DATABASE|SCHEMA 是等价的
   [COMMENT database_comment] --数据库注释
   [LOCATION hdfs_path] --存储在 HDFS 上的位置
   [WITH DBPROPERTIES (property_name=property_value, ...)]; --指定额外属性
   ```

   示例：

   ```sql
   hive (default)> create database db_hive;
   OK
   Time taken: 1.721 seconds
   hive (default)> create database db_hive;
   FAILED: Execution Error, return code 1 from org.apache.hadoop.hive.ql.exec.DDLTask. Database db_hive already exists
   hive (default)> create database if not exists db_hive;
   OK
   Time taken: 0.023 seconds
   hive (default)> 

   ```

   注意：避免要创建的数据库已经存在错误，增加`if not exists`判断。（标准写法）
2) 增加注释

   ```sql
    CREATE DATABASE IF NOT EXISTS hive_test
    COMMENT 'hive database for test'
    WITH DBPROPERTIES ('create'='heibaiying');
   ```

### 6.1.2 查询数据库

#### 6.1.2.1 查看数据列表

```sql
show databases;
```

#### 6.1.2.2 过滤显示查询的数据库

```sql
hive (default)> create database if not exists db_hive1;
OK
Time taken: 0.085 seconds
hive (default)> create database if not exists db_hive2;
OK
Time taken: 0.072 seconds
hive (default)> show databases like '*db_hive';
OK
database_name
db_hive
Time taken: 0.022 seconds, Fetched: 1 row(s)
hive (default)> show databases like 'db_hive*';
OK
database_name
db_hive
db_hive1
db_hive2
```

#### 6.1.1.3 查看数据库信息

语法：

```sql
hive (default)> desc database db_hive;
OK
db_name comment location        owner_name      owner_type      parameters
db_hive         hdfs://hadoop5:8020/user/hive/warehouse/db_hive.db      root    USER  
Time taken: 0.047 seconds, Fetched: 1 row(s)
hive (default)> 

```

显示数据库详细信息，`extended`

```sql
DESC DATABASE  EXTENDED db_hive;
```

#### 6.1.2.4 修改数据库

用户可以使用ALTER DATABASE命令为某个数据库的DBPROPERTIES设置键-值对属性值，来描述这个数据库的属性信息。数据库的其他元数据信息都是不可更改的，包括数据库名和数据库所在的目录位置。

```sql
hive (default)> alter database db_hive set dbproperties('createtime'='20170830');
OK
Time taken: 0.077 seconds
hive (default)> desc database extended db_hive;
OK
db_name comment location        owner_name      owner_type      parameters
db_hive         hdfs://hadoop5:8020/user/hive/warehouse/db_hive.db      root    USER    {createtime=20170830}
Time taken: 0.031 seconds, Fetched: 1 row(s)

```

#### 6.1.2.5 删除数据库

```sql
DROP (DATABASE|SCHEMA) [IF EXISTS] database_name [RESTRICT|CASCADE];
```

默认行为是 RESTRICT，如果数据库中存在表则删除失败。要想删除库及其中的表，可以使用 CASCADE 级联删除。 示例：

```sql
  # CASCADE - 强制删除
  DROP DATABASE IF EXISTS db_hive2 CASCADE;
```

### 6.1.3 创建表

#### 6.1.3.1 建表语法

```sql
CREATE [TEMPORARY] [EXTERNAL] TABLE [IF NOT EXISTS] [db_name.]table_name     --表名
  [(col_name data_type [COMMENT col_comment],
    ... [constraint_specification])]  --列名 列数据类型
  [COMMENT table_comment]   --表描述
  [PARTITIONED BY (col_name data_type [COMMENT col_comment], ...)]  --分区表分区规则
  [
    CLUSTERED BY (col_name, col_name, ...) 
   [SORTED BY (col_name [ASC|DESC], ...)] INTO num_buckets BUCKETS
  ]  --分桶表分桶规则
  [SKEWED BY (col_name, col_name, ...) ON ((col_value, col_value, ...), (col_value, col_value, ...), ...)  
   [STORED AS DIRECTORIES] 
  ]  --指定倾斜列和值
  [
   [ROW FORMAT row_format]  
   [STORED AS file_format]
     | STORED BY 'storage.handler.class.name' [WITH SERDEPROPERTIES (...)]  
  ]  -- 指定行分隔符、存储文件格式或采用自定义存储格式
  [LOCATION hdfs_path]  -- 指定表的存储位置
  [TBLPROPERTIES (property_name=property_value, ...)]  --指定表的属性
  [AS select_statement];   --从查询结果创建表
```

#### 6.1.3.2 字段解释说明

（1）CREATE TABLE 创建一个指定名字的表。如果相同名字的表已经存在，则抛出异常；用户可以用 IF NOT EXISTS 选项来忽略这个异常。

（2）**EXTERNAL关键字可以让用户创建一个外部表，在建表的同时指定一个指向实际数据的路径（LOCATION）**，Hive创建内部表时，会将数据移动到数据仓库指向的路径；若创建外部表，仅记录数据所在的路径，不对数据的位置做任何改变。在删除表的时候，内部表的元数据和数据会被一起删除，而外部表只删除元数据，不删除数据。

（3）COMMENT：为表和列添加注释。

（4）PARTITIONED BY创建分区表

（5）CLUSTERED BY创建分桶表

（6）SORTED BY不常用

（7）ROW FORMAT

DELIMITED [FIELDS TERMINATED BY char] [COLLECTION ITEMS TERMINATED BY char]
[MAP KEYS TERMINATED BY char] [LINES TERMINATED BY char]
| SERDE serde_name [WITH SERDEPROPERTIES (property_name=property_value, property_name=property_value, ...)]

用户在建表的时候可以自定义SerDe或者使用自带的SerDe。如果没有指定ROW FORMAT 或者ROW FORMAT
DELIMITED，将会使用自带的SerDe。在建表的时候，用户还需要为表指定列，用户在指定表的列的同时也会指定自定义的SerDe，Hive通过SerDe确定表的具体的列的数据。

SerDe是Serialize/Deserilize的简称，目的是用于序列化和反序列化。

（8）STORED AS指定存储文件类型

常用的存储文件类型：SEQUENCEFILE（二进制序列文件）、TEXTFILE（文本）、RCFILE（列式存储格式文件）

**如果文件数据是纯文本，可以使用STORED AS TEXTFILE。如果数据需要压缩，使用 STORED AS SEQUENCEFILE。**

（9）LOCATION ：指定表在HDFS上的存储位置。

（10）LIKE允许用户复制现有的表结构，但是不复制数据。

### 6.1.4 管理表（内部表）

默认创建的表都是所谓的**管理表**，有时也被称为内部表。因为这种表，Hive会（或多或少地）控制着数据的生命周期。Hive默认情况下会将这些表的数据存储在由配置项`hive.metastore.warehouse.dir`(
例如，`/user/hive/warehouse`)所定义的目录的子目录下。

**当我们删除一个管理表时，Hive也会删除这个表中数据。** 管理表不适合和其他工具共享数据。

1. 案例实操：

```sql
  CREATE TABLE emp(
    empno INT,
    ename STRING,
    job STRING,
    mgr INT,
    hiredate TIMESTAMP,
    sal DECIMAL(7,2),
    comm DECIMAL(7,2),
    deptno INT)
    ROW FORMAT DELIMITED FIELDS TERMINATED BY "\t"
    stored as textfile
    location '/user/hive/warehouse/student2';
```

2. 根据查询结构创建表（查询结果会添加到新创建的表中）

```sql
hive (default)> create table if not exists student3 as select id, name from student;
```

3. 根据已经存在的表结构创建表

```sql
hive (default)> create table if not exists student4 like student;
```

4. 查询表的类型

```sql
hive (default)> desc formatted student;
Table Type:             MANAGED_TABLE
```

5. 删除表

```sql
drop table IF EXISTS student4
```

- 内部表：不仅会删除表的元数据，同时会删除 HDFS 上的数据；
- 外部表：只会删除表的元数据，不会删除 HDFS 上的数据；
- 删除视图引用的表时，不会给出警告（但视图已经无效了，必须由用户删除或重新创建）。

### 6.1.5 外部表

因为表是外部表，所以Hive并非认为其完全拥有这份数据。**删除表并不会删除掉这份数据，不过描述表的元数据信息会被删除掉。**

**管理表和外部表使用场景：**

> 每天将收集到的网站日志定期流入HDFS文本文件。在外部表（原始日志表）的基础做统计分析，涉及到的中间表、结果表则用内部表存储，数据通过select + insert写入内部表。

```sql
  CREATE EXTERNAL TABLE emp_external(
    empno INT,
    ename STRING,
    job STRING,
    mgr INT,
    hiredate TIMESTAMP,
    sal DECIMAL(7,2),
    comm DECIMAL(7,2),
    deptno INT)
    ROW FORMAT DELIMITED FIELDS TERMINATED BY "\t"
    LOCATION '/hive/emp_external';
```

使用 `desc formatted emp_external` 命令可以查看表的详细信息如下：

```shell
hive (default)> desc formatted emp_external
              > ;
OK
col_name        data_type       comment
# col_name              data_type               comment   
     
empno                   int                             
ename                   string                          
job                     string                          
mgr                     int                             
hiredate                timestamp                       
sal                     decimal(7,2)                    
comm                    decimal(7,2)                    
deptno                  int                             
     
# Detailed Table Information   
Database:               default      
Owner:                  root         
CreateTime:             Tue Apr 19 22:52:05 CST 2022   
LastAccessTime:         UNKNOWN      
Retention:              0            
Location:               hdfs://hadoop5:8020/hive/emp_external    # 存放位置 
Table Type:             EXTERNAL_TABLE     # 标识外部表   
Table Parameters:    
        EXTERNAL                TRUE    
        transient_lastDdlTime   1650379925  
     
# Storage Information  
SerDe Library:          org.apache.hadoop.hive.serde2.lazy.LazySimpleSerDe   
InputFormat:            org.apache.hadoop.mapred.TextInputFormat   
OutputFormat:           org.apache.hadoop.hive.ql.io.HiveIgnoreKeyTextOutputFormat   
Compressed:             No           
Num Buckets:            -1           
Bucket Columns:         []           
Sort Columns:           []           
Storage Desc Params:   
        field.delim             \t      
        serialization.format    \t      
Time taken: 0.1 seconds, Fetched: 34 row(s)

```

### 6.1.6 外部表和内部表示例

分别创建部门和员工外部表，并向表中导入数据。
（1）原始数据文件 `dept.txt` 和 `emp.txt`

```text
# dept.txt
10	ACCOUNTING	1700
20	RESEARCH	1800
30	SALES	1900
40	OPERATIONS	1700

# emp.txt
7369	SMITH	CLERK	7902	1980-12-17	800.00		20
7499	ALLEN	SALESMAN	7698	1981-2-20	1600.00	300.00	30
7521	WARD	SALESMAN	7698	1981-2-22	1250.00	500.00	30
7566	JONES	MANAGER	7839	1981-4-2	2975.00		20
7654	MARTIN	SALESMAN	7698	1981-9-28	1250.00	1400.00	30
7698	BLAKE	MANAGER	7839	1981-5-1	2850.00		30
7782	CLARK	MANAGER	7839	1981-6-9	2450.00		10
7788	SCOTT	ANALYST	7566	1987-4-19	3000.00		20
7839	KING	PRESIDENT		1981-11-17	5000.00		10
7844	TURNER	SALESMAN	7698	1981-9-8	1500.00	0.00	30
7876	ADAMS	CLERK	7788	1987-5-23	1100.00		20
7900	JAMES	CLERK	7698	1981-12-3	950.00		30
7902	FORD	ANALYST	7566	1981-12-3	3000.00		20
7934	MILLER	CLERK	7782	1982-1-23	1300.00		10
```

（2）建表语句

1. 创建部门表

```sql
create external table if not exists default.dept(
deptno int,
dname string,
loc int
)
row format delimited fields terminated by '\t';
```

2.创建员工表

```sql
create external table if not exists default.emp(
empno int,
ename string,
job string,
mgr int,
hiredate string, 
sal double, 
comm double,
deptno int)
row format delimited fields terminated by '\t';
```

3. 查看创建的表

```sql
hive (default)> show tables;
OK
tab_name
dept
emp
```

4. 向外部表中导入数据
   通过

```text
[root@hadoop5 hive_stage]# pwd
/root/hdp/hive_stage
[root@hadoop5 hive_stage]# touch emp.txt
[root@hadoop5 hive_stage]# vi emp.txt
[root@hadoop5 hive_stage]# cat emp.txt
7369    SMITH   CLERK   7902    1980-12-17      800.00          20
7499    ALLEN   SALESMAN        7698    1981-2-20       1600.00 300.00  30
7521    WARD    SALESMAN        7698    1981-2-22       1250.00 500.00  30
7566    JONES   MANAGER 7839    1981-4-2        2975.00         20
7654    MARTIN  SALESMAN        7698    1981-9-28       1250.00 1400.00 30
7698    BLAKE   MANAGER 7839    1981-5-1        2850.00         30
7782    CLARK   MANAGER 7839    1981-6-9        2450.00         10
7788    SCOTT   ANALYST 7566    1987-4-19       3000.00         20
7839    KING    PRESIDENT               1981-11-17      5000.00         10
7844    TURNER  SALESMAN        7698    1981-9-8        1500.00 0.00    30
7876    ADAMS   CLERK   7788    1987-5-23       1100.00         20
7900    JAMES   CLERK   7698    1981-12-3       950.00          30
7902    FORD    ANALYST 7566    1981-12-3       3000.00         20
7934    MILLER  CLERK   7782    1982-1-23       1300.00         10

[root@hadoop5 hive_stage]# touch dept.txt
[root@hadoop5 hive_stage]# vi dept.txt 
[root@hadoop5 hive_stage]# cat dept.txt
10      ACCOUNTING      1700
20      RESEARCH        1800
30      SALES   1900
40      OPERATIONS      17001
[root@hadoop5 hive_stage]# ls -l 
-rw-r--r--. 1 root root  78 4月  19 23:12 dept.txt
-rw-r--r--. 1 root root 657 4月  19 23:13 emp.txt
hive (default)> load data local inpath '/root/hdp/hive_stage/dept.txt' into table default.dept;
hive (default)> load data local inpath '/root/hdp/hive_stage/emp.txt' into table default.emp;
```

### 6.1.7 管理表与外部表的互相转换

1）查询表的类型

```
hive (default)> desc formatted student2;

Table Type: MANAGED_TABLE
```

（2）修改内部表student2为外部表

```
alter table student2 set tblproperties('EXTERNAL'='TRUE');
```

（3）查询表的类型

```
hive (default)> desc formatted student2;

Table Type: EXTERNAL_TABLE
```

（4）修改外部表student2为内部表

```
alter table student2 set tblproperties('EXTERNAL'='FALSE');
```

（5）查询表的类型

```
hive (default)> desc formatted student2;

Table Type: MANAGED_TABLE
```

注意：`('EXTERNAL'='TRUE')`和`('EXTERNAL'='FALSE')`为固定写法，区分大小写！

（6）重命名表

```text
alter table student3 rename to student2;
```

（7）增加/修改/替换列信息

```text
ALTER TABLE name RENAME TO new_name
ALTER TABLE name ADD COLUMNS (col_spec[, col_spec ...])
ALTER TABLE name DROP [COLUMN] column_name
ALTER TABLE name CHANGE column_name new_name new_type
ALTER TABLE name REPLACE COLUMNS (col_spec[, col_spec ...])
```

具体操作，可以参照[此处](https://blog.csdn.net/helloxiaozhe/article/details/80749094)

#### 6.1.8 分区表

分区表实际上就是对应一个HDFS文件系统上的独立的文件夹，该文件夹下该分区所有的数据文件。**hive中的分区就是分目录**，把一个大的数据集根据业务需要分割成小的数据集。在查询通过where子句中的表达式选择查询所需要的指定的分区，这样的查询效率会提高很多。
1．引入分区表（需要根据日期对日志进行管理）

```text
/user/hive/warehouse/log_partition/20170702/20170702.log
/user/hive/warehouse/log_partition/20170703/20170703.log
/user/hive/warehouse/log_partition/20170704/20170704.log
```

2. 创建分区表语法

```sql
create table dept_partition(
deptno int, dname string, loc string
)
partitioned by (month string)
row format delimited fields terminated by '\t';
```

3. 加载数据到分区表中

```sql
hive (default)> load data local inpath '/root/hdp/hive_stage/dept.txt' into table default.dept_partition partition(month='202201');
Loading data to table default.dept_partition partition (month=202201)
OK
Time taken: 2.737 seconds
hive (default)> load data local inpath '/root/hdp/hive_stage/dept.txt' into table default.dept_partition partition(month='202202');
Loading data to table default.dept_partition partition (month=202202)
OK
Time taken: 1.034 seconds
hive (default)> load data local inpath '/root/hdp/hive_stage/dept.txt' into table default.dept_partition partition(month='202203');
Loading data to table default.dept_partition partition (month=202203)
OK
Time taken: 1.023 seconds

```

4. 查看数据

```shell
[root@hadoop5 hive_stage]# hadoop fs -ls /user/hive/warehouse/dept_partition
Found 3 items
drwxrwxrwx   - root supergroup          0 2022-04-20 00:09 /user/hive/warehouse/dept_partition/month=202201
drwxrwxrwx   - root supergroup          0 2022-04-20 00:09 /user/hive/warehouse/dept_partition/month=202202
drwxrwxrwx   - root supergroup          0 2022-04-20 00:09 /user/hive/warehouse/dept_partition/month=202203
```

5. 查询分区表中的数据

```shell
hive (default)> select * from dept_partition where month='202201';
OK
dept_partition.deptno   dept_partition.dname    dept_partition.loc      dept_partition.month
10      ACCOUNTING      1700    202201
20      RESEARCH        1800    202201
30      SALES   1900    202201
40      OPERATIONS      17001   202201
Time taken: 3.049 seconds, Fetched: 4 row(s)
hive (default)> select * from dept_partition where month='202202';
OK
dept_partition.deptno   dept_partition.dname    dept_partition.loc      dept_partition.month
10      ACCOUNTING      1700    202202
20      RESEARCH        1800    202202
30      SALES   1900    202202
40      OPERATIONS      17001   202202
Time taken: 0.341 seconds, Fetched: 4 row(s)
hive (default)> select * from dept_partition where month='202203';
OK
dept_partition.deptno   dept_partition.dname    dept_partition.loc      dept_partition.month
10      ACCOUNTING      1700    202203
20      RESEARCH        1800    202203
30      SALES   1900    202203
40      OPERATIONS      17001   202203
Time taken: 0.276 seconds, Fetched: 4 row(s)
hive (default) select * from dept_partition where month='202203'
              union 
              select * from dept_partition where month='202202'
              union
              select * from dept_partition where month='202201';
OK
_u2.deptno      _u2.dname       _u2.loc _u2.month
10      ACCOUNTING      1700    202201
10      ACCOUNTING      1700    202202
10      ACCOUNTING      1700    202203
20      RESEARCH        1800    202201
20      RESEARCH        1800    202202
20      RESEARCH        1800    202203
30      SALES   1900    202201
30      SALES   1900    202202
30      SALES   1900    202203
40      OPERATIONS      17001   202201
40      OPERATIONS      17001   202202
40      OPERATIONS      17001   202203
Time taken: 77.985 seconds, Fetched: 12 row(s)
```

6．增加分区

```shell
#创建单个分区
hive (default)> alter table dept_partition add partition(month='202204') ;
OK
Time taken: 0.209 seconds
#创建多个分区
hive (default)> alter table dept_partition add partition(month='202205') partition(month='202206');
OK
Time taken: 0.182 seconds
```

7. 删除分区

```shell
# 删除分区
hive (default)> alter table dept_partition drop partition (month='202204');
hive (default)> alter table dept_partition drop partition (month='202205'), partition (month='202206');
```

8. 显示多少分区

```shell
show partitions dept_partition;
```

8. 查看分区表结构

```shell
#管理表信息时查看
hive (default)> desc formatted dept_partition;
Location:               hdfs://hadoop5:8020/user/hive/warehouse/dept_partition   
Table Type:             MANAGED_TABLE  
[root@hadoop5 hive_stage]# hadoop fs -ls /user/hive/warehouse/dept_partition
Found 6 items
drwxrwxrwx   - root supergroup          0 2022-04-20 00:09 /user/hive/warehouse/dept_partition/month=202201
drwxrwxrwx   - root supergroup          0 2022-04-20 00:09 /user/hive/warehouse/dept_partition/month=202202
drwxrwxrwx   - root supergroup          0 2022-04-20 00:09 /user/hive/warehouse/dept_partition/month=202203
drwxrwxrwx   - root supergroup          0 2022-04-20 00:22 /user/hive/warehouse/dept_partition/month=202204
drwxrwxrwx   - root supergroup          0 2022-04-20 00:22 /user/hive/warehouse/dept_partition/month=202205
drwxrwxrwx   - root supergroup          0 2022-04-20 00:22 /user/hive/warehouse/dept_partition/month=202206
#删除分区
hive (default)> alter table dept_partition drop partition (month='202201');
Dropped the partition month=202201
OK
Time taken: 1.759 seconds
#查询分区数和文件价均已被删除
[root@hadoop5 hive_stage]# hadoop fs -ls /user/hive/warehouse/dept_partition
Found 5 items
drwxrwxrwx   - root supergroup          0 2022-04-20 00:09 /user/hive/warehouse/dept_partition/month=202202
drwxrwxrwx   - root supergroup          0 2022-04-20 00:09 /user/hive/warehouse/dept_partition/month=202203
drwxrwxrwx   - root supergroup          0 2022-04-20 00:22 /user/hive/warehouse/dept_partition/month=202204
drwxrwxrwx   - root supergroup          0 2022-04-20 00:22 /user/hive/warehouse/dept_partition/month=202205
drwxrwxrwx   - root supergroup          0 2022-04-20 00:22 /user/hive/warehouse/dept_partition/month=202206
#改为外部表
hive (default)> alter table dept_partition set tblproperties('EXTERNAL'='TRUE');
hive (default)> alter table dept_partition drop partition (month='202202');
Dropped the partition month=202202
OK
Time taken: 0.2 seconds
#查询分区数202202已被删除
hive (default)> show partitions dept_partition;
OK
partition
month=202203
month=202204
month=202205
month=202206
Time taken: 0.225 seconds, Fetched: 4 row(s)
#检查文件是否存在
[root@hadoop5 hive_stage]# hadoop fs -ls /user/hive/warehouse/dept_partition
Found 5 items
drwxrwxrwx   - root supergroup          0 2022-04-20 00:09 /user/hive/warehouse/dept_partition/month=202202
drwxrwxrwx   - root supergroup          0 2022-04-20 00:09 /user/hive/warehouse/dept_partition/month=202203
drwxrwxrwx   - root supergroup          0 2022-04-20 00:22 /user/hive/warehouse/dept_partition/month=202204
drwxrwxrwx   - root supergroup          0 2022-04-20 00:22 /user/hive/warehouse/dept_partition/month=202205
drwxrwxrwx   - root supergroup          0 2022-04-20 00:22 /user/hive/warehouse/dept_partition/month=202206
# 外部表的HDFS文件依然存在；
```

9. 创建二级分区表

```text
hive (default)> create table dept_partition2(
               deptno int, dname string, loc string
               )
               partitioned by (month string, day string)
               row format delimited fields terminated by '\t';
```

10. 加载数据到二级分区表

```text
load data local inpath '/root/hdp/hive_stage/dept.txt' into table default.dept_partition2 partition(month='202203', day='13');
```

> 注意：二级分区会出现查询不到数据问题，注意修复；

11. 分区排序（Distribute By）
    Distribute By：类似MR中partition，进行分区，结合sort by使用。
    注意，Hive要求DISTRIBUTE BY语句要写在SORT BY语句之前。
    对于distribute by进行测试，一定要分配多reduce进行处理，否则无法看到distribute by的效果。
    案例实操：
    （1）先按照部门编号分区，再按照员工编号降序排序。

```
hive (default)> set mapreduce.job.reduces=3;
hive (default)> insert overwrite local directory '/opt/module/datas/distribute-result' select * from emp distribute by deptno sort by empno desc;
```

12. Cluster By
    当distribute by和sorts by字段相同时，可以使用cluster by方式。
    cluster by除了具有distribute by的功能外还兼具sort by的功能。但是排序只能是升序排序，不能指定排序规则为ASC或者DESC。
    1）以下两种写法等价

```
hive (default)> select * from emp cluster by deptno;
hive (default)> select * from emp distribute by deptno sort by deptno;
```

注意：按照部门编号分区，不一定就是固定死的数值，可以是20号和30号部门分到一个分区里面去。

#### 6.1.9 分桶表

```sql
  CREATE EXTERNAL TABLE emp_bucket(
    empno INT,
    ename STRING,
    job STRING,
    mgr INT,
    hiredate TIMESTAMP,
    sal DECIMAL(7,2),
    comm DECIMAL(7,2),
    deptno INT)
    CLUSTERED BY(empno) SORTED BY(empno ASC) INTO 4 BUCKETS  --按照员工编号散列到四个 bucket 中
    ROW FORMAT DELIMITED FIELDS TERMINATED BY "\t"
    LOCATION '/hive/emp_bucket';
```

#### 6.1.10 倾斜表

通过指定一个或者多个列经常出现的值（严重偏斜），Hive 会自动将涉及到这些值的数据拆分为单独的文件。在查询时，如果涉及到倾斜值，它就直接从独立文件中获取数据，而不是扫描所有文件，这使得性能得到提升。

```sql
  CREATE EXTERNAL TABLE emp_skewed(
    empno INT,
    ename STRING,
    job STRING,
    mgr INT,
    hiredate TIMESTAMP,
    sal DECIMAL(7,2),
    comm DECIMAL(7,2)
    )
    SKEWED BY (empno) ON (66,88,100)  --指定 empno 的倾斜值 66,88,100
    ROW FORMAT DELIMITED FIELDS TERMINATED BY "\t"
    LOCATION '/hive/emp_skewed';
```

#### 6.1.11 临时表

临时表仅对当前 session 可见，临时表的数据将存储在用户的暂存目录中，并在会话结束后删除。如果临时表与永久表表名相同，则对该表名的任何引用都将解析为临时表，而不是永久表。临时表还具有以下两个限制：

* 不支持分区列；
* 不支持创建索引。

```sql
  CREATE TEMPORARY TABLE emp_temp(
    empno INT,
    ename STRING,
    job STRING,
    mgr INT,
    hiredate TIMESTAMP,
    sal DECIMAL(7,2),
    comm DECIMAL(7,2)
    )
    ROW FORMAT DELIMITED FIELDS TERMINATED BY "\t";
```

#### 6.1.12 CTAS创建表

支持从查询语句的结果创建表：

```sql
CREATE TABLE emp_copy AS SELECT * FROM emp WHERE deptno='20';
```

#### 6.1.13 复制表结构

语法：

```sql
CREATE [TEMPORARY] [EXTERNAL] TABLE [IF NOT EXISTS] [db_name.]table_name  --创建表表名
   LIKE existing_table_or_view_name  --被复制表的表名
   [LOCATION hdfs_path]; --存储位置
```

示例：

```sql
CREATE TEMPORARY EXTERNAL TABLE  IF NOT EXISTS  emp_co  LIKE emp
```

#### 6.1.14 加载数据到表

加载数据到表中属于 DML 操作，这里为了方便大家测试，先简单介绍一下加载本地数据到表中：

```sql
-- 加载数据到 emp 表中
load data local inpath "/usr/file/emp.txt" into table emp;
```

其中 emp.txt 的内容如下，你可以直接复制使用，也可以到本仓库的[resources](https://github.com/heibaiying/BigData-Notes/tree/master/resources) 目录下载：

```sql
7369    SMITH    CLERK    7902    1980-12-17 00:00:00    800.00        20
7499    ALLEN    SALESMAN    7698    1981-02-20 00:00:00    1600.00    300.00    30
7521    WARD    SALESMAN    7698    1981-02-22 00:00:00    1250.00    500.00    30
7566    JONES    MANAGER    7839    1981-04-02 00:00:00    2975.00        20
7654    MARTIN    SALESMAN    7698    1981-09-28 00:00:00    1250.00    1400.00    30
7698    BLAKE    MANAGER    7839    1981-05-01 00:00:00    2850.00        30
7782    CLARK    MANAGER    7839    1981-06-09 00:00:00    2450.00        10
7788    SCOTT    ANALYST    7566    1987-04-19 00:00:00    1500.00        20
7839    KING    PRESIDENT        1981-11-17 00:00:00    5000.00        10
7844    TURNER    SALESMAN    7698    1981-09-08 00:00:00    1500.00    0.00    30
7876    ADAMS    CLERK    7788    1987-05-23 00:00:00    1100.00        20
7900    JAMES    CLERK    7698    1981-12-03 00:00:00    950.00        30
7902    FORD    ANALYST    7566    1981-12-03 00:00:00    3000.00        20
7934    MILLER    CLERK    7782    1982-01-23 00:00:00    1300.00        10
```

### 6.1.3 修改表

#### 6.1.3.1 重命名表

语法：

```sql
ALTER TABLE table_name RENAME TO new_table_name;
```

示例：

```sql
ALTER TABLE emp_temp RENAME TO new_emp; --把 emp_temp 表重命名为 new_emp
```

#### 6.1.3.2 修改列

语法：

````sql
ALTER TABLE table_name [PARTITION partition_spec] CHANGE [COLUMN] col_old_name col_new_name column_type
  [COMMENT col_comment] [FIRST|AFTER column_name] [CASCADE|RESTRICT];

````

示例：

```sql
-- 修改字段名和类型
ALTER TABLE emp_temp CHANGE empno empno_new INT;

-- 修改字段 sal 的名称 并将其放置到 empno 字段后
ALTER TABLE emp_temp CHANGE sal sal_new decimal(7,2)  AFTER ename;

-- 为字段增加注释
ALTER TABLE emp_temp CHANGE mgr mgr_new INT COMMENT 'this is column mgr';
```

#### 6.1.3.3 新增列

示例：

````sql
ALTER TABLE emp_temp ADD COLUMNS (address STRING COMMENT 'home address');

````

### 6.1.4 清空表/删除表

#### 6.1.4.1 清空表

语法：

```sql
-- 清空整个表或表指定分区中的数据
TRUNCATE TABLE table_name [PARTITION (partition_column = partition_col_value,  ...)];
```

目前只有内部表才能执行 TRUNCATE 操作，外部表执行时会抛出异常 `Cannot truncate non-managed table XXXX`。

示例：

```sql
TRUNCATE TABLE emp_mgt_ptn PARTITION (deptno=20);
```

#### 6.1.4.2 删除表

语法：

```sql
DROP TABLE [IF EXISTS] table_name [PURGE];
```

* 内部表：不仅会删除表的元数据，同时会删除 HDFS 上的数据；
* 外部表：只会删除表的元数据，不会删除 HDFS 上的数据；
* 删除视图引用的表时，不会给出警告（但视图已经无效了，必须由用户删除或重新创建）。

### 6.1.5 其他命令

#### 6.1.5.1 Describe

查看数据库：

```sql
DESCRIBE|Desc DATABASE [EXTENDED] db_name;  --EXTENDED 是否显示额外属性
```

查看表：

```sql
DESCRIBE|Desc [EXTENDED|FORMATTED] table_name --FORMATTED 以友好的展现方式查看表详情
```

#### 6.1.5.2 Show

查看数据库列表

```sql
-- 语法
SHOW (DATABASES|SCHEMAS) [LIKE 'identifier_with_wildcards'];

-- 示例：
SHOW DATABASES like 'hive*';
```

LIKE 子句允许使用正则表达式进行过滤，但是 SHOW 语句当中的 LIKE 子句只支持 `*`（通配符）和 `|`（条件或）两个符号。例如 `employees`，`emp *`，`emp * | * ees`
，所有这些都将匹配名为 `employees` 的数据库。

查看表的列表

```sql
-- 语法
SHOW TABLES [IN database_name] ['identifier_with_wildcards'];

-- 示例
SHOW TABLES IN default;
```

查看视图列表

```sql
SHOW VIEWS [IN/FROM database_name] [LIKE 'pattern_with_wildcards'];   --仅支持 Hive 2.2.0 +
```

查看表的分区列表

```sql
SHOW PARTITIONS table_name;
```

查看表/视图的创建语句

````sql
SHOW CREATE TABLE ([db_name.]table_name|view_name);
````

### 6.1.6 Hive 聚合函数

- 排序：ROW_NUMBER, RANK, DENSE_RANK, NLITE, PERCENT_RANK
- 统计：COUNT, SUM, AVG MAX, MIN
- 分析：CUME_DIST, LEAD, LAG, FIRST_VALUE, LAST_VALUE WINDOW clause (窗口的定义) Case Study (案例分析)

```sql
desc function funcName desc function extended funcName concat_ws：函数用法 collect_set：函数用法 collect_set：返回一个不带重复数据的集合,需要配合group by使用，类似于多行转换为一行
-- 举个栗子
--将一张表中特定字段的行进行合并，并且不对重复的数据进行去重如下，数据形式如下，要对from字段进行 进行合并 subtype from id name type null CommonModule 5 3公立内 Distance null CommonModule 4 2公立内 sort
--concat_ws和collect_set()函数实现（对某列进行去重） 其作用是将多行某些列的多行进行去重合并， 并通过&符 号进行连接，代码如下 select subtype ,concat_ws('&',collect_set(cast(from as string))) from ,concat_ws('&',collect_set(cast(id as string))) id ,concat_ws('&',collect_set(cast(name as string)))name ,concat_ws('&',collect_set(cast(type as string))) type
from table group by subtype; null CommonModule 4&5 2公立内&3公立内 sort&Distance
-- 2、concat_ws和collect_list()函数实现（对某列不进行去重） select subtype ,concat_ws('&',collect_list(cast(from as string))) from ,concat_ws('&',collect_list(cast(id as string))) id ,concat_ws('&',collect_list(cast(name as string)))name ,concat_ws('&',collect_list(cast(type as string))) type
from table group by subtype; null CommonModule&CommonModule 4&5 2公立内&3公立内 sort&Distance
```

- 基本函数的使用

```
1.查看month 相关的函数 show functions like '*month*' 输出如下:
2.查看 add_months 函数的用法 desc function add_months; 
3.查看 add_months 函数的详细说明并举例 desc function extended add_months;
```

### 6.1.7 Hive Window Functions 语法

- 我们都知道在sql中有一类函数叫做聚合函数,例如sum()、avg()、max()等等,这类函数可以将多行数 据按照规则聚集为一行,一般来讲聚集后的行数是要少于聚集前的行数的.但是有时我们想要既显示
  聚集前的数据,又要显示聚集后的数据,这时我们便引入了窗口函数。
- 从Hive 0.11.0开始添加，Hive窗口函数是一组特殊 的函数，它们扫描多个输入行以计算每个输出值
- 分析函数功能强大，不受GROUP BY的限制
- 可以通过它完成复杂的计算和聚合

lag() lead() first_value() last_value()

```
lag()
LAG(col,n,DEFAULT) 用于统计窗口内往上第n行值
第一个参数为列名，第二个参数为往上第n行（可选，默认为1），第三个参数为默认值（当往上n行之内，若当某一行为NULL时候，取默认值，如不指定，则为NULL）
```

```
lead()
与LAG相反
LEAD(col,n,DEFAULT) 用于统计窗口内往下第n行值
第一个参数为列名，第二个参数为往下第n行（可选，默认为1），第三个参数为默认值（当往下第n行为NULL时候，取默认值，如不指定，则为NULL）
```

```
first_value()
取分组内排序后，截止到当前行，第一个值.
如果不指定ORDER BY，则默认按照记录在文件中的偏移量进行排序，会出现错误的结果
```

```
ast_value()
取分组内排序后，截止到当前行，最后一个值
如果不指定ORDER BY，则默认按照记录在文件中的偏移量进行排序，会出现错误的结果
```

## 6.2 DML操作

### 6.2.1 加载文件数据到表

#### 6.2.1.1 语法

```sql
LOAD DATA [LOCAL] INPATH 'filepath' [OVERWRITE] 
INTO TABLE tablename [PARTITION (partcol1=val1, partcol2=val2 ...)]
```

（1）load data:表示加载数据
（2）local:表示从本地加载数据到hive表；否则从HDFS加载数据到hive表
（3）inpath:表示加载数据的路径
（4）overwrite:表示覆盖表中已有数据，否则表示追加
（5）into table:表示加载到哪张表
（6）student:表示具体的表
（7）partition:表示上传到指定分区

* `LOCAL` 关键字代表从本地文件系统加载文件，省略则代表从 HDFS 上加载文件：
* 从本地文件系统加载文件时， `filepath` 可以是绝对路径也可以是相对路径 (建议使用绝对路径)；
* 从 HDFS 加载文件时候，`filepath` 为文件完整的 URL 地址：如 `hdfs://namenode:port/user/hive/project/ data1`
* `filepath` 可以是文件路径 (在这种情况下 Hive 会将文件移动到表中)，也可以目录路径 (在这种情况下，Hive 会将该目录中的所有文件移动到表中)；
* 如果使用 OVERWRITE 关键字，则将删除目标表（或分区）的内容，使用新的数据填充；不使用此关键字，则数据以追加的方式加入；
* 加载的目标可以是表或分区。如果是分区表，则必须指定加载数据的分区；
* 加载文件的格式必须与建表时使用 `STORED AS` 指定的存储格式相同。

  > 使用建议：
  >
  > **不论是本地路径还是 URL 都建议使用完整的** 。虽然可以使用不完整的 URL 地址，此时 Hive 将使用 hadoop 中的 fs.default.name 配置来推断地址，但是为避免不必要的错误，建议使用完整的本地路径或 URL 地址；
  >
  > **加载对象是分区表时建议显示指定分区** 。在 Hive 3.0 之后，内部将加载 (LOAD) 重写为 INSERT AS SELECT，此时如果不指定分区，INSERT AS SELECT 将假设最后一组列是分区列，如果该列不是表定义的分区，它将抛出错误。为避免错误，还是建议显示指定分区。
>

#### 6.2.1.2 示例

新建分区表：

```sql
  CREATE TABLE emp_ptn(
    empno INT,
    ename STRING,
    job STRING,
    mgr INT,
    hiredate TIMESTAMP,
    sal DECIMAL(7,2),
    comm DECIMAL(7,2)
    )
    PARTITIONED BY (deptno INT)   -- 按照部门编号进行分区
    ROW FORMAT DELIMITED FIELDS TERMINATED BY "\t";
```

从 HDFS 上加载数据到分区表：

````sql
LOAD DATA  INPATH "hdfs://hadoop001:8020/mydir/emp.txt" OVERWRITE INTO TABLE emp_ptn PARTITION (deptno=20);
````

> emp.txt 文件可在本仓库的 resources 目录中下载

加载后表中数据如下,分区列 deptno 全部赋值成 20：

![img](./images/2020-10-19-ULIqBH.jpg)

### 6.2.2 查询结果插入到表

#### 6.2.2.1 语法

```sql
INSERT OVERWRITE TABLE tablename1 [PARTITION (partcol1=val1, partcol2=val2 ...) [IF NOT EXISTS]]   
select_statement1 FROM from_statement;

INSERT INTO TABLE tablename1 [PARTITION (partcol1=val1, partcol2=val2 ...)] 
select_statement1 FROM from_statement;
```

* Hive 0.13.0 开始，建表时可以通过使用 TBLPROPERTIES（“immutable”=“true”）来创建不可变表 (immutable table) ，如果不可以变表中存在数据，则 INSERT INTO
  失败。（注：INSERT OVERWRITE 的语句不受 `immutable` 属性的影响）;
* 可以对表或分区执行插入操作。如果表已分区，则必须通过指定所有分区列的值来指定表的特定分区；
* 从 Hive 1.1.0 开始，TABLE 关键字是可选的；
* 从 Hive 1.2.0 开始 ，可以采用 INSERT INTO tablename(z，x，c1) 指明插入列；
* 可以将 SELECT 语句的查询结果插入多个表（或分区），称为多表插入。语法如下：

````sql
  FROM from_statement
  INSERT OVERWRITE TABLE tablename1 
  [PARTITION (partcol1=val1, partcol2=val2 ...) [IF NOT EXISTS]] select_statement1
  [INSERT OVERWRITE TABLE tablename2 [PARTITION ... [IF NOT EXISTS]] select_statement2]
  [INSERT INTO TABLE tablename2 [PARTITION ...] select_statement2] ...;
````

#### 6.2.2.2 动态插入分区

```sql
INSERT OVERWRITE TABLE tablename PARTITION (partcol1[=val1], partcol2[=val2] ...) 
select_statement FROM from_statement;

INSERT INTO TABLE tablename PARTITION (partcol1[=val1], partcol2[=val2] ...) 
select_statement FROM from_statement;
```

在向分区表插入数据时候，分区列名是必须的，但是列值是可选的。如果给出了分区列值，我们将其称为静态分区，否则它是动态分区。动态分区列必须在 SELECT 语句的列中最后指定，并且与它们在 PARTITION() 子句中出现的顺序相同。

注意：Hive 0.9.0 之前的版本动态分区插入是默认禁用的，而 0.9.0 之后的版本则默认启用。以下是动态分区的相关配置：

`hive.exec.dynamic.partition`

默认值：`true`

说明：需要设置为 true 才能启用动态分区插入

`hive.exec.dynamic.partition.mode`

默认值：`strict`

说明：在严格模式 (strict) 下，用户必须至少指定一个静态分区，以防用户意外覆盖所有分区，在非严格模式下，允许所有分区都是动态的

`hive.exec.max.dynamic.partitions.pernode`

默认值：100

说明：允许在每个 mapper/reducer 节点中创建的最大动态分区数

`hive.exec.max.dynamic.partitions`

默认值：1000

说明：允许总共创建的最大动态分区数

`hive.exec.max.created.files`

默认值：100000

说明：作业中所有 mapper/reducer 创建的 HDFS 文件的最大数量

`hive.error.on.empty.partition`

默认值：`false`

说明：如果动态分区插入生成空结果，是否抛出异常

#### 6.2.2.3 示例

1. **1.**新建 emp 表，作为查询对象表

```sql
CREATE TABLE emp(
    empno INT,
    ename STRING,
    job STRING,
    mgr INT,
    hiredate TIMESTAMP,
    sal DECIMAL(7,2),
    comm DECIMAL(7,2),
    deptno INT)
    ROW FORMAT DELIMITED FIELDS TERMINATED BY "\t";

 -- 加载数据到 emp 表中 这里直接从本地加载
load data local inpath "/usr/file/emp.txt" into table emp;
```

完成后 emp 表中数据如下：
![img](./images/2020-10-19-8pGyg3.jpg)

为清晰演示，先清空 emp_ptn 表中加载的数据：

```sql
TRUNCATE TABLE emp_ptn;
```

静态分区演示：从 emp 表中查询部门编号为 20 的员工数据，并插入 emp_ptn 表中，语句如下：

```sql
INSERT OVERWRITE TABLE emp_ptn PARTITION (deptno=20) 
SELECT empno,ename,job,mgr,hiredate,sal,comm FROM emp WHERE deptno=20;
```

完成后 emp_ptn 表中数据如下：
![img](./images/2020-10-19-jDW94w.jpg)

接着演示动态分区：

```sql
-- 由于我们只有一个分区，且还是动态分区，所以需要关闭严格默认。因为在严格模式下，用户必须至少指定一个静态分区
set hive.exec.dynamic.partition.mode=nonstrict;

-- 动态分区   此时查询语句的最后一列为动态分区列，即 deptno
INSERT OVERWRITE TABLE emp_ptn PARTITION (deptno) 
SELECT empno,ename,job,mgr,hiredate,sal,comm,deptno FROM emp WHERE deptno=30;
```

完成后 emp_ptn 表中数据如下：
![img](./images/2020-10-19-WZm24f.jpg)

### 6.2.3. 使用SQL语句插入值

```sql
INSERT INTO TABLE tablename [PARTITION (partcol1[=val1], partcol2[=val2] ...)] 
VALUES ( value [, value ...] )
```

* 使用时必须为表中的每个列都提供值。不支持只向部分列插入值（可以为缺省值的列提供空值来消除这个弊端）；
* 如果目标表表支持 ACID 及其事务管理器，则插入后自动提交；
* 不支持支持复杂类型 (array, map, struct, union) 的插入。

### 6.2.4. 更新和删除数据

#### 6.2.4.1 语法

更新和删除的语法比较简单，和关系型数据库一致。需要注意的是这两个操作都只能在支持 ACID 的表，也就是事务表上才能执行。

```sql
-- 更新
UPDATE tablename SET column = value [, column = value ...] [WHERE expression]

--删除
DELETE FROM tablename [WHERE expression]
```

#### 6.2.4.2 示例

1. 修改配置

首先需要更改 hive-site.xml，添加如下配置，开启事务支持，配置完成后需要重启 Hive 服务。

```md
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
    <name>hive.in.test</name>
    <value>true</value>
</property> 
```

2. 创建测试表

创建用于测试的事务表，建表时候指定属性 transactional = true
则代表该表是事务表。需要注意的是，按照[官方文档](https://cwiki.apache.org/confluence/display/Hive/Hive+Transactions)的说明，目前 Hive 中的事务表有以下限制：

- 必须是 buckets Table;
- 仅支持 ORC 文件格式；
- 不支持 LOAD DATA ...语句。

```sql
CREATE TABLE emp_ts(  
  empno int,  
  ename String
)
CLUSTERED BY (empno) INTO 2 BUCKETS STORED AS ORC
TBLPROPERTIES ("transactional"="true");
```

3. 插入测试数据

```sql
INSERT INTO TABLE emp_ts  VALUES (1,"ming"),(2,"hong");
```

插入数据依靠的是 MapReduce 作业，执行成功后数据如下：
![img](./images/2020-10-19-0zmFLR.jpg)

4. 测试更新和删除

```sql
--更新数据
UPDATE emp_ts SET ename = "lan"  WHERE  empno=1;

--删除数据
DELETE FROM emp_ts WHERE empno=2;
```

更新和删除数据依靠的也是 MapReduce 作业，执行成功后数据如下：
![img](./images/2020-10-19-nhPKez.jpg)

### 6.2.5. 查询结果写出到文件系统

#### 6.2.5.1 语法

```sql
INSERT OVERWRITE [LOCAL] DIRECTORY directory1
  [ROW FORMAT row_format] [STORED AS file_format] 
  SELECT ... FROM ...
```

* OVERWRITE 关键字表示输出文件存在时，先删除后再重新写入；
* 和 Load 语句一样，建议无论是本地路径还是 URL 地址都使用完整的；
* 写入文件系统的数据被序列化为文本，其中列默认由^A 分隔，行由换行符分隔。如果列不是基本类型，则将其序列化为 JSON 格式。其中行分隔符不允许自定义，但列分隔符可以自定义，如下：

```sql
-- 定义列分隔符为'\t' 
insert overwrite local directory './test-04' 
row format delimited 
FIELDS TERMINATED BY '\t'
COLLECTION ITEMS TERMINATED BY ','
MAP KEYS TERMINATED BY ':'
select * from src;
```

#### 6.2.5.2 示例

这里我们将上面创建的 `emp_ptn` 表导出到本地文件系统，语句如下：

```sql
INSERT OVERWRITE LOCAL DIRECTORY '/usr/file/ouput'
ROW FORMAT DELIMITED
FIELDS TERMINATED BY '\t'
SELECT * FROM emp_ptn;
```

导出结果如下：
![img](./images/2020-10-19-5SLPsK.jpg)

## 6.3 视图

### 6.3.1 简介

Hive中的视图和RDBMS中视图的概念一致，都是一组数据的逻辑表示，本质上就是一条select语句的结果集。视图是纯粹的逻辑对象，没有关联的存储(Hive3.0.0引入的物化视图除外)
，当查询引用视图时，Hive可以将视图的定义与查询结合起来，例如将查询中的过滤器推送到视图中。

**视图的特点：**

- 一种逻辑结构，通过隐藏虚拟表中的子查询，连接和函数来简化查询
- Hive视图不存储数据不能物化
- 创建试图后，立即冻结期架构
- 如果删除或更改基础表，则查询视图将失败
- 视图时只读的，不能用作LOAD/INSERT/ALTER的目标

### 6.3.2 创建视图

```sql
CREATE VIEW [IF NOT EXISTS] [db_name.]view_name   -- 视图名称
  [(column_name [COMMENT column_comment], ...) ]    --列名
  [COMMENT view_comment]  --视图注释
  [TBLPROPERTIES (property_name = property_value, ...)]  --额外信息
  AS SELECT ...;   
```

在 Hive 中可以使用 CREATE VIEW 创建视图，如果已存在具有相同名称的表或视图，则会抛出异常，建议使用 IF NOT EXISTS 预做判断。在使用视图时候需要注意以下事项： 视图是只读的，不能用作 LOAD / INSERT
/ ALTER 的目标； 在创建视图时候视图就已经固定，对基表的后续更改（如添加列）将不会反映在视图； 删除基表并不会删除视图，需要手动删除视图； 视图可能包含 ORDER BY 和 LIMIT
子句。如果引用视图的查询语句也包含这类子句，其执行优先级低于视图对应字句。例如，视图 custom_view 指定 LIMIT 5，查询语句为 select * from custom_view LIMIT 10，此时结果最多返回 5 行。
创建视图时，如果未提供列名，则将从 SELECT 语句中自动派生列名； 创建视图时，如果 SELECT 语句中包含其他表达式，例如 x + y，则列名称将以_C0，_C1 等形式生成；

```sql
CREATE VIEW  IF NOT EXISTS custom_view AS SELECT empno, empno+deptno , 1+2 FROM emp;
```

![img](./images/2020-10-19-vBiO95.jpg)

### 6.3.3 查看视图

```sql
-- 查看所有视图： 没有单独查看视图列表的语句，只能使用 show tables
show tables;
-- 查看某个视图
desc view_name;
-- 查看某个视图详细信息
desc formatted view_name;
```

### 6.3.4 删除视图

```sql
DROP VIEW [IF EXISTS] [db_name.]view_name;
```

### 6.3.5 修改视图

```sql
ALTER VIEW [db_name.]view_name AS select_statement;
```

被更改的视图必须存在，且视图不能具有分区，如果视图具有分区，则修改失败。

### 6.3.6 修改视图属性

语法：

```sql
ALTER VIEW [db_name.]view_name SET TBLPROPERTIES table_properties;

table_properties:
  : (property_name = property_value, property_name = property_value, ...)
```

示例：

```sql
ALTER VIEW custom_view SET TBLPROPERTIES ('create'='heibaiying','date'='2019-05-05');
```

![img](./images/2020-10-19-zy8DWl.jpg)

### 6.3.7 Hive侧视图

- 应用表生成功能，将功能输入和输出连接在一起

    - 在一个复杂的sql查询中，可以生成类似于临时的视图一样的功能。
    - 使用Lateral view 如果视图是空值的华，那么最终不会有任何输出结果。需要使用Lateral view out
- lateral view outer

    - 即使输出为空，lateral view outer也会生成结果
    - 视图为空值，也会展示全部结果
- explode函数的用法：

    - 参数：接受的是一个集合
    - 返回值：返回集合的每一个元素
- lateral view 和 explode的使用场景？

    - explode就是将hive一行中复杂的array或者map结构拆分成多行。
    - lateral view用于和[split](https://so.csdn.net/so/search?q=split&spm=1001.2101.3001.7020),
      explode等UDTF一起使用，它能够将一行数据拆成多行数据，在此基础上可以对拆分后的数据进行聚合。lateral view首先为原始表的每行调用UDTF，UDTF会把一行拆分成一或者多行，lateral
      view再把结果组合，产生一个支持别名表的虚拟表。
    - explode将复杂结构一行拆成多行，然后再用lateral view做各种聚合。

示例：

```sql
select * from tb_split; 
 
20141018  aa|bb  7|9|0|3 
20141019  cc|dd  6|1|8|5 
 
使用方式：select datenu,des,type from tb_split  
lateral view explode(split(des,"//|")) tb1 as des 
lateral view explode(split(type,"//|")) tb2 as type 
执行过程是先执行from到as cloumn的列过程，再执行select 和where后边的语句。
```

```sql
   SELECT
        *
    FROM
        ods_aimsen_base_regionhistories lateral VIEW explode(split(ManageBranchNos,'\\}\\{')) tmp
        AS sub
```

可以基于explode+lateral view 实现词频统计

```sql
1. explode基本的功能

select explode(work_place) from employee_external;

2. 查询客户之前工作过的所有地方

select name, explode(work_place) from employee_external;

-- 通过 lateral view 解决这个问题

select name, addr from employee_external lateral view explode(work_place) r1 as

addr;

-- lateral view 无法解决输出为null的问题

select name, addr from employee_external lateral view explode(split(null,',')) a

as addr;


-- lateval view outer 可以解决这个问题

select name, addr from employee_external lateral view outer

explode(split(null,',')) a as

addr;

-- support multiple level

SELECT * FROM table_name

LATERAL VIEW explode(col1) myTable1 AS myCol1

LATERAL VIEW explode(myCol1) myTable2 AS myCol2;

-- 案例

select * from work;

work.name work.location

zs beijing,wuhan

lisi shanghai,guangzhou,shenzhshen

select * from work lateal view explode(split(location,',')) a as loc;

work.name work.location work.loc

zs beijing,wuhan beijing

zs beijing,wuhan wuhan

lisi shanghai,guangzhou,shenzhshen shanghai

lisi shanghai,guangzhou,shenzhshen guangzhou

lisi shanghai,guangzhou,shenzhshen shenzhen

select * from work lateal view explode(split(null,',')) a as loc; --result null

select * from work lateal view outer explode(split(null,',')) a as loc;

work.name work.location work.loc

zs beijing,wuhan null

lisi shanghai,guangzhou,shenzhshen null

SELECT INPUT__FILE__NAME,BLOCK__OFFSET__INSIDE__FILE FROM employee_external;
```

## 6.6 索引

### 6.6.1 简介

Hive 在 0.7.0 引入了索引的功能，索引的设计目标是提高表某些列的查询速度。如果没有索引，带有谓词的查询（如'WHERE table1.column = 10'）会加载整个表或分区并处理所有行。但是如果 column
存在索引，则只需要加载和处理文件的一部分。

### 6.6.2 索引原理

在指定列上建立索引，会产生一张索引表（表结构如下），里面的字段包括：索引列的值、该值对应的 HDFS 文件路径、该值在文件中的偏移量。在查询涉及到索引字段时，首先到索引表查找索引列值对应的 HDFS 文件路径及偏移量，这样就避免了全表扫描。

```sql
+--------------+----------------+----------+--+
|   col_name   |   data_type    | comment     |
+--------------+----------------+----------+--+
| empno        | int            |  建立索引的列  |   
| _bucketname  | string         |  HDFS 文件路径  |
| _offsets     | array<bigint>  |  偏移量       |
+--------------+----------------+----------+--+
```

### 6.6.3 创建索引

```sql
CREATE INDEX index_name     --索引名称
  ON TABLE base_table_name (col_name, ...)  --建立索引的列
  AS index_type    --索引类型
  [WITH DEFERRED REBUILD]    --重建索引
  [IDXPROPERTIES (property_name=property_value, ...)]  --索引额外属性
  [IN TABLE index_table_name]    --索引表的名字
  [
     [ ROW FORMAT ...] STORED AS ...  
     | STORED BY ...
  ]   --索引表行分隔符 、 存储格式
  [LOCATION hdfs_path]  --索引表存储位置
  [TBLPROPERTIES (...)]   --索引表表属性
  [COMMENT "index comment"];  --索引注释
```

### 6.6.4 查看索引

```sql
--显示表上所有列的索引
SHOW FORMATTED INDEX ON table_name;
```

### 6.6.4 删除索引

删除索引会删除对应的索引表。

```sql
DROP INDEX [IF EXISTS] index_name ON table_name;
```

如果存在索引的表被删除了，其对应的索引和索引表都会被删除。如果被索引表的某个分区被删除了，那么分区对应的分区索引也会被删除。

### 6.6.5 重建索引

```sql
ALTER INDEX index_name ON table_name [PARTITION partition_spec] REBUILD;
```

重建索引。如果指定了 PARTITION，则仅重建该分区的索引。

## 6.7 索引案例

### 6.7.1 创建索引

在 emp 表上针对 empno 字段创建名为 emp_index,索引数据存储在 emp_index_table 索引表中

```sql
create index emp_index on table emp(empno) as  
'org.apache.hadoop.hive.ql.index.compact.CompactIndexHandler' 
with deferred rebuild 
in table emp_index_table ;
```

此时索引表中是没有数据的，需要重建索引才会有索引的数据。

### 6.7.2 重建索引

```sql
alter index emp_index on emp rebuild;
```

Hive 会启动 MapReduce 作业去建立索引，建立好后查看索引表数据如下。三个表字段分别代表：索引列的值、该值对应的 HDFS 文件路径、该值在文件中的偏移量。

![img](./images/2020-10-19-4dTaAL.jpg)

### 6.7.3 自动使用索引

默认情况下，虽然建立了索引，但是 Hive 在查询时候是不会自动去使用索引的，需要开启相关配置。开启配置后，涉及到索引列的查询就会使用索引功能去优化查询。

```sql
SET hive.input.format=org.apache.hadoop.hive.ql.io.HiveInputFormat;
SET hive.optimize.index.filter=true;
SET hive.optimize.index.filter.compact.minsize=0;
```

### 6.7.4 查看索引

```sql
SHOW INDEX ON emp;
```

![img](./images/2020-10-19-Xudwmn.jpg)

## 6.6 索引的缺陷

索引表最主要的一个缺陷在于：索引表无法自动 rebuild，这也就意味着如果表中有数据新增或删除，则必须手动rebuild，重新执行 MapReduce 作业，生成索引表数据。
同时按照[官方文档](https://cwiki.apache.org/confluence/display/Hive/LanguageManual+Indexing)的说明，Hive 会从 3.0 开始移除索引功能，主要基于以下两个原因：

- 具有自动重写的物化视图 (Materialized View) 可以产生与索引相似的效果（Hive 2.3.0 增加了对物化视图的支持，在 3.0 之后正式引入）。
- 使用列式存储文件格式（Parquet，ORC）进行存储时，这些格式支持选择性扫描，可以跳过不需要的文件或块。 ORC
  内置的索引功能可以参阅这篇文章：[Hive 性能优化之 ORC 索引–Row Group Index vs Bloom Filter Index](http://lxw1234.com/archives/2016/04/632.htm)

## 6.7 Hive数据查询

### 6.7.1 数据准备

为了演示查询操作，这里需要预先创建三张表，并加载测试数据。

> 数据文件 emp.txt 和 dept.txt 可以仓库[resources](https://github.com/heibaiying/BigData-Notes/tree/master/resources) 目录下载。

#### 6.7.1.1 员工表

```sql
 -- 建表语句
 CREATE TABLE emp(
     empno INT,     -- 员工表编号
     ename STRING,  -- 员工姓名
     job STRING,    -- 职位类型
     mgr INT,   
     hiredate TIMESTAMP,  --雇佣日期
     sal DECIMAL(7,2),  --工资
     comm DECIMAL(7,2),
     deptno INT)   --部门编号
    ROW FORMAT DELIMITED FIELDS TERMINATED BY "\t";

  --加载数据
LOAD DATA LOCAL INPATH "/usr/file/emp.txt" OVERWRITE INTO TABLE emp;
```

#### 6.7.1.2 部门表

```sql
 -- 建表语句
 CREATE TABLE dept(
     deptno INT,   --部门编号
     dname STRING,  --部门名称
     loc STRING    --部门所在的城市
 )
 ROW FORMAT DELIMITED FIELDS TERMINATED BY "\t";

 --加载数据
 LOAD DATA LOCAL INPATH "/usr/file/dept.txt" OVERWRITE INTO TABLE dept;
```

#### 6.7.1.3 分区表

这里需要额外创建一张分区表，主要是为了演示分区查询：

```sql
CREATE EXTERNAL TABLE emp_ptn(
      empno INT,
      ename STRING,
      job STRING,
      mgr INT,
      hiredate TIMESTAMP,
      sal DECIMAL(7,2),
      comm DECIMAL(7,2)
  )
 PARTITIONED BY (deptno INT)   -- 按照部门编号进行分区
 ROW FORMAT DELIMITED FIELDS TERMINATED BY "\t";


--加载数据
LOAD DATA LOCAL INPATH "/usr/file/emp.txt" OVERWRITE INTO TABLE emp_ptn PARTITION (deptno=20)
LOAD DATA LOCAL INPATH "/usr/file/emp.txt" OVERWRITE INTO TABLE emp_ptn PARTITION (deptno=30)
LOAD DATA LOCAL INPATH "/usr/file/emp.txt" OVERWRITE INTO TABLE emp_ptn PARTITION (deptno=40)
LOAD DATA LOCAL INPATH "/usr/file/emp.txt" OVERWRITE INTO TABLE emp_ptn PARTITION (deptno=50)
```

### 6.7.2 单表查询

#### 6.7.2.1 SELECT

```sql
-- 查询表中全部数据
SELECT * FROM emp;
```

#### 6.7.2.2 WHERE

```sql
-- 查询 10 号部门中员工编号大于 7782 的员工信息 
SELECT * FROM emp WHERE empno > 7782 AND deptno = 10;
```

#### 6.7.2.3  DISTINCT

Hive 支持使用 DISTINCT 关键字去重。

```sql
-- 查询所有工作类型
SELECT DISTINCT job FROM emp;
```

#### 6.7.2.4 分区查询

分区查询 (Partition Based Queries)，可以指定某个分区或者分区范围。

```sql
-- 查询分区表中部门编号在[20,40]之间的员工
SELECT emp_ptn.* FROM emp_ptn
WHERE emp_ptn.deptno >= 20 AND emp_ptn.deptno <= 40;
```

#### 6.7.2.5 LIMIT

```sql
-- 查询薪资最高的 5 名员工
SELECT * FROM emp ORDER BY sal DESC LIMIT 5;
```

#### 6.7.2.6 GROUP BY

Hive 支持使用 GROUP BY 进行分组聚合操作。

```sql
set hive.map.aggr=true;

-- 查询各个部门薪酬综合
SELECT deptno,SUM(sal) FROM emp GROUP BY deptno;
```

hive.map.aggr 控制程序如何进行聚合。默认值为 false。如果设置为 true，Hive 会在 map 阶段就执行一次聚合。这可以提高聚合效率，但需要消耗更多内存。

#### 6.7.2.7 ORDER AND SORT

可以使用 ORDER BY 或者 Sort BY 对查询结果进行排序，排序字段可以是整型也可以是字符串：如果是整型，则按照大小排序；如果是字符串，则按照字典序排序。ORDER BY 和 SORT BY 的区别如下：

* 使用 ORDER BY 时会有一个 Reducer 对全部查询结果进行排序，可以保证数据的全局有序性；
* 使用 SORT BY 时只会在每个 Reducer 中进行排序，这可以保证每个 Reducer 的输出数据是有序的，但不能保证全局有序。

由于 ORDER BY 的时间可能很长，如果你设置了严格模式 (hive.mapred.mode = strict)，则其后面必须再跟一个 `limit` 子句。

> 注 ：hive.mapred.mode 默认值是 nonstrict ，也就是非严格模式。

```sql
-- 查询员工工资，结果按照部门升序，按照工资降序排列
SELECT empno, deptno, sal FROM emp ORDER BY deptno ASC, sal DESC;
```

#### 6.7.2.8 HAVING

可以使用 HAVING 对分组数据进行过滤

```sql
-- 查询工资总和大于 9000 的所有部门
SELECT deptno,SUM(sal) FROM emp GROUP BY deptno HAVING SUM(sal)>9000;
```

#### 6.7.2.9 DISTRIBUTE BY

默认情况下，MapReduce 程序会对 Map 输出结果的 Key 值进行散列，并均匀分发到所有 Reducer 上。如果想要把具有相同 Key 值的数据分发到同一个 Reducer 进行处理，这就需要使用 DISTRIBUTE BY
字句。

需要注意的是，DISTRIBUTE BY 虽然能保证具有相同 Key 值的数据分发到同一个 Reducer，但是不能保证数据在 Reducer 上是有序的。情况如下：

把以下 5 个数据发送到两个 Reducer 上进行处理：

```sql
k1
k2
k4
k3
k1
```

Reducer1 得到如下乱序数据：

```sql
k1
k2
k1
```

Reducer2 得到数据如下：

```sql
k4
k3
```

如果想让 Reducer 上的数据时有序的，可以结合 `SORT BY` 使用 (示例如下)，或者使用下面我们将要介绍的 CLUSTER BY。

```sql
-- 将数据按照部门分发到对应的 Reducer 上处理
SELECT empno, deptno, sal FROM emp DISTRIBUTE BY deptno SORT BY deptno ASC;
```

#### 6.7.2.10 CLUSTER BY

如果 `SORT BY` 和 `DISTRIBUTE BY` 指定的是相同字段，且 SORT BY 排序规则是 ASC，此时可以使用 `CLUSTER BY` 进行替换，同时 `CLUSTER BY` 可以保证数据在全局是有序的。

```sql
SELECT empno, deptno, sal FROM emp CLUSTER  BY deptno ;
```

### 6.7.3 多表联结查询

Hive 支持内连接，外连接，左外连接，右外连接，笛卡尔连接，这和传统数据库中的概念是一致的，可以参见下图。

需要特别强调：JOIN 语句的关联条件必须用 ON 指定，不能用 WHERE 指定，否则就会先做笛卡尔积，再过滤，这会导致你得不到预期的结果 (下面的演示会有说明)。

![img](./images/2020-10-19-cLAjNs.jpg)

#### 6.7.3.1 INNER JOIN

```sql
-- 查询员工编号为 7369 的员工的详细信息
SELECT e.*,d.* FROM 
emp e JOIN dept d
ON e.deptno = d.deptno 
WHERE empno=7369;

--如果是三表或者更多表连接，语法如下
SELECT a.val, b.val, c.val FROM a JOIN b ON (a.key = b.key1) JOIN c ON (c.key = b.key1)
```

#### 6.7.3.2 LEFT OUTER  JOIN

LEFT OUTER JOIN 和 LEFT JOIN 是等价的。

```sql
-- 左连接
SELECT e.*,d.*
FROM emp e LEFT OUTER  JOIN  dept d
ON e.deptno = d.deptno;
```

#### 6.7.3.3 RIGHT OUTER  JOIN

1

**--右连接**

```sql
--右连接
SELECT e.*,d.*
FROM emp e RIGHT OUTER JOIN  dept d
ON e.deptno = d.deptno;
```

执行右连接后，由于 40 号部门下没有任何员工，所以此时员工信息为 NULL。这个查询可以很好的复述上面提到的——JOIN 语句的关联条件必须用 ON 指定，不能用 WHERE 指定。你可以把 ON 改成
WHERE，你会发现无论如何都查不出 40 号部门这条数据，因为笛卡尔运算不会有 (NULL, 40) 这种情况。

![](https://image.ldbmcs.com/2020-10-19-MjitHh.jpg)

2020-10-19-MjitHh

#### 6.7.3.4 FULL OUTER  JOIN

```sql
SELECT e.*,d.*
FROM emp e FULL OUTER JOIN  dept d
ON e.deptno = d.deptno;
```

#### 6.7.3.5 LEFT SEMI JOIN

LEFT SEMI JOIN （左半连接）是 IN/EXISTS 子查询的一种更高效的实现。

* JOIN 子句中右边的表只能在 ON 子句中设置过滤条件;
* 查询结果只包含左边表的数据，所以只能 SELECT 左表中的列。

```sql
-- 查询在纽约办公的所有员工信息
SELECT emp.*
FROM emp LEFT SEMI JOIN dept 
ON emp.deptno = dept.deptno AND dept.loc="NEW YORK";

--上面的语句就等价于
SELECT emp.* FROM emp
WHERE emp.deptno IN (SELECT deptno FROM dept WHERE loc="NEW YORK");
```

#### 6.7.3.6 JOIN

笛卡尔积连接，这个连接日常的开发中可能很少遇到，且性能消耗比较大，基于这个原因，如果在严格模式下 (hive.mapred.mode = strict)，Hive 会阻止用户执行此操作。

```sql
SELECT * FROM emp JOIN dept;
```

### 6.7.4 JOIN优化

#### 6.7.4.1 STREAMTABLE

在多表进行联结的时候，如果每个 ON 字句都使用到共同的列（如下面的 `b.key`），此时 Hive 会进行优化，将多表 JOIN 在同一个 map / reduce 作业上进行。同时假定查询的最后一个表（如下面的 c
表）是最大的一个表，在对每行记录进行 JOIN 操作时，它将尝试将其他的表缓存起来，然后扫描最后那个表进行计算。因此用户需要保证查询的表的大小从左到右是依次增加的。

```sql
`SELECT a.val, b.val, c.val FROM a JOIN b ON (a.key = b.key) JOIN c ON (c.key = b.key)`
```

然后，用户并非需要总是把最大的表放在查询语句的最后面，Hive 提供了 `/*+ STREAMTABLE() */` 标志，用于标识最大的表，示例如下：

```sql
SELECT /*+ STREAMTABLE(d) */  e.*,d.* 
FROM emp e JOIN dept d
ON e.deptno = d.deptno
WHERE job='CLERK';
```

#### 6.7.4.2 MAPJOIN

如果所有表中只有一张表是小表，那么 Hive 把这张小表加载到内存中。这时候程序会在 map 阶段直接拿另外一个表的数据和内存中表数据做匹配，由于在 map 就进行了 JOIN 操作，从而可以省略 reduce
过程，这样效率可以提升很多。Hive 中提供了 `/*+ MAPJOIN() */` 来标记小表，示例如下：

```sql
SELECT /*+ MAPJOIN(d) */ e.*,d.* 
FROM emp e JOIN dept d
ON e.deptno = d.deptno
WHERE job='CLERK';
```

### 6.7.5. SELECT的其他用途

查看当前数据库：

```sql
SELECT current_database()
```

### 6.7.6. 本地模式

在上面演示的语句中，大多数都会触发 MapReduce, 少部分不会触发，比如 `select * from emp limit 5` 就不会触发 MR，此时 Hive 只是简单的读取数据文件中的内容，然后格式化后进行输出。在需要执行
MapReduce 的查询中，你会发现执行时间可能会很长，这时候你可以选择开启本地模式。

```sql
--本地模式默认关闭，需要手动开启此功能
SET hive.exec.mode.local.auto=true;
```

启用后，Hive 将分析查询中每个 map-reduce 作业的大小，如果满足以下条件，则可以在本地运行它：

* 作业的总输入大小低于：hive.exec.mode.local.auto.inputbytes.max（默认为 128MB）；
* map-tasks 的总数小于：hive.exec.mode.local.auto.tasks.max（默认为 4）；
* 所需的 reduce 任务总数为 1 或 0。

因为我们测试的数据集很小，所以你再次去执行上面涉及 MR 操作的查询，你会发现速度会有显著的提升。

## 6.8 案例实战

git源码见:`code/chapter05`

百度网盘下载链接：`https://pan.baidu.com/s/1xD6d7N69lq_YujUDW19Zww` 提取码：`ba6w`

### 6.8.1 数据结构

1．视频表


| 字段        | 备注       | 详细描述               |
| ------------- | ------------ | ------------------------ |
| video id    | 视频唯一id | 11位字符串             |
| uploader    | 视频上传者 | 上传视频的用户名String |
| age         | 视频年龄   | 视频在平台上的整数天   |
| category    | 视频类别   | 上传视频指定的视频分类 |
| length      | 视频长度   | 整形数字标识的视频长度 |
| views       | 观看次数   | 视频被浏览的次数       |
| rate        | 视频评分   | 满分5分                |
| ratings     | 流量       | 视频的流量，整型数字   |
| conments    | 评论数     | 一个视频的整数评论数   |
| related ids | 相关视频id | 相关视频的id，最多20个 |

2．用户表


| 字段     | 备注         | 字段类型 |
| ---------- | -------------- | ---------- |
| uploader | 上传者用户名 | string   |
| videos   | 上传视频数   | int      |
| friends  | 朋友数量     | int      |

### 6.8.2 需求描述

统计硅谷影音视频网站的常规指标，各种TopN指标：
--统计视频观看数Top10
--统计视频类别热度Top10
--统计视频观看数Top20所属类别以及类别包含的Top20的视频个数
--统计视频观看数Top50所关联视频的所属类别Rank
--统计每个类别中的视频热度Top10
--统计每个类别中视频流量Top10
--统计上传视频最多的用户Top10以及他们上传的观看次数在前20视频
--统计每个类别视频观看数Top10

### 6.8.3 数据准备

#### 1. 创建表

创建表：gulivideo_ori，gulivideo_user_ori,
创建表：gulivideo_orc，gulivideo_user_orc

gulivideo_ori：

```
create table gulivideo_ori(
    videoId string, 
    uploader string, 
    age int, 
    category array<string>, 
    length int, 
    views int, 
    rate float, 
    ratings int, 
    comments int,
    relatedId array<string>)
row format delimited 
fields terminated by "\t"
collection items terminated by "&"
stored as textfile;
```

gulivideo_user_ori：

```
create table gulivideo_user_ori(
    uploader string,
    videos int,
    friends int)
row format delimited 
fields terminated by "\t" 
stored as textfile;
```

然后把原始数据插入到orc表中
gulivideo_orc：

```
create table gulivideo_orc(
    videoId string, 
    uploader string, 
    age int, 
    category array<string>, 
    length int, 
    views int, 
    rate float, 
    ratings int, 
    comments int,
    relatedId array<string>)
row format delimited fields terminated by "\t" 
collection items terminated by "&" 
stored as orc;
```

gulivideo_user_orc：

```
create table gulivideo_user_orc(
    uploader string,
    videos int,
    friends int)
row format delimited 
fields terminated by "\t" 
stored as orc;
```

#### 2. ETL原始数据

```text
# 文件路径执行
[root@hadoop5 hdp]# hadoop fs -put hive_stage hive_stage
# hadoop路径执行
[root@hadoop5 hadoop-2.7.7]#  hadoop jar share/hadoop/mapreduce/guli-video-1.0-SNAPSHOT.jar com.atguigu.mr.ETLDriver hive_stage/guiliVideo/video/2008/0222 hive_stage/guiliVideo/output/video/2008/0222
```

#### 3.导入ETL后的数据

gulivideo_ori：

```text
hive (default)> load data  inpath "hive_stage/guiliVideo/output/video/2008/0222/" into table gulivideo_ori;
```

gulivideo_user_ori：

```text
load data  inpath "hive_stage/guiliVideo/user/2008/0903/" into table gulivideo_user_ori;
```

向ORC表插入数据
gulivideo_orc：

```
insert into table gulivideo_orc select * from gulivideo_ori;
```

gulivideo_user_orc：

```
insert into table gulivideo_user_orc select * from gulivideo_user_ori;
```

### 6.8.4 业务分析

## 参考资料

1.[Hive列转行 (Lateral View + explode)详解](https://zhuanlan.zhihu.com/p/115913870)
