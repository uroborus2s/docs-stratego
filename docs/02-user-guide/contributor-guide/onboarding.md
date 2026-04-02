# 接入聚合站点

这页回答的是：当源仓文档已经合规后，怎样把它正式登记到 `docs-stratego`。

## 1. 接入前提

开始之前，先确认两件事：

1. 你的源仓已经满足 [源文档标准](source-docs-standard.md)。
2. 你手里有源仓本地路径、远程 Git 地址、目标分支和展示标题。

## 2. 先在源仓做结构校验

在源仓本地执行：

```bash
uv run docs-stratego source validate --repo-path /path/to/source-repo
```

这条命令会复用根仓当前的解析规则，检查：

- 根 `docs/index.md` 是否存在且结构合法
- 声明到导航里的页面是否真实存在
- 每个内容目录是否有 `index.md`
- OpenAPI / MCP tools 契约是否满足最低要求

## 3. 在根仓登记源仓

进入 `docs-stratego` 根仓后，执行：

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

这条命令会更新：

- `config/source-repos.json`

如果你希望它同时把远程仓注册为根仓 submodule，再追加：

```bash
--register-submodule
```

如果你想先看计划写入内容，不真正落盘，追加：

```bash
--dry-run
```

## 4. 远程构建验证

登记完成后，在根仓执行一次接近 CI 的验证：

```bash
uv run docs-stratego sync --project-root /path/to/docs-stratego --source-mode remote
uv run docs-stratego build --project-root /path/to/docs-stratego --source-mode remote
uv run mkdocs build -f /path/to/docs-stratego/.generated/mkdocs.generated.yml -d /path/to/docs-stratego/site
```

验证目标：

- 根仓能真实拉到该源仓
- submodule 路径与配置一致
- 构建器能解析源仓导航、权限和契约

## 5. 接入完成后还差什么

接入成功只说明“根仓认识这个源仓”。

如果你还希望源仓 `docs/**` 变更后自动通知根仓，还要继续完成 [自动联动](automation.md)。

## 6. 接入验收清单

- [ ] 源仓本地校验通过
- [ ] `config/source-repos.json` 已新增仓库定义
- [ ] 如使用 remote 模式，submodule 已成功注册
- [ ] `sync --source-mode remote` 通过
- [ ] `build --source-mode remote` 通过
- [ ] `mkdocs build` 通过
