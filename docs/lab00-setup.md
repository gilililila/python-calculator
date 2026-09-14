# Lab 0: 环境准备与双人工作区搭建

> 🎯 **学习目标**：在 GitHub 上创建项目仓库，并在本地搭建模拟多人的隔离工作区，验证基本连通性。
> 📂 **工作区**：`e:\Coding\MyCode\Learning\learn-cicd`
> ⏱ **预估耗时**：20 分钟

---

## 1. 在 GitHub 网页端创建仓库

**📍 操作位置：GitHub 网页端**

我们需要先在 GitHub 上创建一个用于练习的公开仓库。

1. 登录你的 GitHub 账号（你的用户名是 `Gilililila`）。
2. 点击右上角的 **+** 图标，在下拉菜单中选择 **New repository**。
3. 在 **Repository name** 框中输入：`python-calculator`。
4. 将仓库可见性设置为 **Public**。
5. 勾选 **Add a README file** （这会帮我们初始化仓库并创建第一次提交）。
6. 勾选 **Add .gitignore**，并在右侧的下拉菜单中搜索并选择 **Python** 模板（这会帮我们忽略 Python 相关的临时文件或编译文件）。
7. 点击绿色的 **Create repository** 按钮完成创建。

### ✅ 检查点（Checkpoint）
> **预期输出**：你将看到名为 `python-calculator` 的仓库主页。
> **预期状态**：仓库中已有 `README.md` 和 `.gitignore` 文件，并且产生了初始提交（Initial commit）。

---

## 2. 克隆双工作区

**📍 角色：开发者 | 目录：`e:\Coding\MyCode\Learning\learn-cicd`**

为了模拟真实的团队协作环境，我们将在同一台电脑上创建两个不同的目录，分别代表 Alice 和 Bob 的工作区。

打开你的 **Windows PowerShell**，进入我们的学习目录并执行克隆命令：

```powershell
Set-Location e:\Coding\MyCode\Learning\learn-cicd
git clone git@github.com:Gilililila/python-calculator.git calculator-alice
git clone git@github.com:Gilililila/python-calculator.git calculator-bob
```

### ✅ 检查点（Checkpoint）
> **预期输出**：克隆成功的提示信息，如 `Resolving deltas: 100%...` 等。
> **预期状态**：在当前目录下，你将看到两个新的文件夹：`calculator-alice` 和 `calculator-bob`，它们包含了相同的仓库内容。

---

## 3. 配置身份隔离

为了让后续的提交记录清晰地展示出是 Alice 还是 Bob 做的修改，我们需要为每个工作区单独配置 Git 身份信息。

**📍 角色：Alice | 目录：`calculator-alice/`**

进入 Alice 的工作区，并设置局部（`--local`）的用户名和邮箱：

```powershell
Set-Location .\calculator-alice
git config --local user.name "Alice"
git config --local user.email "alice@example.com"
```

验证配置是否成功：

```powershell
git config user.name
git config user.email
```

**📍 角色：Bob | 目录：`calculator-bob/`**

进入 Bob 的工作区，同样设置局部的身份信息：

```powershell
Set-Location ..\calculator-bob
git config --local user.name "Bob"
git config --local user.email "bob@example.com"
```

验证配置是否成功：

```powershell
git config user.name
git config user.email
```

### ✅ 检查点（Checkpoint）
> **预期输出**：在 `calculator-alice` 下执行验证命令输出 "Alice" 和 "alice@example.com"；在 `calculator-bob` 下输出 "Bob" 和 "bob@example.com"。
> **预期状态**：两个工作区的身份互不干扰。这得益于 `--local` 参数，它只会修改当前仓库（即 `.git/config`）的配置。

---

## 4. SSH 连通性验证

**📍 角色：开发者 | 目录：任意位置**

确保你的本地电脑可以通过 SSH 正常连接到 GitHub：

```powershell
ssh -T git@github.com
```

### ✅ 检查点（Checkpoint）
> **预期输出**：`Hi Gilililila! You've successfully authenticated, but GitHub does not provide shell access.`
> **预期状态**：SSH 密钥配置正确，拥有拉取和推送代码的权限。

---

## 5. 验证克隆结果

让我们看看刚克隆下来的仓库的历史记录。

**📍 角色：Alice | 目录：`calculator-alice/`**

```powershell
Set-Location ..\calculator-alice
git log --oneline
```

**📍 角色：Bob | 目录：`calculator-bob/`**

```powershell
Set-Location ..\calculator-bob
git log --oneline
```

### ✅ 检查点（Checkpoint）
> **预期输出**：一行关于初始提交的记录，例如 `a1b2c3d Initial commit`（前面的哈希值会有所不同）。
> **预期状态**：Alice 和 Bob 现在都处于与远端仓库相同的起点，准备开始协作开发！

---
[目录](../LEARNING_PLAN.md) | [下一节：Lab 1: 第一次提交与 PR ➡](./lab01-first-commit.md)
