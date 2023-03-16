---
title: 一起来玩UNO吧！
date: 2023-08-11
tags:
---

之前写了个终端版的单机UNO([代码](https://github.com/liphx/code/blob/main/src/cplusplus/tools/uno.cpp))，
并且添加了一些额外功能。

在这里想说的是这样一个编程问题(后面发现这个问题叫Multiple Dispatch)

```cpp
class Card {
public:
    virtual bool match(const Card *) const = 0;
};
class NumCard : public Card;
class ActionCard : public Card;
class WildCard : public Card;
```

`Card`是卡牌的基类，UNO中有三种卡牌，每种卡牌都需要实现能否“匹配”其他卡牌，我想通过直接调用
`card->match(other)` 来判断当前卡牌是否满足要求（`card, other`都是`Card *`类型）。为了避免`switch (type)`的逻辑，
我的方法如下

1. 每个子类都实现以下成员函数

   ```cpp
   class Card {
   public:
       virtual bool match(const Card *) const = 0;
       virtual bool match(const NumCard *) const = 0;
       virtual bool match(const ActionCard *) const = 0;
       virtual bool match(const WildCard *) const = 0;
   };
   ```

2. 子类的`match(const Card *)`调用参数的`match`

   ```cpp
   class NumCard : public Card {
   public:
       bool match(const Card *other) const { return other->match(this); }
   };
   ```

3. 子类分别实现与其他卡牌的匹配逻辑

   ```cpp
   class NumCard : public Card {
   public:
       bool match(const WildCard *) const { return true; }
       // 这里实际上是WildCard->match(NumCard)，因此万能牌可以匹配任意牌
   };
   ```

然后就可以愉快的写UNO逻辑了。

Multiple Dispatch相关参考

- <https://en.wikipedia.org/wiki/Multiple_dispatch>
- <https://eli.thegreenplace.net/2016/a-polyglots-guide-to-multiple-dispatch/>
- <https://stackoverflow.com/questions/1749534/multiple-dispatch-in-c>
