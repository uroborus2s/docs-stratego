# 管理员指南 (Admin Guide)

管理员负责聚合站点的基础设施维护、外部仓库接入管理以及权限体系的治理。

## 1. 职责边界与治理要求
管理员的主要职责是确立标准，而非日常内容更新。
- **治理要求**：禁止在根仓直接改写子仓内容，所有权限和导航必须在源仓层面通过 `index.md` 声明。
- **环境隔离**：区分本地开发环境与生产运行环境。

---

## 2. 部署拓扑与架构逻辑
`docs-stratego` 采用“宿主机 Nginx + 容器化认证栈”的混合架构：

- **宿主机 (Host)**：
  - 静态站点目录（由 GitHub Actions 部署）。
  - Nginx 权限转发配置 (`private_locations.conf`)。
- **容器环境 (Docker)**：
  - **Casdoor**：身份认证中心（Github 登录、本地账号）。
  - **oauth2-proxy**：代理认证网关，负责向 Nginx 提供 `auth_request` 指令。
  - **Redis**：存储 Session 会话状态。

---

## 3. 接入一个新源仓 (Standard Onboarding)

接入新项目是管理员最核心的任务。

1. **源仓改造**：要求源项目按 [源文档标准](../04-project-development/04-design/source-docs-standard.md) 完成其 `docs/` 目录和 `index.md` 改造。
2. **配置定义**：在 `config/source-repos.json` 中新增定义。
   - `local` 模式：指向本地路径。
   - `remote` 模式：配置 Git URL 和 `submodule_sparse` 模式。
3. **权限源安装 (针对私有仓库)**：
   - 必须将私有项目安装给 `docs-stratego-source-reader` GitHub App。
4. **验证构建**：
   ```bash
   uv run python scripts/sync_sources.py --source-mode remote
   uv run python scripts/build_site.py --source-mode remote
   ```
5. **发布变更**：合并 PR 后触发生产环境部署。

---

## 4. 关键凭证管理 (Secrets Management)

所有的生产密钥均存储在 GitHub Actions Secrets 中。

| 分类 | 典型 Secret | 说明 |
| :--- | :--- | :--- |
| **部署权限** | `DOCS_DEPLOY_SSH_KEY` | 用于 SSH 传输 site 文件到生产服务器。 |
| **源码读取** | `DOCS_SOURCE_APP_PRIVATE_KEY` | GitHub App (Source Reader) 的私钥。 |
| **联动凭证** | `DOCS_STRATEGO_SYNC_PAT` | 用于自动同步子仓指针的 Personal Access Token。 |
| **子仓通知** | `DOCS_STRATEGO_DISPATCH_TOKEN` | 配置在各子仓中，用于向根仓发送 `repository_dispatch`。 |
| **认证配置** | `CASDOOR_POSTGRES_PWD` | 容器环境内部敏感密码。 |

---

## 5. 首次引导与后续维护
- **首次部署**：请参阅 [安装说明 (Installation)](installation.md)。
- **深度配置**：关于 Redis 共享或多域名配置，请参阅 [配置说明 (Configuration)](configuration.md)。
- **日常排障**：如遇构建失败，按 [维护者指南 (Operator Guide)](operator-guide.md) 的故障处理矩阵排查。
