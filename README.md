# GitHub Study

## 📖 项目介绍

这是我学习 Git、Python 和通信工程编程的仓库。

## 📚 学习内容

- Git
- GitHub
- Markdown
- Python

## 🎯 我的目标

- 学会 Git
- 学会 Python
- 做自己的项目

## 📝 学习记录

- 2026-08-03：开始使用 VS Code 学习 Git
- 完成第一次 GitHub 上传

# 🧮 Python 简单计算器  2026.8.29

这是我的第一个 Python 小项目，也是我用来学习 Python、Git 和 GitHub 的练习项目。

目前已经从最基础的四则运算，逐步增加了历史记录、错误处理、计算统计、彩蛋以及 Windows `.exe` 打包等功能。


# 🧮 Python 简单计算器 · 2026.09.01

这是我的第一个 Python 小项目，也是我用来学习 Python、Git 和 GitHub 的练习项目。

项目最初只是一个简单的四则运算计算器，后来不断增加了历史记录、一元运算、表达式计算、数学函数、错误处理、计算统计、数字彩蛋、JSON 持久化以及 Windows `.exe` 打包等功能。

目前项目同时拥有：

- 命令行 REPL 计算器界面
- Tkinter 图形化计算器（GUI）
- pytest 自动化测试

这个项目会继续作为我的 Python 学习项目进行迭代。

## ✨ 当前功能

### 基础运算

- ➕ 加法 `+`
- ➖ 减法 `-`
- ✖️ 乘法 `*`
- ➗ 除法 `/`
- `%` 取余
- `//` 整除
- `**` 幂运算

### 一元运算

- `sqrt(x)` 开平方根
- `abs(x)` 绝对值

### 表达式计算

支持直接输入复杂数学表达式，例如：

```text
10 + 5 * 2
(10 + 5) * 2
2 ** 3 ** 2
sqrt(9) + 1
sin(pi / 2)
log(100)
支持：

括号
运算符优先级
幂运算右结合
单目正负号
嵌套函数
pi
e
sin()
cos()
tan()
log()（以 10 为底）
ln()（自然对数）

三角函数使用弧度制。

🛡️ 表达式安全解析

表达式计算没有使用 eval() 或 exec()。

程序使用 Python ast 模块解析表达式，并通过白名单限制允许的语法节点，只允许预先定义的数字、运算符、数学函数和常量。

例如：

__import__('os')
open('x')
math.sin(1)
foo(1)

等不在白名单中的表达式都会被拒绝。

📜 历史记录
自动保存计算历史
支持二元运算、一元运算和表达式计算
程序重新启动后仍然可以读取历史记录
支持清空历史记录
历史记录使用 JSON 文件保存

历史记录文件：

python/history.json

该文件已加入 .gitignore，不会上传到 GitHub。

⚠️ 错误处理

程序对常见错误进行了处理，包括：

除数为 0
0 的负数次幂
负数进行非整数次幂
负数开平方根
log() / ln() 非法参数
数值溢出
无穷大 / 非数值结果
非法表达式
过于复杂的表达式
错误的数字输入
Ctrl+C / Ctrl+Z 等中断

程序尽可能避免因为用户输入错误而直接崩溃。

🔢 计算统计
统计当前运行期间的计算次数
连续错误次数统计
计算次数彩蛋
连续错误彩蛋
🥚 数字彩蛋

程序中加入了一些我自己设计的数字彩蛋。

某些特殊计算结果会触发特殊输出。

如果你发现程序突然说了一些奇怪的话，那大概率不是程序坏了。😂

🪟 Windows .exe

项目使用 PyInstaller 打包为 Windows .exe 程序，可以直接运行。

🚀 如何运行
方法一：使用 Python（命令行 REPL）

需要 Python 3.14 或兼容版本。

进入 python 目录后运行：

uv run python calculator.py
方法二：使用 Python（图形界面 GUI）

进入 python 目录后运行：

uv run python gui.py
方法三：直接运行 Windows 程序

项目已经使用 PyInstaller 打包。

进入：

dist/

双击：

calculator.exe

即可运行。

注意：当前仓库中的 dist/calculator.exe 是早期打包的旧版命令行（CLI）程序，并不包含最新的图形化界面（GUI）。如需 GUI 的 .exe，需要以 gui.py 为入口重新打包。

📁 项目结构
python/
├── calculator.py
├── gui.py
├── 计算器获取数字部分.py
├── pyproject.toml
├── uv.lock
├── tests/
│   ├── test_calculator.py
│   └── test_gui.py
├── calculator.spec
├── dist/
│   └── calculator.exe
├── .gitignore
└── README.md

运行计算器后产生的：

history.json

不会被 Git 跟踪。

📚 项目目的

这个项目主要用于记录我学习 Python、Git 和 GitHub 的过程。

通过不断给计算器增加功能，我逐渐学习了：

Python 基础语法
条件判断
循环
函数
异常处理
列表与元组
文件读写
JSON
pathlib
math
ast
表达式解析
安全白名单
uv
Git
GitHub
PyInstaller
Windows .exe 打包

相比一开始的简单四则运算，这个项目已经逐渐变成了一个功能比较完整的小型命令行计算器。

这个项目还会继续更新。
🔮 后续计划
 增加更完善的计算功能
 优化代码结构
 使用字典重构彩蛋系统
 进一步优化 Windows 版本（含 GUI 打包）
📌 Version

Version 1.2

作者：dyy

一个正在学习 Python 的通信工程学生。