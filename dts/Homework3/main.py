from robot import Robot, RobotType, RobotStatus
from miniRobot import MiniRobot
from behaviorImplement import Run, Walk, Jump, Clean, Sleep, Dance


def main() -> None:
    # ========== 1. 创建机器人（用列表保存，至少 3 个，含 mini） ==========
    robots: list[Robot] = [
        Robot("小爱", RobotType.TypeA),
        Robot("小工", RobotType.TypeB, RobotStatus.ERROR),   # 开局就是故障
        Robot("小懒", RobotType.TypeC),
        MiniRobot("小咪"),                                    # 迷你机器人
        MiniRobot("小呆"),                                    # 迷你机器人
    ]

    print("=" * 40)
    print(f"创建完成，共 {len(robots)} 台，存活计数 = {Robot.alive_count()}")
    print("=" * 40)

    # ========== 2. 显示所有机器人信息 ==========
    print("\n>>> 批量显示信息（MiniRobot 会重写 show_info）")
    for r in robots:
        r.show_info()

    # ========== 3. 执行各种行为（cost 各不相同） ==========
    print("\n>>> 依次执行所有行为")
    for behavior in (Walk(), Run(), Jump(), Clean(), Dance(), Sleep()):
        robots[0].work(behavior)

    # ========== 4. 不同机器人执行同一行为（多态：work 都走父类接口） ==========
    print("\n>>> 不同机器人执行同一个 Run 行为")
    run = Run()
    for r in robots:
        r.work(run)

    # ========== 5. 充电（过充测试：MiniRobot 小电池一样能充到上限） ==========
    print("\n>>> 充电测试")
    robots[0].charge(50)
    robots[0].charge(999)        # 暴力充电，Battery 截断
    robots[3].charge(999)        # 迷你机器人也暴力充

    # ========== 6. 电量不足 ==========
    print("\n>>> 电量不足场景")
    robots[0].battery.energy = 3
    robots[0].work(Clean())      # cost 30，不够
    robots[0].work(Sleep())      # cost 1，够电但返回 False

    # ========== 7. MiniRobot 特有：低电量罢工 ==========
    print("\n>>> 迷你机器人低电量罢工（重写 work）")
    robots[3].battery.energy = 5
    robots[3].work(Walk())

    # ========== 8. Battery 校验（外部直接赋值非法值会被拦） ==========
    print("\n>>> 电量校验")
    try:
        robots[0].battery.energy = -10
    except ValueError as e:
        print("拦截负数 ->", e)
    print("过充不报错，被截断 ->", end=" ")
    robots[0].battery.energy = 999
    print(robots[0].battery)

    # ========== 9. 销毁 / 自爆，观察计数变化 ==========
    print("\n>>> 销毁与自爆")
    print("销毁前存活 =", Robot.alive_count())

    robots[0].destroy()                       # 普通销毁
    robots[0].destroy()                       # 重复销毁，应被幂等保护拦住
    print("销毁 1 台后存活 =", Robot.alive_count())

    robots[3].self_destruct("0000")           # 密码错误
    robots[3].self_destruct("1234")           # 正确，自爆
    print("自爆 1 台后存活 =", Robot.alive_count())

    # ========== 10. 遍历列表，统计状态 ==========
    print("\n>>> 最终状态汇总")
    for r in robots:
        mark = "（已离线）" if r.status == RobotStatus.OFFLINE else ""
        print(f"  {r.name:<4} {type(r).__name__:<10} {r.status.value:<4} {r.battery}{mark}")

    alive = sum(1 for r in robots if r.status != RobotStatus.OFFLINE)
    print(f"\n列表中共 {len(robots)} 台，其中存活 {alive} 台，全局计数 {Robot.alive_count()}")

    # ========== 11. 离线机器人无法工作 ==========
    print("\n>>> 离线机器人工作测试")
    robots[0].work(Run())


if __name__ == "__main__":
    main()
