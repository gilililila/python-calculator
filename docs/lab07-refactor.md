# Lab 7: 模块化重构 — 从单文件到 Python 包结构
> 🎯 **学习目标**：掌握如何将简单的 Python 脚本重构为标准的 Python 包结构；了解 `__init__.py` 和 `pyproject.toml` 的作用；验证重构过程中测试和 CI 的保护作用。
> 📂 **工作区**：`calculator-alice/`
> ⏱ **预估耗时**：35 分钟

---

### 1. 同步代码并创建分支

**📍 角色：Alice | 目录：`calculator-alice/`**

Alice 发现所有的代码都堆积在 `calculator.py` 单个文件里，决定对其进行重构。首先，获取最新代码并创建新分支：

```powershell
git status
git switch main
git pull origin main
git switch -c refactor/package-structure
git status
```

---

### 2. 创建目录结构

**📍 角色：Alice | 目录：`calculator-alice/`**

使用 PowerShell 创建标准的包结构：

```powershell
New-Item -ItemType Directory -Path src/calculator -Force
New-Item -ItemType Directory -Path tests -Force
```

> **💡 知识扩展**：`src` 布局（src-layout）是目前推荐的 Python 项目结构，它可以有效避免本地导入时的路径混乱问题，并强制要求像用户一样安装包后才能使用。

---

### 3. 迁移功能代码

**📍 角色：Alice | 目录：`calculator-alice/`**

在 `src/calculator/` 目录下创建 `operations.py` 文件，并将原来 `calculator.py` 中的所有函数实现复制过去。使用编辑器创建并编辑 `src/calculator/operations.py` 为以下完整内容：

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

---

### 4. 统一导出接口

**📍 角色：Alice | 目录：`calculator-alice/`**

为了让外部使用者依然可以方便地从包的顶层导入函数（如 `from calculator import add`），需要创建一个 `__init__.py`。使用编辑器创建 `src/calculator/__init__.py` 为以下完整内容：

```python
from .operations import add, subtract, multiply, divide, power

__all__ = ["add", "subtract", "multiply", "divide", "power"]
```

> **💡 知识扩展**：`__init__.py` 文件将普通目录标识为 Python 包。它不仅在导入包时被执行，还能帮助我们组织内部模块的导出逻辑。

---

### 5. 迁移并修改测试文件

**📍 角色：Alice | 目录：`calculator-alice/`**

在 `tests/` 目录下创建 `test_operations.py`，复制原来的测试用例代码，并确保导入路径保持正常。使用编辑器创建并编辑 `tests/test_operations.py` 为以下完整内容：

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

### 6. 添加配置文件以使其可安装

**📍 角色：Alice | 目录：`calculator-alice/`**

为了让 Python 能够识别 `src/` 下的包，并在测试和 CI 中正确导入，我们需要将项目变成一个可安装的包。在项目根目录下使用编辑器创建 `pyproject.toml` 文件：

```toml
[build-system]
requires = ["setuptools>=68.0"]
build-backend = "setuptools.build_meta"

[project]
name = "python-calculator"
version = "0.1.0"
description = "A simple calculator package"
requires-python = ">=3.10"

[tool.setuptools.packages.find]
where = ["src"]
```

> **💡 知识扩展**：`pyproject.toml` 是 PEP 518 引入的标准化项目配置文件，定义了构建系统和项目元数据。有了它，我们就可以使用 pip 安装自己的项目。

---

### 7. 更新 CI 配置文件

**📍 角色：Alice | 目录：`calculator-alice/`**

CI 也需要适应新的目录结构并安装我们的包。使用编辑器更新 `.github/workflows/ci.yml` 为以下完整内容：

```yaml
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Set up Python 3.13
        uses: actions/setup-python@v5
        with:
          python-version: "3.13"

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install pytest flake8
          pip install -e .

      - name: Run flake8 linting
        run: flake8 src/ tests/ --count --show-source --statistics

      - name: Run pytest
        run: pytest tests/ -v
```

> **💡 知识扩展**：`pip install -e .` 代表以“可编辑模式”安装当前目录的项目。这使得我们的测试可以直接导入 `calculator` 包，就像导入第三方库一样。

---

### 8. 删除旧文件

**📍 角色：Alice | 目录：`calculator-alice/`**

现在结构已经迁移完毕，使用 Git 删除旧的单文件：

```powershell
git rm calculator.py
git rm test_calculator.py
git status
```

---

### 9. 本地安装与测试

**📍 角色：Alice | 目录：`calculator-alice/`**

在提交前，确认所有测试依然能够通过：

```powershell
pip install -e .
pytest tests/ -v
```

### ✅ 检查点（Checkpoint）
> **预期输出**：18 个测试全部通过。
> **预期状态**：重构完成且逻辑依然正确。这就是重构时保持测试覆盖率的重要性。

---

### 10. 提交并推送

**📍 角色：Alice | 目录：`calculator-alice/`**

```powershell
git status
git add .
git commit -m "refactor: restructure project into Python package layout"
git push origin refactor/package-structure
git status
```

---

### 11. 在 GitHub 发起 PR 并合并

**📍 操作位置：GitHub 网页端**

1. 浏览器打开代码仓库。
2. 点击 **Pull requests** → **New pull request**。
3. 选择 `base: main` 和 `compare: refactor/package-structure`。
4. 点击 **Create pull request** 提交。
5. 等待 CI 运行，变绿 ✅ 后，点击 **Merge pull request** → **Confirm merge**。

---

### 12. Bob 同步更新

**📍 角色：Bob | 目录：`calculator-bob/`**

Bob 回来工作时，需要拉取最新的包结构代码，并进行可编辑安装：

```powershell
git switch main
git pull origin main
pip install -e .
```

---
[⬅ 上一节：Lab 6: CI 红绿灯](./lab06-ci-red-green.md) | [目录](../LEARNING_PLAN.md) | [下一节：Lab 8: CLI 入口 ➡](./lab08-cli.md)
