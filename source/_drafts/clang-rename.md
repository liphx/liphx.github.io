```cpp
#include <iostream>

namespace a {

struct A {
    int a;
    A(int a = 42) : a(a) {}
};

}  // namespace a

int main() {
    a::A a;
    std::cout << a.a << std::endl;
}
```

```shell
$ clang-rename --qualified-name=a::A::a --new-name=a_ main.cc
#include <iostream>

namespace a {

struct A {
    int a_;
    A(int a = 42) : a_(a) {}
};

}  // namespace a

int main() {
    a::A a;
    std::cout << a.a_ << std::endl;
}
```
