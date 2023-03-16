---
title: linux
---

# Linux 是一种生活态度

## X Window System

## X server & X Client

## X Display Manager

* gdm3 - GNOME Display Manager
* sddm - Simple Desktop Display Manager
* kdm - KDE Display manager
* lightdm - a display manager

```shell
$ cat /etc/X11/default-display-manager
/usr/sbin/gdm3
$ sudo dpkg-reconfigure lightdm
```

## Desktop Environment

* gnome
* kdm
* xfce
* lxde

## 使用Linux的一些原则

+ 能不用root身份执行的命令尽量不用root
+ 不要执行任何不熟悉的命令
+ 文件命名推荐只使用使用字符的一个子集 `a-z, A-Z, 0-9, ., -, _`
+ 尊重其他用户的隐私（无论你是否以root身份登录）

## 免密登录ssh

把本地的`ssh公钥`，比如文件`~/.ssh/id_rsa.pub`，追加写入服务器的`~/.ssh/authorized_keys`

## 免密sudo

```shell
sudo echo 'your_name ALL=(ALL:ALL) NOPASSWD:ALL' >> /etc/sudoers
```

## 文件/etc/motd

`motd`是`message of the day`的缩写，当我们用`ssh`登录服务器的时候就会显示这个文件中的内容

## 工具

文本对比

diff colordiff

## 限制通过ssh 登录 root

1. 编辑 `/etc/ssh/sshd_config`
2. 设置 `PermitRootLogin no`
3. `service ssh restart`

# Disk

## 硬盘(Hard Disk Drive, HDD, 机械硬盘)

硬盘一般用作电脑上的非易失性存储器，主要由盘片，磁头，盘片转轴，电动机等组成。一个盘片上下表面均有磁性材料（一个盘片有两个盘面），二进制位01即通过不同的模式存储在上面。
每个盘面有一个磁头，磁头贴近地悬浮在盘面上，主要用来读取和改变磁盘表面磁方向。
每个盘面上有多个磁道，它们是盘面上的同心圆，多个盘片处于同一半径圆的多个磁道组成的圆柱面称为柱面。
每个磁道分为多个弧段，称为扇区(Sector)。扇区是磁盘读写的基本单位。整个磁盘的第一个扇区称为引导扇区。
因为半径不同，不同磁道上的扇区数可能不同。

扇区大小可以通过 `fdisk -l` 查看，如以下输出表示扇区大小为 512 字节

```
Units: sectors of 1 * 512 = 512 bytes
Sector size (logical/physical): 512 bytes / 512 bytes
```

磁盘容量即扇区数量乘以扇区容量

### 数据接口

硬盘的数据接口大致分为 ATA(又称IDE), SATA, SCSI, SAS. 不同接口的传输速率不同

### 电源接口

- 3.5存台式机硬盘使用电源口供电，如 SATA 硬盘使用 SATA 电源线
- 2.5存笔记本硬盘使用数据口供电，不需要额外电源口
- 移动硬盘使用 USB 接口传输与供电

## 分区表

硬盘分区是指将硬盘划分为几个逻辑部分（不方便单独对扇区进行管理）

### MBR

MBR(Master Boot Record, 主引导记录) 在磁盘的第一个扇区(512 字节)，其组成(446 字节)如下

- boot loader code (440 字节，最大446)
- 选用磁盘标志 (4 字节)
- 0x0000 (2 字节空值)

MBR 之后是4个16字节的 DPT(磁盘分区表)与2字节的结束标记(55AA)

DPT 结构如下

| 偏移量 | 字节 | 定义 |
| -- | -- | -- |
| 0x00 | 1 | 分区状态: 非活动分区(0x00), 活动分区(0x80) |
| 0x01 | 1 | 分区起始磁头号 |
| 0x02 | 2 | 分区起始扇区号(5 bits) + 分区起始柱面号(11 bits) |
| 0x04 | 1 | 文件系统标识位, 如 0x83 表示 Linux 分区 |
| 0x05 | 1 | 分区结束磁头号 |
| 0x06 | 2 | 分区结束扇区号(5 bits) + 分区结束柱面号(11 bits) |
| 0x08 | 4 | 分区起始相对扇区号 |
| 0x0c | 4 | 分区总的扇区数 |

DPT 只能记录4个分区信息，且每个分区能表示的最大扇区数为(0xFFFFFFFF, 4 字节)，最多支持4个分区，每个分区最大2T 的空间

```
2TB = 2 ^ 32(Sectors) * 512(Bytes/Sector) / 1024(Bytes/KB) / 1024(KB/MB) / 1024(MB/GB) / 1024(GB/TB)
```

文件系统标识位为 0x05 表示扩展分区，扩展分区可以用类似 GPT 的方式描述逻辑分区，因此实际上可以分出任意多个逻辑分区

`fdisk -l` 输出信息 `Disklabel type: dos` 即为 MBR 分区表

`fdisk /dev/sdx` 中命令 `o` 用于创建 MBR 分区表

### GPT

GPT(GUID Partition Table, 全局唯一标识分区表)硬盘中，分区表的信息记录在GPT头中，出于兼容性考虑，硬盘的第一个扇区仍然用作MBR，之后才是GPT头

