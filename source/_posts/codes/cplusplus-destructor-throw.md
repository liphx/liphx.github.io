---
title: 在析构函数中抛出异常
date: 2023-08-11
tags: cplusplus
---

```cpp
#include <cstdio>

struct A {
    ~A() {
        puts("~A()");
        throw 0;
    }
};

int main() {
    try {
        A();
        puts("after ~A()");
    } catch (...) {
        puts("catch");
    }
}
```

分别用C++98和11标准进行编译及运行

```shell
$ g++ examples/destructor-throw.cpp -std=c++98 && ./a.out
~A()
catch
$ g++ examples/destructor-throw.cpp -std=c++11 && ./a.out
examples/destructor-throw.cpp:6:9: warning: '~A' has a non-throwing exception specification but can still throw [-Wexceptions]
        throw 0;
        ^
examples/destructor-throw.cpp:4:5: note: destructor has a implicit non-throwing exception specification
    ~A() {
    ^
1 warning generated.
~A()
libc++abi: terminating with uncaught exception of type int
Abort trap: 6
```

开启C++11标准后，编译器已经给出了警告。实际上，C++11起，析构函数默认是noexcept的，抛出异常将会terminate。

做一点修改，再次编译

```diff
 #include <cstdio>

 struct A {
-    ~A() {
+    ~A() throw(int) {
         puts("~A()");
         throw 0;
     }
```

```shell
$ g++ examples/destructor-throw.cpp -std=c++11 && ./a.out
~A()
catch
$ g++ examples/destructor-throw.cpp -std=c++17 && ./a.out
examples/destructor-throw.cpp:4:10: fatal error: ISO C++17 does not allow dynamic exception specifications [-Wdynamic-exception-spec]
    ~A() throw(int) {
         ^~~~~~~~~~
examples/destructor-throw.cpp:4:10: note: use 'noexcept(false)' instead
    ~A() throw(int) {
         ^~~~~~~~~~
         noexcept(false)
1 error generated.
```

给析构函数添加动态异常说明后，程序不会崩溃。要注意的是，动态异常说明在C++11中标记为弃用，C++17起已经移除了。

总结：不要把异常抛出析构函数。
