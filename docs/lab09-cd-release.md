# Lab 9: 持续交付 — 自动化发版与 GitHub Release

> 🎯 **学习目标**：掌握持续交付（CD）的核心理念，学会使用 GitHub Actions 自动化构建和发版，理解语义化版本控制（SemVer）与 Git Tag 的运用。
> 📂 **工作区**：`calculator-alice/`
> ⏱ **预估耗时**：40 分钟

**前置状态**：项目为完整的 Python 包，CI 流水线正常运行，CLI 已完成。

---

## 1. 切换工作区并创建分支

**📍 角色：Alice | 目录：`calculator-alice/`**

Alice 将负责构建持续交付（CD）流程。首先确保在 `main` 分支最新状态，并创建用于编写 CD 脚本的新分支。

```powershell
Set-Location e:\Coding\MyCode\Learning\learn-cicd\calculator-alice
git switch main
git pull origin main
git switch -c ci/cd-pipeline
```

> **知识讲解：CD（持续交付 vs 持续部署）**
> - **Continuous Delivery (持续交付)**：将软件自动构建、测试，并随时准备好以自动化的方式发布到生产环境或制品库。发版往往需要人工介入触发。
> - **Continuous Deployment (持续部署)**：进一步自动化，任何通过 CI 的代码都会直接无缝部署到生产环境，无需人工干预。

---

## 2. 编写 CD 流水线配置

**📍 角色：Alice | 目录：`calculator-alice/`**

在 `.github/workflows/` 目录下创建 `cd.yml`，我们将配置一个在打出特定格式的 Git Tag 时触发的自动化发版流水线。

创建并编辑 `.github/workflows/cd.yml`，完整文件内容如下：

