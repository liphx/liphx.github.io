# Make Your API Hard To Use Wrong (Jason Turner, 2022)

- Try to use your API incorrectly
- Use better naming
- Use `[[nodiscard]]` (with reasons) liberally
- Never return a raw pointer
- Use `noexcept` to help indicate the type of error handling
- Provide consistent, impossible to ignore, in-band error handling Use stronger types and avoid default conversions
- (Sparingly) delete problematic overloads / prevent conversions Avoid passing pointers (only to be used for single/optional objects) Avoid passing smart pointers
- Limit your API as much as possible
- Fuzz your API
- Enable for `constexpr` Unless You Have a Really Good Reason Not To
- Avoid passing pointers (only to be used for single/optional objects and check it for `nullptr`)  
- Prefer & Parameters For Non-Small, Non- Trivial Objects
- Don’t Pass Smart Pointers Unless You Need to Participate In The Lifetime

1. Cache Invalidation
2. Naming
3. Off-by-one Errors
4. Scope creep
5. Bounds checking

`std::expected`

https://godbolt.org/

```cpp
template<typename WidgetType> [[nodiscard]] WidgetType make_widget()
requires (std::is_base_of_v<Widget, WidgetType>);
```

# Back to Basics - RAII (Andre Kostur, 2022)

Resource Acquisition Is Initialization

Resource Usage Issues
- Leak
- Use-after-disposal
- Double-disposal
RAII Solves the problems

RAII std examples
- lock_guard
- unique_lock
- jthread
- unique_ptr
- shared_ptr
- fstream
- scoped_lock

other problems
- Resource loops
- Deadlocks

R: Resource management
ES.5: Keep scopes small
ES.20: Always initialize an object
ES.21: Don't introduce a variable (or constant) before you need to use it
ES.22: Don't declare a variable until you have a value to initialize it with

# Back to Basics - Smart Pointers (David Olsen, 2022)

- std::span
- std::unique_ptr
- std::shared_ptr
- std::weak_ptr

- dynamic_pointer_cast
- static_pointer_cast
- const_pointer_cast
- reinterpret_pointer_cast

shared_from_this
enable_shared_from_this

# Back to Basics - Templates (Nicolai Josuttis, 2022)

```cpp
template <typename T>
void printColl(const T& coll) {
    for (const auto& elem : coll) {
        std::cout << elem << '\n';
    }
}

// do not need inline in header file
void printColl(const auto& coll) {
    for (const auto& elem : coll) {
        std::cout << elem << '\n';
    }
}
```

Concepts

```cpp
template<typename T>
concept HasLessThan = requires (T x) { {x < x} -> std::convertible_to<bool>; };

template<typename T>
requires std::copyable<T> && HasLessThan<T>
T mymax(T a, T b) {
	return b < a ? a : b;
}

template<typename T1, typename T2>
auto mymax(T1 a, T2 b)
{
	return b < a ? a : b;
}

// Non-Type Template Parameters (NTTP)
template <typename T, int Sz> // stack of at most Sz values of type T
class Stack;


void add(auto& coll, const auto& val)
{
if constexpr (requires { coll.push_back(val); }) { // if push_back() is supported
coll.push_back(val); // - call push_back()
}
else {
coll.insert(val); // - else call insert()
}
}
```

Variadic Templates


