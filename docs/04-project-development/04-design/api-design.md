# 接入契约

## 仓库注册契约

`config/source-repos.json` 使用以下结构：

```json
{
  "version": 3,
  "default_source_mode": "local",
  "repositories": [
    {
      "name": "crawler4j",
      "title": "蛛行演略",
      "repo_url": "https://github.com/uroborus2s/crawler4j",
      "modes": {
        "local": {
          "source_type": "local",
          "local_path": "../../PythonProject/crawler4j/docs"
        },
        "remote": {
          "source_type": "submodule_sparse",
          "git_url": "https://github.com/uroborus2s/crawler4j.git",
          "branch": "main",
          "submodule_path": "sources/crawler4j",
          "docs_path": "docs"
        }
      }
    }
  ]
}
```

字段语义：

- `default_source_mode`：默认使用 `local` 或 `remote`
- `modes.local.source_type=local`：读取本仓或同机目录
- `modes.remote.source_type=submodule_sparse`：通过 Git submodule 更新远程源仓
- `submodule_path`：源仓在根仓中的子模块路径
- `docs_path`：子模块里执行 sparse-checkout 后保留的文档根目录，当前标准固定为 `docs`

## 文档元数据契约

根 `docs/index.md` 必须包含：

- `title`
- `mkdocs.nav`
- 可选 `mkdocs.home_access`

其中：

- 目录节点使用 `title + children`
- 页面节点使用 `title + path + access`
- 页面权限只在页面节点上声明
- 页面节点的 `path` 目前允许三类文件：
  - `*.md`
  - `*.openapi.yaml|yml|json`
  - `*.mcp-tools.yaml|yml|json`

子目录 `index.md` 是普通页面，不再负责导航和权限。

## 契约渲染契约

当页面节点指向机器契约文件时，构建器会自动生成站内参考页：

- `foo.openapi.yaml` -> `foo.openapi.md`
- `bar.mcp-tools.yaml` -> `bar.mcp-tools.md`

其中：

- 渲染页进入 MkDocs 导航和页面 URL
- 原始 `.yaml/.json` 文件保留为可下载资源
- 页面节点声明的 `access` 同时作用于渲染页和原始契约文件

当前支持的机器契约：

- OpenAPI 3.x，站内使用 Scalar API Reference 渲染
- MCP tools 快照，站内生成静态工具参考页

## 构建产物契约

构建器会生成：

- `.generated/site_docs/`
- `.generated/mkdocs.generated.yml`
- `.generated/authz/permissions.json`
- `.generated/nginx/private_locations.conf`

其中 `.generated/site_docs/` 现在既包含源 Markdown 页面，也包含由 OpenAPI / Functions 文件自动生成的参考页。
