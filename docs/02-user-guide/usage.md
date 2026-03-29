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

验证页面路径、导航和构建结果。

### 前置条件

- 已安装 `uv`
- 本机已存在 `crawler4j` 和 `obsync-root` 的工作副本，用于本地模式直接读取

### 操作步骤

```bash
cd <project-root>
./start.sh
```

如果你要在本机先更新子仓，再模拟服务器侧的远程构建：

```bash
cd <project-root>
./start.sh --source-mode remote
```

### 成功判断

- `http://127.0.0.1:8001/` 可访问
- 顶部导航和左侧目录显示正常
- `local` 模式下直接读取本机项目目录中的 `docs/`
- `remote` 模式下 `sources/` 中会更新远程 submodule，并只展开 `docs/` 目录

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
- GitHub Secrets 已按管理员指南配置
- 服务器已经手工部署成功过一次
- 双域名、证书和 GitHub 登录配置可按 [云服务器部署与 CI/CD 实操](cloud-server-cicd-playbook.md) 补齐

### 操作步骤

1. 提交变更到 `main` 或 `master`
2. 等待 GitHub Actions 执行 `Deploy Docs`
3. 在 Actions 日志中确认 `site/` 与 `private_locations.conf` 上传完成
4. 如本次权限规则发生变化，确认 workflow 已执行 `nginx -t && reload`
5. 如需排障，可下载保留 7 天的 Actions artifact，查看 `site/` 与 `private_locations.conf`

### 成功判断

- Workflow 为绿色
- 服务器上静态站点已更新
- `private_locations.conf` 与本次权限规则一致
- 私有页面仍然正常登录

## 5. 私有页面验证

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

## 6. 回滚

### 目标

快速恢复上一版稳定文档。

### 操作步骤

1. 在 Git 中选定上一个稳定 commit 或 tag
2. 重新触发该版本对应的发布 workflow，或把仓库回退后重新 push
3. 如果自动发布不可用，再在完整仓库维护工作区中使用 `bash scripts/deploy_remote.sh` 做全量回退 fallback

### 成功判断

- 首页版本已回退
- 私有页和认证流程正常

## 7. 常见异常与处理

- 构建失败：先看 `config/source-repos.json` 是否仍指向有效仓库和分支，再检查 `sources/<repo>/docs` 是否已初始化
- 登录失败：优先检查 `oidc_issuer_url`、`redirect_url`、Casdoor 应用配置和运维安装的 `Nginx` 配置
- 私有页匿名可见：检查 `/etc/nginx/snippets/docs-stratego/private_locations.conf`
- Actions 成功但页面没更新：检查 `/var/www/docs-stratego` 是否与运维安装的宿主机 Nginx `root` 一致，以及 `site/` 是否上传到了正确目录
- 权限改了但效果没变：检查 `/etc/nginx/snippets/docs-stratego/private_locations.conf` 是否已同步到服务器，并确认 `nginx reload` 已执行
