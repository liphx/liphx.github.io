---
title: gcc -Wreorder
date: 2023-08-25
tags: cplusplus
---

```cpp
#include <iostream>

struct B {
    B(int i) { std::cout << "B(" << i << ")" << std::endl; }
};

class A {
public:
    A(int i) : second(i), first(second) {}
    B first;
    int second;
};

int main() { A(100); }
```

gcc编译会给出`Wreorder`的警告

可能的输出

```
B(-1134720736)
```

<https://cppinsights.io/>处理的结果如下

```cpp
class A
{

  public:
  inline A(int i)
  : first{B(this->second)}
  , second{i}
  {
  }

  B first;
  int second;
};
```

but why? 原因在于C++类的析构要按成员构造的逆序对成员进行析构，而构造函数是可以重载的，
为了确保析构的顺序，构造时按成员声明的顺序进行构造，而非初始化列表中出现的顺序。
