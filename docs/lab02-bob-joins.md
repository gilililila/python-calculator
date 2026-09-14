# Lab 2: Bob 加入协作 — 首次双人协同与 Code Review

> 🎯 **学习目标**：掌握拉取远端代码、发起 Pull Request、进行 Code Review 及根据意见追加提交的完整流程。
> 📂 **工作区**：`calculator-bob/` 目录和 GitHub 网页端
> ⏱ **预估耗时**：35 分钟

## 1. 同步最新代码

**📍 角色：Bob | 目录：`calculator-bob/`**

Bob 在开始工作之前，需要先将远端（GitHub）上的最新代码同步到自己的本地仓库中。目前 main 分支上已经有了 Alice 编写的加法功能。

```powershell
git pull origin main
```

### ✅ 检查点（Checkpoint）
> **预期输出**：终端会显示更新的文件列表。
> **预期状态**：Bob 的 `calculator-bob` 目录下现在应该能看到 `calculator.py` 和 `test_calculator.py` 文件了。

---

## 2. 创建功能分支

**📍 角色：Bob | 目录：`calculator-bob/`**

为了不直接在 `main` 分支上直接修改代码，我们需要创建一个新的功能分支 `feat/subtract-function`。

```powershell
git switch -c feat/subtract-function
```

---

## 3. 实现减法功能

**📍 角色：Bob | 目录：`calculator-bob/`**

使用你的编辑器打开 `calculator.py`，在其中追加减法函数 `subtract`。请将文件内容完全替换为以下代码：

```python
def add(a, b):
    """Return the sum of two numbers."""
    return a + b


def subtract(a, b):
    """Return the difference of two numbers."""
    return a - b
```

---

## 4. 编写减法测试

**📍 角色：Bob | 目录：`calculator-bob/`**

接下来，打开 `test_calculator.py` 文件，导入 `subtract` 函数，并添加针对减法的测试用例。请将文件内容完全替换为以下代码：

```python
from calculator import add, subtract


def test_add_positive_numbers():
    assert add(2, 3) == 5


def test_add_negative_numbers():
    assert add(-1, -1) == -2


def test_add_zero():
    assert add(0, 0) == 0


def test_add_mixed():
    assert add(-1, 1) == 0


def test_subtract_positive():
    assert subtract(5, 3) == 2


def test_subtract_negative():
    assert subtract(-1, -1) == 0


def test_subtract_zero():
    assert subtract(0, 0) == 0
```

---

## 5. 运行测试验证

**📍 角色：Bob | 目录：`calculator-bob/`**

在我们提交代码前，确保所有的单元测试都能正常运行并全部通过。

```powershell
pytest test_calculator.py -v
```

### ✅ 检查点（Checkpoint）
> **预期输出**：终端应显示 7 个测试全部标绿，显示类似 `7 passed in 0.03s`。
> **预期状态**：我们的加法和减法功能均已稳定工作。

---

## 6. 暂存、提交并推送分支

**📍 角色：Bob | 目录：`calculator-bob/`**

现在我们将本次的改动保存下来，并推送到 GitHub 上。先使用 `git status` 查看变更状态：

```powershell
git status
```

你会看到 `calculator.py` 和 `test_calculator.py` 被修改过。接着，我们暂存并提交（注意使用常规的 Commit Message 前缀）：

```powershell
git add calculator.py test_calculator.py
git commit -m "feat: add subtract() function with unit tests"
git push origin feat/subtract-function
```

> **知识点：分支推送**
> 这次我们推送的目标是 `feat/subtract-function` 分支，这样 GitHub 上就会创建一个同名分支，而不会直接修改 `main`。

---

## 7. 发起 Pull Request (PR)

**📍 操作位置：GitHub 网页端**

1. 登录 GitHub 并进入你的仓库页面。
2. 你应该能看到一个黄色的提示条（"feat/subtract-function had recent pushes"），点击右侧的 **Compare & pull request** 按钮。
3. 如果没看到提示条，也可以点击 **Pull requests** 标签页，然后点击 **New pull request**。
4. 确保 "base" 分支是 `main`，"compare" 分支是 `feat/subtract-function`。
5. **PR 标题** 请填写：`feat: add subtract() function with unit tests`
6. 在描述中可以简要写明：“增加了减法运算及其对应测试”。
7. 点击 **Create pull request**。

