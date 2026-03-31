# 源文档标准

本文是外部源仓必须遵守的正式标准。当前模式下，聚合站点以源仓根 `docs/index.md` 为唯一导航与权限事实源，同时支持将 OpenAPI 契约通过 Scalar 渲染为专业 API 文档，并将 MCP tools 快照渲染为静态工具参考页。

## 1. 目标与边界

本标准同时约束三类内容：

- 人类阅读页面：Markdown 正文页、目录概览页、设计说明页
- 机器可消费契约：OpenAPI、MCP tools 快照
- 文档站加载规则：导航、权限、页面 URL、原始契约下载地址与渲染方式

不变原则：

- 源仓自己维护目录、顺序和权限
- 根仓只负责读取、校验、渲染和聚合展示
- 目录树只来自根 `docs/index.md`
- 页面权限只来自根 `docs/index.md` 的页面节点 `access`
- 子目录 `index.md` 只做正文首页，不再声明导航

## 2. 目录标准

源仓至少提供一个文档根目录，默认是 `docs/`。

推荐结构：

```text
docs/
  index.md
  03-developer-guide/
    index.md
    interface-reference.md
    openapi/
      index.md
      public-v1.openapi.yaml
    tools/
      index.md
      public-agent.mcp-tools.json
  04-project-development/
    index.md
    04-design/
      index.md
      api-design.md
      subsystems/
        gateway/
          index.md
          subsystem-overview.md
          openapi/
            index.md
            app.openapi.yaml
            partner.openapi.yaml
          tools/
            index.md
            gateway-runtime.mcp-tools.yaml
```

规则：

- 每个真实内容目录都必须保留自己的 `index.md`
- 每个 Markdown 页面都必须有一级标题 `# 标题`
- 根 `docs/index.md` 是唯一的导航清单文件
- `assets/` 只能放资源文件，不能放 Markdown 页面或契约文件
- 契约文件必须放在真实文档目录下，不能藏在 `assets/`
- 契约文件不能脱离说明页单独存在；至少要与所在目录的 `index.md` 配套

推荐按读者和阶段放置：

- 对外稳定接口与扩展能力：`03-developer-guide/openapi/`、`03-developer-guide/tools/`
- 内部设计期契约：`04-project-development/04-design/**/openapi/`、`04-project-development/04-design/**/tools/`

对于“多子系统、多服务、多端”项目，推荐再按子系统拆一层目录，例如：

- `04-design/subsystems/gateway/openapi/app.openapi.yaml`
- `04-design/subsystems/order-service/openapi/order-public.openapi.yaml`
- `04-design/subsystems/gateway/tools/gateway-runtime.mcp-tools.yaml`

`external/`、`internal/` 可以作为目录命名约定使用，但它们不参与权限判断。是否公开，只看根 `docs/index.md` 中对应页面节点的 `access`。

## 3. 根 `docs/index.md` 标准

根 `docs/index.md` 使用 YAML front matter，在一个文件里声明整个项目的目录树、页面路径和页面权限。

### 3.1 数据结构

- `title`: 项目标题
- `mkdocs.home_access`: 根首页权限，取值为 `public` 或 `private`
- `mkdocs.nav`: 全站目录树
- 目录节点只允许：
  - `title`
  - `children`
- 页面节点只允许：
  - `title`
  - `path`
  - `access`
- 页面权限只写在页面节点，目录节点不写权限

### 3.2 页面节点支持的文件类型

页面节点的 `path` 目前只允许指向以下三类文件：

- Markdown 页面：`*.md`
- OpenAPI 契约：`*.openapi.yaml`、`*.openapi.yml`、`*.openapi.json`
- MCP tools 快照：`*.mcp-tools.yaml`、`*.mcp-tools.yml`、`*.mcp-tools.json`

含义如下：

- `*.md`：按普通正文页加载
- `*.openapi.*`：构建器自动生成一页 Scalar API Reference 包装页，同时保留原始契约下载地址
- `*.mcp-tools.*`：构建器自动生成一页 MCP tools 静态参考页，同时保留原始快照下载地址

