---
title: std::thread, std::async 中的异常
date: 2023-08-11
tags: C++
permalink: code/thread-async/
---

```cpp
#include <future>
#include <iostream>
#include <stdexcept>

int fn(int n) {
    if (n < 1) throw std::invalid_argument("n < 1");
    if (n < 3) return 1;
    return fn(n - 1) + fn(n - 2);
}

int main() {
    try {
        auto fut = std::async(fn, 20);
        std::cout << std::boolalpha;
        int res = fut.get();
        std::cout << "fn(20) = " << res << std::endl;
        auto fut2 = std::async(fn, -20);
        res = fut2.get();
        std::cout << "fn(-20) = " << res << std::endl;
    } catch (const std::invalid_argument& e) {
        std::cerr << e.what() << std::endl;
    }

    try {
        std::thread t(fn, -20);
        t.join();
    } catch (const std::invalid_argument& e) {  // can not catch
        std::cerr << e.what() << std::endl;
    }
}
```

可以看到，不能捕获`std::thread`中抛出的异常。但`std::async`可以通过`std::promise/std::future`设置/捕获异常。

另外，`std::async`未必真的异步，如有必要可以指定`std::launch::async`

```cpp
template <typename F, typename... Ts>
inline std::future<typename std::result_of<F(Ts...)>::type> reallyAsync(F&& f, Ts&&...params) {
    return std::async(std::launch::async, std::forward<F>(f), std::forward<Ts>(params)...);
}

// C++14
template <typename F, typename... Ts>
inline auto reallyAsync(F&& f, Ts&&...params) {
    return std::async(std::launch::async, std::forward<F>(f), std::forward<Ts>(params)...);
}
```
