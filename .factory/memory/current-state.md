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
- 缺陷：修复“公开首页被误认为整站锁定、私有文档缺少站内按需登录交互”的部署与体验问题
- 变更：已批准 `CR-001`，将新增“子仓 `docs/**` 变更自动通知根仓共享 bot PR”的需求、任务与文档口径
- 变更：已批准 `CR-002` / `CR-003`，将公开重构 `Contributor Guide`，并提供源仓接入/移除辅助 CLI
- 变更：已修复 `CR-001` 根仓实现中的事件名、凭证与脚本解析问题，根仓侧自动同步能力已具备
- 变更：已按 CLI-first 收敛项目入口，删除旧 Python 包装脚本，并把 workflow、启动脚本和公开文档统一切到 `docs-stratego` CLI
- 变更：已将源码从 `src/docs_stratego/` 平铺迁移到 `src/`，取消额外包层，打包入口改为顶层模块
- 变更：已补齐“本地开发与预览”“发布前外部配置”和 GitHub Actions 工作流报告，用户指南阅读路径已重新按任务和角色收口
- 变更：`docs-stratego dev` 已支持 `source_mode=local` 的 watch 模式，可在本地源文档变更后自动重新执行 `sync -> build`
- 变更：已重构 `02-user-guide/` 的信息架构与高频操作页，补齐阅读者、本地开发、接入、联动、审核、安装等示意截图，并新增用户指南可读性评审
- 变更：已将 `mkdocs` / `mkdocs-material` 从 CLI 核心依赖拆分为 `site` extra；根仓本地开发与站点构建 workflow 现显式使用 `uv sync --extra site`，外部源仓默认保持轻量安装
- 缺陷：已修复用户指南旧文件名残留导致的 `configuration.md -> usage.md` 文档编译告警
- 验证：已完成当前 CLI-first + watch 模式本地回归，`tests.test_source_sync`、`tests.test_site_builder`、`tests.test_deploy_stack`、`tests.test_sync_source_pointers`、`tests.test_source_admin`、`tests.test_cli` 共 `40` 个测试通过，`docs-stratego build` 与 `mkdocs build` 通过；真实 GitHub 端到端演练仍待执行

## 最新集成

