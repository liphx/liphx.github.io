# A Tour of C++, 3rd

1. The Basics
2. User-Defined Types
3. Modularity
4. Error Handling
5. Classes
6. Essential Operations
7. Templates
8. Concepts and Generic Programming
9. Library Overview
10. Strings and Regular Expressions

Concrete classes – especially classes with small representations – are much like built-in types: we define them as local variables, access them using their names, copy them around, etc. Classes in class hierarchies are different: we tend to allocate them on the free store using new, and we access them through pointers or references.

For historical reasons realated to optimization, the order of evaluation of other expressions (e.g., f(x) + g(y)) and of function arguments (e.g., h(f(x), g(y))) is unfortunately unspecified.

When we want a function to be used only for evaluation at compile time, we declare it consteval rather than constexpr.

The size of an array must be a constant expression

Don’t panic! All will become clear in time

Keep common and local names short; keep uncommon and nonlocal names longer

Since we don’t know anything about the representation of an abstract type (not even its size), we must allocate objects on the free store (§5.2.2) and access them through references or pointers (§1.7, §15.2.1).

The destructor (~Vector_container()) overrides the base class destructor (~Container()). Note that the member destructor (~Vector()) is implicitly invoked by its class’s destructor (~Vector_container()).

Objects are constructed “bottom up” (base first) by constructors and destroyed “top down” (derived first) by destructors.

In many languages, resource management is primarily delegated to a garbage collector. In C++, you can plug in a garbage collector. However, I consider garbage collection the last choice after cleaner, more general, and better localized alternatives to resource management have been exhausted. My ideal is not to create any garbage, thus eliminating the need for a garbage collector: Do not litter!

A function template can be a member function, but not a virtual member. The compiler would not know all instantiations of such a template in a program, so it could not generate a vtbl (§5.4).

The best way to develop a template is often to
- first, write a concrete version
- then, debug, test, and measure it
- finally, replace the concrete types with template arguments.

Templates offer compile-time "duck typing"

Don't reinvent the wheel; use libraries;
