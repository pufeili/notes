# Linux后台运行任务

> 一般来说，常规的简单操作流程如下：
>
> 1. 新建会话  `tmux new -s <session-name>`
> 2. 在 `Tmux` 窗口运行所需的程序 `nohup command >logs.txt &`
> 3. 会话分离 使用命令 `tmux detach` 返回真终端
> 4. 下次使用时，重新连接到会话`tmux attach -t my_session`

## 1 `Tmux` 终端复用

### 1.1 安装

```shell
# Ubuntu 或 Debian
sudo apt-get install tmux
```

### 1.2 新建会话

```bash
tmux new -s <session-name>
# 举例
tmux new -s model
# 此时进入了一个伪终端界面
```

## 2 后台运行脚本

### 2.1 用 `nohup` 和 `&` 后台运行脚本

```bash
# 用法 nohup `command` &
nohup python sleep.py >logs.txt &
# 假如 py 文件的参数很多，可以新建一个sh文件，直接执行shell文件
```

> 注：假如`sleep.py`文件需要从外界传入参数，这个命令不可用，需要新建一个`shell`文件，执行`shell`文件
>
> 如何编写`shell`脚本见 [链接](https://github.com/pufeili/Knowlege/tree/master/shell_tutorial)

其中 `sleep.py` 文件内容是无限打印输出

```python
#!/usr/bin/env python3
import time

while(1):
    now_time = str(time.ctime())
    print(now_time)
    time.sleep(10)
```

> 命令解释：
>
> `nohup` 是指输出重定向，就是将 `python sleep.py` 的输出重定向，默认重定向到当前目录下的 `nohup.out` 文件下；
>
> `python sleep.py` 是指在终端下执行脚本；
>
> `> logs.txt` 是指定重定向输出，本来是重定向到 `nohup.out` 文件下的，现在重定向到 `logs.txt` 文件下。 
>
> `&` 是指将程序转入后台运行

### 2.2 退出伪终端

此时程序已经在后台运行了，并且会将输出重定向在日志文件中。现在可以暂时返回真终端，即使关闭真终端 `terminal` 或者断开服务器的连接，代码也可以在服务器运行。

```bash
tmux detach
```

此时已经返回到真终端，如何忘记伪终端名字，可以查看伪终端

```bash
tmux ls
```

### 2.3 重连伪终端

```bash
tmux attach -t <session_name>
```

## 3 查看后台进程并精准`kill`进程

> 注：使用`kill`杀死进程后，重定向的输出不会保留，无论是直接执行的 `python sleep.py` 还是 `run.sh`
>
> 使用 `fg` 将任务调度到前台，`ctrl+c`则会保留日志。

### 3.1 `ps` 命令：`全局`查看进程信息

==可以在伪终端，也可以在真终端==进行查询进程。简单使用方法如下：

```bash
# 使用ps -ef 或者 ps -aux 结合grep过滤
ps -ef | grep sleep
# 杀死进程  -9 表示强制杀死进程  这种杀死进程 重定向的输出logs文件也会消失
kill -9 PID
```

> `ps`命令是Process Status的缩写，功能比较强大，参数非常多，尤其与其他命令组合时可以完成很复杂的操作。
>
> `ps -ef |grep hzqtest`是常见用法之一：
>
> - `e`：表示列出所有进程
> - `f`：表示输出完整格式
> - `grep hzqtest`：表示过滤筛选`“hzqtest”`关键字。
>
> 上面例子中，第一列：用户名，第二列：PID，第三列：父级PID，最后一列：命令名称或路径

### 3.2 `jobs` 命令 查看`当前终端`任务信息

**注意： `job` 命令需要在伪终端才能查询到任务信息。**

```bash
# 通过jobs命令查看任务号
jobs -l
# 通过任务号 %N 杀死进程
# 这种杀死进程 重定向的输出logs文件也会消失
kill -9 %2

# 通过fg命令调到前台，再使用ctrl+c命令会保留logs文件
fg 任务号
```

- `fg 任务号`命令：将后台中的任务调至前台并继续运行。
- `Ctrl + z `命令：将正在前台执行的命令作业放到后台，并冻结运行状态
- `bg 任务号`命令：将后台冻结的任务再次运行起来，运行后任务还在后台



###  关于重定向输出(目前好像只有方法1可以配合nohup使用) 

- 方法一 `>>` 或者 `>` 符号

```bash
# 示例1：行尾追加内容，不覆盖原来内容
echo "test" >> 1.txt
# 示例2：文本添加内容（会覆盖文本内容）
echo "test" > 1.txt
```

- 方法二 `tee` 命令

```bash
# 示例1：行尾追加内容
echo "test" | tee -a 1.txt
# 示例2：覆盖文本内容
echo "test" | tee 1.txt
```

- 方法三 `awk`命令

```bash
# 示例1： 行尾追加内容
awk -i "$ a test" 1.txt
# 示例2：插入内容
awk -i "2a test" 1.txt
```



## 参考链接

[Linux后台运行任务nohup结合&用法以及如何精准查找进程并kill后台任务实践](https://zhuanlan.zhihu.com/p/96909198) 

[笔记](https://pufeili.github.io/notes/#/Linux/Tutorial-linux?id=_7-task7%e5%9c%a8linux%e7%b3%bb%e7%bb%9f%e4%b8%ad%e5%90%8e%e5%8f%b0%e8%bf%90%e8%a1%8c%e5%ba%94%e7%94%a8%e7%a8%8b%e5%ba%8f%ef%bc%8c%e5%b9%b6%e6%89%93%e5%8d%b0%e6%97%a5%e5%bf%97)

http://t.csdn.cn/BptHB





















