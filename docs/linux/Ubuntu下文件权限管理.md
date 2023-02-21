# `Ubuntu`下文件/目录权限管理

## 1 `ll`命令查看文件/目录权限

- `ubuntu` 下 `ls` 命令：仅列出当前文件名或目录名
- `ll` 命令：列出当前文件或目录的详细信息，`ll` 和 `ls -l` 命令的作用一致，`ll` 是 `ls -l` 的别名。 ==tips: alias 可以查看别名==

`ll` 命令返回说明：

```bash
# 从左往右 共
drwxr-xr-x   2 root root 48 2013-11-27 16:34 test/
lrwxr-xr-x   1 root root 48 2013-11-27 16:34 show/
```

- 档位1：drwxr-xr-x

  ```bash
  # 第一个字母
  d：是英语directory的缩写，表示“目录”。就是说这是一个目录。
  l：是英语link的缩写，表示“符号链接”。就是说这是一个链接。
  -：普通文件
  b：设备文件
  c：字符设备文件
  
  # 后面每3个一组
  r：是英语read的缩写，表示“读”。就是说可以读这个文件。
  w：是英语write的缩写，表示“写”。就是说可以写这个文件，也就是可以修改。
  x：是英语execute的缩写，表示“执行，运行”。就是说可以运行这个文件
  
  d		rwx		 rwx  		rwx
  目录	 所有者u    群组用户g	其它用户o
  第一组rwx表示文件的所有者对于此文件的访问权限。
  第二组rwx表示文件所属的群组的其他用户对于此文件的访问权限。
  第三组rwx表示除前两组之外的其他用户对于此文件的访问权限。
  ```

- 档位2：表示该目录下文件/文件夹的数量，包括 `.` 和 `..` 

- 档位3：表示该文件或目录的拥有者。

- 档位4：表示所属的组（group）。每一个使用者都可以拥有一个以上的组，不过大部分的使用者应该都只属于一个组，只有当系统管理员希望给予某使用者特殊权限时，才可能会给他另一个组。

- 档位5：表示文件大小。文件大小用byte来表示，而空目录一般都是1024byte，当然可以用其它参数使文件显示的单位不同，如使用ls –k就是用kb莱显示一个文件的大小单位，不过一般我们还是以byte为主。

- 档位6：表示最后一次修改时间。以“月，日，时间”的格式表示，如Aug 15 5:46表示8月15日早上5:46分。

- 档位7：表示文件名。我们可以用 `ls –a` 显示隐藏的文件名。



## 2 `chmod`命令修改文件权限

`Linux chmod`（英文全拼：`change mode`）命令是控制用户对文件的权限的命令。`chmod`命令用于修改文件的各种访问权限。

语法：`chmod [-cfvR] [--help] [--version] mode file...` 

```bash
chmod 权限操作 文件名
```

一般来说方括号内是可选参数，可设置可不设置，其中经常用到的是 `-R` ，表示对目前目录下的所有文件与子目录进行相同的权限变更(即以递归的方式逐个变更)，`mode` 就是要更改的权限，有以下两种方式更改权限：

### 2.1 八进制语法指定权限：chmod的绝对用法

Linux系统对每种权限（r，w和x）分配了对应的数字：

```bash
权限  数字
 r   　4
 w   　2
 x   　1
 
# 对不同的权限，有以下几种组合形式，假如我们要分配读，写权限，那么我们就只需要将对应的数字相加，4+2，就等于6。
 权限  　数字     计算
 ---     0   　0 + 0 + 0
 r--     4   　4 + 0 + 0
 -w-     2   　0 + 2 + 0
 --x     1   　0 + 0 + 1
 rw-     6   　4 + 2 + 0
 -wx     3   　0 + 2 + 1
 r-x     5   　4 + 0 + 1
 rwx     7   　4 + 2 + 1
 
# 所以，对于访问权限的三组（所有者的权限，群组用户的权限，其他用户的权限），我们只要分别做加法就可以了，然后把三个和连起来。
chmod 600 file.txt

例如：640分别表示：
1 文件的所有者有读和写的权限。
2 文件所在群组的其他用户具有读的权限。
3 除此之外的其他用户没有任何权限。
```

因此，我们可以给的最宽泛的权限就是 777：所有者，群组用户，其他用户都有读，写和运行的权限。

### 2.2 符号模式指定权限：chmod的相对用法

以`[用户标识][操作符][权限内容]`为语法规则，具体如下：

