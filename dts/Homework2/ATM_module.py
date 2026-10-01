import datetime
import random

from dataclasses import dataclass


# Python 3.7+ 标准库自带 dataclasses，专门用来写这种“数据类”，非常像结构体。
@dataclass
class User:
    userName: str
    money: int

currentUser: User = None
userOnline = False


# 生成一个随机的 6 位交易流水号，例如 000137、482910
# 不足 6 位前面补 0，保证永远是 6 位
def NextTSN()->str:
    return str(random.randint(0, 999999)).zfill(6)


# 统一的时间日志函数，所有 print 都通过它输出，自动带上时间戳
# TSN 是交易流水号，可选是否使用：为 True 时，日志前面会带上一个随机 6 位流水号
def Log(msg: str, TSN: bool = False):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if(TSN):
        print(f"[{now}] [流水号 {NextTSN()}] {msg}")
    else:
        print(f"[{now}] {msg}")


# 查询余额功能
def CheckBalance()->int:
    global currentUser
    if(not userOnline):
        Log("查询余额失败：当前无用户登录")
        return -1
    Log(f"查询余额：用户 {currentUser.userName} 当前余额为 {currentUser.money} 元")
    return currentUser.money


# 存款功能
def Deposit(money: int)->bool:
    if(not userOnline):
            Log("存款失败：当前无用户登录")
            return False
    if(money <= 0):
        Log(f"存款失败：存款金额 {money} 无效，必须大于 0")
        return False
    global currentUser
    currentUser.money += money
    Log(f"存款成功：用户 {currentUser.userName} 存入 {money} 元，当前余额为 {currentUser.money} 元", TSN=True)
    return True

# 取款功能
def WithdrawCash(money: int)->int:
    if(not userOnline):
        Log("取款失败：当前无用户登录")
        return -1
    global currentUser
    if(money <= 0):
        Log(f"取款失败：取款金额 {money} 无效，必须大于 0")
        return -3
    if(money > currentUser.money):
        Log(f"取款失败：用户 {currentUser.userName} 余额 {currentUser.money} 元，不足以取出 {money} 元")
        return -2
    currentUser.money -= money
    Log(f"取款成功：用户 {currentUser.userName} 取出 {money} 元，当前余额为 {currentUser.money} 元", TSN=True)
    return money

# 进入系统功能
def EnterSystem(user: User):
    global currentUser, userOnline
    if(userOnline):
        Log(f"检测到用户 {currentUser.userName} 已登录，先退出当前用户")
        ExitSystem()
    currentUser=user
    userOnline=True
    Log(f"进入系统成功：欢迎用户 {user.userName}，当前余额为 {user.money} 元")


# 退出系统功能
def ExitSystem():
    global currentUser,userOnline
    userOnline=False
    Log(f"退出系统成功：用户 {currentUser.userName} 已下线，感谢使用")
    currentUser = None