- 当前公开源文档标准由 `docs/02-user-guide/contributor-guide/source-docs-standard.md` 定义
- 当前接入公开事实源已迁移到 `docs/02-user-guide/contributor-guide/`，按“标准 -> 接入 -> 联动 -> 移除 -> CLI”组织
- 公开接入指南已进一步收紧 CLI 边界：根仓内继续使用 `uv run docs-stratego`，外部源仓改为“已发布包 + `uvx/uv tool install`”口径，并新增 `CLI 分发与发布` 页面
- 仓库已新增 `publish-cli.yml`：普通 `push` 不发包，只有 `cli-v*.*.*` tag 或手动演练才触发 `TestPyPI -> smoke test -> PyPI` 发布链路
- `Contributor Guide` 已补齐 `CLI 发布手册` 页面，明确版本更新、tag 规则、发布步骤、失败处理和对外升级口径
- 当前源文档标准已扩展为“Markdown 页面 + OpenAPI 契约 + MCP tools 快照”三类可声明内容；根 `docs/index.md` 的页面节点现在允许指向 `*.openapi.*` 与 `*.mcp-tools.*`
- 页面权限当前只认根 `docs/index.md` 页面节点的 `access`；`external/`、`internal/` 只作为目录组织语义，不参与权限判断
- 当前 `docs/index.md` 已按 `docs_profile` 刷新根导航，各级目录 `index.md` 已刷新为正文概览页
- 当前未单独启用 `03-developer-guide`；稳定对外扩展能力仍由用户指南与内部设计文档承载
- 当前构建链路为 `docs-stratego sync` -> `docs-stratego build` -> `mkdocs build`
- 仓库已新增正式 CLI 入口 `uv run docs-stratego`，公开暴露 `dev`、`source validate/add/remove/scaffold-notify/sync-pointers` 与 `sync/build`
- 根仓开发环境现推荐使用 `uv sync --extra site && uv run docs-stratego dev --project-root .`；外部源仓默认只安装轻量 CLI，只有需要站点预览能力时才使用 `docs-stratego[site]`
- 当前源码平铺位于 `src/cli.py`、`src/site_builder.py`、`src/source_admin.py`、`src/source_config.py`、`src/source_pointer_sync.py`、`src/source_sync.py`、`src/models.py`
- 已新增 `.generated/authz/permissions.json` 与 `.generated/nginx/private_locations.conf`
- 认证部署栈为宿主机 Nginx + Docker 内 Casdoor/oauth2-proxy + 现有 Redis
- MkDocs 已切换为单站点构建，并默认关闭匿名全文搜索
- 顶部项目 Tab 现保留 Material 原始 `<a class="md-tabs__link">` 结构与样式，只移除导航行为并改为菜单触发器；首次点击直接弹出下拉菜单，菜单首项固定为“简介”，其余内容来自各项目根 `docs/index.md` 的一级目录，尾项固定为 GitHub 仓库链接
- 左侧主导航已收口为当前一级模块的目录列表，不再附加“项目入口”，模块首页不再显示通用“概览”文案
- `02-user-guide/` 已补齐云服务器私有化部署、配置、使用与管理员内容
- `02-user-guide/installation.md` 已收口为完整安装与 CI/CD 正式事实源，原先重复的 playbook 页面已删除
- GitHub Actions 发布口径已更新为“Runner 构建 + 上传 `site/`、`private_locations.conf`”，不再把服务器侧 `git pull + build` 作为日常主路径
- GitHub Actions 现已补齐 `validate -> deploy` 两阶段，先做依赖安装、单元测试和 MkDocs 构建，再上传制品并按需 reload 宿主机 Nginx；`site/` 与 `private_locations.conf` 会作为 artifact 保留 7 天
- 宿主机 Nginx 现改为运维手工安装 `sites-available/sites-enabled` 域名文件；发布侧只依赖 `/etc/nginx/snippets/docs-stratego/private_locations.conf` 和可选 reload
- 仓库已移除 `deploy/nginx/` 与 `render_host_nginx_conf.sh`；宿主机 Nginx 配置仅保留文档示例，由运维按安装文档手工维护
- Redis 接入策略已收口为“保持现有业务网络不动，由 oauth2-proxy 同时加入内部网络与 Redis 现有网络”
- 服务器侧认证应用目录改为稀疏拉取的 `~/docs-stratego`，只保留 `deploy/docker-compose.yml`、`deploy/casdoor/`、`deploy/oauth2-proxy/`
- 服务器侧静态站点目录改为 `/var/www/docs-stratego`，私有规则文件改为 `/etc/nginx/snippets/docs-stratego/private_locations.conf`
- 当前正式 `config/source-repos.json` 已登记 `docs-stratego`、`crawler4j`、`stratix`、`ride-loop`、`shanforge`、`ctrip_crawler` 六个项目；local 模式直接读本机工作副本，remote 模式在 GitHub Actions 中真实拉取并校验这些源仓
- 当前源仓配置已升级为单文件双模式：同一 `config/source-repos.json` 同时声明 `modes.local` 与 `modes.remote`
- 旧的平铺源仓配置兼容逻辑已删除；仓库定义如果缺少 `modes` 会直接报错，不再接受旧格式
- 本地调试默认使用 `source_mode=local` 直接读取本机文档目录；本地生产预演与 GitHub Actions 正式发布都使用 `source_mode=remote`
- 开发环境已移除 `start.sh`，统一改为 `docs-stratego dev`；`deploy_remote.sh` 与 GitHub Actions 继续使用 `docs-stratego` CLI 和 `--source-mode`
- `ride-loop` 已作为新文档源接入，本地模式指向 `/Users/uroborus/NodeProject/ride-loop/docs`，远程模式指向 `https://github.com/uroborus2s/ride-loop.git@main`
- `ride-loop` 现已在根仓索引中登记为真实 git submodule；`git submodule sync/update` 不再因 pathspec 缺失而失败
- `shanforge` 已作为新文档源接入，本地模式指向 `/Users/uroborus/AiProject/shanforge/docs`，远程模式指向 `https://github.com/uroborus2s/shanforge.git@main`
- `ctrip_crawler` 已作为新文档源接入，本地模式指向 `/Users/uroborus/PythonProject/ctrip_crawler/docs`，远程模式指向 `https://github.com/uroborus2s/ctrip_crawler.git@main`
- `ctrip_crawler` 本地工作副本已补齐根 `docs/index.md` 对 `requirements-analysis.md`、`requirements-verification.md`、`backend-design.md`、`database-design.md`、`ux-ui-design.md`、`implementation-plan.md`、`task-breakdown.md`、`wbs.md`、`requirements-matrix.md` 的 `mkdocs.nav` 声明；`source_mode=local` 构建已恢复
- GitHub Actions 已收口为 GitHub App 唯一正式私有源仓读取方案，并已升级为 `actions/create-github-app-token@v3`
- `docs/02-user-guide/installation.md` 已成为唯一部署事实源；原 `cloud-server-cicd-playbook.md` 已删除，README 与运维文档入口已同步切换
- `docs/02-user-guide/` 已补齐本地 `local/remote` 两种构建入口、`docs-stratego dev --build-only` 用法，以及“子仓文档变更后如何重新触发根仓发布”的说明
- `docs/02-user-guide/local-development.md` 已明确 `docs-stratego dev` 在 `source_mode=local` 下支持 watch 自动重建，在 `source_mode=remote` 下仍需手工重跑
- `docs/02-user-guide/contributor-guide/publish-setup.md` 已补齐 GitHub 环境、TestPyPI、PyPI Trusted Publisher 的首次配置步骤和示意截图
- `docs/02-user-guide/` 现已按“阅读与访问 / 开发与接入 / 运维与发布 / 平台管理”重组导航，关键操作页已补齐成功标志、常见误区和 SVG 操作示意截图
- `docs/04-project-development/08-operations-maintenance/user-guide-readability-review.md` 已记录从阅读者视角出发的可读性评审结论：当前未发现阻断性的知识盲点
- `docs/04-project-development/08-operations-maintenance/github-actions-workflow-report.md` 已记录 4 个 GitHub Actions workflow 的触发条件、凭证依赖、产物流转和风险边界
- GitHub Actions 现显式将 MkDocs 制品输出到 `$GITHUB_WORKSPACE/site`，避免 `.generated/site` 与 deploy 打包路径不一致导致的空制品问题
- 站点静态资源现新增 `access-control.js` 与同源桥接页 `assets/auth/popup-complete.html`：公开与私有页面共用同一套导航且不额外显示锁定标记，匿名用户点击私有页面时同步拉起独立登录小窗；登录成功后由桥接页通过 `postMessage` 通知主页面并自动关闭小窗，关闭小窗则继续浏览公开文档
- 主页面现在会在重新获得焦点或接收到新的页面点击时主动关闭仍未完成的登录小窗，避免小窗仅退到后台
- 私有链接前端鉴权现已增加短时登录态缓存与 `navigation.instant` 站内导航：已登录用户再次点击私有页面时优先走原生即时导航，减少额外整页刷新与白屏闪烁
- `site_builder.py` 现可识别并渲染已在根导航声明的 OpenAPI 与 MCP tools 契约文件：`*.openapi.yaml|yml|json` 自动生成 Scalar API Reference 包装页，`*.mcp-tools.yaml|yml|json` 自动生成 MCP tools 静态参考页，同时保留原始契约文件下载地址并沿用同一套权限控制
- `docs/04-project-development/04-design/openapi/` 与 `docs/04-project-development/04-design/tools/` 已作为当前仓库的规范示例目录接入根导航，用于验证契约渲染能力
- 生成的 `private_locations.conf` 现显式标注“只允许私有 URL 进入鉴权”，用于约束宿主机 Nginx 不要把 `location /` 误配成整站登录
- 用户指南、安装说明、运维手册与 UX 设计文档已同步更新，新增“首页不得直接跳登录”的排障口径
- GitHub Actions deploy 远端 reload 步骤已去掉基于 `EUID` 的分支判断，改为固定走 `sudo nginx -t` 与 `sudo systemctl reload nginx`，避免 `appleboy/ssh-action` 将条件判断的非零退出码误判为部署失败