```yaml
name: CD

on:
  push:
    tags:
      - "v*.*.*"

permissions:
  contents: write

jobs:
  release:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Set up Python 3.13
        uses: actions/setup-python@v5
        with:
          python-version: "3.13"

      - name: Install build tools
        run: |
          python -m pip install --upgrade pip
          pip install build

      - name: Build package
        run: python -m build

      - name: Generate changelog
        id: changelog
        run: |
          echo "## Changes" > CHANGELOG.md
          echo "" >> CHANGELOG.md
          git log $(git describe --tags --abbrev=0 HEAD^ 2>/dev/null || git rev-list --max-parents=0 HEAD)..HEAD --pretty=format:"- %s (%h)" >> CHANGELOG.md
          echo "" >> CHANGELOG.md
          cat CHANGELOG.md

      - name: Create GitHub Release
        uses: softprops/action-gh-release@v2
        with:
          body_path: CHANGELOG.md
          files: dist/*
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

> **深度剖析 CD 脚本细节**：
> - `on: push: tags: - "v*.*.*"`：这代表流水线不会在普通 push 触发，只有在推送到以 `v` 开头且包含点的 tag 时才运行（如 `v1.0.0`）。
> - `permissions: contents: write`：授予 GitHub Actions 写入仓库内容的权限，这样它才能创建 Release。
> - `fetch-depth: 0`：在代码检出时，默认只会拉取最新的一层提交（浅克隆）。`0` 表示拉取完整的提交历史，这是因为后续我们需要通过遍历 Git 历史记录来自动生成变更日志（Changelog）。
> - `python -m build`：调用 `build` 模块，默认会读取 `pyproject.toml` 并生成标准构建产物：源码包（sdist，`.tar.gz` 格式）和编译包（wheel，`.whl` 格式）。
> - `Generate changelog` 步骤：使用 `git log` 和正则表达式技巧，提取当前 Tag 与上一个 Tag 之间的所有提交信息，写入到 `CHANGELOG.md` 中。
> - `softprops/action-gh-release`：这是一个第三方 Action，利用我们生成的 Changelog 自动创建一个 GitHub Release，并将 `dist/*` 里的构建产物作为附件上传。
> - `GITHUB_TOKEN`：这是 GitHub 自动注入到流水线上下文中的身份令牌，用于安全的 API 调用，使该 action 有权在仓库里创建 Release。

---

## 3. 更新包版本号

**📍 角色：Alice | 目录：`calculator-alice/`**

既然我们要进行正式发布，我们需要把原本 `0.1.0` 的版本号提升为正式的 `1.0.0`。

修改 `pyproject.toml`，完整文件如下：

```toml
[build-system]
requires = ["setuptools>=68.0"]
build-backend = "setuptools.build_meta"

[project]
name = "python-calculator"
version = "1.0.0"
description = "A simple calculator package"
requires-python = ">=3.10"

[project.scripts]
calculator = "calculator.cli:main"

[tool.setuptools.packages.find]
where = ["src"]
```

> **知识讲解：语义化版本（SemVer）**
> 版本号格式为 `主版本号.次版本号.修订号` (MAJOR.MINOR.PATCH)，如 `1.0.0`。
> - 主版本号 (MAJOR)：做了不兼容的 API 修改。
> - 次版本号 (MINOR)：做了向下兼容的新功能新增。
> - 修订号 (PATCH)：做了向下兼容的问题修正。
> 我们之前是 `0.x` 的实验性版本，现在功能完备，发布为正式的 `1.0.0` 纪念碑式版本。

---

## 4. 提交并推送 CD 变更

**📍 角色：Alice | 目录：`calculator-alice/`**

保存所有的更改，提交并推送到远程仓库。

```powershell
git status
git add .
git status
git commit -m "ci: add CD pipeline for automated releases"
git push origin ci/cd-pipeline
```

### ✅ 检查点（Checkpoint）
> **预期输出**：代码无冲突，CD 分支成功推送到 GitHub 远程仓库。
> **预期状态**：现在流水线**尚未触发发版**，因为我们只是合并代码，还没有打 Tag。

---

## 5. 在 GitHub 完成 PR 合并

**📍 操作位置：GitHub 网页端**

1. 浏览器打开项目 GitHub 仓库页面。
2. 针对 `ci/cd-pipeline` 发起 Pull Request。
3. 等待基本的 CI 检查通过。
4. 点击 **Merge pull request** 并 **Confirm merge**。
5. 删除 `ci/cd-pipeline` 分支。

---

## 6. 同步主干，并正式打 Tag 发布

**📍 角色：Alice | 目录：`calculator-alice/`**

现在主分支 `main` 包含了我们最新的 CD 流程配置。Alice 需要切回 `main` 并把这些拉取到本地，然后打上第一个版本标签！

```powershell
git switch main
git pull origin main
```

接下来，我们创建一个带有附注的 Git Tag：

```powershell
git tag -a v1.0.0 -m "Release v1.0.0: Full calculator with CLI"
```

> **知识讲解：Git Tag 的概念**
> 标签（Tag）相当于给某个特定提交记录打上一个静态的“快照”标记。常用于标记发布点（如 `v1.0.0`，`v2.0`）。与分支（Branch）会随着新提交移动不同，标签指向的提交是固定的。

把这个新建的标签推送到远程仓库（注意：普通的 `git push` 不会推送标签）：

```powershell
git push origin v1.0.0
```

---

## 7. 见证自动化 CD 奇迹

**📍 操作位置：GitHub 网页端**

1. 导航到 GitHub 项目主页。
2. 点击上方的 **Actions** 标签，你会看到一个名为 **CD** 的流水线正在运行，它的触发原因是 `v1.0.0` 这个 tag！
3. 点进流水线，查看运行的详细步骤（你会看到它安装依赖、构建包、生成 Changelog 等）。
4. **耐心等待该流水线运行并标绿完成**。
5. 返回仓库主页，点击右侧侧边栏的 **Releases** 标题（或进入 `/releases` 页面）。
6. 你会看到 **v1.0.0** 已经被自动创建！
   - 内容中包含通过 git log 自动生成的 **Changelog**。
   - 在 **Assets** 下方，你会看到自动打包出来的产物：`.whl` 和 `.tar.gz` 文件。

> **知识讲解：构建产物（wheel 与 sdist）**
> - **sdist** (Source Distribution): 源分发包（`.tar.gz`），包含未编译的源码。
> - **wheel**: 编译后的二进制分发包格式（`.whl`），安装速度更快，是当今 Python 发版的标准。

---

# 🎓 恭喜毕业！

你已经完成了从零到一的完整 CI/CD 学习旅程。以下是你掌握的技能清单：

- ✅ Git 分支管理与协同工作流（GitHub Flow）
- ✅ Pull Request 全生命周期（创建、审查、批注、修改、合并）
- ✅ Code Review 实战（行级批注、Request Changes、Approve）
- ✅ Merge Conflict 解决（冲突标记识别、手动合并、重新提交）
- ✅ pytest 自动化测试（断言、异常测试、测试驱动思维）
- ✅ GitHub Actions CI 流水线（flake8 + pytest）
- ✅ Branch Protection Rules（质量门禁）
- ✅ CI 故障排查与修复闭环
- ✅ Python 包结构与模块化重构
- ✅ CLI 交互入口设计
- ✅ CD 自动化发版（Tag 触发、Changelog、GitHub Release、构建产物）

---
[⬅ 上一节：Lab 8: CLI 入口](./lab08-cli.md) | [目录](../LEARNING_PLAN.md)
