# c-lab

这是一个 4 人小组的 C 语言学习交流仓库，用来存放大家的练习代码、分享学习心得，同时熟悉 Git 协作流程。

## 目录说明

- `test.c`：第一个测试程序，输出 `Hello git`

## 编译运行

```bash
gcc test.c -o test
./test
```

## 协作约定

原则上有挺多麻烦的规则的，比如master要保证可用别塞脏东西，脏东西自己开分支捣鼓，不过可以慢慢学
想直接推到master就直接推吧，多尝试
提交方式希望是 前缀+自然语言
以下是常用的前缀

| 前缀 | 用途 | 例子 |
| --- | --- | --- |
| `feat` | 新功能、新程序 | `feat: 新增冒泡排序练习` |
| `fix` | 修 bug | `fix: 修复数组越界导致的崩溃` |
| `docs` | 只改文档（README、注释说明等） | `docs: 补充编译运行说明` |
| `style` | 格式调整，不影响逻辑（缩进、空格、换行） | `style: 统一 test.c 的缩进` |
| `refactor` | 重构，逻辑不变但代码结构变了 | `refactor: 把输入处理拆成单独函数` |
| `test` | 增加或修改测试 | `test: 增加链表插入的测试用例` |
| `chore` | 杂项（改 .gitignore、构建脚本等） | `chore: 忽略编译生成的 exe 文件` |
| `revert` | 撤销之前的某次提交 | `revert: 撤销“新增冒泡排序练习”` |

格式是 `前缀: 描述`，冒号后面加一个空格，描述用一句话说清楚改了什么。一次提交最好只做一件事，不然前缀不好选。

```bash
git add bubble_sort.c
git commit -m "feat: 新增冒泡排序练习"
```

这套写法来自 [Conventional Commits](https://www.conventionalcommits.org/zh-hans/) 规范，想深入了解可以看看。

