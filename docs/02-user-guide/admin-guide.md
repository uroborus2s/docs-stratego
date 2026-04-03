# 管理员指南

管理员负责的是平台层，不是日常内容编辑。  
这页用来回答“平台该由谁管、该在哪里配、什么时候该改哪一层配置”。

## 1. 管理员最核心的职责

管理员需要保证 4 件事：

1. 平台运行环境可用
2. 根仓能安全读取远程源仓
3. 发布链路和权限边界稳定
4. 外部源仓和 CLI 的治理规则明确

## 2. 先分清什么归管理员管，什么不归

### 2.1 归管理员管

- 服务器与 Docker 认证栈
- GitHub Actions、GitHub App、Secrets、Variables
- PyPI / TestPyPI Trusted Publisher
- 根仓 `config/source-repos.json` 的正式登记

### 2.2 不归管理员直接改

- 源仓具体文档内容
- 子仓页面排序、正文和权限声明
- 根仓里对外公开的页面内容事实

治理原则：

- 禁止在根仓直接改写子仓文档内容
- 页面权限和导航事实源必须由源仓 `docs/index.md` 声明
- 本地开发环境和生产环境必须分开管理

## 3. 平台运行拓扑

管理员需要记住的拓扑边界是：

- 宿主机 Nginx 提供静态站点与私有路径拦截
- Docker 内运行 `postgres`、`casdoor`、`oauth2-proxy`
- GitHub Actions 在 Runner 中构建站点，再把产物发到服务器

如果你要做首次安装，请直接读 [安装说明](installation.md)。  
如果你要做日常配置调整，请读 [配置说明](configuration.md)。

## 4. 管理员最常见的 3 条工作路径

### 4.1 首次安装平台

阅读顺序：

1. [安装说明](installation.md)
2. [配置说明](configuration.md)
3. [维护者指南](operator-guide.md)

### 4.2 接入一个新的私有源仓

阅读顺序：

1. [子仓库接入指南](usage.md)
2. [接入聚合站点](contributor-guide/onboarding.md)
3. [CLI 命令](contributor-guide/cli.md)

额外动作：

- 将该私有仓安装给 `docs-stratego-source-reader` GitHub App
- 用 remote 模式做一次真实构建验证
- 如需手工补跑共享指针同步，可执行 `uv run docs-stratego source sync-pointers --project-root /path/to/docs-stratego`

### 4.3 发布 CLI 给外部源仓使用

阅读顺序：

1. [CLI 分发与发布](contributor-guide/distribution.md)
2. [发布前外部配置](contributor-guide/publish-setup.md)
3. [CLI 发布手册](contributor-guide/release.md)

## 5. 关键凭证与配置归属

| 分类 | 典型项 | 用途 |
| --- | --- | --- |
| 部署权限 | `DOCS_DEPLOY_SSH_KEY` | 把构建产物上传到服务器 |
| 源码读取 | `DOCS_SOURCE_APP_ID`、`DOCS_SOURCE_APP_PRIVATE_KEY` | 让 GitHub Actions 读取私有源仓 |
| 联动凭证 | `DOCS_STRATEGO_SYNC_PAT` | 根仓维护共享 bot 分支和 PR |
| 子仓通知 | `DOCS_STRATEGO_DISPATCH_TOKEN` | 子仓向根仓发送 `repository_dispatch` |
| 认证运行配置 | `deploy/.env`、`oauth2-proxy.cfg`、`app.conf` | 控制 Casdoor、oauth2-proxy、数据库与 Redis |

## 6. 管理员最容易混淆的边界

### 6.1 `DOCS_STRATEGO_DISPATCH_TOKEN` 在哪里配

它配在源仓，不配在根仓。  
作用是“通知根仓”，不是“替根仓发布”。

### 6.2 GitHub App 和 PyPI Trusted Publisher 是不是同一种东西

不是：

- GitHub App 解决“读取私有源仓”
- Trusted Publisher 解决“发布 CLI 到 TestPyPI / PyPI”

### 6.3 本地预览失败时，管理员一定要先看服务器吗

不一定。  
很多问题先在本地 `docs-stratego dev` 就能复现，应优先区分是“本地构建问题”还是“服务器部署问题”。

## 7. 什么时候应该优先读哪一页

- 想搭服务器：读 [安装说明](installation.md)
- 想改配置：读 [配置说明](configuration.md)
- 想接入或移除源仓：读 [子仓库接入指南](usage.md)
- 想处理共享 PR 和发布后验证：读 [维护者指南](operator-guide.md)
- 想配置 CLI 发布外部依赖：读 [发布前外部配置](contributor-guide/publish-setup.md)

## 8. 管理员侧成功标准

如果平台治理是健康的，你应该能确认：

1. 源仓接入和移除都有标准命令与文档
2. 私有源仓读取和 CLI 发布分别有独立凭证体系
3. 服务器只承载运行时，不承担本地构建职责
4. 维护者能在不依赖管理员的情况下完成日常预览和审核
