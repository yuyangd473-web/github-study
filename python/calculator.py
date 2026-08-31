import ast
import json
import math
from pathlib import Path

HISTORY_FILE = Path(__file__).resolve().parent / "history.json"
EXPR_OPERATOR = "="

print("简单计算器")

def show_about():
    print("\n关于:")
    print("这是一个简单的计算器程序，可以进行加、减、乘、除运算。")
    print("你可以输入两个数字和一个运算符来计算结果。")
    print("此外，你还可以查看历史记录或清空历史记录。")
    print("版本1.0,作者: dyy,一个用于学习python的简单计算器项目")

def show_menu():
    print("\n请选择操作:")
    print("1. 计算两个数字")
    print("2. 查看历史记录")
    print("3. 清空历史记录")
    print("4. 关于")
    print("5. 单个数运算 (sqrt / abs)")
    print("6. 表达式计算")
    print("7. 退出")

def check_easter_eggs(result):
    # 检查彩蛋
    if result == 42:
        print(" 42 是生命、宇宙以及一切的答案！")
    elif result == 3.14:
        print(" 3.14 是圆周率的近似值！")
    elif result == 0:
        print(" 0 是一个神奇的数字！")
    elif result == 67:
         print("Six Seven!!!")
    elif result == 69:
        print("Nice.")
    elif result == 404:
        print("Error 404: Result Not Found.")
    elif result == 666:
         print("666,牛逼")
    elif result == 777:
        print("Lucky Seven!")
    elif result == 233:
         print("233,哈哈哈")
    elif result == 2077:
        print("Wake up, calculator.")
    elif result == 114514:
         print("1919810")
    elif result == 1919810:
         print("114514") 
    elif result == 123456:
        print("Are you testing the calculator?")
    elif result == 123456789:
        print("Counting is easy.")

def check_count_easter_egg(count):
    if count == 10:
        print("已经计算 10 次了！")

    elif count == 20:
        print("你似乎越来越依赖这个计算器了。")

    elif count == 30:
        print("30 次。你的计算能力正在觉醒。")

    elif count == 40:
        print("40 次。计算器已经成为你的好朋友。")

    elif count == 50:
        print("50 次！半百达成！")

    elif count == 60:
        print("60 次。你还在坚持。")

    elif count == 70:
        print("70 次。计算能力 MAX!")

    elif count == 80:
        print("80 次。你真的很喜欢算东西。")

    elif count == 90:
        print("90 次。距离 100 次只差一步！")

    elif count == 100:
        print("100 次！！！里程碑达成！")

def check_error_easter_egg(count):
    if count == 3:
        print("连续错误 3 次。你还好吗？")

    elif count == 5:
        print("连续错误 5 次。计算器已经开始沉默。")

    elif count == 10:
        print("连续错误 10 次。建议检查一下你的输入。")

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


def evaluate_expression(expr):
    try:
        tree = ast.parse(expr, mode="eval")
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

if __name__ == '__main__':
    history = load_history()
    calculation_count = 0
    error_count = 0
    try:
        while True:
            show_menu()
            choice = input("请输入选项: ")

            if choice == "1":
                a, b = get_two_numbers()
                result, operator = calculate(a, b)

                if result is None:
                    error_count += 1
                    check_error_easter_egg(error_count)
                    continue
                check_easter_eggs(result)
                history.append((a, operator, b, result))
                save_history(history)
                calculation_count += 1
                check_count_easter_egg(calculation_count)
                error_count = 0
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

                if result is None:
                    error_count += 1
                    check_error_easter_egg(error_count)
                    continue
                check_easter_eggs(result)
                history.append((num, operator, None, result))
                save_history(history)
                calculation_count += 1
                check_count_easter_egg(calculation_count)
                error_count = 0
            elif choice == "6":
                expr = input("请输入表达式: ").strip()
                result, entry = evaluate_expression(expr)

                if result is None:
                    error_count += 1
                    check_error_easter_egg(error_count)
                    continue
                check_easter_eggs(result)
                history.append(entry)
                save_history(history)
                calculation_count += 1
                check_count_easter_egg(calculation_count)
                error_count = 0
            elif choice == "7":
                print(f"总共进行了 {calculation_count} 次计算。")
                print("感谢使用简单计算器，再见！")
                break
            else:
                print("输入错误，请输入 1、2、3、4、5、6 或 7。")
    except (EOFError, KeyboardInterrupt):
        print("\n感谢使用简单计算器，再见！")
       