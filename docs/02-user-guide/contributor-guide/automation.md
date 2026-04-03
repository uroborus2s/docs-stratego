# 自动联动

这页回答的是：如何让源仓在 `docs/**` 发生变更后，自动通知 `docs-stratego` 根仓发起“同步指针 -> 共享 PR -> 人工审核”的流程。

## 1. 你什么时候需要它

如果你只做一次性接入，先完成 [接入聚合站点](onboarding.md) 就够了。

只有在下面场景，才建议开启自动联动：

- 该源仓会持续更新文档
- 团队希望文档更新后自动推送到根仓审核入口
- 你已经能稳定通过远程构建验证

前提：

- 下面的源仓侧命令默认假设 CLI 已经作为包发布，可由源仓直接调用。
- 如果还没发布，请先看 [CLI 分发与发布](distribution.md)。

## 2. 需要准备的 Secret

在源仓 GitHub 仓库的 `Settings -> Secrets and variables -> Actions` 中新增：

- `DOCS_STRATEGO_DISPATCH_TOKEN`

它只负责调用根仓的 `repository_dispatch`，不负责部署站点。

## 3. 用 CLI 生成 workflow

在源仓本地执行：

```bash
uvx --from 'docs-stratego==<version>' docs-stratego source scaffold-notify \
  --repo-path /path/to/source-repo \
  --branch main
```

如果你的触发分支不止一个，可以重复传入：

```bash
--branch main --branch release
```

默认会生成：

- `.github/workflows/notify-docs-stratego.yml`

默认根仓目标是：

- `uroborus2s/docs-stratego`

如果你要先看结果但不落盘，追加：

```bash
--dry-run
```

## 4. 生成后的 workflow 会做什么

生成的 workflow 固定遵守这几个边界：

- 只监听指定分支的 `docs/**` 变更
- 事件名固定为 `source-pointer-sync-requested`
- 只调用根仓 dispatch，不直接发布站点
- 根仓最终仍由人工审核共享 PR

## 5. 如何移除自动联动

如果你只想停掉自动通知，但暂时不想从根仓下线该源仓，执行：

```bash
uvx --from 'docs-stratego==<version>' docs-stratego source scaffold-notify \
  --repo-path /path/to/source-repo \
  --remove
```

这只会删除源仓里的通知 workflow，不会改根仓登记。

## 6. 验收清单

- [ ] `DOCS_STRATEGO_DISPATCH_TOKEN` 已配置
- [ ] `.github/workflows/notify-docs-stratego.yml` 已提交到源仓
- [ ] 在目标分支修改 `docs/**` 后，源仓 workflow 会触发
- [ ] 根仓收到 `source-pointer-sync-requested`
- [ ] 根仓形成或复用 `bot/sync-source-pointers` 共享 PR
