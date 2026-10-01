from abc import ABC, abstractmethod

# 抽象父类
class Behavior(ABC):
    def __init__(self,cost:int):
        self.__cost = cost
        pass

    @property
    def cost(self) -> int:
        return self.__cost

    @abstractmethod
    def work(self) -> bool:
        """工作行为"""
        raise NotImplementedError #抽象方法未实现的异常抛出