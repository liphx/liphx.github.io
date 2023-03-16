---
title: 安装Python2.7.18
date: 2023-08-18
tags: python
---


- Python2.7.18是python2的最后一个版本
- 最新的Debian已经不提供python2的软件源了
- 下载地址 <https://www.python.org/downloads/release/python-2718/>
- <https://blog.python.org/2020/04/python-2718-last-release-of-python-2.html>

```shell
wget https://www.python.org/ftp/python/2.7.18/Python-2.7.18.tgz
tar xvf Python-2.7.18.tgz
cd Python-2.7.18
./configure && make && make install
```
