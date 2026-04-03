# 源文档标准公开化设计

## 1. 决策

源文档标准的正式公开事实源已经迁移到 `Contributor Guide`：

- [子仓库接入指南](../../02-user-guide/usage.md)
- [源文档标准](../../02-user-guide/contributor-guide/source-docs-standard.md)
- [接入聚合站点](../../02-user-guide/contributor-guide/onboarding.md)
- [自动联动](../../02-user-guide/contributor-guide/automation.md)
- [移除流程](../../02-user-guide/contributor-guide/offboarding.md)
- [CLI 命令](../../02-user-guide/contributor-guide/cli.md)

## 2. 为什么要从内部设计层迁到公开层

- 接入方真正需要的是“怎么做”，不是先理解内部实现细节。
- 旧结构下，公开页 `usage.md` 和私有页 `source-docs-standard.md` 重复解释同一事实，维护成本高。
- 接入动作、移除动作和 CLI 命令属于公开协作面，应当和用户指南放在同一阅读路径里。

## 3. 内部设计层保留什么

内部设计层现在只保留下面这些内容：

- 公开事实源与内部模块的对应关系
- 构建器如何消费这些事实
- 为什么采用“公开规范 + 内部实现”的分层方式

## 4. 实现绑定点

当前实现由以下模块消费公开标准：

- `src/site_builder.py`
  - 解析根 `docs/index.md`
  - 校验 `mkdocs.nav`、页面权限和契约文件
  - 生成导航、权限清单和契约渲染页
- `src/source_admin.py`
  - 提供 `source validate` 命令
  - 复用与构建器一致的解析规则校验源仓

## 5. 设计约束

- 公开事实源只保留一份，不再在内部设计文档中复制完整规范正文。
- 公开层按读者任务组织：标准、接入、联动、移除、CLI。
- 内部层按系统设计组织：构建器、同步器、workflow、权限与部署。
