# 管理员指南

## 1. 职责范围

管理员负责：

- 接入新源仓
- 维护 GitHub Actions Secrets
- 维护 Casdoor 本地账号和 GitHub 登录
- 维护宿主机 `Nginx`、Docker 认证服务和 Redis 网络
- 处理部署失败与回滚

## 2. 接入一个新源仓

1. 要求源仓按 [源文档标准](../04-project-development/04-design/source-docs-standard.md) 改造 `docs/`
2. 在 `config/source-repos.json` 中增加仓库定义
3. 同一条仓库定义同时补齐 `modes.local` 和 `modes.remote`
4. 外部仓库远程模式统一使用 `submodule_sparse`
5. 本地模式统一指向维护机上可直接访问的项目 `docs/` 目录，优先使用相对路径
6. `git_url` 必须能被构建环境访问；在当前默认方案里，这个构建环境是 GitHub Actions Runner
7. 分别验证两种模式：

```bash
uv run python scripts/sync_sources.py --config config/source-repos.json --project-root . --source-mode local
uv run python scripts/build_site.py --config config/source-repos.json --project-root . --output-dir .generated --source-mode local
uv run python scripts/sync_sources.py --config config/source-repos.json --project-root . --source-mode remote
uv run python scripts/build_site.py --config config/source-repos.json --project-root . --output-dir .generated --source-mode remote
```

8. 检查：
   - `.generated/authz/permissions.json`
   - `.generated/nginx/private_locations.conf`

## 3. Casdoor 账号与 GitHub 登录

### 本地账号

- 至少保留一个本地管理员账号
- 本地账号数据存在 Casdoor SQLite 中
- 忘记密码时优先通过 Casdoor 后台重置，不要直接改数据库

### GitHub 登录

Casdoor 当前对 GitHub 登录更推荐使用 GitHub App。配置顺序是：

1. 在 GitHub 中创建一个 GitHub App
2. 把 GitHub App 的 `Client ID` / `Client Secret` 填到 Casdoor 的 GitHub Provider
3. 在 Casdoor Application 中启用该 Provider
4. 保持 `redirect_url=https://docs.example.com/oauth2/callback`

至少核对：

- GitHub App 的 callback URL
- Casdoor 应用中启用该身份源
- oauth2-proxy `client_id/client_secret` 与 Casdoor 应用保持一致

详细步骤见 [云服务器部署与 CI/CD 实操](cloud-server-cicd-playbook.md)。

## 4. GitHub Actions Secrets

Workflow 依赖这些 Secrets：

| Secret | 说明 |
| --- | --- |
| `DOCS_DEPLOY_HOST` | 服务器地址 |
| `DOCS_DEPLOY_USER` | SSH 用户 |
| `DOCS_DEPLOY_SSH_KEY` | 部署私钥 |
| `DOCS_DEPLOY_PORT` | SSH 端口 |
| `DOCS_DEPLOY_SITE_DIR` | 宿主机静态站点目录，例如 `/var/www/docs-stratego`；不填时使用 workflow 默认值 |
| `DOCS_PRIVATE_LOCATIONS_PATH` | 宿主机私有规则文件路径，例如 `/etc/nginx/snippets/docs-stratego/private_locations.conf`；不填时使用 workflow 默认值 |
| `DOCS_RELOAD_HOST_NGINX` | 是否在部署后 reload 宿主机 Nginx，默认 `1` |

日常发布默认不再通过 Actions 在服务器侧执行 `git pull + build`，也不要求每次重启 Docker 认证服务；这些动作只保留给首次部署或维护机上的应急全量重建。

## 5. 首次服务器引导

第一次上服务器至少要做这些事：

1. 用 sparse-checkout 拉取认证运行目录，只保留 `deploy/docker-compose.yml`、`deploy/casdoor/`、`deploy/oauth2-proxy/`
2. 创建 `/var/www/docs-stratego`
3. 创建 `/etc/nginx/snippets/docs-stratego/private_locations.conf`
4. 创建 Docker 网络 `docs-auth-internal`
5. 确认 Redis 继续保留在原有业务网络中，主机名为 `redis`
6. 确认 `oauth2-proxy` 将接入 Redis 所在网络，而不是迁移 Redis
7. 由运维手工安装宿主机 `Nginx` 配置
8. 编辑 `deploy/casdoor/app.conf`
9. 编辑 `deploy/oauth2-proxy/oauth2-proxy.cfg`
10. 手工启动 `docker compose -f deploy/docker-compose.yml up -d`
11. 在浏览器中完成一次认证链路验证
12. 触发一次 GitHub Actions 文档发布

如需一次性验证全量重建链路，请在完整仓库工作区中额外执行 `bash scripts/deploy_remote.sh`，不要在生产服务器的稀疏运行目录里直接执行。

## 6. 日常发布排障

如果 Actions 失败，按这个顺序查：

1. SSH 连通性
2. `validate` job 是否已经先失败
3. Runner 侧 `sync_sources.py` 是否能拉取外部源仓
4. Runner 侧 `mkdocs build` 是否失败
5. `site/` 是否上传到服务器目标目录
6. `private_locations.conf` 是否安装到 `/etc/nginx/snippets/docs-stratego/private_locations.conf`
7. `nginx -t` 或 reload 是否失败
8. 如需核对构建结果，再下载本次 Actions artifact 中的 `site/` 与 `private_locations.conf`
9. 如本次同时改动运行时配置，再检查 `docker compose up -d` 是否失败
10. 确认部署账号是否仍能无密码执行 `sudo nginx -t`、`sudo systemctl reload nginx` 和目标目录下的 `install/mv/rm`

## 7. 不要做的事

- 不要在根仓手工维护页面权限
- 不要接受没有根 `docs/index.md` 清单的源仓
- 不要让 `config/source-repos.json` 继续依赖本机绝对路径
- 不要把 `deploy/oauth2-proxy/oauth2-proxy.cfg` 的真实密钥提交到 Git
- 不要让部署脚本自动覆盖宿主机 `Nginx` 站点配置
