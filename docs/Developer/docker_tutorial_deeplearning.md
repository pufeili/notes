

# Docker入门简明手册

## 1 Docker安装

==Docker版本在18之后都兼容nvidia-docker==，因此不再需要安装nvidia-docker了，只用docker即可。

可以参考官方Docker Hub的帮助文档：[https://docs.docker.com/engine/install/ubuntu/](https://docs.docker.com/engine/install/ubuntu/)

### 1.1 Ubuntu下安装

安装前卸载旧的版本

```shell
$ sudo apt-get remove docker docker-engine docker.io containerd runc
```

只需要这一行命令即可！

```bash
$ sudo curl -sS https://get.docker.com/ | sh
```

安装完毕后，验证是否安装成功

```bash
$ docker --version	# 查看docker版本
$ docker info	
$ docker 命令 --help	# 帮助命令
$ docker run hello-world	# 测试demo
$ docker run -it ubuntu bash	# 测试demo2
```

***如果机器有支持深度学习的Gpu，可以继续执行如下命令以支持容器对gpu 的调用**

**[目前仅支持linux]：**

```bash
# Add the package repositories
	distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
	curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | sudo apt-key add -
	curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | sudo tee /etc/apt/sources.list.d/nvidia-docker.list
	sudo apt-get update && sudo apt-get install -y nvidia-container-toolkit
	sudo systemctl restart docker
```

天池视频教程：[https://tianchi.aliyun.com/course/351/4127](https://tianchi.aliyun.com/course/351/4127)

配置镜像加速器：**阿里控制台 ->容器镜像服务 -> 镜像加速器**

### 1.2 Windows

### 1.3 macOs

## 2 Docker基础命令使用

官方命令帮助文档地址：[https://docs.docker.com/engine/reference/run/](https://docs.docker.com/engine/reference/run/)

### 2.1 拉取镜像

```bash
$ docker pull [选项] [docker 镜像地址:标签]
```

例如：

```bash
$ docker pull hello-world:latest
```

### 2.2 运行镜像

```shell
	$ docker run hello-world:latest
Hello from Docker!
This message shows that your installation appears to be working correctly.
To generate this message, Docker took the following steps:
1. The Docker client contacted the Docker daemon.
2. The Docker daemon pulled the "hello-world" image from the Docker Hub.(amd64)
3. The Docker daemon created a new container from that image which runs theexecutable that produces the output you are currently reading.
4. The Docker daemon streamed that output to the Docker client, which sent itto your terminal.
To try something more ambitious, you can run an Ubuntu container with:
	$ docker run -it ubuntu bash
Share images, automate workflows, and more with a free Docker ID: https://hub.docker.com/
For more examples and ideas, visit: https://docs.docker.com/get-started/
```

### 2.3 运行镜像并进入容器

```bash
	$ docker run -it --rm ubuntu:18.04 bash
	root@e7009c6ce357:/# uname -a
	Linux bff9f261bab2 4.15.0-106-generic #107-Ubuntu SMP Thu Jun 4 11:27:52 UTC 2020 x86_64 x86_64 x86_64 GNU/Linux
	root@e7009c6ce357:/# exit
```

==docker run== 就是运行容器的命令,后面如果只跟镜像，那么就执行镜像的默认命令然后退出。

- ==-it==：这是两个参数，一个是==-i== 交互式操作，一个是==-t== 终端。我们这里打算进入==bash== 执行一些命令并查看返回结果，因此我们需要交互式终端。(==bash 和 /bin/bash区别==)
- ==--rm==：这个参数是说容器退出后随之将其删除。默认情况下，为了排障需求，退出的容器并不会立即删除，除非手动==docker rm==。我们这里只是随便执行个命令，看看结果，不需要排障和保留结果，因此使用==--rm== 可以避免浪费空间。
- ==ubuntu:18.04==：这是指用==ubuntu:18.04== 镜像为基础来启动容器。
- ==bash==：放在镜像名后的是命令，这里我们希望有个交互式==Shell==，因此用的是==bash==。

进入容器后，我们可以在==Shell== 下操作，执行任何所需的命令。通过==exit== 退出。

### 2.4 查看本地镜像（list 镜像）

```shell
$ docker images
REPOSITORY	TAG		IMAGE ID		CREATED		SIZE
redis		latest	5f515359c7f8	5 days ago	183 MB
nginx		latest	05a60462f8ba	5 days ago	181 MB

# 解释
REPOSITORY	镜像的仓库源
TAG			镜像的标签
IMAGE ID	镜像的ID
CREATED		镜像的创建时间
SIZE		镜像的大小

# 可选项
Options:
  -a, --all             Show all images (default hides intermediate images)
  -q, --quiet           Only show image IDs
```

**IMAGE ID 是镜像的唯一标识。**

### 2.5 查看运行中的容器

```shell
$ docker ps
CONTAINER ID	IMAGE		COMMAND		CREATED		STATUS		PORTS		NAMES
9363b1b51118	testlog:1	"bash"		7 weeks ago	Up 			7 weeks 	vigilant_bhaskara
```

==CONTAINER ID== 容器唯一id 可以通过指定这个ID 操作exec shell 进入容器、commit 这个容器的修改、tag 给这个容器打标签等。

- ==docker ps== 罗列的是当前活跃的容器。

- 要查看所有容器执行==docker ps -a==：

  ```shell
  $ docker ps -a
  ```

### 2.6 进入运行中/后台运行的容器
  ```shell
  $ docker exec -it [CONTAINER ID] /bin/bash
  ```

进入运行中的容器后不仅可以调试镜像，还可以对镜像做修改如安装python 包，如果想对修改做保留，可以执行2.7 提交。

### 2.7 保存修改

```shell
$ docker commit [CONTAINER ID] registry.cn-shanghai.aliyuncs.com/test/pytorch:myversion
```

> 注意：通过commint 的形式保存现场为一个新的镜像虽然也能直观的达到构建新镜像的目的，==**但是实际操作中，并不推荐这种形式**==，因为 
>
> 1.commit 操作不仅会把有用的修改保存下来，对一些无关的修改也会保存下来（每一个命令行操作都会生成存储如ls 操作）就会导致镜像比较臃肿；
>
> 2.因为commit 操作属于黑箱操作，后续如果有什么问题维护起来会比较麻烦。

建议commit 仅作为保留现场的手段，然后通过修改dockerfile 构建镜像。

### 2.8 打TAG

有时需要对临时版本，或者节点版本做一个标记保留，打TAG 标签非常好用，并不会额外占用空间：

```shell
$ docker tag registry.cn-shanghai.aliyuncs.com/test/pytorch:myversion my_tmp_version:0.1
```

### 2.9 推送镜像到仓库

```bash
$ docker push registry.cn-shanghai.aliyuncs.com/test/pytorch:myversion
```

### 2.10 使用dockerfile 构建镜像

**Dockerfile 示例(注意一般文件名命名为Dockerfile 无后缀名，如果命名为其他名字，构建时需要额外指定文件 名)：**

```shell
	# Base Images
	## 从天池基础镜像构建(from 的base img 根据自己的需要更换，建议使用天池open list 镜像链接：https://tianchi.aliyun.com/forum/postDetail?postId=67720)
	FROM registry.cn-shanghai.aliyuncs.com/tcc-public/python:3
	##安装依赖包
	RUN pip install numpy -i https://pypi.tuna.tsinghua.edu.cn/simple
	##或者从requirements.txt 安装
	##RUN pip install --no-cache-dir -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
	## 把当前文件夹里的文件构建到镜像的根目录下,并设置为默认工作目录
	ADD . /
	WORKDIR /
	## 镜像启动后统一执行sh run.sh
	CMD ["sh", "run.sh"]
```

### 2.11 构建镜像

```shell
$ docker build -t registry.cn-shanghai.aliyuncs.com/target:test .
```

末尾有一个 ==.== , 表示全选当前目录。

如要指定dockerfile：

```shell
$ docker build -f ./dockerfile -t
$ registry.cn-shanghai.aliyuncs.com/target:test .
```

### 2.12 删除镜像/容器

- 删除镜像：

  ```shell
  $ docker rmi registry.cn-shanghai.aliyuncs.com/target:test
  ```

- 删除容器：

  ```shell
  $ docker rm [CONTAINER ID]
  ```

- 如果容器还在运行，则会删除失败，应先结束掉容器：

  ```shell
  $ docker kill [CONTAINER ID]
  ```

- 查看运行中的容器：

  ```shell
  $ docker ps
  ```
  
- 查看所有容器：
  ```shell
  $ docker ps -a
  ```


### 2.13 常规技巧

- 检查基础镜像软件源和pip 源是否替换为国内源，如果非国内源后续每次构建镜像会比较浪费时间。
- 必备软件包可直接安装于基础镜像内，以减少每次构建镜像时都要安装一遍的等待时间。
- 镜像面临调试问题时，可交互式进入容器后直接调试修改，直到成功后退出再在dockerfile 中修改。
- 养成使用Dockerfile 的习惯，不要依赖于commit。
- 每次镜像修改都给定新的版本号或标签，方便区分版本管理，有意义的版本最好使用有含义的字符作为版本号，如：frist_submit。

**深度学习常用镜像集合（包含国内源和海外源）**

[https://tianchi.aliyun.com/forum/postDetail?postId=67720](https://tianchi.aliyun.com/forum/postDetail?postId=67720)



# 常用命令

## 镜像命令

**docker images** 查看本地主机上所有镜像

```shell
$ docker images
REPOSITORY	TAG		IMAGE ID		CREATED		SIZE
redis		latest	5f515359c7f8	5 days ago	183 MB
nginx		latest	05a60462f8ba	5 days ago	181 MB

# 解释
REPOSITORY	镜像的仓库源
TAG			镜像的标签
IMAGE ID	镜像的ID
CREATED		镜像的创建时间
SIZE		镜像的大小

# 可选项
Options:
  -a, --all             Show all images (default hides intermediate images)
  -q, --quiet           Only show image IDs
# 常用
$ docker images -aq
```

**docker search 搜索镜像**

```shell
root@iZbp13f2qdxw8ego5t0sd8Z:~# docker search mysql
NAME                             DESCRIPTION                                     STARS     OFFICIAL   AUTOMATED
mysql                            MySQL is a widely used, open-source relation…   12320     [OK]
mariadb                          MariaDB Server is a high performing open sou…   4737      [OK]
mysql/mysql-server               Optimized MySQL Server Docker images. Create…   915                  [OK]
percona                          Percona Server is a fork of the MySQL relati…   572       [OK]
phpmyadmin                       phpMyAdmin - A web interface for MySQL and M…   486       [OK]

# 可选项，通过收藏来过滤
root@iZbp13f2qdxw8ego5t0sd8Z:~# docker search mysql --filter=STARS=3000
NAME      DESCRIPTION                                     STARS     OFFICIAL   AUTOMATED
mysql     MySQL is a widely used, open-source relation…   12320     [OK]
mariadb   MariaDB Server is a high performing open sou…   4737      [OK]

```

**docker pull 拉取镜像**

```shell
# 下载镜像 docker pull 镜像名[:tag]
root@iZbp13f2qdxw8ego5t0sd8Z:~# docker pull mysql
Using default tag: latest	# 如果不写tag，默认就是latest
latest: Pulling from library/mysql
72a69066d2fe: Pull complete	# 分层下载,联合文件下载
93619dbc5b36: Pull complete
99da31dd6142: Pull complete
626033c43d70: Pull complete
37d5d7efb64e: Pull complete
ac563158d721: Pull complete
d2ba16033dad: Pull complete
688ba7d5c01a: Pull complete
00e060b6d11d: Pull complete
1c04857f594f: Pull complete
4d7cfa90e6ea: Pull complete
e0431212d27d: Pull complete
Digest: sha256:e9027fe4d91c0153429607251656806cc784e914937271037f7738bd5b8e7709	# 签名
Status: Downloaded newer image for mysql:latest
docker.io/library/mysql:latest	# 真实地址

# 两个等价
docker pull mysql
docker pull mysql:latest
```

**docker rmi 删除镜像**

```shell
root@iZbp13f2qdxw8ego5t0sd8Z:~# docker rmi -f 容器id		# 删除指定容器
root@iZbp13f2qdxw8ego5t0sd8Z:~# docker rmi -f 容器id	容器id	容器id	# 删除指定容器
root@iZbp13f2qdxw8ego5t0sd8Z:~# docker rmi -f $(docker images -aq)		# 删除所有容器
```



## 容器命令

下载了镜像后才可以创建容器，利用centos镜像进行测试学习

```shell
$ docker pull centos
```

- **新建容器并启动**

```shell
$ docker run [OPTIONS] IMAGE

# 常用参数说明
-d, --detach		# Run container in background and print container ID
-i, --interactive	# Keep STDIN open even if not attached
--name="Name"		# Assign a name to the container,给容器命名，区分容器
-p					# Publish a container's port(s) to the host 指定容器端口 -小p
	-p ip:主机端口：容器端口
	-p 主机端口：容器端口  （常用）
	-p 容器端口
	容器端口
-P					# Publish all exposed ports to random ports 随机指定端口  小P
-it 				# 使用交互方式运行，进入容器查看内容
-t					# Allocate a pseudo-TTY

# Example
# 启动并进入容器
root@iZbp13f2qdxw8ego5t0sd8Z:~# docker run -it ubuntu:18.04 /bin/bash
root@ec549defcd4a:/# ls		# 查看容器内的ubuntu
bin  boot  dev  etc  home  lib  lib64  media  mnt  opt  proc  root  run  sbin  srv  sys  tmp  usr  var
```

- 列出所有的运行的容器

```shell
$  docker ps [OPTIONS]
# docker ps 命令
-a	# 列出当前正在运行的容器+带出历史运行过的容器
-n=?	# 显示最近创建的前n个容器
-q		# 只显示容器编号
```

- 退出容器

```shell
exit 	# 容器停止退出
ctrl+p q	# 容器不停止退出
```

- 删除容器

```shell
$ docker rm 容器id				# 删除指定容器，不能删除正在运行的容器，强制删除 rm -f
$ docker rm -f $(docker ps -aq)	 # 删除所有容器
$ docker ps -a -q|xargs docker rm # 删除所有容器
```

- 启动和停止容器的操作

```shell
$ docker start 容器id		# 启动容器
$ docker restart 容器id		# 重启容器
$ docker stop 容器id		# 停止当前正在运行的容器
$ docker kill 容器id		# 强制停止当前容器
```



## 常用其它命令







## 具名挂载和匿名挂载

```shell
# 匿名挂载
-v 容器内路径(没有宿主机路径)
$  docker run -d -P --name ngix01 -v /etc/nginx nginx

# 查看所有卷的情况
root@iZbp13f2qdxw8ego5t0sd8Z:~# docker volume ls
DRIVER    VOLUME NAME
local     151625a73903fe6157efa26b63491fe1c4b443d26f5cf3fb11422d1d35bec96f

# 这里发现，这种就是匿名挂载， 我们在-v只写了容器内的路径，没有容器外的路径

# 具名挂载
# 这里注意 juming-nginx:/etc/nginx 和 /juming-nginx:/etc/nginx 之间的区别
root@iZbp13f2qdxw8ego5t0sd8Z:~# docker run -d -P --name nginx02 -v juming-nginx:/etc/nginx nginx
0b918d9aaa7fe03e22168f4e2e5e9ee5eeb14d79346b94dd967175175db9c36a
root@iZbp13f2qdxw8ego5t0sd8Z:~# docker volume ls
DRIVER    VOLUME NAME
local     151625a73903fe6157efa26b63491fe1c4b443d26f5cf3fb11422d1d35bec96f
local     juming-nginx

# 通过 -v 卷名：容器内路径
# 查看一下这个卷
root@iZbp13f2qdxw8ego5t0sd8Z:~# docker volume inspect juming-nginx
[
    {
        "CreatedAt": "2022-03-29T20:11:03+08:00",
        "Driver": "local",
        "Labels": null,
        "Mountpoint": "/var/lib/docker/volumes/juming-nginx/_data",
        "Name": "juming-nginx",
        "Options": null,
        "Scope": "local"
    }
]
```

所有的docker容器内的卷，没有指定目录的情况下都是在`/var/lib/docker/volumes/xxxxxx/_data ` 下

我们通过具名挂载可以方便的找到我们的卷，大多数情况下使用`具名挂载` 

```shell
# 如何确定是具名挂载还是匿名挂载，还是指定路径挂载！
-v	容器内路径	# 匿名挂载
-v	卷名：容器内路径	# 具名挂载
-v	/宿主机路径：：容器内路径	# 指定路径挂载
```

拓展：

```shell
# 通过 -v 容器内路径：ro rw 改变读写权限
ro		readonly	# 只读
rw		readwrite	# 可读可写

# 一旦使用这个设置了容器的权限，容器对我们挂载出来的内容就有限定了
$ docker run -d -P --name nginx02 -v juming-nginx:/etc/nginx:ro nginx
$ docker run -d -P --name nginx02 -v juming-nginx:/etc/nginx:rw nginx

# ro 只要看到ro就说明 该路径只能通过宿主机操作，容器内无法操作！
```



## 初识Dockerfile



```shell
# 创建Dockerfile文件，名字可以随机取，但是建议使用Dockerfile
# 文件中的内容是 指令（大写）+ 参数

FROM centos
# 这里只是指定了容器内的目录，没有指定容器外的目录，因此是一个匿名挂载
VOLUME ["volume01", "volume02"] 

CMD echo "----end----"

CMD /bin/bash

# 这里每个命令就是一层
```



```shell
root@iZbp13f2qdxw8ego5t0sd8Z:/home/docker-test-volume# docker build -f Dockerfile -t lpf/centos:1.0 .
Sending build context to Docker daemon  2.048kB
Step 1/4 : FROM centos
 ---> 5d0da3dc9764
Step 2/4 : VOLUME ["volume01", "volume02"]
 ---> Running in 8670a9867291
Removing intermediate container 8670a9867291
 ---> d74c76295ceb
Step 3/4 : CMD echo "----end----"
 ---> Running in 501c9951eae3
Removing intermediate container 501c9951eae3
 ---> 63ed92ccbb59
Step 4/4 : CMD /bin/bash
 ---> Running in e2adf1668180
Removing intermediate container e2adf1668180
 ---> da1be65c16b2
Successfully built da1be65c16b2
Successfully tagged lpf/centos:1.0
root@iZbp13f2qdxw8ego5t0sd8Z:/home/docker-test-volume# docker images
REPOSITORY      TAG                  IMAGE ID       CREATED          SIZE
lpf/centos      1.0                  da1be65c16b2   53 seconds ago   231MB
```



![image-20220329205705445](C:\Users\lipufei\AppData\Roaming\Typora\typora-user-images\image-20220329205705445.png)

这个卷的目录一定和外部有一个同步的目录！此时我们新建一个容器内文件(在容器内)

```shell
[root@b73b7796b33b /]# cd volume01
[root@b73b7796b33b volume01]# touch container.txt
[root@b73b7796b33b volume01]# ls
container.txt
[root@b73b7796b33b volume01]#
```



![image-20220329205958003](C:\Users\lipufei\AppData\Roaming\Typora\typora-user-images\image-20220329205958003.png)

查看一下卷挂载的路径 `$ docker inspect b73b7796b33b` ==在宿主机操作==

![image-20220329210558061](C:\Users\lipufei\AppData\Roaming\Typora\typora-user-images\image-20220329210558061.png)

测试刚才新建的文件是否同步出去了!

```shell
root@iZbp13f2qdxw8ego5t0sd8Z:~# cd /var/lib/docker/volumes/1b226e924f1c89235092cf5152cfe7c713c486afe7700a1c67396bc3dc46e4dc/_data
root@iZbp13f2qdxw8ego5t0sd8Z:/var/lib/docker/volumes/1b226e924f1c89235092cf5152cfe7c713c486afe7700a1c67396bc3dc46e4dc/_data# ls
container.txt
```

这种方式未来使用较多，因为我们通常会自己构建镜像！

假设构建镜像的时候没有自动进行挂载， 要手动通过命令参数对镜像进行挂载！ -v 卷名：容器内路径！



## 数据卷容器













# DockerFile

## DockerFile介绍

dockerfile是用来构建docker镜像的文件！相当于一个命令参数脚本！

构建步骤：

1、编写一个dockerfile文件

2、docker build构建成为一个镜像

3、docker run 运行镜像

4、docker push 发布镜像 (DockerHub、阿里云镜像仓库)



## DockerFile构建过程

**基础知识：**

1、每个保留关键字（指令）都必须是大写字母

2、文件内的命令从上到下顺序执行

3、# 表示注释

4、每一个指令都会创建提交一个新的镜像层，并提交！



![image-20220329213727877](C:\Users\lipufei\AppData\Roaming\Typora\typora-user-images\image-20220329213727877.png)



dockerfile是面向开发的，我们以后要发布项目，做镜像，就需要编写dockerfile文件，这个文件十分简单!

Docker镜像逐渐成为企业交付的标准，必须要掌握!

> 步骤：
>
> DockerFile：构建文件，定义了一切的步骤，源代码
>
> Dockerlmages ：通过DockerFile构建生成的镜像，最终发布和运行的产品!
>
> Docker容器：容器就是镜像运行起来提供服务器（相当于一个类的实例对象）
>
> **其中，后面两者是使用其他人的，第一个是自己编写建立的**



## DockerFile的指令

DockerFile的官方帮助手册：https://docs.docker.com/engine/reference/builder/#usage

```shell
FROM				# 基础镜像，一切从这里开始	centos 
MAINTAINER			# 镜像是谁写的，姓名+邮箱
RUN					# 镜像构建的时候需要运行的命令
ADD					# 添加内容，例如 往centos中添加tomcat、jdk等等
WORKDIR				# 镜像的工作目录
VOLUME				# 挂载的目录
EXPOSE				# 暴露端口配置
CMD					# 指定这个容器启动的时候要运行的命令，只有最后一个会生效，可被替代
ENTRYPOINT			# 指定这个容器启动的时候要运行的命令，是追加命令
ONBUILD				# 当构建一个被继承 DockFile 这个时候就会运行 ONBUILD 的指令。触发指令。
COPY				# 类似ADD，将我们的文件拷贝到镜像中
ENV					# 构建的时候设置环境变量
```



![image-20220329212815752](C:\Users\lipufei\AppData\Roaming\Typora\typora-user-images\image-20220329212815752.png)



## 实战测试（构建一个自己的Centos）

DockerHub中99%镜像都是从这个基础镜像过来的 `FROM scratch`，然后配置需要的软件和配置来进行构建

![image-20220329221119679](C:\Users\lipufei\AppData\Roaming\Typora\typora-user-images\image-20220329221119679.png)

> 创建一个自己的Centos镜像

```shell
# 1 编写
root@iZbp13f2qdxw8ego5t0sd8Z:/home/dockerfile# vim mydockerfile
root@iZbp13f2qdxw8ego5t0sd8Z:/home/dockerfile# cat mydockerfile
FROM centos
MAINTAINER lipufei<lipufei@qq.com>

ENV MYPATH /usr/local
WORKDIR $MYPATH

RUN apt install vim
RUN apt install net-tools

EXPOSE 80

CMD echo $MYPATH
CMD echo "----end-----"
CMD /bin/bash
```







Docker网络





