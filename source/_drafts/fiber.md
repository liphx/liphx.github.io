---
title: fiber
---

https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2014/n4024.pdf
Distinguishing coroutines and fibers

fiber: user-space thread(context switching in user space)
  - Multiple conceptually-independent fibers can run on the same kernel thread
  - Two fibers on the same kernel thread will not run simultaneously on different processor cores

like thread
  - fiber-local storage
  - fiber mutex
  - condition_variable
  - barrier
  - future, shared_future, promise, packaged_task

fiber: cooperative context switching
thread: preemptive time-slicing

work-stealing and continuation-stealing

------------

https://www.boost.org/doc/libs/1_82_0/libs/fiber/doc/html/index.html
Boost.Fiber

------------

https://github.com/Tencent/flare/blob/master/flare/doc/fiber.md
flare.Fiber

