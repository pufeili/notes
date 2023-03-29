# frp反向代理

## 1 参考连接

[概览 | frp (gofrp.org)](https://gofrp.org/docs/overview/#为什么使用-frp)

[使用frp进行内网穿透连接远程服务器 - Circle_Wang - 博客园 (cnblogs.com)](https://www.cnblogs.com/CircleWang/p/15392679.html#:~:text=如果想关闭frp进程，可以使用kill,%2Bpid的方式)

[【保姆级教程】个人深度学习工作站配置指南 - 知乎 (zhihu.com)](https://zhuanlan.zhihu.com/p/336429888)

[frp后台运行和停止 - 简书 (jianshu.com)](https://www.jianshu.com/p/43f69a534413)

下载适合自己版本的 [最新的配置文件](https://github.com/fatedier/frp/releases)，分别上传到服务端和客户端。

```bash
# 解压文件
tar -zxvf frp_x.xx.x_linux_amd64.tar.gz
# 移动放在/usr/local/bin 目录下
sudo mv -r frp_x.xx.x_linux_amd64/ /usr/local/bin/frp
```

## 2 服务端配置

配置之前要在云服务器端开放相应的端口，如 `7000`，`7500` 等等。

切换到目录并编辑 `frps.ini` 文件:

```bash
cd /usr/local/bin/frp/
sudo vim frps.ini
```

这里使用了最简化的配置，设置了 frp 服务器用户接收客户端连接的端口：

> **注：frps.ini文件是不可以用#作为注释的，因此文件中一定要把#注释删掉，不然无法打开dashboard** 

```bash
[common]
bind_port = 7000            # 被连接服务器A（客户端）和中介服务器C（服务端）连接的端口
dashboard_port = 7500       # 中介服务器C（服务端）仪表盘端口
token = 123456            # 被连接服务器A（客户端）和中介服务器C（服务端）连接时的口令
dashboard_user = admin      # 仪表盘用户名
dashboard_pwd = admin       # 仪表盘密码
```

启动 `frps` 服务端：

```bash
./frps -c ./frps.ini
```

以上就完成了服务端的frp配置。

在浏览器输入 `[云服务器的公网ip]:7500` 即可访问到 frp的web管理界面。

可以在终端查看端口占用情况：

```shell
netstat -ntlp
```

这里要注意到我们不能关闭服务端的frp进程，因此我们也可以使用以下命令行在启动frp程序的时候使其后台启动。

```shell
# 后台启动
nohup ./frps -c frps.ini &
# 如果想关闭frp进程，可以使用kill +pid的方式
# 找到进程号
ps -aux|grep frp| grep -v grep
# 查看相关(程序名)进程状态
ps -ef|grep [程序名]　　
# 杀死进程
kill -9 PID
```



## 3 客户端配置

切换到目录并编辑 `frpc.ini` 文件：

> **注意，这里编辑的是 `frpc.ini` 文件**

```bash
cd /usr/local/bin/frp/
sudo vim frpc.ini
```

配置内容：

```bash
[common]
server_addr = xxxx.xxx.xxx.xxx  # 中介服务器C的公网IP
authentication_method = token
server_port = 7000　　　　　　　　 # 被连接服务器A（客户端）与中介服务器C（服务端）连接的端口
token = 123456　　　　　　　　　　# 被连接服务器A（客户端）与中介服务器C（服务端）连接时的口令

[ssh]
type = tcp
local_ip = 127.0.0.1
local_port = 22
remote_port = 20022
```

> **注意：remote_port这个设置，这个端口号指的是服务端会监听remote_port这个端口，如果有其他外部电脑连接中介服务端的这个端口，那么就等价于连接客户端的local_port端口。**

完成上面配置之后，在客户端上启动frp程序。(注意是启动frpc.ini)

```shell
./frpc -c frpc.ini
```

到此为止，服务端和客户端的基本配置结束，可以在自己的电脑进行测试：

```bash
# ssh -p 远程端口 用户名@ip地址
ssh -p remotport name@xxx.xxx.xxx.xxx
```

> 这里 remoteport 和客户端配置文件中一致；
> username 是客户端的用户名；
> ip地址是服务端的ip；
> 连接上ssh后要求登录密码，也是客户端的密码；

## 4 使用 systemd 控制 frp 及配置开机自启

[使用 systemd | frp (gofrp.org)](https://gofrp.org/docs/setup/systemd/)

### 4.1 服务端

在终端输入，创建并编辑 `frps.service` 文件：

```shell
sudo vim /etc/systemd/system/frps.service
```

```bash
[Unit]
# 服务名称，可自定义
Description=Frp Server Daemon
After=syslog.target network.target
Wants=network.target

[Service]
Type=simple
# 启动frps的命令，需修改为您的frps的安装路径
ExecStart=/usr/local/bin/frp/frps -c /usr/local/bin/frp/frps.ini # 修改为你的frp实际安装目录
ExecStop=/usr/bin/killall frps
#启动失败1分钟后再次启动
RestartSec=1min
KillMode=control-group
#重启控制：总是重启
Restart=always

[Install]
WantedBy=multi-user.target
```

使用 `systemd` 命令，管理 frps。

```shell
# 启动frp
sudo systemctl start frps
# 停止frp
sudo systemctl stop frps
# 重启frp
sudo systemctl restart frps
# 查看frp状态
sudo systemctl status frps
```

配置 frps 开机自启。

```bash
sudo systemctl enable frps
```



### 4.2 客户端

在终端输入，创建并编辑 `frpc.service` 文件：

```shell
sudo vim /etc/systemd/system/frpc.service
```

```bash
[Unit]
# 服务名称，可自定义
Description=Frp Server Daemon
After=syslog.target network.target
Wants=network.target

[Service]
Type=simple
# 启动frpc的命令，需修改为您的frpc的安装路径
ExecStart=/usr/local/bin/frp/frpc -c /usr/local/bin/frp/frpc.ini # 修改为你的frp实际安装目录
ExecStop=/usr/bin/killall frpc
#启动失败1分钟后再次启动
RestartSec=1min
KillMode=control-group
#重启控制：总是重启
Restart=always

[Install]
WantedBy=multi-user.target
```

使用 `systemd` 命令，管理 frpc。

```shell
# 启动frp
sudo systemctl start frpc
# 停止frp
sudo systemctl stop frpc
# 重启frp
sudo systemctl restart frpc
# 查看frp状态
sudo systemctl status frpc
```

配置 `frpc` 开机自启。

```bash
sudo systemctl enable frpc
```