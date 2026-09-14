# Lab 6: CI 红绿灯 — 故障注入与修复闭环
> 🎯 **学习目标**：体验 CI 的“守门人”机制，学习如何通过 CI 日志排查问题，并完成“红灯（失败）-> 本地修复 -> 绿灯（成功）”的开发闭环。引入测试驱动开发 (TDD) 的基础思路。
> 📂 **工作区**：`calculator-bob/`
> ⏱ **预估耗时**：30 分钟

---

### 1. 同步最新代码并创建分支

**📍 角色：Bob | 目录：`calculator-bob/`**

Bob 需要基于最新的 `main` 分支开发新的 `power` 幂运算功能。

```powershell
git status
git switch main
git pull origin main
git switch -c feat/power-function
git status
```

### ✅ 检查点（Checkpoint）
> **预期输出**：提示 `Switched to a new branch 'feat/power-function'`。
> **预期状态**：当前处于 `feat/power-function` 分支，且代码与远程 `main` 同步。

---

### 2. 添加包含 Bug 的代码

**📍 角色：Bob | 目录：`calculator-bob/`**

Bob 在 `calculator.py` 中添加 `power()` 函数，但他粗心大意，把幂运算写成了加法。请使用你的编辑器修改 `calculator.py` 为以下完整内容：

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


def divide(a, b):
    """Return the quotient of two numbers.

    Raises:
        TypeError: If inputs are not numbers.
        ValueError: If divisor is zero.
    """
    if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
        raise TypeError("Both arguments must be numbers")
    if b == 0:
        raise ValueError("Division by zero is not allowed")
    return round(a / b, 10)


def power(a, b):
    """Return a raised to the power of b."""
    return a + b  # BUG: should be a ** b
```

> **💡 知识扩展**：在真实的开发中，我们通常会先写测试，再写实现代码（测试驱动开发，TDD）。这可以确保我们的代码确实满足了需求，并且没有意外的 Bug。

---

### 3. 添加正确的测试用例

**📍 角色：Bob | 目录：`calculator-bob/`**

虽然功能写错了，但 Bob 按照需求写出了正确的测试。打开 `test_calculator.py`，更新为以下完整内容：

```python
import pytest
from calculator import add, subtract, multiply, divide, power


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


def test_divide_positive():
    assert divide(6, 3) == 2.0


def test_divide_negative():
    assert divide(-10, 2) == -5.0


def test_divide_by_zero():
    with pytest.raises(ValueError, match="Division by zero is not allowed"):
        divide(1, 0)


def test_divide_type_error():
    with pytest.raises(TypeError, match="Both arguments must be numbers"):
        divide("a", 1)


def test_power_basic():
    assert power(2, 3) == 8


def test_power_zero_exponent():
    assert power(5, 0) == 1


def test_power_one():
    assert power(2, 1) == 2
```

---

### 4. 提交并推送含有 Bug 的代码

**📍 角色：Bob | 目录：`calculator-bob/`**

Bob 过于自信，没有在本地运行 pytest 进行测试验证，直接将代码提交并推送到远端（模拟粗心场景）。

```powershell
git status
git add calculator.py test_calculator.py
git commit -m "feat: add power() function with tests"
git push origin feat/power-function
git status
```

---

### 5. 在 GitHub 发起 PR 并观察 CI 失败

**📍 操作位置：GitHub 网页端**

1. 浏览器打开代码仓库。
2. 点击 **Pull requests** → **New pull request**。
3. 选择 `base: main` 和 `compare: feat/power-function`。
4. 点击 **Create pull request**，填写标题和描述后提交。
5. 在 PR 页面向下滚动，观察 CI 状态。

> **💡 知识扩展**：CI (Continuous Integration) 在这里扮演了“守门人”的角色。即使开发人员忘记在本地运行测试，只要代码推送到 PR，CI 就会自动执行测试。

---

### 6. 查看 CI 失败日志 (红灯 ❌)

**📍 操作位置：GitHub 网页端**

此时你会发现 PR 页面的 CI 检查变红 ❌。

1. 点击报错任务右侧的 **Details**（或者点击 PR 底部的 ❌ 图标）。
2. 在打开的日志页面，点击展开 **Run pytest** 步骤。
3. 你会看到如下预期的错误日志：
   `E       assert 5 == 8`
   `E        +  where 5 = power(2, 3)`
4. 返回 PR 主页面，你会看到提示 `"All checks have failed"` 并且 **Merge pull request** 按钮被禁用（变成灰色）。这正是 Branch Protection 发挥的作用。

### ✅ 检查点（Checkpoint）
> **预期输出**：CI 任务失败，明确指出 `power` 函数的测试未通过。
> **预期状态**：PR 被阻断，无法合并。

---

### 7. 本地修复 Bug

**📍 角色：Bob | 目录：`calculator-bob/`**

Bob 意识到自己的错误，回到本地进行修复。使用编辑器将 `calculator.py` 中的 `power` 函数修正为乘方运算符 `**`：

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


def divide(a, b):
    """Return the quotient of two numbers.

    Raises:
        TypeError: If inputs are not numbers.
        ValueError: If divisor is zero.
    """
    if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
        raise TypeError("Both arguments must be numbers")
    if b == 0:
        raise ValueError("Division by zero is not allowed")
    return round(a / b, 10)


def power(a, b):
    """Return a raised to the power of b."""
    return a ** b
```

修复后，在本地运行测试验证：

```powershell
pytest -v
```

### ✅ 检查点（Checkpoint）
> **预期输出**：终端显示全部测试通过（PASSED），绿色提示。
> **预期状态**：Bug 已经在本地方修复。

---

### 8. 追加提交并推送修复

**📍 角色：Bob | 目录：`calculator-bob/`**

Bob 将修复后的代码提交并推送到原有分支：

```powershell
git status
git add calculator.py
git commit -m "fix: correct power() implementation to use exponentiation"
git push origin feat/power-function
git status
```

---

### 9. 观察 CI 成功 (绿灯 ✅)

**📍 操作位置：GitHub 网页端**

1. 回到 GitHub 的 PR 页面。
2. 追加提交会自动触发 CI 重新运行。观察运行状态。
3. 等待几秒钟，CI 变成绿灯 ✅。
4. 页面显示 `"All checks have passed"`，此时 **Merge pull request** 按钮恢复可用（绿色）。
5. 点击 **Merge pull request** → **Confirm merge**，完成代码合并。

> **💡 知识扩展**：追加推送 (Push) 到关联了 PR 的分支，会自动触发 GitHub Actions 重新运行相关 Workflow。

---

### 10. 同步主分支

**📍 角色：Bob | 目录：`calculator-bob/`**

合并完成后，将最新的 `main` 同步到本地：

```powershell
git switch main
git pull origin main
```

---
[⬅ 上一节：Lab 5: CI 自动化](./lab05-ci-setup.md) | [目录](../LEARNING_PLAN.md) | [下一节：Lab 7: 模块化重构 ➡](./lab07-refactor.md)
