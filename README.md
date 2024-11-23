# Build-a-Modern-Computer-from-First-Principles

I use [online-ide](https://nand2tetris.github.io/web-ide/chip) to finish projects.

## 01

德摩根律很有用。

### Mux

核心思路：思考使用合取还是析取将两个输入组合（都可以）

思考在析取或合取什么情况下一边的结果决定了整个表达式的结果

### DMux

与 Mux 不同，选择器单独影响各个输出。而 Mux 是选择器影响最终结果。所以 Mux 得想办法串起来

## 02

### HalfAdder

Xor 不进位加法

And 进位

### ALU

可以通过或门来判断是否全为 0

## 03

### PC

理解 PC reset, inc, load 的顺序，reset 优先级最高，放到最后处理。load 次之，inc 最低。

## 04

### 指针访问

```
@ptr // 指针
A=M // 指针指向的地址
M=D // 将 D 的值写入指针指向的地址
```

## 05
