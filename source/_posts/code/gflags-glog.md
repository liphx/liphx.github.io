---
title: using gflags and glog
date: 2023-08-11
tags: C++
permalink: code/gflags-glog/
---

## gflags

- http://gflags.github.io/gflags/
- https://github.com/gflags/gflags.git

### type

- bool -> bool
- int32/uint32/int64/uint64 -> `int*_t`
- double -> double
- string -> std::string

### declare

```cpp
#include "gflags/gflags_declare.h"

#define GFLAGS_NAMESPACE google
namespace fLS {
typedef std::string clstring;
}  // namespace fLS

#define DECLARE_VARIABLE(type, shorttype, name)                  \
    namespace fL##shorttype {                                    \
        extern GFLAGS_DLL_DECLARE_FLAG type FLAGS_##name;        \
    }                                                            \
    using fL##shorttype::FLAGS_##name

#define DECLARE_bool(name)   DECLARE_VARIABLE(bool, B, name)
#define DECLARE_int32(name)  DECLARE_VARIABLE(::GFLAGS_NAMESPACE::int32, I, name)
#define DECLARE_uint32(name) DECLARE_VARIABLE(::GFLAGS_NAMESPACE::uint32, U, name)
#define DECLARE_int64(name)  DECLARE_VARIABLE(::GFLAGS_NAMESPACE::int64, I64, name)
#define DECLARE_uint64(name) DECLARE_VARIABLE(::GFLAGS_NAMESPACE::uint64, U64, name)
#define DECLARE_double(name) DECLARE_VARIABLE(double, D, name)
#define DECLARE_string(name)                                      \
    namespace fLS {                                               \
    using ::fLS::clstring;                                        \
    extern GFLAGS_DLL_DECLARE_FLAG ::fLS::clstring& FLAGS_##name; \
    }                                                             \
    using fLS::FLAGS_##name
```

### define

```cpp
#include "gflags/gflags.h"

class GFLAGS_DLL_DECL FlagRegisterer {
public:
    template <typename FlagType>
    FlagRegisterer(const char *name, const char *help, const char *filename, FlagType *current_storage,
            FlagType *defvalue_storage) {
        FlagValue *const current = new FlagValue(current_storage, false);
        FlagValue *const defvalue = new FlagValue(defvalue_storage, false);
        RegisterCommandLineFlag(name, help, filename, current, defvalue);
    }
};

#define DEFINE_VARIABLE(type, shorttype, name, value, help)                                  \
    namespace fL##shorttype {                                                                \
        static const type FLAGS_nono##name = value;                                          \
        GFLAGS_DLL_DEFINE_FLAG type FLAGS_##name = FLAGS_nono##name;                         \
        type FLAGS_no##name = FLAGS_nono##name;                                              \
        static GFLAGS_NAMESPACE::FlagRegisterer o_##name(                                    \
                #name, MAYBE_STRIPPED_HELP(help), __FILE__, &FLAGS_##name, &FLAGS_no##name); \
    }                                                                                        \
    using fL##shorttype::FLAGS_##name

#define DEFINE_bool(name, val, txt)                                                                         \
    namespace fLB {                                                                                         \
    typedef ::fLB::CompileAssert                                                                            \
            FLAG_##name##_value_is_not_a_bool[(sizeof(::fLB::IsBoolFlag(val)) != sizeof(double)) ? 1 : -1]; \
    }                                                                                                       \
    DEFINE_VARIABLE(bool, B, name, val, txt)

#define DEFINE_int32(name, val, txt)  DEFINE_VARIABLE(GFLAGS_NAMESPACE::int32, I, name, val, txt)
#define DEFINE_uint32(name, val, txt) DEFINE_VARIABLE(GFLAGS_NAMESPACE::uint32, U, name, val, txt)
#define DEFINE_int64(name, val, txt)  DEFINE_VARIABLE(GFLAGS_NAMESPACE::int64, I64, name, val, txt)
#define DEFINE_uint64(name, val, txt) DEFINE_VARIABLE(GFLAGS_NAMESPACE::uint64, U64, name, val, txt)
#define DEFINE_double(name, val, txt) DEFINE_VARIABLE(double, D, name, val, txt)
#define DEFINE_string(name, val, txt)                                                                                  \
    namespace fLS {                                                                                                    \
    using ::fLS::clstring;                                                                                             \
    using ::fLS::StringFlagDestructor;                                                                                 \
    static union {                                                                                                     \
        void *align;                                                                                                   \
        char s[sizeof(clstring)];                                                                                      \
    } s_##name[2];                                                                                                     \
    clstring *const FLAGS_no##name = ::fLS::dont_pass0toDEFINE_string(s_##name[0].s, val);                             \
    static GFLAGS_NAMESPACE::FlagRegisterer o_##name(                                                                  \
            #name, MAYBE_STRIPPED_HELP(txt), __FILE__, FLAGS_no##name, new (s_##name[1].s) clstring(*FLAGS_no##name)); \
    static StringFlagDestructor d_##name(s_##name[0].s, s_##name[1].s);                                                \
    extern GFLAGS_DLL_DEFINE_FLAG clstring& FLAGS_##name;                                                              \
    using fLS::FLAGS_##name;                                                                                           \
    clstring& FLAGS_##name = *FLAGS_no##name;                                                                          \
    }                                                                                                                  \
    using fLS::FLAGS_##name
```

