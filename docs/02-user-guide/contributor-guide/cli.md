# CLI 命令

本页收口所有“本地开发预览、接入、校验、联动、移除、共享 PR 同步、构建”相关命令。

## 0. 先按任务找命令

| 你要做什么 | 最先看的命令 |
| --- | --- |
| 本地启动开发站点 | `docs-stratego dev` |
| 校验一个源仓是否合规 | `docs-stratego source validate` |
| 把源仓登记到根仓 | `docs-stratego source add` |
| 给源仓生成通知 workflow | `docs-stratego source scaffold-notify` |
| 从根仓移除一个源仓 | `docs-stratego source remove` |
| 手工补跑共享指针同步 | `docs-stratego source sync-pointers` |
| 分步执行同步和构建 | `docs-stratego sync` / `docs-stratego build` |

## 1. 先区分两种运行模式

### 1.1 根仓内开发模式

适用场景：

- 你在 `docs-stratego` 根仓里开发、测试或跑 CI
- 命令来自当前仓库自己的虚拟环境

入口：

```bash
uv run docs-stratego --help
```

### 1.2 外部源仓使用模式

适用场景：

- 你在某个接入源仓里直接执行校验或通知脚手架
- 你不想要求接入方先克隆 `docs-stratego` 根仓

推荐入口：

```bash
uvx --from 'docs-stratego==<version>' docs-stratego --help
```

或安装成常驻工具：

```bash
uv tool install 'docs-stratego==<version>'
docs-stratego --help
```

说明：

- `uv run docs-stratego ...` 只适合当前仓库已经把 `docs-stratego` 作为本地项目装进环境的场景。
- 外部源仓若直接照抄 `uv run docs-stratego ...`，通常不会成立。
- 如果你需要外部源仓直接使用 CLI，请先看 [CLI 分发与发布](distribution.md)。

## 2. 源仓侧命令

### 2.1 校验源仓文档结构

```bash
uvx --from 'docs-stratego==<version>' docs-stratego source validate --repo-path /path/to/source-repo
```

用途：

- 检查根 `docs/index.md`
- 检查页面声明与目录 `index.md`
- 检查 OpenAPI / MCP tools 契约最低要求

### 2.2 生成自动通知 workflow

```bash
uvx --from 'docs-stratego==<version>' docs-stratego source scaffold-notify \
  --repo-path /path/to/source-repo \
  --branch main
```

常用参数：

- `--root-repository`：目标根仓，默认 `uroborus2s/docs-stratego`
- `--branch`：可重复传入，指定哪些分支监听 `docs/**`
- `--dry-run`：只演练，不写文件

### 2.3 删除自动通知 workflow

```bash
uvx --from 'docs-stratego==<version>' docs-stratego source scaffold-notify \
  --repo-path /path/to/source-repo \
  --remove
```

## 3. 根仓侧命令

### 3.1 接入一个新源仓

```bash
uv run docs-stratego source add \
  --project-root /path/to/docs-stratego \
  --name atlas \
  --title 星图 \
  --repo-url https://github.com/example/atlas \
  --git-url https://github.com/example/atlas.git \
  --local-path ../atlas/docs \
  --branch main
```

常用参数：

- `--register-submodule`：同时注册 remote submodule
- `--submodule-path`：自定义 submodule 目录，默认 `sources/<name>`
- `--docs-path`：远程稀疏展开目录，默认 `docs`
- `--dry-run`：只演练，不落盘

### 3.2 移除一个源仓

```bash
uv run docs-stratego source remove \
  --project-root /path/to/docs-stratego \
  --name atlas \
  --yes
```

常用参数：

- `--remove-submodule`：连 submodule 一起移除
- `--dry-run`：只演练，不落盘

安全约束：

- 必须显式带 `--yes`
- `docs-stratego` 自身不会被允许移除

### 3.3 手动同步共享 bot PR

```bash
uv run docs-stratego source sync-pointers \
  --project-root /path/to/docs-stratego
```

用途：

- 拉取 remote 模式下的全部源仓指针
- 收敛 `sources/*` gitlink 变化
- 复用或更新共享 bot PR

常用参数：

- `--branch`：共享 bot 分支，默认 `bot/sync-source-pointers`
- `--title`：共享 PR 标题，默认 `chore: sync source repository pointers`
- `--config`：源仓配置文件，默认 `config/source-repos.json`

### 3.4 本地快速预览开发站点

```bash
uv run docs-stratego dev --project-root /path/to/docs-stratego
```

用途：

- 顺序执行 `sync -> build -> mkdocs serve`
- 默认使用 `source_mode=local`，直接读取维护机本地工作副本，并自动监听源文档变化
- 适合根仓维护者本地调试和预览，不作为外部源仓默认入口

常用参数：

- `--source-mode remote`：用远程仓输入做接近生产的预演
- `--build-only`：只做 `mkdocs build`，不启动预览服务
- `--host` / `--port`：调整本地监听地址
- `--site-dir`：调整 `mkdocs build` 的输出目录

热更新边界：

- `source_mode=local`：支持对根仓 `docs/`、本地源仓 `docs/` 和 `config/source-repos.json` 的自动重建
- `source_mode=remote`：仍然是一轮式预演，不会持续轮询远程仓
- 如果你需要重新确认远程输入，请重新执行 `docs-stratego dev --source-mode remote`

## 4. 构建链路命令

### 4.1 同步源仓

```bash
uv run docs-stratego sync --project-root /path/to/docs-stratego --source-mode remote
```

### 4.2 生成构建输入

```bash
uv run docs-stratego build --project-root /path/to/docs-stratego --source-mode remote
```

`dev` 负责本地开发预览；`sync` 和 `build` 仍是当前仓库和 CI 的正式分步入口，不再保留独立 Python 包装脚本。

## 5. 推荐使用顺序

### 新接入

1. `source validate`
2. `source add`
3. `source scaffold-notify`
4. `sync`
5. `build`

### 下线

1. `source scaffold-notify --remove`
2. `source remove --yes`
3. `sync`
4. `build`

### 共享 bot PR 补跑

1. `source sync-pointers`
2. 等待共享 PR 更新
3. 通过 `sync` / `build` 或对应 CI 校验结果确认可合并

## 6. 版本建议

- 根仓 CI 和本地开发可以继续使用当前工作区里的 `uv run docs-stratego ...`
- 外部源仓应当固定版本，不建议直接跑未锁定的 latest
- 推荐样式：

```bash
uvx --from 'docs-stratego==<version>' docs-stratego source validate --repo-path .
```

如果你准备让外部源仓长期使用这个 CLI，请继续阅读 [CLI 分发与发布](distribution.md)。
