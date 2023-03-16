---
title: "终端模拟器：Alacritty"
date: 2024-02-26
tags: tools
---

[Alacritty](https://alacritty.org/)是我目前使用的终端模拟器，以下几个特点我比较喜欢：

- 开源
- 跨平台(Linux/Mac/Windows)
- 文本配置(yaml)方便同步
- vi模式的搜索
- 可配置选中即复制到粘贴板
- 可右键粘贴
- 自定义配色
- 搭配tmux使用多窗口/多标签页

开源、跨平台、文本化配置是我选择终端模拟器的必要条件。

为了方便使用快捷键在标签页中切换，需要配置键位绑定。
例如，tmux中用`C-b c`创建`window`，为了模拟mac里`Command T`创建新标签页的行为，需要配置按下`Command T`时发送`\x02c`。

其他键位配置如下：

```yaml
key_bindings:
  - { key: T,         mods: Command, chars: "\x02c" }     #  tmux new window C-b c
  - { key: Key0,      mods: Command, chars: "\x020" }     #  tmux select window 0
  - { key: Key1,      mods: Command, chars: "\x021" }     #                 ... 1
  - { key: Key2,      mods: Command, chars: "\x022" }     #                 ... 2
  - { key: Key3,      mods: Command, chars: "\x023" }     #                 ... 3
  - { key: Key4,      mods: Command, chars: "\x024" }     #                 ... 4
  - { key: Key5,      mods: Command, chars: "\x025" }     #                 ... 5
  - { key: Key6,      mods: Command, chars: "\x026" }     #                 ... 6
  - { key: Key7,      mods: Command, chars: "\x027" }     #                 ... 7
  - { key: Key8,      mods: Command, chars: "\x028" }     #                 ... 8
  - { key: Key9,      mods: Command, chars: "\x029" }     #                 ... 9
  - { key: L,         mods: Command, chars: "\x02l" }     # tmux switch between two latest windows
  - { key: W,         mods: Command, chars: "\x02Q" }     # kill current window
  - { key: H,         mods: Command, chars: "\x02\x1b" }  # C-b ESC
  - { key: LBracket,  mods: Command, chars: "\x02(" }     # C-b (
  - { key: RBracket,  mods: Command, chars: "\x02)" }     # C-b )
```

可惜，Alacritty还不支持自动保存终端日志。
