# Lab 5: 持续集成 — 搭建 GitHub Actions CI 流水线
> 🎯 **学习目标**：理解持续集成（CI）的核心理念，学会使用 GitHub Actions 编写和运行 CI 流水线，掌握分支保护规则的设置。
> 📂 **工作区**：`calculator-alice/` 及 GitHub 网页端
> ⏱ **预估耗时**：40 分钟

**前置状态**：`main` 分支有完整的四则运算 `calculator.py` 和 `test_calculator.py`。

---

## 1. 创建配置分支

**📍 角色：Alice | 目录：`calculator-alice/`**

Alice 将负责搭建项目的持续集成（CI）流水线。首先，她创建一个新分支：

```powershell
git switch main
git pull origin main
git switch -c ci/setup-pipeline
```

---

## 2. 编写 CI 配置文件

**📍 角色：Alice | 目录：`calculator-alice/`**

GitHub Actions 的配置文件必须存放在特定的 `.github/workflows` 目录下。Alice 需要先创建这个目录，然后再创建配置文件。

```powershell
New-Item -ItemType Directory -Path .github/workflows -Force
```

接下来，创建或编辑 `.github/workflows/ci.yml`，填入以下完整内容：

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

      - name: Run flake8 linting
        run: flake8 . --count --show-source --statistics

      - name: Run pytest
        run: pytest -v
```

### 💡 知识讲解：YAML 配置解析
- `name`: 流水线的名称，会在 GitHub 界面显示。
- `on`: 触发条件。这里定义了当向 `main` 分支推送（`push`）或发起针对 `main` 的拉取请求（`pull_request`）时触发流水线。
- `jobs`: 流水线包含的任务。这里我们只定义了一个名为 `test` 的任务。
- `runs-on`: 指定运行该任务的服务器操作系统。这里使用 `ubuntu-latest`（最新版 Ubuntu Linux）。**为什么不用 Windows？** 因为 Linux 环境启动速度快，且在 Python 生态中运行测试更为普遍和轻量。
- `steps`: 任务包含的具体执行步骤，按顺序运行。
- `uses`: 调用预先写好的 GitHub Actions。例如 `actions/checkout@v4` 用于将代码拉取到虚拟机上，`actions/setup-python@v5` 用于配置 Python 环境。
- `with`: 为 `uses` 调用的动作提供参数。
- `run`: 在虚拟机上执行的 Shell 命令。

---

## 3. 添加依赖配置文件（推荐）

**📍 角色：Alice | 目录：`calculator-alice/`**

为了让 CI 能够顺利安装依赖，建议将依赖写入 `requirements.txt` 文件。

创建并写入 `requirements.txt`：

```text
pytest>=7.0
flake8>=6.0
```

---

## 4. 提交并推送配置

**📍 角色：Alice | 目录：`calculator-alice/`**

Alice 将新配置提交到代码库并推送到远程：

```powershell
git status
git add .github/workflows/ci.yml requirements.txt
git commit -m "ci: add GitHub Actions CI pipeline with flake8 and pytest"
git push origin ci/setup-pipeline
```

---

## 5. 验证 CI 流水线运行

**📍 操作位置：GitHub 网页端**

1. 切换到 GitHub 网页端，点击 **Compare & pull request** 发起针对 `ci/setup-pipeline` 的 PR。
2. 在 PR 创建完毕后，向下滚动到页面底部，你会看到出现了一个正在运行的 **CI 状态检查**。
3. 点击检查项旁边的 **Details**，进入 GitHub Actions 日志页面。

### 💡 知识讲解：CI 日志结构
在 Actions 页面，你可以看到清晰的层次结构：
- **Workflow**: 对应你的 YAML 配置文件（这里叫 CI）。
- **Job**: 对应配置文件中的 `jobs`（这里叫 test）。
- **Step**: Job 里的每一个执行步骤。你可以点开每一步，查看终端输出（例如 `Run pytest` 的输出结果）。

等待片刻，直到所有步骤完成。当图标变成绿色勾 ✅，表示 CI 流水线运行成功。

---

## 6. 合并配置分支

**📍 操作位置：GitHub 网页端**

既然 CI 流水线已经成功运行并验证了代码没有问题，就可以将配置合并到 `main` 分支了：
1. 点击 **Merge pull request** → **Confirm merge**。

### ✅ 检查点（Checkpoint）
> **预期输出**：`main` 分支包含了 `.github/workflows/ci.yml` 和 `requirements.txt`。
> **预期状态**：GitHub Actions 已经激活，未来每次 PR 都会自动运行。

---

## 7. 设置分支保护规则 (Branch Protection)

仅仅有 CI 是不够的。如果不阻止代码直接推送到 `main` 分支，或者在 CI 失败时仍允许合并，CI 就失去了意义。我们需要配置分支保护规则。

**📍 操作位置：GitHub 网页端**

1. 在仓库主页，点击顶部的 **Settings** 选项卡。
2. 在左侧边栏，点击 **Rules** 下的 **Rulesets**，然后点击 **New branch ruleset**（或在旧版 UI 中点击 **Branches** → **Add branch protection rule**）。
3. 命名规则，例如 "Protect main"。
4. 设置 **Target branches** 为包含默认分支（或明确指定 `main`）。
5. 勾选 **Require a pull request before merging**。这会阻止任何人直接推送代码到 `main` 分支。
6. 勾选 **Require status checks to pass before merging**。
7. 在下方的搜索框中，输入你的 job 名称（即 `test`），并将其添加为必须通过的检查项。
8. 滚动到底部，点击 **Save changes** / **Create**。

### 💡 知识讲解：分支保护的意义
分支保护强制要求所有更改都必须通过 PR 引入，且必须通过自动化测试。这确保了 `main` 分支的代码永远是健康和可部署的。

---

## 8. 验证保护规则是否生效

**📍 角色：Alice | 目录：`calculator-alice/`**

为了验证规则，Alice 尝试直接推送到 `main` 分支：

```powershell
git switch main
git pull origin main
echo "# test direct push" >> README.md
git add README.md
git commit -m "test: try direct push to main"
git push origin main
```

**预期结果**：
你将会看到 `push` 命令失败，并出现类似以下的错误提示：
`remote: error: GH006: Protected branch update failed for refs/heads/main.`
`remote: error: At least 1 approving review is required by reviewers with write access.`

这证明分支保护生效了！直接推送被阻止。

我们需要回退掉这个无效的本地提交：

```powershell
git reset --hard HEAD~1
```

### ✅ 检查点（Checkpoint）
> **预期输出**：直接推送被拒绝，本地撤销了测试提交。
> **预期状态**：强制通过 PR 且带有 CI 检查的开发流程已正式建立。

---
[⬅ 上一节：Lab 4: 合并冲突](./lab04-merge-conflict.md) | [目录](../LEARNING_PLAN.md) | [下一节：Lab 6: CI 红绿灯 ➡](./lab06-ci-red-green.md)
