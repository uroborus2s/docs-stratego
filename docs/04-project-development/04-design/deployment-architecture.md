# 部署与 CI/CD 设计

## 1. 目标

构建一套适用于云服务器私有化部署的交付方案，满足：

- 宿主机已安装 `Nginx`
- 认证服务运行在 Docker 内
- Docker 内已有 `Redis`
- GitHub push 后可直接触发服务器更新

## 2. 运行时拓扑

### 2.1 宿主机

- `Nginx`
- 静态站点目录，例如 `/var/www/docs-stratego`
- Nginx 私有规则文件，例如 `/etc/nginx/snippets/docs-stratego/private_locations.conf`
- 认证应用运行目录，例如 `~/docs-stratego`

### 2.2 Docker

- `casdoor`
- `oauth2-proxy`
- 已存在的 `redis`

### 2.3 域名划分

- `docs.example.com`
  - 公开与私有文档统一入口
  - `/oauth2/*` 交给 oauth2-proxy
- `auth.docs.example.com`
  - 反代到 Casdoor
  - 作为 OIDC Provider 的外部入口

## 3. 权限链路

1. 匿名用户访问私有页面
2. `Nginx` 命中 `/etc/nginx/snippets/docs-stratego/private_locations.conf`
3. `auth_request` 转到 `/oauth2/auth`
4. oauth2-proxy 判断会话是否存在
5. 不存在则跳转到 Casdoor 登录
6. 登录成功后回到原始页面

## 4. 构建链路

日常发布默认在 GitHub Runner 侧完成构建，再把运行时真正消费的制品上传到服务器：

1. Runner 执行 `uv sync`
2. Runner 执行 `uv run docs-stratego sync --source-mode remote`
3. Runner 执行 `uv run docs-stratego build --source-mode remote`
4. Runner 执行 `uv run mkdocs build`
5. 上传 `site/` 到宿主机静态站点目录
6. 安装 `private_locations.conf` 到 `/etc/nginx/snippets/docs-stratego/private_locations.conf`
7. 将 `site/` 与 `private_locations.conf` 作为 Actions artifact 保留 7 天
8. 如权限规则发生变化或采用保守策略，则执行 `nginx -t && reload`

宿主机 `Nginx` 站点配置不在发布时自动覆盖。  
正确流程是：

1. 运维按安装文档手工安装 `/etc/nginx/sites-available/docs.example.com` 与 `/etc/nginx/sites-available/auth.docs.example.com`
2. 首次部署时通过 sparse-checkout 拉取认证运行目录并手工启动 Docker 认证服务
3. 后续发布只更新 `/var/www/docs-stratego` 与 `/etc/nginx/snippets/docs-stratego/private_locations.conf`
4. Docker 认证服务仅在镜像或运行时配置变化时更新

## 5. 配置边界

### 5.1 可进仓内容

- `deploy/docker-compose.yml`
- `scripts/deploy_remote.sh`
- `docs/02-user-guide/installation.md`

### 5.2 运行时内容

- `deploy/casdoor/app.conf`
- `deploy/oauth2-proxy/oauth2-proxy.cfg`
- 宿主机生成后的 `Nginx` 站点配置

原因是运行时内容包含域名、OIDC 密钥、Cookie 密钥等敏感信息。

## 6. Redis 约束

oauth2-proxy 使用 Redis 作为会话存储，要求：

- Redis 保持在现有业务网络中，例如 `webapp_wps_net`
- `oauth2-proxy` 同时加入文档站内部网络和 Redis 所在网络
- `casdoor` 只加入文档站内部网络
- Redis 在 oauth2-proxy 所在网络中需要能通过 `redis:6379` 访问
- 如果现有 Redis 主机名不是 `redis`，运行时必须修改 `redis_connection_url` 或补网络别名

## 7. GitHub Actions 策略

当前选择 Runner 构建后上传制品，而不是每次 SSH 到服务器再执行完整构建。原因：

- 日常发布只需要服务器真正消费的输出：静态站点和权限规则文件
- `Casdoor` / `oauth2-proxy` 作为长驻服务，不需要每次随文档发布重建
- 构建失败会停在 Runner 侧，不会污染服务器当前运行目录
- 认证配置文件仍只保存在服务器运行时目录，不需要从 CI 分发

Workflow 只负责：

- 监听 `main/master` push
- 在 GitHub Runner 中完成依赖安装、单元测试、远程模式 `docs-stratego sync`、`docs-stratego build` 和 `mkdocs build`
- 当远程模式涉及其他私有 GitHub 仓库时，通过 GitHub App 安装令牌为 Git 提供跨仓读取凭证
- 通过 SSH/rsync/scp 上传 `site/` 并安装 `private_locations.conf`
- 将 `site/` 与 `private_locations.conf` 保留为 7 天 artifact，既作为 `validate -> deploy` 的作业交接包，也供排障下载
- 在服务器上执行 `nginx -t` 与可选 reload
- 仅在运行时配置或镜像变化时，另行触发 Docker 认证服务更新

正式策略下，`config/source-repos.json` 是唯一源仓配置文件。只要某个仓库保留在该文件中，GitHub Actions 的 remote 构建就必须真实拉取并校验它；不会再做 repo 级别的条件跳过。

## 8. 回滚策略

回滚优先以“上一版稳定制品”或“上一版稳定 Git 提交”重新发布为单位：

1. 在 GitHub Actions 中重新发布上一个稳定 commit/tag 对应的构建制品
2. 如果自动发布不可用，再在完整仓库维护工作区中执行 `scripts/deploy_remote.sh` 作为全量回退
3. 保持 Casdoor Postgres 数据和 Redis 会话存储不动

## 9. 风险与缓解

| 风险 | 影响 | 缓解 |
| --- | --- | --- |
| 外部源仓分支不存在 | Runner 构建失败 | `config/source-repos.json` 固定真实分支 |
| oauth2-proxy 未接入 Redis 所在网络 | oauth2-proxy 启动失败 | 首次部署前先验证双网络连通性 |
| 域名与回调不一致 | 登录后回不来 | 严格绑定运维手工维护的 Nginx 域名与 `redirect_url` |
| 制品上传不完整 | 页面或权限规则未更新 | 将 `site/`、`private_locations.conf` 作为发布包校验，并保留 7 天 artifact 便于排障 |
| 运维安装的宿主机 Nginx 配置未引入 `/etc/nginx/snippets/docs-stratego/private_locations.conf` | 私有页面不受保护 | 首次上线和每次站点调整后都执行人工配置审查 |
| GitHub Runner 无法读取其他私有源仓 | `docs-stratego sync` 在 `git submodule update` 阶段失败 | 为 workflow 配置 GitHub App 读取凭证，并确认 App 已安装到全部私有源仓 |
