---
title: 章略·墨衡
mkdocs:
  home_access: public
  nav:
    - title: 入门说明
      children:
        - title: 概览
          path: 01-getting-started/index.md
          access: public
        - title: 项目概览
          path: 01-getting-started/project-overview.md
          access: public
        - title: 快速开始
          path: 01-getting-started/quick-start.md
          access: public
        - title: 文档地图
          path: 01-getting-started/document-map.md
          access: public
    - title: 用户指南
      children:
        - title: 概览
          path: 02-user-guide/index.md
          access: public
        - title: 阅读者指南
          path: 02-user-guide/reader-guide.md
          access: public
        - title: 维护者指南
          path: 02-user-guide/operator-guide.md
          access: public
        - title: 子仓库接入指南
          path: 02-user-guide/usage.md
          access: public
        - title: 安装说明
          path: 02-user-guide/installation.md
          access: public
        - title: 配置说明
          path: 02-user-guide/configuration.md
          access: public
        - title: 管理员指南
          path: 02-user-guide/admin-guide.md
          access: public
    - title: 项目开发文档（内）
      children:
        - title: 概览
          path: 04-project-development/index.md
          access: private
        - title: 项目治理
          children:
            - title: 概览
              path: 04-project-development/01-governance/index.md
              access: private
            - title: 项目章程
              path: 04-project-development/01-governance/project-charter.md
              access: private
        - title: 调研与决策
          children:
            - title: 概览
              path: 04-project-development/02-discovery/index.md
              access: private
            - title: 输入背景
              path: 04-project-development/02-discovery/input.md
              access: private
            - title: 头脑风暴记录
              path: 04-project-development/02-discovery/brainstorm-record.md
              access: private
        - title: 需求
          children:
            - title: 概览
              path: 04-project-development/03-requirements/index.md
              access: private
            - title: 产品需求文档
              path: 04-project-development/03-requirements/prd.md
              access: private
            - title: 需求分析
              path: 04-project-development/03-requirements/requirements-analysis.md
              access: private
            - title: 需求一致性校验
              path: 04-project-development/03-requirements/requirements-verification.md
              access: private
            - title: 需求变更日志
              path: 04-project-development/03-requirements/changelog.md
              access: private
        - title: 设计文档
          children:
            - title: 概览
              path: 04-project-development/04-design/index.md
              access: private
            - title: 技术选型与工程规则
              path: 04-project-development/04-design/technical-selection.md
              access: private
            - title: 系统架构
              path: 04-project-development/04-design/system-architecture.md
              access: private
            - title: 模块边界
              path: 04-project-development/04-design/module-boundaries.md
              access: private
            - title: 接入契约
              path: 04-project-development/04-design/api-design.md
              access: private
            - title: 认证与权限服务设计
              path: 04-project-development/04-design/backend-design.md
              access: private
            - title: 认证数据存储设计
              path: 04-project-development/04-design/database-design.md
              access: private
            - title: 部署与 CI/CD 设计
              path: 04-project-development/04-design/deployment-architecture.md
              access: private
            - title: UI 与信息架构
              path: 04-project-development/04-design/ux-ui-design.md
              access: private
            - title: OpenAPI 契约
              children:
                - title: 概览
                  path: 04-project-development/04-design/openapi/index.md
                  access: private
                - title: Scalar 渲染示例
                  path: 04-project-development/04-design/openapi/docs-rendering-example.openapi.yaml
                  access: private
            - title: 工具契约（MCP）
              children:
                - title: 概览
                  path: 04-project-development/04-design/tools/index.md
                  access: private
                - title: 站点构建工具目录
                  path: 04-project-development/04-design/tools/site-builder.mcp-tools.yaml
                  access: private
            - title: crawler4j 接入包
              path: 04-project-development/04-design/crawler4j-integration-package.md
              access: private
            - title: 源文档标准
              path: 04-project-development/04-design/source-docs-standard.md
              access: private
        - title: 开发过程文档
          children:
            - title: 概览
              path: 04-project-development/05-development-process/index.md
              access: private
            - title: 软件开发流程
              path: 04-project-development/05-development-process/software-development-process.md
              access: private
            - title: 工作分解结构
              path: 04-project-development/05-development-process/wbs.md
              access: private
            - title: 实施计划
              path: 04-project-development/05-development-process/implementation-plan.md
              access: private
            - title: 任务分解文档
              path: 04-project-development/05-development-process/task-breakdown.md
              access: private
        - title: 测试与验证
          children:
            - title: 概览
              path: 04-project-development/06-testing-verification/index.md
              access: private
            - title: 测试计划
              path: 04-project-development/06-testing-verification/test-plan.md
              access: private
            - title: 测试用例
              path: 04-project-development/06-testing-verification/test-cases.md
              access: private
            - title: 测试报告
              path: 04-project-development/06-testing-verification/test-report.md
              access: private
        - title: 发布与交付
          children:
            - title: 概览
              path: 04-project-development/07-release-delivery/index.md
              access: private
            - title: 验收清单
              path: 04-project-development/07-release-delivery/acceptance-checklist.md
              access: private
            - title: 交付文档
              path: 04-project-development/07-release-delivery/delivery-package.md
              access: private
            - title: 发布说明
              path: 04-project-development/07-release-delivery/release-notes.md
              access: private
        - title: 运维与维护
          children:
            - title: 概览
              path: 04-project-development/08-operations-maintenance/index.md
              access: private
            - title: 部署手册
              path: 04-project-development/08-operations-maintenance/deployment-guide.md
              access: private
            - title: 运维手册
              path: 04-project-development/08-operations-maintenance/operations-runbook.md
              access: private
            - title: 服务器部署 SOP
              path: 04-project-development/08-operations-maintenance/server-deployment-sop.md
              access: private
        - title: 演进复盘
          children:
            - title: 概览
              path: 04-project-development/09-evolution/index.md
              access: private
            - title: Skill 进化方案
              path: 04-project-development/09-evolution/skill-evolution-plan.md
              access: private
            - title: 项目复盘
              path: 04-project-development/09-evolution/retrospective.md
              access: private
        - title: 追踪矩阵
          children:
            - title: 概览
              path: 04-project-development/10-traceability/index.md
              access: private
            - title: 需求追踪矩阵
              path: 04-project-development/10-traceability/requirements-matrix.md
              access: private
            - title: 接口追踪矩阵
              path: 04-project-development/10-traceability/interface-matrix.md
              access: private
            - title: 文档索引
              path: 04-project-development/10-traceability/document-index.md
              access: private
---

# 章略·墨衡

这是 `docs-stratego` 的正式项目文档源。当前 `docs_profile` 启用了三个顶层模块：入门说明、用户指南、项目开发文档（内）。`开发者指南` 暂不单独启用，待项目形成稳定 SDK、公共 API 或插件扩展面后再补齐。

当前模式下：

- 只有根 `docs/index.md` 负责整站目录树
- 页面权限只写在这个文件的页面节点里
- 子目录 `index.md` 只作为对应目录的正文首页

## 你应该先看什么

1. [项目概览](01-getting-started/project-overview.md)
2. [管理员指南](02-user-guide/admin-guide.md)
3. [源文档标准](04-project-development/04-design/source-docs-standard.md)
4. [部署与 CI/CD 设计](04-project-development/04-design/deployment-architecture.md)
5. [部署手册](04-project-development/08-operations-maintenance/deployment-guide.md)
