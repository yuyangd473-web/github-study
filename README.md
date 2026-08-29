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

## ✨ 当前功能

* ➕ 加法
* ➖ 减法
* ✖️ 乘法
* ➗ 除法
* `%` 取余
* `//` 整除
* `**` 幂运算
* 输入错误处理
* 除零错误处理
* 📜 历史记录
* 🗑️ 清空历史记录
* 🔢 计算次数统计
* 🥚 数字彩蛋
* 💀 连续错误彩蛋
* ℹ️ 关于页面
* 🔢 计算结果格式化
* 🪟 使用 PyInstaller 打包为 Windows `.exe`

## 🥚 彩蛋

程序中加入了一些我自己设计的数字彩蛋

此外还有计算次数和彩蛋，以及连续计算错误的彩蛋。

如果你发现了什么奇怪的输出，那大概率不是程序坏了。😂

## 🚀 如何运行

### 方法一：使用 Python

需要 Python 3.14 或兼容版本。

```bash
uv run python calculator.py
```

### 方法二：直接运行 Windows 程序

项目已经使用 PyInstaller 打包。

进入：

```text
dist/
```

双击：

```text
calculator.exe
```

即可运行，无需通过 VS Code 启动。

## 📁 项目结构

```text
python/
├── calculator.py
├── 计算器获取数字部分.py
├── pyproject.toml
├── uv.lock
├── calculator.spec
├── dist/
│   └── calculator.exe
└── README.md
```

## 📚 项目目的

这个项目主要用于记录我学习 Python 的过程。

通过不断给计算器增加功能，我逐渐学习了：

* Python 基础语法
* 条件判断
* 循环
* 函数
* 异常处理
* 列表与元组
* 文件与项目结构
* uv
* Git
* GitHub
* PyInstaller
* Windows `.exe` 打包

这个项目还会继续更新。

## 🔮 后续计划

* [ ] 增加更完善的计算功能
* [ ] 优化代码结构
* [ ] 使用字典重构彩蛋系统
* [ ] 保存历史记录到文件
* [ ] 制作图形化界面（GUI）
* [ ] 进一步优化 Windows 版本

---

**Version 1.1**

作者：dyy

一个正在学习 Python 的通信工程学生。
