# CLI 命令

本页收口所有“接入、校验、联动、移除”相关命令。它们都通过同一个入口执行：

```bash
uv run docs-stratego --help
```

## 1. 源仓侧命令

### 1.1 校验源仓文档结构

```bash
uv run docs-stratego source validate --repo-path /path/to/source-repo
```

用途：

- 检查根 `docs/index.md`
- 检查页面声明与目录 `index.md`
- 检查 OpenAPI / MCP tools 契约最低要求

### 1.2 生成自动通知 workflow

```bash
uv run docs-stratego source scaffold-notify \
  --repo-path /path/to/source-repo \
  --branch main
```

常用参数：

- `--root-repository`：目标根仓，默认 `uroborus2s/docs-stratego`
- `--branch`：可重复传入，指定哪些分支监听 `docs/**`
- `--dry-run`：只演练，不写文件

### 1.3 删除自动通知 workflow

```bash
uv run docs-stratego source scaffold-notify \
  --repo-path /path/to/source-repo \
  --remove
```

## 2. 根仓侧命令

### 2.1 接入一个新源仓

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

### 2.2 移除一个源仓

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

## 3. 构建链路命令

### 3.1 同步源仓

```bash
uv run docs-stratego sync --project-root /path/to/docs-stratego --source-mode remote
```

### 3.2 生成构建输入

```bash
uv run docs-stratego build --project-root /path/to/docs-stratego --source-mode remote
```

这两条命令是对现有同步和构建脚本的正式 CLI 封装。CI 仍可继续使用脚本包装层，但面向接入方的推荐入口已经切到 `docs-stratego`。

## 4. 推荐使用顺序

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
