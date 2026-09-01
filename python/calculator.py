import ast
import json
import math
from pathlib import Path

HISTORY_FILE = Path(__file__).resolve().parent / "history.json"
EXPR_OPERATOR = "="

def show_about():
    print("\n关于:")
    print("这是一个简单的计算器程序，可以进行加、减、乘、除运算。")
    print("你可以输入两个数字和一个运算符来计算结果。")
    print("此外，你还可以查看历史记录或清空历史记录。")
    print("版本1.2,作者: dyy,一个用于学习python的简单计算器项目")

def show_menu():
    print("\n请选择操作:")
    print("1. 计算两个数字")
    print("2. 查看历史记录")
    print("3. 清空历史记录")
    print("4. 关于")
    print("5. 单个数运算 (sqrt / abs)")
    print("6. 表达式计算")
    print("7. 删除历史记录")
    print("8. 撤销上一条历史记录")
    print("9. 退出")

def check_easter_eggs(result):
    # 检查彩蛋
    if result == 42:
        return " 42 是生命、宇宙以及一切的答案！"
    if result == 3.14:
        return " 3.14 是圆周率的近似值！"
    if result == 0:
        return " 0 是一个神奇的数字！"
    if result == 67:
        return "Six Seven!!!"
    if result == 69:
        return "Nice."
    if result == 404:
        return "Error 404: Result Not Found."
    if result == 666:
        return "666,牛逼"
    if result == 777:
        return "Lucky Seven!"
    if result == 233:
        return "233,哈哈哈"
    if result == 2077:
        return "Wake up, calculator."
    if result == 114514:
        return "1919810"
    if result == 1919810:
        return "114514"
    if result == 123456:
        return "Are you testing the calculator?"
    if result == 123456789:
        return "Counting is easy."
    return None

def check_count_easter_egg(count):
    if count == 10:
        return "已经计算 10 次了！"
    if count == 20:
        return "你似乎越来越依赖这个计算器了。"
    if count == 30:
        return "30 次。你的计算能力正在觉醒。"
    if count == 40:
        return "40 次。计算器已经成为你的好朋友。"
    if count == 50:
        return "50 次！半百达成！"
    if count == 60:
        return "60 次。你还在坚持。"
    if count == 70:
        return "70 次。计算能力 MAX!"
    if count == 80:
        return "80 次。你真的很喜欢算东西。"
    if count == 90:
        return "90 次。距离 100 次只差一步！"
    if count == 100:
        return "100 次！！！里程碑达成！"
    return None

def check_error_easter_egg(count):
    if count == 3:
        return "连续错误 3 次。你还好吗？"
    if count == 5:
        return "连续错误 5 次。计算器已经开始沉默。"
    if count == 10:
        return "连续错误 10 次。建议检查一下你的输入。"
    return None

def format_number(number):
    if number.is_integer():
        return str(int(number))
    return f"{number:.6f}".rstrip('0').rstrip('.')

def get_number(prompt='请输入数字: '):
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print('输入错误，请输入数字！')


def get_two_numbers():
    num1 = get_number('请输入第一个数字: ')
    num2 = get_number('请输入第二个数字: ')
    return num1, num2


def calculate(num1, num2):
    operator = input("请输入运算符(+ - * / % // **): ").strip()

    if operator == "+":
        result = num1 + num2

    elif operator == "-":
        result = num1 - num2

    elif operator == "*":
        result = num1 * num2

    elif operator == "/":
        if num2 != 0:
            result = num1 / num2
        else:
            print("错误:不能除以0")
            return None, None

    elif operator == "%":
        if num2 != 0:
            result = num1 % num2
        else:
            print("错误:不能对0取模")
            return None, None

    elif operator == "//":
        if num2 != 0:
            result = num1 // num2
        else:
            print("错误:不能除以0")
            return None, None

    elif operator == "**":
        if num1 == 0 and num2 < 0:
            print("错误:0的负数次幂")
            return None, None
        if num1 < 0 and not num2.is_integer():
            print("错误:不能对负数进行非整数次幂")
            return None, None
        try:
            result = num1 ** num2
        except OverflowError:
            print("错误:数值过大")
            return None, None

    else:
        print("错误：未知运算符")
        return None, None

    if not math.isfinite(result):
        print("错误:结果为无穷大或非数值")
        return None, None

    print("结果:", format_number(result))
    return result, operator




