---
title: Git 稀疏检出
date: 2023-08-28
tags: tools
---

<https://git-scm.com/docs/git-sparse-checkout>

```shell
$ git status
无文件要提交，干净的工作区
$ find . -type f | wc -l
787024
$ git sparse-checkout set path...
$ find . -type f | wc -l
86072
$ git status
您处于稀疏检出状态，包含 2% 的跟踪文件
无文件要提交，干净的工作区
$ git sparse-checkout list
```
