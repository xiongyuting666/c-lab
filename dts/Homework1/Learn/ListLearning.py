# -*- coding: utf-8 -*-
"""Python 列表（list）基础示例

列表是 Python 中最常用的可变序列：
- 有序、可重复、可修改（增删改查）
- 可以存放任意类型的数据
"""


def basic_usage() -> None:
    """1. 创建列表与基本访问"""
    fruits = ["苹果", "香蕉", "橘子", "葡萄"]
    print("列表内容:", fruits)
    print("长度:", len(fruits))

    # 索引：正向从 0 开始，反向从 -1 开始
    print("第一个元素:", fruits[0])
    print("最后一个元素:", fruits[-1])

    # 切片 [start:stop:step]，左闭右开
    print("前两个:", fruits[:2])
    print("后两个:", fruits[-2:])
    print("反转:", fruits[::-1])


def add_and_remove() -> None:
    """2. 增删元素"""
    nums = [1, 2, 3]
    print("初始:", nums)

    nums.append(4)              # 末尾追加一个元素
    print("append(4):", nums)

    nums.insert(0, 0)           # 在指定位置插入
    print("insert(0, 0):", nums)

    nums.extend([5, 6])         # 追加多个元素
    print("extend([5, 6]):", nums)

    nums.remove(3)              # 删除第一个值为 3 的元素
    print("remove(3):", nums)

    last = nums.pop()           # 弹出末尾元素
    print(f"pop() -> {last}, 剩余:", nums)

    del nums[0]                 # 按索引删除
    print("del nums[0]:", nums)


def modify_and_query() -> None:
    """3. 修改与查询"""
    scores = [85, 92, 78, 96, 88]
    print("成绩:", scores)

    scores[0] = 90              # 按索引修改
    print("修改后:", scores)

    print("最大值:", max(scores))
    print("最小值:", min(scores))
    print("总和:", sum(scores))
    print("平均分:", sum(scores) / len(scores))

    print("92 在列表中吗:", 92 in scores)
    print("92 的索引:", scores.index(92))
    print("78 出现的次数:", scores.count(78))


def sort_and_reverse() -> None:
    """4. 排序与反转"""
    data = [3, 1, 4, 1, 5, 9, 2, 6]
    print("原始:", data)

    data.sort()                          # 原地升序排序
    print("sort() 升序:", data)

    data.sort(reverse=True)              # 原地降序排序
    print("sort(reverse=True):", data)

    data.reverse()                       # 原地反转
    print("reverse():", data)

    # sorted() 返回新列表，不改变原列表
    new_list = sorted(data)
    print("sorted() 新列表:", new_list)
    print("原列表不变:", data)


def iterate_list() -> None:
    """5. 遍历列表"""
    names = ["Tom", "Jerry", "Spike"]

    # 直接遍历元素
    for name in names:
        print("名字:", name)

    # enumerate 同时拿到索引和元素
    for i, name in enumerate(names):
        print(f"第 {i} 个: {name}")

    # 列表推导式：一行生成新列表
    # [表达式 for 变量 in 可迭代对象 if 条件]
    
    squares = [x * x for x in range(1, 6)]
    print("1~5 的平方:", squares)

    '''
    squares = []
    for x in range(1, 6):
        squares.append(x * x)
    '''

    even = [x for x in range(10) if x % 2 == 0]
    print("10 以内的偶数:", even)

    '''
    even = []
    for x in range(10):
        if x % 2 == 0:
            even.append(x)
    '''


def list_comprehension_more() -> None:
    """6. 嵌套列表与常用技巧"""
    matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    print("矩阵:", matrix)
    print("第二行:", matrix[1])
    print("第二行第三列:", matrix[1][2])

    # 展平嵌套列表
    flat = [num for row in matrix for num in row]
    print("展平后:", flat)

    # 拼接与复制
    print("列表拼接:", [1, 2] + [3, 4])
    print("重复 3 次:", [0] * 3)

    # 复制列表（注意：= 只是引用，要用 copy()）
    a = [1, 2, 3]
    b = a.copy()
    b.append(4)
    print("原列表 a:", a)
    print("副本 b:", b)


def main() -> None:
    print("=" * 30, "1. 创建与访问", "=" * 30)
    basic_usage()

    print("\n" + "=" * 30, "2. 增删元素", "=" * 30)
    add_and_remove()

    print("\n" + "=" * 30, "3. 修改与查询", "=" * 30)
    modify_and_query()

    print("\n" + "=" * 30, "4. 排序与反转", "=" * 30)
    sort_and_reverse()

    print("\n" + "=" * 30, "5. 遍历列表", "=" * 30)
    iterate_list()

    print("\n" + "=" * 30, "6. 嵌套与技巧", "=" * 30)
    list_comprehension_more()


if __name__ == "__main__":
    main()
