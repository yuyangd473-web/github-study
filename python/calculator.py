print("简单计算器")

def calculate():
    try:
        num1 = float(input("请输入第一个数字: "))
    except ValueError:
        print("输入错误，请输入数字！")
        return False

    operator = input("请输入运算符(+ - * /): ")
    try:
        num2 = float(input("请输入第二个数字: "))
    except ValueError:
        print("输入错误，请输入数字！")
        return False

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
            result = "错误：不能除以0"

    else:
        result = "错误：未知运算符"

    print("结果:", result)
    return True
while True:
    success = calculate()

    if not success:
        continue

    again = input("是否继续计算？(y/n): ")

    if again.lower() != "y":
        print("感谢使用简单计算器，再见！")
        break
