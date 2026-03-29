# 部署手册

## 1. 适用范围

本文描述 `docs-stratego` 在云服务器上的标准部署方式：

- 宿主机：`Nginx`
- Docker：`casdoor`、`oauth2-proxy`、已存在的 `redis`
- 触发方式：GitHub Actions 构建并上传静态制品与权限规则文件

## 2. 构建与发布步骤

Runner 侧构建：

```bash
uv sync
uv run python scripts/sync_sources.py --config config/source-repos.json --project-root . --source-mode remote
uv run python scripts/build_site.py --config config/source-repos.json --project-root . --output-dir .generated --source-mode remote
uv run mkdocs build -f .generated/mkdocs.generated.yml -d site
```

服务器侧发布：

- 上传 `site/` 到 `/var/www/docs-stratego`
- 安装 `private_locations.conf` 到 `/etc/nginx/snippets/docs-stratego/private_locations.conf`
- 将 `site/` 与 `private_locations.conf` 作为 Actions artifact 保留 7 天
- 需要时执行 `sudo nginx -t && sudo systemctl reload nginx`
- 仅当认证镜像或运行时配置变化时，再执行 `docker compose -f deploy/docker-compose.yml up -d`

注意：

- 首次部署建议按“HTTP 引导配置 -> Certbot -> HTTPS 正式配置”顺序执行
- 运维负责审核并安装 `Nginx` 配置，发布脚本不会自动覆盖 `/etc/nginx/sites-available/*.conf`
- 详细步骤见 [安装说明](../../02-user-guide/installation.md)

## 3. 关键目录

- `sources/`
  外部源仓文档的稀疏同步目录
- `.generated/site_docs/`
  MkDocs 实际读取的聚合文档目录
- `.generated/authz/permissions.json`
  页面权限清单
- `.generated/nginx/private_locations.conf`
  Runner 生成的宿主机 Nginx 私有页面规则源文件
- `/etc/nginx/snippets/docs-stratego/private_locations.conf`
  服务器实际使用的宿主机 Nginx 私有页面规则
- `site/` 或服务器 `/var/www/docs-stratego`
  最终静态站点目录
- `deploy/casdoor/app.conf`
  Casdoor 运行配置
- `deploy/oauth2-proxy/oauth2-proxy.cfg`
  oauth2-proxy 运行配置

## 4. 宿主机 Nginx 责任

- 服务静态站点目录
- 代理 `/oauth2/*` 到 `127.0.0.1:4180`
- 代理认证域名到 `127.0.0.1:8000`
- 引入 `/etc/nginx/snippets/docs-stratego/private_locations.conf`
- 为私有页面调用 `auth_request`
- 由运维手工安装和变更站点配置

## 5. Docker 责任

### Casdoor

- 提供本地用户名密码和 GitHub 登录
- 使用 Postgres 保存账号与应用配置

### oauth2-proxy

- 接入 Casdoor OIDC
- 使用 Redis 保存会话
- 向宿主机 Nginx 暴露 `auth_request` 接口
- 同时加入 `docs-auth-internal` 和 Redis 所在现有网络

### Redis 网络建议

- 可以让单个容器加入多个 Docker 网络
- 推荐做法不是迁移 Redis，而是让 `oauth2-proxy` 额外加入 Redis 已经所在的网络
- `casdoor` 不必加入 Redis 网络，保持只在文档站内部网络即可

## 6. GitHub Actions 责任

- 在 `main/master` push 后触发
- 先执行 CI 校验：依赖安装、单元测试、站点元数据生成、MkDocs 构建
- 在 Runner 中产出 `site/`、`.generated/nginx/private_locations.conf`、`.generated/authz/permissions.json`
- SSH 登录服务器并上传 `site/`，同时安装 `private_locations.conf`
- 将 `site/` 与 `private_locations.conf` 额外保留为 7 天 artifact
- 如权限规则发生变化，执行 `nginx -t` 与 reload
- 仅在认证栈变更时，额外执行 Docker 服务更新

## 7. 发布检查点

- `config/source-repos.json` 中的仓库已同时声明 `local` / `remote` 两种模式
- Runner 构建时显式使用 `DOCS_SOURCE_MODE=remote`
- `.generated/authz/permissions.json` 中存在私有页面
- `.generated/nginx/private_locations.conf` 已生成
- `site/` 已上传到服务器静态目录
- 宿主机站点配置已经手工引入 `/etc/nginx/snippets/docs-stratego/private_locations.conf`
- 宿主机 `nginx -t` 通过
- 认证栈未变更时，不要求每次执行 `docker compose up -d`
- 登录链路完整

## 8. 回滚

优先做法：

1. 重新发布上一个稳定 commit/tag 对应的制品
2. 重新同步 `site/` 与 `/etc/nginx/snippets/docs-stratego/private_locations.conf`
3. reload 宿主机 `Nginx`

如需在维护机做一次完整重建：

```bash
cd ~/docs-stratego-full
git checkout <stable-tag-or-commit>
export SKIP_GIT_PULL=1
bash scripts/deploy_remote.sh
```

回滚不会清空：

- Casdoor Postgres 数据
- Redis 会话库

如果你需要强制用户重新登录，可以单独清理 Redis 中 oauth2-proxy 使用的会话键。
