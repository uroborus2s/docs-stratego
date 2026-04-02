# 任务分解文档

## 变更项

- `CR-001`：子仓 `docs/**` 变更自动同步到根仓共享 bot PR
- `CR-002`：重构接入文档，公开化标准并按角色阅读路径重组
- `CR-003`：新增源仓接入/移除辅助 CLI

## 任务清单

| ID | 类型 | 内容 | 负责人 | 估算（人天） | 依赖 | 产出 |
| --- | --- | --- | --- | --- | --- | --- |
| TASK-001 | 重构 | 拆分根仓“同步子仓指针”和“正式发布站点”的 workflow 边界，新增 `sync-source-pointers.yml` 并调整 `deploy-docs.yml` 触发条件。 | 项目协调者 / 后端工程师 | 1.0 | 无 | 根仓 workflow 骨架与触发规则 |
| TASK-002 | 功能 | 为根仓实现共享 bot 分支与共享 PR 复用逻辑，支持把所有已落后的 `sources/*` gitlink 汇总到一个 PR。 | 后端工程师 | 1.0 | `TASK-001` | `bot/sync-source-pointers` 分支与 PR 自动化 |
| TASK-003 | 功能 | 新增 `validate-source-pointer-pr.yml`，把单元测试、`sync_sources.py --source-mode remote`、`build_site.py` 和 `mkdocs build` 收口为 merge gate。 | 后端工程师 / QA 工程师 | 0.5 | `TASK-001` | 指针同步 PR 校验链路 |
| TASK-004 | 接入规范 | 在本仓库沉淀子仓自动通知接入规范、`notify-docs-stratego.yml` 模板、Secret 命名和验收清单，明确由各子仓接入方自行在子仓落地，不由 `docs-stratego` 直接改子仓代码。 | 项目协调者 / 文档与记忆管理员 | 1.0 | `TASK-001` | 接入规范、模板与验收清单 |
| TASK-005 | 文档 | 更新 `usage.md`、`admin-guide.md`、`configuration.md`，明确子仓新增文件、凭证边界、人工审核动作与手动回退口径。 | 文档与记忆管理员 | 0.5 | 无 | 用户与管理员文档 |
| TASK-006 | 回归 | 选择至少一个已接入子仓做端到端演练：子仓 push -> 根仓共享 PR -> 人工合并 -> `Deploy Docs` 发布。 | QA 工程师 / 项目协调者 | 0.5 | `TASK-002`、`TASK-003`、`TASK-004`、`TASK-005` | 回归记录与上线前证据 |
| TASK-007 | 文档重构 | 把公开标准、接入、联动、移除与 CLI 命令重构为 `Contributor Guide` 的清晰分层结构。 | 文档与记忆管理员 | 1.0 | `TASK-005` | 公开接入文档集 |
| TASK-008 | CLI | 新增 `docs-stratego` CLI，收口 `source validate/add/remove/scaffold-notify` 与 `sync/build` 入口。 | 后端工程师 | 1.5 | 无 | CLI 入口、配置操作与通知脚手架 |
| TASK-009 | 回归 | 补齐 CLI 单元测试与文档导航回归，并把新测试并入 CI。 | QA 工程师 / 后端工程师 | 0.5 | `TASK-007`、`TASK-008` | 测试与 CI 同步 |

## 实施顺序

1. 先完成 `TASK-001`，冻结事件名、分支名和权限边界。
2. 再完成 `TASK-002` 与 `TASK-003`，保证根仓能先形成可审核的共享 PR。
3. 然后执行 `TASK-004` 与 `TASK-005`，把接入规范、模板和文档入口补齐。
4. 并行完成 `TASK-007` 与 `TASK-008`，把公开文档和 CLI 一起收口。
5. 最后执行 `TASK-006` 与 `TASK-009`，补齐真实链路和自动回归证据。
