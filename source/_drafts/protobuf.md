- https://github.com/protocolbuffers/protobuf
- https://protobuf.dev/

forward compatible 向前(未来)兼容：旧代码可以读取由新代码编写的记录

新协议新增字段：旧协议代码忽略新增字段
新协议删除字段：不能删除必需字段，旧协议代码使用默认字段(对于repeated则是空)

backward compatible 向后(过去)兼容：新代码可以读取由旧代码编写的记录

新协议新增字段：不能新增必需字段
新协议删除字段：新协议代码忽略该字段

适用的数据大小：几兆字节

Why required and optional is removed in Protocol Buffers 3
https://stackoverflow.com/questions/31801257/why-required-and-optional-is-removed-in-protocol-buffers-3

- required 不利于兼容
- required 可能 not required，或者其类型发生改变
- 必要性检查只是有效性检查的一部分，去除required利于架构简化

Data Types

- Scalar Value Types
- message
- enum
- oneof
- map

BUILD.bazel

```bazel
load("@rules_cc//cc:defs.bzl", "cc_library")
load("@rules_proto//proto:defs.bzl", "proto_library")

cc_proto_library(
    name = "search_cc_proto",
    deps = [":search_proto"],
)

proto_library(
    name = "search_proto",
    srcs = ["search.proto"],
)
```

search.proto

```proto
syntax = "proto2";

message SearchRequest {
    optional string query = 1;
    optional int32 page_number = 2;
    optional int32 result_per_page = 3;
}

message SearchResponse {
    optional int32 code = 1;
}
```

https://protobuf.dev/programming-guides/proto2/

```proto
syntax = "proto2";
// Comments
/* Comments */

// Importing Definitions
import "myproject/other_protos.proto";

message <NAME> {
  // <optional|repeated|required> <TYPE> <NAME> = <ID>;
  optional string query = 1;
}
```

packed encoding
https://protobuf.dev/programming-guides/encoding/#packed

```proto
repeated int32 samples = 4 [packed = true];
repeated ProtoEnum results = 5 [packed = true];
```

compiler

```cpp
namespace google::protobuf::compiler {

class CodeGenerator {
 public:
  CodeGenerator() {}
  CodeGenerator(const CodeGenerator&) = delete;
  CodeGenerator& operator=(const CodeGenerator&) = delete;
  virtual ~CodeGenerator();
  virtual bool Generate(const FileDescriptor* file,
                        const std::string& parameter,
                        GeneratorContext* generator_context,
                        std::string* error) const = 0;
  virtual bool GenerateAll(const std::vector<const FileDescriptor*>& files,
                           const std::string& parameter,
                           GeneratorContext* generator_context,
                           std::string* error) const;
};

class GeneratorContext {
 public:
  GeneratorContext() {}
  GeneratorContext(const GeneratorContext&) = delete;
  GeneratorContext& operator=(const GeneratorContext&) = delete;
  virtual ~GeneratorContext();
  virtual io::ZeroCopyOutputStream* Open(const std::string& filename) = 0;
  virtual io::ZeroCopyOutputStream* OpenForAppend(const std::string& filename);
  virtual io::ZeroCopyOutputStream* OpenForInsert(
      const std::string& filename, const std::string& insertion_point);
  virtual io::ZeroCopyOutputStream* OpenForInsertWithGeneratedCodeInfo(
      const std::string& filename, const std::string& insertion_point,
      const google::protobuf::GeneratedCodeInfo& info);
  virtual void ListParsedFiles(std::vector<const FileDescriptor*>* output);
  virtual void GetCompilerVersion(Version* version) const;
};

} // namespace google::protobuf::compiler
```
