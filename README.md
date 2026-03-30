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
- `src/docs_stratego/`
  稀疏同步、元数据解析、站点构建和权限清单生成逻辑
- `scripts/sync_sources.py`
  更新 submodule 并只展开源仓 `docs/`
- `scripts/build_site.py`
  生成 `.generated/site_docs/`、`permissions.json`、Nginx 私有规则和 MkDocs 配置
- `scripts/deploy_remote.sh`
  面向完整仓库工作区的全量重建与应急部署入口；标准生产服务器不依赖它做日常发布
- `deploy/`
  Casdoor、oauth2-proxy 与宿主机 Nginx 配置模板

## 快速开始

```bash
uv sync
uv run python scripts/sync_sources.py --config config/source-repos.json
uv run python scripts/build_site.py --config config/source-repos.json --output-dir .generated
uv run mkdocs build -f .generated/mkdocs.generated.yml -d site
```

本地快速重建并启动预览：

```bash
./start.sh
```

如果要在本机模拟服务器侧的远程拉仓行为：

```bash
./start.sh --source-mode remote
```

`start.sh` 内部统一使用 `uv sync`、`uv run python` 和 `uv run mkdocs`，不再直接调用 `.venv/bin/...`。

如果虚拟环境或缓存异常，需要删除 `.venv` 并用 `uv` 重新初始化：

```bash
./start.sh --reset-venv
```

当前正式配置已经包含 5 个项目：

- `docs-stratego`
- `crawler4j`
- `stratix`
- `ride-loop`
- `shanforge`

当前配置文件已经支持同一仓库条目下的两种来源模式：

- `local`
  本地调试直接读取本机项目目录中的 `docs/`
- `remote`
  远程构建先初始化 submodule，再在子仓内显式 `fetch + checkout` 目标分支，并只保留顶层 `docs/`

因此本地预览和 GitHub Actions 会走同一套同步逻辑，只是 source mode 不同；`start.sh` 也会在构建前先执行 `scripts/sync_sources.py`。

## 文档标准

正式标准见 [source-docs-standard.md](./docs/04-project-development/04-design/source-docs-standard.md)。

最关键的约束是：

- 每个目录都必须有 `index.md`
- 只有根 `docs/index.md` 声明 `mkdocs.nav`
- 根 `docs/index.md` 的正文只写简介和维护说明，不再重复写目录树或章节清单
- 页面私有化只允许在根 `docs/index.md` 的页面节点中声明
- 未声明的 Markdown 页面直接视为构建错误

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
