# 源文档标准

这是源仓接入 `docs-stratego` 的公开标准事实源。你只要让自己的 `docs/` 满足这里的规则，聚合站点就能稳定读取、校验、构建和控制访问权限。

## 1. 先记住这三个原则

1. 源仓自己维护目录、顺序和权限。
2. 根仓只负责读取、校验、聚合和发布，不反向改写源仓文档。
3. 根 `docs/index.md` 是唯一导航与权限事实源。

## 2. 最小合规目录

一个最小可接入的源仓至少要有：

```text
docs/
  index.md
  01-getting-started/
    index.md
```

如果你要接 OpenAPI 或 MCP tools 契约，推荐结构如下：

```text
docs/
  index.md
  03-developer-guide/
    index.md
    openapi/
      index.md
      public-v1.openapi.yaml
    tools/
      index.md
      public-agent.mcp-tools.yaml
```

## 3. 根 `docs/index.md` 怎么写

根 `docs/index.md` 必须同时承担两件事：

- 首页正文
- 全站导航与权限清单

它必须包含 YAML front matter：

```md
---
title: 项目名称
mkdocs:
  home_access: public
  nav:
    - title: 快速开始
      children:
        - title: 概览
          path: 01-getting-started/index.md
          access: public
    - title: API 参考
      children:
        - title: Public API v1
          path: 03-developer-guide/openapi/public-v1.openapi.yaml
          access: private
---
# 项目名称
```

字段规则：

- `title`：项目标题。
- `mkdocs.home_access`：首页权限，只允许 `public` 或 `private`。
- `mkdocs.nav`：整棵目录树。
- 页面节点只允许 `title`、`path`、`access`。
- 目录节点只允许 `title`、`children`。

## 4. 页面与目录的硬规则

- 每个真实内容目录都必须保留自己的 `index.md`。
- 每个 Markdown 页面都必须有一级标题 `# 标题`。
- 页面路径只能写相对根 `docs/` 的路径。
- `path` 中不允许出现 `../`。
- `assets/` 只能放资源文件，不能放 Markdown 页面或契约文件。
- 权限只写在页面节点里，不写在目录节点里。

## 5. 支持的内容类型

### Markdown 页面

- 后缀：`*.md`
- 用途：普通正文页、说明页、目录首页

### OpenAPI 契约

- 后缀：`*.openapi.yaml`、`*.openapi.yml`、`*.openapi.json`
- 作用：构建器会生成对应的 Scalar API Reference 页面
- 最低要求：
  - `openapi: 3.x`
  - `info.title`
  - `info.version`

### MCP tools 快照

- 后缀：`*.mcp-tools.yaml`、`*.mcp-tools.yml`、`*.mcp-tools.json`
- 作用：构建器会生成静态工具参考页
- 最低要求：
  - 顶层 `tools` 数组，或 `{ result: { tools: [...] } }`
  - 每个工具至少有 `name`、`description`、`inputSchema`

## 6. 权限怎么判断

只看根 `docs/index.md` 页面节点里的 `access`。

这几个信息都不参与权限判断：

- 目录名是不是 `internal/` 或 `external/`
- 文件名里有没有 `private`
- 子目录 `index.md` 里写了什么正文

## 7. 子目录 `index.md` 的职责

子目录 `index.md` 还必须存在，但它现在只做正文首页：

- 解释这一组文档解决什么问题
- 说明适合哪些读者
- 为本目录下的契约或资源补上下文

它不再负责：

- 声明 `mkdocs.nav`
- 决定目录顺序
- 决定页面权限

## 8. 交付前自检

接入前，至少确认下面这些项：

- [ ] 根 `docs/index.md` 存在，且 front matter 合法。
- [ ] 所有声明到 `mkdocs.nav` 的页面文件都真实存在。
- [ ] 所有实际内容目录都有 `index.md`。
- [ ] 契约文件不放在 `assets/` 下。
- [ ] 私有页面只通过页面节点 `access: private` 声明。
- [ ] 在源仓目录执行 `uvx --from 'docs-stratego==<version>' docs-stratego source validate` 能通过。

下一步请读 [接入聚合站点](onboarding.md)。
