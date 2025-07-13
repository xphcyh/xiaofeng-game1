def add(x, y):
    return x + y

def subtract(x, y):
    return x - y

def multiply(x, y):
    return x * y

def divide(x, y):
    if y == 0:
        return "Error: Division by zero!"
    return x / y

def main():
    print("简单计算器：加(+), 减(-), 乘(*), 除(/)")
    while True:
        try:
            num1 = float(input("请输入第一个数字（或输入q退出）："))
        except ValueError:
            print("已退出计算器。")
            break
        op = input("请输入运算符 (+, -, *, /)：")
        try:
            num2 = float(input("请输入第二个数字："))
        except ValueError:
            print("输入无效，请重新输入。"); continue
        if op == '+':
            result = add(num1, num2)
        elif op == '-':
            result = subtract(num1, num2)
        elif op == '*':
            result = multiply(num1, num2)
        elif op == '/':
            result = divide(num1, num2)
        else:
            print("无效的运算符，请重新输入。"); continue
        print(f"结果: {result}\n")

if __name__ == "__main__":
    # 启动命令行或GUI，二选一
    print("1. 命令行计算器\n2. 图形界面计算器")
    choice = input("请选择模式（1/2）：")
    if choice == '2':
        launch_gui()
    else:
        main()
