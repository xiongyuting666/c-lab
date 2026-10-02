# PR 流程说明书

目标：**任何改动都通过 Pull Request 进入 `master`，没有人直接往 `master` 上推。**

适用对象：c-lab 小组的 4 位成员。本文假设你已经在本地 clone 了仓库。

配套阅读：[README.md](./README.md) 里的提交信息前缀表和目录约定。

> **写在前面**：[README.md](./README.md) 里对直接推 `master` 还比较宽松（"想直接推就直接推吧，多尝试"），本文写的是**目标流程**。等大家都跑通一遍之后，建议把 README 的措辞收紧，并按[第七节](#七把约定变成机制推荐)打开分支保护，让规则从"靠自觉"变成"点不动"。

---

## 一、一句话版本

```bash
git switch master && git pull          # 1. 同步
git switch -c 你的名字/改什么           # 2. 开分支
# 3. 改代码
git add <文件> && git commit -m "fix: 描述"
git push -u origin 你的名字/改什么      # 4. 推分支（不是 master！）
# 5. 去 GitHub 上点 Compare & pull request
# 6. 等别人 review 后，由对方点 Merge
```

---

## 二、先分清三件事

新手最容易把这三件事混成一件：

| 动作 | 命令 / 操作 | 对 `master` 的影响 |
| --- | --- | --- |
| **推分支** | `git push origin 你的分支` | 无。只是在远程多了一条分支 |
| **开 PR** | GitHub 网页上点按钮 | 无。只是发起一个合并提议 |
| **合并** | 在 PR 页面上点 `Merge` 按钮 | 你的改动进入 `master` |

**关键认知：`git push` 推的是"分支"，不是"代码进 master"。** 只要推的是你自己的分支名，`master` 就一点没动。

### 哪些操作算"直接推 master"（禁止）

```bash
git switch master
git merge 你的分支
git push                      # ← 这一下就等于绕过 PR 直接改 master
```

### 哪些操作是合法的

```bash
git switch master
git merge origin/master       # 站在自己的分支上把 master 合进来，方向相反，安全
```

同一句 `git merge`，**站在哪条分支上跑，方向完全相反**。记住：`git merge A` = 把 A 合进"我当前所在的分支"，A 本身不动。

---

## 三、完整流程

### 1. 同步并开分支

```bash
git switch master
git pull
git switch -c yangyi/fix-testc
```

分支命名建议 `你的名字/改什么`，**尽量用英文和连字符**（如 `yangyi/py-naming-doc`）。中文分支名能用，但在命令行要加引号，在 URL 里会变成一长串 `%E5%...`，容易出错。

### 2. 改完提交

提交信息格式见 [README.md](./README.md) 的前缀表：`前缀: 描述`，例如 `docs: 添加关于 Python 命名规范的文档`。一次提交只做一件事。

### 3. 推分支

```bash
git push -u origin yangyi/fix-testc
```

`-u` 只需要第一次加，之后直接 `git push` 即可。

> 推送时如果要求输密码，用 GitHub 的 **Personal Access Token** 或浏览器登录，不是账号密码。

### 4. 在 GitHub 上开 PR

推完分支后，打开仓库首页，顶部通常会出现黄色的 **Compare & pull request** 按钮。没有的话走 **Pull requests → New pull request**。

页面上确认两件事：

- **方向**：`base: master ← compare: yangyi/fix-testc`，箭头从右往左。**方向反了 diff 会变成一大坨删除**，一眼就能看出来。
- **改动**：看一眼 `Files changed`，确认没夹带无关文件。

标题用提交信息的风格写清楚改了什么；描述里说清**这个改动是什么、为什么加**，而不是"我在测试流程"——reviewer 想看的是改动本身。

### 5. 等 review 并合并

- 可以在评论里 @ 组员来 review
- PR 还没合的时候想继续改？**在同一个分支继续 `commit` + `push` 就行，PR 会自动更新**，不用重开
- 由别人看过之后（或组里约定同意后）点 **Merge pull request**

**谁能点 Merge？** 见 [第六节](#六谁能点-merge)。

### 6. 收尾

合并后（远程分支一般会被一起删掉）：

```bash
git switch master
git pull
git branch -d yangyi/fix-testc     # 删掉本地分支
git fetch --prune                  # 清掉远程已删除分支的追踪记录
```

---

## 四、常见情况

### 情况 1：PR 还没合并，我想接着开发

看新开发跟这个 PR 是不是**同一件事**：

| 情况 | 做法 |
| --- | --- |
| **同一件事的后续**（补边界、改 bug） | 就在原分支继续 `commit` + `push`，PR 自动更新 |
| **完全不相干的新功能** | 从最新 `master` 开新分支，两个 PR 各审各合 |
| **新东西依赖还没合并的改动** | 从当前分支再开分支，开 PR 时 `base` 选**旧的功能分支**而不是 master |

第三种叫 stacked PR，等底层那个合并后 base 会自动切到 master，但对小仓库来说不如"先合前者再开发后者"简单。

### 情况 2：master 有新提交，我的分支落后了

```bash
git switch yangyi/fix-testc
git fetch origin
git merge origin/master
git push
```

`git merge origin/master` = 把 master 的提交合进**我当前的分支**，`master` 一点不动。合并完要 `push`，PR 上才会显示冲突已解决。如果 master 没有新提交，会提示 `Already up to date.`，什么都不发生。

> 这里的 `origin/master` 是**本地对远程 master 的快照**，所以要先 `git fetch origin` 刷新它，否则可能合进来一份过期的 master。

### 情况 3：出现冲突

PR 页面会提示 `This branch has conflicts that must be resolved`。在本地：

```bash
git switch yangyi/fix-testc
git fetch origin
git merge origin/master
```

打开冲突文件，会看到：

```
<<<<<<< HEAD
你自己的版本
=======
master 的版本
>>>>>>> origin/master
```

手工改成最终想要的样子的**同时删掉这三行标记**，然后：

```bash
git add <解决后的文件>
git status                    # 确认没有残留的 unmerged 路径
git commit                    # merge 冲突解决后，直接 commit 即可
git push
```

想放弃这次合并、回到冲突前的状态：

```bash
git merge --abort
```

**冲突的正确解法是手工合并两边的意图，不是随便选一边**。挑不好就问代码的主人。

### 情况 4：两人同时改同一个文件

两份 PR 都会冲突，而且要先合一个、另一个再解。所以**开工前先在群里认领文件**，别同时动同一批文件。

---

## 五、红线

### 1. 绝对不要 `git push -f`

强推会重写远程历史，把别人的提交"顶掉"，别人再 pull 就是一团乱。这条 README 里也写了。

### 2. 不要在本地合并后推 master

```bash
git switch master && git merge 你的分支 && git push    # ← 禁止
```

要走 PR，就不要在本地碰 `master`。

### 3. 不要在 PR 分支上用 `git rebase`

`rebase` 会改写提交历史，改完必须 `push -f` 才能推上去，和红线 1 冲突。**用 `merge` 同步 master**，虽然会多出一个 merge 节点，但安全合法。

### 4. 不要把无关改动塞进一个 PR

一个 PR 一件事，否则标题和前缀都不好写，reviewer 也没法看。

---

## 六、谁能点 Merge

| 角色 | 能不能点 Merge |
| --- | --- |
| Admin / Maintain / Write | ✅ 能，包括合别人的 PR，也包括合自己开的 PR |
| Triage | ❌ 不能 |
| Read 或没被邀请的人 | ❌ 按钮是灰的或看不到 |

加人方式：仓库 **Settings → Collaborators → Add people**，一般给 **Write**。

**只要大家都有 Write，"每个人都能点任何人的 Merge 按钮"**，包括你自己合自己的 PR。所以这件事光靠权限卡不住，得靠下面的机制或者自觉。

---

## 七、把约定变成机制（推荐）

分支保护让规则从"靠自觉"变成"点不动"。**需要仓库管理员 / owner 权限。**

### 方式 A：Rulesets（新版，推荐）

1. 仓库 → **Settings**
2. 左侧 **Rules → Rulesets → New ruleset → New branch ruleset**
3. `Ruleset Name` 填 `protect-master`，`Enforcement status` 选 **Active**
4. **Target branches → Add target → Include default branch**（或按 pattern 填 `master`）
5. 勾选 **Require a pull request before merging**
   - 展开后把 **Required approvals** 设为 `1`
   - 可选：勾 **Dismiss stale pull request approvals when new commits are pushed**（有人批准后又推了新提交，批准作废需重批）
6. 建议同时勾 **Block force pushes** —— 这条正好把 README 里"不要 `push -f`"变成硬规则
7. **Create**

### 方式 B：Classic Branch protection（旧版界面）

1. 仓库 → **Settings → Branches → Add branch protection rule**
2. `Branch name pattern` 填 `master`
3. 勾 **Require a pull request before merging** → **Require approvals** 设为 `1`
4. 想连管理员也拦就勾 **Do not allow bypassing the above settings**
5. **Save changes**

### 启用后会发生什么

- 谁都不能直接 `git push` 到 `master`，必须走 PR
- **必须至少有一个"别人"批准**才能合并。GitHub 不允许给自己批准，所以**作者本人就点不动 Merge 了**，这条能有效防"自己开自己合"
- 强推被拒

> 注意：打开 `Require approvals: 1` 之后，组里必须有人及时 review，否则改动会卡住。4 人小组要商量好谁来当"值班 review"。

---

## 八、命令速查

| 想干什么 | 命令 |
| --- | --- |
| 看当前状态 | `git status` |
| 看本地/远程分支 | `git branch -vv` / `git branch -r` |
| 同步 master | `git switch master` + `git pull` |
| 开新分支 | `git switch -c 名字/内容` |
| 切换分支 | `git switch <分支名>` |
| 提交 | `git add <文件>` + `git commit -m "前缀: 描述"` |
| 推分支 | `git push -u origin <分支名>` |
| 我的分支合进 master 的最新内容 | `git fetch origin` + `git merge origin/master` |
| 放弃一次合并 | `git merge --abort` |
| 看某个 PR 分支比 master 多了什么 | `git log --oneline origin/master..origin/<分支>` |
| 看改动统计 | `git diff --stat origin/master...origin/<分支>` |
| 删除已合并的本地分支 | `git branch -d <分支名>` |
| 清理远程已删分支的记录 | `git fetch --prune` |
