# 使用说明

## 1. 核心任务清单

维护者最常见的任务有 5 个：

1. 本地预览文档站
2. 手工完成首次服务器引导
3. 通过 GitHub push 触发自动发布并上传制品
4. 检查私有页面是否跳转登录
5. 回滚到上一个稳定版本

## 2. 本地预览

### 目标

验证页面路径、导航和构建结果，并区分本地开发模式与本地生产预演模式。

### 前置条件

- 已安装 `uv`
- 本机已存在 `crawler4j` 和 `obsync-root` 的工作副本，用于本地模式直接读取

### 操作步骤

本地开发模式：

```bash
cd <project-root>
./start.sh
```

等价于：

```bash
cd <project-root>
./start.sh --source-mode local
```

本地生产预演模式：

```bash
cd <project-root>
./start.sh --source-mode remote
```

如果你只想重建站点，不启动本地预览服务：

```bash
cd <project-root>
./start.sh --build-only --source-mode local
./start.sh --build-only --source-mode remote
```

### 成功判断

- `http://127.0.0.1:8001/` 可访问
- 顶部导航和左侧目录显示正常
- `local` 模式下直接读取本机项目目录中的 `docs/`，适合日常开发
- `remote` 模式下会按 CI 相同方式更新远程子仓并只展开 `docs/`，适合发布前预演
- `--build-only` 模式下会刷新 `.generated/` 与 `site/`，但不会启动 `mkdocs serve`

## 3. 首次服务器引导

### 目标

完成认证运行目录、宿主机 `Nginx` 和静态站点目录的首次准备。

### 前置条件

- 已按 [安装说明](installation.md) 完成首次准备
- Casdoor 与 oauth2-proxy 配置文件已填写

### 操作步骤

```bash
cd ~/docs-stratego
export DOCKER_COMPOSE_FILE=~/docs-stratego/deploy/docker-compose.yml
export DOCS_INTERNAL_DOCKER_NETWORK=docs-auth-internal
export DOCS_REDIS_DOCKER_NETWORK=webapp_wps_net
docker compose -f deploy/docker-compose.yml up -d
docker compose -f deploy/docker-compose.yml ps
```

### 成功判断

- `docker compose ps` 正常
- `sudo nginx -t` 通过
- `https://auth.docs.example.com` 可访问

## 4. 通过 GitHub 自动发布

### 目标

在提交到 `main/master` 后自动完成 Runner 构建、制品上传和规则同步。

### 前置条件

- `.github/workflows/deploy-docs.yml` 已启用
- GitHub Actions Variables / Secrets 已按安装说明或管理员指南配置
- 服务器已经手工部署成功过一次
- 双域名、证书、GitHub App 和自动发布配置统一按 [安装说明](installation.md) 补齐

### 操作步骤

1. 提交变更到 `main` 或 `master`
2. 等待 GitHub Actions 执行 `Deploy Docs`
3. 在 Actions 日志中确认 `validate` 阶段固定使用 `--source-mode remote`
4. 确认 `site/` 与 `private_locations.conf` 上传完成
5. 如果这次是子仓文档变更，确认你已经触发了根仓 workflow：
   - 直接在根仓 push
   - 手工运行 `workflow_dispatch`
   - 或由子仓向根仓发送 `repository_dispatch: source-docs-updated`
6. 如本次权限规则发生变化，确认 workflow 已执行 `nginx -t && reload`
7. 如需排障，可下载保留 7 天的 Actions artifact，查看 `site/` 与 `private_locations.conf`

### 成功判断

- Workflow 为绿色
- 服务器上静态站点已更新
- `private_locations.conf` 与本次权限规则一致
- 私有页面仍然正常登录

## 5. 子仓文档更新后如何更新网站

### 目标

让 `crawler4j`、`stratix`、`ride-loop` 等子仓的新文档重新进入聚合站点。

### 关键原则

- 子仓文档内容更新后，根仓线上站点不会自动变化，除非根仓 `Deploy Docs` 被再次触发
- GitHub Actions 的正式发布固定使用 `source_mode=remote`
- 因此线上更新看到的永远是“触发发布时，远程仓库上的最新文档状态”

### 常用做法

1. 子仓改完并 push 到配置中声明的目标分支
2. 在根仓手工运行一次 `Deploy Docs`
3. 或者在根仓再 push 一次文档/配置变更
4. 如果后面要做全自动联动，再让子仓调用根仓的 `repository_dispatch: source-docs-updated`

### 成功判断

- 根仓 workflow 成功
- 新文档页面出现在站点里
- 权限和导航与子仓最新 `docs/index.md` 保持一致

## 6. 私有页面验证

### 目标

确认公开页、私有页和资源文件的权限边界正确。

### 操作步骤

1. 匿名打开文档首页
2. 随机访问一个公开页面
3. 再访问一个私有页面
4. 完成登录
5. 回到原页面
6. 再打开私有页面中的图片或附件

### 成功判断

- 公开页不要求登录
- 私有页首次访问跳登录
- 登录后返回原页面
- 私有资源文件同样受保护

## 7. 回滚

### 目标

快速恢复上一版稳定文档。

### 操作步骤

1. 在 Git 中选定上一个稳定 commit 或 tag
2. 重新触发该版本对应的发布 workflow，或把仓库回退后重新 push
3. 如果自动发布不可用，再在完整仓库维护工作区中使用 `bash scripts/deploy_remote.sh` 做一次维护机全量重建

### 成功判断

- 首页版本已回退
- 私有页和认证流程正常

## 8. 常见异常与处理

- 构建失败：先看 `config/source-repos.json` 是否仍指向有效仓库和分支，再检查 `sources/<repo>/docs` 是否已初始化
- `git submodule` 报 `pathspec ... did not match any file(s) known to git`：说明仓库条目虽然写进了 `config/source-repos.json` 或 `.gitmodules`，但还没有真正注册成根仓里的 git submodule
- 登录失败：优先检查 `oidc_issuer_url`、`redirect_url`、Casdoor 应用配置和运维安装的 `Nginx` 配置
- 私有页匿名可见：检查 `/etc/nginx/snippets/docs-stratego/private_locations.conf`
- Actions 成功但页面没更新：检查 `/var/www/docs-stratego` 是否与运维安装的宿主机 Nginx `root` 一致，以及 `site/` 是否上传到了正确目录
- 权限改了但效果没变：检查 `/etc/nginx/snippets/docs-stratego/private_locations.conf` 是否已同步到服务器，并确认 `nginx reload` 已执行
