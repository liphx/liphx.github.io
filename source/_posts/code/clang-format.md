---
title: 使用clang-format格式化C++代码
date: 2023-08-11
updated:
tags: C++
permalink: code/clang-format/
---

0. clang-format文档

- <https://clang.llvm.org/docs/ClangFormat.html>
- <https://clang.llvm.org/docs/ClangFormatStyleOptions.html>

1. 查看预设的coding style

```
clang-format -style=google -dump-config
```

2. 设置项目的coding style

项目根目录下配置文件`.clang-format`

3. 代码风格

```
---
Language:                           Cpp
BasedOnStyle:                       Google
ColumnLimit:                        120
IndentWidth:                        4
AccessModifierOffset:               -4
ConstructorInitializerIndentWidth:  8
ContinuationIndentWidth:            8
PointerAlignment:                   Right
ReferenceAlignment:                 Left
DerivePointerAlignment:             false
IndentCaseLabels:                   false
AlignAfterOpenBracket:              DontAlign
```

基于Google的代码风格（最广泛使用的C++代码风格之一），有以下一些区别

- 列宽120，Google默认80
- 4空格缩进，Google默认2，访问控制符不缩进（`public, protected, private`）
- 同时设置`ConstructorInitializerIndentWidth, ContinuationIndentWidth`为8
   ```cpp
   class A {
   public:
       A(int x, int y)
               : x1234567890123456789_(x),
                 y1234567890123456789_(y) {
           if (x1234567890123456789_ > 0 &&
                   y1234567890123456789_ > 0) {
               ++x1234567890123456789_;
           }
       }

   private:
       int x1234567890123456789_;
       int y1234567890123456789_;
   };
   ```
  - 初始化列表多一次缩进以区别构造函数内的缩进
  - 续行多一次缩进以区别下一行的缩进
- 指针和引用的位置，指针在右边，引用在左边（纯个人偏好）
  ```cpp
  int *fn(const int& a, int *b);
  ```
- `case`不缩进
  ```cpp
  switch (n) {
  case 0:
      break;
  default:
      break;
  }
  ```
- 开括号后不对齐
  对齐的效果如下
  ```cpp
  void func(int varvarvarvar0,
            int varvarvarvar1,
            int& varvarvarvar2) {
      if (varvarvarvar0 > 0 &&
          varvarvarvar1 > 0) {
          varvarvarvar2++;
      }
  }
  ```
  `if (`刚好4字符，与if内缩进相同，没有区分度
  不对齐（按ContinuationIndentWidth配置缩进）效果如下
  ```cpp
  void func(int varvarvarvar0,
          int varvarvarvar1,
          int& varvarvarvar2) {
      if (varvarvarvar0 > 0 &&
              varvarvarvar1 > 0) {
          varvarvarvar2++;
      }
  }
  ```

4. 某些代码段不想格式化

```cpp
// clang-format off
这段代码不会格式化
// clang-format on
```
