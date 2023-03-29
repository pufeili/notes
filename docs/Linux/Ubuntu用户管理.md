## 1. 准备知识

参考链接：[链接1](https://cloud.tencent.com/developer/article/1611042#:~:text=adduser%E5%92%8Cuseradd%E7%9A%84%E5%8C%BA%E5%88%AB%201%20%E9%A6%96%E5%85%88%E5%8F%AF%E4%BB%A5%E7%A1%AE%E5%AE%9A%E7%9A%84%E4%B8%80%E7%82%B9%E6%98%AF%EF%BC%8Cadduser%E5%92%8Cuseradd%E5%9C%A8Ubuntu%E4%B8%AD%E9%83%BD%E5%8F%AF%E4%BB%A5%E7%94%A8%E6%9D%A5%E5%88%9B%E5%BB%BA%E7%94%A8%E6%88%B7%EF%BC%8C%E4%B8%8D%E5%AD%98%E5%9C%A8%E4%B8%80%E4%B8%AA%E5%8F%AF%E4%BB%A5%E4%B8%80%E4%B8%AA%E4%B8%8D%E5%8F%AF%E4%BB%A5%E7%9A%84%E6%A6%82%E5%BF%B5%EF%BC%9B%202%20Linux%E4%B8%AD%E9%80%9A%E5%B8%B8%E4%BC%9A%E4%BD%BF%E7%94%A8useradd%EF%BC%8C%E8%80%8CUbuntu%E4%B8%AD%E9%80%9A%E5%B8%B8%E4%BD%BF%E7%94%A8adduser%EF%BC%9B,3%20adduser%E5%91%BD%E4%BB%A4%E5%80%BE%E5%90%91%E4%BA%8E%E4%B8%80%E7%A7%8D%E4%BA%BA%E9%99%85%E5%AF%B9%E8%AF%9D%E7%9A%84%E8%BF%87%E7%A8%8B%EF%BC%8C%E5%AE%83%E4%BC%9A%E6%8F%90%E7%A4%BA%E6%93%8D%E4%BD%9C%E8%80%85%E6%8C%89%E7%85%A7%E6%AD%A5%E9%AA%A4%E8%AE%BE%E7%BD%AE%EF%BC%8C%E5%89%8D%E4%B8%A4%E6%AD%A5%E5%BD%93%E7%84%B6%E5%B0%B1%E6%98%AF%E8%BE%93%E5%85%A5%E5%AF%86%E7%A0%81%E5%92%8C%E5%86%8D%E6%AC%A1%E7%A1%AE%E8%AE%A4%E5%AF%86%E7%A0%81%EF%BC%8C%E8%80%8Cuseradd%E6%98%AF%E6%B2%A1%E6%9C%89%E4%BA%BA%E6%9C%BA%E5%AF%B9%E8%AF%9D%E8%BF%87%E7%A8%8B%E7%9A%84%EF%BC%9B%204%20adduser%E5%91%BD%E4%BB%A4%E5%8F%AF%E4%BB%A5%E4%B8%8D%E5%B8%A6%E4%BB%BB%E4%BD%95%E5%8F%82%E6%95%B0%E4%BD%BF%E7%94%A8%EF%BC%8C%E5%B9%B6%E5%9C%A8%E5%AE%8C%E6%88%90%E5%90%8E%E8%87%AA%E5%8A%A8%E5%88%9B%E5%BB%BA%E4%B8%BB%E7%9B%AE%E5%BD%95%EF%BC%8C%E8%80%8Cuseradd%E5%8D%B4%E4%B8%8D%E8%A1%8C%EF%BC%8C%E7%BD%91%E4%B8%8A%E6%9C%89%E4%B8%80%E7%A7%8D%E8%AF%B4%E6%B3%95%E6%98%AFuseradd%E5%88%9B%E5%BB%BA%E5%87%BA%E6%9D%A5%E7%9A%84%E7%94%A8%E6%88%B7%E6%B2%A1%E6%9C%89%E5%AF%86%E7%A0%81%E5%92%8C%E4%B8%BB%E7%9B%AE%E5%BD%95%EF%BC%8C%E8%BF%99%E7%A7%8D%E8%AF%B4%E6%B3%95%E6%98%AF%E4%B8%8D%E5%87%86%E7%A1%AE%E7%9A%84%EF%BC%8C%E5%9B%A0%E4%B8%BAuseradd%E4%B8%8D%E5%B8%A6%E5%8F%82%E6%95%B0%E7%9A%84%E4%BD%BF%E7%94%A8%E6%89%8D%E4%BC%9A%E8%BF%99%E6%A0%B7%EF%BC%8C%E8%BF%99%E5%B1%9E%E4%BA%8E%E4%BD%BF%E7%94%A8useradd%E5%88%9B%E5%BB%BA%E7%94%A8%E6%88%B7%E6%B2%A1%E6%9C%89%E5%81%9A%E5%AE%8C%E3%80%82%205%20useradd%E5%88%9B%E5%BB%BA%E7%94%A8%E6%88%B7%E7%9A%84%E8%BF%87%E7%A8%8B%EF%BC%8C%E7%94%A8%E6%88%B7%E5%90%8D%EF%BC%8C%E5%AF%86%E7%A0%81%E5%92%8C%E4%B8%BB%E7%9B%AE%E5%BD%95%E4%B8%89%E4%B8%AA%E8%BF%87%E7%A8%8B%E6%98%AF%E5%88%86%E5%BC%80%E8%BF%9B%E8%A1%8C%E7%9A%84%EF%BC%8C%E5%AE%83%E4%BB%AC%E5%88%86%E5%88%AB%E5%AF%B9%E5%BA%94%EF%BC%9A)、[useradd和adduser的区别](https://www.51cto.com/article/256231.html)、[菜鸟教程1](https://www.runoob.com/linux/linux-comm-useradd.html)、[菜鸟教程2](https://www.runoob.com/linux/linux-comm-adduser.html)、

- `adduser`和`useradd`在`Ubuntu`中都可以用来创建用户，不存在一个可以一个不可以的概念；

- `Linux`中通常会使用`useradd`，而`Ubuntu`中通常使用`adduser`；

- `adduser`命令倾向于一种人际对话的过程，它会提示操作者按照步骤设置，前两步当然就是输入密码和再次确认密码，而`useradd`是没有人机对话过程的；

- `adduser`命令可以不带任何参数使用，并在完成后自动创建主目录，而`useradd`却不行，网上有一种说法是`useradd`创建出来的用户没有密码和主目录，这种说法是不准确的，因为`useradd`不带参数的使用才会这样，这属于使用`useradd`创建用户没有做完。

- `useradd`创建用户的过程，用户名，密码和主目录三个过程是分开进行的，它们分别对应

  ```bash
  # 1.创建一个用户newuser
  useradd newuser
  
  # 2.为newuser设置密码
  passwd newuser
  
  # 2.为newuser设置主目录
  useradd -d /home/newuser newuser
  ```

- 上面三个过程，如果用`adduser`创建的话，就只需要：

  ```shell
  # 创建一个用户newuser，并交互式的设置密码
  adduser newuser
  ```



查看系统中创建过的用户： [链接](https://blog.csdn.net/tsummer2010/article/details/104427776)

```bash
# 第二个冒号后的值（用户ID）大于1000时，就是普通用户；
cat /etc/passwd

# 只筛选出了有用的信息，方便查看，【推荐使用这个命令】
cat /etc/passwd |cut -d: -f 1-3

# 输入：lastlog ，这个是系统的所有用户，绝大部分是系统内置的
```



## 2. 创建新用户

参考链接：[链接2](https://www.cnblogs.com/SH-xuliang/p/8422753.html)、[useradd 命令详解](http://data.digitser.net/ubuntu/zh-CN/useradd.html#)、[链接](https://blog.csdn.net/yl19870518/article/details/100776136)、

- `useradd`
- `adduser`

### 2.1 `useradd`创建用户

这里我们使用`useradd` 创建新用户，优点是可以自定义各种；

```bash
# 创建新用户
sudo useradd -d /mnt/md0/LPF -s /bin/bash -m LPF
sudo useradd -d /mnt/md0/LPF -m LPF

'''
-d, --home-dir HOME_DIR	home directory of the new account	新帐户主目录,若不指定默认在/home/username
-m, --create-home	create the users home directory	创建用户主目录 仅仅与-d一起用，没有参数
'''
```

**此时，登录该用户时shell开头为$，不显示用户名和路径。**

### 2.2 `usermod`修改用户信息

**原因：新建的用户未指定shell。我们只需将其指定为/bin/bash即可**  `usermod`

```bash
# 使用usermod命令修改shell类型
$ usermod [options] UserName
sudo usermod -s /bin/bash LPF
```

==此时还无法登录，因为没有设置登录密码==

```bash
sudo passwd LPF

# 设置密码后，切换到新建的用户
su LPF
```



### 2.3 设置`sudo`权限

- 方法1

  修改 `/etc/sudoers` 文件，在`root ALL=(ALL) ALL`后面添加新的一行`用户名 ALL=(ALL) ALL` ，保存并退出，添加超级用户权限完成。

  ```bash
  username ALL=(ALL) ALL
  ```

- 方法2

  使用 `adduser` 命令，直接一行，实际是将用户添加到 `sudo` 组中

  ```bash
  adduser username sudo
  ```



### 2.4 修改密码

参考链接：[链接1](https://linux.cn/article-10580-1.html)

- 修改当前用户的密码，只需要简单地在终端执行此命令：

  ```bash
  passwd
  ```

  系统会要求你输入当前密码和两次新的密码。

  

- 修改其他用户的密码，你也可以使用 `passwd` 命令来做。

  此处执行 `sudo`，要先输入你的 sudo 密码，如上提示已经修改，再输入给其它用户设置的新密码 两次。

  ```shell
  sudo passwd <user_name>
  ```





> **如何让用户之间文件相互隔离？**
>
> **-R参数：递归地修改访问权限**
>
> chmod配合-R参数可以递归地修改文件访问权限。
>
> 假如我要只允许newname这个用户能读，写，运行/home/newname这个目录的所有文件（当然，root不算，root可以做任何事），该怎么做呢？
>
> ```shell
> # 切换到newname用户账号下
> chmod -R 700 /home/newname
> ```





## 3. 删除用户及文件

删除用户`username`在系统文件中的记录以及用户的主目录

```bash
userdel -r username
```



- `userdel` 和 `deluser` 区别

```bash
userdel -h
deluser -h
```



```bash
# 将用户从一个组中删除 deluser USER GROUP
deluser mike students
```



## `TODO` 

### 分配账号流程

```shell
# 1 新建用户
sudo useradd -s /bin/bash -m LPF

# 2 设置密码
sudo passwd LPF

# 3 设置sudo权限, 在 root ALL=(ALL) ALL 后面添加新的一行`用户名 ALL=(ALL) ALL 
vim /etc/sudoers

# 4 给用户 home_dir 设置权限
chmod -R 700 /home/LPF

# 5 在挂载的硬盘里设置权限
chmod -R 700 /mnt/md0/LPF
```



### 安装软件环境，大家共享？？

### a. 文件/目录权限管理

[参考1](https://blog.csdn.net/yl19870518/article/details/100776136)、[参考2](https://www.cnblogs.com/SH-xuliang/p/8422753.html)、

### b. 组的管理

见参考1