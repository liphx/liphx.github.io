---
title: Git
date: 2023-01-01
updated: 2023-08-14
tags: tools
---

## config

`git config` 进行配置

```shell
git config --global user.name <name>
git config --global user.email <email>
git config -l, --list
```

`.gitconfig` 配置文件

- `/etc/gitconfig` 系统中对所有用户 `git config --system` 读写这个文件
- `~/.gitconfig` 适用于当前用户 `git config --global` 读写这个文件
- `${dir}/.git/config` 针对当前项目有效 `git config --local` 读写这个文件

每一个级别的配置都会覆盖上层的相同配置

## init

- `git init` 在现有目录中初始化仓库
- `git init dir` 创建`dir`目录并初始化成git项目

## clone

`git clone` 克隆现有的仓库

```shell
git clone [<options>] [--] <repo> [<dir>]
git clone git@github.com:liphx/example.git -b master my_dir
```

## status

`git status` 检查当前文件状态

```shell
$ git status
On branch master
nothing to commit, working tree clean
$ git status -s # 以更为紧凑的格式输出
 M file1
MM file2
A  file3
M  file4
?? file5
```

- ?? 标记：新添加的未跟踪文件
- A  标记：新添加到暂存区中的文件
- M  标记：修改过的文件

出现在右边的 M 表示该文件被修改了但是还没放入暂存区，出现在靠左边的 M 表示该文件被修改了并放入了暂存区

## add

`git add` 跟踪新文件、暂存已修改文件

```shell
git add <files>
git add -u
```

## diff

`git diff` 比较差异

```
--name-only
--name-status
```

## commit

`git commit` 提交更新

```shell
$ git commit -m "first commit"
[master (root-commit) 07baa89] first commit
 1 file changed, 0 insertions(+), 0 deletions(-)
 create mode 100644 file1
$ git commit -a -m "second commit" # 把所有已经跟踪过的文件暂存起来一并提交
```

## rm, mv

`git rm` 移除文件

从暂存区域移除，并连带从工作目录中删除指定的文件

如果删除之前修改过并且已经放到暂存区域的话，则必须要用强制删除选项 -f

把文件从 Git 仓库中删除（亦即从暂存区域移除），但仍然希望保留在当前工作目录中 --cached

`git mv` 移动文件

这条命令等价于

```shell
mv file1 file2
git rm file1
git add file2
```

## log

`git log` 查看提交历史

```shell
git log
git log --oneline
git log --all
git log -n 5
git log --graph
```

## remote

`git remote` 远程仓库

```shell
git remote
git remote -v
git remote show origin
git remote add <name> <url> # 添加远程仓库
git remote remove <name> # 移除远程仓库
git remote rename <old> <new> # 重命名远程仓库
```

## fetch

`git fetch` 从远程仓库中获得数据

## push

`git push` 推送到远程仓库

## tag

`git tag` 标签

```shell
git tag # 列出标签
git tag -a v1.0 -m 'my version 1.0' # -a 创建附注标签 -m 指定存储在标签中的信息
git show v1.0 # 查看标签信息与对应的提交信息
git tag v1.1-lw # 无-a 选项，创建轻量标签，它只是一个特定提交的引用
git tag -a v0.9 <commit> # 对过去的提交打标签
git push origin [tagname] # 传送标签到远程仓库服务器
git tag -d <tagname> # 删除本地仓库标签
git push <remote>:refs/tags/<tagname> # 更新远程仓库标签
```

## branch

`git branch` git分支

```shell
git branch # 显示当前所有分支， -v 还会显示各分支最后一次提交， --merged 与 --no-merged显示已合并与未合并的分支
git branch new-branch # 创建新分支
git checkout new-branch # 切换到已存在分支， HEAD 现在指向 new-branch
git checkout -b iss99 # 创建新分支并切换
git branch -d iss99 # 删除分支
```

## merge

`git merge` 分支合并

## rebase

`git rebase` 变基

https://stackoverflow.com/questions/22992543/how-do-i-git-rebase-the-first-commit
`git rebase -i --root`

## reset

`git reset` 回退

```shell
git reset --hard [commit_id]
```

## gitignore

`.gitignore` 忽略文件

文件 .gitignore 的格式规范如下：

- 所有空行或者以 ＃ 开头的行都会被 Git 忽略。
- 可以使用标准的 glob 模式匹配。
- 匹配模式可以以（/）开头防止递归。
- 匹配模式可以以（/）结尾指定目录。
- 要忽略指定模式以外的文件或目录，可以在模式前加上惊叹号（!）取反。

所谓的 glob 模式是指 shell 所使用的简化了的正则表达式。

## ssh密钥复制

```shell
chmod 600 ~/.ssh/id_rsa
eval "$(ssh-agent -s)"
ssh-add
ssh -T git@github.com
```

## bisect

<https://www.ruanyifeng.com/blog/2018/12/git-bisect.html>

## sshkey error

- <https://stackoverflow.com/questions/69875520/git-error-no-matching-host-key-type-found-their-offer-ssh-rsa>
- <https://help.gitee.com/enterprise/code-manage/%E6%9D%83%E9%99%90%E4%B8%8E%E8%AE%BE%E7%BD%AE/%E9%83%A8%E7%BD%B2%E5%85%AC%E9%92%A5%E7%AE%A1%E7%90%86/SSH%20Key%20%E7%AA%81%E7%84%B6%E5%A4%B1%E6%95%88%E9%97%AE%E9%A2%98%E8%A7%A3%E7%AD%94%E5%8F%8A%E5%A4%84%E7%90%86%E5%8A%9E%E6%B3%95>