格式如下

- LBA 0(MBR), 兼容传统 MBR 结构，仅有一个分区，标识位为 0xEE, 标识这块硬盘使用 GPT 分区表
- LBA 1(分区表)

## 分区格式

Linux cpu cache命中率

```shell
$ sudo apt install linux-perf

$ cat /proc/sys/kernel/perf_event_paranoid
-1

$ g++ -g -std=c++11 main.cpp && perf record -a ./a.out && perf report
$ perf stat ./a.out

 Performance counter stats for './a.out':

            786.25 msec task-clock                #    0.998 CPUs utilized          # cpu利用率
                 7      context-switches          #    0.009 K/sec                  # 进程切换次数
                 0      cpu-migrations            #    0.000 K/sec                  # CPU迁移，使用另一个核调度
                42      page-faults               #    0.053 K/sec
   <not supported>      cycles                                                                                                   # 处理器时钟
   <not supported>      instructions                                                                                               # 机器指令数目
   <not supported>      branches
   <not supported>      branch-misses

       0.787566384 seconds time elapsed

       0.786847000 seconds user
       0.000000000 seconds sys

$ perf stat -e cache-misses,cache-references -r 5 ./a.out

 Performance counter stats for './a.out' (5 runs):

            14,539      cache-misses                                                  ( +-  9.11% )

       0.165718286 seconds time elapsed                                          ( +-  0.73% )

$ LD_LIBRARY_PATH=/docker/opt/rh/devtoolset-3/root/usr/lib64 perf top -p $(pidof sf) -e cache-misses,cache-references

1min
压缩 qpm(2.12K)
Available samples
616K cache-misses
661K cache-references

未压缩 qpm(2.33K)
Available samples
741K cache-misses
787K cache-references

>>> 616/661
0.9319213313161876
>>> 741/787
0.9415501905972046

```

```cpp
#include <cstdint>

const int N = 1024;
int64_t arr[N][N][N];

int main() {
    for (int i = 0; i < N; i++)
        for (int j = 0; j < N; j++)
            for (int k = 0; k < N; k++)
                arr[i][j][k]++;
}
```

```shell
$ diff main.cpp main2.cpp  -u
--- main.cpp    2022-06-29 15:50:20.015520972 +0800
+++ main2.cpp   2022-06-29 15:45:00.561930419 +0800
@@ -7,5 +7,5 @@
     for (int i = 0; i < N; i++)
         for (int j = 0; j < N; j++)
             for (int k = 0; k < N; k++)
-                arr[i][j][k]++;
+                arr[k][j][i]++;
 }
```

```shell
$ perf stat -e cache-misses,cache-references ./test1

 Performance counter stats for './test1':

        17,353,890      cache-misses              #   17.681 % of all cache refs
        98,152,559      cache-references

       5.383523208 seconds time elapsed

dev:~$ perf stat -e cache-misses,cache-references ./test2

 Performance counter stats for './test2':

     1,118,657,362      cache-misses              #   73.016 % of all cache refs
     1,532,064,546      cache-references

      32.273535127 seconds time elapsed

```

cache memories

```shell
$ getconf -a | grep CACHE
LEVEL1_ICACHE_SIZE                 32768
LEVEL1_ICACHE_ASSOC                8
LEVEL1_ICACHE_LINESIZE             64
LEVEL1_DCACHE_SIZE                 32768
LEVEL1_DCACHE_ASSOC                8
LEVEL1_DCACHE_LINESIZE             64
LEVEL2_CACHE_SIZE                  524288
LEVEL2_CACHE_ASSOC                 8
LEVEL2_CACHE_LINESIZE              64
LEVEL3_CACHE_SIZE                  268435456
LEVEL3_CACHE_ASSOC                 0
LEVEL3_CACHE_LINESIZE              64
LEVEL4_CACHE_SIZE                  0
LEVEL4_CACHE_ASSOC                 0
LEVEL4_CACHE_LINESIZE              0
$ cat /proc/cpuinfo
cache size      : 512 KB
cache_alignment : 64
$ lscpu
L1d cache:             32K
L1i cache:             32K
L2 cache:              512K
L3 cache:              32768K

```

## 局部性（locality）

时间局部性：引用过的内存位置，不久后再次引用。

空间局部性：引用过的内存位置，不久后引用附件的位置。

硬件上：高速缓存存储器保存最近被引用的指令和数据项。

操作系统：使用主存作为虚拟地址空间最近被引用块的高速缓存。

```shell
$ free
             total       used       free     shared    buffers     cached
Mem:      67108864   44951396   22157468          0          0   42561568
-/+ buffers/cache:    2389828   64719036
Swap:      2097152      59532    2037620

# total = used + free
```

Page cache



```
perf top -p $(pidof sf) -e cache-references,cache-misses,cycles,instructions,branches,L1-dcache-load-misses,L1-dcache-loads,L1-dcache-stores,L1-icache-load-misses,LLC-loads,LLC-load-misses,LLC-stores,LLC-store-misses
```

```
```

perf record -g -p $(pidof sf)


core dumped

`man 5 core`
`ulimit -c unlimited`
`/proc/sys/kernel/core_pattern`
