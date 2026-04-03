# 章略·墨衡

`docs-stratego` 是一个“单站点 + 页面级权限”的文档聚合仓。它的核心目标不是把源仓文档改写成另一套结构，而是：

- 让源仓在自己的 `docs/` 下按统一标准维护文档
- 用 Git submodule + sparse-checkout 只展开外部源仓的 `docs/`
- 在构建前根据根 `docs/index.md` 的全站清单生成导航和权限清单
- 用 MkDocs 生成单个静态站点
- 用 Casdoor + oauth2-proxy + Nginx 对私有页面做登录控制
- 默认关闭匿名全文搜索，避免私有内容进入公开搜索索引

## 当前目录

- `docs/`
  本仓自己的标准化文档源，同时也是外部源仓的写法示例
- `src/`
  CLI、稀疏同步、元数据解析、站点构建和权限清单生成逻辑
- `scripts/deploy_remote.sh`
  面向完整仓库工作区的全量重建与应急部署入口；日常同步与构建统一走 `docs-stratego` CLI，标准生产服务器不依赖它做日常发布
- `deploy/`
  Casdoor、oauth2-proxy 与宿主机 Nginx 配置模板

## 快速开始

```bash
uv sync
uv run docs-stratego dev --project-root .
```

本地快速重建并启动预览：

```bash
uv run docs-stratego dev --project-root .
```

如果要在本机模拟服务器侧的远程拉仓行为：

```bash
uv run docs-stratego dev --project-root . --source-mode remote
```

如果你只想做一次构建、不启动本地预览：

```bash
uv run docs-stratego dev --project-root . --build-only
```

`docs-stratego dev` 内部会顺序执行 `sync -> build -> mkdocs serve`；`--build-only` 时执行 `mkdocs build`。

注意：

- 当前 `docs-stratego dev` 在 `source_mode=local` 下会自动监听根仓 `docs/`、本地源仓 `docs/` 和 `config/source-repos.json`
- 当前 `source_mode=remote` 仍然是一次性预演；如果你改了远程输入配置后要重新确认，请重新运行 `docs-stratego dev --source-mode remote`

如果虚拟环境或缓存异常，直接删除 `.venv` 后重新执行：

```bash
rm -rf .venv
uv sync
```

当前正式配置已经包含 6 个项目：

- `docs-stratego`
- `crawler4j`
- `stratix`
- `ride-loop`
- `shanforge`
- `ctrip_crawler`

当前配置文件已经支持同一仓库条目下的两种来源模式：

- `local`
  本地调试直接读取本机项目目录中的 `docs/`
- `remote`
  远程构建先初始化 submodule，再在子仓内显式 `fetch + checkout` 目标分支，并只保留顶层 `docs/`

因此本地预览和 GitHub Actions 会走同一套同步逻辑，只是 source mode 不同；开发环境统一使用 `docs-stratego dev`，CI 和发布链路仍保持 `docs-stratego sync` 与 `docs-stratego build` 分步执行。

## 文档标准

正式公开标准见 [source-docs-standard.md](./docs/02-user-guide/contributor-guide/source-docs-standard.md)。

最关键的约束是：

- 每个目录都必须有 `index.md`
- 只有根 `docs/index.md` 声明 `mkdocs.nav`
- 根 `docs/index.md` 的正文只写简介和维护说明，不再重复写目录树或章节清单
- 页面私有化只允许在根 `docs/index.md` 的页面节点中声明
- 页面节点除了 `*.md`，还可以声明 `*.openapi.*` 与 `*.mcp-tools.*` 契约文件
- 已声明的 OpenAPI 文件会自动生成 Scalar API Reference 页面；已声明的 MCP tools 快照会自动生成工具参考页，并保留原始 `.yaml/.json` 下载地址
- 未声明的 Markdown 页面直接视为构建错误

源仓接入、自动联动、移除和 CLI 命令说明见 [子仓接入指南](./docs/02-user-guide/usage.md)。
本地开发与预览方式见 [本地开发与预览](./docs/02-user-guide/local-development.md)。

## 认证与部署

- Casdoor：本地账号密码 + GitHub 登录
- oauth2-proxy：提供标准 `auth_request` 接口
- Nginx：服务静态站点，并根据生成的私有页面路径拦截请求
- 运行时配置文件：`deploy/casdoor/app.conf`、`deploy/oauth2-proxy/oauth2-proxy.cfg`
- 推荐发布方式：GitHub Actions 在 Runner 侧构建 `site/` 与 `private_locations.conf`，再把 `site/` 发布到 `/var/www/docs-stratego`、把 `private_locations.conf` 安装到 `/etc/nginx/snippets/docs-stratego/private_locations.conf`；这两份构建产物会作为 artifact 保留 7 天，用于 `validate -> deploy` 作业交接和短期排障；Docker 认证服务通常只在首次部署或运行时配置变更时更新

部署说明见 [deployment-guide.md](./docs/04-project-development/08-operations-maintenance/deployment-guide.md)。  
如果是云服务器私有化部署，请优先阅读：

- [安装说明](./docs/02-user-guide/installation.md)
- [配置说明](./docs/02-user-guide/configuration.md)
- [管理员指南](./docs/02-user-guide/admin-guide.md)
