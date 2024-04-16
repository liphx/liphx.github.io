---
title: 替换gethostbyname
date: 2024-04-16
tags: net
---

## gethostbyname

为了获取域名的ip地址，我写了如下代码

```cpp
std::string host2ip(const std::string& host) {
    if (host.empty()) return {};
    std::regex valid_ipv4_re(R"(^((25[0-5]|(2[0-4]|1\d|[1-9]|)\d)\.?\b){4}$)");
    std::smatch ipv4_match;
    if (std::regex_match(host, ipv4_match, valid_ipv4_re)) {
        return host;
    }
    struct hostent *server = gethostbyname(host.c_str());
    if (!server) {
        LOG(ERROR) << "gethostbyname fail, host: " << host;
        return {};
    }
    char addr[128];
    inet_ntop(server->h_addrtype, server->h_addr, addr, sizeof(addr));
    return addr;
}
```

如果参数是个ipv4地址，则直接返回，否则通过`gethostbyname`函数查询。

服务运行了一个半月左右，登上机器一看发现有两次coredump（有脚本辅助重启，客户端没感知到），堆栈如下

```
#0  inet_ntop4 (size=128, dst=0x7f864afcc870 "\020", src=0x0) at ./resolv/inet_ntop.c:85
#1  __GI_inet_ntop (af=2, src=0x0, dst=0x7f864afcc870 "\020", size=128) at ./resolv/inet_ntop.c:57
#2  0x000055f656081cab in liph::host2ip(std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > const&)
    ()
```

`src`参数为`null`，再查看下`gethostbyname`[函数手册](https://man7.org/linux/man-pages/man3/gethostbyname.3.html)，发现是不可重入的。可重入版本是`gethostbyname_r`，但是POSIX规范中这些函数都被标记为`deprecated`，我们有更好的选择。

## getaddrinfo

```c
#include <netdb.h>
#include <sys/socket.h>
#include <sys/types.h>

struct addrinfo {
    int ai_flags;
    int ai_family;
    int ai_socktype;
    int ai_protocol;
    socklen_t ai_addrlen;
    struct sockaddr *ai_addr;
    char *ai_canonname;
    struct addrinfo *ai_next;
};

int getaddrinfo(const char *restrict node, const char *restrict service, const struct addrinfo *restrict hints, struct addrinfo **restrict res); // 线程安全
void freeaddrinfo(struct addrinfo *res);
const char *gai_strerror(int errcode);
```

替换如下

```cpp
std::string host2ip(const std::string& host) {
    if (host.empty()) return {};
    std::regex valid_ipv4_re(R"(^((25[0-5]|(2[0-4]|1\d|[1-9]|)\d)\.?\b){4}$)");
    std::smatch ipv4_match;
    if (std::regex_match(host, ipv4_match, valid_ipv4_re)) {
        return host;
    }
    struct addrinfo hints;
    memset(&hints, 0, sizeof(hints));
    hints.ai_family = AF_UNSPEC;  // IPv4 or IPv6
    struct addrinfo *result;
    int r = getaddrinfo(host.c_str(), nullptr, &hints, &result);
    if (r != 0) {
        LOG(ERROR) << "host: " << host;
        LOG(ERROR) << "getaddrinfo fail: " << gai_strerror(r);
        return {};
    }
    if (result) {  // do not need result->ai_next
        char addr[128];
        void *src = nullptr;
        if (result->ai_family == AF_INET) {
            src = &(((struct sockaddr_in *)result->ai_addr)->sin_addr.s_addr);
        } else if (result->ai_family == AF_INET6) {
            src = &(((struct sockaddr_in6 *)result->ai_addr)->sin6_addr);
        } else {
            return {};
        }
        inet_ntop(result->ai_family, src, addr, sizeof(addr));
        freeaddrinfo(result);
        return addr;
    }
    return {};
}
```

