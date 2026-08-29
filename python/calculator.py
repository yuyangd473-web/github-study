print("简单计算器")
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
    operator = input("请输入运算符(+ - * /): ").strip()

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
            print("错误：不能除以0")
            return None,None

    else:
        print("错误：未知运算符")
        return None,None
    print("结果:", result)
    return result,operator
def show_history(history):
    if not history:
        print("没有历史记录。")
        return

    print("\n历史记录:")
    for i, (num1, operator, num2, result) in enumerate(history, start=1):
        print(f"{i}: {num1} {operator} {num2} = {result}")
if __name__ == '__main__':
    history = []
    while True:
        a, b = get_two_numbers()
        result, operator = calculate(a, b)

        if result is None:
            continue

        history.append((a, operator, b, result))
        again = input("是否继续计算？(y/h/n): ")

        if again.lower() == "h":
            show_history(history)
        elif again.lower() == "n":
            print("感谢使用简单计算器，再见！")
            break
