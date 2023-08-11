# C++实现basename与dirname

实现字符串函数，`basename, dirname`，基本功能与同名命令`man 1`相同

```cpp
namespace liph {

inline std::string basename(std::string_view path) {
    std::string ret;
    bool start = true;
    for (char ch : path) {
        if (ch != '/' && start) {
            ret += ch;
        } else if (ch == '/') {
            start = false;
        } else if (ch != '/' && !start) {
            ret.clear();
            ret += ch;
            start = true;
        }
    }
    if (!path.empty() && path.back() == '/' && ret.empty()) return "/";
    return ret;
}

inline std::string dirname(std::string_view path) {
    auto pos = path.find_last_not_of('/');
    if (pos == std::string_view::npos) return path.empty() ? "." : "/";  // empty or only contain '/'
    path = path.substr(0, pos + 1);                                      // remove the trailing '/'
    pos = path.find_last_of('/');
    if (pos == std::string_view::npos) return ".";  // not contain '/'
    path = path.substr(0, pos);                     // remove the trailing "/xxxx"
    if (path.empty()) return "/";                   // '/' or "////" before substr
    pos = path.find_last_not_of('/');
    if (pos != std::string_view::npos) path = path.substr(0, pos + 1);  // remove trailing duplicate '/'
    return std::string(path);
}

}  // namespace liph
```

## 测试

```cpp
TEST(string, basename) {
    EXPECT_EQ(liph::basename(""), "");
    EXPECT_EQ(liph::basename("abc"), "abc");
    EXPECT_EQ(liph::basename("/"), "/");
    EXPECT_EQ(liph::basename("//////"), "/");
    EXPECT_EQ(liph::basename("/usr/bin/ls"), "ls");
    EXPECT_EQ(liph::basename("/usr/bin/"), "bin");
    EXPECT_EQ(liph::basename("/usr/bin///"), "bin");
    EXPECT_EQ(liph::basename("/usr/////bin/"), "bin");
    EXPECT_EQ(liph::basename("/tmp/"), "tmp");
    EXPECT_EQ(liph::basename("tmp/"), "tmp");
    EXPECT_EQ(liph::basename("tmp/abc///"), "abc");
    EXPECT_EQ(liph::basename("../.."), "..");
}

TEST(string, dirname) {
    EXPECT_EQ(liph::dirname(""), ".");
    EXPECT_EQ(liph::dirname("abc"), ".");
    EXPECT_EQ(liph::dirname("/"), "/");
    EXPECT_EQ(liph::dirname("//////"), "/");
    EXPECT_EQ(liph::dirname("/usr/bin/ls"), "/usr/bin");
    EXPECT_EQ(liph::dirname("/usr/bin/"), "/usr");
    EXPECT_EQ(liph::dirname("/usr/bin///"), "/usr");
    EXPECT_EQ(liph::dirname("/usr/////bin/"), "/usr");
    EXPECT_EQ(liph::dirname("/tmp/"), "/");
    EXPECT_EQ(liph::dirname("tmp/"), ".");
    EXPECT_EQ(liph::dirname("tmp/abc///"), "tmp");
    EXPECT_EQ(liph::dirname("/tmp////abc/a"), "/tmp////abc");
    EXPECT_EQ(liph::dirname("../.."), "..");
}
```
