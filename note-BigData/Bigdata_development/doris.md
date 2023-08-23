```powershell
$ wget https://dist.apache.org/repos/dist/dev/incubator/doris/0.15/0.15.0-rc04/apache-doris-0.15.0-incubating-src.tar.gz

$ mkdir /opt/software  # (根目录下)

$ tar -zxvf apache-doris-0.15.0-incubating-src.tar.gz -C /opt/software

$ docker pull apache/incubator-doris:build-env-for-0.15.0

$ docker images

$ docker run -it -v /opt/software/.m2:/root/.m2 -v /opt/software/apache-doris-0.15.0-incubating-src/:/root/apachedoris-0.15.0-incubating-src/  apache/incubator-doris:build-env-for-0.15.0
```

 

### 资料

1. https://doris.apache.org/zh-CN/docs/dev/install/standard-deployment