### 3.3 完整模板

```md
---
title: 蛛行演略
mkdocs:
  home_access: public
  nav:
    - title: 开发者指南
      children:
        - title: 概览
          path: 03-developer-guide/index.md
          access: public
        - title: OpenAPI 契约
          children:
            - title: 概览
              path: 03-developer-guide/openapi/index.md
              access: public
            - title: Public API v1
              path: 03-developer-guide/openapi/public-v1.openapi.yaml
              access: public
        - title: 工具契约（MCP）
          children:
            - title: 概览
              path: 03-developer-guide/tools/index.md
              access: public
            - title: Public Agent Tools
              path: 03-developer-guide/tools/public-agent.mcp-tools.json
              access: public

    - title: 项目开发文档（内）
      children:
        - title: 概览
          path: 04-project-development/index.md
          access: private
        - title: 子系统设计
          children:
            - title: Gateway
              children:
                - title: 概览
                  path: 04-project-development/04-design/subsystems/gateway/index.md
                  access: private
                - title: Gateway OpenAPI
                  children:
                    - title: 概览
                      path: 04-project-development/04-design/subsystems/gateway/openapi/index.md
                      access: private
                    - title: App API
                      path: 04-project-development/04-design/subsystems/gateway/openapi/app.openapi.yaml
                      access: public
                - title: Gateway Tools
                  children:
                    - title: 概览
                      path: 04-project-development/04-design/subsystems/gateway/tools/index.md
                      access: private
                    - title: Runtime Tools
                      path: 04-project-development/04-design/subsystems/gateway/tools/gateway-runtime.mcp-tools.yaml
                      access: private
---
# 蛛行演略
```

## 4. 页面路径与权限规则

- 目录树只来自根 `docs/index.md` 的 `mkdocs.nav`
- `children` 可以继续嵌套，表示目录和二级目录
- `path` 统一写相对根 `docs/` 的路径
- 不允许在 `path` 中使用 `../`
- 不允许把 `assets/` 下的文件写成页面路径
- 权限只写在页面节点上，取值只允许 `public` 或 `private`
- 根首页权限由 `mkdocs.home_access` 决定
- 私有页面会保留在同一套左侧目录中，但访问时进入登录链路

契约文件的权限规则与普通页面完全一致：

- 页面节点声明的权限同时作用于“渲染后的参考页”和“原始契约文件下载地址”
- 目录名、文件名、子系统名都不参与权限判断
- `external/`、`internal/` 只是目录组织语义，不是权限事实源

## 5. OpenAPI 契约标准

适用场景：

- 外部 REST API
- 内部 HTTP 服务接口
- 多端分流接口，如 Web、App、小程序、后台
- 多版本或多服务并行维护的 API 契约

文件命名：

- 推荐：`{domain|channel|service}[.v{major}].openapi.yaml`
- 允许：`.yaml`、`.yml`、`.json`

最低要求：

- 声明 `openapi: 3.x`
- 声明 `info.title`
- 声明 `info.version`

推荐要求：

- 使用 `tags`
- 所有操作都写 `operationId`
- 复杂响应尽量放到 `components.schemas`
- 设计期契约要和 `api-design.md`、端规格文档、数据库设计保持一致

组织原则：

- 一个文件代表一份可独立联调、独立评审、独立渲染的 API 契约
- 多端项目按“调用方/端形态”拆分比按资源粗暴合并更实用
- 多服务项目按“服务边界”拆分比按团队拆分更稳定
- 同一子系统下可以再按公开面、版本或渠道拆分目录，但权限仍由根导航决定

渲染规则：

- `foo.openapi.yaml` -> 构建器生成 `foo.openapi.md`
- 该生成页在站内嵌入 Scalar API Reference
- 原始 `foo.openapi.yaml` 继续保留并可下载

## 6. 工具契约（MCP）标准

适用场景：

