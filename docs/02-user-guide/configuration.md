# 配置说明

## 1. 配置分层

当前部署有四层配置：

| 层级 | 位置 | 作用 | 是否允许进仓 |
| --- | --- | --- | --- |
| 源仓文档配置 | 各项目 `docs/index.md` | 页面路径、顺序、权限 | 是 |
| 根仓站点配置 | `config/source-repos.json` | 站点接入源仓与同步方式 | 是 |
| 认证运行配置 | `deploy/casdoor/app.conf`、`deploy/oauth2-proxy/oauth2-proxy.cfg` | 登录、OIDC、Redis、会话 | 服务器运行时文件 |
| 宿主机网关配置 | `Nginx` 站点 conf | 静态站点、私有页面拦截、认证域名反代 | 服务器运行时文件 |

## 2. 关键配置项

### 2.1 `config/source-repos.json`

当前推荐写法是只保留一份 `config/source-repos.json`，并在同一条仓库定义里同时声明两种 source mode：

- `local`
  本地调试直接读取维护机上的项目文档目录
- `remote`
  GitHub Actions 或正式生产构建时，先初始化 submodule，再在子仓内显式拉取目标分支后构建文档

规则收口为：

- `source-repos.json` 是唯一源仓配置文件
- 每个仓库都必须同时声明 `modes.local` 与 `modes.remote`
- 本地开发默认使用 `source_mode=local`
- 本地生产预演使用 `source_mode=remote`
- GitHub Actions 正式生产构建使用 `source_mode=remote`
- 只要某个仓库保留在 `source-repos.json` 中，remote 构建就会真实拉取并校验它

顶层字段：

| 字段 | 说明 | 示例 |
| --- | --- | --- |
| `version` | 配置版本 | `3` |
| `default_source_mode` | 默认模式 | `local` |

关键字段：

| 字段 | 说明 | 示例 |
| --- | --- | --- |
| `name` | 站点路径前缀 | `crawler4j` |
| `title` | 顶部导航展示名 | `蛛行演略` |
| `modes.local.source_type` | 本地模式来源类型 | `local` |
| `modes.local.local_path` | 本地文档目录 | `../../PythonProject/crawler4j/docs` |
| `modes.remote.source_type` | 远程模式来源类型 | `submodule_sparse` |
| `modes.remote.git_url` | 远程 Git 地址 | `https://github.com/uroborus2s/crawler4j.git` |
| `modes.remote.branch` | 远程分支 | `main` |
| `modes.remote.submodule_path` | 子模块路径 | `sources/crawler4j` |
| `modes.remote.docs_path` | 稀疏展开的文档目录 | `docs` |

示例：

```json
{
  "version": 3,
  "default_source_mode": "local",
  "repositories": [
    {
      "name": "crawler4j",
      "title": "蛛行演略",
      "repo_url": "https://github.com/uroborus2s/crawler4j",
      "modes": {
        "local": {
          "source_type": "local",
          "local_path": "../../PythonProject/crawler4j/docs"
        },
        "remote": {
          "source_type": "submodule_sparse",
          "git_url": "https://github.com/uroborus2s/crawler4j.git",
          "branch": "main",
          "submodule_path": "sources/crawler4j",
          "docs_path": "docs"
        }
      }
    }
  ]
}
```

推荐入口：

- 新增仓库：优先执行 [CLI 命令](contributor-guide/cli.md) 中的 `uv run docs-stratego source add`
- 移除仓库：优先执行 [CLI 命令](contributor-guide/cli.md) 中的 `uv run docs-stratego source remove --yes`
- 手工编辑 `config/source-repos.json` 只建议在批量修订或排障场景使用

### 2.2 `deploy/casdoor/app.conf`

关键项：

| 配置 | 说明 | 建议 |
| --- | --- | --- |
| `driverName` | 认证数据存储类型 | `postgres` |
| `dataSourceName` | 数据源占位符 | `${DB_DSN}` |
| `httpport` | 容器内监听端口 | `8000` |

### 2.3 `deploy/oauth2-proxy/oauth2-proxy.cfg`

关键项：

