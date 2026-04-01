# 站点构建工具目录

> 本页基于 MCP tools 快照渲染，源文件为 `04-project-development/04-design/tools/site-builder.mcp-tools.yaml`

<p class="docs-contract-note">MCP 目前没有像 Swagger UI 那样成熟的通用文档 UI；本页提供静态参考，交互调试建议使用 MCP Inspector。</p>

<div class="docs-contract-meta">
<span class="docs-contract-pill">2 tools</span>
<a class="docs-contract-pill" href="site-builder.mcp-tools.yaml">下载原始快照</a>
<a class="docs-contract-pill" href="https://modelcontextprotocol.io/docs/tools/inspector" target="_blank" rel="noreferrer">MCP Inspector</a>
</div>

## 工具总览

| 名称 | 标题 | 输入 | 说明 |
| --- | --- | --- | --- |
| sync_sources | 同步源仓文档 | object; fields: config, source_mode; required: config | 同步源仓文档目录到聚合工作区。 |
| build_site | 构建聚合文档站 | object; fields: config, output_dir; required: config, output_dir | 生成站点文档树、权限清单与 Nginx 私有规则。 |

### `sync_sources`

同步源仓文档目录到聚合工作区。

| 字段 | 值 |
| --- | --- |
| 标题 | 同步源仓文档 |
| 输入 Schema | object; fields: config, source_mode; required: config |
| 输出 Schema | object; fields: syncedRepositories, docsRoots |

Annotations

| 字段 | 值 |
| --- | --- |
| readOnlyHint | False |
| destructiveHint | False |
| idempotentHint | False |
| openWorldHint | False |

输入 Schema

```json
{
  "type": "object",
  "required": [
    "config"
  ],
  "properties": {
    "config": {
      "type": "string",
      "description": "源仓配置文件路径"
    },
    "source_mode": {
      "type": "string",
      "enum": [
        "local",
        "remote"
      ],
      "description": "文档源模式"
    }
  }
}
```

输出 Schema

```json
{
  "type": "object",
  "properties": {
    "syncedRepositories": {
      "type": "integer"
    },
    "docsRoots": {
      "type": "array",
      "items": {
        "type": "string"
      }
    }
  }
}
```

### `build_site`

生成站点文档树、权限清单与 Nginx 私有规则。

| 字段 | 值 |
| --- | --- |
| 标题 | 构建聚合文档站 |
| 输入 Schema | object; fields: config, output_dir; required: config, output_dir |
| 输出 Schema | object; fields: docsDir, mkdocsConfig, permissionsFile, privateLocationsFile |

Annotations

| 字段 | 值 |
| --- | --- |
| readOnlyHint | False |
| destructiveHint | False |
| idempotentHint | True |
| openWorldHint | False |

输入 Schema

```json
{
  "type": "object",
  "required": [
    "config",
    "output_dir"
  ],
  "properties": {
    "config": {
      "type": "string",
      "description": "源仓配置文件路径"
    },
    "output_dir": {
      "type": "string",
      "description": "构建输出目录"
    }
  }
}
```

输出 Schema

```json
{
  "type": "object",
  "properties": {
    "docsDir": {
      "type": "string"
    },
    "mkdocsConfig": {
      "type": "string"
    },
    "permissionsFile": {
      "type": "string"
    },
    "privateLocationsFile": {
      "type": "string"
    }
  }
}
```

<details>
<summary>原始 MCP tools 快照</summary>

```yaml
tools:
  - name: sync_sources
    title: 同步源仓文档
    description: 同步源仓文档目录到聚合工作区。
    annotations:
      readOnlyHint: false
      destructiveHint: false
      idempotentHint: false
      openWorldHint: false
    inputSchema:
      type: object
      required: [config]
      properties:
        config:
          type: string
          description: 源仓配置文件路径
        source_mode:
          type: string
          enum: [local, remote]
          description: 文档源模式
    outputSchema:
      type: object
      properties:
        syncedRepositories:
          type: integer
        docsRoots:
          type: array
          items:
            type: string
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
          description: 源仓配置文件路径
        output_dir:
          type: string
          description: 构建输出目录
    outputSchema:
      type: object
      properties:
        docsDir:
          type: string
        mkdocsConfig:
          type: string
        permissionsFile:
          type: string
        privateLocationsFile:
          type: string
```

</details>
