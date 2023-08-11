---
title: 字符串算法：kmp与manacher
date: 2023-08-11
tags: C++
permalink: code/kmp-manacher/
---

## KMP

```cpp
#include <iostream>
#include <iterator>
#include <vector>
using namespace std;

/*
 * pattern.length() > 0
 * pattern.length() == next.size()
 */
void get_next(const string& pattern, vector<int>& next) {
    int n = pattern.length();
    next[0] = -1;
    int i = 0, j = -1;
    while (i < n) {
        while (j >= 0 && pattern[i] != pattern[j]) j = next[j];
        i++;
        j++;
        if (pattern[i] == pattern[j])
            next[i] = next[j];
        else
            next[i] = j;
    }
}

/*
 * 在 str 中查找 pattern
 * 辅助数组 next 表示失配后与模式串的哪一位比较才可能导致匹配
 * pattern.length() == next.size()
 * 返回 pattern 在 str 中出现的位置
 */
vector<int> kmp(const string& str, const string& pattern, const vector<int>& next) {
    vector<int> ans;
    int n = str.length();
    int m = pattern.length();
    int i = 0, j = 0;
    while (i < n) {
        while (j >= 0 && str[i] != pattern[j]) j = next[j];
        i++;
        j++;
        if (j == m) {
            ans.emplace_back(i - m);
            j = next[m];
        }
    }
    return ans;
}
int main() {
    string str = "aabcd";
    string pattern = "abab";
    vector<int> next(pattern.length());
    get_next(pattern, next);
    copy(next.begin(), next.end(), ostream_iterator<int>(cout, " "));

    auto ans = kmp(str, pattern, next);
    copy(ans.begin(), ans.end(), ostream_iterator<int>(cout, " "));
}
```

## manacher

```cpp
#include <cassert>
#include <iostream>
#include <string>
using namespace std;

string manacher(const string& s) {
    string ret;

    // 预处理，假设原字符串中无'#' '$'
    assert(s.find('#') == string::npos);
    assert(s.find('$') == string::npos);
    string str = "$#";  // 优化
    for (int i = 0; i < s.length(); ++i) str = str + s[i] + '#';

    // 计算回文半径数组p
    // 以s[i]为中心（无论奇偶）的回文子串在原串中的长度为p[i] - 1
    // 算法的核心为计算p数组
    int n = str.length();
    int p[n];
    // 引入辅助变量 MaxRight 表示当前已确定的回文子串能触及的最右端字符位置
    // pos 为其对称中心的位置
    int MaxRight = 0, pos = 0;
    int m = -1, mi = 0;  // 记录最长子串的长度和位置
    for (int i = 1; i < n; ++i) {
        if (MaxRight > i)
            p[i] = min(p[2 * pos - i], MaxRight - i + 1);  //核心算法
        else
            p[i] = 1;
        while (str[i + p[i]] == str[i - p[i]]) p[i]++;  // 开头加了'$'字符，不用考虑边界
        if (p[i] + i - 1 > MaxRight) {
            MaxRight = p[i] + i - 1;
            pos = i;
        }
        if (p[i] > (m + 1)) {
            m = p[i] - 1;
            mi = i;
        }
    }
    // 无论m奇偶都适用
    for (int i = mi - (m - 1); i <= mi + (m - 1); i += 2) ret += str[i];

    return ret;
}

int main() {
    cout << manacher("babad") << endl;  //=>bab
    cout << manacher("cbbd") << endl;   //=>bb

    return 0;
}
```
