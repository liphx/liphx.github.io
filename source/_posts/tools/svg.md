---
title: svg基础
date: 2024-04-15
tags: tools
---

SVG（Scalable Vector Graphics）：可缩放矢量图形

SVG规范 <https://www.w3.org/Graphics/SVG/>

## 基本形状

### 线段

```svg
<line x1="75" y1="95" x2="135" y2="85" style="stroke: black;"/>
```

- `x1, y1` 起点坐标
- `x2, y2` 终点坐标
- `style`
  - `stroke-width` 笔画宽度
  - `stroke` 笔画颜色
  - `stroke-opacity` 不透明度（0.0-1.0，0表示完全透明，1表示完全不透明）
  - `stroke-dasharray` 线的长度和空隙的长度，实现点线或虚线

### 矩形

```svg
<rect x="10" y="10" width="30" height="30"/>
<rect x="60" y="10" rx="10" ry="10" width="30" height="30"/>
```

- `x, y` 矩形左上角坐标
- `width, height` 矩形宽和高
- `rx, ry` x，y方向圆角半径，最大值为矩形宽度，高度的一半，如果只指定其中一个值，则认为他们相等
- `rx, ry`不相等意味着什么：圆角是椭圆而不是圆的一部分

### 圆

```svg
<circle cx="70" cy="95" r="50"/>
```

- `cx, cy` 圆心坐标
- `r` 半径

### 椭圆

```svg
<ellipse cx="75" cy="75" rx="20" ry="5"/>
```

- `cx, cy` 中心坐标
- `rx, ry` x，y方向半径

### 多边形

```svg
<polygon points="0,0 0,100 100,100 100,0" style="fill: none; stroke: black;"/>
```

`points` 各点x，y坐标对，多边形为封闭图形，会自动回到起始坐标

### 折线

```svg
<polyline points="0,0 0,100 100,100 100,0" style="fill: none; stroke: black;"/>
```

同多边形，图形不封闭

### 路径

```svg
<path d="M10,20 L100,20 L100,50"/>
```

- `d` data，描述路径的命令
  - `Mx,y` moveto，每个路径都必须以 moveto 命令开始，设置当前位置
  - `Lx,y` lineto，绘制一条线
  - `lx,y` 等价于`Lcurrent_x+x,current_y+y`
  - `Z` closepath，回到起点
  - `Hx` 水平线，等价于`Lx,current_y`
  - `hx` 水平线，等价于`lx,0`
  - `Vy` 垂直线，等价于`Lcurrent_x,y`
  - `vy`垂直线，等价于`l0,y`

### 文本

```svg
<text x="20" y="30" style="font-family: monospace;
                           font-size: 20px;
                           font-style: italic;
                           text-decoration: underline;">
    Hello World!</text>
```

## 分组和引用对象

### `<g>`

```svg
<g id="box" style="stroke: black; fill: none;">
    <circle cx="10" cy="10" r="10"/>
    <line x1="0" y1="30" x2="20" y2="30"/>
</g>
```

用于组合元素

### `<use>`

```svg
<use href="#box" x="40" y="0"/>
```

- `href` 引用元素
- `x, y` 移动到的位置

### `<defs>`

```svg
<defs>
    <g id="box" style="stroke: black; fill: none;">
        <circle cx="10" cy="10" r="10"/>
        <line x1="0" y1="30" x2="20" y2="30"/>
    </g>
</defs>

<use href="#box" x="40" y="0"/>
```

只定义，不显示

## 坐标变换

### translate

`translate(x, y)` 移动

### scale

`scale(xFactor, yFactor)` 缩放

`scale(x)` 等价于 `scale(x, x)`

### rotate

`rotate(angle)` 以原点`(0, 0)` 为中心旋转

`rotate(angle, x, y)` 以`(x, y)` 为中心旋转

### 组合

```svg
<defs><text id="hello" style="font-size: 12px;">Hello World!</text></defs>
<use href="#hello" transform="translate(100, 100) scale(3)" style="font-family: monospace;"/>
```

平移后缩放

## 渐变

### 线性渐变

```svg
<defs>
    <linearGradient id="two">
        <stop offset="0%" style="stop-color: #ffcc00;"/>
        <stop offset="100%" style="stop-color: #0099cc;"/>
    </linearGradient>
</defs>

<rect x="20" y="20" width="200" height="100" style="fill: url(#two);"/>
```

`linearGradient` 线性渐变

`stop` 渐变点

### 径向渐变

```svg
<defs>
    <radialGradient id="two">
        <stop offset="0%" style="stop-color: #ffcc00;"/>
        <stop offset="100%" style="stop-color: #0099cc;"/>
    </radialGradient>
</defs>

<rect x="20" y="20" width="200" height="100" style="fill: url(#two);"/>
```

`radialGradient` 径向渐变
