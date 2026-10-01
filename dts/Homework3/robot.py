
from enum import Enum
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from behavior import Behavior


class RobotType(Enum):
    """机器人类型枚举"""
    TypeA = "RobotTypeA"
    TypeB = "RobotTypeB"
    TypeC = "RobotTypeC"


class RobotStatus(Enum):
    """机器人状态枚举"""
    NORMAL = "健康"
    ERROR = "故障"
    OFFLINE = "离线"

class Battery:
    """电池：外部直接读写 energy，校验在 setter 里做"""

    MAX_ENERGY: int = 100

    def __init__(self, energy: int = MAX_ENERGY):
        self.energy = energy          # 走 setter，创建时就校验

    @property
    def energy(self) -> int:
        return self.__energy

    @energy.setter
    def energy(self, value: int):
        if not isinstance(value, int):
            raise TypeError(f"电量必须是整数：{value!r}")
        if value < 0:
            raise ValueError(f"电量不能为负数：{value}")
        # 过充不报错，直接截断到上限（由电池自己兜底）
        self.__energy = min(value, Battery.MAX_ENERGY)

    def __str__(self) -> str:
        return f"Battery({self.energy}/{Battery.MAX_ENERGY})"


class Robot:

    countId: int = 0        # 已分配的 ID 序号（下一个要用的号）

    countRobot: int = 0     # 当前存活的机器人总数

    def __init__(self, name: str, type: RobotType, status: RobotStatus = RobotStatus.NORMAL):
        self.name = name
        self.type = type
        self.status = status
        self.battery = Battery(100)

        self.robot_id = Robot.countId
        Robot.countId += 1
        Robot.countRobot += 1

    def show_info(self) -> None:
        """显示机器人基本信息"""
        print(f"[ID={self.robot_id}] {self.name}")
        print(f"  类型：{self.type.value}")
        print(f"  状态：{self.status.value}")
        print(f"  电量：{self.battery}")

    def work(self, behavior: "Behavior") -> bool:
        """
        工作：执行一个行为，消耗该行为声明的电量。
        电量不足或状态异常时不能工作，返回 False。
        """
        if self.status != RobotStatus.NORMAL:
            print(f"{self.name} 当前状态为 {self.status.value}，无法工作")
            return False

        cost = behavior.cost
        if self.battery.energy < cost:
            print(f"{self.name} 电量不足（{self.battery.energy}<{cost}），无法工作")
            return False

        self.battery.energy -= cost
        ok = behavior.work()
        print(f"{self.name} 消耗 {cost} 电量，剩余 {self.battery.energy}，行为结果：{ok}")
        return ok

    def charge(self, amount: int = Battery.MAX_ENERGY) -> None:
        """充电：直接加电，过充由 Battery 截断"""
        before = self.battery.energy
        self.battery.energy += amount
        print(f"{self.name} 充电 {self.battery.energy - before}，当前电量 {self.battery.energy}")

    @staticmethod
    def alive_count() -> int:
        """当前存活的机器人总数（全类共享）"""
        return Robot.countRobot

    def destroy(self) -> None:
        """销毁：从存活计数中减一，并且只减一次"""
        if self.status == RobotStatus.OFFLINE:
            print(f"{self.name} 已经离线了")
            return
        self.status = RobotStatus.OFFLINE
        Robot.countRobot -= 1
        print(f"{self.name} 已销毁，存活数量：{Robot.countRobot}")