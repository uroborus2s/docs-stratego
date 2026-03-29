# 执行日志

## 2026-03-25

- 使用最新版 `factory-init` 初始化 `docs-stratego`
- 修复初始化器误生成旧版 D3 目录的问题
- 清理项目中的旧目录残留
- 将原始方案重写为最新文档结构下的治理、需求、方案、部署和交接文档
- 2026-03-25: 刷新项目规则文件 `AGENTS.md` / `GEMINI.md`，负责人：Codex，备注：迁移到单隐藏目录架构。

## 2026-03-26

- 完成新方案头脑风暴，确认放弃双站点和中间聚合目录
- 收口为“单站点 + 页面级登录 + 源仓自维护权限”架构
- 明确外部源仓通过 Git submodule + sparse-checkout 同步 `docs/`

## 2026-03-27

- 新增 `src/docs_stratego/source_sync.py`，通过 sparse-checkout 只同步源仓 `docs/`
- 新增 `src/docs_stratego/site_builder.py`，从根 `docs/index.md` 全站清单生成导航、权限清单和 Nginx 私有规则
- 重写 README、治理、需求、方案、运维、交接与 `.factory` 记忆，统一到单站点页面级鉴权方案
- 新增 Casdoor、oauth2-proxy、Nginx Docker 部署骨架
- 默认关闭 MkDocs 匿名全文搜索，避免私有内容进入公开搜索索引
- 2026-03-28: 完成 docs 结构重构迁移，负责人：Codex。
- 2026-03-28: 刷新 docs-stratego 目录索引，负责人：Codex。
- 2026-03-28: 刷新 docs-stratego 目录索引，负责人：Codex。
- 2026-03-28: 刷新 docs-stratego 目录索引，负责人：Codex。
