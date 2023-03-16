---
title: C/C++ AddressSanitizer Examples
date: 2023-08-11
tags: cplusplus
---

<https://github.com/google/sanitizers/wiki/AddressSanitizer>

## heap-use-after-free

```shell
$ cat heap-use-after-free.cpp 
#include <iostream>

int main() {
    int *p = new int;
    delete p;
    std::cout << *p << std::endl;
}
$ g++ -fsanitize=address -O1 -fno-omit-frame-pointer -g heap-use-after-free.cpp && ./a.out
=================================================================
==40665==ERROR: AddressSanitizer: heap-use-after-free on address 0x602000000010 at pc 0x56530f385261 bp 0x7fffdf2b04e0 sp 0x7fffdf2b04d8
READ of size 4 at 0x602000000010 thread T0
    #0 0x56530f385260 in main /tmp/asan/heap-use-after-free.cpp:6
    #1 0x7f1065e39d09 in __libc_start_main ../csu/libc-start.c:308
    #2 0x56530f385139 in _start (/tmp/asan/a.out+0x1139)

0x602000000010 is located 0 bytes inside of 4-byte region [0x602000000010,0x602000000014)
freed by thread T0 here:
    #0 0x7f1066264467 in operator delete(void*, unsigned long) ../../../../src/libsanitizer/asan/asan_new_delete.cpp:172
    #1 0x56530f385217 in main /tmp/asan/heap-use-after-free.cpp:5
    #2 0x7f1065e39d09 in __libc_start_main ../csu/libc-start.c:308

previously allocated by thread T0 here:
    #0 0x7f1066263647 in operator new(unsigned long) ../../../../src/libsanitizer/asan/asan_new_delete.cpp:99
    #1 0x56530f385207 in main /tmp/asan/heap-use-after-free.cpp:4
    #2 0x7f1065e39d09 in __libc_start_main ../csu/libc-start.c:308

SUMMARY: AddressSanitizer: heap-use-after-free /tmp/asan/heap-use-after-free.cpp:6 in main
Shadow bytes around the buggy address:
  0x0c047fff7fb0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0c047fff7fc0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0c047fff7fd0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0c047fff7fe0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0c047fff7ff0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x0c047fff8000: fa fa[fd]fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c047fff8010: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c047fff8020: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c047fff8030: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c047fff8040: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c047fff8050: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
Shadow byte legend (one shadow byte represents 8 application bytes):
  Addressable:           00
  Partially addressable: 01 02 03 04 05 06 07 
  Heap left redzone:       fa
  Freed heap region:       fd
  Stack left redzone:      f1
  Stack mid redzone:       f2
  Stack right redzone:     f3
  Stack after return:      f5
  Stack use after scope:   f8
  Global redzone:          f9
  Global init order:       f6
  Poisoned by user:        f7
  Container overflow:      fc
  Array cookie:            ac
  Intra object redzone:    bb
  ASan internal:           fe
  Left alloca redzone:     ca
  Right alloca redzone:    cb
  Shadow gap:              cc
==40665==ABORTING
```

## heap-buffer-overflow

```shell
$ cat heap-buffer-overflow.cpp 
#include <iostream>

int main() {
    int *p = new int[100];
    std::cout << p[100] << std::endl;
    delete[] p;
}
$ g++ -fsanitize=address -O1 -fno-omit-frame-pointer -g heap-buffer-overflow.cpp && ./a.out 
=================================================================
==40692==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x6140000001d0 at pc 0x556801de6264 bp 0x7fff73c2bff0 sp 0x7fff73c2bfe8
READ of size 4 at 0x6140000001d0 thread T0
    #0 0x556801de6263 in main /tmp/asan/heap-buffer-overflow.cpp:5
    #1 0x7f8cdaee0d09 in __libc_start_main ../csu/libc-start.c:308
    #2 0x556801de6139 in _start (/tmp/asan/a.out+0x1139)

0x6140000001d0 is located 0 bytes to the right of 400-byte region [0x614000000040,0x6140000001d0)
allocated by thread T0 here:
    #0 0x7f8cdb30a7a7 in operator new[](unsigned long) ../../../../src/libsanitizer/asan/asan_new_delete.cpp:102
    #1 0x556801de6207 in main /tmp/asan/heap-buffer-overflow.cpp:4
    #2 0x7f8cdaee0d09 in __libc_start_main ../csu/libc-start.c:308

SUMMARY: AddressSanitizer: heap-buffer-overflow /tmp/asan/heap-buffer-overflow.cpp:5 in main
Shadow bytes around the buggy address:
  0x0c287fff7fe0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0c287fff7ff0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0c287fff8000: fa fa fa fa fa fa fa fa 00 00 00 00 00 00 00 00
  0x0c287fff8010: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0c287fff8020: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x0c287fff8030: 00 00 00 00 00 00 00 00 00 00[fa]fa fa fa fa fa
  0x0c287fff8040: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c287fff8050: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c287fff8060: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c287fff8070: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c287fff8080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
Shadow byte legend (one shadow byte represents 8 application bytes):
  Addressable:           00
  Partially addressable: 01 02 03 04 05 06 07 
  Heap left redzone:       fa
  Freed heap region:       fd
  Stack left redzone:      f1
  Stack mid redzone:       f2
  Stack right redzone:     f3
  Stack after return:      f5
  Stack use after scope:   f8
  Global redzone:          f9
  Global init order:       f6
  Poisoned by user:        f7
  Container overflow:      fc
  Array cookie:            ac
  Intra object redzone:    bb
  ASan internal:           fe
  Left alloca redzone:     ca
  Right alloca redzone:    cb
  Shadow gap:              cc
==40692==ABORTING
```

