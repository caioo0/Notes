###  Docker网络

将docker网络之前，先将本地所有镜像和容器删除，**如果在工作环境中，此操作慎重**

```
docker rm -f $(docker ps -aq) # 删除本第所有容器
docker rmi -f $(docker images -qa) # 删除所有镜像
```



## 安装msyql8.0

```
sudo docker pull mysql:8.0
sudo docker images
```

```
sudo docker run -p 3308:3306 --name mysql \
-v /usr/local/docker/mysql/mysql-files:/var/lib/mysql-files \
-v /usr/local/docker/mysql/conf:/etc/mysql \
-v /usr/local/docker/mysql/logs:/var/log/mysql \
-v /usr/local/docker/mysql/data:/var/lib/mysql \
-e MYSQL_ROOT_PASSWORD=root \
-d mysql:8.0

```



```
docker stop mysql
docker start mysql
sudo docker exec -it mysql bash
mysql -uroot -proot
docker update mysql --restart=always
docker restart mysql
whereis mysql
sudo systemctl stop firewalld.service
sudo systemctl restart docker
docker start mysql

```

