# 输入背景

## 项目基础信息

- 项目名称：章略·墨衡
- 根仓目录：`docs-stratego`
- 负责人：uroborus
- 目标形态：单个静态文档站点 + 页面级登录保护 + Agent 可消费索引

## 原始构想摘要

用户提出将多个项目文档集合与知识库集中维护在一个根仓中，并要求源仓自己维护 `docs/` 的目录、导航和页面私有化规则。根仓只负责稀疏同步 `docs/`、生成导航与权限清单、构建 MkDocs 静态站点，并通过认证网关实现“左侧目录可见、点击私有页才登录”的体验。

## 本次初始化采用的修正方向

- 保留“多仓聚合、文档随代码走、Agent 联动”这些核心目标。
- 放弃旧版 `00-brainstorm / 01-requirements / 02-design / 03-plan / 04-testing / 05-acceptance` 目录命名。
- 统一改为最新生命周期结构：`00-governance` 到 `09-evolution`。
- 采用单站点 + 页面级登录方案，私有化规则由根 `docs/index.md` 的页面节点统一声明。
- 根仓通过 `git clone --filter=blob:none --no-checkout` + `sparse-checkout set docs` 只同步外部仓库文档目录。
- 匿名全文搜索默认关闭，避免私有页面标题、正文和摘要泄露。

## 目标读者

- 文档平台建设者
- 接入项目负责人
- 构建与部署维护者
- Agent 协作者