## stack-buffer-overflow

```shell
$ cat stack-buffer-overflow.cpp 
#include <iostream>

int main() {
    int p[100];
    std::cout << p[100] << std::endl;
}
$ g++ -fsanitize=address -O1 -fno-omit-frame-pointer -g stack-buffer-overflow.cpp && ./a.out 
=================================================================
==40707==ERROR: AddressSanitizer: stack-buffer-overflow on address 0x7ffe28541820 at pc 0x56152e4b32e6 bp 0x7ffe28541650 sp 0x7ffe28541648
READ of size 4 at 0x7ffe28541820 thread T0
    #0 0x56152e4b32e5 in main /tmp/asan/stack-buffer-overflow.cpp:5
    #1 0x7fb19a22dd09 in __libc_start_main ../csu/libc-start.c:308
    #2 0x56152e4b3129 in _start (/tmp/asan/a.out+0x1129)

Address 0x7ffe28541820 is located in stack of thread T0 at offset 448 in frame
    #0 0x56152e4b31f4 in main /tmp/asan/stack-buffer-overflow.cpp:3

  This frame has 1 object(s):
    [48, 448) 'p' (line 4) <== Memory access at offset 448 overflows this variable
HINT: this may be a false positive if your program uses some custom stack unwind mechanism, swapcontext or vfork
      (longjmp and C++ exceptions *are* supported)
SUMMARY: AddressSanitizer: stack-buffer-overflow /tmp/asan/stack-buffer-overflow.cpp:5 in main
Shadow bytes around the buggy address:
  0x1000450a02b0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x1000450a02c0: 00 00 00 00 00 00 00 00 00 00 00 00 f1 f1 f1 f1
  0x1000450a02d0: f1 f1 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x1000450a02e0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x1000450a02f0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x1000450a0300: 00 00 00 00[f3]f3 f3 f3 f3 f3 f3 f3 00 00 00 00
  0x1000450a0310: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x1000450a0320: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x1000450a0330: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x1000450a0340: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x1000450a0350: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
Shadow byte legend (one shadow byte represents 8 application bytes):
  Addressable:           00
  Partially addressable: 01 02 03 04 05 06 07 
  Heap left redzone:       fa
  Freed heap region:       fd
  Stack left redzone:      f1
  Stack mid redzone:       f2
  Stack right redzone:     f3
  Stack after return:      f5
  Stack use after scope:   f8
  Global redzone:          f9
  Global init order:       f6
  Poisoned by user:        f7
  Container overflow:      fc
  Array cookie:            ac
  Intra object redzone:    bb
  ASan internal:           fe
  Left alloca redzone:     ca
  Right alloca redzone:    cb
  Shadow gap:              cc
==40707==ABORTING
```

## global-buffer-overflow

