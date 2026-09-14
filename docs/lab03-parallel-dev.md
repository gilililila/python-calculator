# Lab 3: 并行开发 — Alice 与 Bob 同时推进功能

> 🎯 **学习目标**：掌握并行开发的核心思想，体验在独立的特性分支上同时开发互不干扰的流程，并学习应对异常测试和不同功能的合并。
> 📂 **工作区**：`calculator-alice/` 目录和 `calculator-bob/` 目录交替操作
> ⏱ **预估耗时**：35 分钟

## 1. 各自拉取最新主干代码

在开始新的开发周期时，所有开发者都应确保他们的起点是最新的主分支代码。

**📍 角色：Alice | 目录：`calculator-alice/`**
```powershell
git switch main
git pull origin main
```

**📍 角色：Bob | 目录：`calculator-bob/`**
```powershell
git switch main
git pull origin main
```

---

## 2. Alice 开发乘法功能

**📍 角色：Alice | 目录：`calculator-alice/`**

Alice 准备接手乘法功能。她先创建自己的功能分支：

```powershell
git switch -c feat/multiply-function
```

接着，打开 `calculator.py`，加入 `multiply` 函数。请将文件内容完全替换为以下代码：

```python
def add(a, b):
    """Return the sum of two numbers."""
    return a + b


def subtract(a, b):
    """Return the difference of two numbers."""
    return a - b


def multiply(a, b):
    """Return the product of two numbers."""
    return a * b
```

然后，打开 `test_calculator.py`，导入 `multiply`，并加入相关测试用例。完整代码如下：

```python
from calculator import add, subtract, multiply


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


def test_multiply_positive():
    assert multiply(2, 3) == 6


def test_multiply_negative():
    assert multiply(-1, 5) == -5


def test_multiply_zero():
    assert multiply(0, 100) == 0
```

运行测试确认（共有 11 个测试应该全部通过）：
```powershell
pytest test_calculator.py -v
```

测试通过后，Alice 提交并推送：
```powershell
git add calculator.py test_calculator.py
git commit -m "feat: add multiply() function with unit tests"
git push origin feat/multiply-function
```

---

## 3. Bob 开发除法功能

与此同时，Bob 在开发除法功能。注意：此时 Bob 也是从原有的 `main` 出发的，他**不知道** Alice 正在写乘法，他的本地代码中也没有乘法功能。

**📍 角色：Bob | 目录：`calculator-bob/`**

```powershell
git switch -c feat/divide-function
```

Bob 打开 `calculator.py` 添加除法。由于除数不能为 0，他加入了防御式编程设计，抛出 `ValueError`。完整内容如下：

```python
def add(a, b):
    """Return the sum of two numbers."""
    return a + b


def subtract(a, b):
    """Return the difference of two numbers."""
    return a - b


def divide(a, b):
    """Return the quotient of two numbers.

    Raises:
        ValueError: If b is zero.
    """
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b
```

> **知识点：ValueError 的设计思路**
> 在 Python 中遇到非法参数（如除以 0）时，主动抛出异常（Exception）通常比默默返回错误码更好。这可以让调用方明确感知错误并予以捕获，提升程序的健壮性。

Bob 接着打开 `test_calculator.py` 添加测试。他利用 `pytest.raises` 来验证异常是否被正确抛出。完整代码如下（注意导入了 `pytest` 以及 `divide` 函数，但没有 `multiply`）：

```python
import pytest
from calculator import add, subtract, divide


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


def test_divide_positive():
    assert divide(6, 3) == 2.0


def test_divide_negative():
    assert divide(-10, 2) == -5.0


def test_divide_by_zero():
    with pytest.raises(ValueError, match="Cannot divide by zero"):
        divide(1, 0)
```

> **知识点：pytest.raises 异常测试**
> `with pytest.raises(...)` 会捕获代码块抛出的异常。如果对应的异常没有被抛出，或者异常信息与 `match` 正则不符，测试将会失败。

运行测试确认（共有 11 个测试全部通过）：
```powershell
pytest test_calculator.py -v
```

测试通过后，Bob 提交并推送：
```powershell
git add calculator.py test_calculator.py
git commit -m "feat: add divide() function with zero-division guard and tests"
git push origin feat/divide-function
```

---

## 4. 并行开发核心理念解析

### ✅ 检查点（Checkpoint）
> **预期状态**：到目前为止，Alice 的远端分支上有加、减、乘；Bob 的远端分支上有加、减、除。双方都不知道对方的最新进展。
> **分支隔离的价值**：这是并行开发中最重要的一环。在独立分支开发不仅互不干扰代码修改，更意味着在各自环境运行测试时，不会被尚未写完或包含 Bug 的他人代码破坏本地运行环境。这就是 Git 赋能团队效率的强大之处。

---

## 5. Alice 提交 PR 并合并

**📍 操作位置：GitHub 网页端 | 角色：Alice**

1. 登录 GitHub，为 `feat/multiply-function` 发起 Pull Request。
2. 因为此时 `main` 分支还是 Lab 2 结束时的样子，不会有任何冲突。
3. （这里我们假定 Review 已完成）点击 **Merge pull request** 并确认合并。

此时，远端 `main` 分支包含了 `add`, `subtract` 和 `multiply`，共计 3 个功能。

---

## 6. Bob 发起 PR 并解决潜在冲突

**📍 操作位置：GitHub 网页端 | 角色：Bob**

1. 登录 GitHub，为 `feat/divide-function` 发起 Pull Request。
2. 此时，由于 Alice 已经合入了修改，远端的 `main` 分支已经包含了乘法逻辑和最新的 import 声明。
3. GitHub 将会尝试自动合并（Automated merge）。
   - 有可能 GitHub 的智能算法能够自动合入不同行的修改（没有报冲突，可以直接合并）。
   - 如果发生 **冲突 (Conflict)**，GitHub 会提示 "This branch has conflicts that must be resolved"。你可以直接在网页端点击 **Resolve conflicts**，保留双方的更改（即保留乘法与除法及其各自对应的 import），完成解决后点击 **Mark as resolved** 和 **Commit merge**。
4. 确认代码无误后，点击 **Merge pull request** 将除法也合入主干。

最终，GitHub 上的 `main` 仓库代码已经将四则运算及其测试完整聚合！

---

## 7. 各自同步最新成果

功能合并完成后，本地就可以切回 main，拉取包含了所有人劳动的最终代码。

**📍 角色：Alice | 目录：`calculator-alice/`**
```powershell
git switch main
git pull origin main
```

**📍 角色：Bob | 目录：`calculator-bob/`**
```powershell
git switch main
git pull origin main
```

两人可以通过检查文件确认 `calculator.py` 中已经同时拥有了 `add`、`subtract`、`multiply` 和 `divide` 了。

---
[⬅ 上一节：Lab 2: Bob 加入协作](./lab02-bob-joins.md) | [目录](../LEARNING_PLAN.md) | [下一节：Lab 4: 合并冲突 ➡](./lab04-merge-conflict.md)
