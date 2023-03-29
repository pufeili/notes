# Git Bash使用代理拉取仓库

> 使用git在拉取仓库时速度==很慢或者经常超时==
> 报错 `Failed to connect to github.com port 443
> after 21085 ms: Timed out`

在本地开代理后， `git bash` 需要进行相应的设置才能使用，简单记录一下：

## 1. 取消`git bash`代理

```bash
git config --global --unset http.proxy
git config --global --unset https.proxy
```

## 2. 更新`DNS`缓存

```bash
ipconfig /flushdns
```

## 3. 设置`git bash`代理

```bash
 git config --global https.proxy http://127.0.0.1:1080
 git config --global https.proxy https://127.0.0.1:1080
```

或者

```bash
git config --global http.proxy 'socks5://127.0.0.1:10808'
git config --global https.proxy 'socks5://127.0.0.1:10808
```
根据自己情况自行设置。
设置完成后，`git bash` 也可以借助科学上网进行加速了。