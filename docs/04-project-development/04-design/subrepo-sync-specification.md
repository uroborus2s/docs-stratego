# 子仓自动同步接入规范

## 1. 概述

为了实现子仓文档变更后自动触发根仓 `docs-stratego` 的同步与发布，子仓需要按本规范自行集成一个轻量 workflow，在 `docs/**` 发生变更并推送到目标分支后，向根仓发送通知。

## 2. 接入步骤

### 2.1 配置凭证 (Secrets)

在子仓的 GitHub 仓库设置中 (`Settings -> Secrets and variables -> Actions`)，新增以下 Secret：

- `DOCS_STRATEGO_DISPATCH_TOKEN`：能够成功调用根仓 `repository_dispatch` 接口的 fine-grained PAT 或 GitHub App token。
  - 推荐使用最小权限 token。
  - 只用于向根仓发送同步事件，不用于发布站点。

### 2.2 添加工作流文件

在子仓根目录下创建 `.github/workflows/notify-docs-stratego.yml`。

这个文件由各子仓接入方自行提交到各自仓库；`docs-stratego` 根仓只负责提供规范和模板，不直接代改子仓代码。

### 2.3 模板内容

```yaml
name: Notify Docs Stratego

on:
  push:
    branches:
      - main
      - master
    paths:
      - 'docs/**'
  workflow_dispatch:

jobs:
  notify:
    runs-on: ubuntu-latest
    steps:
      - name: Send Repository Dispatch to docs-stratego
        run: |
          curl -L \
            -X POST \
            -H "Accept: application/vnd.github+json" \
            -H "Authorization: Bearer ${{ secrets.DOCS_STRATEGO_DISPATCH_TOKEN }}" \
            -H "X-GitHub-Api-Version: 2022-11-28" \
            https://api.github.com/repos/uroborus2s/docs-stratego/dispatches \
            -d '{"event_type":"source-pointer-sync-requested","client_payload":{"repository":"${{ github.repository }}","branch":"${{ github.ref_name }}","sha":"${{ github.sha }}"}}'
```

*如果根仓迁移到其他 owner/repo，请同步替换 dispatch URL。*

## 3. Secret 命名规范

| 命名 | 说明 | 作用 |
| --- | --- | --- |
| `DOCS_STRATEGO_DISPATCH_TOKEN` | 根仓 dispatch 调用令牌 | 用于调用 GitHub API 发送 `repository_dispatch` 事件。 |

## 4. 验收清单

- [ ] 子仓已正确配置 `DOCS_STRATEGO_DISPATCH_TOKEN`。
- [ ] 子仓已在主分支添加 `notify-docs-stratego.yml`。
- [ ] 修改子仓 `docs/` 下的任意文件并 push，观察子仓工作流是否成功触发。
- [ ] 检查根仓 `docs-stratego` 的 `Actions` 页面，确认是否触发了 `Sync Source Pointers` 工作流。
- [ ] 确认根仓是否生成了名为 `bot/sync-source-pointers` 的共享 PR。
