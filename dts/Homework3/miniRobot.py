from robot import Robot, RobotType, RobotStatus, Battery


class MiniRobot(Robot):
    """迷你机器人：电量上限更低，且没有打扫、跳舞这类重活"""

    def __init__(self, name: str,
                 type: RobotType = RobotType.TypeC,
                 status: RobotStatus = RobotStatus.NORMAL):
        super().__init__(name, type, status)
        self.battery = Battery(50)      # 小电池，上限也只有 50

    def show_info(self) -> None:
        """重写：加一行机型标记"""
        print(f"【迷你】", end="")
        super().show_info()

    def work(self, behavior) -> bool:
        """重写：迷你机器人电量低于 10 就先罢工"""
        if self.battery.energy < 10:
            print(f"{self.name} 电量太低（{self.battery.energy}），迷你机器人罢工了")
            return False
        return super().work(behavior)

    def self_destruct(self, code: str) -> bool:
        """
        自爆：需要正确的引爆密码，且不能已经离线。
        成功后电量清零、状态置为离线，返回 True。
        """
        if self.status == RobotStatus.OFFLINE:
            print(f"{self.name} 已经离线，无法自爆")
            return False
        if code != self.DETONATE_CODE:
            print(f"{self.name} 引爆密码错误，自爆取消")
            return False

        print(f"{self.name} 自爆倒计时：3...2...1...💥")
        self.battery.energy = 0
        self.destroy()          # 复用父类的销毁逻辑，统一维护存活计数
        return True

    DETONATE_CODE: str = "1234"     # 引爆密码
