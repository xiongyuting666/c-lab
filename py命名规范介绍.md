Python 的命名规范，简单说就是：**不同类型的对象用不同的写法，让名字自己说明它是什么，别人（包括三个月后的自己）一眼就能看懂。**

官方依据是 [PEP 8 -- Style Guide for Python Code](https://peps.python.org/pep-0008/)，下面按常用程度整理。

---

## 1. 为什么要管命名

- 代码主要是给人读的，写的时间远小于改的时间
- 风格统一，review 时就不用吵“到底该用驼峰还是蛇形”
- 有工具能自动检查，规范了才能开自动检查

---

## 2. 四种基本风格

| 风格 | 写法 | 用在哪 |
| ---- | ---- | ------ |
| 蛇形 snake_case | 全小写，下划线分词 | 变量、函数、方法、模块、包 |
| 大驼峰 PascalCase | 每个单词首字母大写 | 类、异常、类型别名 |
| 全大写下划线 UPPER_CASE | 全大写，下划线分词 | 常量 |
| 下划线开头 / 结尾 | `_x`、`__x`、`__x__` | 私有约定、名称改写、魔术方法 |

```python
MAX_SIZE = 100          # 常量：全大写下划线
default_timeout = 30    # 变量：蛇形

def get_user_name():    # 函数：蛇形
    pass

class HttpClient:       # 类：大驼峰
    pass
```

---

## 3. 各类对象怎么写

| 对象 | 风格 | 例子 |
| ---- | ---- | ---- |
| 模块（`.py` 文件） | 全小写蛇形 | `my_module.py` |
| 包（文件夹） | 全小写，尽量不加下划线 | `utils/`、`mypackage/` |
| 类 | 大驼峰 | `MyClass`、`HttpClient` |
| 异常 | 大驼峰 + `Error` 后缀 | `ValueError`、`ConfigParseError` |
| 类型别名 / 泛型 | 大驼峰；泛型常用 `T`、`K`、`V` | `Vector`、`T`、`KT` |
| 函数 / 方法 | 蛇形，动词开头 | `get_user`、`parse_config` |
| 变量 / 属性 | 蛇形，名词 | `user_count`、`file_path` |
| 常量 | 全大写下划线 | `MAX_SIZE`、`DEFAULT_TIMEOUT` |
| 布尔值 | 蛇形，`is_` / `has_` / `can_` 开头 | `is_valid`、`has_next` |
| 私有成员 | 前面加一个下划线 | `_cache`、`_helper()` |
| 魔术方法 | 前后各两个下划线，别自己造 | `__init__`、`__len__` |
| 枚举成员 | 全大写下划线（社区惯例） | `Color.RED` |
| 不用的一次性变量 | 单个下划线 | `for _ in range(3):` |

补充几条：

- 模块名不要用 `-`，不然 `import` 不进来；也别和标准库重名，比如自己写个 `json.py` 会把自己的模块顶掉
- 泛型里 `T_co` 这种写法表示协变，`_co` / `_contra` 是 PEP 8 的约定后缀
- 缩写要么全大写要么全小写，别 `HTTPServer` 和 `HttpServer` 混着来，PEP 8 推荐 `HttpServer`

---

## 4. 下划线的三种含义

### `_name`：软私有，只是约定

一个下划线开头，表示“这是内部用的，别从外面碰”。解释器不会真的拦你，只是约定。

```python
class Counter:
    def __init__(self):
        self._count = 0      # 约定：内部用

    def _reset(self):        # 约定：内部方法
        self._count = 0
```

`from module import *` 也不会导入 `_` 开头的名字（除非写在 `__all__` 里）。

### `__name`：名称改写，真的有影响

两个下划线开头（结尾最多一个下划线），Python 会把名字改写成 `_类名__名字`，用来避免子类意外覆盖。

```python
class User:
    def __init__(self):
        self.__token = "secret"

u = User()
print(u.__dict__)
```

输出：

```text
{'_User__token': 'secret'}
```

所以这样会报错：

```python
print(u.__token)
```

```text
AttributeError: 'User' object has no attribute '__token'
```

因为它们其实是同一个属性：

```python
print(u._User__token)
```

```text
secret
```

注意：只是改名字，不是加密，别拿它当安全手段。

### `__name__`：前后都双下划线，魔术方法

`__init__`、`__str__`、`__len__`、`__all__`、`__main__` 这些由 Python 自己定义和调用，你只负责实现，**不要自己发明 `__my_thing__` 这种名字**。

```python
class Box:
    def __init__(self, items):
        self.items = items

    def __len__(self):        # 实现后 len(box) 就能用
        return len(self.items)

print(len(Box([1, 2, 3])))
```

输出：

```text
3
```

---

## 5. 函数参数有固定写法

这些名字是约定俗成的，换掉别人会看不懂：

| 名字 | 用在哪 | 例子 |
| ---- | ------ | ---- |
| `self` | 实例方法第一个参数 | `def save(self):` |
| `cls` | 类方法第一个参数 | `def create(cls):` |
| `*args` | 任意位置参数 | `def f(*args):` |
| `**kwargs` | 任意关键字参数 | `def f(**kwargs):` |

```python
class User:
    def __init__(self, name):
        self.name = name

    @classmethod
    def from_dict(cls, data):
        return cls(data["name"])

    def rename(self, new_name, *, force=False):
        self.name = new_name
```

---

## 6. 名字要表达意图

命名规范只是底线，真正难的是取个能看懂的名字。

| 不好 | 好 | 原因 |
| ---- | ---- | ---- |
| `flag` | `is_ready` | 布尔要能读出真假含义 |
| `data`、`tmp` | `user_list`、`raw_config` | 说清楚装的是什么 |
| `getUserInfo` | `get_user_info` | Python 不用驼峰 |
| `usr_cnt` | `user_count` | 少用没必要的缩写 |
| `list`、`len`、`id` | `items`、`length`、`user_id` | 别覆盖内置名字 |
| `l`、`O`、`I` | `line`、`count` | 和数字 1、0 太像 |
| `userList` | `users` | 集合用复数就够了 |

几条经验：

- 名字长度和作用域匹配：循环里 `i`、`x` 没问题，模块级常量就得写清楚
- 变量用名词，函数用“动词 + 名词”：`parse_config()`、`send_email()`
- 布尔用 `is_` / `has_` / `can_` / `should_` 开头
- 别中英夹杂着拼，也别用拼音当名字（`yonghu`），除非是业务里的专有名词
- 别在名字里写类型（`user_list_of_str`），类型交给类型注解

---

## 7. 常见坑

### 坑 1：覆盖内置名字

```python
list = [1, 2, 3]   # 现在 list 是列表，不再是内置类型
```

后面再用 `list()` 转换类型就会报错：

```text
TypeError: 'list' object is not callable
```

`str`、`int`、`id`、`sum`、`type`、`max`、`open` 都是高危名字。

### 坑 2：魔术方法写错一个下划线

```python
class A:
    def _init_(self):    # 错：这是普通方法，不会被自动调用
        self.x = 1

a = A()
print(a.__dict__)
```

输出：

```text
{}
```

必须是 `__init__`，前后各两个下划线。

### 坑 3：以为 `__x` 是“私有变量”

它只是被改名成 `_类名__x`，继承和调试时照样能访问，别拿它保护敏感数据。

### 坑 4：模块名和标准库撞车

项目里有个 `random.py`，同目录下 `import random` 导入的就是你的文件，标准库反而进不来。

---

## 8. 和 C 的习惯对比

小组里的人大多从 C 过来，这几个地方最容易顺手写错：

| C 里常见 | Python 应该写成 | 说明 |
| -------- | --------------- | ---- |
| `MAX_SIZE` | `MAX_SIZE` | 常量写法一致，都是全大写 |
| `struct Node` / `typedef Node` | `class Node:` | 类型名用大驼峰 |
| `getUserInfo()` | `get_user_info()` | 函数从驼峰改蛇形 |
| `int userCount;` | `user_count` | 变量从驼峰改蛇形 |
| `int g_count;` | `count` | Python 不用 `g_` 这种前缀标全局 |
| `#define PI 3.14` | `PI = 3.14` | 宏的位置换成模块级常量 |
| `my_lib.h` / `my_lib.c` | `my_lib.py` | 文件名风格一样，小写下划线 |
| 单字符 `l`、`O` 当变量 | `line`、`count` | C 里也常被警告，Python 更该避免 |

一句话：**类型用大驼峰，其他一律蛇形，常量全大写。**

---

## 总结

记住这几条就够了：

1. **类用大驼峰，函数/变量/模块用蛇形，常量全大写下划线**
2. 一个下划线 `_x` 是约定私有，两个下划线 `__x` 会被改名成 `_类名__x`
3. `__x__` 是 Python 留的魔术方法，自己不要造这种名字
4. `self`、`cls`、`*args`、`**kwargs` 是固定写法，别换
5. 名字要能看出用途，布尔用 `is_` / `has_` 开头，集合用复数
6. 不要覆盖 `list`、`len`、`id` 这类内置名字
7. 别用 `l`、`O`、`I` 这种和数字打架的单字符
8. 装个 flake8 + pep8-naming 或 ruff，让机器帮你盯着