```shell
$ cat global-buffer-overflow.cpp 
#include <iostream>

int p[100];

int main() {
    std::cout << p[100] << std::endl;
}
$ g++ -fsanitize=address -O1 -fno-omit-frame-pointer -g global-buffer-overflow.cpp && ./a.out 
=================================================================
==40722==ERROR: AddressSanitizer: global-buffer-overflow on address 0x5582a8be53f0 at pc 0x5582a8be221c bp 0x7fffb9c61fb0 sp 0x7fffb9c61fa8
READ of size 4 at 0x5582a8be53f0 thread T0
    #0 0x5582a8be221b in main /tmp/asan/global-buffer-overflow.cpp:6
    #1 0x7f933e583d09 in __libc_start_main ../csu/libc-start.c:308
    #2 0x5582a8be2119 in _start (/tmp/asan/a.out+0x1119)

0x5582a8be53f0 is located 48 bytes to the left of global variable '__ioinit' defined in '/usr/include/c++/10/iostream:74:25' (0x5582a8be5420) of size 1
  '__ioinit' is ascii string ''
0x5582a8be53f0 is located 0 bytes to the right of global variable 'p' defined in 'global-buffer-overflow.cpp:3:5' (0x5582a8be5260) of size 400
SUMMARY: AddressSanitizer: global-buffer-overflow /tmp/asan/global-buffer-overflow.cpp:6 in main
Shadow bytes around the buggy address:
  0x0ab0d5174a20: f9 f9 f9 f9 f9 f9 f9 f9 00 00 00 00 00 00 00 00
  0x0ab0d5174a30: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0ab0d5174a40: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0ab0d5174a50: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0ab0d5174a60: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x0ab0d5174a70: 00 00 00 00 00 00 00 00 00 00 00 00 00 00[f9]f9
  0x0ab0d5174a80: f9 f9 f9 f9 01 f9 f9 f9 f9 f9 f9 f9 00 00 00 00
  0x0ab0d5174a90: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0ab0d5174aa0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0ab0d5174ab0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0ab0d5174ac0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
Shadow byte legend (one shadow byte represents 8 application bytes):
  Addressable:           00
  Partially addressable: 01 02 03 04 05 06 07 
  Heap left redzone:       fa
  Freed heap region:       fd
  Stack left redzone:      f1
  Stack mid redzone:       f2
  Stack right redzone:     f3
  Stack after return:      f5
  Stack use after scope:   f8
  Global redzone:          f9
  Global init order:       f6
  Poisoned by user:        f7
  Container overflow:      fc
  Array cookie:            ac
  Intra object redzone:    bb
  ASan internal:           fe
  Left alloca redzone:     ca
  Right alloca redzone:    cb
  Shadow gap:              cc
==40722==ABORTING
```

## stack-use-after-scope

```shell
$ cat stack-use-after-scope.cpp 
#include <iostream>

int *p;

void f() {
    int i;
    p = &i;
}

int main() {
    f();
    std::cout << *p << std::endl;
}
$ g++ -fsanitize=address -O1 -fno-omit-frame-pointer -g stack-use-after-scope.cpp && ./a.out 
=================================================================
==40835==ERROR: AddressSanitizer: stack-use-after-scope on address 0x7ffd94a68c00 at pc 0x56052611637b bp 0x7ffd94a68bd0 sp 0x7ffd94a68bc8
READ of size 4 at 0x7ffd94a68c00 thread T0
    #0 0x56052611637a in main /tmp/asan/stack-use-after-scope.cpp:12
    #1 0x7fef44c4dd09 in __libc_start_main ../csu/libc-start.c:308
    #2 0x560526116129 in _start (/tmp/asan/a.out+0x1129)

Address 0x7ffd94a68c00 is located in stack of thread T0 at offset 32 in frame
    #0 0x56052611629f in main /tmp/asan/stack-use-after-scope.cpp:10

  This frame has 1 object(s):
    [32, 36) 'i' (line 6) <== Memory access at offset 32 is inside this variable
HINT: this may be a false positive if your program uses some custom stack unwind mechanism, swapcontext or vfork
      (longjmp and C++ exceptions *are* supported)
SUMMARY: AddressSanitizer: stack-use-after-scope /tmp/asan/stack-use-after-scope.cpp:12 in main
Shadow bytes around the buggy address:
  0x100032945130: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x100032945140: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x100032945150: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x100032945160: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x100032945170: 00 00 00 00 00 00 00 00 00 00 00 00 f1 f1 f1 f1
=>0x100032945180:[f8]f3 f3 f3 00 00 00 00 00 00 00 00 00 00 00 00
  0x100032945190: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x1000329451a0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x1000329451b0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x1000329451c0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x1000329451d0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
Shadow byte legend (one shadow byte represents 8 application bytes):
  Addressable:           00
  Partially addressable: 01 02 03 04 05 06 07 
  Heap left redzone:       fa
  Freed heap region:       fd
  Stack left redzone:      f1
  Stack mid redzone:       f2
  Stack right redzone:     f3
  Stack after return:      f5
  Stack use after scope:   f8
  Global redzone:          f9
  Global init order:       f6
  Poisoned by user:        f7
  Container overflow:      fc
  Array cookie:            ac
  Intra object redzone:    bb
  ASan internal:           fe
  Left alloca redzone:     ca
  Right alloca redzone:    cb
  Shadow gap:              cc
==40835==ABORTING
```

