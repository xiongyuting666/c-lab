import ATM_module


# 主菜单：显示操作选项，读取用户选择
def PrintMenu() -> int:
    print("--------------------------------")
    print("***    您好，欢迎来到银行ATM，请选择操作：")
    print("查询余额  【输入1】")
    print("存款      【输入2】")
    print("取款      【输入3】")
    print("退出      【输入4】")
    print("请输入您的选择：", end="")
    choice = input()
    if not choice.isdigit(): # 判断是不是数字字符串
        print("输入无效，请输入数字 1-4")
        return -1
    return int(choice)


# 读取金额
# 这里只负责把输入转成数字，具体金额是否合法交给各个功能函数自己判断
def ReadMoney(prompt: str) -> int:
    text = input(prompt)
    try:
        money = int(text)
    except ValueError:
        print("输入无效，请输入正确的金额")
        return -1
    return money


# 查询余额
def DoCheckBalance():
    ATM_module.CheckBalance()


# 存款
def DoDeposit():
    money = ReadMoney("请输入存款金额：")
    if money < 0:
        return
    ATM_module.Deposit(money)


# 取款
def DoWithdraw():
    money = ReadMoney("请输入取款金额：")
    if money < 0:
        return
    ATM_module.WithdrawCash(money)


# 主流程
def Main():
    # 初始金额 5000，无需密码
    userA = ATM_module.User("userA", 5000)
    ATM_module.EnterSystem(userA)

    print("userA已登录")

    # 菜单循环
    while True:
        choice = PrintMenu()
        if choice == 1:
            DoCheckBalance()
        elif choice == 2:
            DoDeposit()
        elif choice == 3:
            DoWithdraw()
        elif choice == 4:
            ATM_module.ExitSystem()
            print("感谢使用，再见！")
            break
        else:
            if choice != -1:
                print("无效的选择，请输入 1-4")
        print()


if __name__ == "__main__":
    Main()