- MCP tools
- Agent 可调用工具
- CLI / 脚本 / 自动化入口，只要适合以 JSON Schema 描述输入输出

文件命名：

- 推荐：`{domain|runtime|channel}.mcp-tools.yaml`
- 允许：`.yaml`、`.yml`、`.json`

内容模型：

- 使用 MCP tools 数据模型
- 顶层推荐直接写 `tools` 数组
- 若导出的是完整 `tools/list` 响应，也允许写成 `{ result: { tools: [...] } }`

示例：

```yaml
tools:
  - name: build_site
    title: 构建聚合文档站
    description: 生成站点文档树、权限清单与 Nginx 私有规则。
    annotations:
      readOnlyHint: false
      destructiveHint: false
      idempotentHint: true
      openWorldHint: false
    inputSchema:
      type: object
      required: [config, output_dir]
      properties:
        config:
          type: string
        output_dir:
          type: string
    outputSchema:
      type: object
      properties:
        docsDir:
          type: string
```

最低要求：

- 非空 `tools` 列表
- 每个工具至少声明：
  - `name`
  - `description`
  - `inputSchema`

推荐补齐：

- `title`
- `outputSchema`
- `annotations`

渲染规则：

- `foo.mcp-tools.yaml` -> 构建器生成 `foo.mcp-tools.md`
- 站内展示静态工具参考页
- 原始快照文件继续保留并可下载
- 交互调试由 MCP Inspector 承担，不在文档站内解决

## 7. 子目录 `index.md` 的职责

子目录 `index.md` 仍然必须存在，但职责已经变成：

- 作为该目录的正文首页
- 提供目录介绍、边界说明和上下文
- 作为资源文件权限继承的锚点页面
- 对契约目录说明“这组契约解决什么问题、给谁看、如何拆分”

它不再负责：

- 声明 `mkdocs.nav`
- 决定左侧目录树
- 决定其他页面的权限
- 重复抄写本目录下的完整页面清单

## 8. 多子系统项目的推荐组织方式

如果仓库里包含多个子系统，推荐采用：

- 全局总览页：说明整体接口版图、统一规则、子系统归属
- 子系统目录：每个子系统各自维护 `index.md`
- 子系统下再拆 `openapi/` 和 `tools/`
- 每个契约目录都保留自己的 `index.md`

推荐结构：

```text
04-design/
  api-design.md
  subsystems/
    gateway/
      index.md
      openapi/
        index.md
        app.openapi.yaml
      tools/
        index.md
        gateway-runtime.mcp-tools.yaml
    order-service/
      index.md
      openapi/
        index.md
        order-public.openapi.yaml
```

这样做的目的不是增加层级，而是确保：

- 每个契约都有 owner
- 每组契约都有说明页
- 导航、权限、原始文件下载和渲染页能稳定对应

## 9. 根 `docs/index.md` 正文要求

根 `docs/index.md` 只允许承担首页正文职责，不允许再手写第二套目录结构。

允许写：

- 项目简介
- 文档范围边界
- 面向读者说明
- 维护规则

不允许写：

- 目录树镜像
- 章节顺序清单
- 和 `mkdocs.nav` 重复的链接列表
- 人工维护的“推荐阅读顺序”目录

## 10. 构建器实际读取什么

要构建出目录树、页面 URL、权限和契约渲染页，构建器只需要：

1. 根 `docs/index.md` 的 front matter
2. 文件系统，校验 `path` 指向的 Markdown 或契约文件是否存在
3. Markdown 页面自身的一级标题
4. 契约文件自身的最小结构：
   - OpenAPI：`openapi`、`info.title`、`info.version`
   - MCP tools：`tools[]` 或 `result.tools[]`

换句话说：

- 左侧目录树来自根 `docs/index.md`
- 页面 URL 来自根 `docs/index.md` 的 `path` 与契约渲染规则
- 页面权限来自根 `docs/index.md` 的 `access`
- 子目录 `index.md` 只参与站点内容，不参与导航生成
- 原始契约文件和渲染页共享同一套访问控制规则