| 配置 | 说明 | 示例 |
| --- | --- | --- |
| `oidc_issuer_url` | Casdoor 外部地址 | `https://auth.docs.example.com` |
| `redirect_url` | 文档站回调地址 | `https://docs.example.com/oauth2/callback` |
| `client_id` | Casdoor 应用 ID | 手工填写 |
| `client_secret` | Casdoor 应用密钥 | 手工填写 |
| `cookie_secret` | Cookie 加密密钥 | 32 字节 Base64 |
| `session_store_type` | 会话存储方式 | `redis` |
| `redis_connection_url` | Redis 地址 | `redis://redis:6379/0` |

### 2.4 GitHub Actions 制品发布路径

日常发布走“Runner 构建 + 上传制品”时，至少要明确这些服务器路径：

| 变量 | 说明 | 示例 |
| --- | --- | --- |
| `DOCS_DEPLOY_SITE_DIR` | 宿主机静态站点目录；不填时 workflow 默认使用 `/var/www/docs-stratego` | `/var/www/docs-stratego` |
| `DOCS_PRIVATE_LOCATIONS_PATH` | 宿主机私有规则文件路径；不填时 workflow 默认使用 `/etc/nginx/snippets/docs-stratego/private_locations.conf` | `/etc/nginx/snippets/docs-stratego/private_locations.conf` |
| `DOCS_RELOAD_HOST_NGINX` | 发布后是否 reload 宿主机 Nginx | `1` |

Actions Variables：

| 变量 | 说明 | 示例 |
| --- | --- | --- |
| `DOCS_SOURCE_APP_ID` | 源码读取 GitHub App 的 App ID | `1234567` |

Actions Secrets：

| Secret | 说明 | 示例 |
| --- | --- | --- |
| `DOCS_SOURCE_APP_PRIVATE_KEY` | 推荐；源码读取 GitHub App 的私钥 | `-----BEGIN RSA PRIVATE KEY-----` |
| `DOCS_STRATEGO_SYNC_PAT` | 推荐；根仓更新共享 bot 分支和 PR 的写入凭证 | `github_pat_xxx` |

默认同步目标：

- `/var/www/docs-stratego`
- `/etc/nginx/snippets/docs-stratego/private_locations.conf`

默认构建 artifact：

- `site/`
- `.generated/nginx/private_locations.conf`

其中：

- 服务器真正消费 `site/` 与 `private_locations.conf`
- artifact 的主要用途是把 `validate` job 的构建结果传给 `deploy` job
- workflow 会强制使用 GitHub App installation token 读取私有源仓
- workflow 已关闭 `actions/checkout` 的持久化凭证，避免根仓 `GITHUB_TOKEN` 干扰后续跨仓拉取

### 2.5 子仓自动通知根仓的配置

如果启用“子仓 `docs/**` 变更 -> 根仓共享 bot PR”方案，还需要固定这些配置项：

| 位置 | 名称 | 说明 |
| --- | --- | --- |
| 子仓文件 | `.github/workflows/notify-docs-stratego.yml` | 子仓文档变更通知根仓的 workflow 文件 |
| 子仓 Secret | `DOCS_STRATEGO_DISPATCH_TOKEN` | 子仓向根仓发送 `repository_dispatch` 的凭证 |
| 根仓事件名 | `source-pointer-sync-requested` | 子仓通知根仓时使用的事件名 |
| 根仓 bot 分支 | `bot/sync-source-pointers` | 汇总所有已落后子仓指针的自动化分支 |
| 根仓共享 PR 标题 | `chore: sync source repository pointers` | reviewer 识别共享 PR 的固定标题 |

设计边界：

- 子仓通知 workflow 只对目标分支的 `docs/**` 生效。
- 根仓共享 bot PR 必须先经人工审核，不能直接代替发布 workflow。
- 根仓通过 `Sync Source Pointers` 工作流自动维护 PR 内容，多个子仓连续通知会收敛到同一个 PR。
- 推荐通过 [CLI 命令](contributor-guide/cli.md) 中的 `source scaffold-notify` 生成或移除源仓通知 workflow，避免手写模板漂移。


