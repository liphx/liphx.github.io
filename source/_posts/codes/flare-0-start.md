---
title: "flare 0 - start"
date: 2023-08-18
tags:
  - cplusplus
  - flare
categories: code
---

#### flare

github地址 <https://github.com/Tencent/flare>

简介：腾讯广告使用的C++后台服务框架，包含一系列基础库，fiber库，RPC等特性

环境支持：Linux x86-64 gcc8+

#### 编译

```shell
apt install git-lfs
git lfs install
git lfs pull
cd thirdparty/blade/
./install
source ~/.profile
blade build ...
```

#### example

示例文档 <https://github.com/Tencent/flare/blob/master/flare/doc/intro-rpc.md>

1. `flare/init.h`

   1. `int flare::Start(int argc, char** argv, Function<int(int, char**)> cb);` 执行用户回调前后初始化与清理环境。
   1. `flare::WaitForQuitSignal()`
2. `flare/rpc/server.h`
   1. `Server::Server(Options options = Options())`  以`options`初始化`Server`
   1. `Server::AddProtocol(const std::vector<std::string>& names)` 在服务上注册通信协议
   1. `Server::AddService()` 添加服务类的实例
   1. `Server::ListenOn()` listen on endpoint
   1. `Server::Start()`
   1. `Server::Stop()`
   1. `Server::Join()`
3. `flare/rpc/protocol/protobuf/rpc_channel.h`
   1. `class flare::RpcChannel : public google::protobuf::RpcChannel`
4. `flare/rpc/protocol/protobuf/rpc_client_controller.h`
   1. `class flare::RpcClientController : public protobuf::RpcControllerCommon`

运行

```shell
$ ./server
$ ./client
I0818 08:14:46.082238  3432 init.cc:114] Flare started.
I0818 08:14:46.088726  3432 runtime.cc:425] Using fiber scheduling profile [neutral].
I0818 08:14:46.088794  3432 runtime.cc:220] Starting 6 worker threads per group, for a total of 1 groups. The system is treated as UMA.
I0818 08:14:46.095507  3432 init.cc:122] Flare runtime initialized.
I0818 08:14:46.128015  3447 client.cc:43] Received: [Hello there.]
I0818 08:14:46.268503  3432 init.cc:162] Exited
```

