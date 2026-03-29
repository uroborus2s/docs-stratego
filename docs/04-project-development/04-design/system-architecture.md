# 系统架构

```mermaid
flowchart LR
  A["Source Repositories"] --> B["git submodule update --init"]
  B --> C["git fetch origin <branch>"]
  C --> D["git checkout -B <branch> FETCH_HEAD"]
  D --> E["sparse-checkout set /docs/ /docs/**"]
  E --> F["sources/<repo>/docs"]
  F --> G["read root docs/index.md"]
  G --> H[".generated/site_docs"]
  G --> I["permissions.json"]
  G --> J["private_locations.conf"]
  H --> K["mkdocs build"]
  K --> L["site/"]
  M["Casdoor"] --> N["oauth2-proxy"]
  J --> O["Nginx"]
  N --> O
  L --> O
```

## 组件职责

- `sync_sources.py`：更新子模块到目标分支，并在子模块内部只展开 `docs/`
- `build_site.py`：解析根 `docs/index.md` 的全站清单，生成导航、权限清单和 Nginx 规则
- `mkdocs build`：只负责把已整理好的文档树编译成静态站点
- `Casdoor`：提供用户名密码、GitHub 登录和用户管理
- `oauth2-proxy`：把 Casdoor 登录态转成 Nginx 可用的 `auth_request`
- `Nginx`：服务静态页面，并对私有页面路径发起认证请求
