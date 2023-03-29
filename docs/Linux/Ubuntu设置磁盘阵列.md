## `Ubuntu`设置磁盘阵列

> 实验室服务器重装之后，刚开始大家不知道磁盘设置了阵列，后来发现有两个硬盘里面内容一模一样，并且无法设置自动挂载，但是已经内容不同步了，现在硬盘快用满了，因此重新设置了阵列。

### 1 准备

https://www.cnblogs.com/Ray-liang/p/5996271.html

https://mlog.club/article/2077993

查看当前机器上是否具有磁盘阵列的配置（在 `/proc/mdstat` 文件内）

```shell
cat /proc/mdstat
```

```bash
> Output
> Personalities : [raid0] [linear] [multipath] [raid1] [raid6] [raid5] [raid4] [raid10] 
> md0 : active raid0 sdc[1] sdd[0]
>       209584128 blocks super 1.2 512k chunks
>
>            unused devices: <none>

# 如果没有
Personalities : 
unused devices: <none>
```

从文件系统中取消挂载磁盘:

sudo umount /dev/md0



#### 1.1 格式化原来的硬盘

参考：

https://blog.csdn.net/kkae8643150/article/details/106389639

https://zhuanlan.zhihu.com/p/385448034

**格式化出现错误**： https://blog.csdn.net/weixin_42728126/article/details/88887350

```bash
# 1. 查看磁盘情况
sudo fdisk -l

Disk /dev/sdb：1.8 TiB，2000398934016 字节，3907029168 个扇区
单元：扇区 / 1 * 512 = 512 字节
扇区大小(逻辑/物理)：512 字节 / 512 字节
I/O 大小(最小/最佳)：512 字节 / 512 字节
磁盘标签类型：dos
磁盘标识符：0x69776904

设备       启动       起点       末尾       扇区   大小 Id 类型
/dev/sdb1             2048 3711741951 3711739904   1.7T  f W95 扩展 (LBA)
/dev/sdb5             8192 1855983615 1855975424   885G  7 HPFS/NTFS/exFAT
/dev/sdb6       1855987712 3711741951 1855754240 884.9G  7 HPFS/NTFS/exFAT

# 2. 删除所有分区
sudo fdisk /dev/sdb
# 输入m，打印菜单
# 输入p，打印目前已有分区
# 输入d，去删除多余的分区 默认是最大编号的那个分区，如此下去一路d,回车，直至删除所有分区。
# 再输入p，打印下分区查看情况
# 这个时候要注意了，一定要保存，否则上述修改无效，保存方式按w

# 3. 不分区整个盘作文件系统 注：这里没有增加分区
# 查看dm管理状态
sudo dmsetup status
# 手工移除DM占用
sudo dmsetup remove_all
sudo dmsetup status

# 不分区整个盘作文件系统
sudo mkfs.ext4 /dev/sdb
sudo mkfs.ext4 /dev/sdc

# 4. 检查是否硬盘可以挂载(正常的硬盘)
# 挂载硬盘到该文件夹上
mount /dev/sde /data
# 查看挂载好的硬盘信息
df -hT
# 取消挂载
umount /dev/sde
# 查看磁盘状态
lsblk -o NAME,SIZE,FSTYPE,TYPE,MOUNTPOINT

# 5. 创建 RAID 1
sudo mdadm --create --verbose /dev/md0 --level=1 --raid-devices=2 /dev/sdb /dev/sdc
# 检查磁盘阵列的状态
cat /proc/mdstat
Personalities : [raid1] 
md0 : active raid1 sdc[1] sdb[0]
      1953382464 blocks super 1.2 [2/2] [UU]
      [>....................]  resync =  0.1% (3099584/1953382464) finish=167.7min speed=193724K/sec
      bitmap: 15/15 pages [60KB], 65536KB chunk

unused devices: <none>


```



### 2 硬盘格式化







### 3 设置`RAID`

参考：[链接](https://www.cnblogs.com/Ray-liang/p/5996271.html)

#### 3.1 创建 `RAID1`

```BASH
# 查看磁盘状态
lsblk -o NAME,SIZE,FSTYPE,TYPE,MOUNTPOINT

# 创建 RAID 1
sudo mdadm --create --verbose /dev/md0 --level=1 --raid-devices=2 /dev/sdb /dev/sdc
# 检查磁盘阵列的状态
cat /proc/mdstat
Personalities : [raid1] 
md0 : active raid1 sdc[1] sdb[0]
      1953382464 blocks super 1.2 [2/2] [UU]
      [>....................]  resync =  0.1% (3099584/1953382464) finish=167.7min speed=193724K/sec
      bitmap: 15/15 pages [60KB], 65536KB chunk

unused devices: <none>
```

#### 3.2 挂载文件系统

```bash
# 1.在阵列上创建文件系统
sudo mkfs.ext4 -F /dev/md0

# 2.在文件系统上创建挂载点的文件夹
sudo mkdir -p /mnt/md0

# 3.挂载阵列至挂载点文件夹上
sudo mount /dev/md0 /mnt/md0

# 4.检查是否已具有新的磁盘空间
df -h -x devtmpfs -x tmpfs

"""
Filesystem      Size  Used Avail Use% Mounted on
/dev/sda1       458G  150G  285G   35% /
/dev/md0        1.8T   77M  1.7T    1% /mnt/md0
"""
```

现在文件系统已经成载挂载将可以访问了。

#### 3.3 开机自动挂载

为了确保阵列开机时被载入，我们应该调整一下 `/etc/mdadm/mdadm.conf` 的配置文件，可以加以下的指令使系统在启动自检时扫描磁盘阵列的详细信息：

```shell
sudo mdadm --detail --scan | sudo tee -a /etc/mdadm/mdadm.conf
```

关于 `tee` 的用法可以参考下面的链接：[链接](https://zhuanlan.zhihu.com/p/34510815)

另外，可以更新 ` initfamfs ` 或者初始化RAM文件系统，这样一来阵列会在启动前就可以生效：

```shell
sudo update-initramfs -u
```

最重要的一点是一定要在 `/etc/fstab` 配置文件内加入自动挂载的设置：

```shell
echo '/dev/md0 /mnt/md0 ext4 defaults,nofail,discard 0 0' | sudo tee -a /etc/fstab
```

这样 ubuntu 启动后就会自动将磁盘阵列挂入了。



另外，如果没有设置自动挂载，在系统重启后或磁盘名称更改（插入其它硬盘会导致盘名变更的）例如 `/dev/md0` 变成了 `/dev/md127` 就可能会出现磁盘不能被挂载的问题，此时切记重新创建阵列，因这将会毁掉你的一切！重新手工挂载一下就OK了：

```shell
sudo mount /dev/md127 /mnt/md0
```



# -------------

```shell
lsblk -o NAME,SIZE,FSTYPE,TYPE,MOUNTPOINT



```



1 删除分区

