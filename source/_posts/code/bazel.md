---
title: Bazel
date: 2023-08-16
tags: tools
---

## Bazel

* <https://bazel.build>
* <https://github.com/bazelbuild/bazel>
* <https://github.com/bazelbuild/examples>

### Workspace, Repositories, Packages, Targets, Labels

```
project/
|-- package1
|   `-- BUILD
|-- package2
|   `-- BUILD
`-- WORKSPACE
```

`WORKSPACE` 文件标识了项目的根目录，这个目录下也会存放 bazel 的输出。`WORKSPACE` 可以为空，也可以包含对外部依赖的引用。代码以仓库（Repositories）的形式组织，包含 `WORKSPACE` 文件的目录称为主仓库（main repository, `@`）。

含有 `BUILD` 的目录是一个包。包包含该目录下的所有文件，包括子目录（含有`BUILD`文件的子目录除外，它是另一个包）。包中的元素称为目标（Targets），有以下几类目标。

* 文件（File）
  * 源文件（Source File）
  * 生成的文件（Generated File）
* 规则（Rule）
* 包组（Package Groups）

目标的名称称为标签（Label），例如 `@myrepo//my/app/main:app_binary`（`@myrepo` 内部可以简写为 `//my/app/main:app_binary`）

标签由冒号分为两部分，包名（`my/app/main`）和 目标名（`app_binary`）, 当省略冒号时，目标名等同包名最后一段路径，例如
`//my/app` 等价于 `//my/app:app`。引用当前包内目标时，包名也可以省略，因此以下四种写法等价。

```bazel
# /文件 /my/app:BUILD 内
//my/app:app
//my/app
:app
app
```

BUILD 文件中可以定义规则，用以指定输入输出间的关系及构建输出的步骤。

### Workspace Rules

```bazel
local_repository(name, path, repo_mapping)
new_local_repository(name, build_file, build_file_content, path, repo_mapping, workspace_file, workspace_file_content)
```

例如

```bazel
# 通过 @my-ssl 引用该仓库
local_repository(
    name = "my-ssl",
    path = "/home/user/ssl",
)

new_local_repository(
    name = "my-ssl",
    path = "/home/user/ssl",
    build_file = "BUILD.my-ssl",
)
```

`BUILD.my-ssl` 如下

```bazel
java_library(
    name = "openssl",
    srcs = glob(['*.java'])
    visibility = ["//visibility:public"],
)
```

可以不指定 `build_file` 而是指定 `build_file_content` （必须有其中一个），以包含文件中的内容（注意缩进要和BUILD文件一致）

```bazel
# Loading an extension
load("@bazel_tools//tools/build_defs/repo:git.bzl", "git_repository")
load("@bazel_tools//tools/build_defs/repo:http.bzl", "http_archive")

git_repository(name, branch, commit, init_submodules, patch_args, patch_cmds, patch_cmds_win,
               patch_tool, patches, recursive_init_submodules, remote, shallow_since, strip_prefix,
               tag, verbose)

new_git_repository(name, branch, build_file, build_file_content, commit, init_submodules,
                   patch_args, patch_cmds, patch_cmds_win, patch_tool, patches,
                   recursive_init_submodules, remote, shallow_since, strip_prefix, tag, verbose,
                   workspace_file, workspace_file_content)

http_archive(name, auth_patterns, build_file, build_file_content, canonical_id, netrc, patch_args,
             patch_cmds, patch_cmds_win, patch_tool, patches, sha256, strip_prefix, type, url, urls,
             workspace_file, workspace_file_content)

http_file(name, auth_patterns, canonical_id, downloaded_file_path, executable, netrc, sha256, urls)

http_jar(name, auth_patterns, canonical_id, netrc, sha256, url, urls)
```

### BUILD Rules

#### C/C++ Rules

```bazel
cc_binary
cc_import
cc_library
cc_proto_library
fdo_prefetch_hints
fdo_profile
propeller_optimize
cc_test
cc_toolchain
cc_toolchain_suite
```

### Bazel CLI

```shell
bazel clean             # 删除输出文件
bazel build <target>    # 构建目标
```

