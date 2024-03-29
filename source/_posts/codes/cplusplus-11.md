---
title: C++11速览
date: 2023-08-11
tags: cplusplus
---

## 1 nullptr

空指针字面量，强类型`std::nullptr_t`，可以隐式转换为任何指针类型。

```cpp
#ifndef __cplusplus
#define NULL ((void *)0)
#else   /* C++ */
#define NULL 0
#endif
```

C++中，NULL 是字面量 0，而不是`(void *)0`

```cpp
class A{};

int main() {
    A *p1 = nullptr;
    A *p2 = NULL;
    A *p3 = 0;
    // A *p4 = (void *)0;
    // error: cannot initialize a variable of type 'A *' with an rvalue of type 'void *'
}
```

C++中，NULL是为兼容C代码而定义的，C++11前，C++代码推荐使用0代替NULL（0即是空值，false，空指针）。
C++代码中大量使用NULL，一方面是习惯，另一方面NULL比0更方便阅读，让人看上去就知道变量、参数是指针类型。

```cpp
this->ptr = 0;
this->ptr = NULL;

func(0, 0);
func(0, NULL);
```

C++98/03中，模板函数调用时，0作为无类型值，无法进行类型推导（往往当成int）。C++11新增`nullptr`就是为了更好地支持泛型（模板）。

```cpp
#include <cstddef>

template <class T>
constexpr T clone(const T& t) {
    return t;
}

void g(int *) {}

int main() {
    g(nullptr);
    g(NULL);
    g(0);

    g(clone(nullptr));
    // g(clone(NULL));
    // g(clone(0));
    // error: no matching function for call to 'g'
    // candidate function not viable: no known conversion from 'int' to 'int *' for 1st argument
}
```

作为强类型的`nullptr`还可以解决如下二义性问题

```cpp
#include <cstddef>
#include <iostream>

void f(int *) { std::cout << "f(int *) called." << std::endl; }
void f(int) { std::cout << "f(int) called." << std::endl; }

void g(char *) { std::cout << "g(char *) called." << std::endl; }
void g(char) { std::cout << "g(char) called." << std::endl; }

int main() {
    f(nullptr);  // f(int *) called.
    f(0);        // f(int) called.
    // f(NULL); error: call to 'f' is ambiguous
    // assert(typeid(long) == typeid(NULL));

    g(nullptr);  // g(char *) called.
    // g(0);    error: call to 'g' is ambiguous
    // g(NULL); error: call to 'g' is ambiguous
}
```

总结：C++11后，使用强类型的`nullptr`替代`NULL/0`;

## 2 initialization/std::initializer_list

```cpp
#include <cstddef>
#include <iostream>

class A {
public:
    A() : p(nullptr) {}
    A(int) : p(nullptr) {}
    A(long) : p{nullptr} {}  // c++11
    A(double) : A() {}       // delegating constructors, c++11
private:
    char *p;
};

class A2 {
private:
    char *p = nullptr;  // c++11
    char *p2{nullptr};  // c++11
    // char *p3(nullptr); // error
};

int main() {
    int i1(0);
    int i2 = 0;
    int i3{0};             // c++11
    int *pi = new int{0};  // c++11
    A a{0};                // c++11

    std::atomic<int> ai1{0};
    std::atomic<int> ai2(0);
    // std::atomic<int> ai3 = 0;
    // error in c++11, atomic(const atomic&) = delete;
}
```

总结: C++11后新的初始化方式使代码更简洁，统一。

## 3 auto/decltype

auto在C++11前就是一个关键字, 变量前加auto(或不加)表示自动存储期, C++11起用作自动类型推导。

C++11里auto用于推导变量的类型, C++14里可以推导函数返回类型, 其规则同模板实参推导规则。

