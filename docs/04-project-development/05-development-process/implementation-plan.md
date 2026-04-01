# 实施计划

## 范围

- 本轮实施仅覆盖 `CR-001`：子仓自动通知、根仓共享 bot PR、人工审核合并、再触发正式发布。
- 不改变根仓“只聚合 `docs/`、站点仍由 `Deploy Docs` 发布”的核心边界。

## 阶段 1：根仓 workflow 解耦

1. 新增 `sync-source-pointers.yml`
2. 新增 `validate-source-pointer-pr.yml`
3. 调整 `deploy-docs.yml`，移除自动同步事件入口

退出标准：

- 子仓通知只会更新共享 bot PR，不会直接触发线上发布
- 根仓仍可通过 `push main` 和 `workflow_dispatch` 正常发布

## 阶段 2：共享 bot PR 自动化

1. 固定事件名 `source-pointer-sync-requested`
2. 固定 bot 分支 `bot/sync-source-pointers`
3. 固定共享 PR 标题 `chore: sync source repository pointers`
4. 只在 `sources/*` gitlink 发生变化时提交和更新 PR

退出标准：

- 连续两次触发时，根仓只保留一个未合并 PR
- 多个子仓落后时，同一个 PR 中能汇总全部指针更新

## 阶段 3：子仓接入与文档同步

1. 在根仓文档中提供 `.github/workflows/notify-docs-stratego.yml` 模板、事件字段、Secret 命名和接入步骤
2. 为根仓配置 bot push/PR Secret，并明确子仓需要自行配置的 dispatch Secret
3. 更新用户与管理员文档，明确“根仓给规范，子仓自行落地”的边界和审核动作

退出标准：

- 新接入子仓时，有固定文件和 Secret 清单可照单执行
- 文档能明确回答“子仓需要加什么文件、根仓需要加什么 Secret”，且不会把子仓代码改动误记为根仓自身实施内容

## 阶段 4：回归与发布演练

1. 选一个已接入子仓做 `docs/**` push 演练
2. 检查根仓共享 bot PR diff、checks 和人工合并动作
3. 合并后验证 `Deploy Docs` 发布链路

退出标准：

- 共享 bot PR checks 全绿
- 人工 `Squash and merge` 后，`main` 触发正式发布
- 发布后站点内容与被合并的子仓指针一致