## 下一步建议

- 用真实外部仓库验证 `git submodule update --init` + 子仓内 `fetch + checkout` + `sparse-checkout` 只展开顶层 `docs/`
- 当前本地模式构建已通过；远程模式仍被 `crawler4j` 远端分支中的未声明页面阻塞
- 在部署环境中完成 Casdoor GitHub Provider 配置
- 选择一个已接入子仓，在真实 GitHub 环境执行一次 `repository_dispatch -> Sync Source Pointers -> 共享 PR -> Squash and merge -> Deploy Docs` 演练
- 若 `crawler4j` 和 `stratix` 继续保留在正式 `source-repos.json` 中，GitHub Actions remote 构建会持续按生产标准校验它们
- `shanforge` 接入后，也要同步验证本地 `../shanforge/docs` 与远程 `sources/shanforge/docs` 两条链路都能完成 `docs-stratego sync -> docs-stratego build -> mkdocs build`
- `ctrip_crawler` 接入后，也要同步验证本地 `../../PythonProject/ctrip_crawler/docs` 与远程 `sources/ctrip_crawler/docs` 两条链路都能完成 `docs-stratego sync -> docs-stratego build -> mkdocs build`
- 将 `ctrip_crawler` 当前本地工作副本里的 `docs/index.md` 导航补丁提交并推送到 `main`，再重新跑一次 `source_mode=remote` 构建与 CI
- 在新接入源仓时，同时验证 `local` 与 `remote` 两种模式都能完成 `docs-stratego sync -> docs-stratego build -> mkdocs build`
- 若工作项进入收尾，确认根仓文档与 `.factory/memory/` 已同步更新
- 在外部源仓接入 OpenAPI 或函数契约时，除更新目录说明页外，还要把契约文件本身显式加入根 `docs/index.md`，否则不会自动生成参考页
