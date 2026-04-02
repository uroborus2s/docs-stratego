# 子仓库接入指南

本文是 `Contributor Guide` 的入口页，面向三类读者：

- 源仓文档作者：需要先把自己的 `docs/` 写到合规。
- 接入执行者：需要把源仓登记到 `docs-stratego` 根仓。
- 下线执行者：需要安全移除自动联动和根仓登记。

## 1. 先按角色选阅读路径

| 你现在要做什么 | 先读什么 | 再读什么 | 最后做什么 |
| --- | --- | --- | --- |
| 第一次接入一个新源仓 | [源文档标准](contributor-guide/source-docs-standard.md) | [接入聚合站点](contributor-guide/onboarding.md) | [自动联动](contributor-guide/automation.md) |
| 已接入源仓，想补齐自动同步 | [自动联动](contributor-guide/automation.md) | [CLI 命令](contributor-guide/cli.md) | [维护者指南](operator-guide.md) |
| 想批量执行接入、校验或移除 | [CLI 命令](contributor-guide/cli.md) | [接入聚合站点](contributor-guide/onboarding.md) | [移除流程](contributor-guide/offboarding.md) |
| 想下线一个源仓 | [移除流程](contributor-guide/offboarding.md) | [CLI 命令](contributor-guide/cli.md) | [管理员指南](admin-guide.md) |

## 2. 如果你只想快速完成接入

按这个顺序读最省脑力：

1. [源文档标准](contributor-guide/source-docs-standard.md)
2. [接入聚合站点](contributor-guide/onboarding.md)
3. [自动联动](contributor-guide/automation.md)
4. [CLI 命令](contributor-guide/cli.md)

## 3. 接入总览

一个完整接入流程有四步：

1. 在源仓把 `docs/` 改到合规，确保根 `docs/index.md` 是唯一导航和权限事实源。
2. 在源仓本地执行 `uv run docs-stratego source validate --repo-path /path/to/source-repo` 做结构校验。
3. 在 `docs-stratego` 根仓执行 `uv run docs-stratego source add ...` 完成配置登记，必要时同时注册 submodule。
4. 在源仓执行 `uv run docs-stratego source scaffold-notify --repo-path /path/to/source-repo` 生成自动通知 workflow。

## 4. 命令入口

本次接入相关的正式命令已经收口到 `docs-stratego` CLI：

- `uv run docs-stratego source validate`
- `uv run docs-stratego source add`
- `uv run docs-stratego source scaffold-notify`
- `uv run docs-stratego source remove`
- `uv run docs-stratego sync`
- `uv run docs-stratego build`

完整参数、样例和安全开关见 [CLI 命令](contributor-guide/cli.md)。

## 5. 本指南包含哪些页面

- [接入知识地图](contributor-guide/index.md)：帮助你判断每一页解决什么问题。
- [源文档标准](contributor-guide/source-docs-standard.md)：公开标准事实源。
- [接入聚合站点](contributor-guide/onboarding.md)：根仓登记与验证流程。
- [自动联动](contributor-guide/automation.md)：源仓通知根仓的 workflow 与 Secret。
- [移除流程](contributor-guide/offboarding.md)：暂停联动或完整下线的步骤。
- [CLI 命令](contributor-guide/cli.md)：所有接入/移除相关命令。
