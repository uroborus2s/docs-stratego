# 工作分解结构

## `CR-001` 子仓自动同步指针

### 交付物 1：需求与契约收口

- 完成 `REQ-009` 到 `REQ-013`、`NFR-006` 到 `NFR-008`
- 冻结事件名、bot 分支名、共享 PR 标题和凭证命名

### 交付物 2：根仓自动化重构

- 新增根仓 `sync-source-pointers` workflow
- 新增根仓 `validate-source-pointer-pr` workflow
- 调整 `Deploy Docs`，移除子仓自动同步入口，保留 `push` / `workflow_dispatch`

### 交付物 3：子仓接入模板

- 在 `docs-stratego` 内提供 `.github/workflows/notify-docs-stratego.yml` 的模板、字段说明和接入步骤
- 明确子仓与根仓各自需要的 Secret / Variable
- 约束子仓改动由各子仓接入方自行落地，不由根仓代改

### 交付物 4：文档与交接

- 更新使用指南，明确自动联动的接入动作和人工审核方式
- 更新管理员指南与配置说明，明确根仓与子仓的凭证边界
- 输出可重复执行的实施清单

### 交付物 5：验证与灰度

- 验证单仓触发、聚合 PR、人工合并和正式发布链路
- 验证多仓连续触发时共享 bot PR 的并发收口行为
