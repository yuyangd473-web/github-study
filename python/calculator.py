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
    operator = input("请输入运算符(+ - * /): ")

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
            return False

    else:
        print("错误：未知运算符")
        return False
    print("结果:", result)
    return True


if __name__ == '__main__':
    while True:
        a, b = get_two_numbers()
        success = calculate(a, b)

        if not success:
            continue

        again = input("是否继续计算？(y/n): ")

        if again.lower() != "y":
            print("感谢使用简单计算器，再见！")
            break
