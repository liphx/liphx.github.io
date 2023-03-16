---
title: 在区分大小写的mac文件系统上运行steam
date: 2024-04-19
tags: tools
---

重装Mac后文件系统选了APFS(区分大小写)，没想到安装完Steam运行报错：`~/Library/Application Support/Steam`要求安装在不区分大小写的文件系统中。

好在有解决办法

1. 打开磁盘工具新增宗卷，格式为APFS(不区分大小写)
2. 在`/Volumes/apfs/`(apfs为宗卷名)下创建目录`Steam`
3. 在`/Volumes/apfs/`下安装steam
4. `ln -sf /Volumes/apfs/Steam "/Users/liph/Library/Application Support/Steam"`
5. 启动steam，完成更新
