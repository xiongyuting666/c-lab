dist_log = [56, 22, 8, 91, 44, 15, 77]


def AddData(a: int):
    dist_log.append(a)


def printData():
    print(f"-" * 20)
    for data in dist_log:
        print(f"当前检测距离：{data} cm，数据类型：{type(data)}")
    print(f"-" * 20)


def dataCheak():
    print(f"-" * 20)
    for data in dist_log:
        if data < 0:
            print(f"数据异常：{data}")
            continue
        print(f"当前检测距离：{data} cm，数据类型：{type(data)}")
    print(f"-" * 20)


def dataClassification():
    print(f"-" * 20)
    for data in dist_log:
        if data < 0:
            print(f"数据异常：{data}")
            continue

        if (data <= 10):
            print(f"紧急避让：{data}")
        elif (data <= 30):
            print(f"谨慎行驶：{data}")
        else:
            print(f"正常运行：{data}")
    print(f"-" * 20)


def dataStatistics():
    print(f"-" * 20)

    count_10less = []
    count_30less = []
    count_safe = []
    count_unsafe = []

    for data in dist_log:
        if data < 0:
            count_unsafe.append(data)
            continue

        if (data <= 10):
            count_10less.append(data)
        elif (data <= 30):
            count_30less.append(data)
        else:
            count_safe.append(data)

    valid_total = len(count_10less) + len(count_30less) + len(count_safe)

    print(f"====设备日志数据分析报告====")
    print(f"危险数据次数：{len(count_10less)} 次")
    print(f"近距离数据次数：{len(count_30less)} 次")
    print(f"安全数据次数：{len(count_safe)} 次")
    print(f"有效数据总次数：{valid_total} 次")
    
    # 没有有效数据时避免除以 0
    if valid_total > 0:
        average = (sum(count_10less) + sum(count_30less) + sum(count_safe)) / valid_total
        print(f"本次检测平均距离：{average:.2f} cm")
    else:
        print(f"本次检测平均距离：无有效数据")
    print(f"异常数据条数：{len(count_unsafe)} 条")


def main() -> None:
    AddData(-5)
    printData()
    dataCheak()
    dataClassification()
    dataStatistics()


if __name__ == "__main__":
    main()