for example

```cpp
DEFINE_int32(number, 0, "default is 0");
/////
DEFINE_VARIABLE(GFLAGS_NAMESPACE::int32, I, number, 0, "default is 0");
/////

namespace fLI {
static const int32_t FLAGS_nononumber = 0;
int32_t FLAGS_number = FLAGS_nononumber;
static int32_t FLAGS_nonumber = FLAGS_nononumber;
static google::FlagRegisterer o_number("number", "default is 0", __FILE__, &FLAGS_number, &FLAGS_nonumber);
}  // namespace fLI
using fLI::FLAGS_number;
```

### RegisterFlagValidator

```cpp
#include "gflags/gflags.h"

DEFINE_string(module, "aa", "one of aa|ab|bc");
DEFINE_validator(module, [](const char *, const std::string& value) {
    if (value != "aa" && value != "ab" && value != "bc") {
        return false;
    }
    return true;
});

int main(int argc, char **argv) {
    google::ParseCommandLineFlags(&argc, &argv, true);
}
```

```shell
./a.out --module=bb
ERROR: failed validation of new value 'bb' for flag 'module'
```

### ParseCommandLineFlags

```cpp
uint32_t ParseCommandLineFlags(int* argc, char*** argv, bool remove_flags);

DEFINE_string(module, "aa", "one of aa|ab|bc");

static void print_args(int argc, char **argv) {
    std::cout << "argc: " << argc << ", argv:";
    for (int i = 1; i < argc; i++) {
        std::cout << " " << argv[i];
    }
    std::cout << std::endl;
}

int main(int argc, char **argv) {
    print_args(argc, argv);
    google::ParseCommandLineFlags(&argc, &argv, true);
    print_args(argc, argv);
}
```

```shell
# remove_flags is true
$ ./a.out 1 2 --module=ab 3 4
argc: 6, argv: 1 2 --module=ab 3 4
argc: 5, argv: 1 2 3 4
# remove_flags is false, flags will be the beginning in argv
./a.out 1 2 --module=ab 3 4
argc: 6, argv: 1 2 --module=ab 3 4
argc: 6, argv: --module=ab 1 2 3 4
```

## glog

https://github.com/google/glog

### bazel build

```bazel
load("@bazel_tools//tools/build_defs/repo:http.bzl", "http_archive")

http_archive(
    name = "com_github_gflags_gflags",
    sha256 = "34af2f15cf7367513b352bdcd2493ab14ce43692d2dcd9dfc499492966c64dcf",
    strip_prefix = "gflags-2.2.2",
    urls = ["https://github.com/gflags/gflags/archive/v2.2.2.tar.gz"],
)

http_archive(
    name = "com_github_google_glog",
    sha256 = "122fb6b712808ef43fbf80f75c52a21c9760683dae470154f02bddfc61135022",
    strip_prefix = "glog-0.6.0",
    urls = ["https://github.com/google/glog/archive/v0.6.0.zip"],
)
```

```bazel
cc_binary(
    name = "main",
    srcs = ["main.cpp"],
    deps = ["@com_github_google_glog//:glog"],
)
```

### quick start

Severity Levels: INFO, WARNING, ERROR, and FATAL

Logging a FATAL message terminates the program (after the message is logged)

Messages of a given severity are logged not only in the logfile for that severity, but also in all logfiles of lower severity.

默认日志文件

```
/tmp/\<program name\>.\<hostname\>.\<user name\>.log.\<severity level\>.\<date\>-\<time\>.\<pid\>
```

glog copies the log messages of severity level ERROR or FATAL to standard error (stderr) in addition to log files.

```cpp
#include "glog/logging.h"

int main(int, char **argv) {
    google::InitGoogleLogging(argv[0]);
    LOG(INFO) << "info log";
    LOG(WARNING) << "warning log";
    LOG(ERROR) << "error log";
    LOG(FATAL) << "fatal log";
}
```

```shell
$ ./a.out
E20230131 16:13:24.209595 1260326 glog.cpp:7] error log
F20230131 16:13:24.209903 1260326 glog.cpp:8] fatal log
*** Check failure stack trace: ***
    @        0x1035aee0d  google::LogMessage::Fail()
    @        0x1035ad56f  google::LogMessage::SendToLog()
    @        0x1035ae3da  google::LogMessage::Flush()
    @        0x1035b3519  google::LogMessageFatal::~LogMessageFatal()
    @        0x1035af475  google::LogMessageFatal::~LogMessageFatal()
    @        0x1034d2255  main
    @     0x7ff81683d310  start
Abort trap: 6
```

### flags

```shell
./a.out --log_dir=log    # if gflags is installed
GLOG_log_dir=log ./a.out # else
```

- `log_dir` (string, default="")
- `minloglevel` (int, default=0, which is INFO)
- `max_log_size` (uint32, 1800)
