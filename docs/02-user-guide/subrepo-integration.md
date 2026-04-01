# 子仓库接入指南

本文面向子项目开发者，介绍如何按标准编写文档并将其接入到聚合站点中。

## 1. 接入流程概览

接入过程分为三个阶段：

1. **规范化准备**：按 [源文档标准](#2-源文档标准规范) 整理子仓 `docs/` 目录。
2. **根仓登记**：联系维护者在根仓配置子仓指针。
3. **启用联动**：在子仓配置 GitHub Actions，实现变更自动同步。

---

## 2. 源文档标准规范

子仓必须在根目录下提供一个 `docs/` 目录，并遵守以下核心规则：

### 2.1 目录结构建议
```text
docs/
  index.md           <-- 唯一导航与权限事实源 (必须)
  01-getting-started/
    index.md         <-- 该目录的正文首页
    quick-start.md
  openapi/           <-- OpenAPI 契约存放地
    index.md
    api-v1.openapi.yaml
```

### 2.2 核心导航配置 (`docs/index.md`)
根 `docs/index.md` 必须包含 YAML front matter，用于定义整个子仓的目录树和权限：

```md
---
title: 项目名称
mkdocs:
  home_access: public    # 首页是否公开 (public/private)
  nav:
    - title: 快速入门
      children:
        - title: 概览
          path: 01-getting-started/index.md
          access: public
    - title: API 参考
      children:
        - title: V1 接口
          path: openapi/api-v1.openapi.yaml
          access: private  # 私有页面需登录访问
---
# 项目简介正文
```

### 2.3 支持的内容类型
- **Markdown (`*.md`)**：普通正文页。
- **OpenAPI 契约 (`*.openapi.yaml/json`)**：自动渲染为交互式 API 文档。
- **MCP Tools 契约 (`*.mcp-tools.yaml/json`)**：自动渲染为工具参考页。

---

## 3. 根仓登记

在子仓代码准备就绪后，需要联系根仓维护者完成以下登记工作：

1. **更新 `config/source-repos.json`**：
   - 登记子仓的本地开发路径 (`modes.local`)。
   - 登记子仓的远程仓库地址及分支 (`modes.remote`)。
2. **注册 Git Submodule**：
   - 将子仓添加为根仓 `sources/` 目录下的子模块。

---

## 4. 启用自动同步 (GitHub 联动)

为了让子仓的变更能自动反映到聚合站点，请在子仓中完成以下配置：

### 4.1 添加 Workflow 文件
在子仓创建 `.github/workflows/notify-docs-stratego.yml`：

```yaml
name: Notify Docs Stratego

on:
  push:
    branches: [ main, master ]
    paths:
      - 'docs/**'  # 仅当文档变更时触发

jobs:
  notify:
    runs-on: ubuntu-latest
    steps:
      - name: Repository Dispatch
        uses: peter-evans/repository-dispatch@v3
        with:
          token: ${{ secrets.DOCS_STRATEGO_DISPATCH_TOKEN }}
          repository: uroborus2s/docs-stratego
          event-type: sync-source-pointers
          client-payload: '{"repo": "${{ github.repository }}", "ref": "${{ github.ref_name }}"}'
```

### 4.2 配置密钥
在子仓 `Settings -> Secrets and variables -> Actions` 中添加：
- **`DOCS_STRATEGO_DISPATCH_TOKEN`**：由根仓维护者提供的具有 `repo` 权限的 GitHub 个人访问令牌 (PAT) 或 GitHub App 令牌。

---

## 5. 接入验证

完成配置后，您可以通过以下方式验证：

1. **触发同步**：修改子仓 `docs/` 下的任意文件并推送。
2. **检查 PR**：前往根仓查看是否自动生成了名为 `chore: sync source repository pointers` 的 PR。
3. **预览结果**：在该 PR 的 `Validate Source Pointer PR` 工作流运行成功后，维护者合并 PR 即可在正式站点查看更新。

## 6. 常见问题 (FAQ)

- **为什么我的 API 契约没渲染？**
  确认契约文件后缀名为 `.openapi.yaml` 且已在 `docs/index.md` 的 `nav` 中声明。
- **私有页面匿名可见？**
  检查 `docs/index.md` 中的 `access: private` 是否配置正确。
- **自动同步没触发？**
  确认子仓的 Secret 名称拼写正确，且变更发生在 `docs/` 目录下。
