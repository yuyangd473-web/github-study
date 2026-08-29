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
    print("5. 退出")

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
        result = num1 ** num2

    else:
        print("错误：未知运算符")
        return None, None

    print("结果:", format_number(result))
    return result, operator





def show_history(history):
    if not history:
        print("没有历史记录。")
        return

    print("\n历史记录:")
    for i, (num1, operator, num2, result) in enumerate(history, start=1):
       print(f"{i}: {format_number(num1)} {operator} {format_number(num2)} = {format_number(result)}")

if __name__ == '__main__':
    history = []
    calculation_count = 0
    error_count = 0
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
            calculation_count += 1
            check_count_easter_egg(calculation_count)
            error_count = 0
        elif choice == "2":
            show_history(history)
        elif choice == "3":
            again = input("是否清空历史记录？(y/n): ")
            if again.lower() == "y":
                history.clear()
                print("历史记录已清空。")
        elif choice == "4":
            show_about()
        elif choice == "5":
            print(f"总共进行了 {calculation_count} 次计算。")
            print("感谢使用简单计算器，再见！")
            break
        else:
            print("输入错误，请输入 1、2、3、4 或 5。")
       