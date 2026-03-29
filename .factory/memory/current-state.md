# 当前状态

- 当前模式：cli_direct
- 当前阶段：IMPLEMENTATION
- 活跃任务：1
- 活跃变更：1
- 活跃缺陷：0
- 活跃 PR：0

- 角色目录总数：9
- 当前阶段主要角色：项目协调者、解决方案架构师、文档与记忆管理员

- 当前技术画像：自定义技术画像
- 技术画像预设：custom
- 关键工程规则数：5
- 设计交付物数：4

## 最近条目

- 任务：迁移 `docs/` 到四大模块结构并拉齐 docs-stratego 索引
- 变更：完成旧生命周期目录到四大模块骨架的迁移，并按 `docs_profile` 启用 `01-getting-started`、`02-user-guide`、`04-project-development`
- 缺陷：无

## 最新集成

- 当前文档标准由 `docs/04-project-development/04-design/source-docs-standard.md` 定义
- 当前 `docs/index.md` 已按 `docs_profile` 刷新根导航，各级目录 `index.md` 已刷新为正文概览页
- 当前未单独启用 `03-developer-guide`；稳定对外扩展能力仍由用户指南与内部设计文档承载
- 当前构建链路为 `sync_sources.py` -> `build_site.py` -> `mkdocs build`
- 已新增 `.generated/authz/permissions.json` 与 `.generated/nginx/private_locations.conf`
- 认证部署栈为宿主机 Nginx + Docker 内 Casdoor/oauth2-proxy + 现有 Redis
- MkDocs 已切换为单站点构建，并默认关闭匿名全文搜索
- 顶部项目 Tab 已支持点击下拉，内容来自各项目根 `docs/index.md` 的一级目录，尾项固定为 GitHub 仓库链接
- 左侧主导航已收口为当前一级模块的目录列表，不再附加“项目入口”，模块首页不再显示通用“概览”文案
- `02-user-guide/` 已补齐云服务器私有化部署、配置、使用与管理员内容
- 已新增 `02-user-guide/cloud-server-cicd-playbook.md`，覆盖双域名、GitHub App、Certbot、Nginx HTTPS、GitHub Actions Secrets 与首发验证步骤
- GitHub Actions 发布口径已更新为“Runner 构建 + 上传 `site/`、`private_locations.conf`”，不再把服务器侧 `git pull + build` 作为日常主路径
- GitHub Actions 现已补齐 `validate -> deploy` 两阶段，先做依赖安装、单元测试和 MkDocs 构建，再上传制品并按需 reload 宿主机 Nginx；`site/` 与 `private_locations.conf` 会作为 artifact 保留 7 天
- 宿主机 Nginx 现改为运维手工安装 `sites-available/sites-enabled` 域名文件；发布侧只依赖 `/etc/nginx/snippets/docs-stratego/private_locations.conf` 和可选 reload
- 宿主机 Nginx 模板已拆为 `docs/auth` 两组 HTTP 引导版与正式 HTTPS 版，便于按域名单独维护
- Redis 接入策略已收口为“保持现有业务网络不动，由 oauth2-proxy 同时加入内部网络与 Redis 现有网络”
- 服务器侧认证应用目录改为稀疏拉取的 `~/docs-stratego`，只保留 `deploy/docker-compose.yml`、`deploy/casdoor/`、`deploy/oauth2-proxy/`
- 服务器侧静态站点目录改为 `/var/www/docs-stratego`，私有规则文件改为 `/etc/nginx/snippets/docs-stratego/private_locations.conf`
- 当前正式 `config/source-repos.json` 已登记 `docs-stratego`、`crawler4j`、`stratix` 三个项目
- 当前源仓配置已升级为单文件双模式：同一 `config/source-repos.json` 同时声明 `modes.local` 与 `modes.remote`
- 本地调试默认使用 `source_mode=local` 直接读取本机文档目录，服务器发布与 GitHub Actions 默认使用 `source_mode=remote`
- `start.sh`、`sync_sources.py`、`build_site.py`、`deploy_remote.sh` 与 GitHub Actions 已统一接入 `--source-mode`

## 下一步建议

- 用真实外部仓库验证 `git submodule update --init` + 子仓内 `fetch + checkout` + `sparse-checkout` 只展开顶层 `docs/`
- 当前本地模式构建已通过；远程模式仍被 `crawler4j` 远端分支中的未声明页面阻塞
- 在部署环境中完成 Casdoor GitHub Provider 配置
- 等 `crawler4j` 和 `stratix` 远程分支修正根清单与权限值后，再重新并入正式生产配置
- 在新接入源仓时，同时验证 `local` 与 `remote` 两种模式都能完成 `sync_sources -> build_site -> mkdocs build`
- 若工作项进入收尾，确认根仓文档与 `.factory/memory/` 已同步更新
