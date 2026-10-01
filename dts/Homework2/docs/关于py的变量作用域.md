Python 的作用域，简单说就是：**一个变量在哪些地方能被访问、被修改，以及查找一个名字时按什么顺序找。**

核心规则是 **LEGB**。

---

## 1. LEGB 查找顺序

当 Python 遇到一个变量名时，会按这个顺序找：

| 层级 | 含义                | 例子                    |
| ---- | ------------------- | ----------------------- |
| L    | Local，当前函数内部 | 函数里的局部变量        |
| E    | Enclosing，外层函数 | 闭包中外层函数的变量    |
| G    | Global，模块全局    | 当前 `.py` 文件顶层变量 |
| B    | Built-in，内置      | `print`、`len`、`range` |

查找顺序：

```text
Local -> Enclosing -> Global -> Built-in
```

找不到就报 `NameError`。

例子：

```python
x = "全局"

def outer():
    x = "外层"

    def inner():
        x = "局部"
        print(x)

    inner()

outer()
```

输出：

```text
局部
```

如果 `inner` 里没有 `x`，就会找 `outer` 的 `x`；再没有，找全局；再没有，找内置。

---

## 2. 函数内赋值默认是局部变量

只要你在函数里给一个变量赋值，Python 就认为它是局部变量，不管外面有没有同名的。

```python
x = 10

def f():
    print(x)
    x = 20

f()
```

这会报错：

```text
UnboundLocalError: local variable 'x' referenced before assignment
```

因为函数里有 `x = 20`，所以整个函数内的 `x` 都被当成局部变量，但打印时还没赋值。

如果只是想读全局变量，可以：

```python
x = 10

def f():
    print(x)

f()
```

输出：

```text
10
```

---

## 3. `global`：在函数内修改全局变量

```python
count = 0

def add():
    global count
    count += 1

add()
print(count)
```

输出：

```text
1
```

注意：

- 读全局变量不一定要 `global`
- 修改全局变量的绑定，需要 `global`
- 如果只是修改可变对象内容，比如 `list.append()`，可以不用 `global`

```python
nums = []

def add_num():
    nums.append(1)  # 没有重新绑定 nums，可以

add_num()
print(nums)
```

输出：

```text
[1]
```

但这样不行：

```python
nums = []

def reset():
    nums = [1, 2]  # 这是创建局部变量

reset()
print(nums)  # []
```

---

## 4. `nonlocal`：修改外层函数变量

用于嵌套函数，修改外层函数的变量，不是全局。

```python
def outer():
    x = 0

    def inner():
        nonlocal x
        x += 1
        return x

    return inner

f = outer()
print(f())
print(f())
```

输出：

```text
1
2
```

`nonlocal` 不能用于全局变量，只能用于外层函数作用域。

---

## 5. 闭包

内层函数引用了外层函数的变量，并且外层函数返回内层函数，就形成闭包。

```python
def make_counter():
    count = 0

    def counter():
        nonlocal count
        count += 1
        return count

    return counter

c = make_counter()
print(c())
print(c())
```

输出：

```text
1
2
```

`count` 虽然外层函数已经执行完了，但被内层函数引用，所以还保留着。

---

## 6. 哪些结构会创建作用域？

会创建新作用域的：

- 模块，也就是一个 `.py` 文件
- 函数
- 类
- 列表推导式、生成器表达式，Python 3 中也有自己的作用域

不会创建新作用域的：

- `if`
- `for`
- `while`
- `try`
- `with`

所以：

```python
for i in range(3):
    pass

print(i)
```

输出：

```text
2
```

因为 `for` 不创建作用域，`i` 会留在当前作用域里。

---

## 7. 列表推导式的作用域

Python 3 里，列表推导式有自己的作用域，循环变量不会泄漏到外面。

```python
x = 10
squares = [x * x for x in range(1, 6)]
print(squares)
print(x)
```

输出：

```text
[1, 4, 9, 16, 25]
10
```

列表推导式里的 `x` 不会覆盖外面的 `x`。

生成器表达式也一样：

```python
g = (x * x for x in range(3))
```

它也有自己的作用域。

---

## 8. 类作用域比较特殊

类体本身是一个作用域，但方法内部不会把类作用域当作外层作用域。

```python
class C:
    x = 10

    def f(self):
        print(x)  # 报错，NameError
```

方法里要访问类变量，得用：

```python
class C:
    x = 10

    def f(self):
        print(self.x)
        print(C.x)
```

类体里的列表推导式也不能直接访问类变量：

```python
class C:
    x = 10
    y = [x for _ in range(3)]  # NameError
```

因为列表推导式有自己的作用域，而类作用域不参与 LEGB 的 E 层。

---

## 9. 内置作用域

`print`、`len`、`range`、`list` 这些都在内置作用域。

```python
print(len("hello"))
```

如果自己定义了一个 `len`，会遮蔽内置的：

```python
len = 10

# 现在 len("hello") 会报错，因为 len 变成了整数
```

所以不要随便用内置函数名当变量名。

---

## 10. 查看作用域

```python
x = 10

def f():
    y = 20
    print(locals())  # 局部变量
    print(globals()) # 全局变量

f()
```

- `locals()`：当前局部命名空间
- `globals()`：全局命名空间
- `vars()`：类似
- `dir()`：查看对象属性

---

## 11. 常见坑

### 坑 1：函数内赋值导致全局变量不可读

```python
x = 10

def f():
    print(x)
    x = 20  # 报 UnboundLocalError
```

### 坑 2：可变默认参数

```python
def add(item, lst=[]):
    lst.append(item)
    return lst

print(add(1))
print(add(2))
```

输出：

```text
[1]
[1, 2]
```

因为默认参数在函数定义时只创建一次。

### 坑 3：循环里创建函数

```python
funcs = []
for i in range(3):
    funcs.append(lambda: i)

print([f() for f in funcs])
```

输出：

```text
[2, 2, 2]
```

因为 `lambda` 里的 `i` 是外层作用域的变量，循环结束后 `i` 是 2。

想固定值可以这样：

```python
funcs = []
for i in range(3):
    funcs.append(lambda i=i: i)

print([f() for f in funcs])
```

输出：

```text
[0, 1, 2]
```

---

## 总结

记住这几条：

1. 查找变量顺序：**局部 -> 外层 -> 全局 -> 内置**
2. 函数内赋值默认创建局部变量
3. 改全局用 `global`
4. 改外层函数变量用 `nonlocal`
5. `if`、`for`、`while` 不创建作用域
6. 函数、类、列表推导式会创建作用域
7. 类作用域不参与方法的 LEGB 外层查找
8. Python 3 列表推导式变量不会泄漏