## CMake

一些链接

* <https://cmake.org/>
* <https://github.com/Kitware/CMake/>

一些书籍

<http://cliutils.gitlab.io/modern-cmake/>

### 安装（升级）cmake

Debian stable 10.7, apt 源里的cmake 版本是3.13.4, 最新CMake(2021-2-2) 已经发布了 3.19.4版本。由于我的系统已经不满足不少项目里指定的`cmake_minimum_required`， 因此我需要更新一下Cmake。

最新的cmake 可以在 <https://cmake.org/download/> 获取，实际上它的下载链接指向 github Releases 页面。下载页面有二进制和源代码版本，我打算从源代码安装。

```shell
$ wget https://github.com/Kitware/CMake/releases/download/v3.19.4/cmake-3.19.4.tar.gz
$ sudo tar xvf cmake-3.19.4.tar.gz -C /opt
$ cd /opt/cmake-3.19.4/
$ sudo ./configure
$ sudo make
$ echo 'export PATH=/opt/cmake-3.19.4/bin:$PATH' >> ~/.profile
$ source ~/.profile
$ cmake --version
cmake version 3.19.4

CMake suite maintained and supported by Kitware (kitware.com/cmake).
```

3.19 版本的参考文档可以在 <https://cmake.org/cmake/help/v3.19/> 获取。

### 使用

正如使用tarball 编译软件的经典步骤`./configure && make && make install` 一样，使用cmake 构建项目也有经典的步骤

```shell
mkdir build
cd build
cmake ..
make
```

或者使用

```shell
cmake -S . -B build
cmake --build build
```

这些选项都可以通过`cmake --help` 获取，使用后者的好处是不用频繁切换目录

### 简单的例子

hello 目录下两个文件，`hello.c` 以及 `CMakeLists.txt`

```c
#include <stdio.h>

int main() {
    printf("hello, world\n");
    return 0;
}
```

```cmake
cmake_minimum_required(VERSION 3.13)

project(hello)

add_executable(hello hello.c)
```

执行 `cmake -S . -B build` 指定源代码目录与构建目录，终端会输出编译器与系统信息

再执行 `cmake --build build` 则会进行编译步骤，同时会输出编译信息

现在来看文件`CMakeLists.txt`

* `cmake_minimum_required` 指定了构建需要的cmake 的最低版本
* `project` 指定项目名称
* `add_executable` 生成可执行文件

再来看一个构建库的例子

文件 `add.c` 以及 `CMakeLists.txt`

```c
int add(int x, int y) {
    return x + y;
}
```

```cmake
project(math)

add_library(math SHARED add.c)
```

构建完成会生成`libmath.so`，`add_library` 不加`SHARED`或指定`STATIC` 则会构建静态库 `libmath.a`

`CMakeLists.txt` 里的指令是大小写不敏感的

### 另一个例子

```
.
|-- CMakeLists.txt
|-- hello.cpp
|-- hello.h.in
`-- mylib
    |-- add.cpp
    |-- add.h
    `-- CMakeLists.txt
```

顶层 `CMakeLists.txt`

```cmake
# cmake minimum version
cmake_minimum_required(VERSION 3.13)

# set the project name and version
project(hello   VERSION 1.0
                DESCRIPTION "A simple project")

# specify the C++ standard
set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED True)

configure_file(hello.h.in hello.h)

add_subdirectory(mylib)

add_executable(hello hello.cpp)

target_link_libraries(hello PUBLIC mylib)

target_include_directories(hello PUBLIC
                          "${PROJECT_BINARY_DIR}"
                          "${PROJECT_SOURCE_DIR}/mylib"
                        )
```

`hello.h.in`

```c
#ifndef HELLO_H_
#define HELLO_H_

#define HELLO_VERSION_MAJOR @hello_VERSION_MAJOR@
#define HELLO_VERSION_MINOR @hello_VERSION_MINOR@

#endif // HELLO_H_
```

`hello.cpp`

```cpp
#include "hello.h"
#include "add.h"
#include <cstdio>

int main(int argc, char *argv[]) {
    printf("hello version: %d.%d\n", HELLO_VERSION_MAJOR, HELLO_VERSION_MINOR);
    printf("add(1, 2) = %d\n", add(1, 2));
}
```

`mylib/CMakeLists.txt`

```cmake
add_library(mylib add.cpp)
```

