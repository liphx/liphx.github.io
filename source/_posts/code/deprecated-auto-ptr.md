---
title: C++11为什么弃用std::auto_ptr
date: 2023-08-11
tags: C++
permalink: code/deprecated-auto-ptr/
---

先看一下`auto_ptr`的拷贝构造函数(C++11前还没有移动语义)

```cpp
auto_ptr(auto_ptr&);
auto_ptr& operator=(auto_ptr&);
```

与一般的拷贝构造函数不同的是，`std::auto_ptr`为了获取对象的所有权，会修改参数(release())

一个简单的问题如下

```cpp
std::auto_ptr<int> pa(new int(100));
std::auto_ptr<int> pb(pa);
std::cout << *pa << std::endl;
```

由于对象的所有权由`pb`所有，`pa.release`后，`*pa`实际上是对`nullptr`解引用，直接Segmentation fault了。

当然，尽管这是个低级错误，但是像下面的使用也会有同样的问题

```cpp
void f(std::auto_ptr<int> ptr);
std::vector<std::auto_ptr<int> > vc; // C++03这里需要一个空格
```

那么，为什么`std::auto_ptr`不仅仅弃用拷贝构造与赋值运算符呢？

首先，`boost::scoped_ptr`就是这么做的，`boost::scoped_ptr<T>` 基本上等价于`const std::auto_ptr<T>`
（当然，`const std::auto_ptr<T>`不能执行`reset`），之所以叫`scoped_ptr`是因为这个类强调它的作用只是**RAII**

其次，`auto_ptr`最初的目的是帮助程序员管理对象的所有权，它期望用户完全明白它的行为与内部实现（这也是C++被人诟病的地方）。

最后，C++11起，有了移动语义，有了`std::unique_ptr`，自然也就不需要`std::auto_ptr`了。
`std::auto_ptr`在C++11中被标记为弃用，在C++17中已经正式移除了。