```cpp
{
    auto x = 0;  // int
}
{
    auto x = 0u;  // unsigned int
}
{
    auto x{0};  // int
}
{
    // auto x{0, 1};
    // error: initializer for variable 'x' with type 'auto' contains multiple expressions
}
{
    auto x = {0};  // std::initializer_list<int>
}
{
    const auto& x = 0;  // const int&
}
{
    std::map<int, int> map;
    for (auto x : map) {
    }  // std::pair<const int, int>

    for (auto& x : map) {
    }  // &

    for (const auto& x : map) {
    }  // const std::pair<const int, int>&

    map<string, int> map2;
    for (const std::pair<std::string, int>& kv : map2) ;       // copy
    for (const std::pair<const std::string, int>& kv : map2) ;
    for (const auto& kv : map2) ;
}
{
    // c++17
    std::map<std::string, int> data{{"abc", 1}, {"bcd", 2}};
    for (const auto& [k, v] : data) {
        std::cout << k << ": " << v << std::endl;
    }
}
{
    auto x = new int{0};
    // int *
}
{
    auto *x = new int{0};
    // int *
}

{
    // auto x = 1, y = 2.0;
    // error: 'auto' deduced as 'int' in declaration of 'x' and deduced as 'double' in declaration of 'y'
}

{
    int x{0};
    int& y = x;
    auto z = y;  // int, not int&
}

{
    const int x{0};
    volatile int y{0};
    auto z1 = x;  // int, not const int
    auto z2 = x;  // int, not volatile int
}
{
    const int x{0};
    auto& y = x;  // const int&
}
{
    int x[]{0, 1, 2};
    auto y = x;  // int *, not int[3]
}
{
    int x[]{0, 1, 2};
    auto& y = x;  // int[3]
}
```

```cpp
void f() {}

template <typename T, typename U>
auto add(T t, U u) -> decltype(t + u) {
    return t + u;
}

int main() {
    int x{0};
    decltype(x) y;  // int

    decltype(f) func;  // void ()

    decltype(0.1) f;  // double

    auto g = [](int a, int b) { return a + b; };
    decltype(g) func2 = g;                  // lambda
    std::cout << func2(1, 2) << std::endl;  // 3

    const int i{0};
    decltype(i) j = i;  // const int

    int a{0};
    int& b = a;
    decltype(b) c = a;  // int&

    auto ret = add(1.0, 2.1);  // double
}
```

总结: auto/decltype 有助于简化代码, 但细节很多`(*, &, const, volatile)`, 将其理解为占位符而不是一种新类型。

## 4 lambda

Lambda 表达式: 可以捕获变量的匿名函数对象。

```cpp
std::vector<int> data(10);
std::generate(data.begin(), data.end(), [n = 0]() mutable { return n++; });
// 0 1 2 3 4 5 6 7 8 9

typedef void (*func)();

int main() {
    func f = []() { std::cout << "func1" << std::endl; };
    f();  // func1
    int x = 100;
    // func f2 = [x]() { std::cout << "func2, x = " << x << std::endl; };
    // error: no viable conversion from '(lambda)' to 'func' (aka 'void (*)()')
    std::function<void()> f2 = [x]() { std::cout << "func2, x = " << x << std::endl; };
    f2();  // func2, x = 100

    std::function<void()> f3 = std::bind([](int x) { std::cout << "func3, x = " << x << std::endl; }, 200);
    f3();  // func3, x = 200
}
```

总结：lambda可以简化代码，可以用来实现闭包（包括operator(), std::function, std::bind 等）。

## 5 Rvalue reference/std::move

5.1 左值/右值

一般而言，左值出现在等号左边，右值出现在等号右边，左值可以取地址，右值不能取地址。

```
a++             // 右值
++a             // 左值
&a              // r
a, b            // a是左值，b是右值
"hello"         // 字符串字面量，左值
nullptr 0 true  // 其他字面量，右值
this            // 右值
string()        // 右值
枚举项          // 右值

变量的名字，不论其类型(右值引用)，由其名字构成的表达式仍是左值表达式
```

5.2 左值引用/右值引用

C++支持引用（创建对象的别名），C++11起，支持右值引用。

```cpp
// 左值引用，可拥有不同的 cv 限定
std::string s;
std::string& s2 = s;                // s的引用，可通过s2修改s
const std::string& s3 = s;          // s的常量引用，不可通过s3修改s

void f(const std::string& s);       // 参数为引用

///////////

// 右值引用
int& n = 42;                // error, 不能绑定到左值引用
const int& n = 42;          // ok, const
int&& n = 42;               // ok, 右值引用

// 右值引用/到const的左值引用 可用于为临时对象延长生存期
std::string s1 = "hello, ";
std::string s2 = "world.";
string&& s3 = s1 + s2;
std::cout << s3 << std::endl;

struct A {
    ~A() { std::cout << "~A()" << std::endl; }
};

int main() {
    A&& a = A();
    std::cout << "here" << std::endl;
}

// g++ -fno-elide-constructors -std=c++11, 关闭返回值优化
// here
// ~A()

int main() {
    A a = A();
    std::cout << "here" << std::endl;
}
// ~A()
// here
// ~A()
```

5.3 std::move

