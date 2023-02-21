## Ubuntu 18.04搭建samba服务器，实现磁盘映射

将服务器的磁盘映射网络驱动器，使得本地windows可以便捷访问

### 1. samba的安装

```
sudo apt-get install samba      
sudo apt-get install cifs-utils //新版本  
sudo apt-get install smbclient
sudo apt-get install samba-common
```

执行`smbstatus`,看到打印信息说明安装成功。

### 2. samba的配置

- 备份原始配置文件

  ```
  sudo cp /etc/samba/smb.conf /etc/samba/smb.conf.bak 
  ```

- 修改现有的配置文件

  ```
  sudo vim /etc/samba/smb.conf 
  ```

  在smb.conf文件最后一行添加以下信息

  ```
  [server1]			#在windows映射网络驱动器下显示的名字(修改)
  security = share		#共享
  comment = share all 
  path = /home/share	#ubuntu要共享的文件名字路径(修改)
  browseable = yes		#可浏览
  writable = yes		#可写
  available = yes		
  public = yes
  force user = root
  valid users = doubleh,root  #用户名，root权限(修改)
  write list = doubleh,root   #用户名，root权限(修改)
  create mask = 0777		   #创建时开全部权限
  directory mask = 0777	   #文件夹开最高
  force directory mode = 0777
  force create mode = 0777
  ```

### 3. 重启Samba服务器使其生效

  这里键入samba时按tab键补全信息，后面+空格restart

  ```
  sudo /etc/init.d/samba restart
  ```

### 4. 为访问当前Ubuntu添加samba用户

```
sudo smbpasswd -a xxx  #xxx为用户名
```

会提示输入密码，为在windows连接时用，可以为空。此时在ubuntu端的操作全部完成。

### 5. Windows端建立映射

`win+r` 打开运行，键入 `\\xxx.xx.xx.xxx`  (ip地址)回车，输入刚才**步骤4设置的用户名和密码登录**，右键共享的文件夹->映射网络驱动器，即可将其映射在windows虚拟磁盘下。

references:
[blog1](https://blog.csdn.net/DynastyDoubleH/article/details/88742488?utm_medium=distribute.pc_relevant.none-task-blog-2~default~baidujs_title~default-1.no_search_link&spm=1001.2101.3001.4242), [blog2](https://blog.csdn.net/nameofcsdn/article/details/78458930?locationNum=9&fps=1&utm_medium=distribute.pc_relevant.none-task-blog-2~default~baidujs_title~default-0.no_search_link&spm=1001.2101.3001.4242), [blog3](https://blog.csdn.net/weixin_43835377/article/details/88844021?utm_medium=distribute.pc_relevant_t0.none-task-blog-2%7Edefault%7ECTRLIST%7Edefault-1.no_search_link&depth_1-utm_source=distribute.pc_relevant_t0.none-task-blog-2%7Edefault%7ECTRLIST%7Edefault-1.no_search_link)
