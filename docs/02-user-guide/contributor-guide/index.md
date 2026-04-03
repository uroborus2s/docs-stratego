# 子仓接入知识地图

这个目录是公开的接入知识层，目标不是解释内部架构，而是让接入方按最短路径完成事情。

如果你只记一件事，请记住：

- 第一次接入：先读标准，再做登记，再做 remote 构建验证
- 需要自动联动：在接入稳定后再开
- 需要发布 CLI：把外部配置和正式发版分开看

## 1. 每一页分别解决什么问题

| 页面 | 你在什么时候读它 | 读完应得到什么 |
| --- | --- | --- |
| [源文档标准](source-docs-standard.md) | 还没开始改源仓 `docs/` | 明确哪些目录、页面和契约写法是合规的 |
| [接入聚合站点](onboarding.md) | 源仓文档已经基本合规 | 知道如何把源仓登记到 `docs-stratego` |
| [自动联动](automation.md) | 想让 `docs/**` 变更自动触发根仓同步 | 知道 workflow、Secret 和验收口径 |
| [移除流程](offboarding.md) | 想暂停联动或彻底下线源仓 | 知道该删什么、保留什么 |
| [CLI 命令](cli.md) | 想把人工步骤变成可重复执行的命令 | 知道命令、参数和安全开关 |
| [CLI 分发与发布](distribution.md) | 想让外部源仓直接使用 CLI | 知道安装方式、发布路径和版本治理 |
| [发布前外部配置](publish-setup.md) | 准备首次把 CLI 发到 TestPyPI / PyPI | 知道 GitHub 环境、Trusted Publisher 和手动演练如何配置 |
| [CLI 发布手册](release.md) | 你已经决定发新版本 | 知道怎么 bump 版本、打 tag、发布和验证 |

## 2. 推荐阅读顺序

### 第一次接入

1. `source-docs-standard.md`
2. `onboarding.md`
3. `cli.md`
4. `automation.md`
5. `distribution.md`
6. `publish-setup.md`
7. `release.md`

### 已接入后的日常维护

1. `cli.md`
2. `automation.md`
3. [维护者指南](../operator-guide.md)

### 下线或迁移

1. `offboarding.md`
2. `cli.md`
3. [管理员指南](../admin-guide.md)

## 3. 公开层与内部层的边界

你在这个目录里看到的是公开事实源，适合给源仓接入方直接照着做。

内部设计层只保留两类内容：

- 为什么平台要这样设计
- 构建器、workflow 和权限生成逻辑怎样消费这些公开事实

如果你的目标是“把仓接进来”或“把仓移出去”，优先读这个目录，不需要先翻内部设计文档。