```cpp
// from gcc 11.3.0, 等价于static_cast到相应类型的右值引用
template<typename _Tp>
_GLIBCXX_NODISCARD
constexpr typename std::remove_reference<_Tp>::type&&
move(_Tp&& __t) noexcept
{ return static_cast<typename std::remove_reference<_Tp>::type&&>(__t); }
```

5.4 移动构造函数

```cpp
struct A {
    A() {}
    A(const A&) { std::cout << "A(const A&)" << std::endl; }
    A(A&&) { std::cout << "A(A&&)" << std::endl; }
};

int main() {
    std::vector<A> vc;
    vc.emplace_back(A());
}

// A(A&&)

int main() {
    std::string s("hello");
    std::string s2 = std::move(s);
    std::cout << std::boolalpha << s.empty() << std::endl;
    std::cout << s2 << std::endl;
}
// true
// hello
```

5.5 std::forward

```cpp
// 引用折叠
T& &   =>  T&
T&& &  =>  T&
T& &&  =>  T&
T&& && =>  T&&

// from gcc 11.3.0
template<typename _Tp>
_GLIBCXX_NODISCARD
constexpr _Tp&&
forward(typename std::remove_reference<_Tp>::type& __t) noexcept
{ return static_cast<_Tp&&>(__t); }

// 完美转发
struct A {
    void f() & { std::cout << "&" << std::endl; }
    void f() && { std::cout << "&&" << std::endl; }
};
template <typename T>
void Print(T&& t) {    // 转发引用(无cv限定的模板函数形参、auto&&)
    t.f();                   // &
    std::move(t).f();        // &&
    std::forward<T>(t).f();  // & or &&
}
int main() {
    A a;
    Print(a);
    Print(A());
}

// std::vector::emplace_back => placement new 根据左值/右值决定拷贝构造/移动构造

for (auto&& x: f()); // 转发引用，f() 可以是左值/右值
```

总结：移动语义节省拷贝构造的开销，是升级至C++11最重要的特性之一；没有移动语义，就没有unique_ptr（C++11前只能用auto_ptr）；std::move/std::forward 不移动/转发任何东西，只做cast。

## 6 forEach

```cpp
int arr[]{0, 1, 2};
for (int& x : arr) {
    x++;
}

// https://cppinsights.io/

{

int arr[3] = {0, 1, 2};
{
int (&__range1)[3] = arr;
for(int * __begin1 = __range1, *__end1 = __range1 + 3L; __begin1 != __end1; ++__begin1) {
  int & x = *__begin1;
  x++;
}

}

// 数组 定义了begin和end 花括号初始化器列表
```

总结：用于遍历，方便，更可读。

## 7 constexpr

修饰变量或函数，用于常量表达式，（要求编译器）进行编译期求值。

```cpp
// 用std::numeric_limits<int>::max()替代INT_MAX
template<class T> class numeric_limits {
public:
    static constexpr T max() noexcept {}
};
```

总结：扩展了常量表达式的范围，显示要求编译器。

## 8 raw string literal

原始字符串字面量。

```cpp
std::cout << R"dxxx( hello, world. )dxxx" << std::endl;
//  hello, world.

std::cout << R"(ABC
123)" << std::endl;
// ABC\n123

std::cout << R"(
{
  "k1" : true,
  "k2" : "str"
}
)" << std::endl;

std::regex word_regex(R"(\w+)");
// \\w+
```

总结：避免转义字符，json、regex、换行时好用。

## 9 variadic templates

可变模版参数

```cpp
void print() { std::cout << std::endl; }

template <class T, class... Args>
void print(const T& arg0, const Args&...args) {
    std::cout << arg0 << " ";
    print(args...);
}

print(1, 1.0, true, "hello");
```

```cpp
// c++14, auto in lambda parameter
template <class... Args>
void print(const Args&...args) {
    (void)std::initializer_list<int>{([](auto i) { std::cout << i << " "; }(args), 0)...};
    std::cout << std::endl;
}
```

总结：强大，优美！

## 10

**lang**

- noexcept
- thread_local
- static_assert
- ...

**library**

- 容器：std::array, std::unordered_map, std::unordered_set, std::unordered_multiset, std::unordered_multimap, std::forward_list
- 智能指针：std::unique_ptr, std::shared_ptr, std::weak_ptr
- 正则表达式库：regex
- 并发：std::thread, std::atomic, std::mutex, std::condition_variable
- ...

## Reference

- <https://zh.cppreference.com>
- <https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2011/n3242.pdf>
- <https://github.com/CnTransGroup/EffectiveModernCppChinese>