def calculate_unary():
    operator = input("请输入运算符(sqrt abs): ").strip()

    if operator not in ("sqrt", "abs"):
        print("错误：未知运算符")
        return None, None, None

    num = get_number('请输入数字: ')

    if operator == "sqrt":
        if num < 0:
            print("错误:不能对负数开平方根")
            return None, None, None
        result = math.sqrt(num)
    else:
        result = abs(num)

    if not math.isfinite(result):
        print("错误:结果为无穷大或非数值")
        return None, None, None

    print("结果:", format_number(result))
    return result, operator, num


class _ExpressionError(Exception):
    pass


def _eval_ast(node):
    if isinstance(node, ast.Constant):
        if isinstance(node.value, bool) or not isinstance(node.value, (int, float)):
            raise _ExpressionError("非法表达式")
        return float(node.value)

    if isinstance(node, ast.Name):
        if node.id == "pi":
            return math.pi
        if node.id == "e":
            return math.e
        raise _ExpressionError("非法表达式")

    if isinstance(node, ast.BinOp):
        left = _eval_ast(node.left)
        right = _eval_ast(node.right)

        if isinstance(node.op, ast.Add):
            return left + right
        if isinstance(node.op, ast.Sub):
            return left - right
        if isinstance(node.op, ast.Mult):
            return left * right
        if isinstance(node.op, ast.Div):
            if right == 0:
                raise _ExpressionError("不能除以0")
            return left / right
        if isinstance(node.op, ast.FloorDiv):
            if right == 0:
                raise _ExpressionError("不能除以0")
            return left // right
        if isinstance(node.op, ast.Mod):
            if right == 0:
                raise _ExpressionError("不能对0取模")
            return left % right
        if isinstance(node.op, ast.Pow):
            if left == 0 and right < 0:
                raise _ExpressionError("0的负数次幂")
            if left < 0 and not right.is_integer():
                raise _ExpressionError("不能对负数进行非整数次幂")
            return left ** right
        raise _ExpressionError("非法表达式")

    if isinstance(node, ast.UnaryOp):
        operand = _eval_ast(node.operand)
        if isinstance(node.op, ast.USub):
            return -operand
        if isinstance(node.op, ast.UAdd):
            return +operand
        raise _ExpressionError("非法表达式")

    if isinstance(node, ast.Call):
        if (isinstance(node.func, ast.Name)
                and node.func.id in ("sqrt", "abs", "sin", "cos", "tan", "log", "ln")
                and len(node.args) == 1
                and not node.keywords):
            value = _eval_ast(node.args[0])
            name = node.func.id
            if name == "sqrt":
                if value < 0:
                    raise _ExpressionError("不能对负数开平方根")
                return math.sqrt(value)
            if name == "abs":
                return abs(value)
            if name == "sin":
                return math.sin(value)
            if name == "cos":
                return math.cos(value)
            if name == "tan":
                return math.tan(value)
            if name == "log":
                if value <= 0:
                    raise _ExpressionError("log 的参数必须大于0")
                return math.log10(value)
            if name == "ln":
                if value <= 0:
                    raise _ExpressionError("ln 的参数必须大于0")
                return math.log(value)
        raise _ExpressionError("非法表达式")

    raise _ExpressionError("非法表达式")


def _scan_number(expr, start):
    i = start
    n = len(expr)

    if expr[i] == ".":
        i += 1
        while i < n and expr[i].isdigit():
            i += 1
    else:
        while i < n and expr[i].isdigit():
            i += 1
        if i < n and expr[i] == ".":
            i += 1
            while i < n and expr[i].isdigit():
                i += 1

    if i < n and expr[i] in "eE":
        j = i + 1
        if j < n and expr[j] in "+-":
            j += 1
        if j < n and expr[j].isdigit():
            i = j
            while i < n and expr[i].isdigit():
                i += 1

    return i


