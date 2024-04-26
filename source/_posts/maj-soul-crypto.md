---
title: 雀魂麻将牌山加密
date: 2024-04-26
tags:
---

每局游戏对局开始，点击左上角，可查看`牌山编码+盐`及`盐字符串`的 `SHA256码`

<img src="begin.jpg" style="zoom:30%;" />

对局结束，可通过牌谱查看牌山及盐字符串编码

<img src="end.jpg" style="zoom:30%;" />

雀魂每张牌都使用两位字符编码：1万-9万的编码是`1m-9m`，1筒-9筒的编码是`1p-9p`，1索-9索的编码是`1s-9s`，东南西北白发中的编码是`1z-7z`，红5万5筒5索的编码为`0m,0p,0s`

以这局三麻为例（108张牌，缺2-8万），可通过如下代码验证

```cpp
#include <openssl/sha.h>

#include <iostream>
#include <string>

namespace {

char hex(unsigned char ch) {
    if (ch < 10) return ch + '0';
    return ch - 10 + 'a';
}

std::string sha256(const std::string& str) {
    std::string ret;
    unsigned char md_buf[32];
    if (SHA256(reinterpret_cast<const unsigned char *>(str.data()), str.size(), md_buf)) {
        for (unsigned char ch : md_buf) {
            ret += (hex(ch >> 4));
            ret += (hex(ch % (1 << 4)));
        }
    }
    return ret;
}

}  // namespace

int main(int argc, char **argv) {
    const std::string salt = "3BTPHcg7hr3NXhMWuswVwC4F4TmBmguY";
    const std::string str =
            "5p7s6z9m1m3z7p1p4z9p3z6s6p2z6p1p3p2s3p0s7z1m3p8p4p1z2s1z4p1z5z4z2z7s3z5s5z3p5p4s6p4p4s"
            "5p9s3s8p9m6z3z5s9s8p5z8s8p6s9p4z1m7p7p9p3s0p6s6s6z5s7s5z7z1p1s2z2s9p7p3s9m1s1z8s4z2p4s"
            "9m4p9s2s7z7s9s2p7z3s1s2p2z6z6p1p2p4s8s8s1m1s";
    std::cout << sha256(salt) << '\n';
    std::cout << sha256(str + salt) << '\n';
}
```

输出如下

```
140d927b6c2d628f93823483df4694cfc023aa4e555928ca945115e58c19ebe9
baa9a22c3151b771d6e7107d885015d33927e557a33e30d8974ac8175e9a8c05
```

与对局开始给出的SHA256码一致。
