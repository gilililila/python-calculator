# Lab 4: 合并冲突 — 正面迎击 Merge Conflict
> 🎯 **学习目标**：理解代码冲突的产生原因，学会读懂冲突标记，掌握手动解决冲突并完成合并的完整流程。
> 📂 **工作区**：`calculator-alice/` 和 `calculator-bob/`
> ⏱ **预估耗时**：40 分钟

**前置状态**：`main` 分支上有 `calculator.py`（含 add, subtract, multiply, divide 四个函数）和 `test_calculator.py`。两人的本地 `main` 都已同步到最新。

**冲突场景设计**：Alice 和 Bob 同时想改进 `divide()` 函数。Alice 要添加类型检查（确保参数是数字），Bob 要改进错误消息并添加浮点精度处理。两人修改了同一个函数的同一区域，必然产生冲突。

---

## 1. Alice 添加类型检查

**📍 角色：Alice | 目录：`calculator-alice/`**

首先，Alice 创建一个新分支来开发她的特性。

```powershell
git switch -c feat/divide-type-check
```

Alice 修改 `calculator.py` 中的 `divide` 函数，添加类型检查。请将 `calculator.py` 更新为以下完整内容：

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
        ValueError: If b is zero.
    """
    if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
        raise TypeError("Both arguments must be numbers")
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b
```

接着，Alice 需要在 `test_calculator.py` 中添加对应的测试（此处省略测试文件的具体改动，假设 Alice 已经完成了相应的更新并运行通过）。

Alice 提交代码并推送到远程仓库：

```powershell
git status
git add calculator.py
git commit -m "feat: add type checking to divide()"
git push origin feat/divide-type-check
```

**📍 操作位置：GitHub 网页端**

1. 切换到 GitHub 网页端，点击 **Compare & pull request**。
2. 填写 PR 标题和描述，点击 **Create pull request**。
3. 检查没有问题后，点击 **Merge pull request** → **Confirm merge**。

### ✅ 检查点（Checkpoint）
> **预期输出**：GitHub 上的 `main` 分支现在包含了 Alice 的类型检查代码。
> **预期状态**：Alice 的改动已经成功合入。

---

## 2. Bob 改进错误消息并添加精度处理

**📍 角色：Bob | 目录：`calculator-bob/`**

与此同时，Bob 在他本地的 `main` 分支上开始工作。**注意**：Bob 此时还没有拉取 Alice 的代码。

Bob 创建他的分支：

```powershell
git switch -c feat/divide-improvement
```

Bob 修改了 `calculator.py` 中的 `divide` 函数，改进了错误消息，并使用了 `round()` 函数。Bob 眼中的 `calculator.py` 完整内容如下：

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
        ValueError: If divisor is zero.
    """
    if b == 0:
        raise ValueError("Division by zero is not allowed")
    return round(a / b, 10)
```

Bob 提交他的改动并推送到远程仓库：

```powershell
git status
git add calculator.py
git commit -m "feat: improve divide() error message and precision"
git push origin feat/divide-improvement
```

---

## 3. 遭遇合并冲突

**📍 操作位置：GitHub 网页端**

Bob 来到 GitHub 网页端，像往常一样发起 PR：
1. 点击 **Compare & pull request**，发起基于 `feat/divide-improvement` 的 PR。
2. 页面上会显示一个警告信息：**"This branch has conflicts that must be resolved."**

### 💡 知识讲解：什么是合并冲突（Merge Conflict）？
当两个不同的分支修改了**同一个文件的同一部分代码**时，Git 无法自动决定应该保留哪一部分改动。这时候，Git 就会暂停合并操作，并要求开发者手动介入来解决冲突。在这个场景中，Alice 和 Bob 都修改了 `divide` 函数，Git 不知道是应该保留类型检查，还是保留新的错误信息，或者两者都要。

---

## 4. 本地解决冲突

**📍 角色：Bob | 目录：`calculator-bob/`**

Bob 需要在本地解决这个冲突。首先，他需要将远程 `main` 分支（包含了 Alice 的改动）拉取下来，并尝试合并到他当前的分支中。

```powershell
git fetch origin
git merge origin/main
```

此时，Git 会提示出现冲突（`CONFLICT (content): Merge conflict in calculator.py`）。

### 💡 知识讲解：`git fetch` vs `git pull`
- `git fetch`：只把远程的更新下载到本地的隐藏分支（如 `origin/main`），但**不会**修改你的工作区文件。
- `git pull`：相当于 `git fetch` 加上 `git merge`。它不仅下载更新，还会立即尝试合并到当前分支。推荐在处理冲突前使用 `fetch` + `merge`，这样过程更可控。

现在，Bob 打开 `calculator.py`，会看到类似这样的冲突标记：

```python
<<<<<<< HEAD
    if b == 0:
        raise ValueError("Division by zero is not allowed")
    return round(a / b, 10)
=======
    if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
        raise TypeError("Both arguments must be numbers")
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b
>>>>>>> origin/main
```

### 💡 知识讲解：读懂冲突标记
- `<<<<<<< HEAD`：这下面是你（当前分支，即 Bob）的改动。
- `=======`：分隔符，上方是你当前分支的内容，下方是你要合并进来的内容。
- `>>>>>>> origin/main`：这上面是目标分支（这里是 `origin/main`，即 Alice 的改动）。

**解决策略**：Bob 决定将两者的优点结合起来：保留 Alice 的类型检查，采用 Bob 的错误提示信息，并保留 Bob 的 `round()` 处理。

Bob 删除了冲突标记，并将 `calculator.py` 修改为以下完整内容：

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
```

---

## 5. 提交解决冲突后的代码

**📍 角色：Bob | 目录：`calculator-bob/`**

Bob 确认代码无误后，标记冲突已解决并推送到远程仓库：

```powershell
git status
git add calculator.py
git commit -m "fix: resolve merge conflict in divide()"
git push origin feat/divide-improvement
```

---

## 6. 完成合并

**📍 操作位置：GitHub 网页端**

Bob 回到 GitHub 的 PR 页面。刷新后，系统提示冲突已解决，绿色按钮再次亮起：
1. 点击 **Merge pull request** → **Confirm merge**。

---

## 7. 双方同步 main 分支

现在 `main` 分支包含了双方的最新改动。Alice 和 Bob 都需要更新本地代码。

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

### ✅ 检查点（Checkpoint）
> **预期输出**：Alice 和 Bob 本地的 `main` 分支完全一致，包含了所有的改动。
> **预期状态**：冲突顺利解决，项目继续推进。

---
[⬅ 上一节：Lab 3: 并行开发](./lab03-parallel-dev.md) | [目录](../LEARNING_PLAN.md) | [下一节：Lab 5: CI 自动化 ➡](./lab05-ci-setup.md)
