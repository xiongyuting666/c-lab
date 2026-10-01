from behavior import Behavior


class Run(Behavior):
    def __init__(self):
        super().__init__(20)

    def work(self) -> bool:
        print("很努力的run了，cost 20")
        return True


class Walk(Behavior):
    def __init__(self):
        super().__init__(5)

    def work(self) -> bool:
        print("悠闲地走了走，cost 5")
        return True


class Jump(Behavior):
    def __init__(self):
        super().__init__(15)

    def work(self) -> bool:
        print("高高地跳了一下，cost 15")
        return True


class Clean(Behavior):
    def __init__(self):
        super().__init__(30)

    def work(self) -> bool:
        print("认真地打扫了房间，cost 30")
        return True


class Sleep(Behavior):
    def __init__(self):
        super().__init__(1)

    def work(self) -> bool:
        print("呼呼大睡，几乎不耗电，cost 1")
        return False      # 睡着了，没干活，返回 False


class Dance(Behavior):
    def __init__(self):
        super().__init__(40)

    def work(self) -> bool:
        print("跳了一支舞，cost 40")
        return True