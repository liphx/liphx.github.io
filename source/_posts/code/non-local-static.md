---
title: non-local static 对象初始化的顺序
date: 2023-08-11
tags: C++
permalink: code/non-local-static/
---

```cpp
// A.h, no header guard
#include <iostream>
class A {
public:
    int n;
    A(int i) : n(i) { std::cout << "A(" << n << ")" << std::endl; }
    int f() { return n; }
};

// A.cpp
#include "A.h"
extern A a;
A a(100);

// B.cpp
#include "A.h"
extern A a;
class B {
public:
    B() {
        std::cout << "B()" << std::endl;
        std::cout << a.f() << std::endl;
    }
};
B b;
int main() {}
```

```shell
$ g++ A.cpp B.cpp && ./a.out
A(100)
B()
100
$ g++ B.cpp A.cpp && ./a.out
B()
0
A(100)
```

不同翻译单元内 non-local static 对象初始化的顺序是不确定的，使用 Singleton 解决此类问题

```cpp
A& GetA() {
    static A a(100);
    return a;
}
```
