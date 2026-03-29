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

当前推荐写法是一份配置文件同时声明两种 source mode：

- `local`
  本地调试直接读取维护机上的项目文档目录
- `remote`
  CI/CD 或维护机侧全量重建时先初始化 submodule，再在子仓内显式拉取目标分支后构建文档

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

### 2.2 `deploy/casdoor/app.conf`

关键项：

| 配置 | 说明 | 建议 |
| --- | --- | --- |
| `driverName` | 认证数据存储类型 | `sqlite3` |
| `dataSourceName` | SQLite 路径 | `/data/casdoor.db` |
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

默认同步目标：

- `/var/www/docs-stratego`
- `/etc/nginx/snippets/docs-stratego/private_locations.conf`

默认构建 artifact：

- `site/`
- `.generated/nginx/private_locations.conf`

其中：

- 服务器真正消费 `site/` 与 `private_locations.conf`
- artifact 的主要用途是把 `validate` job 的构建结果传给 `deploy` job

### 2.5 维护机全量重建 fallback

如果走 `scripts/deploy_remote.sh` 做全量重建，需要一个包含完整仓库的维护工作区；标准生产服务器上的稀疏运行目录不适合直接执行它。

| 变量 | 说明 | 示例 |
| --- | --- | --- |
| `PROJECT_ROOT` | 完整仓库工作区目录 | `~/docs-stratego-full` |
| `SITE_DIR` | 静态站点目录 | `/var/www/docs-stratego` |
| `DOCKER_COMPOSE_FILE` | Compose 文件路径 | `~/docs-stratego-full/deploy/docker-compose.yml` |
| `DOCS_INTERNAL_DOCKER_NETWORK` | 文档站内部网络 | `docs-auth-internal` |
| `DOCS_REDIS_DOCKER_NETWORK` | Redis 所在现有网络 | `webapp_wps_net` |

## 3. 环境差异

### 本地开发

- 可以直接运行 `./start.sh`
- 默认 `source_mode=local`
- 如需模拟远程仓构建，可运行 `./start.sh --source-mode remote`
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

## 4. 配置变更要求

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