## stack-use-after-return

```shell
$ cat stack-use-after-return.cpp 
#include <iostream>

int *p;

void f() {
    int i[100];
    p = &i[0];
}

int main() {
    f();
    std::cout << *p << std::endl;
}
$ g++ -fsanitize=address -O1 -fno-omit-frame-pointer -g stack-use-after-return.cpp && ASAN_OPTIONS=detect_stack_use_after_return=1 ./a.out 
=================================================================
==40871==ERROR: AddressSanitizer: stack-use-after-return on address 0x7f0c3a630030 at pc 0x562cdb120340 bp 0x7ffe757b4230 sp 0x7ffe757b4228
READ of size 4 at 0x7f0c3a630030 thread T0
    #0 0x562cdb12033f in main /tmp/asan/stack-use-after-return.cpp:12
    #1 0x7f0c3db4cd09 in __libc_start_main ../csu/libc-start.c:308
    #2 0x562cdb120129 in _start (/tmp/asan/a.out+0x1129)

Address 0x7f0c3a630030 is located in stack of thread T0 at offset 48 in frame
    #0 0x562cdb1201f4 in f() /tmp/asan/stack-use-after-return.cpp:5

  This frame has 1 object(s):
    [48, 448) 'i' (line 6) <== Memory access at offset 48 is inside this variable
HINT: this may be a false positive if your program uses some custom stack unwind mechanism, swapcontext or vfork
      (longjmp and C++ exceptions *are* supported)
SUMMARY: AddressSanitizer: stack-use-after-return /tmp/asan/stack-use-after-return.cpp:12 in main
Shadow bytes around the buggy address:
  0x0fe2074bdfb0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0fe2074bdfc0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0fe2074bdfd0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0fe2074bdfe0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0fe2074bdff0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x0fe2074be000: f5 f5 f5 f5 f5 f5[f5]f5 f5 f5 f5 f5 f5 f5 f5 f5
  0x0fe2074be010: f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5
  0x0fe2074be020: f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5
  0x0fe2074be030: f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5
  0x0fe2074be040: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0fe2074be050: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
Shadow byte legend (one shadow byte represents 8 application bytes):
  Addressable:           00
  Partially addressable: 01 02 03 04 05 06 07 
  Heap left redzone:       fa
  Freed heap region:       fd
  Stack left redzone:      f1
  Stack mid redzone:       f2
  Stack right redzone:     f3
  Stack after return:      f5
  Stack use after scope:   f8
  Global redzone:          f9
  Global init order:       f6
  Poisoned by user:        f7
  Container overflow:      fc
  Array cookie:            ac
  Intra object redzone:    bb
  ASan internal:           fe
  Left alloca redzone:     ca
  Right alloca redzone:    cb
  Shadow gap:              cc
==40871==ABORTING
```

## initialization-order-fiasco

[example](non-local-static.html)

