# 用户指南

## 1. 这套站点解决什么问题

`docs-stratego` 是一个单站点文档聚合与页面级权限入口。多个项目继续在各自源仓维护 `docs/`，根仓只负责：

- 稀疏同步外部仓库的 `docs/`
- 根据根 `docs/index.md` 生成导航和权限清单
- 构建 MkDocs 静态站点
- 通过宿主机 `Nginx` + Docker 内认证服务实现私有页面登录保护

## 2. 两类访问方式

### 2.1 匿名访问

- 公开页面可以直接阅读
- 公开页面出现在和私有页面同一套导航中
- 匿名用户不能直接访问私有页面

### 2.2 登录访问

- 当用户点击私有页面时，`Nginx` 会通过 `auth_request` 转发到 `oauth2-proxy`
- `oauth2-proxy` 再跳转到 Casdoor 登录页
- Casdoor 支持两种登录方式：
  - 本地用户名密码
  - GitHub 登录
- 登录成功后，用户会被带回原始目标页面

## 3. 部署后的标准拓扑

- 宿主机：
  - `Nginx`
  - 静态站点目录，例如 `/var/www/docs-stratego`
  - 私有规则文件，例如 `/etc/nginx/snippets/docs-stratego/private_locations.conf`
- Docker 内：
  - `casdoor`
  - `oauth2-proxy`
  - 已存在的 `redis`
- 认证应用运行目录：
  - 稀疏拉取后的运行目录，例如 `~/docs-stratego`
  - 只保留 `deploy/docker-compose.yml`、`deploy/casdoor/`、`deploy/oauth2-proxy/`

## 4. 日常使用者需要知道的边界

- 页面顺序和权限不在根仓手工维护，而是由源仓根 `docs/index.md` 声明
- 根仓不会改写源仓内容
- 私有页面的正文、图片和附件都会一起受保护
- 如果导航里能看到页面但点开后要求登录，这是设计行为，不是故障

## 5. 首次部署与后续发布的关系

- 首次部署：
  - 手工准备云服务器目录、域名、宿主机 `Nginx`
  - 手工编辑 Casdoor 与 oauth2-proxy 运行配置
  - 手工跑通一次构建、Docker 服务启动和登录验证
- 后续发布：
  - 通过 GitHub Actions 在 `main/master` push 后触发
  - Workflow 在 Runner 中执行 `sync_sources + build_site + mkdocs build`
  - 上传 `site/` 到 `/var/www/docs-stratego`
  - 安装 `private_locations.conf` 到 `/etc/nginx/snippets/docs-stratego/private_locations.conf`
  - 将 `site/` 与 `private_locations.conf` 作为 Actions artifact 保留 7 天，既用于 `validate -> deploy` 交接，也用于短期排障
  - 只有当权限规则变化时才需要 reload 宿主机 `Nginx`
  - Docker 内认证服务通常保持长期运行，只有运行时配置或镜像变化时才更新

## 6. 推荐阅读路径

- 第一次搭环境：看 [安装说明](installation.md)
- 要改域名、回调、Redis、Docker 网络：看 [配置说明](configuration.md)
- 要日常发布、检查、回滚：看 [使用说明](usage.md)
- 要接入新仓、配置 GitHub Secrets、维护账号：看 [管理员指南](admin-guide.md)