def _convert_degrees(expr):
    out = []
    i = 0
    n = len(expr)

    while i < n:
        ch = expr[i]
        if ch.isdigit() or (ch == "." and i + 1 < n and expr[i + 1].isdigit()):
            end = _scan_number(expr, i)
            number = expr[i:end]
            if end < n and expr[end] == "°":
                if i > 0 and (expr[i - 1].isalpha() or expr[i - 1] == "_"):
                    raise _ExpressionError("° 前不能紧跟函数名或变量")
                out.append(f"({number}*pi/180)")
                i = end + 1
            else:
                out.append(number)
                i = end
        else:
            out.append(ch)
            i += 1

    return "".join(out)


def evaluate_expression(expr):
    try:
        tree = ast.parse(_convert_degrees(expr), mode="eval")
        result = _eval_ast(tree.body)
    except SyntaxError:
        print("错误:表达式语法错误")
        return None, None
    except _ExpressionError as e:
        print(f"错误:{e}")
        return None, None
    except ZeroDivisionError:
        print("错误:不能除以0")
        return None, None
    except OverflowError:
        print("错误:数值过大")
        return None, None
    except RecursionError:
        print("错误:表达式过于复杂")
        return None, None
    except ValueError:
        print("错误:参数超出定义域")
        return None, None

    if not math.isfinite(result):
        print("错误:结果为无穷大或非数值")
        return None, None

    print("结果:", format_number(result))
    return result, (expr, EXPR_OPERATOR, None, result)





def show_history(history):
    if not history:
        print("没有历史记录。")
        return

    print("\n历史记录:")
    for i, (num1, operator, num2, result) in enumerate(history, start=1):
        if operator == EXPR_OPERATOR:
            print(f"{i}: {num1} = {format_number(result)}")
        elif num2 is None:
            print(f"{i}: {operator}({format_number(num1)}) = {format_number(result)}")
        else:
            print(f"{i}: {format_number(num1)} {operator} {format_number(num2)} = {format_number(result)}")

def load_history():
    if not HISTORY_FILE.exists():
        return []

    try:
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
    except (json.JSONDecodeError, OSError):
        print("警告:历史记录文件损坏，已忽略。")
        return []

    if not isinstance(data, list):
        print("警告:历史记录文件格式错误，已忽略。")
        return []

    history = []
    for entry in data:
        if isinstance(entry, (list, tuple)) and len(entry) == 4:
            history.append(tuple(entry))
        else:
            print("警告:历史记录中存在无效条目，已忽略。")
    return history

def save_history(history):
    try:
        text = json.dumps(history, ensure_ascii=False, indent=2, allow_nan=False)
        with open(HISTORY_FILE, "w", encoding="utf-8") as f:
            f.write(text)
    except (OSError, ValueError):
        print("警告:历史记录保存失败。")

def delete_history_entry_at(history, index):
    if not history:
        print("没有历史记录。")
        return None

    if index < 1 or index > len(history):
        print("错误:编号不存在。")
        return None

    removed = history.pop(index - 1)
    save_history(history)
    print(f"已删除第 {index} 条历史记录。")
    show_history(history)
    return removed

def delete_history_entry(history):
    if not history:
        print("没有历史记录。")
        return None

    show_history(history)
    choice = input("请输入要删除的编号: ").strip()

    try:
        index = int(choice)
    except ValueError:
        print("错误:请输入有效的编号。")
        return None

    return delete_history_entry_at(history, index)

def undo_history(history):
    if not history:
        print("没有可撤销的历史记录。")
        return None

    removed = history.pop()
    save_history(history)
    print("已撤销上一条历史记录。")
    show_history(history)
    return removed

COMMANDS = {"history", "undo", "delete", "clear", "help", "about", "exit", "quit", "menu"}

def classify_line(line):
    text = line.strip()
    if not text:
        return ("blank", None)

    parts = text.split(maxsplit=1)
    name = parts[0].lower()
    rest = parts[1].strip() if len(parts) > 1 else ""

    if name in COMMANDS:
        return ("command", name, rest)
    return ("expression", text)

