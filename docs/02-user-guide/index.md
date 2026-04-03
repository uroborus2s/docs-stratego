# 用户指南

这套用户指南不是“从头到尾顺读”的手册，而是一套按任务组织的执行入口。

如果你只想知道一件事，请先回答这两个问题：

1. 你现在扮演的是谁。
2. 你眼前要完成的动作是什么。

## 1. 先按任务找入口

| 你现在要做什么 | 直接读哪一页 | 读完后应该得到什么 |
| --- | --- | --- |
| 正常阅读聚合站点 | [阅读者指南](reader-guide.md) | 知道公开页、私有页、登录小窗和常见异常的处理方式 |
| 在本机启动开发预览 | [本地开发与预览](local-development.md) | 知道 `docs-stratego dev` 怎么启动、什么时候会自动重建、什么时候要重启 |
| 接入、联动或移除一个源仓 | [子仓库接入指南](usage.md) | 知道完整接入闭环、命令边界和下线流程 |
| 审核共享 PR、跟进发布结果 | [维护者指南](operator-guide.md) | 知道日常预览、同步 PR 审核、发布后验证和排障顺序 |
| 搭服务器、管 GitHub、管 PyPI 发布 | [管理员指南](admin-guide.md) | 知道安装、配置、凭证边界、发布外部配置和维护职责 |

## 2. 再按角色选最短阅读路径

### 阅读站点的人

1. [阅读者指南](reader-guide.md)

### 源仓接入执行者

1. [子仓库接入指南](usage.md)
2. [源文档标准](contributor-guide/source-docs-standard.md)
3. [接入聚合站点](contributor-guide/onboarding.md)
4. [自动联动](contributor-guide/automation.md)
5. [CLI 命令](contributor-guide/cli.md)

### 根仓维护者

1. [本地开发与预览](local-development.md)
2. [维护者指南](operator-guide.md)
3. [子仓库接入指南](usage.md)

### 管理员 / 发布执行者

1. [安装说明](installation.md)
2. [配置说明](configuration.md)
3. [管理员指南](admin-guide.md)
4. [发布前外部配置](contributor-guide/publish-setup.md)
5. [CLI 发布手册](contributor-guide/release.md)

## 3. 当前目录是怎么组织的

为了让第一次接手的人也能快速定位，这一层按 4 组内容组织：

- 阅读与访问：
  面向“我只是要看文档”的读者。
- 本地开发与接入：
  面向“我要在本地改文档、预览、接入源仓”的执行者。
- 运维与发布：
  面向“我要审核同步、验证发布、处理线上问题”的维护者。
- 平台管理：
  面向“我要管理服务器、Secrets、GitHub App、PyPI 发布”的管理员。

## 4. 第一次接手仓库的 30 分钟阅读顺序

如果你第一次维护这个仓库，建议按下面顺序读：

1. [项目概览](../01-getting-started/project-overview.md)
2. [本地开发与预览](local-development.md)
3. [子仓库接入指南](usage.md)
4. [维护者指南](operator-guide.md)
5. [安装说明](installation.md)
6. [配置说明](configuration.md)

这样读的好处是：

- 先掌握“如何启动和看结果”
- 再掌握“文档怎么接进来”
- 最后再理解“平台如何发布和治理”

## 5. 什么时候应该跳过某页

- 你只想本地看改动：先读 [本地开发与预览](local-development.md)，不必先读 [安装说明](installation.md)。
- 你只想接入源仓：先读 [子仓库接入指南](usage.md)，不必先读管理员页。
- 你只想发 CLI：先读 [发布前外部配置](contributor-guide/publish-setup.md) 和 [CLI 发布手册](contributor-guide/release.md)。

## 6. 阅读这套指南时的判断标准

如果一页合格，你应当在 3 分钟内判断出：

- 这页是不是我现在该读的
- 我看完后下一步该执行什么命令或操作
- 操作成功时应该看到什么结果

如果你只是想解决眼前问题，不需要顺序读完整个 `02-user-guide/`。