```shell
$ alias g++='g++ -fsanitize=address -O1 -fno-omit-frame-pointer -g'
$ g++ A.cpp B.cpp && ASAN_OPTIONS=check_initialization_order=true ./a.out 
A(100)
B()
100
$ g++ B.cpp A.cpp && ASAN_OPTIONS=check_initialization_order=true ./a.out 
B()
=================================================================
==40909==ERROR: AddressSanitizer: initialization-order-fiasco on address 0x5622ccb774c0 at pc 0x5622ccb74507 bp 0x7fff6b58ca00 sp 0x7fff6b58c9f8
READ of size 4 at 0x5622ccb774c0 thread T0
    #0 0x5622ccb74506 in A::f() /tmp/asan/A.h:6
    #1 0x5622ccb74506 in B::B() /tmp/asan/B.cpp:7
    #2 0x5622ccb74506 in __static_initialization_and_destruction_0 /tmp/asan/B.cpp:10
    #3 0x5622ccb74506 in _GLOBAL__sub_I_b /tmp/asan/B.cpp:11
    #4 0x5622ccb74854 in __libc_csu_init (/tmp/asan/a.out+0x1854)
    #5 0x7fc91ca41c99 in __libc_start_main ../csu/libc-start.c:264
    #6 0x5622ccb74199 in _start (/tmp/asan/a.out+0x1199)

0x5622ccb774c0 is located 0 bytes inside of global variable 'a' defined in 'A.cpp:3:3' (0x5622ccb774c0) of size 4
  registered at:
    #0 0x7fc91cdf6f40 in __asan_register_globals ../../../../src/libsanitizer/asan/asan_globals.cpp:341
    #1 0x5622ccb74807 in _sub_I_00099_1 (/tmp/asan/a.out+0x1807)
    #2 0x5622ccb74854 in __libc_csu_init (/tmp/asan/a.out+0x1854)

SUMMARY: AddressSanitizer: initialization-order-fiasco /tmp/asan/A.h:6 in A::f()
Shadow bytes around the buggy address:
  0x0ac4d9966e40: f9 f9 f9 f9 f9 f9 f9 f9 f9 f9 f9 f9 f9 f9 f9 f9
  0x0ac4d9966e50: f9 f9 f9 f9 f9 f9 f9 f9 f9 f9 f9 f9 00 00 00 00
  0x0ac4d9966e60: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0ac4d9966e70: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0ac4d9966e80: 00 00 00 00 01 f9 f9 f9 f9 f9 f9 f9 01 f9 f9 f9
=>0x0ac4d9966e90: f9 f9 f9 f9 00 00 00 00[f6]f6 f6 f6 f6 f6 f6 f6
  0x0ac4d9966ea0: f6 f6 f6 f6 f6 f6 f6 f6 00 00 00 00 00 00 00 00
  0x0ac4d9966eb0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0ac4d9966ec0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0ac4d9966ed0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0ac4d9966ee0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
Shadow byte legend (one shadow byte represents 8 application bytes):
  Addressable:           00
  Partially addressable: 01 02 03 04 05 06 07 
  Heap left redzone:       fa
  Freed heap region:       fd
  Stack left redzone:      f1
  Stack mid redzone:       f2
  Stack right redzone:     f3
  Stack after return:      f5
  Stack use after scope:   f8
  Global redzone:          f9
  Global init order:       f6
  Poisoned by user:        f7
  Container overflow:      fc
  Array cookie:            ac
  Intra object redzone:    bb
  ASan internal:           fe
  Left alloca redzone:     ca
  Right alloca redzone:    cb
  Shadow gap:              cc
==40909==ABORTING
```

## memory-leaks

```shell
$ cat memory-leaks.cpp 
int main() {
    new int;
}
$ g++ memory-leaks.cpp -fsanitize=address && ./a.out 

=================================================================
==41013==ERROR: LeakSanitizer: detected memory leaks

Direct leak of 4 byte(s) in 1 object(s) allocated from:
    #0 0x7f5dd4590647 in operator new(unsigned long) ../../../../src/libsanitizer/asan/asan_new_delete.cpp:99
    #1 0x55df72344162 in main (/tmp/asan/a.out+0x1162)
    #2 0x7f5dd4333d09 in __libc_start_main ../csu/libc-start.c:308

SUMMARY: AddressSanitizer: 4 byte(s) leaked in 1 allocation(s).
```

## sanitize-recover

```shell
$ cat sanitize-recover.cpp 
#include <iostream>

int main() {
    int *p = new int;
    delete p;
    delete p;
    std::cout << "here" << std::endl;
}
$ g++ -fsanitize=address -fsanitize-recover=address sanitize-recover.cpp 
$ ASAN_OPTIONS=halt_on_error=0:log_path=asan.log ./a.out
here
$ cat asan.log.41106 
=================================================================
==41106==ERROR: AddressSanitizer: attempting double-free on 0x602000000010 in thread T0:
    #0 0x7f13c4942467 in operator delete(void*, unsigned long) ../../../../src/libsanitizer/asan/asan_new_delete.cpp:172
    #1 0x55ca1580f226 in main (/tmp/asan/a.out+0x1226)
    #2 0x7f13c4517d09 in __libc_start_main ../csu/libc-start.c:308
    #3 0x55ca1580f129 in _start (/tmp/asan/a.out+0x1129)

0x602000000010 is located 0 bytes inside of 4-byte region [0x602000000010,0x602000000014)
freed by thread T0 here:
    #0 0x7f13c4942467 in operator delete(void*, unsigned long) ../../../../src/libsanitizer/asan/asan_new_delete.cpp:172
    #1 0x55ca1580f210 in main (/tmp/asan/a.out+0x1210)
    #2 0x7f13c4517d09 in __libc_start_main ../csu/libc-start.c:308

previously allocated by thread T0 here:
    #0 0x7f13c4941647 in operator new(unsigned long) ../../../../src/libsanitizer/asan/asan_new_delete.cpp:99
    #1 0x55ca1580f1f6 in main (/tmp/asan/a.out+0x11f6)
    #2 0x7f13c4517d09 in __libc_start_main ../csu/libc-start.c:308

SUMMARY: AddressSanitizer: double-free ../../../../src/libsanitizer/asan/asan_new_delete.cpp:172 in operator delete(void*, unsigned long)
```