- 用户标识：
  u——表示文件所属用户（user）
  g——表示所属用户组（group）
  o——表示其他用户（other）
  a——表示以上三个所有（all）；

- 操作符：
  `+`——增加权限
  `-`——删除权限
  `=`——分配权限；
- 权限内容：（权限内容可以多项一起）
  r——读权限
  w——写权限
  x——执行权限

>举几个例子：（这里省略了可能需要的管理员权限，如果需要就在下列命令前加sudo）
>chmod u+w aFile：给aFile的所属用户增加对aFile的写权限
>chmod g-w aFile：使aFile的所属用户组对aFile不能写
>chmod a+rwx aFile：给所有用户对aFile增加读、写、执行权限
>chmod u=rw：将aFile的所属用户对aFile的权限设置为读、写（这里没有x所以相当于rw-，即使修改之前所属用户有执行权限，执行该命令后执行权限会被删除）。

```bash
#文件file.txt的所有者分配读，写和执行的权限；群组其他用户分配读的权限，不能写或执行；其他用户没有任何权限。
chmod u=rwx,g=r,o=- file.txt
```

**-R参数：递归地修改访问权限**

chmod配合-R参数可以递归地修改文件访问权限。

假如我要只允许newname这个用户能读，写，运行/home/newname这个目录的所有文件（当然，root不算，root可以做任何事），该怎么做呢？

```bash
chmod -R 700 /home/newname
```

## 3 `chown`命令修改文件所属权

`Linux chown`（英文全拼：**change owner**）命令用于设置==文件所有者==和==文件关联组==的命令。

只有超级用户和属于组的文件所有者才能变更文件关联组。非超级用户如需要设置关联组可能需要使用 [chgrp](https://www.runoob.com/linux/linux-comm-chgrp.html) 命令。

语法和 `chmod` 类似：`chown [-cfhvR] [--help] [--version] user[:group] file...`

举例：

```bash
# 把 /var/run/httpd.pid 的所有者设置 root
chown root /var/run/httpd.pid

# 将文件 file1.txt 的拥有者设为 runoob，群体的使用者 runoobgroup
chown runoob:runoobgroup file1.txt

# 将当前前目录下的所有文件与子目录的拥有者皆设为 runoob，群体的使用者 runoobgroup
chown -R runoob:runoobgroup *

# 把 /home/runoob 的关联组设置为 512 （关联组ID），不改变所有者
chown :512 /home/runoob
```

```bash
#遇到权限不足的情况自行添加sudo，没sudo权限就联系管理员吧
chown user1 aFile #修改aFile的所属用户为user1；
chown user1: aFile #修改aFile的所属用户为user1，所属用户组为user1所在的主组；
chown :Group1 aFile #修改aFile的所属用户组为Group1，所属用户不变；
chown user1:Group2 aFile #修改aFile的所属用户为user1，所属用户组为Group2；
```

## 4 `chgrp`命令修改文件群组

`Linux chgrp`（英文全拼：change group）命令用于变更文件或目录的所属群组。

与 [chown](https://www.runoob.com/linux/linux-comm-chown.html) 命令不同，`chgrp `允许普通用户改变文件所属的组，只要该用户是该组的一员。

语法： 

```bash
chgrp [-cfhRv][--help][--version][所属群组][文件或目录...] 或 
chgrp [-cfhRv][--help][--reference=<参考文件或目录>][--version][文件或目录...]

# 举例
chgrp newname file.txt
```



---

**举例说明**：Linux系统新挂载了一个硬盘，命名为publicspace。 
设置一个公共盘publicshare，所有用户都可以访问该文件夹来分享文件

```bash
chmod 777 publicshare -R
```

 

若在该文件夹新建文件夹newname,只能让用户newname有权限对文件夹newname

```bash
# 更改文件的所有者和组
sudo chown newname:newname newname
```

 

```bash
# 更改文件的读写权限
sudo chmod go-rw newname
```

---



## 5 `TODO`

### /etc/skel目录

### 新建用户的独立性

见博客2



## 参考链接：

[ls命令的用法](https://www.linuxidc.com/Linux/2018-07/153131.htm)、[ll用法](https://www.cnblogs.com/linxisuo/p/13883762.html)   

[chmod命令](https://www.runoob.com/linux/linux-comm-chmod.html)、[Linux chown 命令](https://www.runoob.com/linux/linux-comm-chown.html)、

[博客1](https://blog.csdn.net/yl19870518/article/details/100776136)、

[博客2](https://www.cnblogs.com/SH-xuliang/p/8422753.html)、



