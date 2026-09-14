# Lab 8: CLI 交互入口 — 编写命令行计算器

> 🎯 **学习目标**：理解并实现 CLI 交互式应用（REPL），学习 `if __name__ == "__main__"` 的用法，以及通过 `pyproject.toml` 配置命令行入口点（console_scripts）。
> 📂 **工作区**：`calculator-bob/`
> ⏱ **预估耗时**：30 分钟

**前置状态**：项目已重构为包结构（`src/calculator/`），CI 流水线正常运行。

---

## 1. 切换工作区并创建分支

**📍 角色：Bob | 目录：`calculator-bob/`**

Bob 将负责为计算器添加命令行界面（CLI）。首先，确保我们在主分支上拥有最新代码，并创建一个新分支。

```powershell
Set-Location e:\Coding\MyCode\Learning\learn-cicd\calculator-bob
git switch main
git pull origin main
git switch -c feat/cli-interface
```

> **知识讲解：CLI 与 REPL**
> - **CLI** (Command Line Interface)：命令行界面，允许用户通过控制台文本与程序交互。
> - **REPL** (Read-Eval-Print Loop)：“读取-求值-输出”循环，是交互式编程环境的基本形态，用户输入一段指令，系统执行并输出结果，然后等待下一次输入。

---

## 2. 编写 CLI 代码

**📍 角色：Bob | 目录：`calculator-bob/`**

创建 `src/calculator/cli.py` 文件，实现完整的 REPL 交互循环。

使用你喜欢的编辑器，或者使用以下命令（需要手动写入内容）创建或编辑 `src/calculator/cli.py`，完整文件内容如下：

```python
from calculator import add, subtract, multiply, divide, power


OPERATIONS = {
    "+": add,
    "-": subtract,
    "*": multiply,
    "/": divide,
    "**": power,
}


def display_menu():
    """Display the calculator menu."""
    print("\n===== Python Calculator =====")
    print("Available operations: +, -, *, /, **")
    print("Type 'quit' or 'q' to exit.")
    print("============================\n")


def get_number(prompt):
    """Prompt user for a number and return it."""
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("Invalid input. Please enter a number.")


def main():
    """Main REPL loop for the calculator."""
    display_menu()

    while True:
        operation = input("Enter operation (+, -, *, /, **, or quit): ").strip()

        if operation.lower() in ("quit", "q"):
            print("Goodbye!")
            break

        if operation not in OPERATIONS:
            print(f"Unknown operation: '{operation}'. Please try again.")
            continue

        a = get_number("Enter first number: ")
        b = get_number("Enter second number: ")

        try:
            result = OPERATIONS[operation](a, b)
            print(f"\n  {a} {operation} {b} = {result}\n")
        except (ValueError, TypeError) as e:
            print(f"\n  Error: {e}\n")


if __name__ == "__main__":
    main()
```

> **知识讲解：`if __name__ == "__main__":` 的作用**
> 当一个 Python 文件被直接运行时（如 `python cli.py`），其 `__name__` 变量的值为 `__main__`；如果它是被其他模块 `import` 导入的，则 `__name__` 的值为模块名。使用这种写法可以使得文件既能作为脚本直接执行，又能在作为模块被导入时不自动运行 `main()` 函数。

---

## 3. 保持现有导出不变

**📍 角色：Bob | 目录：`calculator-bob/`**

确保 `src/calculator/__init__.py` 保持不变，包含之前所有的函数导出。完整文件内容如下：

```python
from .operations import add, subtract, multiply, divide, power

__all__ = ["add", "subtract", "multiply", "divide", "power"]
```

---

## 4. 添加命令入口点配置

**📍 角色：Bob | 目录：`calculator-bob/`**

更新项目根目录下的 `pyproject.toml` 文件，添加 `[project.scripts]` 以配置 `console_scripts`，这样用户可以通过输入 `calculator` 直接启动程序。

修改 `pyproject.toml`，完整文件如下：

```toml
[build-system]
requires = ["setuptools>=68.0"]
build-backend = "setuptools.build_meta"

[project]
name = "python-calculator"
version = "0.1.0"
description = "A simple calculator package"
requires-python = ">=3.10"

[project.scripts]
calculator = "calculator.cli:main"

[tool.setuptools.packages.find]
where = ["src"]
```

> **知识讲解：`console_scripts` 入口点**
> 配置文件中的 `calculator = "calculator.cli:main"` 告诉打包工具（如 pip 和 setuptools）：
> 在安装这个包时，创建一个名为 `calculator` 的可执行命令，当执行这个命令时，调用 `calculator.cli` 模块中的 `main` 函数。

---

## 5. 本地安装与测试

**📍 角色：Bob | 目录：`calculator-bob/`**

以可编辑模式重新安装当前包，以激活新的命令行脚本。

```powershell
pip install -e .
```

现在测试我们的 CLI 应用！可以通过直接运行脚本模块的方式启动：

```powershell
python -m calculator.cli
```

也可以直接输入我们在配置文件里声明的命令（如果环境配置正确）：

```powershell
calculator
```

**模拟交互过程**：
```
===== Python Calculator =====
Available operations: +, -, *, /, **
Type 'quit' or 'q' to exit.
============================

Enter operation (+, -, *, /, **, or quit): +
Enter first number: 2
Enter second number: 3

  2.0 + 3.0 = 5.0

Enter operation (+, -, *, /, **, or quit): quit
Goodbye!
```

### ✅ 检查点（Checkpoint）
> **预期输出**：成功进入 REPL 循环，测试执行一次加法操作（`2 + 3 = 5`），并能通过输入 `quit` 退出程序。
> **预期状态**：本地修改就绪，运行无报错，命令行工具表现符合预期。

---

## 6. 提交修改并推送到远程仓库

**📍 角色：Bob | 目录：`calculator-bob/`**

将我们开发的 CLI 界面代码提交并推送。

```powershell
git status
git add .
git status
git commit -m "feat: add CLI REPL interface for calculator"
git push origin feat/cli-interface
```

---

## 7. 在 GitHub 提交并发起合并请求

**📍 操作位置：GitHub 网页端**

1. 浏览器打开项目 GitHub 仓库页面。
2. 点击绿色的 **Compare & pull request** 按钮（针对 `feat/cli-interface` 分支）。
3. 检查标题，可以输入描述，然后点击 **Create pull request**。
4. 等待 GitHub Actions 执行（CI 验证）。
5. 当状态显示全绿（All checks have passed）后，点击 **Merge pull request**，然后 **Confirm merge**。
6. 点击 **Delete branch** 清理远程分支。

---

## 8. Alice 同步最新代码

**📍 角色：Alice | 目录：`calculator-alice/`**

Bob 的新功能已经合并，现在 Alice 需要把主干代码同步到她本地的工作区。

```powershell
Set-Location e:\Coding\MyCode\Learning\learn-cicd\calculator-alice
git switch main
git pull origin main
```

可以通过 `git log -1` 确认刚合并的提交已经到了本地。

---
[⬅ 上一节：Lab 7: 模块化重构](./lab07-refactor.md) | [目录](../LEARNING_PLAN.md) | [下一节：Lab 9: CD 自动发版 ➡](./lab09-cd-release.md)
