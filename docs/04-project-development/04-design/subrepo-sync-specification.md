# 子仓自动同步公开化设计

## 1. 公开事实源

子仓自动同步的公开接入说明已经放到：

- [自动联动](../../02-user-guide/contributor-guide/automation.md)
- [CLI 命令](../../02-user-guide/contributor-guide/cli.md)

## 2. 内部设计层保留的内容

内部层只记录这些固定约束：

- 根仓事件名：`source-pointer-sync-requested`
- 根仓共享 bot 分支：`bot/sync-source-pointers`
- 根仓共享 PR 标题：`chore: sync source repository pointers`
- 源仓 workflow 文件名：`.github/workflows/notify-docs-stratego.yml`

## 3. 为什么要公开化

- 自动联动是接入方直接要执行的动作，不应该藏在内部设计文档里。
- 生成 workflow 的 CLI 命令已经成为公开能力，文档应与命令入口保持同层。
- 内部设计文档继续作为“实现边界”和“固定常量”的审计记录即可。