def run_command(history, name, rest):
    if name == "history":
        show_history(history)
    elif name == "undo":
        undo_history(history)
    elif name == "delete":
        if not rest:
            print("用法: delete <编号>")
        else:
            try:
                index = int(rest)
            except ValueError:
                print("错误:请输入有效的编号。")
            else:
                delete_history_entry_at(history, index)
    elif name == "clear":
        again = input("是否清空历史记录？(y/n): ")
        if again.lower() == "y":
            history.clear()
            save_history(history)
            print("历史记录已清空。")
    elif name == "help":
        print("可用命令:")
        print("  history        查看历史记录")
        print("  undo           撤销上一条历史记录")
        print("  delete <编号>  删除指定历史记录")
        print("  clear          清空历史记录")
        print("  about          关于")
        print("  menu           进入旧菜单")
        print("  exit / quit    退出")
        print("直接输入表达式即可计算，例如: 12 + 5、sqrt(144)")
    elif name == "about":
        show_about()
    elif name == "exit":
        return "exit"
    elif name == "quit":
        return "exit"
    elif name == "menu":
        return "menu"
    return "continue"

calculation_count = 0
error_count = 0


def record_result(result):
    global calculation_count, error_count

    messages = []
    if result is None:
        error_count += 1
        message = check_error_easter_egg(error_count)
        if message:
            messages.append(message)
        return messages

    message = check_easter_eggs(result)
    if message:
        messages.append(message)
    calculation_count += 1
    message = check_count_easter_egg(calculation_count)
    if message:
        messages.append(message)
    error_count = 0
    return messages


def print_messages(messages):
    for message in messages:
        print(message)


def handle_expression(history, line):
    expr = line.strip()
    result, entry = evaluate_expression(expr)
    messages = record_result(result)

    if result is None:
        print_messages(messages)
        return

    history.append(entry)
    save_history(history)
    print_messages(messages)


def run_menu_loop(history):
    while True:
        show_menu()
        choice = input("请输入选项: ")

        if choice == "1":
            a, b = get_two_numbers()
            result, operator = calculate(a, b)
            messages = record_result(result)

            if result is None:
                print_messages(messages)
                continue
            history.append((a, operator, b, result))
            save_history(history)
            print_messages(messages)
        elif choice == "2":
            show_history(history)
        elif choice == "3":
            again = input("是否清空历史记录？(y/n): ")
            if again.lower() == "y":
                history.clear()
                save_history(history)
                print("历史记录已清空。")
        elif choice == "4":
            show_about()
        elif choice == "5":
            result, operator, num = calculate_unary()
            messages = record_result(result)

            if result is None:
                print_messages(messages)
                continue
            history.append((num, operator, None, result))
            save_history(history)
            print_messages(messages)
        elif choice == "6":
            expr = input("请输入表达式: ").strip()
            result, entry = evaluate_expression(expr)
            messages = record_result(result)

            if result is None:
                print_messages(messages)
                continue
            history.append(entry)
            save_history(history)
            print_messages(messages)
        elif choice == "7":
            delete_history_entry(history)
        elif choice == "8":
            undo_history(history)
        elif choice == "9":
            return
        else:
            print("输入错误，请输入 1、2、3、4、5、6、7、8 或 9。")


def run_cli():
    global calculation_count, error_count

    history = load_history()
    calculation_count = 0
    error_count = 0

    print("简单计算器")
    print("输入 help 查看帮助。")

    try:
        while True:
            line = input(">>> ")

            kind, *rest = classify_line(line)

            if kind == "blank":
                continue

            if kind == "command":
                name, args = rest
                action = run_command(history, name, args)
                if action == "exit":
                    print(f"总共进行了 {calculation_count} 次计算。")
                    print("感谢使用简单计算器，再见！")
                    return
                if action == "menu":
                    run_menu_loop(history)
                continue

            handle_expression(history, line)
    except (EOFError, KeyboardInterrupt):
        print("\n感谢使用简单计算器，再见！")


if __name__ == '__main__':
    run_cli()