## 3. 模式边界

这里需要明确区分两件事：

- `source_mode`
  只决定“文档从哪里读”，取值只有 `local` 或 `remote`
- `运行场景`
  决定“这次构建是本地开发、本地生产预演，还是正式生产发布”

推荐口径：

| 运行场景 | 典型入口 | `source_mode` | 说明 |
| --- | --- | --- | --- |
| 本地开发 | `uv run docs-stratego dev --project-root .` | `local` | 直接读取维护机本地工作副本，迭代最快 |
| 本地生产预演 | `uv run docs-stratego dev --project-root . --build-only --source-mode remote` 或手动 `docs-stratego sync + docs-stratego build + mkdocs build` | `remote` | 用远程仓输入做一次接近正式发布的静态构建验证 |
| 正式生产发布 | GitHub Actions `validate -> deploy` | `remote` | 强制从 GitHub 远程仓库重新拉取，验证真实发布输入 |

补充说明：

- 当前 `docs-stratego dev` 会在 `source_mode=local` 下自动重新执行 `sync` 和 `build`
- `source_mode=remote` 仍然是一轮式预演，修改远程输入后需要重跑命令
- 具体操作见 [本地开发与预览](local-development.md)

## 4. 维护机全量重建

如果走 `scripts/deploy_remote.sh` 做全量重建，需要一个包含完整仓库的维护工作区；标准生产服务器上的稀疏运行目录不适合直接执行它。

| 变量 | 说明 | 示例 |
| --- | --- | --- |
| `PROJECT_ROOT` | 完整仓库工作区目录 | `~/docs-stratego-full` |
| `SITE_DIR` | 静态站点目录 | `/var/www/docs-stratego` |
| `DOCKER_COMPOSE_FILE` | Compose 文件路径 | `~/docs-stratego-full/deploy/docker-compose.yml` |
| `DOCS_INTERNAL_DOCKER_NETWORK` | 文档站内部网络 | `docs-auth-internal` |
| `DOCS_REDIS_DOCKER_NETWORK` | Redis 所在现有网络 | `webapp_wps_net` |

## 5. 环境差异

### 本地开发

- 可以直接运行 `uv run docs-stratego dev --project-root .`
- 默认 `source_mode=local`
- 如需模拟远程仓构建，可运行 `uv run docs-stratego dev --project-root . --source-mode remote`
- 修改真实本地源文档后，会自动触发重建
- 如需重新确认远程仓输入，需重新启动 `docs-stratego dev --source-mode remote`
- 本地模式直接依赖维护机上的项目工作副本
- 本地不一定跑宿主机 Nginx
- 主要验证目录、页面、主题和导航

### 测试/生产服务器

- 默认 `source_mode=remote`
- 必须使用真实域名
- `cookie_secure=true`
- Casdoor 必须有至少一个本地管理员账号
- 宿主机 `Nginx` 必须能反代文档域名和认证域名
- GitHub Actions 默认在 Runner 侧构建，再把 `site/` 与 `private_locations.conf` 上传到服务器
- `site/` 与 `private_locations.conf` 默认作为 artifact 保留 7 天，供作业间传递和排障时下载
- 服务器标准运行目录只需要稀疏拉取的 `deploy/` 运行文件，不需要完整仓库与 Python 构建环境
- 宿主机 `Nginx` 站点配置由运维按安装文档手工维护，不再作为仓库模板交付

## 6. 配置变更要求

改下面任一内容时，必须同步更新文档：

- 域名
- `redirect_url`
- Redis 地址、容器主机名或 Docker 网络
- 静态站点目录
- `PRIVATE_LOCATIONS_PATH`
- GitHub Actions Secrets
- source mode 的本地路径或远程仓库分支

建议同时更新：

- [部署与 CI/CD 设计](../04-project-development/04-design/deployment-architecture.md)
- [部署手册](../04-project-development/08-operations-maintenance/deployment-guide.md)
- [服务器部署 SOP](../04-project-development/08-operations-maintenance/server-deployment-sop.md)
- [阅读者指南](reader-guide.md)
- [管理员指南](admin-guide.md)
