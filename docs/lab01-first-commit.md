# Lab 1: Alice 的第一次提交 — add() 函数与单测起步

> 🎯 **学习目标**：学习基本的分支开发流程、编写简单的 Python 代码及单元测试、在 GitHub 上发起和合并 Pull Request (PR)。
> 📂 **工作区**：`calculator-alice/`
> ⏱ **预估耗时**：30 分钟

---

## 1. 创建功能分支

在实际开发中，我们通常不在主分支（`main`）上直接编写代码。这是因为 `main` 分支应该始终保持稳定、可运行的状态。我们为新功能创建一个独立的分支，这样即使代码写到一半出现问题，也不会影响到其他人。

**📍 角色：Alice | 目录：`calculator-alice/`**

Alice 需要开发一个加法功能，首先她创建并切换到一个名为 `feat/add-function` 的新分支：

```powershell
git switch -c feat/add-function
```

### ✅ 检查点（Checkpoint）
> **预期输出**：`Switched to a new branch 'feat/add-function'`
> **预期状态**：Alice 现在在 `feat/add-function` 分支上工作，接下来的所有改动都会记录在这个分支上。

---

## 2. 编写 `calculator.py` 业务代码

**📍 角色：Alice | 目录：`calculator-alice/`**

请在当前目录下创建一个名为 `calculator.py` 的文件，并将以下完整的代码写入：

```python
def add(a, b):
    """Return the sum of two numbers."""
    return a + b
```

---

## 3. 编写 `test_calculator.py` 测试代码

为了确保 `add()` 函数工作正常，Alice 需要编写单元测试。在 pytest 框架中，所有以 `test_` 开头的函数都会被自动识别为测试用例。

**📍 角色：Alice | 目录：`calculator-alice/`**

请创建一个名为 `test_calculator.py` 的文件，并将以下完整的代码写入：

```python
from calculator import add


def test_add_positive_numbers():
    assert add(2, 3) == 5


def test_add_negative_numbers():
    assert add(-1, -1) == -2


def test_add_zero():
    assert add(0, 0) == 0


def test_add_mixed():
    assert add(-1, 1) == 0
```

---

## 4. 安装 pytest 并本地运行测试

**📍 角色：Alice | 目录：`calculator-alice/`**

在提交代码前，必须确保本地测试通过。首先安装 pytest，然后运行它：

```powershell
pip install pytest
pytest test_calculator.py -v
```

### ✅ 检查点（Checkpoint）
> **预期输出**：
> ```
> test_calculator.py::test_add_positive_numbers PASSED
> test_calculator.py::test_add_negative_numbers PASSED
> test_calculator.py::test_add_zero PASSED
> test_calculator.py::test_add_mixed PASSED
> ========================== 4 passed in 0.02s ==========================
> ```
> **预期状态**：所有的测试用例都已经通过，说明 `add()` 函数逻辑正确。

---

## 5. 暂存并提交代码

**📍 角色：Alice | 目录：`calculator-alice/`**

查看当前工作区的状态，然后将新文件暂存并提交。这里我们遵循 Conventional Commits 规范，使用 `feat:` 前缀表示新增功能。

```powershell
git status
git add calculator.py test_calculator.py
git commit -m "feat: add add() function with unit tests"
```

### ✅ 检查点（Checkpoint）
> **预期输出**：提交成功的信息，显示 `2 files changed`。
> **预期状态**：修改已经被记录到本地仓库的 `feat/add-function` 分支中。

---

## 6. 推送分支到 GitHub

**📍 角色：Alice | 目录：`calculator-alice/`**

现在 Alice 需要将她本地的这根分支推送到 GitHub 远端，以便其他人可以审查她的代码：

```powershell
git push origin feat/add-function
```

---

## 7. 发起 Pull Request (PR)

Pull Request（拉取请求，简称 PR）是一种通知团队成员你已经完成某个功能，并请求他们审查并合并代码到 `main` 分支的机制。

**📍 操作位置：GitHub 网页端**

1. 打开 GitHub 上你的 `python-calculator` 仓库页面。
2. 你可能会在页面上方看到一个黄色的提示框，显示 `feat/add-function had recent pushes`，点击旁边的 **Compare & pull request** 按钮。
   *(如果没有看到提示框，请点击 **Pull requests** 标签页 → **New pull request**，将 base 设置为 `main`，compare 设置为 `feat/add-function`。)*
3. **PR 标题** 请确保为：`feat: add add() function with unit tests`
4. 在 **Write** 描述框中，写明本次 PR 的内容，例如：
   > 实现了基础的 `add()` 加法函数，并为其添加了 4 个 pytest 测试用例（正数、负数、零、一正一负），所有测试在本地均已通过。
5. 点击下方的 **Files changed** 标签页，你可以直观地看到本次提交所做的所有代码改动（绿色代表新增内容）。
6. 确认无误后，点击绿色的 **Create pull request** 按钮。

---

## 8. 合并 PR

**📍 操作位置：GitHub 网页端**

由于这是一个简单的功能练习，我们可以直接合并（现实中这通常需要其他同事进行 Code Review）：

1. 在刚刚创建的 PR 页面中，点击绿色的 **Merge pull request** 按钮。
2. 点击 **Confirm merge**。
3. （可选）合并成功后，你可以点击 **Delete branch** 按钮删除远端的 `feat/add-function` 分支以保持仓库整洁。

### ✅ 检查点（Checkpoint）
> **预期状态**：此时如果你点击仓库的 `<> Code` 标签页，返回到 `main` 分支查看，你应该能看到 `calculator.py` 和 `test_calculator.py` 文件已经被合并进来了。

---

## 9. 本地同步代码

**📍 角色：Alice | 目录：`calculator-alice/`**

GitHub 上的 `main` 分支已经包含了新代码，但 Alice 本地的 `main` 分支还是旧的。她需要将远端的最新更改拉取下来，并清理掉已经无用的本地开发分支：

```powershell
git switch main
git pull origin main
git branch -d feat/add-function
```

### ✅ 检查点（Checkpoint）
> **预期状态**：Alice 的本地 `main` 分支已经更新，包含加法功能代码。开发分支已被成功删除。

---
[⬅ 上一节：Lab 0: 环境准备](./lab00-setup.md) | [目录](../LEARNING_PLAN.md) | [下一节：Lab 2: Bob 加入协作 ➡](./lab02-bob-joins.md)
