# Python 计算器

这是我的第一个 Python 小项目。

项目从最初只能完成简单四则运算的 CLI 计算器开始，在学习过程中一步步加入表达式计算、AST 安全解析、数学函数、历史记录、彩蛋、Tkinter GUI、角度后缀 `°` 和自动化测试，最终发展成一个功能相对完整的小型桌面计算器。

> 本仓库也用于记录我学习 Git、GitHub、Markdown 和 Python 的过程。

## 项目特色

- AST 白名单表达式解析，不使用 `eval()` / `exec()`
- CLI 与 GUI 共用同一套计算核心
- CLI 与 GUI 共用彩蛋和计数机制
- 历史记录 JSON 持久化
- `°` 角度后缀
- pytest 自动化测试
- PyInstaller Windows EXE 打包支持

## 功能

### 基础计算

- 加法 `+`
- 减法 `-`
- 乘法 `*`
- 除法 `/`
- 取余 `%`
- 整除 `//`
- 幂运算 `**`

### 数学函数与常量

- `sqrt(x)` 开平方根
- `abs(x)` 绝对值
- `sin(x)` / `cos(x)` / `tan(x)` 三角函数
- `log(x)` 以 10 为底的对数
- `ln(x)` 自然对数
- `pi` 圆周率
- `e` 自然常数

### 表达式计算

支持直接输入复杂表达式，支持括号和正常的运算优先级：

```text
12 + 5 * 2
sqrt(144)
sin(pi / 2)
sin(30°)
```

### ° 角度后缀

`°` 是数字字面量的角度后缀，会把前面的数字从角度换算为弧度后再参与计算：

```text
30°        -> π/6
sin(30°)   -> 0.5
cos(60°)   -> 0.5
tan(45°)   -> 1
```

- 函数形式需要写成 `sin(30°)`
- 不支持 `sin30°`、`sqrt9°` 这类标识符与数字 `°` 的隐式并置
- 没有 `°` 时，`sin` / `cos` / `tan` 仍然使用弧度制，例如 `sin(pi/2) = 1`

## 安全表达式解析

表达式计算**没有使用** `eval()` 或 `exec()`。

用户输入首先通过 Python `ast` 模块解析，然后由白名单限制允许的节点、运算符、函数和常量。这样可以避免直接执行用户输入，并将表达式能力限制在项目明确允许的范围内。

不在白名单中的表达式（如 `__import__('os')`、`open('x')`、`math.sin(1)`、`foo(1)`）都会被拒绝。

## 历史记录

- CLI 与 GUI 共用同一份历史记录
- 支持查看、删除、撤销和清空历史记录
- 使用 JSON 文件持久化（`history.json`）
- 普通 Python 运行时，历史记录保存在项目目录中的 `history.json`
- PyInstaller frozen 模式下，使用用户 `AppData` 下的 `calculator` 目录保存

`history.json` 已加入 `.gitignore`，不会提交到 Git。

## 彩蛋

项目内置了一些彩蛋，某些特殊结果或计数会触发特殊输出。例如：

- `42`
- `69`
- `2077`
- `114514`
- `1919810`

此外还有计算次数和连续错误次数相关的彩蛋，等你慢慢发现。

## GUI

使用 Tkinter 和 `ttk`（`clam` 主题）构建的简洁图形界面，包含：

- 表达式与结果显示区
- 数字、运算符、数学函数和 `°` 按钮
- 历史记录窗口
- 彩蛋提示
- 关于窗口（含作者信息）

支持键盘操作：

- `Enter` 计算
- `Backspace` 退格
- `Esc` 清空

## 运行方法

需要 Python 3.14 或兼容版本，使用 `uv` 管理。

### 命令行（CLI）

```bash
cd python
uv run python calculator.py
```

### 图形界面（GUI）

```bash
cd python
uv run python gui.py
```

## 打包 Windows EXE

项目支持使用 PyInstaller 自行打包 Windows GUI 程序：

```bash
cd python
uv run pyinstaller --noconsole --onefile --name Calculator gui.py
```

输出文件位于 `python/dist/Calculator.exe`。

> 当前仓库未发布打包好的 EXE，如需使用请自行打包。

## 测试

当前共有 229 个测试：

```text
229 passed
0 failed
0 warnings
```

测试覆盖：

- 表达式计算
- AST 安全边界
- 数学函数
- `°` 角度运算
- 历史记录
- 彩蛋与计数机制
- GUI 行为
- 键盘交互
- 关于窗口

运行测试：

```bash
cd python
uv run pytest
```

## 项目结构

```text
README.md
AGENTS.md
python/
├── calculator.py
├── gui.py
├── 计算器获取数字部分.py
├── pyproject.toml
├── uv.lock
├── .python-version
├── .gitignore
├── src/python/__init__.py
└── tests/
    ├── test_calculator.py
    └── test_gui.py
```

## 项目定位

这是一个个人 Python 学习项目，重点不是追求商业计算器的复杂功能，而是通过一个实际项目学习 Python、Git、GitHub、测试、GUI 开发、代码组织和软件迭代。

## 项目目的

这个项目主要用于记录我学习 Python、Git 和 GitHub 的过程，通过学习过程中不断给计算器增加功能来练习：

- Python 基础语法与异常处理
- 文件读写与 JSON
- `pathlib`、`math`、`ast`
- 表达式解析与安全白名单
- `uv`
- Git 与 GitHub
- PyInstaller 与 Windows EXE 打包

## 作者

作者：dyy

一个正在学习 Python 的通信工程学生。
