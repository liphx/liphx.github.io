# Memory Allocation

## process memory layout

```
            Kernel

            argv, environ

            Stack

                    <-- Program break
            Heap

            Uninitialized data(bss)

            Initialized data

            Text(program code)
0x00000000
```

## `brk, sbrk`

```c
#include <unistd.h>

int brk(void *end_data_segment);
// Returns 0 on success, or –1 on error

void *sbrk(intptr_t increment);
// Returns previous program break on success, or (void *) –1 on error
```

由于虚拟内存以页为单位进行分配，`end_data_segment` 实际会四舍五入到下一个内存页的边界处。

sbrk(0)将返回 program break 的当前位置。

## `alloca`

```c
#include <alloca.h>
void *alloca(size_t size);
// allocates size bytes of space in the stack frame of the caller
```

## `malloc, calloc, realloc, free`

```c
void* malloc(size_t size);
void* calloc(size_t num, size_t size);
void *realloc(void *ptr, size_t new_size);
void free(void* ptr);
```

`malloc(0)`: implementation-defined, may not be NULL
