# 项目索引

- 项目名称：章略·墨衡
- 当前模式：cli_direct
- 当前阶段：IMPLEMENTATION
- 项目负责人：uroborus
- 技术栈：MkDocs Material + Python/uv + git submodule + sparse-checkout + Casdoor + oauth2-proxy + Nginx + Gemini CLI/Codex
- 当前技术画像：自定义技术画像
- 设计交付物数：0
- 当前阶段主要角色：项目协调者、解决方案架构师、UX/UI 设计师、文档与记忆管理员

## 项目创意摘要

建设一个集中维护公司多个项目文档集合与知识库的静态文档工程。根仓 docs-stratego 只稀疏同步各源仓 `docs/`，根据根 `docs/index.md` 的全站清单生成导航与权限清单，构建单个 MkDocs 站点，并通过 Casdoor、oauth2-proxy 与 Nginx 实现页面级登录保护。

## 项目概况

- 任务数：6
- 变更数：1
- 缺陷数：0
- 活跃 PR 数：0
- 已合并 PR 数：0
- AI 入口：`/.factory/memory/runtime-brief.md`、`/.factory/memory/role-charter.project.md`、`/.factory/memory/current-state.md`、`/.factory/memory/doc-map.md`

## 已接入文档源

- `platform`：`/Users/uroborus/AiProject/docs-stratego/docs`
- 外部源仓按 `config/source-repos.json` 声明后，通过 Git submodule + sparse-checkout 接入 `sources/<repo>/docs`
- 当前外部源仓：`crawler4j`、`stratix`、`ride-loop`、`shanforge`、`ctrip_crawler`、`sinan-captcha`

## 当前站点能力

- 左侧导航按根 `docs/index.md` 的全站清单自动生成
- 页面点击后按 URL 路径触发登录
- 私有页面和资源在构建期生成权限清单与 Nginx 规则
- GitHub Push 后经 SSH 触发的服务器本地自动部署
- 部署前自动更新外部源仓的 `docs/`
- 完整部署手册与源仓接入标准

## 当前批准中的增量变更

- `CR-001`：子仓 `docs/**` 变更自动通知根仓，形成共享 bot PR，经人工审核合并后再发布
