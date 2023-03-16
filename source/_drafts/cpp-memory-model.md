---
title: C++内存模型
date: 2024-01-23
tags: cplusplus
---

处理器会按代码编写的顺序执行吗?

不一定

- 编译器优化
  - Vectorization https://zhuanlan.zhihu.com/p/337756824
  - Compile time
  - Loop unrolling 循环展开
  - 移除无用代码
  - ...
- CPU优化
  - INO Execution
  - Branch Prediction
  - OOO Execution
  - Dynamic Scheduling
  - ...