> **知识点：PR 的生命周期**
> 一个 Pull Request 代表一个合入代码的请求，它不仅包含了代码 diff，还是团队成员讨论、审查（Review）和修改迭代的地方。

---

## 8. 进行 Code Review

**📍 操作位置：GitHub 网页端 | 角色：Alice（作为审查者）**

现在轮到 Alice 对这段代码进行审查（Code Review）了。通过 Review，团队可以及早发现潜在问题并统一代码风格。

1. 在 GitHub 的 PR 页面，点击 **Files changed** 标签页，查看具体修改。
2. 找到 `test_calculator.py` 的结尾处，将鼠标悬停在最后一行代码的行号左侧，会出现一个蓝色的 **"+"** 按钮。
3. 点击 **"+"** 按钮，在弹出的文本框中输入行级批注，例如：
   > *"建议添加一个边界测试用例 `subtract(0, 5)` 来确认负数结果是否正确。"*
4. 点击右下角的 **Start a review**（如果是单独一句话也可以点击 Add single comment，但建议走正式 Review 流程）。
5. 批注写完后，点击页面右上角的绿色的 **Review changes** 按钮。
6. 在弹窗中选择 **Request changes**（请求修改），然后点击 **Submit review**。

> **知识点：Code Review 的三种状态**
> - **Comment（评论）**：单纯给出意见或提问，不强制要求修改。
> - **Approve（批准）**：认为代码完美，可以合并。
> - **Request changes（请求修改）**：发现问题，必须修复后才能进行合并。

---

## 9. 响应 Review 意见，追加提交

**📍 角色：Bob | 目录：`calculator-bob/`**

Bob 收到了 Alice 的修改要求，他需要在本地补全相应的测试用例。

再次打开 `test_calculator.py`，添加 `test_subtract_resulting_negative` 函数。完整的文件内容更新如下：

```python
from calculator import add, subtract


def test_add_positive_numbers():
    assert add(2, 3) == 5


def test_add_negative_numbers():
    assert add(-1, -1) == -2


def test_add_zero():
    assert add(0, 0) == 0


def test_add_mixed():
    assert add(-1, 1) == 0


def test_subtract_positive():
    assert subtract(5, 3) == 2


def test_subtract_negative():
    assert subtract(-1, -1) == 0


def test_subtract_zero():
    assert subtract(0, 0) == 0


def test_subtract_resulting_negative():
    assert subtract(0, 5) == -5
```

修改后，直接提交并推送到同一分支：

```powershell
git add test_calculator.py
git commit -m "test: add edge case for subtract per review feedback"
git push origin feat/subtract-function
```

### ✅ 检查点（Checkpoint）
> **预期状态**：回到 GitHub 网页端的 PR 页面，你会发现无需手动操作，刚才的这一条提交（`test: add edge case...`）已经**自动更新**到了当前的 PR 中。这也是 PR 机制非常重要的一环——在 PR 合并之前，对对应分支的所有 Push 都会被追加进来。

---

## 10. 批准并合并 PR

**📍 操作位置：GitHub 网页端 | 角色：Alice**

1. Alice 再次打开该 PR 页面，查看新的提交是否解决了刚才提出的问题。
2. 点击 **Files changed**，确认测试已被添加。
3. 点击 **Review changes**。
4. 这次选择 **Approve**，然后点击 **Submit review**。
5. 返回到 Conversation 页面，点击绿色的 **Merge pull request** 按钮，再点击 **Confirm merge**。

现在，Bob 的功能终于成功合入到了主分支！

---

## 11. 清理工作与本地同步

**📍 角色：Bob | 目录：`calculator-bob/`**

功能完成后，本地和远端的特性分支就可以删除了。Bob 需要切回主干并同步最新代码。

```powershell
git switch main
git pull origin main
git branch -d feat/subtract-function
```

> **知识点：分支清理**
> `git branch -d` 用于删除本地分支。定期清理已经合入的分支可以保持本地环境的清爽。

---
[⬅ 上一节：Lab 1: 第一次提交与 PR](./lab01-first-commit.md) | [目录](../LEARNING_PLAN.md) | [下一节：Lab 3: 并行开发 ➡](./lab03-parallel-dev.md)
