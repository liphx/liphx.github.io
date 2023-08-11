---
title: 函数默认参数与继承
date: 2023-08-11
tags: cplusplus
permalink: code/defaut-args-and-inheritance/
---

以下代码的输出是？

```cpp
#include <iostream>
using namespace std;

class A {
public:
    virtual void f(int x = 100) { cout << "class A: " << x << endl; }
    virtual ~A() {}
};

class B : public A {
public:
    void f(int x = 200) { cout << "class B: " << x << endl; }
};

int main() {
    A *obj = new B;
    obj->f();

    delete obj;
}
```

答案是 `class B: 100`

把代码贴进`https://cppinsights.io/`跑一下就很明确了，`obj->f()`等价于`obj->f(100)`

默认参数是编译期的行为，虚函数的多态发生在运行时，因此使用虚函数时要注意一下默认参数。
