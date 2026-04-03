# CLI 分发与发布

这页回答的是：怎样把 `docs-stratego` CLI 从“只在根仓本地可用”，演进成“外部源仓可以直接安装和执行”。

如果你现在已经准备实际发版，请直接读 [CLI 发布手册](release.md)。

## 1. 当前边界

当前仓库里的命令入口：

```bash
uv run docs-stratego ...
```

只对这类场景天然成立：

- 你在 `docs-stratego` 根仓里
- 当前环境已经安装了这个项目本身
- CI 正在这个仓库里执行

它不等于“任意源仓天然可用”。

## 2. 外部源仓推荐怎么用

### 2.1 一次性执行

推荐用 `uvx`：

```bash
uvx --from 'docs-stratego==<version>' docs-stratego source validate --repo-path .
```

适合：

- 接入仓临时校验
- 一次性生成通知 workflow
- CI 中按版本拉起命令

### 2.2 常驻安装

推荐用 `uv tool install`：

```bash
uv tool install 'docs-stratego==<version>'
docs-stratego source validate --repo-path .
```

适合：

- 某个团队长期维护多个接入仓
- 需要把 CLI 固定到同一台机器或 Runner 上

## 3. 推荐发布路径

### 方案 A：发布到私有 PyPI 仓库

适用场景：

- CLI 主要给同组织的接入仓使用
- 还不确定是否要对外公开
- 默认值、命名和工作流明显偏向组织内部

优点：

- 分发方便
- 不暴露组织内实现细节
- 可以先验证版本治理和安装体验

### 方案 B：发布到公开 PyPI

适用场景：

- 你希望任何外部接入方都能直接安装
- CLI 已经足够通用
- 项目命名、README、元数据和发布策略都准备好公开

优点：

- 接入成本最低
- 文档里可以直接给出统一安装命令

约束：

- 需要确认包名可用
- 需要准备更完整的公开元数据和发布治理

### 建议顺序

推荐采用：

1. 先打通 TestPyPI
2. 再落正式私有 PyPI
3. 评估后再决定是否同步发布到公开 PyPI

这样最稳。

## 4. 生产可用发布方案

### 4.0 什么时候才需要发新版本

不是“仓库有改动就发包”，而是“CLI 对外行为值得发布时才发包”。

建议把需要发版的变更收口为：

- `src/cli.py`
- `src/source_admin.py`
- `src/source_sync.py`
- `src/site_builder.py`
- `pyproject.toml` 中影响包安装、版本和入口的部分
- 外部源仓会直接感知到的命令、参数、模板或校验逻辑变化

通常不需要单独发版的变更：

- `.factory/` 记忆层
- 纯项目文档
- 只影响根仓内部协作的流程文档
- 不改变已发布包行为的仓库级调整

推荐规则：

1. 平时所有变更只跑普通 CI。
2. 只有确认“外部源仓需要新 CLI 能力”时，才 bump 版本。
3. 只有版本 bump 后，才打 `cli-vX.Y.Z` tag 触发发布。

### 4.1 打包前准备

发布前至少确认：

- `pyproject.toml` 已包含稳定的 `name`、`version`、`project.scripts`
- README 能作为包首页说明
- 版本号采用明确的语义化版本
- CLI 默认值里哪些是组织专用、哪些必须改为参数化，已经想清楚

### 4.2 构建

推荐使用 `uv`：

```bash
uv build --no-sources
```

这会生成标准的 `dist/` 产物。

### 4.3 预发布验证

先推到 TestPyPI 做烟雾测试，再验证：

```bash
uvx --from 'docs-stratego==<version>' docs-stratego --help
uvx --from 'docs-stratego==<version>' docs-stratego source validate --help
```

### 4.4 正式发布

推荐使用 GitHub Actions + Trusted Publishing，而不是长期 PyPI Token。

原因：

- 凭证是短时的
- 不需要把长期上传密钥存进仓库 Secret
- 官方文档已经把它作为推荐路径

发布触发建议：

- 只在推送 `cli-vX.Y.Z` tag 时发布
- 先 build
- 再发布到 TestPyPI
- 烟雾验证通过后发布到正式索引

### 4.5 使用方式

发布后，源仓文档统一给出这两类命令：

- 一次性运行：
  - `uvx --from 'docs-stratego==<version>' docs-stratego ...`
- 常驻安装：
  - `uv tool install 'docs-stratego==<version>'`

## 5. GitHub Actions 方案

推荐工作流结构：

1. `build`
2. `publish-testpypi`
3. `smoke-test`
4. `publish-pypi`

关键点：

- `build` 只负责产出 `dist/`
- 发布作业使用 GitHub Environment
- PyPI / TestPyPI 都使用 Trusted Publishing
- 普通 `push` 不触发发布
- `workflow_dispatch` 只用于手动演练 TestPyPI 或补发
- 正式发布只在 `cli-vX.Y.Z` tag 上运行

## 6. 当前项目的建议

对 `docs-stratego`，我建议采用下面的落地策略：

1. 保留当前根仓内 `uv run docs-stratego ...` 作为开发入口
2. 增加“已发布包”的外部源仓入口，统一文档写法为 `uvx --from 'docs-stratego==<version>' ...`
3. 先打通 TestPyPI 和内部正式索引
4. 等 CLI 默认值、包元数据和版本治理稳定后，再决定是否发布到公开 PyPI

当前推荐的 CI/CD 策略是：

- 普通分支：只跑测试和构建，不发布
- 手动触发：可发布到 TestPyPI，或在确认需要时发布到两边
- 版本 tag：自动走 `TestPyPI -> smoke test -> PyPI`

## 7. 参考安装口径

### 根仓内

```bash
uv run docs-stratego source add ...
```

### 外部源仓

```bash
uvx --from 'docs-stratego==<version>' docs-stratego source validate --repo-path .
```

## 8. 参考资料

- [Python Packaging User Guide: Publishing with GitHub Actions](https://packaging.python.org/en/latest/guides/publishing-package-distribution-releases-using-github-actions-ci-cd-workflows/)
- [PyPI Docs: Trusted Publishers](https://docs.pypi.org/trusted-publishers/using-a-publisher/)
- [uv Docs: Building and publishing a package](https://docs.astral.sh/uv/guides/package/)
