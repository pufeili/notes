> remote# 表示服务器端
>
> local# 表示本地主机

# 登录远程Jupyter

1、确保你的服务器有`jupyter notebook`，如果没有bash输入`pip install jupyter`安装

或者安装 `jupyter-lab`，命令：`pip install jupyterlab`。

2、**先ssh连接到服务器**，然后**创建jupyter notebook密码**， bash输入

```shell
remote# jupyter notebook password

# 或者
remote# jupyter server password
```

3、**进入要使用的`服务端的python环境`(conda activate env)**，在服务器的某端口打开jupyter notebook，bash输入

```shell
remote# conda activate env_name
remote# jupyter notebook --no-browser --port=20000

# 或者
remote# jupyter-lab --no-browser --port=20000
```

> 这里20000为远程端口， 读者可自定义。
>
> 这里可以使用nohup命令将jupyter挂在系统后台，这样就不用打开第二个终端进行后续的操作。

4、在本地通过端口转发，ssh隧道远程JupyterNotebook

```shell
local# ssh -L localhost:2000:localhost:20000 username@IP
ssh -L localhost:2000:localhost:20000 li@172.20.62.41
```

5、在本地打开浏览器输入 `http://localhost:2000/`，即可登录。

---



# 退出远程Jupyter

## 方法1

在本地浏览器打开远程jupyter后点击右上角quit

## 方法2

```shell
# 1. 远程服务器命令行：
jupyter notebook stop your_port

# 2. 本地命令行
ssh username:password@remote_server_ip   "jupyter notebook stop  your_port"

# 3. 远程服务器bash
ssh username:password@remote_server_ip "pkill -u username jupyter"
```



# 安装tensorboard

TensorBoard 包含在 TensorFlow 库中，所以如果我们成功安装了 TensorFlow，我们也可以使用 TensorBoard。要单独安装 TensorBoard 可以使用如下命令：

```shell
pip install tensorboard
pip install tensorflow-gpu
```



## 启动 TensorBoard

1、本地启动TensorBoard

要启动 TensorBoard，打开终端或命令提示符并运行：

```shell
tensorboard --logdir=<directory_name>
```

将 `directory_name` 标记替换为保存数据的目录。默认是“logs”。

运行此命令后，我们将看到以下提示：

```shell
Serving TensorBoard on localhost; to expose to the network, use a proxy or pass –bind_allTensorBoard 2.2.0 at http://localhost:6006/ (Press CTRL+C to quit)
```

这说明 TensorBoard 已经成功上线。我们可以用浏览器打开http://localhost:6006/查看。

2、远程运行 TensorBoard

除了在本地运行之外，还可以远程运行 TensorBoard。如果我们在具有更强大 [GPU](https://cloud.tencent.com/product/gpu?from=10680) 的不同服务器之间进行并行训练，也可以本地检查结果。

首先， 使用SSH 并将远程服务器的端口映射到本地的计算机。

```shell
ssh -L 6006:127.0.0.1:6006 username@server_ip
```

然后只需要在远程服务器上启动 TensorBoard。在远程服务器上运行：

```shell
tensorboard --logdir=’logs’ --port=6006
```

我们可以访问 localhost:6006 来查看远程的TensorBoard。

3、在 Jupyter Notebooks 中使用 TensorBoard

如果想在 Jupyter Notebooks 中使用 TensorBoard，可以使用以下命令：

```shell
%load_ext tensorboard
```

运行这行代码将加载 TensorBoard并允许我们将其用于可视化。加载扩展后，我们现在可以启动 TensorBoard：

```shell
%tensorboard --logdir logs
```







参考：

https://blog.csdn.net/qq_34769162/article/details/107947034

https://zhuanlan.zhihu.com/p/367020783

























