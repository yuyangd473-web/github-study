print("简单计算器")

while True:
    num1 = float(input("请输入第一个数字: "))
    operator = input("请输入运算符(+ - * /): ")
    num2 = float(input("请输入第二个数字: "))

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