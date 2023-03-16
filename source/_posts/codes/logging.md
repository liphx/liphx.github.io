---
title: 实现简单的C++日志库
date: 2023-08-15 10:29:18
tags: cplusplus
---

### 0. 接口

```cpp
std::string str = "world";
LOG << "hello " << str;
LOG << format("The answer is {}", 42);
```

流式输出，不需要 `init`，日志追加写入固定的文件中，格式如下

```
[2023-08-15 10:39:26 logging_test.cpp:8] hello world
[2023-08-15 10:39:26 logging_test.cpp:9] The answer is 42
```

### 1. `LOG`宏

要实现流式输出，需要用到C++的析构函数，`LOG`宏即构造一个`stream`对象，析构时将其内容输出

```cpp
#ifndef __FILENAME__
#define __FILENAME__ ((strrchr(__FILE__, '/') ?: __FILE__ - 1) + 1)
#endif
#define LOG liph::log_message(__FILENAME__, __LINE__).stream()
```

### 2. `log_message`

```cpp
class log_message {
public:
    log_message(const char *filename, int line) {
        ss_.str("");
        ss_ << '[' << time_format() << ' ' << filename << ':' << line << "] ";
    }

    std::ostringstream& stream() { return ss_; }

    ~log_message() {
        ss_ << '\n';
        singleton<logger>::instance().log(ss_);
    }

private:
    inline thread_local static std::ostringstream ss_;
};
```

### 3. `logger`

```cpp
class logger : noncopyable {
private:
    static constexpr char logfilename[] = "std.log";

public:
    logger() {
        producer_ = &buffer_[0];
        consumer_ = &buffer_[1];
        write_file_.open(logfilename, std::ios_base::out | std::ios_base::app);
        if (!write_file_.is_open()) std::cerr << "open log file fail, use stderr\n";
        started_ = true;
        tid_ = std::thread(&logger::run, this);
    }

    ~logger() {
        started_ = false;
        if (tid_.joinable()) tid_.join();
        if (write_file_.is_open()) write_file_.close();
    }

    void log(std::ostringstream& ss) {
        std::lock_guard<std::mutex> lock(lock_);
        producer_->emplace_back(std::move(ss).str());
    }

private:
    void run() {
        std::ostream& os = write_file_.is_open() ? write_file_ : std::cerr;
        while (started_) {
            consume(os);
            std::this_thread::sleep_for(std::chrono::milliseconds(100));
        }
        consume(os);
    }

    void consume(std::ostream& os) {
        {
            std::lock_guard<std::mutex> lock(lock_);
            std::swap(producer_, consumer_);
        }
        if (!consumer_->empty()) {
            for (const std::string& str : *consumer_) {
                os << str;
            }
            os.flush();
            consumer_->clear();
        }
    }

    std::ofstream write_file_;
    std::atomic<bool> started_;
    std::thread tid_;
    std::vector<std::string> *producer_, *consumer_;
    std::vector<std::string> buffer_[2];
    mutable std::mutex lock_;
};
```

### 4. benchmark

测试数据，日志长度128，线程数16，fstream文件输出时使用mutex同步，format与上面相同

```
Run on (12 X 2600 MHz CPU s)
CPU Caches:
  L1 Data 32 KiB
  L1 Instruction 32 KiB
  L2 Unified 256 KiB (x6)
  L3 Unified 12288 KiB
Load Average: 2.43, 2.53, 2.36
***WARNING*** Library was built as DEBUG. Timings may be affected.
-----------------------------------------------------
Benchmark           Time             CPU   Iterations
-----------------------------------------------------
fstream_mt    2390740 ns       242201 ns         2850
logging_mt    1852941 ns       329709 ns         2141
glog_mt       5449782 ns       322837 ns         1000
```

完整代码见 <https://github.com/liphx/code/blob/main/src/cplusplus/liph/logging.h>
