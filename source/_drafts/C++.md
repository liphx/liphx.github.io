- <https://github.com/xiaoweiChen/CPP-Concurrency-In-Action-2ed-2019>

clang-tidy

- https://clang.llvm.org/extra/clang-tidy/
- https://github.com/llvm/llvm-project/releases

flare
https://techmap.woa.com/project/22243
https://github.com/Tencent/flare

| 缩写 | 含义            |
| ---- | --------------- |
| lhs  | left hand side  |
| rhs  | right hand side |
| aux  | auxiliary       |
| std  | standred        |

检查未使用的返回值

1.  `__attribute__ ((warn_unused_result))`

   `gcc -Wunused-result`

   https://gcc.gnu.org/onlinedocs/gcc-4.9.2/gcc/Function-Attributes.html

2. clang-tidy

   https://clang.llvm.org/extra/clang-tidy/checks/bugprone/unused-return-value.html

1. 创建一个线程需要消耗多少资源


https://stackoverflow.com/questions/56497350/thread-guard-vs-scoped-thread

- lock_guard
- unique_lock

libevent
```shell
./configure PKG_CONFIG_PATH=/usr/local/Cellar/openssl@3/3.0.0_1/lib/pkgconfig
make
ls .libs/
./sample/hello-world
netcat 127.0.0.1 9995
```